# IDM/OAS vs Parallel Researchers — Direct Comparison

## Overview

This project compares **IDM1.0/OAS/CIP/CIW** (LuciferNg) against **6 parallel alternative cosmological frameworks** found on GitHub. The comparison is at the **ontological, mathematical, and empirical** levels.

| Your Framework | Parallel Researchers |
|:--------------|:--------------------|
| IDM (Interacting Dark Matter) | SRC (Scalar Relaxation Cosmology) — warpXspeed |
| OAS (Observer-Aware System) | VSR (Viscoelastic Strain Reservoir) — warpXspeed |
| W-field (precision budget) | φ-field (scalar relaxation) — warpXspeed |
| — | ITSM (Integrated Toroidal-Syntropic Model) — brendohxd |
| — | TEP (Temporal Topology) — matthewsmawfield |
| — | ACM (Anchor Collapse Model) — lesleyliuhaitao-ctrl |

---

## 1. warpXspeed — Scalar Relaxation Cosmology (SRC)

### README
**File:** `scalar-relaxation-cosmology/README.md`

### Core Claims
SRC proposes that the observable universe emerges from **relaxation processes in a single, eternal scalar field** φ. There is no Big Bang, no dark energy, no inflation — just one slow wave on an eternal lake.

### Key Concepts
| Concept | SRC (warpXspeed) | IDM (LuciferNg) | Overlap |
|---------|:----------------:|:----------------:|:-------:|
| Substrate | φ (scalar field) | W (precision field) | **High** — both pre-spacetime |
| Mechanism | Viscoelastic relaxation | CLT fluctuation (ε=α/√N) | **Medium** — different math |
| Origin | Eternal (no Big Bang) | Finite domain decomposition | **Medium** |
| Dark Energy | Replaced by relaxation | Replaced by W allocation | **High** |
| Galaxy formation | Eddy dynamics (SREC) | W reallocation at z≈0.6 | **Medium** |
| Testability | MCMC + SPARC + DESI | 12 tests A–L | IDM more tested |

### Empirical Status
- SRC: **Qualitative framework**, limited quantitative tests
- IDM: **12 quantitative tests**, all completed, most passing

### Key Differences
| Aspect | SRC | IDM |
|--------|-----|-----|
| Mathematical foundation | Viscoelastic wave equation | ε = α/√N (CLT) |
| Domain decomposition | None — single φ field | N_i = 44, 4, 10⁶, 3 |
| Number predictions | None explicit | **ε_cosmic=0.1545, ε_EW=0.0161, ε_gal=0.001, Σm_ν=0.031 eV** |
| Observer role | Not addressed | **Active observer (Lemma 4)** |
| Sync dip | Not predicted | **ε=0.1545, zc=0.6 — verified** |

### Conclusion: SRC shares the same pre-spacetime ontological direction but lacks IDM's mathematical precision and empirical validation.

---

## 2. warpXspeed — Viscoelastic Strain Reservoir (VSR)

### Core Claims
VSR is a **viscoelastic scalar field** φ that stores latent strain energy. Like a fluid for slow changes, like a crystal for fast ones. All reality emerges from its relaxation patterns.

### Key Concepts
| Concept | VSR | IDM W-field |
|---------|:---:|:-----------:|
| Nature | Viscoelastic φ | Precision budget W |
| Dynamics | Damped wave relaxation | ε fluctuation from CLT |
| Eternality | Yes — cyclic | Yes — finite domains |
| Particles | Emerge from φ patterns | Emerge from address allocation |
| Gravity | Emergent from φ strain | T_μν = δ²S/δW_μδW_ν |

### Technical Documents
- `Technical-Foundations.md` — formal mathematical basis
- `Fits-and-Replacements.md` — how VSR replaces standard physics
- `Glossary.md` — terminology

### Key Difference: **VSR uses a continuous field (φ) while IDM uses a discrete precision field (W).** VSR's viscoelastic damping is deterministic; IDM's ε fluctuation is statistical (CLT-derived).

---

## 3. warpXspeed — SREC Cosmology

### Core Claims
Scalar Relaxation Eddy Cosmology: a unified model for **solar system formation and cosmic resets**. Eddy dynamics in the scalar field create structures at all scales.

### Overlap with IDM
- SREC's "eddies" ≈ IDM's "domain fluctuations"
- Both predict structure formation from substrate dynamics
- SREC is more focused on local (solar system) scales; IDM on cosmic scales

---

## 4. brendohxd — Integrated Toroidal-Syntropic Model (ITSM)

### README
**File:** `ITSM-Integrated-Toroidal-Syntropic-Model/`

### Core Claims
ITSM proposes **toroidal topology** as the fundamental geometry of spacetime. Relativistic field equations with topology-induced superfluid dynamics. 274 commits — most active repo.

### Technical Capabilities
| Feature | ITSM | IDM |
|---------|:----:|:---:|
| CAMB solver | ✅ Custom patch | ✅ CLASS patch |
| MCMC | ✅ For SPARC | ✅ For cosmological data |
| SPARC fitting | ✅ | — |
| NANOGrav | ✅ | — |
| DESI data | ✅ | ✅ |
| CMB | ✅ | ✅ |
| Number of tests | ~5 | **12** |

### Key Difference
ITSM uses **toroidal topology** as the fundamental geometric framework. IDM uses **domain decomposition (N_i)** as the fundamental counting framework. Both are pre-geometric but in different ways.

### Active Status
- Latest commit: **5 hours ago**
- 274 commits total
- Manuscript + code + data + analysis pipeline
- Actively responding to reviewer comments on S8 and Bullet Cluster

---

## 5. matthewsmawfield — Temporal Topology (TEP)

### Repos
- `TEP-RBH`: RBH-1 runaway black hole as Temporal Topology soliton
- `TEP-UCD`: Universal critical density ρ_T ≈ 20 g/cm³

### Core Claims
Temporal Topology proposes that **temporal structure itself** carries topological defects. These appear as:
- Runaway black holes (TEP-RBH)
- Universal critical density ρ_T ≈ 20 g/cm³ (TEP-UCD)

### Calibration
TEP is **calibrated using GNSS data**: R_T ≈ 7.8×10⁷ km, L_c ≈ 4200 km.

### Comparison with IDM
| Aspect | TEP | IDM |
|--------|:---:|:---:|
| Foundation | Temporal topology | Domain decomposition |
| Calibration | GNSS atomic clocks | Planck + fσ₈ + eBOSS |
| Predictions | ρ_T ≈ 20 g/cm³ | ε = α/√N across domains |
| Tests | 2 (RBH, UCD) | **12** |
| Observer role | Not addressed | **Active observer** |

### Interesting Connection
TEP's GNSS calibration suggests they found something in **GPS satellite clock data** — which could be a W-field signature at Earth-scale. Worth investigating.

---

## 6. lesleyliuhaitao-ctrl — Anchor Collapse Model (ACM)

### README
**File:** `anchor-collapse-model/README.md`

### Core Claims
ACM is a **rigid holographic framework for galactic dynamics**. Predicts galaxy rotation from baryonic distributions via linear holographic screening. "No galaxy-by-galaxy fits. No hidden knobs. Just the physics of the background floor."

### Comparison with IDM
| Aspect | ACM | IDM |
|--------|:---:|:---:|
| Galaxy rotation | ✅ Predicts from baryons | — (not tested) |
| Holographic principle | ✅ — rigid holographic screen | — (different approach) |
| Dark matter | Replaced by screening | Replaced by W allocation |
| Test data | SPARC | fσ₈, CMB, eBOSS, DESI |
| Precision | Continuous screening | ε = α/√N |

### Key Overlap
ACM's "background floor" is conceptually similar to IDM's "finite W budget". Both propose that galaxy dynamics emerge from a **fundamental ontological floor**, not from dark matter particles.

---

## Consolidated Comparison

| Dimension | IDM/OAS | SRC/VSR | ITSM | TEP | ACM |
|:----------|:-------:|:-------:|:----:|:---:|:---:|
| **Pre-spacetime** | ✅ W-field | ✅ φ-field | ✅ Toroidal | ✅ Temporal | ✅ Holographic |
| **Mathematical precision** | ✅✅ ε=α/√N | ⚠️ Qualitative | ✅ Field eqns | ⚠️ Calibration | ✅ Screening |
| **Number predictions** | ✅✅ 4 domains | ❌ None | ❌ None | ✅ ρ_T | ❌ None |
| **Empirical tests** | ✅✅ 12 tests | ⚠️ 1-2 | ✅ ~5 | ✅ 2 | ✅ SPARC |
| **Observer role** | ✅✅ Lemma 4 | ❌ Not addressed | ❌ Not addressed | ❌ Not addressed | ❌ Not addressed |
| **Code quality** | ✅ Python/CLASS | ⚠️ Python scripts | ✅✅ Full pipeline | ⚠️ Manuscripts | ✅ Python |
| **Active development** | ⚠️ Paused | ⚠️ (2 weeks ago) | ✅✅ (5 hours ago) | ⚠️ (1 month ago) | ⚠️ (4 months ago) |
| **Public papers** | ✅ docs/ | ✅ Manuscripts | ✅ Manuscripts | ✅ Manuscripts | ✅ Manuscript + LaTeX |

## Key Findings

1. **SRC/VSR (warpXspeed)** — Closest ontological match to IDM. Same pre-spacetime direction, but less mathematical. IDM has **ε = α/√N**; SRC has qualitative wave relaxation.

2. **ITSM (brendohxd)** — Most technically capable rival. 274 commits, CAMB patch, MCMC pipeline, actve manuscript. Different topology (toroidal vs domain), but equally serious.

3. **TEP (matthewsmawfield)** — Interesting calibration method (GNSS). Temporal topology is a different angle on the same pre-spacetime concept.

4. **ACM (lesleyliuhaitao-ctrl)** — Clean galaxy rotation test without dark matter. "Background floor" concept matches IDM's "finite W budget."

## Recommendation

1. **Contact warpXspeed** — most aligned directionally. Merge SRC + IDM = stronger framework.
2. **Study ITSM code** — borrow their MCMC pipeline for IDM's parameter fitting.
3. **Check TEP's GNSS data** — potential W-field signature at Earth scale.
4. **Collaborate with ACM** — apply IDM's ε predictions to their SPARC pipeline.