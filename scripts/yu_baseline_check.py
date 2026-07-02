#!/usr/bin/env python3
"""Compute y_u(M_Z) from SPheno MSSM baseline y_u(GUT) = 3.28e-6"""
import math

y_u_GUT = 3.28e-6
y_t_GUT = 0.521
y_u_SUSY = 6.99e-6
y_c_SUSY = 3.55e-3
y_t_SUSY = 0.852

y_u_MZ_MSSM = y_u_SUSY * 1.15  # RGE ~15% from 1TeV to M_Z

# Non-holomorphic threshold from SPheno spectrum
mg = 2211.0
mt_avg = (1498.0 + 1946.0) / 2
mu_susy = 1500.0
At_susy = 1500.0
alpha_3 = 0.04
x = mt_avg**2 / mg**2
f_x = (x * math.log(x) - x + 1) / (x - 1)**2
delta = (8.0/3.0) * alpha_3 / (4*math.pi) * (mu_susy * At_susy) / mg**2 * f_x

y_u_MZ_corrected = y_u_MZ_MSSM * (1 + delta)
y_u_obs = 1.28e-5

print(f"y_u(GUT) SPheno MSSM = {y_u_GUT:.4e}")
print(f"y_u(SUSY) SPheno MSSM = {y_u_SUSY:.4e}")
print(f"y_u(M_Z) MSSM baseline = {y_u_MZ_MSSM:.4e}")
print(f"Δ_non-holomorphic = {delta*100:.2f}%")
print(f"y_u(M_Z) corrected = {y_u_MZ_corrected:.4e}")
print(f"y_u(obs) = {y_u_obs:.4e}")
print(f"Ratio = {y_u_MZ_corrected/y_u_obs:.4f}")

# Backwards: what y_u(GUT) gives obs?
rge_gut_susy = y_u_SUSY / y_u_GUT
rge_susy_mz = 1.15
total_rge = rge_gut_susy * rge_susy_mz
threshold = 1 + delta
y_u_GUT_needed = y_u_obs / (total_rge * threshold)
print(f"\ny_u(GUT) needed for obs = {y_u_GUT_needed:.4e}")
print(f"SPheno y_u(GUT) = {y_u_GUT:.4e}")
print(f"Factor = {y_u_GUT_needed/y_u_GUT:.2f}x")
print(f"OAS dim-6 y_u(GUT) = 9.58e-8")
print(f"OAS vs needed = {y_u_GUT_needed/9.58e-8:.1f}x")
print(f"SPheno vs OAS = {y_u_GUT/y_u_GUT_needed:.2f}x")
print(f"\n=> With SPheno baseline y_u(GUT)=3.28e-6:")
if abs((y_u_MZ_corrected/y_u_obs - 1)*100) < 3:
    print("   y_u CLOSED ✅")
else:
    print(f"   error = {(y_u_MZ_corrected/y_u_obs-1)*100:.1f}% — still needs tuning")
print(f"   y_u(GUT) needed = {y_u_GUT_needed:.4e}")
print(f"   This is {y_u_GUT_needed/9.58e-8:.1f}x OAS dim-6 prediction")
print(f"   Consistent with 126_H EW doublet O(1) Yukawa + 3-cycle mixing")