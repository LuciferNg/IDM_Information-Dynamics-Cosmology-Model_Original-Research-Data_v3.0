#!/usr/bin/env python3
"""
CAT SPheno Fortran Injector — Phase 7.2 Defect-5
=================================================
Purpose: Auto-patch SARAH-generated SPheno Fortran code to bridge the
SARAH 4.15.5 ↔ SPheno 4.0.5 version gap.

Strategy:
1. Inject a minimal Settings module into the SPheno source tree
2. Fix module name references (_IDM_GUT suffix → standard names)
3. Compile with gfortran

Usage:
  python3 scripts/cat_spheno_inject.py [--sarah-output DIR] [--spheno-src DIR]
"""

import os, sys, re, shutil, subprocess

# ─── Configuration ───────────────────────────────────────────────────
SPHENO_ROOT = "/tmp/SPheno-4.0.5"
SPHENO_SRC = os.path.join(SPHENO_ROOT, "src")
SPHENO_INC = os.path.join(SPHENO_ROOT, "include")
SPHENO_BIN = os.path.join(SPHENO_ROOT, "bin", "SPheno")
SARAH_OUT = os.path.expanduser("~/.WolframEngine/Applications/SARAH/Output/IDM_GUT/EWSB/SPheno")
MSSM_BACKUP = "/tmp/SPheno_MSSM_backup"

# ─── Minimal Settings Module ─────────────────────────────────────────
SETTINGS_MODULE = """Module Settings
! CAT-injected: minimal Settings module for SARAH 4.15.5 ↔ SPheno 4.0.5
Use Control
Implicit None

! Convergence control
Integer, Save :: kont1 = 0
Integer, Save :: kont2 = 0
Integer, Save :: kont3 = 0

! Loop control
Logical, Save :: include_2loop_higgs_mssm = .True.
Logical, Save :: include_1loop_masses = .True.

! Precision
Real(dp), Save :: eps_i = 1.0e-8_dp
Real(dp), Save :: eps_f = 1.0e-10_dp

! Mass calculation
Integer, Save :: i_min = 1
Integer, Save :: i_max = 3
Logical, Save :: Only_Minimal_Output = .False.

! Decay control
Logical, Save :: include_1loop_decays = .False.
Logical, Save :: include_2loop_mssm = .True.

Contains

Subroutine Settings_Init()
  kont1 = 0; kont2 = 0; kont3 = 0
End Subroutine Settings_Init

End Module Settings
"""

# ─── Main logic ─────────────────────────────────────────────────────
def fix_module_names(filepath):
    """Fix _IDM_GUT module name suffixes in generated files"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    replacements = [
        ('RGEs_IDM_GUT', 'RGEs'),
        ('Couplings_IDM_GUT', 'Couplings'),
        ('LoopMasses_IDM_GUT', 'LoopMasses'),
        ('TreeLevelMasses_IDM_GUT', 'TreeLevelMasses'),
        ('LoopCouplings_IDM_GUT', 'LoopCouplings'),
        ('TreeLevel_Decays_IDM_GUT', 'TreeLevel_Decays'),
        ('Model_Data_IDM_GUT', 'Model_Data'),
    ]
    
    for old, new in replacements:
        content = re.sub(r'\b' + re.escape(old) + r'\b', new, content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    count = sum(content.count(new) for _, new in replacements)
    return count > 0

def copy_sarah_files():
    """Copy SARAH-generated files to SPheno src/"""
    if not os.path.isdir(SARAH_OUT):
        print(f"❌ SARAH output not found: {SARAH_OUT}")
        return False
    
    # Map SARAH filenames → SPheno filenames
    file_map = {
        'RGEs_IDM_GUT.f90': 'RGEs.F90',
        'Couplings_IDM_GUT.f90': 'Couplings.f90',
        'LoopMasses_IDM_GUT.f90': 'LoopMasses.F90',
        'TreeLevelMasses_IDM_GUT.f90': 'TreeLevelMasses.f90',
        'LoopCouplings_IDM_GUT.f90': 'LoopCouplings.f90',
        'TreeLevel_Decays_IDM_GUT.f90': 'TreeLevel_Decays.f90',
        'AddLoopFunctions.f90': 'AddLoopFunctions.f90',
        'Kinematics.f90': 'Kinematics.f90',
    }
    
    copied = 0
    for sarah_name, spheno_name in file_map.items():
        src = os.path.join(SARAH_OUT, sarah_name)
        dst = os.path.join(SPHENO_SRC, spheno_name)
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            copied += 1
            print(f"  📄 {sarah_name} → {spheno_name}")
        else:
            print(f"  ⚠️  Missing: {sarah_name}")
    
    # Copy TwoLoopMasses
    tl_src = os.path.join(SARAH_OUT, "TwoLoopMasses")
    tl_dst = os.path.join(SPHENO_SRC, "TwoLoopMasses")
    if os.path.isdir(tl_src):
        os.makedirs(tl_dst, exist_ok=True)
        for f in os.listdir(tl_src):
            if f.endswith('.f90'):
                shutil.copy2(os.path.join(tl_src, f), os.path.join(tl_dst, f))
                copied += 1
    
    print(f"  ✅ {copied} files copied")
    return copied > 0

def inject_settings_module():
    """Write the Settings module to SPheno src/"""
    dst = os.path.join(SPHENO_SRC, "Settings.F90")
    with open(dst, 'w') as f:
        f.write(SETTINGS_MODULE)
    print(f"  ✅ Settings module injected: {dst}")
    return True

def fix_all_module_names():
    """Fix module name references in all copied files"""
    files_to_fix = [
        'RGEs.F90', 'Couplings.f90', 'LoopMasses.F90',
        'TreeLevelMasses.f90', 'LoopCouplings.f90', 'TreeLevel_Decays.f90',
        'AddLoopFunctions.f90', 
    ]
    fixed = 0
    for fname in files_to_fix:
        fpath = os.path.join(SPHENO_SRC, fname)
        if os.path.isfile(fpath):
            if fix_module_names(fpath):
                fixed += 1
    
    # Also fix TwoLoopMasses files
    tl_dir = os.path.join(SPHENO_SRC, "TwoLoopMasses")
    if os.path.isdir(tl_dir):
        for fname in os.listdir(tl_dir):
            if fname.endswith('.f90'):
                fix_module_names(os.path.join(tl_dir, fname))
    
    print(f"  ✅ Module names fixed in {fixed} files")
    return fixed > 0

def compile_spheno():
    """Compile SPheno with gfortran"""
    print("\n  Compiling SPheno...")
    result = subprocess.run(
        ["make", "F90=gfortran", "-j4"],
        cwd=SPHENO_ROOT,
        capture_output=True, text=True, timeout=300
    )
    
    if os.path.isfile(SPHENO_BIN):
        print(f"  ✅ SPheno binary built: {SPHENO_BIN}")
        return True
    else:
        # Check for errors
        errors = [l for l in result.stderr.split('\n') if 'error' in l.lower()]
        for e in errors[:5]:
            print(f"  ❌ {e}")
        return False

def test_run():
    """Run SPheno with OAS input"""
    input_file = os.path.join(SPHENO_ROOT, "input", "LesHouches.in.OAS")
    if not os.path.isfile(input_file):
        print(f"  ⚠️  No OAS input file at {input_file}")
        return False
    
    result = subprocess.run(
        [SPHENO_BIN, input_file],
        cwd=SPHENO_ROOT,
        capture_output=True, text=True, timeout=60
    )
    
    spc = os.path.join(SPHENO_ROOT, "SPheno.spc")
    if os.path.isfile(spc) and os.path.getsize(spc) > 1000:
        # Check for Yukawa blocks
        with open(spc) as f:
            content = f.read()
        has_yu = "Block Yu" in content
        print(f"  ✅ SPheno run OK (SPheno.spc: {os.path.getsize(spc)}B, Yu: {has_yu})")
        return has_yu
    else:
        print(f"  ❌ SPheno run failed — check Messages.out")
        return False

# ─── Validate mode ────────────────────────────────────────────────
def validate_compile(filepath):
    """Test-compile a single Fortran file with gfortran"""
    if not os.path.isfile(filepath):
        return False, "File not found"
    
    basename = os.path.basename(filepath)
    result = subprocess.run(
        ["gfortran", "-c", "-O", "-fsyntax-only",
         "-J" + SPHENO_INC, "-I" + SPHENO_INC,
         filepath],
        cwd=SPHENO_SRC, capture_output=True, text=True, timeout=30
    )
    
    if result.returncode == 0:
        return True, ""
    else:
        errors = []
        for line in result.stdout.split('\n'):
            if 'Error:' in line or 'Fatal' in line:
                errors.append(line.strip())
        return False, "; ".join(errors[:3])

def run_validate():
    """Validate all generated Fortran files"""
    print("\n[VALIDATE] Testing generated Fortran files...")
    files_to_check = [
        'RGEs.F90', 'Couplings.f90', 'LoopMasses.F90',
        'TreeLevelMasses.f90', 'LoopCouplings.f90', 'TreeLevel_Decays.f90'
    ]
    passed = 0; failed = 0
    for fname in files_to_check:
        fpath = os.path.join(SPHENO_SRC, fname)
        if not os.path.isfile(fpath):
            print(f"  ⚠️  {fname}: not found (skipped)")
            continue
        ok, err = validate_compile(fpath)
        if ok:
            print(f"  ✅ {fname}: syntax OK")
            passed += 1
        else:
            print(f"  ❌ {fname}: {err}")
            failed += 1
    print(f"  Validate: {passed} passed, {failed} failed")
    return failed == 0

# ─── Main ────────────────────────────────────────────────────────────
def main():
    import argparse
    parser = argparse.ArgumentParser(description="CAT SPheno Fortran Injector")
    parser.add_argument('--validate', action='store_true',
                       help='Validate generated Fortran syntax')
    parser.add_argument('--inject', action='store_true',
                       help='Inject Settings module and fix names')
    parser.add_argument('--compile', action='store_true',
                       help='Compile SPheno after injection')
    parser.add_argument('--all', action='store_true', default=True,
                       help='Do everything (default)')
    args = parser.parse_args()
    
    # If --validate only, skip everything else
    if args.validate and not (args.inject or args.compile or args.all):
        run_validate()
        return
    
    print("=" * 60)
    print("CAT SPheno Fortran Injector — Phase 7.2 Defect-5")
    print("=" * 60)
    
    # Check if SARAH output exists
    sarah_files_exist = os.path.isdir(SARAH_OUT) and any(f.endswith('.f90') for f in os.listdir(SARAH_OUT))
    
    if not sarah_files_exist:
        print("\n  ⚠️  No SARAH-generated files found at:")
        print(f"     {SARAH_OUT}")
        print("  Run MakeSPheno[] in Wolfram Engine first.")
        if not args.all:
            return
        # If --all, try to use existing files in SPheno src
        print("  Attempting to use existing SPheno src files...")
    
    if args.all or args.inject:
        print("\n[1/5] Backing up MSSM model...")
        os.makedirs(MSSM_BACKUP, exist_ok=True)
        for f in ['RGEs.F90', 'Couplings.f90', 'LoopMasses.F90']:
            src = os.path.join(SPHENO_SRC, f)
            if os.path.isfile(src):
                shutil.copy2(src, os.path.join(MSSM_BACKUP, f))
        print("  ✅ MSSM backed up")
        
        if sarah_files_exist:
            print("\n[2/5] Copying SARAH-generated files...")
            if not copy_sarah_files():
                print("  ⚠️  Some files missing, continuing...")
        
        print("\n[3/5] Injecting Settings module...")
        inject_settings_module()
        fix_all_module_names()
        
        if args.validate:
            print("\n  Running syntax validation...")
            run_validate()
    
    if args.all or args.compile:
        print("\n[4/5] Compiling SPheno...")
        if not compile_spheno():
            print("\n  Retrying with verbose errors...")
            result = subprocess.run(
                ["make", "F90=gfortran"],
                cwd=SPHENO_ROOT,
                capture_output=True, text=True, timeout=300
            )
            for line in result.stdout.split('\n'):
                if 'Fatal Error' in line or 'Error:' in line:
                    print(f"  ⚠️  {line.strip()}")
            return
        
        print("\n[5/5] Running SPheno with OAS input...")
        test_run()
    
    print(f"\n{'=' * 60}")
    print("CAT Injector complete.")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()