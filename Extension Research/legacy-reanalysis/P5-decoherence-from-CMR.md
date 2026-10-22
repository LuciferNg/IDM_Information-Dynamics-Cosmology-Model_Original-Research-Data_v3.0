# Legacy Reanalysis: P5 — Decoherence from CMR

**Original (IDM2.0):** IBM Quantum Decoherence — IDM predicts extra decoherence power law.  
**IDM3.0 Reanalysis:** Decoherence rate = |del W| — W gradient drives budget flow.

---

## Original P5 Formula

P_IDM(t) = P_QM(t) * (1 + t/tau_0)^(-epsilon)

## CMR Reinterpretation

Decoherence is NOT an extra term — it's the NATURAL consequence of W allocation:

Gamma_dec ∝ |del W| = |dW/dN_c| * |dN_c/dt|

where:
- dW/dN_c = -(ALPHA/2) * N_c^(-3/2) (from epsilon = ALPHA/sqrt(N_c))
- dN_c/dt = coupling rate to environment (how fast new coherent modes are activated)

## Testable Prediction

Gamma_dec = Gamma_0 * N_c^(-3/2) * (dN_c/dt)

This connects decoherence rate to mode count — falsifiable with controlled cold atom experiments:

| System | N_c | Predicted Gamma_dec | Observable |
|:-------|:---:|:-------------------:|:-----------|
| Trapped ion (single) | 1 | Baseline | Standard QM |
| BEC (near T_c) | 1-10⁶ | 10⁴× increase across threshold | Quantum Zeno transition |
| Cold atom lattice (2 atoms) | 2 | ~35% of single | Controlled coupling |

## Key Change from P5

- P5 (IDM2.0): "IDM adds extra decoherence on top of QM"
- CMR (IDM3.0): "Decoherence = natural result of W allocation gradient. No extra term needed."

## Verdict

**The power-law prediction from P5 is preserved but reinterpreted: (1 + t/tau)^(-epsilon) emerges naturally from N_c(t) evolution in CMR, not as an ad-hoc addition.**

For full decoherence analysis, see `IDM3.0-Extensions/04-decoherence/` after Q1 completion.