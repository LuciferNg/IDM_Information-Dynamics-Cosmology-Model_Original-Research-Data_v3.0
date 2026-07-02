#!/usr/bin/env python3
"""
IDM Batch Hallucination Pipeline v1.0
======================================
批量餵 prompt 俾本地模型 → 收集 output → IDM consistency verify → 出 hallucination report.

Usage:
  # 基本用法：用預設模型 qwen3.5:9b 測試 prompts.txt
  python3 idm_hal_pipeline.py prompts.txt

  # 指定模型 + system prompt kernel
  python3 idm_hal_pipeline.py prompts.txt --model qwen2.5-coder:32b --kernel

  # 用 JSON 格式嘅 prompts（每個 item 有 id, prompt, expected）
  python3 idm_hal_pipeline.py prompts.json --json

  # 只 verify 已有 output，唔 call model
  python3 idm_hal_pipeline.py --verify-only outputs.json

  # 輸出手機友好嘅 HTML report
  python3 idm_hal_pipeline.py prompts.txt --html

  # 比較兩個模型嘅 hallucination rate
  python3 idm_hal_pipeline.py prompts.txt --model qwen3.5:9b --model qwen2.5-coder:32b
"""

import json
import re
import sys
import time
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

# ── 引入 IDM Verifier ──
sys.path.insert(0, str(Path(__file__).parent))
from idm_consistency_verifier import IDMVerifier


# ═══════════════════════════════════════════════════════════════
# Config
# ═══════════════════════════════════════════════════════════════

# 預設直達 Windows Ollama（用 ip route 自動 detect）
import subprocess


def detect_ollama_host() -> str:
    """Detect Ollama host (Windows from WSL or local)."""
    # Try localhost first
    for host in ["http://localhost:11434", "http://127.0.0.1:11434"]:
        try:
            req = urllib.request.Request(f"{host}/api/tags", method="GET")
            urllib.request.urlopen(req, timeout=2)
            return host
        except Exception:
            pass
    # Try Windows IP from WSL `ip route`
    try:
        result = subprocess.run(
            ["ip", "route"],
            capture_output=True, text=True, timeout=5
        )
        for line in result.stdout.splitlines():
            if "default" in line:
                # Format: "default via 172.26.176.1 dev eth0"
                parts = line.split()
                if "via" in parts:
                    via_idx = parts.index("via")
                    if via_idx + 1 < len(parts):
                        win_ip = parts[via_idx + 1]
                        return f"http://{win_ip}:11434"
    except Exception:
        pass
    return "http://localhost:11434"


OLLAMA_HOST = detect_ollama_host()
print(f"🔗 Ollama host: {OLLAMA_HOST}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════
# Data Structures
# ═══════════════════════════════════════════════════════════════

@dataclass
class PromptItem:
    id: str
    prompt: str
    expected: str = ""
    category: str = "general"
    system_prompt: str = ""

@dataclass
class ModelOutput:
    id: str
    prompt: str
    model: str
    output: str
    latency_ms: float
    violations: list = field(default_factory=list)
    hallucination: bool = False
    severity: str = "none"
    timestamp: str = ""

@dataclass
class PipelineReport:
    model: str
    total: int
    hallucinated: int
    hallucination_rate: float
    critical: int
    high: int
    medium: int
    low: int
    by_category: dict = field(default_factory=dict)
    outputs: list = field(default_factory=list)
    timestamp: str = ""


# ═══════════════════════════════════════════════════════════════
# Ollama API
# ═══════════════════════════════════════════════════════════════

def ollama_generate(model: str, prompt: str, system: str = "",
                    temperature: float = 0.7, max_tokens: int = 2048) -> dict:
    """Call Ollama generate API. Returns {output, latency_ms, error?}."""
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "system": system,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False,
        "options": {"num_ctx": 8192},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:  # 5 min 超時
            result = json.loads(resp.read().decode("utf-8"))
        latency = (time.time() - start) * 1000
        return {
            "output": result.get("response", ""),
            "latency_ms": round(latency, 1),
        }
    except urllib.error.HTTPError as e:
        return {
            "output": "",
            "latency_ms": 0,
            "error": f"HTTP {e.code}: {e.read().decode()[:200]}",
        }
    except Exception as e:
        return {
            "output": "",
            "latency_ms": 0,
            "error": str(e),
        }


# ═══════════════════════════════════════════════════════════════
# Prompt Loaders
# ═══════════════════════════════════════════════════════════════

def load_prompts(path: str, is_json: bool = False) -> list:
    """Load prompts from file. Supports TXT (one prompt per line) and JSON."""
    content = Path(path).read_text(encoding="utf-8")

    if is_json or path.endswith(".json"):
        data = json.loads(content)
        if isinstance(data, list):
            return [
                PromptItem(
                    id=item.get("id", f"p{i+1}"),
                    prompt=item.get("prompt", item.get("text", "")),
                    expected=item.get("expected", ""),
                    category=item.get("category", "general"),
                )
                for i, item in enumerate(data)
            ]
        return []

    # TXT: prompt per line, skip empty lines and comments
    prompts = []
    for i, line in enumerate(content.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        prompts.append(PromptItem(id=f"p{i}", prompt=line))
    return prompts


# ═══════════════════════════════════════════════════════════════
# Core Pipeline
# ═══════════════════════════════════════════════════════════════

def run_pipeline(prompts: list, model: str, system_prompt: str = "",
                 temperature: float = 0.7, max_tokens: int = 2048,
                 show_progress: bool = True) -> PipelineReport:
    """Run the full pipeline: prompt → model → verify → report."""
    verifier = IDMVerifier(strict=True)
    outputs = []
    total = len(prompts)
    hallucinated = 0
    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    by_category = {}

    for idx, item in enumerate(prompts):
        if show_progress:
            print(f"  [{idx+1}/{total}] {item.id}... ", end="", file=sys.stderr)
            sys.stderr.flush()

        # 1. Call model
        sp = item.system_prompt or system_prompt
        result = ollama_generate(
            model=model,
            prompt=item.prompt,
            system=sp,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        if "error" in result:
            if show_progress:
                print(f"❌ {result['error']}", file=sys.stderr)
            outputs.append(ModelOutput(
                id=item.id, prompt=item.prompt, model=model,
                output=f"[ERROR] {result['error']}",
                latency_ms=result.get("latency_ms", 0),
                violations=[{"severity": "error", "message": result["error"]}],
                hallucination=True, severity="error",
                timestamp=datetime.now().isoformat(),
            ))
            continue

        output_text = result["output"]

        # 2. Verify
        report = verifier.check(output_text, source=item.id)
        violations = report["violations"]
        is_hallucination = not report["pass"]

        # 3. Determine severity
        sev = "none"
        if is_hallucination:
            if report["stats"]["critical"] > 0:
                sev = "critical"
            elif report["stats"]["high"] > 0:
                sev = "high"
            elif report["stats"]["medium"] > 0:
                sev = "medium"
            elif report["stats"]["low"] > 0:
                sev = "low"

        if is_hallucination:
            hallucinated += 1
            if sev in severity_counts:
                severity_counts[sev] += 1

        # 4. Category tracking
        cat = item.category
        if cat not in by_category:
            by_category[cat] = {"total": 0, "hallucinated": 0}
        by_category[cat]["total"] += 1
        if is_hallucination:
            by_category[cat]["hallucinated"] += 1

        mo = ModelOutput(
            id=item.id, prompt=item.prompt, model=model,
            output=output_text,
            latency_ms=result["latency_ms"],
            violations=violations,
            hallucination=is_hallucination,
            severity=sev,
            timestamp=datetime.now().isoformat(),
        )
        outputs.append(mo)

        if show_progress:
            icon = "🔴" if is_hallucination else "✅"
            score = f"{sev}" if is_hallucination else "pass"
            print(f"{icon} {score} ({result['latency_ms']:.0f}ms)", file=sys.stderr)

    rate = (hallucinated / total * 100) if total > 0 else 0.0
    return PipelineReport(
        model=model,
        total=total,
        hallucinated=hallucinated,
        hallucination_rate=round(rate, 1),
        critical=severity_counts["critical"],
        high=severity_counts["high"],
        medium=severity_counts["medium"],
        low=severity_counts["low"],
        by_category=by_category,
        outputs=outputs,
        timestamp=datetime.now().isoformat(),
    )


# ═══════════════════════════════════════════════════════════════
# Reporting
# ═══════════════════════════════════════════════════════════════

def print_report(report: PipelineReport, verbose: bool = False):
    """Print text report to stdout."""
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"  IDM Hallucination Report — {report.model}")
    print(f"  {report.timestamp}")
    print(sep)
    print(f"  總計: {report.total} prompts")
    print(f"  幻覺: {report.hallucinated}/{report.total} ({report.hallucination_rate}%)")
    print(f"  嚴重度分布:")
    print(f"    🔴 Critical: {report.critical}")
    print(f"    🟠 High:     {report.high}")
    print(f"    🟡 Medium:   {report.medium}")
    print(f"    🟢 Low:      {report.low}")
    if report.by_category:
        print(f"\n  分類統計:")
        for cat, stats in sorted(report.by_category.items()):
            hr = (stats["hallucinated"] / stats["total"] * 100) if stats["total"] > 0 else 0
            bar = "█" * int(hr / 5) + "░" * (20 - int(hr / 5))
            print(f"    {cat:15s}: {stats['hallucinated']:2d}/{stats['total']:2d} ({hr:5.1f}%) {bar}")
    print(sep)

    if verbose:
        for o in report.outputs:
            if o.hallucination:
                print(f"\n  🔴 {o.id} ({o.severity})")
                print(f"  Prompt: {o.prompt[:80]}...")
                print(f"  Output: {o.output[:120]}...")
                for v in o.violations:
                    print(f"    ├─ [{v['severity']}] {v['message']}")
                print()


def print_html_report(report: PipelineReport, output_path: str):
    """Generate a mobile-friendly HTML report."""
    rows = ""
    for o in report.outputs:
        sev_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢", "none": "✅", "error": "❌"}
        icon = sev_icon.get(o.severity, "⚪")
        vio_str = "<br>".join(
            f"<span class='badge badge-{v['severity']}'>{v['severity']}</span> {v['message']}"
            for v in o.violations
        ) if o.violations else "<span class='pass'>✓ no violations</span>"
        rows += f"""
        <tr class="{'hallucination' if o.hallucination else 'clean'}">
            <td><code>{o.id}</code></td>
            <td class="prompt">{o.prompt[:100]}</td>
            <td class="output">{o.output[:200]}</td>
            <td>{icon} {o.severity}</td>
            <td>{vio_str}</td>
            <td>{o.latency_ms:.0f}ms</td>
        </tr>"""

    cat_bars = ""
    for cat, stats in sorted(report.by_category.items()):
        hr = (stats["hallucinated"] / stats["total"] * 100) if stats["total"] > 0 else 0
        bar = "█" * int(hr / 2) + "░" * (50 - int(hr / 2))
        cat_bars += f"""
        <div class="cat-bar">
            <span class="cat-label">{cat}</span>
            <span class="cat-bar-vis">{bar}</span>
            <span class="cat-stat">{stats['hallucinated']}/{stats['total']} ({hr:.1f}%)</span>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IDM Hallucination Report — {report.model}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, 'Segoe UI', sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; }}
h1 {{ color: #58a6ff; margin-bottom: 5px; }}
h2 {{ color: #8b949e; font-size: 14px; font-weight: normal; margin-bottom: 20px; }}
.summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 24px; }}
.card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; text-align: center; }}
.card .num {{ font-size: 28px; font-weight: bold; }}
.card .label {{ font-size: 12px; color: #8b949e; }}
.critical .num {{ color: #f85149; }}
.high .num {{ color: #d29922; }}
.medium .num {{ color: #58a6ff; }}
.low .num {{ color: #3fb950; }}
.pass .num {{ color: #3fb950; }}
.cat-bars {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin-bottom: 24px; }}
.cat-bar {{ display: flex; align-items: center; margin: 6px 0; gap: 10px; }}
.cat-label {{ width: 100px; font-size: 13px; color: #8b949e; }}
.cat-bar-vis {{ font-size: 16px; letter-spacing: 1px; }}
.cat-stat {{ font-size: 12px; color: #8b949e; white-space: nowrap; }}
table {{ width: 100%; border-collapse: collapse; background: #161b22; border: 1px solid #30363d; border-radius: 8px; overflow: hidden; }}
th {{ background: #21262d; color: #8b949e; font-size: 12px; text-transform: uppercase; padding: 10px 12px; text-align: left; }}
td {{ padding: 10px 12px; border-top: 1px solid #30363d; font-size: 13px; }}
tr.hallucination {{ background: rgba(248,81,73,0.05); }}
.prompt, .output {{ max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.badge {{ display: inline-block; padding: 1px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; }}
.badge-critical {{ background: rgba(248,81,73,0.2); color: #f85149; }}
.badge-high {{ background: rgba(210,153,34,0.2); color: #d29922; }}
.badge-medium {{ background: rgba(88,166,255,0.2); color: #58a6ff; }}
.badge-low {{ background: rgba(63,185,80,0.2); color: #3fb950; }}
.pass {{ color: #3fb950; }}
@media (max-width: 768px) {{ .prompt, .output {{ max-width: 120px; }} }}
</style>
</head>
<body>
<h1>IDM Hallucination Report</h1>
<h2>Model: {report.model} · {report.timestamp} · Total: {report.total} prompts</h2>

<div class="summary">
    <div class="card">
        <div class="num pass">{report.total}</div>
        <div class="label">Total Prompts</div>
    </div>
    <div class="card">
        <div class="num" style="color:#f85149">{report.hallucinated}</div>
        <div class="label">Hallucinated ({report.hallucination_rate}%)</div>
    </div>
    <div class="card critical">
        <div class="num">{report.critical}</div>
        <div class="label">Critical</div>
    </div>
    <div class="card high">
        <div class="num">{report.high}</div>
        <div class="label">High</div>
    </div>
    <div class="card medium">
        <div class="num">{report.medium}</div>
        <div class="label">Medium</div>
    </div>
    <div class="card low">
        <div class="num">{report.low}</div>
        <div class="label">Low</div>
    </div>
</div>

{cat_bars}

<table>
<thead>
<tr><th>ID</th><th>Prompt</th><th>Output</th><th>Sev</th><th>Violations</th><th>Latency</th></tr>
</thead>
<tbody>{rows}</tbody>
</table>
</body>
</html>"""
    Path(output_path).write_text(html, encoding="utf-8")
    print(f"  📄 HTML report: {output_path}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="IDM Hallucination Batch Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("input", nargs="?", help="Prompt file (TXT or JSON)")
    parser.add_argument("--model", "-m", action="append", default=[],
                        help="Model(s) to test (repeatable for comparison)")
    parser.add_argument("--json", action="store_true", help="Input is JSON format")
    parser.add_argument("--kernel", "-k", action="store_true",
                        help="Prepend IDM F kernel as system prompt")
    parser.add_argument("--temperature", "-t", type=float, default=0.7,
                        help="Generation temperature (default: 0.7)")
    parser.add_argument("--max-tokens", type=int, default=2048,
                        help="Max tokens per generation (default: 2048)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Detailed output per violation")
    parser.add_argument("--html", action="store_true",
                        help="Output HTML report")
    parser.add_argument("--verify-only", metavar="JSON",
                        help="Skip model call, verify existing outputs JSON")
    parser.add_argument("--output", "-o", default="",
                        help="Save report JSON to file")
    parser.add_argument("--model-list", action="store_true",
                        help="List available Ollama models")

    args = parser.parse_args()

    # ── List models ──
    if args.model_list:
        try:
            req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
            print("Available models:")
            for m in data.get("models", []):
                name = m["name"]
                size = m.get("details", {}).get("parameter_size", "?")
                print(f"  {name:30s} ({size})")
        except Exception as e:
            print(f"Error: {e}")
        return

    # ── Verify only mode ──
    if args.verify_only:
        with open(args.verify_only) as f:
            outputs_data = json.load(f)
        outputs = [ModelOutput(**o) for o in outputs_data]
        total = len(outputs)
        hallucinated = sum(1 for o in outputs if o.hallucination)
        report = PipelineReport(
            model=outputs[0].model if outputs else "unknown",
            total=total, hallucinated=hallucinated,
            hallucination_rate=round(hallucinated / total * 100, 1) if total else 0,
            critical=sum(1 for o in outputs if o.severity == "critical"),
            high=sum(1 for o in outputs if o.severity == "high"),
            medium=sum(1 for o in outputs if o.severity == "medium"),
            low=sum(1 for o in outputs if o.severity == "low"),
            outputs=outputs,
            timestamp=datetime.now().isoformat(),
        )
        print_report(report, verbose=args.verbose)
        return

    # ── Load prompts ──
    if not args.input:
        print("Please provide a prompt file or use --verify-only")
        parser.print_help()
        sys.exit(1)

    prompts = load_prompts(args.input, is_json=args.json)
    if not prompts:
        print(f"❌ No prompts loaded from {args.input}")
        sys.exit(1)
    print(f"📥 Loaded {len(prompts)} prompts from {args.input}", file=sys.stderr)

    # ── System prompt ──
    system_prompt = ""
    if args.kernel:
        from idm_consistency_verifier import IDMVerifier as V
        v = V()
        system_prompt = v.kernel()
        print(f"📋 Prepended F kernel (system prompt active)", file=sys.stderr)

    # ── Models ──
    models = args.model if args.model else ["qwen3.5:9b"]

    for model in models:
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"  Model: {model}", file=sys.stderr)
        print(f"{'='*60}", file=sys.stderr)

        report = run_pipeline(
            prompts=prompts,
            model=model,
            system_prompt=system_prompt,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            show_progress=True,
        )

        # ── Output ──
        print_report(report, verbose=args.verbose)

        if args.html:
            html_path = f"idm_hal_report_{model.replace(':', '_')}.html"
            print_html_report(report, html_path)

        if args.output:
            out_path = args.output
            if len(models) > 1:
                base = Path(out_path)
                out_path = str(base.parent / f"{base.stem}_{model.replace(':', '_')}{base.suffix}")
            with open(out_path, "w") as f:
                json.dump(asdict(report), f, ensure_ascii=False, indent=2)
            print(f"  💾 Report saved: {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()