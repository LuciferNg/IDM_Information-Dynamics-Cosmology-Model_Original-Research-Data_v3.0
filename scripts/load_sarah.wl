(* Load SARAH with Wolfram Engine workaround *)
(* SARAH.m uses FindFile[$Input] which fails in Wolfram Engine CLI *)

(* Create a patched version of SARAH.m in temp *)
sarahOrig = ExpandFileName["~/.WolframEngine/Applications/SARAH/SARAH.m"];
sarahPatch = "/tmp/SARAH_patched.m";

(* Read original, fix the $Input line *)
orig = ReadList[sarahOrig, String];
patched = StringReplace[orig,
  "$sarahDir=SetDirectory[DirectoryName[System`Private`FindFile[$Input]]]" ->
    "$sarahDir=SetDirectory[ExpandFileName[\"~/.WolframEngine/Applications/SARAH\"]]"
];

Export[sarahPatch, patched, "Lines"];

(* Load the patched version *)
Get[sarahPatch];

(* Verify *)
Print["SARAH version: ", SA`Version];
$sarahModelDir = ToFileName[{$sarahDir, "Models"}];
Print["Available models: ", ShowModels[]];
Exit[];