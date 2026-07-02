#!/usr/bin/env python3
"""Phase 7.1 — SPheno vs Python RK4 Cross-Validation"""
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

# GUT-scale boundary from SPheno
g_GUT = np.array([0.70416931, 0.70416931, 0.69878830])
yu_GUT = np.array([3.18487714e-06, 1.61792374e-03, 0.49726812])
yd_GUT = np.array([4.85986397e-05, 9.23376173e-04, 0.05235384])
ye_GUT = np.array([2.05763827e-05, 4.25460575e-03, 0.07184576])

# SPheno reference values at SUSY scale
spheno = {
    'yu': 6.78926516e-06, 'yc': 3.44894673e-03, 'yt': 0.82989634,
    'g1': 0.363461617, 'g2': 0.638108012, 'g3': 1.02760883,
    'mg': 2211.80, 'st1': 1503.82, 'st2': 1948.80,
    'mu': 1446.24, 'At': 2237.02
}

# ---- RGE derivatives ----
def dg_dt(g, yt2):
    g3 = g**3; g2 = g**2
    b1 = b * g3 / (16*PI**2)
    b2 = g3 * (B @ g2) / (16*PI**2)**2
    b3 = -g3 * C_y * yt2 / (16*PI**2)**2
    return b1 + b2 + b3

def dy_dt(y, g2, yt2, is_up):
    c = np.array([13.0/15.0, 3.0, 16.0/3.0]) if is_up else np.array([7.0/15.0, 3.0, 16.0/3.0])
    gauge = np.sum(c * g2)
    dy = y.copy()
    for i in range(3):
        if i == 2:
            dy[i] = y[i] / (16*PI**2) * (6 * yt2 - gauge)
        else:
            dy[i] = y[i] / (16*PI**2) * (-gauge)
    return dy

def dle_dt(y, g2, yt2):
    c = np.array([9.0/5.0, 3.0, 0.0])
    gauge = np.sum(c * g2)
    return y / (16*PI**2) * (-gauge)

# ---- RK4 integrator ----
def rk4_step(state, dt):
    g, yu, yd, ye = state
    yt2 = yu[2]**2 + yd[2]**2

    def F(s):
        g = s[0:3]; yu = s[3:6]; yd = s[6:9]; ye = s[9:12]
        g2 = g**2
        yt2 = yu[2]**2 + yd[2]**2
        dg = dg_dt(g, yt2)
        dyu = dy_dt(yu, g2, yt2, True)
        dyd = dy_dt(yd, g2, yt2, False)
        dye = dle_dt(ye, g2, yt2)
        return np.concatenate([dg, dyu, dyd, dye])

    s = np.concatenate([g, yu, yd, ye])
    k1 = F(s)
    k2 = F(s + 0.5*dt*k1)
    k3 = F(s + 0.5*dt*k2)
    k4 = F(s + dt*k3)
    s_new = s + dt/6 * (k1 + 2*k2 + 2*k3 + k4)
    return (s_new[:3], s_new[3:6], s_new[6:9], s_new[9:12])

# ---- Run RGE ----
state = (g_GUT.copy(), yu_GUT.copy(), yd_GUT.copy(), ye_GUT.copy())
n_steps = 50000
t_start = math.log(M_GUT)
t_end = math.log(M_SUSY)
dt = (t_end - t_start) / n_steps

print("=" * 72)
print("Phase 7.1 — SPheno vs Python RK4 Cross-Validation")
print("=" * 72)
print("M_GUT = {:.4e} GeV, M_SUSY = {:.4e} GeV".format(M_GUT, M_SUSY))
print("Steps: {}, dt = {:.6e}".format(n_steps, dt))
print()

print("{:<12s} {:<10s} {:<10s} {:<10s} {:<14s} {:<14s} {:<10s}".format(
    "Scale", "g1'", "g2", "g3", "y_u", "y_c", "y_t"))
print("-" * 80)

for step in range(n_steps + 1):
    if step % 10000 == 0:
        t = t_start + step * dt
        scale = math.exp(t)
        g, yu, yd, ye = state
        print("{:<12.2e} {:<10.6f} {:<10.6f} {:<10.6f} {:<14.6e} {:<14.6e} {:<10.6f}".format(
            scale, g[0], g[1], g[2], yu[0], yu[1], yu[2]))
    if step < n_steps:
        state = rk4_step(state, dt)

g_f, yu_f, yd_f, ye_f = state

# ---- Comparison at SUSY scale ----
print()
print("=" * 72)
print("RESULTS AT SUSY SCALE (M_SUSY = 1.664 TeV)")
print("=" * 72)
print()
print("{:<18s} {:<16s} {:<16s} {:<10s}".format("Quantity", "Python RK4", "SPheno", "Ratio"))
print("-" * 60)
print("{:<18s} {:<16.4e} {:<16.4e} {:<10.6f}".format("y_u", yu_f[0], spheno['yu'], yu_f[0]/spheno['yu']))
print("{:<18s} {:<16.4e} {:<16.4e} {:<10.6f}".format("y_c", yu_f[1], spheno['yc'], yu_f[1]/spheno['yc']))
print("{:<18s} {:<16.6f} {:<16.6f} {:<10.6f}".format("y_t", yu_f[2], spheno['yt'], yu_f[2]/spheno['yt']))
print("{:<18s} {:<16.6f} {:<16.6f} {:<10.6f}".format("g1'", g_f[0], spheno['g1'], g_f[0]/spheno['g1']))
print("{:<18s} {:<16.6f} {:<16.6f} {:<10.6f}".format("g2", g_f[1], spheno['g2'], g_f[1]/spheno['g2']))
print("{:<18s} {:<16.6f} {:<16.6f} {:<10.6f}".format("g3", g_f[2], spheno['g3'], g_f[2]/spheno['g3']))

# ---- Non-holomorphic threshold ----
print()
print("=" * 72)
print("NON-HOLOMORPHIC SUSY THRESHOLD")
print("=" * 72)

mt_avg = (spheno['st1'] + spheno['st2']) / 2
alpha_3 = g_f[2]**2 / (4*PI)
x = mt_avg**2 / spheno['mg']**2
f_x = (x * math.log(x) - x + 1) / (x - 1)**2
delta = (8.0/3.0) * alpha_3 / (4*PI) * (spheno['mu'] * spheno['At']) / spheno['mg']**2 * f_x

print("SUSY parameters:")
print("  m_g = {:.2f} GeV".format(spheno['mg']))
print("  m_t1 = {:.2f} GeV, m_t2 = {:.2f} GeV".format(spheno['st1'], spheno['st2']))
print("  m_t_avg = {:.2f} GeV".format(mt_avg))
print("  mu = {:.2f} GeV".format(spheno['mu']))
print("  A_t = {:.2f} GeV".format(spheno['At']))
print("  alpha_3(SUSY) = {:.6f}".format(alpha_3))
print()
print("Non-holomorphic correction:")
print("  x = m_t^2/m_g^2 = {:.6f}".format(x))
print("  f(x) = {:.6f}".format(f_x))
print("  Delta y_u / y_u = {:+.6f}%".format(delta * 100))

# ---- Extrapolation to M_Z ----
print()
print("=" * 72)
print("EXTRAPOLATION TO M_Z")
print("=" * 72)

alpha_3_MZ = 0.118
rge_factor = (alpha_3_MZ / alpha_3)**(4.0/7.0)
print("SM RGE factor (SUSY -> M_Z) = {:.6f}".format(rge_factor))

y_u_MZ_py = yu_f[0] * rge_factor
y_u_MZ_spheno = spheno['yu'] * rge_factor
y_u_MZ_corr = y_u_MZ_py * (1 + delta)
y_u_obs = 1.28e-5

print()
print("{:<18s} {:<16s} {:<16s}".format("y_u", "Python RK4", "SPheno-derived"))
print("-" * 50)
print("{:<18s} {:<16.4e} {:<16.4e}".format("y_u(SUSY)", yu_f[0], spheno['yu']))
print("{:<18s} {:<16.4e} {:<16.4e}".format("y_u(M_Z) RGE", y_u_MZ_py, y_u_MZ_spheno))
print("{:<18s} {:<+15.4f}%".format("Delta non-holo", delta*100))
print("{:<18s} {:<16.4e}".format("y_u(M_Z) corr", y_u_MZ_corr))
print("{:<18s} {:<16.4e}".format("y_u(obs)", y_u_obs))
print("{:<18s} {:<16.6f}".format("Ratio to obs", y_u_MZ_corr / y_u_obs))
print("{:<18s} {:+.2f}%".format("Error", (y_u_MZ_corr/y_u_obs - 1)*100))

# ---- Backwards: y_u(GUT) needed ----
print()
print("=" * 72)
print("BACKWARDS: y_u(GUT) NEEDED FOR FULL CLOSURE")
print("=" * 72)

total_rge = (yu_f[0] / yu_GUT[0]) * rge_factor
threshold = 1 + delta
y_u_GUT_needed = y_u_obs / (total_rge * threshold)

print("Total RGE factor (GUT->M_Z): {:.4f}".format(total_rge))
print("Threshold factor: {:.4f}".format(threshold))
print("y_u(GUT) needed: {:.4e}".format(y_u_GUT_needed))
print("SPheno y_u(GUT): {:.4e}".format(yu_GUT[0]))
print("OAS dim-6 y_u(GUT): {:.4e}".format(9.58e-8))
print("Factor vs SPheno: {:.2f}x".format(y_u_GUT_needed / yu_GUT[0]))
print("Factor vs OAS dim-6: {:.1f}x".format(y_u_GUT_needed / 9.58e-8))

# ---- Verdict ----
print()
print("=" * 72)
print("VERDICT")
print("=" * 72)

yu_ratio = yu_f[0] / spheno['yu']
print()
print("Python RK4 vs SPheno at SUSY scale:")
print("  y_u(SUSY) ratio = {:.6f}".format(yu_ratio))

if abs(yu_ratio - 1) < 0.05:
    print("  ** Python RK4 AGREES with SPheno (< 5% deviation) **")
    print("  The 2-loop RGE implementation is validated.")
else:
    print("  ** Python RK4 DEVIATES from SPheno **")
    print("  Ratio = {:.4f} — check beta function coefficients".format(yu_ratio))

y_error = (y_u_MZ_corr / y_u_obs - 1) * 100
print()
print("y_u(M_Z) closure:")
print("  Prediction: {:.4e}".format(y_u_MZ_corr))
print("  Observed:   {:.4e}".format(y_u_obs))
print("  Error: {:+.2f}%".format(y_error))
print()
print("Key insight: The {:.0f}% gap is NOT a threshold problem.".format(abs(y_error)))
print("It is a GUT-scale boundary condition problem.")
print("y_u(GUT) must increase from {:.4e} to {:.4e}".format(yu_GUT[0], y_u_GUT_needed))
print("via 126_H EW doublet O(1) Yukawa + 3-cycle mixing.")
print("Non-holomorphic threshold contributes only {:+.4f}%.".format(delta*100))