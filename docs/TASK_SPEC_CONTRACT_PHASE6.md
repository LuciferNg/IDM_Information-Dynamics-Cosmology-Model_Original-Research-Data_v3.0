# Task Spec Contract — Phase 6: Peer Review Hardening

**Project:** IDM Domain Framework
**Phase:** 6
**Report:** 6.0
**Date:** 2026-07-03
**Preceding Phase:** Report 5.0 (Phases 2–5: 7/7 attack vectors, SO(10) forced, 9/10 Qs closed)
**Repository:** `github.com/LuciferNg/IDM-Domain-Framework`
**Mode:** **Direct** — no TDD/pytest, theorem-proof format, 繁體中文/English mixed

---

## 1. Purpose

Phase 6 = **Peer Review Hardening**. Report 5.0 achieved 7/7 attack vectors and 100% self-consistency scorecard (81/81) but was audited by an external peer reviewer (Gemini) who identified **4 critical vulnerabilities** that would kill the framework in formal review:

| # | Vulnerability | Severity | Target |
|:-:|:--------------|:--------:|:-------|
| 1 | Appendix A: Mass dimension mismatch in gravitational threshold derivation → ε²v² equated to dimensionless ε·C₀ | **🔴 Fatal** | Rewrite derivation |
| 2 | Appendix C: Static κ conflated with dynamic a(t) → logical loop | **🔴 Fatal** | Separate topology from dynamics |
| 3 | Scorecard: Claims 100% self-consistency while y_u has 22% error + shooting method contradicts "zero ad-hoc" | **🟠 Major** | Honest scorecard |
| 4 | β framing: Code bug fix packaged as theoretical discovery | **🟡 Minor** | Correct framing |

### Strategic Principle

**攻克為目的，並非語言上的誠實修飾** — each vulnerability receives a **substantive technical resolution**, not a cosmetic linguistic polish. Where the critique identifies a genuine error, we **fix the underlying physics** and document the correction. Where the critique overstates the issue (Appendix A v2 already fixed via spectral approach), we prove the **equivalence** between the spectral and Π'(p²) methods.

---

## 2. Input Assumptions (Locked)

| # | Assumption | Source | Rationale |
|:-:|:-----------|:-------|:----------|
| A1 | Report 5.0 appendices are the current reference (Appendix A v2, Appendix C v2) | repo | Phase 6 builds on existing corrected content |
| A2 | Gemini's critique is taken at face value — no straw-man reduction | Gemini audit | Must survive rigorous peer review |
| A3 | Identified known issues (Appendix A v2 is spectral not Π'(p²); Appendix C v2 already separates κ from a(t) but narrative still conflates; scorecard 100% includes 22% y_u error; β framing as breakthrough) | repo audit | Phase 6 fixes these |
| A4 | All OAS axioms (T1-T9, forced parameter chain) remain unchanged | Report 5.0 | Phase 6 does not add new physics — it hardens existing claims |
| A5 | Domain Independence (T5) prohibits cross-domain parameter derivation | Programme narrative | All fixes stay within respective domains |

---

## 3. Derivation Targets

### T1: Gravitational Threshold — Π'(p²) Derivation

**Defect:** Gemini identifies that the original (and v2 spectral) derivation equates a mass² quantity to a dimensionless quantity. v2 Appendix A fixed this via spectral Laplacian approach but did not connect to standard QFT field-strength renormalization.

**Resolution:** Provide the **Π'(p²) derivation** that:
1. Starts from the standard gauge boson self-energy Π_μν^{ab}(p) at 1-loop
2. Uses the **derivative Π'(p²) at p²=0** (field-strength renormalization)
3. Shows that m_W² = λ₀·M_Pl² where λ₀ = dim(G)·ε·C₀ is the Laplacian eigenvalue
4. Shows that the M_Pl² cancels between numerator and denominator → Δ(1/g²) = dim(G)·ε·C₀/(16π²)
5. **Proves equivalence** between spectral approach and Π'(p²) approach

**Output:** `report/av1_pi_prime_derivation.py` + section in Report 6.0 §AV-1

### T2: Static κ vs Dynamic a(t) — Formal Separation

**Defect:** Gemini identifies that κ (a static topological constant) cannot "generate" a(t) (a dynamic function).

**Resolution:** Provide the **sync field Friedmann equations** that show:
1. κ determines the **local metric signature (−+++)** only — fixed by directed Laplacian contour integral
2. a(t) evolves according to **sync field EoM**: (ȧ/a)² = (8πG/3)ρ_W(t) where ρ_W(t) comes from the sync field's kinetic + potential energy
3. The **gap coupling**: the O(1/ln N) ≈ 26% residual at finite N sets the metric coefficient uncertainty — this is the source of O(1) coupling constants
4. **κ → conformal structure; a(t) → sync field relaxation** — completely separate mechanisms

**Output:** Section in Report 6.0 §AV-2

### T3: Scorecard Honesty Restoration

**Defect:** Report 5.0 claims 81/81 = 100% self-consistency despite:
- y_u: 1.0×10⁻⁵ predicted vs 1.28×10⁻⁵ observed (22% error, marked 🟡 0.8× in §9.12 but counted as ✅ in summary)
- Shooting method for y_b (numerical fitting) contradicts "zero ad-hoc" claim
- β fix restored standard MSSM, not a new prediction

**Resolution:**
- Downgrade EW empirical verification: **5/5 → 3/5** (t,b good; c,s approximate; u pending)
- Downgrade self-consistency: **81/81 = 100% → 75/81 = 92.6%**
- Acknowledge shooting method = numerical fit for y_b (not first-principles)
- Acknowledge y_u needs 2-loop MSSM RGE with full SPheno/SARAH spectrum — a computational frontier, not a theoretical deficiency
- Maintain: SO(10) forced, θ_QCD=0, Born rule, κ contour integral, C₀ residue theorem — these are genuine forced-chain derivations

**Output:** Honest scorecard table in Report 6.0 §AV-3

### T4: β Framing Correction

**Defect:** Report 5.0 Chapter 1 titles "The β Factor Bug — A Critical Correction" and presents g₂≈g₃ as a breakthrough, when it's restoring known MSSM.

**Resolution:**
- Reframe: "β Factor Convention Standardisation — Code Verification"
- Clarify: g₂≈g₃ at 2×10¹⁶ GeV is a known MSSM unification signature — its recovery proves the RGE pipeline is now reliable
- The actual contribution: the **gravitational threshold** that then forces SO(10) — that remains the framework's predictive content
- Add a **Verification Scorecard**: pre-fix vs post-fix numbers, confirmation that MSSM standard result is reproduced

**Output:** Section in Report 6.0 §AV-4

---

## 4. Verification Matrix

| Target | Verification Method | Output | Accept Criteria |
|:-------|:--------------------|:-------|:----------------|
| T1: Π'(p²) derivation | Analytic proof + Python symbolic verification | `scripts/av1_pi_prime.py` | Δ(1/g²) = dim(G)·ε·C₀/(16π²) derived from Π'(0), no dimension mismatch |
| T2: κ≠a(t) separation | Formal statement + sync field Friedmann eq | Report 6.0 §AV-2 | κ → signature only; a(t) → sync field dynamics |
| T3: Honest scorecard | Numerical comparison table | Report 6.0 §AV-3 | y_u at 22% error explicitly stated; score lowered to 92% |
| T4: β framing | Narrative correction | Report 6.0 §AV-4 | g₂≈g₃ identified as MSSM verification, not new prediction |

---

## 5. Boundaries

| # | Boundary | Reason |
|:-:|:---------|:-------|
| B1 | No modification of existing files EXCEPT for documented known bugs | User directive |
| B2 | No new physics beyond existing forced-chain parameters | Phase 6 is hardening, not discovery |
| B3 | Appendices A, B, C remain read-only (v2 corrected versions are accepted) | User directive |
| B4 | Gemini's critique text is added verbatim as external peer review, integrated into §AV-0 | Authenticity |

---

## 6. Known Constraints

| # | Constraint | Impact | Mitigation |
|:-:|:-----------|:-------|:-----------|
| C1 | y_u 22% error cannot be resolved without 2-loop MSSM RGE with full SUSY spectrum | Not fixable in this phase | Acknowledge as computational frontier; plan for Phase 7 |
| C2 | Shooting method for y_b is numerical fitting | Framework claim must be downgraded | Acknowledge as "guided numerical convergence within locked Clebsch structure" |
| C3 | β fix = code convention standardisation | Narrative re-framing only | No physics content change needed |
| C4 | Appendix A v2 spectral approach is valid but not standard QFT language | Need equivalence proof | Π'(p²) derivation shows spectral approach = standard approach |

---

## 7. Repository Impact

| File | Action | Content |
|:-----|:-------|:--------|
| `docs/TASK_SPEC_CONTRACT_PHASE6.md` | **CREATE** (this file) | Phase 6 contract |
| `narrative/phase6.md` | **CREATE** | Phase 6 narrative |
| `report/report_6.0.md` | **CREATE** | Full Phase 6 report |
| `scripts/av1_pi_prime.py` | **CREATE** | Π'(p²) verification script |
| Existing appendices | **NO MODIFICATION** (v2 already correct) | Read-only |
| Existing report_5.0.md | **NO MODIFICATION** (Phase 5 concluded) | Read-only |

---

*End of Task Spec Contract — Phase 6. Generated by Hermes Agent. Direct mode with theorem-proof structure.*