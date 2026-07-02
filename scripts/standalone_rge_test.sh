#!/bin/bash
# standalone_rge_test.sh — Compile SARAH-generated RGEs module standalone
# Uses the existing 13 files from the partial generation
set -e

SARAH_OUT="$HOME/.WolframEngine/Applications/SARAH/Output/IDM_GUT/EWSB/SPheno"
WORK=/tmp/oas_rge_test
mkdir -p $WORK
cd $WORK

echo "=== Standalone OAS RGE Fortran Test ==="
echo "Copying SARAH-generated files..."

cp "$SARAH_OUT/RGEs_IDM_GUT.f90" RGEs.f90
cp "$SARAH_OUT/AddLoopFunctions.f90" .
cp "$SARAH_OUT/Kinematics.f90" .

# Create minimal Control module needed by RGEs
cat > Control.f90 << 'EOF'
Module Control
  Integer, Parameter :: dp = Selected_Real_Kind(15, 307)
  Real(dp), Parameter :: Pi = 3.1415926535897932384626433832795_dp
  Complex(dp), Parameter :: i_ = (0._dp, 1._dp)
  Real(dp), Parameter :: sqrt2 = 1.4142135623730950488016887242097_dp
  Real(dp), Parameter :: degree = Pi / 180._dp
End Module Control
EOF

# Create minimal Mathematics module needed by RGEs
cat > Mathematics.f90 << 'EOF'
Module Mathematics
  Use Control
  Implicit None
  Real(dp), Parameter :: eps0 = 1.0e-8_dp
Contains
  Subroutine Check_Convergence(msg, val1, val2, tol, kont)
    Character(len=*), Intent(in) :: msg
    Real(dp), Intent(in) :: val1, val2, tol
    Integer, Intent(out) :: kont
    If (Abs(val1 - val2) < tol) Then; kont = 0; Else; kont = 1; End If
  End Subroutine
  Subroutine AddToSelection(sel, val)
    Integer, Intent(inout) :: sel
    Integer, Intent(in) :: val
    sel = Ior(sel, val)
  End Subroutine
End Module Mathematics
EOF

# Create minimal Model_Data for RGEs
cat > Model_Data.f90 << 'EOF'
Module Model_Data
  Use Control
  Implicit None
  Real(dp), Save :: g1, g2, g3
  Real(dp), Save :: Yu(3,3), Yd(3,3), Ye(3,3)
  Real(dp), Save :: scale
  Integer, Save :: kont = 0
  Real(dp), Parameter :: M_GUT = 2.0e16_dp
Contains
  Subroutine Model_Data_Init()
    g1 = 0.704_dp; g2 = 0.704_dp; g3 = 0.699_dp
    Yu = 0._dp; Yu(1,1) = 3.81e-6_dp; Yu(2,2) = 1.62e-3_dp; Yu(3,3) = 0.497_dp
    Yd = 0._dp; Yd(1,1) = 4.86e-5_dp; Yd(2,2) = 9.23e-4_dp; Yd(3,3) = 0.0524_dp
    Ye = 0._dp; Ye(1,1) = 2.06e-5_dp; Ye(2,2) = 4.25e-3_dp; Ye(3,3) = 0.0718_dp
    kont = 0
  End Subroutine
End Module Model_Data
EOF

# Compile modules in order
echo "Compiling..."
gfortran -c -O Control.f90 2>&1 | head -3
gfortran -c -O Mathematics.f90 2>&1 | head -3
gfortran -c -O Model_Data.f90 2>&1 | head -3
gfortran -c -O AddLoopFunctions.f90 2>&1 | head -3
gfortran -c -O Kinematics.f90 2>&1 | head -3
gfortran -c -O RGEs.f90 2>&1 | head -3
echo "=== Build complete ==="
ls -la *.o *.mod 2>/dev/null