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
(* GUT-scale boundary conditions from SO(10) 16-plet:
   3 generations, each 16 of SO(10) *)
SuperFields[[1]] = {q,  3, {uL,  dL},    1/6, 2, 3, RpM};  (* LH quarks *)
SuperFields[[2]] = {l,  3, {vL,  eL},   -1/2, 2, 1, RpM};  (* LH leptons *)
SuperFields[[3]] = {Hd, 1, {Hd0, Hdm},  -1/2, 2, 1, RpP};   (* down-type Higgs *)
SuperFields[[4]] = {Hu, 1, {Hup, Hu0},   1/2, 2, 1, RpP};   (* up-type Higgs *)

(* RH fermion superfields *)
SuperFields[[5]] = {d, 3, conj[dR],   1/3, 1, -3, RpM};  (* RH down quarks *)
SuperFields[[6]] = {u, 3, conj[uR],  -2/3, 1, -3, RpM};  (* RH up quarks *)
SuperFields[[7]] = {e, 3, conj[eR],     1, 1,  1, RpM};  (* RH charged leptons *)
SuperFields[[8]] = {v, 3, conj[vR],     0, 1,  1, RpM};  (* RH neutrinos *)

(*====================================================*)
(* Superpotential                                       *)
(*====================================================*)
(*
  GUT-scale Yukawa structure from SO(10):
  - 10_H gives up-type Yukawa (Y10 → Yu)
  - 126_H gives down-type/charged-lepton Yukawa (Y126 → Yd, Ye)
  - 126_H_bar also contributes to bottom/neutrino hierarchy
  
  OAS 126_H EW doublet → O(1) Yukawa coupling
  3-cycle eigenvector mixing → y_u suppression via 10_H/126_H operator hierarchy
*)

SuperPotential = 
  (* Up-type Yukawa: from 10_H of SO(10) *)
  Yu u.q.Hu - 
  (* Down-type Yukawa: from 126_H of SO(10) *)
  Yd d.q.Hd - 
  (* Charged lepton Yukawa: from 126_H → SU(5) 45-plet *)
  Ye e.l.Hd - 
  (* Neutrino Yukawa: from 126_H, Type-I seesaw *)
  Yv v.l.Hu + 
  (* RH neutrino Majorana mass: from 126_H VEV *)
  Mv v.v +
  (* μ-term: MSSM Higgs mass parameter *)
  μ Hu.Hd;

(*====================================================*)
(* Soft SUSY Breaking Terms (GUT-scale mSUGRA)         *)
(*====================================================*)

(* Universal scalar mass: m₀ = 1 TeV at M_GUT *)
SoftScalarMass = {
  mq2 * q[x].conj[q[x]],          (* squark doublets *)
  ml2 * l[x].conj[l[x]],          (* slepton doublets *)
  md2 * d[x].conj[d[x]],          (* RH down squarks *)
  mu2 * u[x].conj[u[x]],          (* RH up squarks *)
  me2 * e[x].conj[e[x]],          (* RH sleptons *)
  mv2 * v[x].conj[v[x]],          (* RH sneutrinos *)
  mHd2 * Hd[x].conj[Hd[x]],      (* down-type Higgs *)
  mHu2 * Hu[x].conj[Hu[x]]       (* up-type Higgs *)
};

(* Universal trilinear couplings: A₀ = -1.5 TeV at M_GUT *)
SoftAterms = {
  T_Yu * u.q.Hu + T_Yd * d.q.Hd + T_Ye * e.l.Hd + T_Yv * v.l.Hu
};

(* Gaugino masses: M₁/₂ = 1 TeV at M_GUT *)
SoftGauginoMass = {
  {B, MassB},      (* bino *)
  {WB, MassWB},    (* wino *)
  {G, MassG}       (* gluino *)
};

(*====================================================*)
(* State Names and Rotations                           *)
(*====================================================*)

NameOfStates = {GaugeES, EWSB};

(* Gauge Eigenstates *)
DEFINITION[GaugeES][DiracSpinors] = {
  Bino  -> {fB, conj[fB]},
  Wino  -> {fWB, conj[fWB]},
  Glu   -> {fG, conj[fG]},
  H0    -> {FHd0, conj[FHu0]},
  HC    -> {FHdm, conj[FHup]},
  Fd1   -> {FdL, 0},
  Fd2   -> {0, FdR},
  Fu1   -> {FuL, 0},
  Fu2   -> {0, FuR},
  Fe1   -> {FeL, 0},
  Fe2   -> {0, FeR},
  Fv    -> {FvL, 0}
};

(* EWSB Sector *)
DEFINITION[EWSB][GaugeSector] = {
  {{VB, VWB[3]}, {VP, VZ}, ZZ},
  {{VWB[1], VWB[2]}, {VWm, conj[VWm]}, ZW}
};