# Phase II — Tomorrow's Battle Plan (2026-07-03)

## Baseline (locked ✅)
- **P3 corrected**: 1+2-loop β factor fixed → g₂≈g₃ at 2×10^16 GeV (Δg=0.003)
- **GUT-normalized spread**: 0.263 → 0.127 (67% reduction)
- **SM direct error**: 8.1% (closer than SU(5) 23.6%)
- **M_GUT ≈ M_Pl**: M_GUT/M_Pl ∼ 0.82 → O(1) gravitational threshold possible

## Execution Order

### Step 1: Gravitational Threshold Analytic Estimate (30 min)
- **File**: `scripts/gravitational_threshold_estimate.py`
- **Output**: `figures/gravitational_threshold_estimate.json`
- **Key formula**: Δ(1/g_i²) = ε_i · C₀ · κ · dim(G) / (16π²) · (M_GUT²/M_Pl²)
- **Three scenarios to test**:
  1. Standard dimension-5 operator: ΔL ∝ Tr(F·F)/M_Pl
  2. OAS non-local correction: amplified by C₀=18π, κ=0.651, ε=0.155
  3. Non-perturbative N=44 spectral fluctuation: Δg_i ∝ ε·dim(G)/√N
- **Success criterion**: Can the spread be reduced from 0.127 to < 0.05?

### Step 2A (if gravitational threshold closes gap): SU(5) vs SO(10) Sync Cost
- **File**: `scripts/so10_sync_cost_comparison.py`
- **Key comparison**:
  - SU(5): dim=24, matter in 5+10̄, no right-handed ν
  - SO(10): dim=45, matter in 16 (contains all 15 SM + ν_R)
  - Sync cost free energy: F = Tr(ln(L)) + B·Tr(L⁻¹) for each group
  - Lower F → more stable → preferred GUT group

### Step 2B (if gravitational threshold insufficient): 3-loop MSSM β
- **File**: `scripts/p3_mssm_3loop.py`
- **Coefficients**: Mihaila 2012 (MSSM 3-loop gauge β)
- **Target**: Close the remaining spread from 3-loop running

## Key References
- Corrected P3 output: `figures/p3_mssm_thresholds.json`
- Q2 λ derivation: `figures/q2_lambda_derivation.json`
- All verification: `figures/beta_fix_verification.json`