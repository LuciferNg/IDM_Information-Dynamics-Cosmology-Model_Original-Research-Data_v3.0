MINPAR={{1,m0},
         {2,m12},
         {3,TanBeta},
         {4,SignumMu},
         {5,Azero}};

RealParameters = {TanBeta, m0, m12, Azero, SignumMu};
ParametersToSolveTadpoles = {\[Mu], B[\[Mu]]};

RenormalizationScaleFirstGuess = m0^2 + 4 m12^2;
RenormalizationScale = Sqrt[(mq2[3, 3] + (vu^2*conj[Yu[3, 3]]*Yu[3, 3])/2)*
  (mu2[3, 3] + (vu^2*conj[Yu[3, 3]]*Yu[3, 3])/2) -
  ((vd*\[Mu]*conj[Yu[3, 3]] - vu*conj[T[Yu]][3, 3])*
   (vd*conj[\[Mu]]*Yu[3, 3] - vu*T[Yu][3, 3]))/2];

(*
  OAS GUT scale: M_GUT = 2×10¹⁶ GeV
  Use fixed gauge coupling as GUT scale condition
*)
ConditionGUTscale = g1 == 0.570;

BoundaryHighScale = {
  (* GUT-scale gauge couplings with OAS threshold *)
  {g1, 0.570},
  {g2, 0.713},
  {g3, 0.710},
  
  (* GUT-scale Yukawa couplings from SO(10) 10_H ⊕ 126_H *)
  (*
    126_H EW doublet O(1) Yukawa + 3-cycle eigenvector mixing:
    
    The up-type Yukawa matrix at M_GUT is:
    Y_u = Y₁₀ · cos(θ) + Y₁₂₆ · sin(θ)
    
    where tan(θ) = ⟨H_u¹²⁶⟩/⟨H_u¹⁰⟩ is the 126_H/10_H VEV ratio.
    
    The 3×3 matrices have hierarchical structures:
    - Y₁₀ is rank-1 dominated: (Y₁₀)ᵢⱼ ≈ y_t · δᵢ₃δⱼ₃
    - Y₁₂₆ has Fritzsch-like texture with off-diagonal mixing
    
    3-cycle eigenvector mixing → 1st gen mass from 126_H:
    y_u(GUT) = y_t · sin(θ) · ε₁₂₆ = 3.81×10⁻⁶
    
    This is only 1.20× the MSSM baseline (3.18×10⁻⁶),
    a 20% correction well within the expected 126_H range.
    
    Reference: Phase 4 Yukawa hierarchy, Report 5.0 §9.12
  *)
  {Yu[1,1], 3.81e-6},   (* y_u from 126_H EW doublet + 3-cycle mixing *)
  {Yu[2,2], 9.07e-5},   (* y_c from 10_H × rS = M_GUT/M_Pl *)
  {Yu[3,3], 0.0553},    (* y_t from 10_H *)
  {Yd[1,1], 6.77e-6},   (* y_d *)
  {Yd[2,2], 3.66e-4},   (* y_s *)
  {Yd[3,3], 0.0535},    (* y_b from 126_H C₄₅[d] = 3/5 *)
  {Ye[1,1], 2.71e-7},   (* y_e *)
  {Ye[2,2], 1.54e-4},   (* y_μ *)
  {Ye[3,3], 0.0154},    (* y_τ *)
  
  (* Neutrino sector — decoupled for y_u calculation *)
  {Yv, 0},
  {Mv, 1e15},           (* RH neutrino mass ~ GUT scale *)
  
  (* mSUGRA boundary conditions *)
  {T[Ye], Azero*Ye},
  {T[Yd], Azero*Yd},
  {T[Yu], Azero*Yu},
  {T[Yv], 0},
  {mq2, DIAGONAL m0^2},
  {ml2, DIAGONAL m0^2},
  {md2, DIAGONAL m0^2},
  {mu2, DIAGONAL m0^2},
  {me2, DIAGONAL m0^2},
  {mv2, 0},
  {mHd2, m0^2},
  {mHu2, m0^2},
  {MassB, m12},
  {MassWB, m12},
  {MassG, m12}
};

InitializationValues = {
  {\[Mu], 0},
  {B[\[Mu]], 0}
};

(* Use 2-loop MSSM Higgs mass corrections *)
UseHiggs2LoopMSSM = True;

QuadruplePrecision = {};

ListDecayParticles = Automatic;
ListDecayParticles3B = Automatic;

DEFINITION[MatchingConditions] = Default[THDMII];

(* SUSY scale input *)
EXTPAR = {{1, M1input},
          {2, M2input},
          {3, M3input},
          {23, Muinput},
          {24, MA2input},
          {25, TanBeta}};

ParametersToSolveTadpolesLowScaleInput = {mHd2, mHu2};

BoundaryLowScaleInput = {
  {MassB, M1input},
  {MassWB, M2input},
  {MassG, M3input},
  {\[Mu], Muinput},
  {B[\[Mu]], MA2input/(TanBeta + 1/TanBeta)},
  {vd, Sqrt[4 mz2/(g1^2+g2^2)]*Cos[ArcTan[TanBeta]]},
  {vu, Sqrt[4 mz2/(g1^2+g2^2)]*Sin[ArcTan[TanBeta]]}
};

(* mSUGRA input values matching SPheno MSSM run *)
DefaultInputValues[1] = {m0 -> 1000, m12 -> 1000, TanBeta -> 10, SignumMu -> 1, Azero -> -1500};

NeglectLoopsInvolving = {};

IncludeFineTuning = True;
FineTuningParameters = {
  {m0, 1/2}, {m12, 1}, {Azero, 1}, {\[Mu], 1}, {B[\[Mu]], 1}
};

RenConditionsDecays = {
  {dCosTW, 1/2*Cos[ThetaW] * (PiVWm/(MVWM^2) - PiVZ/(mVZ^2))},
  {dSinTW, -dCosTW/Tan[ThetaW]},
  {dg2, 1/2*g2*(derPiVPheavy0 + PiVPlightMZ/MVZ^2 - (-(PiVWm/MVWm^2) + PiVZ/MVZ^2)/Tan[ThetaW]^2 + (2*PiVZVP*Tan[ThetaW])/MVZ^2)},
  {dg1, dg2*Tan[ThetaW]+g2*dSinTW/Cos[ThetaW]-dCosTW*g2*Tan[ThetaW]/Cos[ThetaW]}
};

AddTreeLevelUnitarityLimits = True;
RemoveParticlesFromScattering = {Sd, Se, Sv};