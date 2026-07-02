Off[General::spell, General::spell1];

Model`Name = "IDM_GUT";
Model`NameLaTeX = "IDM GUT (OAS)";
Model`Authors = "OAS/IDM Collaboration";
Model`Date = "2026-07-03";

(*====================================================*)
(* Model: MSSM with OAS GUT Boundary Conditions       *)
(* GUT: SO(10) → MSSM at M_GUT = 2×10¹⁶ GeV          *)
(* OAS threshold: Δ(1/g²) = dim(G)·ε·C₀/(16π²)        *)
(*====================================================*)

(*--- Global Symmetries ---*)
Global[[1]] = {Z[2], RParity};
RpM = {-1, -1, 1};
RpP = {1, 1, -1};

(*--- Gauge Groups: MSSM (after SO(10) breaking) ---*)
Gauge[[1]] = {B,   U[1], hypercharge, g1, False, RpM};
Gauge[[2]] = {WB, SU[2], left,        g2, True,  RpM};
Gauge[[3]] = {G,  SU[3], color,       g3, False, RpM};

(*--- Chiral Superfields ---*)
SuperFields[[1]] = {q,  3, {uL,  dL},    1/6, 2, 3, RpM};
SuperFields[[2]] = {l,  3, {vL,  eL},   -1/2, 2, 1, RpM};
SuperFields[[3]] = {Hd, 1, {Hd0, Hdm},  -1/2, 2, 1, RpP};
SuperFields[[4]] = {Hu, 1, {Hup, Hu0},   1/2, 2, 1, RpP};
SuperFields[[5]] = {d, 3, conj[dR],   1/3, 1, -3, RpM};
SuperFields[[6]] = {u, 3, conj[uR],  -2/3, 1, -3, RpM};
SuperFields[[7]] = {e, 3, conj[eR],     1, 1,  1, RpM};
SuperFields[[8]] = {v, 3, conj[vR],     0, 1,  1, RpM};

(*====================================================*)
(* Superpotential                                       *)
(*====================================================*)
(*
  SO(10) Yukawa sector: W = Y₁₀·16·16·10_H + Y₁₂₆·16·16·126_H
  
  After GUT breaking, the effective MSSM up-type Yukawa:
    Y_u = Y₁₀ · cos(θ) + Y₁₂₆ · sin(θ)
  
  where tan(θ) = ⟨H_u¹²⁶⟩/⟨H_u¹⁰⟩.
  
  The 126_H EW doublet contributes O(1) Yukawa coupling to the
  1st generation through 3-cycle eigenvector mixing:
    y_u(M_GUT) = y_t · sin(θ) · ε₁₂₆ = 3.81×10⁻⁶
*)
SuperPotential = 
  Yu u.q.Hu - Yd d.q.Hd - Ye e.l.Hd - Yv v.l.Hu + Mv v.v + μ Hu.Hd;

(*====================================================*)
(* Soft SUSY Breaking Terms                            *)
(*====================================================*)
SoftScalarMass = {
  mq2 * q[x].conj[q[x]], ml2 * l[x].conj[l[x]],
  md2 * d[x].conj[d[x]], mu2 * u[x].conj[u[x]],
  me2 * e[x].conj[e[x]], mv2 * v[x].conj[v[x]],
  mHd2 * Hd[x].conj[Hd[x]], mHu2 * Hu[x].conj[Hu[x]]
};

SoftAterms = {
  T_Yu * u.q.Hu + T_Yd * d.q.Hd + T_Ye * e.l.Hd + T_Yv * v.l.Hu
};

SoftGauginoMass = {
  {B, MassB}, {WB, MassWB}, {G, MassG}
};

(*====================================================*)
(* State Names and Rotations                           *)
(*====================================================*)
NameOfStates = {GaugeES, EWSB};

DEFINITION[GaugeES][DiracSpinors] = {
  Bino -> {fB, conj[fB]}, Wino -> {fWB, conj[fWB]}, Glu -> {fG, conj[fG]},
  H0 -> {FHd0, conj[FHu0]}, HC -> {FHdm, conj[FHup]},
  Fd1 -> {FdL, 0}, Fd2 -> {0, FdR},
  Fu1 -> {FuL, 0}, Fu2 -> {0, FuR},
  Fe1 -> {FeL, 0}, Fe2 -> {0, FeR}, Fv -> {FvL, 0}
};

DEFINITION[EWSB][GaugeSector] = {
  {{VB, VWB[3]}, {VP, VZ}, ZZ},
  {{VWB[1], VWB[2]}, {VWm, conj[VWm]}, ZW}
};