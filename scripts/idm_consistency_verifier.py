#!/usr/bin/env python3
"""
IDM Consistency Verifier v1.0
=============================
驗證本地模型輸出是否違反 IDM Domain Framework 嘅 F 總結公理。
可用作 batch prompt 處理 pipeline 嘅 consistency gate，或直接嵌入 system prompt 作為 kernel。

Usage:
  python3 idm_consistency_verifier.py check "model output text..."
  python3 idm_consistency_verifier.py batch output1.txt output2.txt ...
  python3 idm_consistency_verifier.py kernel       # 輸出 system prompt kernel
  python3 idm_consistency_verifier.py list         # 列出所有 constraint
"""

import re
import sys
import json
from pathlib import Path


# ═══════════════════════════════════════════════════════════════
# F — IDM Domain Framework 完整體系（硬編碼一致性內核）
# ═══════════════════════════════════════════════════════════════

F_CONSTANTS = {
    "n_horizon": 44,
    "n_ew": 2.5e33,
    "n_gal": 1e6,
    "n_planck": 1,
    "alpha": 1.025,
    "epsilon_cosmic": 0.1545,
    "epsilon_ew": 2e-17,
    "epsilon_gal": 0.001,
    "epsilon_planck": 1.0,
    "t_zz_cosmic": 0.158,
    "v_higgs_gev": 246,
    "lambda_higgs": 0.1293,
    "n_crit": 150,
    "chi2_dof": 0.51,
    "delta_chi2": -50.8,
    "z_c": 0.60,
}

F_AXIOMS = {
    "A1": {"label": "OAS Address Space", "rule": "N ∈ ℕ⁺ — N must be positive integer"},
    "A2": {"label": "CLT Forcing", "rule": "ε = α/√N — fluctuation scale from CLT"},
    "A3": {"label": "Domain Independence", "rule": "N_i ⟂ N_j — domains are causally independent"},
    "A4": {"label": "Phase Resolution", "rule": "N determines discrete (N<150) vs continuous (N≥150) phase"},
}

F_THEOREMS = {
    "T1": "SO(N) Sync Evolution — sync evolution preserves norm, forms rotation group",
    "T2": "CLT Phase Continuization — as N→∞, discrete rotation angles become continuous",
    "T3": "U(1) Emergence — each SO(N) rotation plane → U(1) in continuous limit",
    "T4": "i as U(1) Generator — i = d/dθ|₀ e^{iθ}, i² = −1, from dimensional compression",
    "T5": "Domain Independence — N_i ⟂ N_j, no causal relation between domains",
    "T6": "Gauge = Address Conservation — gauge symmetry = sync propagation conserves address quantum numbers",
    "T7": "Minimal Chiral Group — SU(3)×SU(2)×U(1) is unique rank-4 chiral minimal gauge group",
}

F_COROLLARIES = {
    "C1": "λ/ε coincidence = ACCIDENTAL — not causal, not fine-tuned",
    "C2": "Gauge unification fallacy — N_horizon=44 cannot predict EW gauge couplings",
    "C3": "Cross-domain prediction error — domain parameters cannot predict each other",
    "C4": "i from large-N → P4 must rewrite — complex numbers not fundamental at N<150",
    "C5": "Born rule is EW domain property — probability from large-N sync statistics",
    "C6": "Scattering = sync exchange — all interactions are sync propagation",
    "C7": "EWSB = EW domain sync dip — Higgs mechanism is sync dip at v=246 GeV",
    "C8": "T_μν sign flip from λ(z) EoM — classical +0.158 → quantum negative",
}

F_OPEN_QUESTIONS = {
    "Q1": "Why 3 generations? — 🔴 open, no OAS derivation",
    "Q2": "Exact λ=0.1293? — 🔴 open, needs EW domain structure",
    "Q3": "ħ exact emergence? — 🟡 conceptual, direction known",
    "Q4": "α=1.025 exact? — 🟡 scale-free argument, not derived",
    "Q5": "Domain transition? — 🟢 70% independent, weak exclusion η≈10⁻³²",
}

F_DOMAINS = {
    "Planck": {"N": 1, "ε": 1.0, "physics": "raw OAS"},
    "Cosmic": {"N": 44, "ε": 0.1545, "physics": "GR, DE, time"},
    "Galaxy": {"N": 1e6, "ε": 0.001, "physics": "entropy effects"},
    "EW": {"N": 2.5e33, "ε": 2e-17, "physics": "Higgs, QM, gauge"},
}

# ═══════════════════════════════════════════════════════════════
# 違規模式庫 — 每個 violation 係一個 (regex, severity, message, ref)
# ═══════════════════════════════════════════════════════════════

VIOLATION_PATTERNS = [
    # ── Axiom Violations ──
    (r"α\s*[=≈]\s*(1\.0[0-9]|1\.[0-9]{2,})(?![^.]*scale-free)",
     "HIGH", "A2: α={match} 偏離 1.025，但未標註 scale-free 特例", "D"),
    (r"(N\s*[=≈]\s*(-\d+|0)[^.]|N\s*[=≈]\s*[0-9]*\.[0-9]+[^eE])",
     "HIGH", "A1: N 必須為正整數", "A1"),
    (r"(N|address count)\s*(is|is not|can be)\s*(negative|zero|fractional|non.?integer)",
     "HIGH", "A1: N ∈ ℕ⁺ — address count 不能為負/零/非整數", "A1"),

    # ── Theorem 5 + Corollary 1: Domain Independence ──
    (r"(fine.?tun(ing|ed)|conspiracy|anthropic)\s+(between|of)\s+(λ.*ε|ε.*λ|lambda.*epsilon)",
     "CRITICAL", "C1: λ/ε 被視為因果關係 — 但 Theorem 5 證明係偶然", "C1"),
    (r"(N_horizon|N=44|44\s*addresses)\s.*(predict|derive|determine|fix)\s.*(gauge|coupling|SU|EW|weak|strong)",
     "CRITICAL", "C2: Gauge Unification Fallacy — N=44 不能預測規範耦合", "C2"),
    (r"(cosmic.*(predict|determine|fix).*EW|EW.*(predict|determine|fix).*cosmic|galaxy.*(predict|determine|fix).*cosmic)",
     "CRITICAL", "C3: Cross-domain prediction error — 領域間無因果關係", "C3"),

    # ── Theorem 4: i from large-N ──
    (r"(i|imaginary unit|complex numbers?)\s+(is|are)\s+fundamental.*?\b(at|for)\s+(all|any|Planck|small|N\s*[<≤]\s*150|N\s*[<≤]\s*1)",
     "HIGH", "T4: i 唔係 fundamental — 從 large-N CLT 湧現", "T4"),
    (r"(complex structure|complex numbers?) exist(s)? at (Planck|N\s*[=≈]\s*1)",
     "HIGH", "T4: Planck domain (N=1) 冇 complex structure", "T4"),

    # ── Theorem 2: Phase Continuization ──
    (r"(continuous|continuum|smooth).*(phase|rotation|angle).*(N\s*[<≤]\s*150|small N|discrete N)",
     "MEDIUM", "T2: N<150 時 phase 係 discrete，唔係 continuous", "T2"),

    # ── Theorem 7: Gauge Group ──
    (r"(gauge group|SM group|symmetry group)[^.]*?\b(is|should be|might be)\b[^.]*?SU\(5\)",
     "MEDIUM", "T7: Minimal chiral gauge group 係 SU(3)×SU(2)×U(1)，唔係 GUT group", "T7"),
    (r"(gauge group|SM group|symmetry group)[^.]*?\b(is|should be|might be)\b[^.]*?\b(SU\(4\)|G₂|F₄|E₆)\b",
     "MEDIUM", "T7: 唯一 rank-4 chiral minimal group 係 SU(3)×SU(2)×U(1)", "T7"),

    # ── Corollary 6: Scattering = Sync Exchange ──
    (r"(virtual particle|off.?shell).*(is|as|represents)\s+(a\s+)?(real|physical|actual|fundamental).*(particle|entity)",
     "MEDIUM", "C6: 虛粒子 = 位址暫態借調，非實體粒子", "C6"),

    # ── Corollary 7: EWSB as Sync Dip ──
    (r"EWSB\s+(is|should be)\s+(a\s+)?(phase transition|symmetry breaking).*(not|unrelated|separate).*(sync|dip)",
     "LOW", "C7: EWSB = EW domain sync dip — 兩者同源", "C7"),

    # ── Corollary 5: Born Rule ──
    (r"(Born rule|probability\s+interpretation|quantum\s+probability)\s+(is|comes from|fundamental|axiom)",
     "MEDIUM", "C5: Born rule 係 EW domain property，唔係 fundamental axiom", "C5"),

    # ── Constant Violations ──
    (r"(N_horizon|N=44|44\s*addresses)\s*[=≈]\s*((?!44)\d+)",
     "HIGH", "Constant: N_horizon = 44, 唔係 {match}", "F"),
    (r"α\s*[=≈]\s*1\.0(25)?\s*(?!\s*\(scale-free\))",
     "LOW", "D: α = 1.025 係觀測值，scale-free 極限係 1", "D"),
    (r"(ε|epsilon)\s*[=≈]\s*0\.1(54|55)\s.*(N|address|domain)",
     "LOW", "A2: ε_cosmic = 0.1545, 確認用 ε = α/√N", "A2"),

    # ── Open Questions Mistaken as Solved ──
    (r"(explain(ed|s)?|deriv(e|ed)|prove[dn]?)\s+3\s+(generations|families)",
     "MEDIUM", "Q1: 3 generations 係 open problem，未推導", "Q1"),
    (r"(explain(ed|s)?|deriv(e|ed)|prove[dn]?)\s+(λ|lambda)\s*[=≈]\s*0\.1293",
     "MEDIUM", "Q2: λ=0.1293 係 open problem，未推導", "Q2"),
    (r"(explain(ed|s)?|deriv(e|ed)|prove[dn]?)\s+(θ_QCD|strong CP|CP\s+problem)",
     "MEDIUM", "Q6: θ_QCD 未在 framework 中 address", "F"),
]


class IDMVerifier:
    """IDM Domain Framework Consistency Verifier"""

    def __init__(self, strict: bool = False):
        self.strict = strict
        self.stats = {"checked": 0, "violations": 0, "critical": 0, "high": 0, "medium": 0, "low": 0}

    # ── Public API ──

    def check(self, text: str, source: str = "<input>") -> dict:
        """Verify a single text against all F constraints. Returns report dict."""
        report = {
            "source": source,
            "pass": True,
            "violations": [],
            "stats": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "summary": "",
        }
        self.stats["checked"] += 1

        for pattern, severity, message, ref in VIOLATION_PATTERNS:
            # 使用 finditer 而非 findall 以正確獲取 match text
            for m in re.finditer(pattern, text, re.IGNORECASE):
                # 低嚴重度可喺 strict mode 先報
                if severity == "LOW" and not self.strict:
                    continue
                match_text = m.group(0).strip()
                violation = {
                    "severity": severity,
                    "ref": ref,
                    "message": message.format(match=match_text[:60]),
                    "pattern": pattern,
                    "matched": match_text[:80],
                }
                report["violations"].append(violation)
                report["pass"] = False
                report["stats"][severity.lower()] += 1
                self.stats[severity.lower()] += 1
                self.stats["violations"] += 1

        # Summary
        if report["pass"]:
            report["summary"] = "✅ PASS — 無違規"
        else:
            c = report["stats"]["critical"]
            h = report["stats"]["high"]
            m = report["stats"]["medium"]
            l = report["stats"]["low"]
            report["summary"] = f"❌ FAIL — {c} critical, {h} high, {m} medium, {l} low"

        return report

    def check_batch(self, texts: list, sources: list = None) -> list:
        """Verify multiple texts. Returns list of reports."""
        if sources is None:
            sources = [f"<input {i+1}>" for i in range(len(texts))]
        return [self.check(t, s) for t, s in zip(texts, sources)]

    def check_file(self, path: str) -> dict:
        """Verify content of a text file."""
        content = Path(path).read_text(encoding="utf-8")
        return self.check(content, source=path)

    def check_files(self, *paths: str) -> list:
        """Verify multiple files."""
        return [self.check_file(p) for p in paths]

    # ── Reporting ──

    def print_report(self, report: dict, verbose: bool = False):
        """Print a human-readable report."""
        print(f"\n{'='*60}")
        print(f"  Source: {report['source']}")
        print(f"  Result: {report['summary']}")
        if report["violations"]:
            print(f"{'─'*60}")
            for v in report["violations"]:
                icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(v["severity"], "⚪")
                print(f"  {icon} [{v['severity']:8s}] {v['message']}")
                if verbose:
                    print(f"     ref: {v['ref']}, pattern: {v['pattern']}")
        print(f"{'='*60}\n")

    def print_summary(self):
        """Print aggregate statistics."""
        print(f"\n{'─'*40}")
        print(f"  IDM Verifier 統計:")
        print(f"  Checked: {self.stats['checked']}")
        print(f"  Violations: {self.stats['violations']}")
        if self.stats["violations"] > 0:
            print(f"    🔴 Critical: {self.stats['critical']}")
            print(f"    🟠 High:     {self.stats['high']}")
            print(f"    🟡 Medium:   {self.stats['medium']}")
            print(f"    🟢 Low:      {self.stats['low']}")
        print(f"{'─'*40}\n")

    # ── System Prompt Kernel ──

    def kernel(self) -> str:
        """Generate the F system prompt kernel for embedding in model prompts."""
        return f"""# IDM Domain Framework — System Prompt Kernel
## 你必須遵守以下所有公理和推論，否則視為幻覺（Hallucination）

## 四條公理
{chr(10).join(f'- {k}: {v["label"]} — {v["rule"]}' for k, v in F_AXIOMS.items())}

## 七大定理
{chr(10).join(f'- {k}: {v}' for k, v in F_THEOREMS.items())}

## 八大推論（不可違反）
{chr(10).join(f'- {k}: {v}' for k, v in F_COROLLARIES.items())}

## 關鍵常數
{chr(10).join(f'- {k} = {v}' for k, v in sorted(F_CONSTANTS.items()))}

## 開放問題（不可當作已解決）
{chr(10).join(f'- {k}: {v}' for k, v in F_OPEN_QUESTIONS.items())}

## 四大領域
{chr(10).join(f'- {k}: N={v["N"]}, ε={v["ε"]}, physics={v["physics"]}' for k, v in F_DOMAINS.items())}

## 紅線（永遠不可違反）
- CRITICAL: λ/ε 係偶然，唔係因果關係
- CRITICAL: N=44 不能預測規範耦合 (Gauge Unification Fallacy)
- CRITICAL: 領域間無因果關係 (Domain Independence)
- HIGH: α=1.025, 偏離需標註 scale-free
- HIGH: i 唔係 fundamental — 從 large-N CLT 湧現
- HIGH: N 必須為正整數
"""

    def list_constraints(self) -> str:
        """List all constraints in a readable format."""
        lines = ["# IDM Verifier — 完整約束列表", ""]
        lines.append("## 常數")
        for k, v in sorted(F_CONSTANTS.items()):
            lines.append(f"  {k} = {v}")
        lines.append("")
        lines.append("## 違規模式")
        for i, (pattern, severity, message, ref) in enumerate(VIOLATION_PATTERNS, 1):
            lines.append(f"  [{severity:8s}] [{ref:4s}] {message}")
            lines.append(f"          pattern: {pattern}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    verifier = IDMVerifier(strict=False)

    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "check":
        if len(sys.argv) < 3:
            print("Usage: idm_consistency_verifier.py check <text>")
            return
        text = sys.argv[2]
        if text.startswith("@"):
            # 從檔案讀取
            text = Path(text[1:]).read_text(encoding="utf-8")
            report = verifier.check_file(text[1:])
        else:
            report = verifier.check(text)
        verifier.print_report(report, verbose=True)
        verifier.print_summary()
        sys.exit(0 if report["pass"] else 1)

    elif cmd == "batch":
        paths = sys.argv[2:]
        if not paths:
            print("Usage: idm_consistency_verifier.py batch <file1> [file2 ...]")
            return
        reports = verifier.check_files(*paths)
        for r in reports:
            verifier.print_report(r)
        verifier.print_summary()
        all_pass = all(r["pass"] for r in reports)
        sys.exit(0 if all_pass else 1)

    elif cmd == "kernel":
        print(verifier.kernel())

    elif cmd == "list":
        print(verifier.list_constraints())

    elif cmd == "json":
        # JSON mode for pipeline integration
        if len(sys.argv) >= 3:
            text = sys.argv[2]
            report = verifier.check(text)
        else:
            report = {"error": "no text provided"}
        print(json.dumps(report, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()