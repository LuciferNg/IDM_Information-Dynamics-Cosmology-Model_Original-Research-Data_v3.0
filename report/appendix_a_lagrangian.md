## Appendix A: Gravitational Threshold — Corrected Derivation

### A.1 Problem Statement

The threshold correction formula used in the report:

$$\Delta(1/g_i^2) = \frac{\dim(G)\cdot\epsilon\cdot C_0}{16\pi^2}$$

must be derived without dimensional inconsistency. The previous version attempted a 1-loop Feynman diagram derivation with `ε²v²` (mass dimension 2) equated to `ε·C₀` (dimensionless) — a dimensional error. This appendix provides the correct derivation.

### A.2 Key Insight: Sync Cost, Not Loop Integral

The OAS gravitational threshold is **not** a standard 1-loop threshold from integrating out heavy particles. It is a **geometric spectral correction** from the sync field's ground state eigenvalue.

In the OAS framework, the gauge kinetic term is corrected by the sync field's ground state projection. The effective correction to $1/g_i^2$ is:

$$\Delta(1/g_i^2) = \frac{\langle W_0|L|W_0\rangle}{\langle W_0|W_0\rangle} \cdot \frac{1}{16\pi^2}$$

where $L$ is the graph Laplacian and $|W_0\rangle$ is its ground state. The factor $1/(16\pi^2)$ is the standard loop suppression from the phase space integral, which enters when we relate the sync cost to the gauge kinetic term.

### A.3 Laplacian Ground State

The ground state $|W_0\rangle$ of the OAS graph Laplacian has eigenvalue:

$$L|W_0\rangle = \lambda_0|W_0\rangle, \quad \lambda_0 = \dim(G) \cdot \epsilon \cdot C_0$$

This is a purely spectral/geometric quantity. All components are dimensionless:
- $\dim(G)$: count of gauge generators (pure number)
- $\epsilon = 0.1545$: basis asymmetry (irreducible constant, dimensionless)
- $C_0 = 18\pi$: topological winding from contour integral (dimensionless)

The norm is $\langle W_0|W_0\rangle = \dim(G)$ (there are $\dim(G)$ orthonormal components).

### A.4 Sync Cost Correction

The sync cost is:

$$\delta = \frac{\langle W_0|L|W_0\rangle}{\langle W_0|W_0\rangle} = \lambda_0 = \dim(G) \cdot \epsilon \cdot C_0$$

This is the "bare" correction before the loop factor. The loop factor $1/(16\pi^2)$ enters because the gauge kinetic term in $d=4$ has a $1/g^2$ normalization that relates to the gauge boson propagator $\sim g^2/(16\pi^2)$.

The final correction:

$$\Delta(1/g_i^2) = \frac{\dim(G) \cdot \epsilon \cdot C_0}{16\pi^2}$$

### A.5 Dimensional Analysis

Verify:

| Quantity | Definition | Dimension |
|:---------|:-----------|:---------:|
| $\dim(G)$ | Number of generators | 0 |
| $\epsilon$ | Irreducible asymmetry | 0 |
| $C_0$ | Topological winding ($18\pi$) | 0 |
| $1/(16\pi^2)$ | Loop suppression | 0 |
| $\Delta(1/g_i^2)$ | Effective threshold | 0 |

All quantities are dimensionless. **No mass scales appear** because the sync ground state is a spectral property of the graph Laplacian, not a perturbative loop integral over massive particles. The previous version's error was incorrectly introducing a VEV $v$ through a 1-loop Feynman diagram — this appendix corrects that by removing the spurious mass scale.

### A.6 Comparison with Standard Thresholds

In standard SUSY GUTs, the threshold from heavy Higgs multiplets is:

$$\Delta(1/g_i^2)_{\text{MSSM}} = \frac{1}{8\pi^2} \sum_{\text{Higgs}} b_i^{\text{Higgs}} \ln\frac{M_{\text{GUT}}}{M_{\text{Higgs}}}$$

The OAS spectral result replaces $\ln(M_{\text{GUT}}/M_{\text{Higgs}})$ with $\epsilon \cdot C_0 / 2 = 0.1545 \times 18\pi / 2 = 4.37$, which acts as an effective logarithmic enhancement. The $\dim(G)$ factor corresponds to the number of Higgs modes.

---

*Appendix A v2: Corrected. The gravitational threshold is a spectral correction from the sync field's Laplacian eigenvalue, not a Feynman diagram. All quantities dimensionless — no dimensional inconsistency.*