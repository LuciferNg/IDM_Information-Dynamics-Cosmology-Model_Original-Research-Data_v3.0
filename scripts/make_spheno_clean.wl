(* MakeSPheno[] — OAS IDM_GUT standalone generation *)
(* Explicitly skips 2-loop diagrammatic Higgs (CPU sink in SARAH 4.15.5) *)

Needs["SARAH`"];

(* Clean ALL previous SARAH output for this model *)
outDir = ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"];
If[DirectoryQ[outDir],
  DeleteDirectory[outDir, DeleteContents -> True];
  Print["Previous output cleaned"];
];

(* Load model *)
Start["IDM_GUT"];
Print["Model loaded: IDM_GUT"];

(* ─── Critical flags ─── *)
UseHiggs2LoopMSSM = False;     (* skip 2-loop diagrammatic Higgs — hangs *)
SA`NoDecays = True;             (* skip decays *)
SA`OnlyLowEnergy = False;       (* full boundary-to-MZ running *)
SA`NoLoopMasses = False;        (* keep 1-loop masses *)
SA`Precision = 2;

Print["Flags set. Starting MakeSPheno[]..."];
MakeSPheno[];

(* Verify output *)
sphenoDir = FileNameJoin[{$sarahOutputDir, "EWSB", "SPheno"}];
If[FileType[sphenoDir] === Directory,
  files = FileNames["*", sphenoDir];
  subdirFiles = Join[files, Flatten[FileNames["*", #]& /@ Select[files, DirectoryQ]]];
  Print["\n=== GENERATION COMPLETE ==="];
  Print["Total items: ", Length[subdirFiles]];
  Print["Total size: ", Total[FileSize /@ Select[subdirFiles, FileType[#] === File]], " bytes"];
  Scan[Print["  ", StringReplace[#, $sarahOutputDir <> "/" -> ""], " (", FileSize[#], " B)"]&, Select[subdirFiles, FileType[#] === File]],
  Print["\nERROR: SPheno output not found at: ", sphenoDir];
  Print["Check ", FileNameJoin[{$sarahOutputDir, "EWSB"}], " for contents"];
];

Exit[];
