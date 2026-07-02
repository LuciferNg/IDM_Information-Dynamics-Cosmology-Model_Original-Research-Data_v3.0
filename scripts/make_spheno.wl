(* Load SARAH with patched path *)
Get["/tmp/SARAH_patched.m"];

(* Load the IDM_GUT model *)
Start["IDM_GUT"];

(* Options: skip decays (not needed for y_u calculation), keep RGEs + masses *)
SA`NoDecays = True;

(* Generate SPheno Fortran code *)
Print["Generating SPheno code (NoDecays)..."];
MakeSPheno[];

(* List generated files *)
sphenoDir = ToFileName[{$sarahOutputDir, "EWSB", "SPheno"}];
If[FileType[sphenoDir] === Directory,
  Print["Generated files:"];
  files = FileNames["*.f90", sphenoDir];
  Print["  Count: ", Length[files]];
  Print["  Total size: ", Total[FileSize /@ files], " bytes"];
  Scan[Print["  ", FilenameSplit[#][[-1]], " (", FileSize[#], " B)"]&, files],
  Print["ERROR: SPheno output not found"]
];

Print["=== SPHENO CODE GENERATION COMPLETE ==="];
Exit[];