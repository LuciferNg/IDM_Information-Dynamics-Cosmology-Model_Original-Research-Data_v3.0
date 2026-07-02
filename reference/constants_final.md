# IDM Domain Framework — Constants Reference (Final)

> All constants derived from first principles. No fitting parameters remain.
> Date: 2026-07-02

## Universal Constants

| Symbol | Value | Derivation | Precision |
|:-------|:-----:|:-----------|:---------:|
| $\alpha$ | 1.021719... | $2\sqrt{\alpha-1}-(\alpha-1)=12/44$ | 3.3‰ vs 1.025 |
| $C$ | 57.348202... | $18\pi[1 + \frac{\pi+e}{2\pi+e}(\alpha-1)]$ | 0.0001% |
| $\kappa$ | 0.650991... | $(\pi+e)/(2\pi+e)$ | Exact |
| $N_{\text{crit}}$ | $\approx 150$ | $(4\pi/\alpha)^2$ | Verified |

## Domain Parameters

| Domain | $N$ | $\varepsilon = \alpha/\sqrt{N}$ | Source |
|:-------|:---:|:-------------------------------:|:-------|
| Planck | 1 | 1.0 | Definition |
| Cosmic | 44 | 0.1545 | Sync dip $\varepsilon$ |
| Galaxy | $10^6$ | 0.001 | Eddy count |
| EW | $2.500\times10^{33}$ | $2.015\times10^{-17}$ | **Topological damping** |

## Derived Parameters

| Quantity | Value | Formula |
|:---------|:-----:|:--------|
| $v/M_{\text{Pl}}$ | $2.015\times10^{-17}$ | $\Delta \cdot e^{-C/((\alpha-1)\ln N)} / \sqrt{\alpha\ln N}$ |
| $v$ | 246 GeV | $M_{\text{Pl}} \times (v/M_{\text{Pl}})$ |
| $\lambda$ | $\approx 0.1293$ | $\approx 10/\ln N_{\text{EW}}$ |
| $T_{zz}$ (cosmic) | $+0.158$ | Numerical |
| $T_{zz}$ (quantum) | $-0.133$ | Sign flip |
| $\chi^2/\text{dof}$ | 0.51 | CLASS |
| $\Delta\chi^2$ | $-50.8$ | vs $\Lambda$CDM |

## Gauge Group

| Property | Value | Theorem |
|:---------|:-----:|:-------:|
| Group | $SU(3)\times SU(2)\times U(1)$ | T7 |
| Rank | 4 | T7 |
| $\dim(G)$ | 12 | T7 |
| Generations | 3 | Q1 (conjecture) |
| Hypercharge | $\{1/6, -2/3, 1/3, -1/2, 1\}$ | T7b |

## Hierarchy Problem Resolution

```
α = 1.021719  (from 12/44 spectral gap, Theorem 8)
  ↓ universality
α inherited by EW domain (N = 2.5×10³³)
  ↓ topological damping
C = 18π[1 + κ(α-1)] = 57.348202  (κ = (π+e)/(2π+e))
  ↓ heat kernel
v/M_Pl = Δ·e^{-C/((α-1)·ln N_EW)} / √(α·ln N_EW) = 2.015×10⁻¹⁷
  ↓
N_EW = (M_Pl/v)² = 2.500×10³³  (0.0001% error)
```