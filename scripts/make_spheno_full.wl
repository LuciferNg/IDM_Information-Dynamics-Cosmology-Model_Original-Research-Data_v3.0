(* Load SARAH and regenerate SPheno code — complete run *)
Get["/tmp/SARAH_patched.m"];

(* Clean previous output *)
If[DirectoryQ[ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"]],
  DeleteDirectory[ExpandFileName["~/.WolframEngine/Applications/SARAH/Output/IDM_GUT"],
    DeleteContents -> True];
  Print["Previous output cleaned"]
];

(* Load the IDM_GUT model *)
Start["IDM_GUT"];
Print["Model loaded: IDM_GUT"];

(* Generate SPheno Fortran code - NO skips, complete generation *)
Print["Starting MakeSPheno[] — complete generation..."];
MakeSPheno[];

(* Verify output *)
sphenoDir = ToFileName[{$sarahOutputDir, "EWSB", "SPheno"}];
If[FileType[sphenoDir] === Directory,
  files = FileNames["*.f90", sphenoDir];
  Print["=== GENERATION COMPLETE ==="];
  Print["Files: ", Length[files]];
  Print["Total size: ", Total[FileSize /@ files], " bytes"];
  Scan[Print[FilenameSplit[#][[-1]], " (", FileSize[#], " B)"]&, files],
  Print["ERROR: SPheno output not found"]
];

Exit[];