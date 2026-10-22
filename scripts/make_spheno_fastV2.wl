(* Load SARAH and generate SPheno code — optimised for speed *)
(* SARAH.m already patched for CLI *)
(* Just load it directly *)
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

(* ───── SARAH options for fast SPheno generation ───── *)
SA`NoDecays = True;           (* skip all decay calculations *)
SA`OnlyLowEnergy = False;     (* full RGE from GUT to M_Z *)
SA`NoLoopMasses = False;      (* keep 1-loop masses *)
(* Set decay output to minimal *)
SPheno`WriteBranchingRatios = False;
SPheno`WriteCrossSections = False;

(* Set mass precision *)
SA`Precision = 2;             (* moderate precision *)

(* Generate SPheno Fortran code *)
Print["Starting MakeSPheno[] with optimised settings..."];
MakeSPheno[];

(* Verify output *)
sphenoDir = FileNameJoin[{$sarahOutputDir, "EWSB", "SPheno"}];
If[FileType[sphenoDir] === Directory,
  files = FileNames["*.f90", sphenoDir];
  Print["=== GENERATION COMPLETE ==="];
  Print["Files: ", Length[files]];
  Print["Total size: ", Total[FileSize /@ files], " bytes"];
  Scan[Print[FilenameSplit[#][[-1]], " (", FileSize[#], " B)"]&, files],
  Print["ERROR: SPheno output not found"]
];

Exit[];