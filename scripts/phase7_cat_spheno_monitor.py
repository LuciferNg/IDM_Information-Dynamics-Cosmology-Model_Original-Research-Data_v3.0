#!/usr/bin/env python3
"""
CAT SPheno Monitor — Phase 7 Automation Component

Purpose: Monitor SPheno spectrum output, track y_u RGE trajectory,
verify SUSY threshold correction closes the 22% gap.

Usage:
  python3 scripts/phase7_cat_spheno_monitor.py [--spheno-output SPHENO.OUT] [--watch]

References: Phase 7 AV-5, CAT system
"""
import argparse
import time
import os
import sys

# =============================================================================
# Expected SPheno output format
# =============================================================================
# SPheno spectrum files contain:
# - Yukawa couplings at M_Z
# - SUSY particle masses
# - RGE running data

# Reference: y_u(obs) = 1.28 × 10⁻⁵
# Target: |y_u(SPheno) - y_u(obs)| / y_u(obs) < 3%

Y_U_OBS = 1.28e-5
Y_U_TARGET = 1.28e-5
Y_U_TOLERANCE = 0.03  # 3%

def parse_spheno_yukawa(filepath):
    """
    Parse SPheno output file for Yukawa couplings at M_Z.
    
    SPheno format (typical):
    ...
    Yu[1,1] : 1.23456789E-05
    Yu[2,2] : 7.50000000E-03
    Yu[3,3] : 9.35000000E-01
    ...
    """
    y_u = None
    y_c = None
    y_t = None
    
    with open(filepath, 'r') as f:
        for line in f:
            if 'Yu[1,1]' in line and 'E' in line:
                try:
                    y_u = float(line.split(':')[1].strip())
                except (IndexError, ValueError):
                    pass
            elif 'Yu[2,2]' in line and 'E' in line:
                try:
                    y_c = float(line.split(':')[1].strip())
                except (IndexError, ValueError):
                    pass
            elif 'Yu[3,3]' in line and 'E' in line:
                try:
                    y_t = float(line.split(':')[1].strip())
                except (IndexError, ValueError):
                    pass
    
    return y_u, y_c, y_t

def parse_spheno_susy_masses(filepath):
    """
    Parse SPheno output for SUSY particle masses.
    Needed for non-holomorphic threshold verification.
    """
    masses = {}
    key_map = {
        'MGlio': 'gluino',
        'MSf[1,3]': 'stop_1',
        'MSf[2,3]': 'stop_2',
        'Mhh': 'higgs_light',
        'Mhh': 'higgs_heavy',
        'MChi[1]': 'neutralino_1',
        'MChi[2]': 'neutralino_2',
        'MChi[3]': 'neutralino_3',
        'MChi[4]': 'neutralino_4',
        'MCha[1]': 'chargino_1',
        'MCha[2]': 'chargino_2',
    }
    
    with open(filepath, 'r') as f:
        for line in f:
            for key, name in key_map.items():
                if key in line and 'E' in line:
                    try:
                        masses[name] = float(line.split(':')[1].strip())
                    except (IndexError, ValueError):
                        pass
    
    return masses

def check_y_u_convergence(y_u, y_c, y_t):
    """Check if y_u is within 3% of observed value."""
    if y_u is None:
        return "NO_DATA", 0
    
    error = abs(y_u - Y_U_OBS) / Y_U_OBS * 100
    if error < 3:
        return "PASS", error
    elif error < 10:
        return "MONITOR", error
    else:
        return "OPEN", error

def compute_non_holomorphic_correction(masses):
    """
    Compute the non-holomorphic Δy_u/y_u from SPheno spectrum.
    
    Δy_u/y_u = (8/3) × α_3/(4π) × (μ·A_t/m̃_g²) × f(m̃_t²/m̃_g²)
    """
    required = ['gluino', 'stop_1', 'stop_2']
    for r in required:
        if r not in masses:
            return None, "MISSING: " + r
    
    # Approximate μ from neutralino/chargino masses
    mu = masses.get('neutralino_2', 1.5e3) if 'neutralino_2' in masses else 1.5e3
    
    # Effective A_t (approximate)
    A_t_eff = 1.5e3  # placeholder
    
    # Gluino mass
    m_g = masses['gluino']
    
    # Average stop mass
    m_t_avg = (masses['stop_1'] + masses['stop_2']) / 2
    
    # α_3 at M_SUSY
    alpha_3 = 0.04
    
    # Loop function
    x = m_t_avg**2 / m_g**2
    if abs(x - 1) < 1e-6:
        f_x = 0.5
    else:
        f_x = (x * __import__('math').log(x) - x + 1) / (x - 1)**2
    
    delta = (8.0/3.0) * alpha_3 / (4 * __import__('math').pi) * (mu * A_t_eff) / m_g**2 * f_x
    return delta, f"μ={mu:.0f}, m̃_g={m_g:.0f}, m̃_t={m_t_avg:.0f}, f(x)={f_x:.4f}"

def main():
    parser = argparse.ArgumentParser(description="CAT SPheno Monitor — y_u Convergence")
    parser.add_argument('--spheno-output', '-o', type=str, default='SPHENO.OUT',
                        help='Path to SPheno spectrum output file')
    parser.add_argument('--watch', '-w', action='store_true',
                        help='Watch mode: poll for file changes every 10s')
    parser.add_argument('--interval', '-i', type=int, default=10,
                        help='Polling interval in seconds (default: 10)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("CAT SPheno Monitor — Phase 7 AV-5")
    print("=" * 60)
    print(f"\nWatching: {args.spheno_output}")
    print(f"Target: y_u = {Y_U_OBS:.3e} ± {Y_U_TOLERANCE*100:.0f}%")
    print(f"Mode: {'WATCH' if args.watch else 'ONESHOT'}")
    
    if not os.path.exists(args.spheno_output):
        print(f"\n⚠️  File not found: {args.spheno_output}")
        print("   Run SPheno first to generate the spectrum output.")
        print("   Expected: SARAH → SPheno → SPHENO.OUT")
        sys.exit(1)
    
    if args.watch:
        last_size = 0
        try:
            while True:
                current_size = os.path.getsize(args.spheno_output)
                if current_size != last_size:
                    last_size = current_size
                    y_u, y_c, y_t = parse_spheno_yukawa(args.spheno_output)
                    masses = parse_spheno_susy_masses(args.spheno_output)
                    status, error = check_y_u_convergence(y_u, y_c, y_t)
                    delta, info = compute_non_holomorphic_correction(masses)
                    
                    print(f"\n[{time.strftime('%H:%M:%S')}]")
                    print(f"  y_u = {y_u:.4e}  (obs: {Y_U_OBS:.4e})  error: {error:.2f}%  status: {status}")
                    if y_c: print(f"  y_c = {y_c:.4e}")
                    if y_t: print(f"  y_t = {y_t:.4f}")
                    if delta:
                        print(f"  Δy_u/y_u (non-holomorphic) = {delta*100:+.2f}%")
                    if status == "PASS":
                        print(f"  ✅ y_u CONVERGED — threshold correction verified!")
                        break
                
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n\nMonitor stopped.")
    else:
        # One-shot mode
        y_u, y_c, y_t = parse_spheno_yukawa(args.spheno_output)
        masses = parse_spheno_susy_masses(args.spheno_output)
        status, error = check_y_u_convergence(y_u, y_c, y_t)
        delta, info = compute_non_holomorphic_correction(masses)
        
        print(f"\nResults:")
        print(f"  y_u = {y_u:.4e}  (obs: {Y_U_OBS:.4e})")
        print(f"  Error: {error:.2f}%")
        print(f"  Status: {status}")
        if delta:
            print(f"  Non-holomorphic correction: {delta*100:+.2f}%")
            print(f"  Parameters: {info}")
        
        # CAT machine-readable output
        print(f"\nCAT_AV5_y_u: {y_u:.4e}")
        print(f"CAT_AV5_error: {error:.2f}")
        print(f"CAT_AV5_status: {status}")
        print(f"CAT_AV5_delta_yu: {delta*100 if delta else 0:.2f}")
        
        if status == "PASS":
            print(f"\n✅ Phase 7 AV-5 COMPLETE: y_u gap closed.")
        else:
            print(f"\n⚠️ Phase 7 AV-5 PENDING: need to iterate SPheno parameters.")

if __name__ == '__main__':
    main()