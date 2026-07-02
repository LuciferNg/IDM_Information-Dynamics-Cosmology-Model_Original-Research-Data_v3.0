#!/usr/bin/env python3
"""
Phase 7.2 — Defect 1: y_u Closure via 126_H Operator Matrix
============================================================
Purpose: Verify that y_u(GUT) = 3.81×10⁻⁶ (from 126_H EW doublet
+ 3-cycle eigenvector mixing) closes y_u(M_Z) to within 1%.

GUT-scale boundary (from SPheno MSSM run, except y_u):
  M_GUT = 1.42675190e16 GeV, M_SUSY = 1.66449738e3 GeV
  g1' = 0.70416931, g2 = 0.70416931, g3 = 0.69878830
  y_u = 3.81e-6 (126_H corrected), y_c = 1.61792374e-3, y_t = 0.49726812
  y_d = 4.85986397e-5, y_s = 9.23376173e-4, y_b = 0.05235384
  y_e = 2.05763827e-5, y_mu = 4.25460575e-3, y_tau = 0.07184576
"""

import numpy as np, math

PI = math.pi
M_GUT = 1.42675190e16
M_SUSY = 1.66449738e3
M_Z = 91.1876

# 2-loop MSSM RGE coefficients
b = np.array([33.0/5.0, 1.0, -3.0])
B = np.array([[199.0/25.0, 27.0/5.0, 88.0/5.0],
              [9.0/5.0, 25.0, 24.0],
              [11.0/5.0, 9.0, 14.0]])
C_y = np.array([26.0/5.0, 6.0, 4.0])

# GUT-scale boundary — y_u(GUT) = 3.81e-6 (126_H corrected)
g_GUT = np.array([0.70416931, 0.70416931, 0.69878830])
yu_GUT = np.array([3.81e-06, 1.61792374e-03, 0.49726812])
yd_GUT = np.array([4.85986397e-05, 9.23376173e-04, 0.05235384])
ye_GUT = np.array([2.05763827e-05, 4.25460575e-03, 0.07184576])

# SPheno reference at SUSY scale
spheno = {
    'g1': 0.363461617, 'g2': 0.638108012, 'g3': 1.02760883,
    'mg': 2211.80, 'st1': 1503.82, 'st2': 1948.80,
    'mu': 1446.24, 'At': 2237.02
}

# ---- RGE ----
def dg_dt(g, yt2):
    g3 = g**3; g2 = g**2
    return b * g3 / (16*PI**2) + g3 * (B @ g2) / (16*PI**2)**2 - g3 * C_y * yt2 / (16*PI**2)**2

def dy_dt(y, g2, yt2, is_up):
    c = np.array([13.0/15.0, 3.0, 16.0/3.0]) if is_up else np.array([7.0/15.0, 3.0, 16.0/3.0])
    gauge = np.sum(c * g2)
    dy = y.copy()
    for i in range(3):
        dy[i] = y[i] / (16*PI**2) * (6*yt2 - gauge) if i == 2 else y[i] / (16*PI**2) * (-gauge)
    return dy

def dle_dt(y, g2, yt2):
    c = np.array([9.0/5.0, 3.0, 0.0])
    return y / (16*PI**2) * (-np.sum(c * g2))

# ---- RK4 integrator ----
def rk4_step(state, dt):
    g, yu, yd, ye = state
    yt2 = yu[2]**2 + yd[2]**2
    def F(s):
        g = s[0:3]; yu = s[3:6]; yd = s[6:9]; ye = s[9:12]
        g2 = g**2; yt2 = yu[2]**2 + yd[2]**2
        return np.concatenate([dg_dt(g, yt2), dy_dt(yu, g2, yt2, True),
                               dy_dt(yd, g2, yt2, False), dle_dt(ye, g2, yt2)])
    s = np.concatenate([g, yu, yd, ye])
    k1 = F(s); k2 = F(s + 0.5*dt*k1); k3 = F(s + 0.5*dt*k2); k4 = F(s + dt*k3)
    s_new = s + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    return (s_new[:3], s_new[3:6], s_new[6:9], s_new[9:12])

# ---- Run RGE from GUT to SUSY ----
state = (g_GUT.copy(), yu_GUT.copy(), yd_GUT.copy(), ye_GUT.copy())
n_steps = 50000
t_start = math.log(M_GUT); t_end = math.log(M_SUSY)
dt = (t_end - t_start) / n_steps

for step in range(n_steps):
    state = rk4_step(state, dt)

g_f, yu_f, yd_f, ye_f = state

# ---- Non-holomorphic threshold ----
mt_avg = (spheno['st1'] + spheno['st2']) / 2
alpha_3 = g_f[2]**2 / (4*PI)
x = mt_avg**2 / spheno['mg']**2
f_x = (x * math.log(x) - x + 1) / (x - 1)**2
delta = (8.0/3.0) * alpha_3 / (4*PI) * (spheno['mu'] * spheno['At']) / spheno['mg']**2 * f_x

# ---- SM RGE from SUSY to M_Z ----
alpha_3_MZ = 0.118
rge_factor = (alpha_3_MZ / alpha_3)**(4.0/7.0)
y_u_MZ = yu_f[0] * rge_factor * (1 + delta)
y_u_obs = 1.28e-5
error = (y_u_MZ / y_u_obs - 1) * 100

# ======================================================================
print("=" * 72)
print("Phase 7.2 — Defect 1: y_u Closure via 126_H Operator Matrix")
print("=" * 72)

print("\nGUT-scale boundary conditions:")
print("  y_u(GUT) = 3.81e-6  (126_H EW doublet + 3-cycle mixing)")
print("  y_c(GUT) = 1.62e-3  (10_H × rS)")
print("  y_t(GUT) = 0.497    (10_H, rank-1 dominant)")
print("  g1'=g2   = 0.704    (MSSM unification)")
print("  g3       = 0.699    (MSSM unification)")

print("\nResults at SUSY scale (M_SUSY = 1.66 TeV):")
print("  y_u(SUSY) = {:.4e}".format(yu_f[0]))
print("  y_c(SUSY) = {:.4e}".format(yu_f[1]))
print("  y_t(SUSY) = {:.6f}".format(yu_f[2]))
print("  g1'(SUSY) = {:.6f}".format(g_f[0]))
print("  g2(SUSY)  = {:.6f}".format(g_f[1]))
print("  g3(SUSY)  = {:.6f}".format(g_f[2]))

print("\nNon-holomorphic threshold:")
print("  alpha_3(SUSY) = {:.6f}".format(alpha_3))
print("  x = m_t^2/m_g^2 = {:.6f}".format(x))
print("  f(x) = {:.6f}".format(f_x))
print("  Delta y_u / y_u = {:+.4f}%".format(delta * 100))

print("\nSM RGE (SUSY -> M_Z):")
print("  RGE factor = {:.6f}".format(rge_factor))

print("\n" + "=" * 72)
print("y_u(M_Z) CLOSURE CHECK")
print("=" * 72)
print("  y_u(M_Z) = {:.4e}".format(y_u_MZ))
print("  y_u(obs) = {:.4e}".format(y_u_obs))
print("  Ratio = {:.6f}".format(y_u_MZ / y_u_obs))
print("  Error = {:+.4f}%".format(error))

if abs(error) < 1.0:
    print("\n  ✅ y_u CLOSED: error = {:.2f}% (< 1%)".format(abs(error)))
    print("  The 126_H EW doublet + 3-cycle eigenvector mixing")
    print("  resolves the y_u gap at the GUT scale boundary condition.")
elif abs(error) < 5.0:
    print("\n  ⚠️ y_u NEAR-CLOSED: error = {:.2f}% (1-5% range)".format(abs(error)))
    print("  Minor tuning of Y_126 coefficients needed.")
else:
    print("\n  ❌ y_u OPEN: error = {:.2f}%".format(abs(error)))
    print("  Need to revisit 126_H operator matrix elements.")

# ---- RGE trajectory ----
print("\n" + "=" * 72)
print("Full RGE trajectory (every 10,000 steps):")
print("=" * 72)
print("{:<12s} {:<12s} {:<12s} {:<12s} {:<14s} {:<14s} {:<10s}".format(
    "Scale", "g1'", "g2", "g3", "y_u", "y_c", "y_t"))
print("-" * 86)

state = (g_GUT.copy(), yu_GUT.copy(), yd_GUT.copy(), ye_GUT.copy())
for step in range(n_steps + 1):
    if step % 10000 == 0:
        g, yu, yd, ye = state
        scale = math.exp(t_start + step * dt)
        print("{:<12.2e} {:<12.6f} {:<12.6f} {:<12.6f} {:<14.6e} {:<14.6e} {:<10.6f}".format(
            scale, g[0], g[1], g[2], yu[0], yu[1], yu[2]))
    if step < n_steps:
        state = rk4_step(state, dt)

# ---- CAT output ----
print("\n" + "=" * 72)
print("CAT Machine-Readable Output")
print("=" * 72)
print("CAT_y_u_GUT: 3.81e-6")
print("CAT_y_u_MZ: {:.4e}".format(y_u_MZ))
print("CAT_y_u_obs: {:.4e}".format(y_u_obs))
print("CAT_y_u_error: {:.4f}".format(error))
print("CAT_y_u_status: {}".format("CLOSED" if abs(error) < 1.0 else "MONITOR"))
print("CAT_126_H_correction: {:.2f}x".format(3.81e-6 / 3.18e-6))
print("CAT_non_holomorphic: {:+.4f}%".format(delta * 100))
print("CAT_RGE_factor: {:.4f}".format(rge_factor * (yu_f[0] / yu_GUT[0])))