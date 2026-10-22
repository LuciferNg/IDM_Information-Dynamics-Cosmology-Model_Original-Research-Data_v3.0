(* MakeSPheno[] — ultra-minimal: only core SPheno files *)
(* Skips ALL 2-loop diagrammatic generation (hangs in SARAH 4.15.5) *)

Needs["SARAH`"];

(* Clean previous *)
If[DirectoryQ[ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"]],
  DeleteDirectory[ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"],
    DeleteContents -> True];
  Print["Previous output cleaned"]
];

Start["IDM_GUT"];
Print["Model loaded"];

(* ─── Skip ALL heavy 2-loop generation ─── *)
UseHiggs2LoopMSSM = False;
Use2LoopFromLiterature = False;
SA`Add2LoopCorrections = False;
SA`NoDecays = True;

(* Keep 1-loop masses and tree-level *)
SA`NoLoopMasses = False;
SA`OnlyLowEnergy = False;

Print["Options set: UseHiggs2LoopMSSM=False, SA`Add2LoopCorrections=False"];

Print["\nStarting MakeSPheno[]..."];
MakeSPheno[];

(* Verify *)
sphenoDir = FileNameJoin[{$sarahOutputDir, "EWSB", "SPheno"}];
Print["\nOutput: ", sphenoDir];
If[FileType[sphenoDir] === Directory,
  files = FileNames["*", sphenoDir];
  Print["=== GENERATION COMPLETE ==="];
  Print["Files: ", Length[files]];
  Print["Total size: ", Total[FileSize /@ files], " bytes"];
  Scan[Print["  ", StringReplace[#, sphenoDir <> "/" -> ""], " (", FileSize[#], " B)"]&, files],
  Print["ERROR: SPheno output not found"]
];

Print["\nDone."];
Exit[];
