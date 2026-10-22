(* MakeSPheno[] — standalone OAS IDM_GUT SPheno package *)
(* Skips 2-loop diagrammatic Higgs to avoid SARAH 4.15.5 CPU sink *)

Needs["SARAH`"];

(* Clean previous output *)
If[DirectoryQ[ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"]],
  DeleteDirectory[ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"],
    DeleteContents -> True];
  Print["Previous output cleaned"]
];

(* Load the IDM_GUT model *)
Start["IDM_GUT"];
Print["Model loaded: IDM_GUT"];

(* ───── SARAH options ───── *)
SA`NoDecays = True;              (* skip decays — not needed for y_u closure *)
SA`OnlyLowEnergy = False;        (* full RGE from GUT to M_Z *)
SA`NoLoopMasses = False;         (* keep 1-loop masses *)
UseHiggs2LoopMSSM = False;          (* skip 2-loop diagrammatic — CPU sink in SARAH 4.15.5 *)
SA`Precision = 2;                (* moderate precision *)

(* Generate SPheno Fortran code *)
Print["Starting MakeSPheno[] — standalone package..."];
MakeSPheno[];

(* Verify output *)
sphenoDir = FileNameJoin[{$sarahOutputDir, "EWSB", "SPheno"}];
If[FileType[sphenoDir] === Directory,
  files = FileNames["*", sphenoDir];
  Print["=== GENERATION COMPLETE ==="];
  Print["Files: ", Length[files]];
  Print["Total size: ", Total[FileSize /@ files], " bytes"];
  (* List all files *)
  Scan[Print["  ", StringReplace[#, sphenoDir <> "/" -> ""], " (", FileSize[#], " B)"]&, files],
  Print["ERROR: SPheno output not found at: ", sphenoDir]
];

Exit[];
