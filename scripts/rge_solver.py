#!/usr/bin/env python3
"""
RGE Solver — Phase II WP-0
===========================
2-loop Standard Model RGE solver with:
- SU(3) × SU(2) × U(1) gauge couplings
- Top Yukawa threshold
- GUT normalization √(5/3) for U(1)_Y
- RK4 integration forward and backward

gi = hermes-agent rge solver — Phase II Gauge Coupling Attack
"""
import numpy as np
import json, sys, math
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent / ".." / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# SM Constants (PDG 2024)
# ═══════════════════════════════════════════════════════════════
M_Z = 91.1876  # GeV
M_t = 172.69   # GeV (top pole mass)
M_H = 125.25   # GeV (Higgs mass)
M_W = 80.377   # GeV

# Gauge couplings at M_Z (MS-bar, PDG 2024)
g1_obs = 0.357   # U(1)_Y (GUT-normalized: g1 = √(5/3) × g_Y)
g2_obs = 0.652   # SU(2)_L
g3_obs = 1.221   # SU(3)_c

# GUT normalization factor
GUT_NORM = math.sqrt(5.0 / 3.0)

g_Y_obs = g1_obs / GUT_NORM  # actual U(1)_Y coupling before GUT norm

# ═══════════════════════════════════════════════════════════════
# SM RGE Coefficients (1-loop and 2-loop, non-SUSY)
# ═══════════════════════════════════════════════════════════════

b = np.array([41.0/10.0, -19.0/6.0, -7.0])  # 1-loop beta coefficients

# 2-loop coefficient matrix B[i][j]
B = np.array([
    [199.0/50.0,  27.0/10.0,   44.0/5.0],
    [9.0/10.0,    35.0/6.0,    12.0],
    [11.0/10.0,   9.0/2.0,     -26.0]
])

# Top Yukawa contribution coefficients C[i]
C = np.array([17.0/10.0, 3.0/2.0, 2.0])

# Top Yukawa at M_Z (MS-bar, from m_t pole)
y_t_MZ = 0.935  # top Yukawa

# ═══════════════════════════════════════════════════════════════
# Beta Function
# ═══════════════════════════════════════════════════════════════

def beta_1loop(g):
    """1-loop beta function: dg_i/dt = b_i * g_i^3 / (16π²)"""
    return b * g**3 / (16.0 * np.pi**2)

def beta_2loop(g, y_t=None):
    """2-loop beta function.
    t = ln(μ²), so dg/dt = β(g)/2
    """
    if y_t is None:
        y_t = y_t_MZ
    
    g_sq = g**2
    
    # 1-loop term
    dg = b * g**3 / (16.0 * np.pi**2)
    
    # 2-loop term
    two_loop = np.zeros(3)
    for i in range(3):
        two_loop[i] = g[i]**3 / (16.0 * np.pi**2)**2 * (
            np.sum(B[i] * g_sq) - C[i] * y_t**2
        )
    
    return dg + two_loop

def dg_dlnmu(g, y_t=None):
    """dg / d(ln μ) = β(g) / 2 (since t = ln μ² = 2 ln μ)"""
    return beta_2loop(g, y_t) / 2.0

# ═══════════════════════════════════════════════════════════════
# RGE Integration (RK4)
# ═══════════════════════════════════════════════════════════════

def integrate_rk4(g0, mu_start, mu_end, steps=2000, y_t=None):
    """
    Integrate RGE from mu_start to mu_end using RK4.
    Supports both forward (mu_end > mu_start) and backward (mu_end < mu_start).
    
    Returns: (mu_vals, g_vals) where g_vals[i] = [g1, g2, g3] at mu_vals[i]
    """
    # Generate log-spaced step points
    log_start = math.log(mu_start)
    log_end = math.log(mu_end)
    log_mu_vals = np.linspace(log_start, log_end, steps)
    mu_vals = np.exp(log_mu_vals)
    
    g = np.array(g0, dtype=float)
    g_vals = [g.copy()]
    
    for i in range(1, steps):
        h = log_mu_vals[i] - log_mu_vals[i-1]  # step in ln(μ)
        
        # RK4
        k1 = dg_dlnmu(g, y_t)
        k2 = dg_dlnmu(g + h * k1 / 2.0, y_t)
        k3 = dg_dlnmu(g + h * k2 / 2.0, y_t)
        k4 = dg_dlnmu(g + h * k3, y_t)
        
        g = g + h * (k1 + 2*k2 + 2*k3 + k4) / 6.0
        g_vals.append(g.copy())
    
    return mu_vals, np.array(g_vals)

# ═══════════════════════════════════════════════════════════════
# GUT Boundary Detection
# ═══════════════════════════════════════════════════════════════

def detect_unification(mu_vals, g_vals):
    """
    Find the scale where g₁ ≈ g₂ ≈ g₃ (unification).
    
    Returns: (mu_unif, g_unif, spread) where spread = max(g_i) - min(g_i)
    """
    g1, g2, g3 = g_vals[:, 0], g_vals[:, 1], g_vals[:, 2]
    spread = np.max(np.abs(np.column_stack([g1-g2, g1-g3, g2-g3])), axis=1)
    
    idx_min = np.argmin(spread)
    return mu_vals[idx_min], np.mean(g_vals[idx_min]), spread[idx_min]

# ═══════════════════════════════════════════════════════════════
# GUT Boundary Scanner (WP-1)
# ═══════════════════════════════════════════════════════════════

def scan_gut_boundary(gut_min=14.0, gut_max=18.0, n_scan=50, steps=2000):
    """
    Scan M_GUT and g_GUT² space to find best fit with SM couplings at M_Z.
    
    For each (log_M_GUT, g_GUT²), forward-integrate RGEs from M_GUT to M_Z,
    compare g_i(M_Z) with observed values.
    """
    logM_vals = np.linspace(gut_min, gut_max, n_scan)
    g2_vals = np.linspace(0.3, 2.0, n_scan)
    
    results = []
    
    for logM in logM_vals:
        M_GUT = 10.0**logM
        for g2 in g2_vals:
            g_GUT = math.sqrt(g2)
            # Start with unified coupling at M_GUT
            g0 = [g_GUT, g_GUT, g_GUT]
            # Forward-integrate to M_Z
            mu_vals, g_vals = integrate_rk4(g0, M_GUT, M_Z, steps)
            g_final = g_vals[-1]
            
            # Compute χ²
            chi2 = sum((g_final[i] - [g1_obs, g2_obs, g3_obs][i])**2 /
                       (0.01 * [g1_obs, g2_obs, g3_obs][i])**2 for i in range(3))
            
            results.append({
                "log10_M_GUT": logM,
                "M_GUT": M_GUT,
                "g_GUT2": g2,
                "g_GUT": g_GUT,
                "g1_pred": float(g_final[0]),
                "g2_pred": float(g_final[1]),
                "g3_pred": float(g_final[2]),
                "chi2": float(chi2),
            })
    
    return results


def scan_gut_from_mz(n_scan=100):
    """
    Backward-integrate from M_Z to high scales.
    Find the scale where couplings unify (minimum spread).
    """
    g0 = [g1_obs, g2_obs, g3_obs]
    
    # Backward-integrate from M_Z to 10^19 GeV
    mu_vals, g_vals = integrate_rk4(g0, M_Z, 10**19, steps=n_scan*10)
    
    # Find unification
    mu_unif, g_unif, spread = detect_unification(mu_vals, g_vals)
    
    return {
        "M_GUT": float(mu_unif),
        "log10_M_GUT": float(math.log10(mu_unif)),
        "g_GUT": float(g_unif),
        "g_GUT2": float(g_unif**2),
        "spread": float(spread),
        "g1_at_GUT": float(g_vals[np.argmin(np.max(np.abs(np.column_stack(
            [g_vals[:,0]-g_vals[:,1], g_vals[:,0]-g_vals[:,2], 
             g_vals[:,1]-g_vals[:,2]])), axis=1))][0]),
        "g2_at_GUT": float(g_vals[np.argmin(np.max(np.abs(np.column_stack(
            [g_vals[:,0]-g_vals[:,1], g_vals[:,0]-g_vals[:,2],
             g_vals[:,1]-g_vals[:,2]])), axis=1))][1]),
        "g3_at_GUT": float(g_vals[np.argmin(np.max(np.abs(np.column_stack(
            [g_vals[:,0]-g_vals[:,1], g_vals[:,0]-g_vals[:,2],
             g_vals[:,1]-g_vals[:,2]])), axis=1))][2]),
    }


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

def main():
    print("=" * 70)
    print("  RGE Solver — Phase II WP-0")
    print(f"  {datetime.now().isoformat()}")
    print("=" * 70)
    
    # ──────────────────────────────
    # Test 1: Verify known SM running
    # ──────────────────────────────
    print("\n【Test 1】SM Running from M_Z to Planck")
    print("-" * 50)
    
    mu_vals, g_vals = integrate_rk4([g1_obs, g2_obs, g3_obs], M_Z, 10**19, steps=500)
    
    print(f"  At M_Z = {M_Z} GeV:")
    print(f"    g₁ = {g_vals[0,0]:.5f}  (obs: {g1_obs})")
    print(f"    g₂ = {g_vals[0,1]:.5f}  (obs: {g2_obs})")
    print(f"    g₃ = {g_vals[0,2]:.5f}  (obs: {g3_obs})")
    
    print(f"\n  At 10¹⁴ GeV:")
    idx_14 = np.argmin(np.abs(mu_vals - 10**14))
    print(f"    g₁ = {g_vals[idx_14,0]:.5f}")
    print(f"    g₂ = {g_vals[idx_14,1]:.5f}")
    print(f"    g₃ = {g_vals[idx_14,2]:.5f}")
    
    print(f"\n  At 10¹⁶ GeV:")
    idx_16 = np.argmin(np.abs(mu_vals - 10**16))
    print(f"    g₁ = {g_vals[idx_16,0]:.5f}")
    print(f"    g₂ = {g_vals[idx_16,1]:.5f}")
    print(f"    g₃ = {g_vals[idx_16,2]:.5f}")
    
    print(f"\n  At 10¹⁹ GeV (Planck):")
    print(f"    g₁ = {g_vals[-1,0]:.5f}")
    print(f"    g₂ = {g_vals[-1,1]:.5f}")
    print(f"    g₃ = {g_vals[-1,2]:.5f}")
    
    # ──────────────────────────────
    # Test 2: Backward scan → unification
    # ──────────────────────────────
    print("\n【Test 2】Backward Unification Scan (from M_Z → high)")
    print("-" * 50)
    
    unif = scan_gut_from_mz(100)
    print(f"\n  Best unification point:")
    print(f"    M_GUT = 10^{unif['log10_M_GUT']:.2f} GeV")
    print(f"    g_GUT = {unif['g_GUT']:.4f} (g² = {unif['g_GUT2']:.4f})")
    print(f"    Spread = {unif['spread']:.4f}")
    print(f"    g₁(GUT) = {unif['g1_at_GUT']:.4f}")
    print(f"    g₂(GUT) = {unif['g2_at_GUT']:.4f}")
    print(f"    g₃(GUT) = {unif['g3_at_GUT']:.4f}")
    
    # ──────────────────────────────
    # Test 3: Forward scan (WP-1)
    # ──────────────────────────────
    print("\n【Test 3】Forward GUT Boundary Scan (coarse)")
    print("-" * 50)
    
    results = scan_gut_boundary(14.0, 18.0, 20, 1000)
    
    # Find minimum χ²
    best = min(results, key=lambda r: r["chi2"])
    print(f"\n  Best fit (from forward scan):")
    print(f"    M_GUT = 10^{best['log10_M_GUT']:.2f} GeV")
    print(f"    g_GUT² = {best['g_GUT2']:.4f}")
    print(f"    g_GUT = {best['g_GUT']:.4f}")
    print(f"    χ² = {best['chi2']:.2f}")
    print(f"    Predicted at M_Z:")
    print(f"      g₁ = {best['g1_pred']:.4f} (obs: {g1_obs})")
    print(f"      g₂ = {best['g2_pred']:.4f} (obs: {g2_obs})")
    print(f"      g₃ = {best['g3_pred']:.4f} (obs: {g3_obs})")
    
    # ──────────────────────────────
    # Save results
    # ──────────────────────────────
    output = {
        "timestamp": datetime.now().isoformat(),
        "sm_running_test": {
            "M_Z": M_Z,
            "g_MZ": [float(g_vals[0,0]), float(g_vals[0,1]), float(g_vals[0,2])],
            "g_10_14": [float(g_vals[idx_14,0]), float(g_vals[idx_14,1]), float(g_vals[idx_14,2])],
            "g_10_16": [float(g_vals[idx_16,0]), float(g_vals[idx_16,1]), float(g_vals[idx_16,2])],
            "g_Planck": [float(g_vals[-1,0]), float(g_vals[-1,1]), float(g_vals[-1,2])],
        },
        "backward_unification": unif,
        "forward_best_fit": best,
        "all_forward": [best],  # truncated for brevity
    }
    
    path = OUTPUT_DIR / "rge_scan_results.json"
    with open(path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\n  💾 Saved results: {path}")
    
    print(f"\n{'='*70}")
    print("  RGE Solver Status: ✅ Running")
    print("  To do: full 2D scan with high resolution")
    print("  → python scripts/rge_solver.py --full-scan")
    print(f"{'='*70}")


if __name__ == "__main__":
    # Parse args for full scan
    if "--full-scan" in sys.argv:
        print("Full 2D scan mode — this will take a moment...")
        results = scan_gut_boundary(14.0, 18.0, 40, 2000)
        best = min(results, key=lambda r: r["chi2"])
        print(f"\n  Best fit: M_GUT=10^{best['log10_M_GUT']:.2f}, g_GUT²={best['g_GUT2']:.4f}")
        print(f"  χ² = {best['chi2']:.2f}")
        print(f"  g1_pred(M_Z)={best['g1_pred']:.4f}, g2_pred={best['g2_pred']:.4f}, g3_pred={best['g3_pred']:.4f}")
        
        path = OUTPUT_DIR / "rge_scan_full.json"
        with open(path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"  Full scan saved: {path}")
    else:
        main()
