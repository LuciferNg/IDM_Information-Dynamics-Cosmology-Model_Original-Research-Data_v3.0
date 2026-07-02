#!/usr/bin/env python3
"""
IDM Hallucination Benchmark Runner
==================================
Run the 59-prompt benchmark incrementally:
  - Saves progress after each prompt (resumable)
  - Generates report at end

Usage:
  python3 run_hal_benchmark.py                        # Run full 59 prompts
  python3 run_hal_benchmark.py --first 10             # Run first 10 only (quick test)
  python3 run_hal_benchmark.py --model qwen3.5:0.8b   # Specify model
  python3 run_hal_benchmark.py --resume               # Resume from last saved state
"""

import sys, json, time, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from idm_hal_pipeline import detect_ollama_host, ollama_generate, print_report, print_html_report
from idm_consistency_verifier import IDMVerifier
from dataclasses import dataclass, field, asdict
from datetime import datetime

BENCHMARK_PATH = Path(__file__).parent / "idm_hal_benchmark_50.json"
SAVE_PATH = Path(__file__).parent / "idm_hal_benchmark_progress.json"


@dataclass
class OutputItem:
    id: str
    prompt: str
    category: str
    model: str
    output: str
    latency_ms: float
    violations: list = field(default_factory=list)
    hallucination: bool = False
    severity: str = "none"
    timestamp: str = ""


def main():
    parser = argparse.ArgumentParser(description="IDM Hallucination Benchmark Runner")
    parser.add_argument("--model", default="qwen3.5:0.8b", help="Model to test")
    parser.add_argument("--first", type=int, default=0, help="Run only first N prompts")
    parser.add_argument("--resume", action="store_true", help="Resume from saved progress")
    parser.add_argument("--no-model", action="store_true", help="Skip model calls, just verify (for already-saved data)")
    args = parser.parse_args()

    verifier = IDMVerifier(strict=True)

    # Load prompts
    with open(BENCHMARK_PATH) as f:
        all_prompts = json.load(f)

    prompts = all_prompts[:args.first] if args.first > 0 else all_prompts
    total = len(prompts)

    # Resume from saved state
    completed_ids = set()
    if args.resume and SAVE_PATH.exists():
        with open(SAVE_PATH) as f:
            saved = json.load(f)
        completed_ids = {item["id"] for item in saved}
        results = [OutputItem(**item) for item in saved]
        print(f"📂 Resumed: {len(completed_ids)} already completed", file=sys.stderr)
    else:
        results = []

    # Determine which prompts to run
    remaining = [p for p in prompts if p["id"] not in completed_ids]

    if not remaining:
        print("✅ All prompts already completed!", file=sys.stderr)
    else:
        host = detect_ollama_host()
        print(f"🔗 Ollama: {host}", file=sys.stderr)
        print(f"📋 Model: {args.model}", file=sys.stderr)
        print(f"📥 Prompts: {len(remaining)} remaining / {total} total", file=sys.stderr)
        print(f"{'─'*60}", file=sys.stderr)

        for idx, p in enumerate(remaining):
            p_id = p["id"]
            prompt = p["prompt"]
            cat = p.get("category", "general")

            print(f"  [{len(completed_ids)+idx+1}/{total}] {p_id:12s} ({cat:6s})... ", end="", file=sys.stderr)
            sys.stderr.flush()

            if args.no_model:
                output = ""
                latency = 0
            else:
                result = ollama_generate(
                    model=args.model,
                    prompt=prompt,
                    system="",
                    temperature=0.7,
                    max_tokens=1024,
                )
                if "error" in result:
                    print(f"❌ {result['error']}", file=sys.stderr)
                    output = f"[ERROR] {result['error']}"
                    latency = result.get("latency_ms", 0)
                else:
                    output = result["output"]
                    latency = result["latency_ms"]

            # Verify
            report = verifier.check(output, source=p_id)
            is_hal = not report["pass"]
            sev = "none"
            if is_hal:
                if report["stats"]["critical"] > 0: sev = "critical"
                elif report["stats"]["high"] > 0: sev = "high"
                elif report["stats"]["medium"] > 0: sev = "medium"
                elif report["stats"]["low"] > 0: sev = "low"

            item = OutputItem(
                id=p_id, prompt=prompt, category=cat, model=args.model,
                output=output[:500], latency_ms=latency,
                violations=report["violations"],
                hallucination=is_hal, severity=sev,
                timestamp=datetime.now().isoformat(),
            )
            results.append(item)

            icon = "🔴" if is_hal else "✅"
            print(f"{icon} {sev:8s} ({latency:.0f}ms)", file=sys.stderr)

            # Save progress after each prompt
            with open(SAVE_PATH, "w") as f:
                json.dump([asdict(r) for r in results], f, ensure_ascii=False, indent=2)

    # ── Generate Report ──
    total_done = len(results)
    hal_count = sum(1 for r in results if r.hallucination)
    rate = round(hal_count / total_done * 100, 1) if total_done else 0

    severity_counts = {
        "critical": sum(1 for r in results if r.severity == "critical"),
        "high": sum(1 for r in results if r.severity == "high"),
        "medium": sum(1 for r in results if r.severity == "medium"),
        "low": sum(1 for r in results if r.severity == "low"),
    }

    # By category
    by_cat = {}
    for r in results:
        cat = r.category
        if cat not in by_cat:
            by_cat[cat] = {"total": 0, "hallucinated": 0}
        by_cat[cat]["total"] += 1
        if r.hallucination:
            by_cat[cat]["hallucinated"] += 1

    # ── Print report ──
    sep = "═" * 60
    print(f"\n{sep}")
    print(f"  IDM Hallucination Benchmark — {args.model}")
    print(f"  {datetime.now().isoformat()}")
    print(sep)
    print(f"  總計: {total_done} prompts")
    print(f"  幻覺: {hal_count}/{total_done} ({rate}%)")
    print(f"  嚴重度:")
    print(f"    🔴 Critical: {severity_counts['critical']}")
    print(f"    🟠 High:     {severity_counts['high']}")
    print(f"    🟡 Medium:   {severity_counts['medium']}")
    print(f"    🟢 Low:      {severity_counts['low']}")
    print()
    print(f"  分類統計:")
    for cat in ["trap", "positive", "open-q", "rewrite", "combined", "edge"]:
        if cat in by_cat:
            s = by_cat[cat]
            hr = round(s["hallucinated"] / s["total"] * 100, 1) if s["total"] else 0
            bar = "█" * int(hr / 5) + "░" * (20 - int(hr / 5))
            print(f"    {cat:10s}: {s['hallucinated']:2d}/{s['total']:2d} ({hr:6.1f}%) {bar}")
    print(sep)

    # ── Worst offenders ──
    print(f"\n  🔴 Top violations (頻次):")
    all_vio = {}
    for r in results:
        for v in r.violations:
            key = v["ref"]
            all_vio[key] = all_vio.get(key, 0) + 1
    for ref, count in sorted(all_vio.items(), key=lambda x: -x[1])[:10]:
        print(f"    {ref:6s}: {count:2d}次")

    # ── Save ──
    report_path = Path(__file__).parent / f"idm_hal_benchmark_{args.model.replace(':','_')}.json"
    with open(report_path, "w") as f:
        json.dump({
            "model": args.model,
            "total": total_done,
            "hallucinated": hal_count,
            "rate": rate,
            "severity": severity_counts,
            "by_category": by_cat,
            "top_violations": {k: v for k,v in sorted(all_vio.items(), key=lambda x: -x[1])[:15]},
            "timestamp": datetime.now().isoformat(),
            "outputs": [asdict(r) for r in results],
        }, f, ensure_ascii=False, indent=2)
    print(f"\n  💾 Report saved: {report_path}")

    # ── HTML ──
    html_path = Path(__file__).parent / f"idm_hal_benchmark_{args.model.replace(':','_')}.html"
    if total_done <= 60:
        # Simple HTML
        from idm_hal_pipeline import PipelineReport
        summary = PipelineReport(
            model=args.model, total=total_done,
            hallucinated=hal_count, hallucination_rate=rate,
            critical=severity_counts["critical"],
            high=severity_counts["high"],
            medium=severity_counts["medium"],
            low=severity_counts["low"],
            by_category=by_cat,
            outputs=results,
            timestamp=datetime.now().isoformat(),
        )
        print_html_report(summary, str(html_path))
    print(f"  📄 HTML report: {html_path}")


if __name__ == "__main__":
    main()