(* MakeSPheno — wait until full completion *)

Needs["SARAH`"];
Start["IDM_GUT"];

SA`NoDecays = True;
SA`Precision = 2;

Print["Starting MakeSPheno[] at ", DateString[]];
t1 = AbsoluteTime[];
MakeSPheno[];
t2 = AbsoluteTime[];
Print["Completed in ", Round[t2 - t1], " seconds at ", DateString[]];

(* Full listing *)
sphenoDir = FileNameJoin[{$sarahOutputDir, "EWSB", "SPheno"}];
Print["\n=== FULL OUTPUT ==="];
If[DirectoryQ[sphenoDir],
  allFiles = FileNames["*", sphenoDir, Infinity];
  Print["Total: ", Length[allFiles], " files / ", 
    Total[FileSize /@ Select[allFiles, FileType[#] === File&]], " bytes"];
  Scan[Print["  ", StringReplace[#, sphenoDir <> "/" -> ""], " (", FileSize[#], " B)"]&,
    Sort[allFiles]];
];
Exit[];
