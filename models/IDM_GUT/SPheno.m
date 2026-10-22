(* ::Package:: *)

(* SARAH model file for IDM_GUT (OAS SO(10) → SM effective theory) *)
(* Generated: 2026-07-03 *)
(* Phase 7: OAS SPheno Pipeline *)

(* ─── Renormalization Group Input ─── *)
MINPAR={{1,m0},
         {2,m12},
         {3,TanBeta},
         {4,SignumMu},
         {5,Azero}};

(* ─── Custom LesHouches Blocks for OAS boundary control ─── *)
(* These blocks can be set in LesHouches.in.OAS to override
   the hardcoded OAS GUT-scale boundary conditions.           *)
(*                                                           *)
ReadBlocks = {GUTSCALE, GAUGEORIGIN, YUKAWAORIGIN};

(* Block GUTSCALE:  1  M_GUT  (default: 2.0E16) *)
(* Block GAUGEORIGIN:
   1  g1_GUT  (default: 0.570)
   2  g2_GUT  (default: 0.713)
   3  g3_GUT  (default: 0.710) *)
(* Block YUKAWAORIGIN:
  11  y_t_GUT  (default: 0.0553)
  12  y_c_GUT  (default: 9.07E-5)
  13  y_u_GUT  (default: 3.81E-6)
  14  y_tau_GUT (default: 0.0154)
  15  y_b_GUT  (default: 0.0535)
  16  y_s_GUT  (default: 3.66E-4)
  17  y_d_GUT  (default: 6.77E-6)
  18  y_mu_GUT (default: 1.54E-4)
  19  y_e_GUT  (default: 2.71E-7) *)

RealParameters = {TanBeta, m0, m12, Azero, SignumMu};
ParametersToSolveTadpoles = {\[Mu], B[\[Mu]]};

RenormalizationScaleFirstGuess = m0^2 + 4 m12^2;
RenormalizationScale = Sqrt[(mq2[3, 3] + (vu^2*conj[Yu[3, 3]]*Yu[3, 3])/2)*
  (mu2[3, 3] + (vu^2*conj[Yu[3, 3]]*Yu[3, 3])/2) -
  ((vd*\[Mu]*conj[Yu[3, 3]] - vu*conj[T[Yu]][3, 3])*
   (vd*conj[\[Mu]]*Yu[3, 3] - vu*T[Yu][3, 3]))/2];

(* ─── GUT scale condition ─── *)
(* Use GAUGEORIGIN block [1] if defined, else OAS hardcoded g1=0.570 *)
ConditionGUT = If[DefinedBlock[GAUGEORIGIN], GAUGEORIGIN[1], 0.570] == g1;

(* ─── GUT-scale boundary conditions ─── *)
(* Each parameter reads from custom block if defined, else OAS default *)
BoundaryHighScale = {
  {g1, If[DefinedBlock[GAUGEORIGIN], GAUGEORIGIN[1], 0.570]},
  {g2, If[DefinedBlock[GAUGEORIGIN], GAUGEORIGIN[2], 0.713]},
  {g3, If[DefinedBlock[GAUGEORIGIN], GAUGEORIGIN[3], 0.710]},
  
  {Yu[1,1], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[13], 3.81e-6]},
  {Yu[2,2], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[12], 9.07e-5]},
  {Yu[3,3], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[11], 0.0553]},
  
  {Yd[1,1], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[17], 6.77e-6]},
  {Yd[2,2], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[16], 3.66e-4]},
  {Yd[3,3], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[15], 0.0535]},
  
  {Ye[1,1], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[19], 2.71e-7]},
  {Ye[2,2], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[18], 1.54e-4]},
  {Ye[3,3], If[DefinedBlock[YUKAWAORIGIN], YUKAWAORIGIN[14], 0.0154]},
  
  {Yv, 0},
  {Mv, 1e15},
  
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
(* Disabled: UseHiggs2LoopMSSM = True;     (* 2-loop diagrammatic — skip for CLI generation *) *)

(* ─── SPheno output: write used boundary values ─── *)
OutputBlocks = {GUTSCALE, GAUGEORIGIN, YUKAWAORIGIN};

(* ─── Decay and fine-tuning settings ─── *)
QuadruplePrecision = {};
ListDecayParticles = Automatic;
ListDecayParticles3B = Automatic;
DEFINITION[MatchingConditions] = Default[THDMII];

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
