(* Full MakeSPheno[] — clean SARAH, unlimited timeout *)

Needs["SARAH`"];

(* Clean output *)
outDir = ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"];
If[DirectoryQ[outDir], DeleteDirectory[outDir, DeleteContents -> True]; Print["Cleaned"]];

Start["IDM_GUT"];

(* UseHiggs2LoopMSSM already commented out in SPheno.m; 2-loop still runs but completes *)
SA`NoDecays = True;
SA`OnlyLowEnergy = False;
SA`NoLoopMasses = False;
SA`Precision = 2;

Print["Starting MakeSPheno[] — expect 8-12 minutes"];
t1 = AbsoluteTime[];
MakeSPheno[];
t2 = AbsoluteTime[];
Print["Elapsed: ", t2 - t1, " s"];

(* Verify *)
sphenoDir = FileNameJoin[{$sarahOutputDir, "EWSB", "SPheno"}];
Print["\n=== OUTPUT ==="];
If[DirectoryQ[sphenoDir],
  allFiles = FileNames["*", sphenoDir];
  f90Files = Select[allFiles, StringEndsQ[#, ".f90"] || StringEndsQ[#, ".F90"]&];
  Print["All files: ", Length[allFiles]];
  Print["Source files: ", Length[f90Files]];
  
  (* Check critical framework files *)
  critical = {"SPhenoIDM_GUT.f90", "Makefile", "InputOutput_IDM_GUT.f90", 
              "Model_Data_IDM_GUT.f90", "Settings.f90", "TwoLoopHiggsMass.f90",
              "SugraRuns_IDM_GUT.f90", "Boundaries_IDM_GUT.f90",
              "LowEnergy_IDM_GUT.f90", "FineTuning_IDM_GUT.f90",
              "Unitarity_IDM_GUT.f90", "HiggsCS_IDM_GUT.f90"};
  Scan[
    If[FileExistsQ[FileNameJoin[{sphenoDir, #}]],
      Print["  ✅ ", #, " (", FileSize[FileNameJoin[{sphenoDir, #}]], " B)"],
      Print["  ❌ ", #]
    ]&,
    critical
  ];
];

Exit[];
