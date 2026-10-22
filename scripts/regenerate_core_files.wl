(* Regenerate 13 core SPheno files — clean SARAH 4.15.5 *)

Needs["SARAH`"];

(* Clean output *)
outDir = ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"];
If[DirectoryQ[outDir], DeleteDirectory[outDir, DeleteContents -> True]; Print["Cleaned"]];

Start["IDM_GUT"];

UseHiggs2LoopMSSM = False;  (* Will be overridden by SPheno.m; skip 2-loop diagrammatic *)
SA`NoDecays = True;
SA`OnlyLowEnergy = False;
SA`NoLoopMasses = False;
SA`Precision = 2;

Print["MakeSPheno[]..."];
MakeSPheno[];

(* Show result *)
sphenoDir = FileNameJoin[{$sarahOutputDir, "EWSB", "SPheno"}];
Print["\n=== OUTPUT ==="];
files = FileNames["*", sphenoDir];
Print["Files: ", Length[files]];
Scan[Print["  ", StringReplace[#, sphenoDir <> "/" -> ""], " (", FileSize[#], " B)"]&, 
  Select[files, FileType[#] === File]];
Exit[];
