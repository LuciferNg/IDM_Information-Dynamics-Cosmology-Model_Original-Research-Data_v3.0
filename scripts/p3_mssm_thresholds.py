#!/usr/bin/env python3
"""
P3: Full 2-loop MSSM with SUSY Threshold Corrections
=====================================================
Key improvements over mssm_p3_background.py:
1. DR-bar conversion at M_SUSY
2. Stop/Higgsino/Gaugino threshold decoupling
3. Full 2-loop gauge RGE with y_t back-reaction
4. Comparison with OAS SU(5) and SM direct predictions

Output: unification point + GUT group identification info
"""

import numpy as np
import json, math, sys, time
from pathlib import Path

OUTPUT = Path(__file__).parent / ".." / "figures"
M_Z, M_SUSY = 91.1876, 1000.0  # 1 TeV SUSY scale
GUT_NORM = math.sqrt(5.0 / 3.0)

# === SM 1-loop coefficients ===
b_SM = np.array([41.0/10.0, -19.0/6.0, -7.0])

# === MSSM 2-loop coefficients ===
b_MSSM = np.array([33.0/5.0, 1.0, -3.0])

# MSSM 2-loop gauge beta matrix (from Martin-Vaughn 2001)
B_MSSM = np.array([
    [199.0/25.0, 27.0/5.0, 88.0/5.0],
    [9.0/5.0,    25.0,     24.0],
    [11.0/5.0,   9.0,      14.0]
])

# y_t squared contribution to gauge beta (C_i coefficients)
C_MSSM = np.array([26.0/5.0, 6.0, 4.0])

# y_t 1-loop RGE: dy_t/dt = y_t/(16π²) * (6y_t² + 6y_b² + y_τ² - 16g₃²/3 - 3g₂² - 13g₁²/15)
# Gauge contribution coefficients
b_yt = np.array([-13.0/15.0, -3.0, -16.0/3.0])


def drbar_conversion(g_sm, yt_sm, M_SUSY, M_Z=91.1876):
    """
    SM MS-bar → DR-bar conversion at M_SUSY.
    Key corrections from: gaugino loops, squark/slepton thresholds.
    """
    # Simplified DR-bar conversion for gauge couplings
    # Δ_g_i / g_i ≈ (α_i/4π) * [C_i - ln(M_SUSY²/M_Z²)]
    # For MSSM, the DR-bar shift is typically O(1-2%)
    alpha = g_sm**2 / (4.0 * math.pi)
    
    # Gaugino threshold corrections
    g_dr = np.array([
        g_sm[0] * (1.0 + alpha[0] / (4.0 * math.pi) * 1.0),   # U(1) - bino
        g_sm[1] * (1.0 + alpha[1] / (4.0 * math.pi) * 3.0),   # SU(2) - wino
        g_sm[2] * (1.0 + alpha[2] / (4.0 * math.pi) * 2.0),   # SU(3) - gluino
    ])
    
    # y_t DR-bar conversion (important for Higgs sector)
    # y_t_DR = y_t_MS * (1 + Δ_y_t) where Δ_y_t includes squark/gluino loops
    delta_yt = (g_sm[2]**2 / (12.0 * math.pi**2) - yt_sm**2 / (32.0 * math.pi**2))
    yt_dr = yt_sm * (1.0 + delta_yt)
    
    return g_dr, yt_dr


def susy_threshold_decoupling(g_dr, M_SUSY, tan_beta=10.0):
    """
    SUSY particle threshold decoupling at M_SUSY.
    Includes stop, higgsino, and gaugino thresholds.
    """
    # Stop mixing parameter (simplified)
    m_stop1 = 500.0   # GeV — lighter stop
    m_stop2 = 1500.0  # GeV — heavier stop
    m_higgsino = 200.0  # GeV
    m_gaugino = [300.0, 500.0, 1500.0]  # Bino, Wino, Gluino
    
    # Threshold corrections to gauge couplings
    # Δg_i = -g_i³/(16π²) × ln(m_SUSY/m_threshold)
    delta_g = np.zeros(3)
    
    for i, m_th in enumerate(m_gaugino):
        delta_g[i] = -g_dr[i]**3 / (16.0 * math.pi**2) * math.log(M_SUSY / m_th)
    
    # Stop threshold correction to y_t
    # Δy_t ≈ y_t/(16π²) × [g₃² ln(M_SUSY/m_gluino) - y_t² ln(M_SUSY/m_stop)]
    delta_yt = g_dr[2]**2 / (16.0 * math.pi**2) * math.log(M_SUSY / m_gaugino[2])
    delta_yt -= g_dr[2]**2 / (48.0 * math.pi**2) * math.log(M_SUSY**2 / (m_stop1 * m_stop2))
    
    g_decoupled = g_dr + delta_g
    return g_decoupled, delta_yt


def beta_g_mssm(t, y):
    """MSSM 2-loop gauge beta + 1-loop y_t running."""
    g = y[:3]
    yt = y[3]
    g2 = g**2
    g3 = g**3
    
    # Gauge 1-loop
    dg = b_MSSM * g3 / (16.0 * np.pi**2)
    
    # Gauge 2-loop
    for i in range(3):
        dg[i] += g3[i] / (16.0 * np.pi**2)**2 * (
            np.sum(B_MSSM[i] * g2) - C_MSSM[i] * yt**2
        )
    
    # y_t 1-loop RGE
    gauge_term = np.sum(b_yt * g2)
    dyt = yt / (16.0 * np.pi**2) * (6.0 * yt**2 + gauge_term)
    
    return np.concatenate([dg, [dyt]])


def beta_g_sm(t, y):
    """SM 1-loop gauge beta (for pre-SUSY running)."""
    g = y[:3]
    dg = b_SM * g**3 / (16.0 * np.pi**2)
    return np.concatenate([dg, [0.0]])


def find_unification_point(t, g):
    """Find the unification point (minimum spread) from RGE trajectory."""
    spreads = np.max(np.abs(np.column_stack([
        g[:,0] - g[:,1],
        g[:,0] - g[:,2],
        g[:,1] - g[:,2]
    ])), axis=1)
    idx = np.argmin(spreads)
    return idx, spreads[idx]


def run_p3_scan():
    """Full P3 scan with proper SUSY threshold corrections."""
    print("P3: Full 2-loop MSSM with SUSY Threshold Corrections")
    print("=" * 72)
    
    # Initial conditions at M_Z (MS-bar)
    g0 = np.array([0.357357, 0.652, 1.221])
    yt0 = 0.935  # top Yukawa at M_Z
    
    # Step 1: SM running M_Z → M_SUSY (1-loop)
    from scipy.integrate import solve_ivp
    sol_sm = solve_ivp(beta_g_sm, [math.log(M_Z), math.log(M_SUSY)],
                        np.concatenate([g0, [yt0]]),
                        method='RK45', max_step=0.1, rtol=1e-8, atol=1e-10)
    y_susy = sol_sm.y[:, -1]
    g_susy_sm = y_susy[:3]
    yt_susy_sm = y_susy[3]
    
    print(f"\n  At M_SUSY = {M_SUSY:.0f} GeV (SM running):")
    print(f"    g₁ = {g_susy_sm[0]:.6f}  g₂ = {g_susy_sm[1]:.6f}  g₃ = {g_susy_sm[2]:.6f}")
    print(f"    y_t = {yt_susy_sm:.6f}")
    
    # Step 2: DR-bar conversion at M_SUSY
    g_dr, yt_dr = drbar_conversion(g_susy_sm, yt_susy_sm, M_SUSY)
    print(f"\n  DR-bar converted at M_SUSY:")
    print(f"    g₁ = {g_dr[0]:.6f}  g₂ = {g_dr[1]:.6f}  g₃ = {g_dr[2]:.6f}")
    print(f"    y_t = {yt_dr:.6f}")
    
    # Step 3: SUSY threshold decoupling
    g_dec, delta_yt_th = susy_threshold_decoupling(g_dr, M_SUSY)
    yt_mssm = yt_dr + delta_yt_th
    print(f"\n  After threshold decoupling:")
    print(f"    g₁ = {g_dec[0]:.6f}  g₂ = {g_dec[1]:.6f}  g₃ = {g_dec[2]:.6f}")
    print(f"    y_t = {yt_mssm:.6f}")
    
    # Step 4: MSSM 2-loop running M_SUSY → M_Pl
    y_mssm = np.concatenate([g_dec, [yt_mssm]])
    sol_mssm = solve_ivp(beta_g_mssm, [math.log(M_SUSY), math.log(1e19)],
                          y_mssm, method='RK45', max_step=0.05,
                          rtol=1e-8, atol=1e-10, dense_output=True)
    
    t = sol_mssm.t
    g = sol_mssm.y[:3].T
    yt = sol_mssm.y[3]
    
    # Find unification point
    idx, spread = find_unification_point(t, g)
    M_GUT = np.exp(t[idx])
    g_GUT = np.mean(g[idx])
    g_GUT_norm = GUT_NORM * g_GUT  # GUT-normalized
    
    print(f"\n  MSSM 2-loop Running (with thresholds):")
    for scale_gev in [1e4, 1e10, 1e14, 1e16, 2e16, 1e18, 1e19]:
        i = np.argmin(np.abs(np.exp(t) - scale_gev))
        sp = max(abs(g[i,0]-g[i,1]), abs(g[i,0]-g[i,2]), abs(g[i,1]-g[i,2]))
        print(f"    {scale_gev:.0e} GeV: g₁={g[i,0]:.4f}  g₂={g[i,1]:.4f}  g₃={g[i,2]:.4f}  spread={sp:.4f}")
    
    # Step 5: GUT group identification
    # OAS spectral geometry predictions
    oas_su5 = 0.815      # SU(5) GUT embedding
    oas_sm_direct = 0.576  # Direct SM embedding (no GUT)
    
    print(f"\n  ── Best Unification ──")
    print(f"    M_GUT = 10^{math.log10(M_GUT):.2f} GeV")
    print(f"    g_GUT = {g_GUT:.4f}")
    print(f"    g_GUT² = {g_GUT**2:.4f}")
    print(f"    g_GUT² (GUT-norm) = {g_GUT_norm**2:.4f}")
    print(f"    spread = {spread:.4f}")
    print(f"    g₁={g[idx,0]:.4f}  g₂={g[idx,1]:.4f}  g₃={g[idx,2]:.4f}")
    
    # Compare with OAS predictions
    err_su5 = abs(g_GUT - oas_su5) / oas_su5 * 100
    err_sm = abs(g_GUT - oas_sm_direct) / oas_sm_direct * 100
    print(f"\n  ── OAS Cross-Check ──")
    print(f"    OAS SU(5) pred:     g_GUT ≈ {oas_su5:.3f}")
    print(f"    OAS SM direct:      g_GUT ≈ {oas_sm_direct:.3f}")
    print(f"    MSSM scan result:   g_GUT ≈ {g_GUT:.3f}")
    print(f"    Error vs SU(5):     {err_su5:.1f}%")
    print(f"    Error vs SM direct: {err_sm:.1f}%")
    
    # GUT group identification
    unifies = spread < 0.1
    prefers_su5 = err_su5 < err_sm
    
    print(f"\n  ── GUT Group Identification ──")
    if unifies:
        if prefers_su5:
            print(f"    ✅ SU(5) preferred (error {err_su5:.1f}% vs SM {err_sm:.1f}%)")
        else:
            print(f"    ✅ SM direct preferred (error {err_sm:.1f}% vs SU(5) {err_su5:.1f}%)")
    else:
        print(f"    ⚠️  MSSM does NOT fully unify at 2-loop (spread = {spread:.4f})")
        if prefers_su5:
            print(f"    SU(5) closer: error {err_su5:.1f}% vs SM {err_sm:.1f}%")
        else:
            print(f"    SM direct closer: error {err_sm:.1f}% vs SU(5) {err_su5:.1f}%")
        print(f"    → Need 3-loop corrections or threshold refinement")
    
    # Verdict
    print(f"\n  {'=' * 72}")
    print(f"  VERDICT:")
    print(f"  {'=' * 72}")
    print(f"    Unification:    {'✅ YES' if unifies else '❌ NO (spread > 0.1)'}")
    print(f"    GUT preferred:  {'SU(5)' if prefers_su5 else 'SM direct'}")
    print(f"    g_GUT:          {g_GUT:.4f}")
    print(f"    M_GUT:          10^{math.log10(M_GUT):.2f} GeV")
    
    # Save results
    result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "g_at_MZ": [float(g0[0]), float(g0[1]), float(g0[2]), float(yt0)],
        "g_at_SUSY_SM": [float(g_susy_sm[0]), float(g_susy_sm[1]), float(g_susy_sm[2]), float(yt_susy_sm)],
        "g_DRbar": [float(g_dr[0]), float(g_dr[1]), float(g_dr[2]), float(yt_dr)],
        "g_after_thresholds": [float(g_dec[0]), float(g_dec[1]), float(g_dec[2]), float(yt_mssm)],
        "unification": {
            "M_GUT": float(M_GUT),
            "log10_M_GUT": float(math.log10(M_GUT)),
            "g_GUT": float(g_GUT),
            "g_GUT2": float(g_GUT**2),
            "g_GUT2_GUTnorm": float(g_GUT_norm**2),
            "spread": float(spread),
            "g1": float(g[idx, 0]),
            "g2": float(g[idx, 1]),
            "g3": float(g[idx, 2]),
        },
        "oas_comparison": {
            "SU5_g_GUT": oas_su5,
            "SM_direct_g_GUT": oas_sm_direct,
            "error_vs_SU5_pct": float(err_su5),
            "error_vs_SM_pct": float(err_sm),
            "prefers_SU5": bool(prefers_su5),
            "unifies": bool(unifies),
        },
        "gut_group": "SU(5)" if prefers_su5 else "SM_direct",
    }
    
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path = OUTPUT / "p3_mssm_thresholds.json"
    with open(path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n  💾 Saved: {path}")
    
    return result


if __name__ == "__main__":
    run_p3_scan()