# P9 Migration Note — Moved to IDM3.0

**P9 (Early Universe W-Budget Concentration) has been moved from IDM2.0-Extensions to IDM3.0-Extensions/P9-migrated/.**

## Reason for Migration

P9 uses the **Domain Framework's W allocation mechanism** to explain JWST z>8 galaxy anomalies. This is IDM3.0's approach — applying the finite rendering budget axiom across scales.

## Status

All original files preserved:
- `TASK_SPEC_CONTRACT.md` — task specification (unchanged)
- `P9_REPORT.md` — full report (unchanged)
- `p9_derivation.py` — numerical derivation (unchanged)

## Next Steps for P9 in IDM3.0

1. Rewrite using CMR language: "W budget per coherent mode at cosmic scale"
2. Connect N_cosmic=44 to CMR's coherent mode framework
3. Use proper CAMB-based HMF for absolute normalization

See `IDM3.0-Extensions/01-coherent-mode-rendering/` for the core theory that P9 now builds upon.

---

*Migrated 2026-07-09.*