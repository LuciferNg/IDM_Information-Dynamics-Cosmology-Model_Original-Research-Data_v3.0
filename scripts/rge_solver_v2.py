#!/usr/bin/env python3
"""
RGE Solver v2 — Phase II WP-0/WP-1
===================================
2-loop SM RGE solver with:
- non-SUSY and SUSY (MSSM) beta functions
- GUT unification detection
- Fast parameter scanning via scipy minimization
- Overflow protection via clipping
- Numerical results for Phase II strategy

gi = hermes-agent rge solver v2 — Phase II Gauge Coupling Attack
"""
import numpy as np
from numpy import linalg as LA
import json, sys, math
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

OUTPUT_DIR = Path(__file__).parent / ".." / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# SM Constants (PDG 2024)
# ═══════════════════════════════════════════════════════════════
M_Z = 91.1876     # GeV
M_t = 172.69      # GeV
M_H = 125.25      # GeV
M_W = 80.377      # GeV
M_SUSY = 1.0e3    # GeV (SUSY scale, default 1 TeV)

# Gauge couplings at M_Z (MS-bar)
g1_obs = 0.357357  # U(1)_Y GUT-normalized
g2_obs = 0.652     # SU(2)_L
g3_obs = 1.221     # SU(3)_c
GUT_NORM = math.sqrt(5.0 / 3.0)

# ═══════════════════════════════════════════════════════════════
# RGE Coefficients
# ═══════════════════════════════════════════════════════════════

COEFF = {
    "SM": {
        "b": np.array([41.0/10.0, -19.0/6.0, -7.0]),
        "B": np.array([
            [199.0/50.0, 27.0/10.0, 44.0/5.0],
            [9.0/10.0, 35.0/6.0, 12.0],
            [11.0/10.0, 9.0/2.0, -26.0]
        ]),
        "C": np.array([17.0/10.0, 3.0/2.0, 2.0]),
        "y_t": 0.935,
        "label": "SM (non-SUSY)",
    },
    "MSSM": {  # Minimal SUSY SM
        "b": np.array([33.0/5.0, 1.0, -3.0]),
        "B": np.array([
            [199.0/25.0, 27.0/5.0, 88.0/5.0],
            [9.0/5.0, 25.0, 24.0],
            [11.0/5.0, 9.0, 14.0]
        ]),
        "C": np.array([26.0/5.0, 6.0, 4.0]),
        "y_t": 0.94,  # SM-like for tanβ ≈ 10
        "label": "MSSM (SUSY)",
    }
}


def dg_dlnmu(g, coeff):
    """2-loop RGE: dg_i / d(ln μ)"""
    g = np.clip(g, 0.0, 10.0)  # overflow protection
    g_sq = g**2
    dg = coeff["b"] * g**3 / (16.0 * np.pi**2)
    two_loop = np.zeros(3)
    for i in range(3):
        two_loop[i] = g[i]**3 / (16.0 * np.pi**2)**2 * (
            np.sum(coeff["B"][i] * g_sq) - coeff["C"][i] * coeff["y_t"]**2
        )
    dg = dg + two_loop
    return dg / 2.0  # d/d(ln μ) not d/dt where t = ln μ²


def integrate_rk4(g0, mu_start, mu_end, steps=1000, coeff=None, clip=True):
    """RK4 integration with log-spaced steps and overflow protection."""
    if coeff is None:
        coeff = COEFF["SM"]
    
    log_start = math.log(mu_start)
    log_end = math.log(mu_end)
    log_mu = np.linspace(log_start, log_end, steps)
    mu = np.exp(log_mu)
    
    g = np.array(g0, dtype=float)
    g_vals = [g.copy()]
    
    for i in range(1, steps):
        h = log_mu[i] - log_mu[i-1]
        
        k1 = dg_dlnmu(g, coeff)
        k2 = dg_dlnmu(g + h * k1 / 2.0, coeff)
        k3 = dg_dlnmu(g + h * k2 / 2.0, coeff)
        k4 = dg_dlnmu(g + h * k3, coeff)
        
        g = g + h * (k1 + 2*k2 + 2*k3 + k4) / 6.0
        
        if clip:
            g = np.clip(g, 0.0, 10.0)
        
        g_vals.append(g.copy())
    
    return mu, np.array(g_vals)


def run_rge_sm(g0, mu_start, mu_end, steps=1000, susy_scale=None):
    """
    Run RGE from mu_start to mu_end.
    If susy_scale is set: use SM below susy_scale, MSSM above.
    """
    if susy_scale is None or susy_scale <= 0:
        # Pure SM
        return integrate_rk4(g0, mu_start, mu_end, steps, COEFF["SM"])
    
    # Two-stage: SM below susy_scale, MSSM above
    if mu_start == mu_end:
        return np.array([mu_start]), np.array([g0])
    
    if (mu_start < mu_end and mu_start < susy_scale < mu_end) or \
       (mu_end < mu_start and mu_end < susy_scale < mu_start):
        # Crosses SUSY threshold
        n_sm = int(steps * abs(math.log(susy_scale / mu_start)) / abs(math.log(mu_end / mu_start)))
        n_sm = max(10, min(steps - 10, n_sm))
        
        mu1, g1 = integrate_rk4(g0, mu_start, susy_scale, n_sm, COEFF["SM"])
        mu2, g2 = integrate_rk4(g1[-1], susy_scale, mu_end, steps - n_sm, COEFF["MSSM"])
        
        mu = np.concatenate([mu1[:-1], mu2])
        g_vals = np.concatenate([g1[:-1], g2])
        return mu, g_vals
    elif abs(susy_scale - min(mu_start, mu_end)) / min(mu_start, mu_end) < 0.1:
        # Very close to threshold — pure MSSM
        return integrate_rk4(g0, mu_start, mu_end, steps, COEFF["MSSM"])
    else:
        # Stay in one regime
        coeff = COEFF["MSSM"] if min(mu_start, mu_end) >= susy_scale else COEFF["SM"]
        return integrate_rk4(g0, mu_start, mu_end, steps, coeff)


# ═══════════════════════════════════════════════════════════════
# Unification Analysis
# ═══════════════════════════════════════════════════════════════

def find_unification(mu, g_vals):
    """
    Find the scale where g₁ ≈ g₂ ≈ g₃ (minimal spread).
    Returns dict with unification parameters.
    """
    spread = np.max(np.abs(np.column_stack([
        g_vals[:,0] - g_vals[:,1],
        g_vals[:,0] - g_vals[:,2],
        g_vals[:,1] - g_vals[:,2]
    ])), axis=1)
    
    idx = np.argmin(spread)
    return {
        "M_GUT": float(mu[idx]),
        "log10_M_GUT": float(math.log10(mu[idx])),
        "g_GUT": float(np.mean(g_vals[idx])),
        "g_GUT2": float(np.mean(g_vals[idx])**2),
        "g1": float(g_vals[idx, 0]),
        "g2": float(g_vals[idx, 1]),
        "g3": float(g_vals[idx, 2]),
        "spread": float(spread[idx]),
    }


def backward_scan_from_mz(susy_scale=None, steps=2000):
    """Backward-integrate from M_Z to Planck scale to find unification."""
    g0 = [g1_obs, g2_obs, g3_obs]
    mu, g_vals = run_rge_sm(g0, M_Z, 1.0e19, steps, susy_scale)
    return find_unification(mu, g_vals)


def forward_scan_gut(n_logM=50, n_g2=30, susy_scale=None, steps=1000, coarse=True):
    """
    Scan (M_GUT, g_GUT²) space and compute χ² at M_Z.
    Coarse=True: faster scan with fewer points.
    """
    if coarse:
        n_logM, n_g2 = 15, 12
    
    logM_vals = np.linspace(12.0, 19.0, n_logM)
    g2_vals = np.linspace(0.1, 1.5, n_g2)
    
    best = {"chi2": float('inf')}
    results = []
    
    for logM in logM_vals:
        M_GUT = 10.0**logM
        for g2 in g2_vals:
            g_GUT = math.sqrt(g2)
            g0 = [g_GUT, g_GUT, g_GUT]
            
            try:
                mu, g_vals = run_rge_sm(g0, M_GUT, M_Z, steps, susy_scale)
                g_final = g_vals[-1]
                
                chi2 = sum(
                    (g_final[i] - [g1_obs, g2_obs, g3_obs][i])**2 
                    / (0.02 * [g1_obs, g2_obs, g3_obs][i])**2 
                    for i in range(3)
                )
                
                result = {
                    "log10_M_GUT": float(logM),
                    "M_GUT": float(M_GUT),
                    "g_GUT2": float(g2),
                    "g_GUT": float(g_GUT),
                    "g1_pred": float(g_final[0]),
                    "g2_pred": float(g_final[1]),
                    "g3_pred": float(g_final[2]),
                    "chi2": float(chi2),
                }
                results.append(result)
                
                if chi2 < best["chi2"]:
                    best = result
            except Exception as e:
                pass  # skip unstable points
    
    return best, results


# ═══════════════════════════════════════════════════════════════
# OAS Prediction Analysis
# ═══════════════════════════════════════════════════════════════

def oas_gut_prediction(alpha=1.0217, dim_G=24, d_f=2.0, N_GUT=1e4):
    """
    OAS spectral geometry prediction for g_GUT².
    
    g_GUT² = 4π · α · dim(G) / N_horizon(N_GUT)
    where N_horizon = N_GUT^(d_f/3)
    
    For SU(5): dim=24, d_f=2, N_GUT=10^4 → g_GUT² ≈ 0.664
    For direct SM: dim=12, d_f=2, N_GUT=10^4 → g_GUT² ≈ 0.332
    """
    N_horiz = N_GUT ** (d_f / 3.0)
    g2 = 4.0 * math.pi * alpha * dim_G / N_horiz
    return {
        "alpha": alpha,
        "dim_G": dim_G,
        "d_f": d_f,
        "N_GUT": N_GUT,
        "N_horizon": float(N_horiz),
        "g_GUT2": float(g2),
        "g_GUT": float(math.sqrt(g2)),
        "alpha_GUT_inv": float(4.0 * math.pi / g2),
    }


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 72)
    print("  RGE Solver v2 — Phase II WP-0/WP-1")
    print(f"  {datetime.now().isoformat()}")
    print("=" * 72)
    
    # ═══════════════════════════════════════
    # 1. SM Running (non-SUSY)
    # ═══════════════════════════════════════
    print("\n## 1. SM Running (non-SUSY) ##")
    print("-" * 50)
    
    mu, g = run_rge_sm([g1_obs, g2_obs, g3_obs], M_Z, 1e19, 2000)
    
    for scale, label in [(0, "M_Z"), (500, "10¹⁴ GeV"), (1500, "10¹⁶ GeV"), (-1, "M_Pl")]:
        print(f"  {label:8s}: g₁={g[scale,0]:.4f}  g₂={g[scale,1]:.4f}  g₃={g[scale,2]:.4f}")
    
    unif_sm = find_unification(mu, g)
    print(f"\n  Best unification (SM):")
    print(f"    M = 10^{unif_sm['log10_M_GUT']:.2f} GeV")
    print(f"    g_GUT = {unif_sm['g_GUT']:.4f}  (spread = {unif_sm['spread']:.4f})")
    print(f"    g₁={unif_sm['g1']:.4f}  g₂={unif_sm['g2']:.4f}  g₃={unif_sm['g3']:.4f}")
    print(f"    → NON-UNIFIED (expected): SM does not unify")
    
    # ═══════════════════════════════════════
    # 2. MSSM Running (SUSY at 1 TeV)
    # ═══════════════════════════════════════
    print("\n## 2. MSSM Running (SUSY at 1 TeV) ##")
    print("-" * 50)
    
    mu2, g2_vals = run_rge_sm([g1_obs, g2_obs, g3_obs], M_Z, 1e19, 2000, susy_scale=1e3)
    
    for idx in [0, -1]:
        print(f"  {'M_Z' if idx == 0 else 'M_Pl'}: g₁={g2_vals[idx,0]:.4f}  g₂={g2_vals[idx,1]:.4f}  g₃={g2_vals[idx,2]:.4f}")
    
    unif_mssm = find_unification(mu2, g2_vals)
    print(f"\n  Best unification (MSSM):")
    print(f"    M = 10^{unif_mssm['log10_M_GUT']:.2f} GeV")
    print(f"    g_GUT = {unif_mssm['g_GUT']:.4f}  (spread = {unif_mssm['spread']:.4f})")
    print(f"    g₁={unif_mssm['g1']:.4f}  g₂={unif_mssm['g2']:.4f}  g₃={unif_mssm['g3']:.4f}")
    
    # ═══════════════════════════════════════
    # 3. OAS GUT Predictions
    # ═══════════════════════════════════════
    print("\n## 3. OAS Spectral Geometry Predictions ##")
    print("-" * 50)
    
    predictions = []
    for dim_G, label in [(12, "SM direct (no GUT)"), (16, "SO(10) SM subset"), (24, "SU(5) GUT")]:
        pred = oas_gut_prediction(dim_G=dim_G)
        pred["label"] = label
        predictions.append(pred)
        match = "✅" if abs(pred["g_GUT"] - unif_mssm["g_GUT"]) / unif_mssm["g_GUT"] < 0.3 else "⚠️"
        print(f"  {label:25s}: g_GUT²={pred['g_GUT2']:.3f}  g_GUT={pred['g_GUT']:.3f}  "
              f"N_horiz={pred['N_horizon']:.0f}  {match}")
    
    # ═══════════════════════════════════════
    # 4. Fast Forward Scan (non-SUSY)
    # ═══════════════════════════════════════
    print("\n## 4. Forward GUT Boundary Scan (non-SUSY) ##")
    print("-" * 50)
    
    best_sm, _ = forward_scan_gut(coarse=True, susy_scale=None)
    print(f"  Best fit (non-SUSY):")
    print(f"    M_GUT = 10^{best_sm['log10_M_GUT']:.2f} GeV,  g_GUT² = {best_sm['g_GUT2']:.3f}")
    print(f"    g₁(M_Z)={best_sm['g1_pred']:.4f}  g₂={best_sm['g2_pred']:.4f}  g₃={best_sm['g3_pred']:.4f}")
    print(f"    χ² = {best_sm['chi2']:.1f} (ideal: < 3.0)")
    
    # ═══════════════════════════════════════
    # 5. Fast Forward Scan (MSSM)
    # ═══════════════════════════════════════
    print("\n## 5. Forward GUT Boundary Scan (MSSM, SUSY=1TeV) ##")
    print("-" * 50)
    
    best_mssm, _ = forward_scan_gut(coarse=True, susy_scale=1e3, steps=500)
    print(f"  Best fit (MSSM):")
    print(f"    M_GUT = 10^{best_mssm['log10_M_GUT']:.2f} GeV,  g_GUT² = {best_mssm['g_GUT2']:.3f}")
    print(f"    g₁(M_Z)={best_mssm['g1_pred']:.4f}  g₂={best_mssm['g2_pred']:.4f}  g₃={best_mssm['g3_pred']:.4f}")
    print(f"    χ² = {best_mssm['chi2']:.1f} (ideal: < 3.0)")
    
    # ═══════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════
    print(f"\n{'='*72}")
    print("  PHASE II GAUGE COUPLING — INITIAL VERDICT")
    print(f"{'='*72}")
    
    print(f"")
    print(f"  Backward integration from M_Z → high:")
    print(f"    SM (non-SUSY):   minimal spread at 10^{unif_sm['log10_M_GUT']:.1f} GeV (spread={unif_sm['spread']:.3f})")
    print(f"    MSSM (SUSY):     minimal spread at 10^{unif_mssm['log10_M_GUT']:.1f} GeV (spread={unif_mssm['spread']:.3f})")
    print(f"")
    print(f"  OAS spectral prediction (GUT scale, d_f=2, N_GUT=10^4):")
    for p in predictions:
        print(f"    {p['label']:25s}: g_GUT² = {p['g_GUT2']:.3f},  g_GUT = {p['g_GUT']:.3f}")
    print(f"")
    print(f"  Forward scan best fit (non-SUSY): g_GUT²={best_sm['g_GUT2']:.3f}, χ²={best_sm['chi2']:.0f}")
    print(f"  Forward scan best fit (MSSM):     g_GUT²={best_mssm['g_GUT2']:.3f}, χ²={best_mssm['chi2']:.0f}")
    print(f"")
    
    # Determine which scenario the OAS favours
    print(f"  KEY QUESTION: Does OAS require unified couplings?")
    print(f"  → If YES: MSSM is preferred (spread={unif_mssm['spread']:.3f} vs {unif_sm['spread']:.3f})")
    print(f"  → If NO:  SM non-unified is acceptable; OAS predicts g_GUT ≈ 0.58 (dim=12)")
    print(f"")
    print(f"  Critical test: run SU(5) OAS prediction (g_GUT≈{predictions[2]['g_GUT']:.3f})")
    print(f"  through MSSM RGE → does it match SM at M_Z?")
    print(f"{'='*72}")
    
    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "sm_running": {
            "g_at_MZ": [g[0,0], g[0,1], g[0,2]],
            "g_at_10_16": [g[1500,0], g[1500,1], g[1500,2]],
            "g_at_Planck": [g[-1,0], g[-1,1], g[-1,2]],
        },
        "unification": {
            "SM": unif_sm,
            "MSSM": unif_mssm,
        },
        "oas_predictions": predictions,
        "forward_scan_best": {
            "SM": best_sm,
            "MSSM": best_mssm,
        },
    }
    
    path = OUTPUT_DIR / "rge_solver_v2_results.json"
    with open(path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  💾 Saved: {path}")


if __name__ == "__main__":
    main()