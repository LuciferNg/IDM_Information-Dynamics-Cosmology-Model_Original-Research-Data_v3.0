# TASK SPECIFICATION CONTRACT — P9: 早期宇宙 W-Budget 集中效應
# Early Universe W-Budget Concentration Effect

**Project ID:** IDM-EXT-P9  
**Status:** ⏳ 新建 — 理論推導中  
**Date:** 2026-07-09  
**Core Claim:** JWST 觀測到嘅 z>8 成熟星系（too massive, too early）可以由 IDM 框架嘅 W allocation 機制解釋：早期宇宙結構數目少 → 每個 structure 分配到更多 rendering budget（W）→ accelerated assembly。隨 redshift 下降，更多結構競爭 W → growth rate converge 到 ΛCDM。

---

## 1. INPUT ASSUMPTIONS（已鎖定基礎）

| # | Assumption | Source | Status |
|:-:|:-----------|:-------|:------:|
| A1 | IDM core: ε=0.1545, z_c=0.60, f_ID(z), α_B, Horndeski action | IDM v4.0 + Lagr. Rev. Eng. | ✅ Locked |
| A2 | W-field 係 finite rendering budget：W ∈ [0,1]，total available W(t) 隨宇宙膨脹改變 | IDM OAS framework | ✅ Locked |
| A3 | 每個 structure（galaxy / halo）consume 一定量 W 去維持 coherence。Structure 越多，每個 structure 分到嘅 W 越少 | W allocation theorem | ✅ Locked |
| A4 | JWST CEERS/JADES/RXJ2129 觀測：z~9-11 存在質量 ~10⁹-10¹⁰ M☉ 嘅星系，比 ΛCDM halo mass function 預測多 10-100× | Observational literature (Labbe 2023, Boyett 2024) | ✅ Known |
| A5 | High-z 時 horizon 細 → N_horizon 細 → ε = α/√N_horizon 大 → IDM effects stronger | IDM CLT scaling | ✅ Locked |
| A6 | ΛCDM halo mass function 喺 high-z 嘅 suppression 來自 structure formation timescale — IDM 嘅 modified growth 可以 relax 呢個 constraint | Growth index shift | ✅ Locked |

---

## 2. DERIVATION TARGETS

| # | Target | Method | Success Criteria |
|:-:|:-------|:-------|:----------------|
| **Phase 0 — W Budget at High z** | | | |
| T0 | 推導 high-z W_available(z)：早期宇宙嘅 total rendering budget | IDM cosmology + N_horizon(z) scaling | Monotonic decrease with z (fewer structures → more W per structure) |
| T1 | 推導 structure count N_struct(z)：喺 redshift z 存在嘅 coherence structures 數量 | Halo mass function + merger tree | Increases with cosmic time (decreases with z) |
| **Phase 1 — Accelerated Assembly** | | | |
| T2 | 推導 W_per_structure(z) = W_available(z) / N_struct(z) | Combine T0 + T1 | W_per_structure ∝ 1/N_struct(z) at fixed z |
| T3 | 推導 accelerated assembly factor A(z) = dM/dt_IDM / dM/dt_ΛCDM | Modified growth + W budget | A(z) > 1 at high z, A(z) → 1 at low z |
| **Phase 2 — Observable Predictions** | | | |
| T4 | 推導 IDM-modified halo mass function HMF_IDM(M, z) | Sheth-Tormen + W correction | Enhanced high-mass tail at z>8 |
| T5 | 推導 predicted galaxy stellar mass function GSMF_IDM(M*, z) at z>8 | HMF × baryon conversion + W efficiency | 10-100× enhancement over ΛCDM at M* ~ 10⁹-10¹⁰ M☉ |
| T6 | 推導 z-dependent transition：assembly acceleration fading redshift | Analytic | Smooth transition from accelerated (z>8) → standard (z<4) |
| **Phase 3 — Distinguishing Predictions** | | | |
| T7 | IDM vs ΛCDM distinguishing signature：mass function slope difference | Numerical | IDM predicts shallower high-mass slope at z>8 |
| T8 | Feature at sync dip：z~0.6 W reallocation → late-time structure suppression? | Cross-check P3 | Consistent with sync dip as local W reallocation |

---

## 3. CORE MECHANISM

### W Budget Concentration

喺 standard ΛCDM，early universe 嘅 galaxy assembly 受 Hubble time + cooling timescale 限制。IDM 加多一層：**finite rendering budget**。

```
W_total(t) = finite, set by rendering engine capacity
N_struct(z) = number of coherent structures at redshift z
W_per_structure(z) = W_total(z) / N_struct(z)

At high z (z>8):
  N_struct is SMALL → W_per_structure is LARGE → assembly is fast

At low z (z<1):
  N_struct is LARGE → W_per_structure is SMALL → assembly converges to ΛCDM

At sync dip (z~0.6):
  Local W reallocation event → subtle suppression → P3 cross-check
```

### Why This Is Not Ad-Hoc

呢個 mechanism 唔係為咗 fit JWST data 而發明嘅。佢直接由 IDM 嘅 core axioms 推出：

1. W-field 係 finite rendering budget（core axiom）
2. 每個 structure 需要 W 去 maintain coherence（W allocation theorem）
3. Structure count N 隨宇宙膨脹增加
4. W 係 finite → N 增加 → per-structure W 減少

呢個 logic chain 完全由 framework 內部推出，唔需要 ad-hoc parameters。

---

## 4. VERIFICATION MATRIX

| Verification | Type | Tool | Expected |
|:-------------|:----:|:----:|:--------|
| [ ] T0: W_available(z) derived | Analytic | Python/numpy | Monotonic with z |
| [ ] T1: N_struct(z) from HMF | Numeric | HMF calculator + IDM correction | Smooth function |
| [ ] T2: W_per_structure(z) computed | Numeric | Combine T0+T1 | ∝ 1/N at high z |
| [ ] T3: A(z) > 1 at high z, →1 at low z | Numeric | Growth model | Smooth convergence |
| [ ] T4: HMF_IDM enhanced at high-mass tail | Numeric | Sheth-Tormen + W corr | 10-100× at M>10⁹ at z>8 |
| [ ] T5: GSMF_IDM matches JWST abundance | Statistical | Compare to Labbe+23, Boyett+24 | Within JWST error bars |
| [ ] T6: z-dependent transition smooth | Numeric | Check continuity | No discontinuities |
| [ ] T7: Distinguishing signature identified | Analytic | HMF slope difference | >2σ distinguishable |
| [ ] T8: Sync dip cross-check consistent | Cross-check | Compare P3 prediction | No contradiction |

| **Risk** | Worst case: if W_per_structure(z) scales as 1/N_struct(z), and N_struct(z) at z>8 is >0, then W_per_structure might not be large enough to explain 10-100× enhancement. Need explicit numerical calculation. |

---

## 5. BOUNDARIES（唔會做嘅嘢）

- ❌ 唔會做 full hydrodynamical simulation（budget/code constraint）
- ❌ 唔會修改 IDM core parameters（ε, z_c, α_B already locked）
- ❌ 唔會 claim「IDM fits all JWST data」— 只做 specific enhancement prediction
- ❌ 唔會引入 ad-hoc early universe model（用 IDM 嘅 W allocation 就夠）
- ❌ 唔會同 standard ΛCDM galaxy formation compete on precision（目標係 alternative explanation + testable distinguishing prediction）

---

## 6. KEY BOTTLENECK

**HMF at extreme z:** Standard halo mass function calculators (e.g., HMFcalc, Colossus) have uncertain extrapolation at z>8. The IDM correction is model-dependent until we have a calibrated IDM HMF. 

**Suggested response:** Use analytic Sheth-Tormen form with IDM-modified growth factor D(z) and critical density δ_c. This is first-principles enough for a distinguishing prediction without full simulation.

---

## 7. WAVE PLACEMENT PROPOSAL

| Dimension | Assessment |
|:----------|:-----------|
| **Wave** | **2.8**（follows P7 + P8） |
| **Feasibility** | 🟡 Medium（depends on HMF extrapolation reliability） |
| **Dependency** | Needs IDM core parameters (ε, z_c, α_B) — all locked |
| **Risk** | W_per_structure enhancement may be insufficient to explain 10-100× factor |

---

*Generated 2026-07-09. Initial contract — awaiting derivation.*
