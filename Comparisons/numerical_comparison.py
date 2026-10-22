"""IDM vs Parallel Researchers — Numerical Comparison Script"""
import numpy as np

print("=" * 65)
print("IDM vs PARALLEL RESEARCHERS — Numerical Comparison")
print("=" * 65)

# ─── IDM Predictions ───
print("\n## 1. IDM (LuciferNg) — Core Numbers")
print("=" * 45)
idm = {
    "ε_cosmic": 0.1545,
    "N_cosmic": 44,
    "α (universal)": 1.0248,
    "zc (sync dip)": 0.6,
    "ε_EW": 0.0161,
    "N_EW": 4,
    "ε_galaxy": 0.001,
    "N_galaxy": 1e6,
    "ε_neutrino": 0.5917,
    "N_neutrino": 3,
    "Σm_ν prediction": 0.031,  # eV
    "δr_s/r_s (BAO)": 0.077,
    "σ₈ CMB": 0.794,
    "σ₈ WL": 0.769,
    "σ₈ RSD": 0.736,
}
for k, v in idm.items():
    if isinstance(v, float):
        print(f"  {k:20s} = {v:.4f}" if v < 10 else f"  {k:20s} = {v:.1f}")
    else:
        print(f"  {k:20s} = {v}")

# ─── SRC/VSR (warpXspeed) — No explicit numbers ───
print("\n## 2. SRC/VSR (warpXspeed)")
print("=" * 45)
print("  No explicit numerical predictions found.")
print("  Framework is qualitative/descriptive.")

# ─── ITSM (brendohxd) ───
print("\n## 3. ITSM (brendohxd)")
print("=" * 45)
print("  - Toroidal topology radius parameter")
print("  - CAMB solver patch for alternative cosmology")
print("  - No explicit ε or N predictions")
print("  MCMC framework for SPARC + NANOGrav + DESI")

# ─── TEP (matthewsmawfield) ───
print("\n## 4. TEP (matthewsmawfield)")
print("=" * 45)
tep = {
    "ρ_T (universal critical density)": 20,  # g/cm³
    "R_T (GNSS calibration)": 7.8e7,  # km
    "L_c (GNSS correlation)": 4200,  # km
}
for k, v in tep.items():
    print(f"  {k:35s} = {v}")

# ─── ACM (lesleyliuhaitao-ctrl) ───
print("\n## 5. ACM (lesleyliuhaitao-ctrl)")
print("=" * 45)
print("  - Holographic screening parameter")
print("  - Baryonic-only fits to SPARC galaxies")
print("  - No explicit ε or N predictions")

# ─── COMPARISON TABLE ───
print("\n" + "=" * 65)
print("CROSS-COMPARISON TABLE")
print("=" * 65)
print()
print(f"{'Framework':<12} {'ε/N param':>12} {'# Tests':>8} {'Observers':>10} {'Formal math':>12} {'Code':>10}")
print("-" * 64)
print(f"{'IDM/OAS':<12} {'✅ ε=α/√N':>12} {'12':>8} {'✅ Lemma 4':>10} {'✅ Theorems':>12} {'✅ CLASS':>10}")
print(f"{'SRC/VSR':<12} {'❌ None':>12} {'1-2':>8} {'❌ No':>10} {'⚠️ Eqns':>12} {'⚠️ Python':>10}")
print(f"{'ITSM':<12} {'⚠️ None':>12} {'~5':>8} {'❌ No':>10} {'✅ Field eqns':>12} {'✅ Full':>10}")
print(f"{'TEP':<12} {'⚠️ ρ_T':>12} {'2':>8} {'❌ No':>10} {'⚠️ Partial':>12} {'⚠️ PDFs':>10}")
print(f"{'ACM':<12} {'⚠️ Screen':>12} {'SPARC':>8} {'❌ No':>10} {'✅ Holography':>12} {'✅ Python':>10}")

print()
print("=" * 65)
print("VERDICT")
print("=" * 65)
print()
print("IDM/OAS is the ONLY framework with:")
print("  1. Domain decomposition (N_i)")
print("  2. CLT-derived precision scaling (ε = α/√N)")
print("  3. Specific numerical predictions (ε_cosmic, ε_EW, Σm_ν)")
print("  4. Active observer ontology (Lemma 4)")
print("  5. 12 completed empirical tests")
print()
print("SRC/VSR is the CLOSEST ontological match (pre-spacetime field)")
print("ITSM is the closest TECHNICAL rival (CAMB patch, MCMC, active)")
print("TEP has the most interesting calibration method (GNSS)")
print("ACM has the cleanest galaxy rotation test (no dark matter)")
print()
print("IDM should: borrow ITSM's MCMC pipeline, check TEP's GNSS data,")
print("  collaborate with ACM on SPARC, and open a dialogue with warpXspeed.")