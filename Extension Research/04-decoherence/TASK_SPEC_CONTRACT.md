# TASK SPECIFICATION CONTRACT — Q4: Decoherence from CMR

**Project ID:** IDM3.0-Q4  
**Status:** ⏳ Theory derivation  
**Date:** 2026-07-09  
**Core Claim:** Decoherence rate = |del W| = gradient of W allocation across coherent modes.

---

## 1. INPUT AXIOMS (from Q1 CMR)

| # | Axiom | Source |
|:-:|:------|:-------|
| A1 | W ∈ [0,1] finite, allocated per coherent mode | Q1 |
| A2 | epsilon = ALPHA/sqrt(N_c) sets uncertainty | Q1 |
| A3 | Coupled systems share W budget via gradient | Q1, Q2 |
| A4 | dW/dN_c = -(ALPHA/2) * N_c^(-3/2) | Q1 derived |
| A5 | Environment = many coherent modes (N_env >> N_sys) | This work |

## 2. DERIVATION TARGETS

| # | Target | Criteria |
|:-:|:-------|:--------|
| T0 | Gamma_dec = |del W| = |dW/dN_c| * |dN_c/dt| | Formal decoherence rate |
| T1 | Gamma_dec = (ALPHA/2) * N_c^(-3/2) * (dN_c/dt) | Empirical form |
| T2 | Power law: P_IDM(t) = P_QM(t) * (1 + t/tau)^(-epsilon) | Matches P5 prediction |
| T3 | N_c(t) evolution for open systems | dN_c/dt = coupling rate to environment |
| T4 | Connection to standard decoherence theory | Reproduce known results |

## 3. FALSIFIABLE PREDICTIONS

| # | Prediction | Test |
|:-:|:-----------|:-----|
| F1 | Gamma_dec ∝ N_c^(-3/2) — power law decoherence | Cold atom experiments with controlled N_c |
| F2 | Fast decoherence near measurement apparatus (steep W gradient) | Proximity-dependent decoherence |
| F3 | IDM power law tail: (1+t/tau)^(-epsilon) beyond standard exponential | Fault-tolerant QC (30yr) |

---

*Generated 2026-07-09.*