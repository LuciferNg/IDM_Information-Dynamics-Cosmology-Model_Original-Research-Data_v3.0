(* Load SARAH with patched path *)
Get["/tmp/SARAH_patched.m"];

(* Try to load the IDM_GUT model *)
Print["Loading IDM_GUT model..."];
Start["IDM_GUT"];
Print["=== MODEL LOADED SUCCESSFULLY ==="];
Print["Particle content: ", ParticleTable];
Exit[];