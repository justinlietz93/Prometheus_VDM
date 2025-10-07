# VDM Overview

> Author: Justin K. Lietz  
> Date: August 9, 2025  
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.<br>
> Commercial use requires written permission from Justin K. Lietz.  
> See LICENSE file for full terms.

Note on scope and merge resolution
- This file was reconciled to include a comprehensive macro banner and overview while enforcing the repository’s policy: RD is the canonical baseline; EFT/KG content is quarantined as future work and explicitly labeled.

## Macro Banner: Core Equations and Mappings

Two-layer model (separated clearly)

### 1. Canonical RD branch [PROVEN]

Discrete on-site (near homogeneous state):

$$
\frac{d W_i}{dt} = (\alpha - \beta)\, W_i - \alpha \, W_i^{2} + J \sum_{j\in \mathrm{nbr}(i)} (W_j - W_i)
$$

(RD-1)

Continuum PDE (1D notation; generalizes by components):

$$
\partial_t \phi = D\, \nabla^{2}\phi + r\, \phi - u\, \phi^{2} \quad \bigl[ -\lambda\, \phi^{3} \text{ (optional stabilization)} \bigr]
$$

(RD-2)

Discrete → continuum mapping:

$$
\begin{aligned}
D &= J a^{2} && \text{(site Laplacian)}\\
D &= \tfrac{J}{z} a^{2} && \text{(neighbor-average form)}\\
r &= \alpha - \beta,\quad u = \alpha
\end{aligned}
$$

(RD-3)

### 2. EFT/KG branch (quarantined; future work) [PLAUSIBLE]

Kinetic/action normalization from the discrete action:

$$
c^{2} = 2 J a^{2} \quad \text{(per-site)}, \qquad c^{2} = \kappa a^{2},\; \kappa = 2J \quad \text{(per-edge)}
$$

(EFT-1)

Second-order field equation:

$$
\square \phi + V'(\phi) = 0, \qquad \square = \partial_t^{2} - c^{2} \nabla^{2}
$$

(EFT-2)

Effective mass is parameter-dependent:

$$
m_{\mathrm{eff}}^{2} = V''(v)
$$

(EFT-3)

References:  
[kinetic_term_derivation.md](Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md:1), [effective_field_theory_approach.md](Prometheus_VDM/derivation/effective_field_theory/effective_field_theory_approach.md:1)

## VDM Dimensionless Constants (sanity set)

| Subsystem | Symbol | Definition | Meaning | Typical from runs |
| --- | --- | --- | --- | --- |
| LBM | $\nu$ | $\tfrac{1}{3}\bigl(\tau - \tfrac{1}{2}\bigr)$ | kinematic viscosity | 0.1333 ($\tau=0.9$) |
| LBM | $\mathrm{Re}$ | $\dfrac{U L}{\nu}$ | inertia vs. viscosity | 9.6 (64²), 19.2 (128²) |
| LBM | $\mathrm{Ma}$ | $\dfrac{U}{\sqrt{1/3}}$ | compressibility | 0.035-0.017 (low) |
| RD | $\Pi_{Dr}$ | $\dfrac{D}{r L^{2}}$ | diffusion at scale $L$ | choose $L$ → report |
| RD | $c^{\ast}$ | $\dfrac{c}{2\sqrt{D r}}$ | normalized KPP speed | ~0.95-1.0 |
| VDM | $\Theta$ | fit scale in $\Theta\,\Delta m$ or $\Theta\,\|\nabla m\|$ | junction gating strength | $k \approx 1$, $b \approx 0$ |
| VDM | $\Lambda$ | exploration/retention ratio | turnover vs. memory | as swept in heatmaps |
| VDM | $\Gamma$ | retention fraction | memory persistence | ~0.3-0.75 (representative) |
| VDM | $D_{a}$ | anisotropic diffusion index | transport anisotropy | {1, 3, 5, 7} |
| VDM | $\kappa L$ | curvature × scale | path bending | linear vs. $\Theta\,\|\nabla m\|$ |
| VDM | $g$ | void gain | stabilization strength | e.g., 0.5 |

## Core dimensionless groups (why they matter)

1. Void Debt Number 𝔇 — unresolved debt vs. resolved flux at walker level (stability vs. runaway)  
2. Emergent Coupling Ratio Ξ — void interaction gain vs. local relaxation; controls synchronization/stiffness  
3. Inverse-Scaling Exponent $\alpha$ — information density rises as system size shrinks: $\mathcal{I}(N) \propto N^{-\alpha}$  
4. Void Mach $M_v$ — void flux vs. signal speed; stability requires $M_v < 1$  
5. Topological Information Ratio $\Theta$ — information carried by topology vs. node states (void walkers effect)  
6. Symmetry Debt $\Sigma$ — broken symmetry flux vs. conserved symmetry flux (dimensionless energy-balance analog)  
7. Dispersion-to-Convergence $\Lambda$ — divergence vs. convergence rate under modulation (Lyapunov-like)

---

## What is Proven (numeric validation; RD branch)

Front-speed (Fisher-KPP pulled front) [PROVEN]

$$
c_{\text{front}} = 2\sqrt{D r}
$$

(RD-4)

Representative defaults: $c_{\mathrm{meas}} \approx 0.953$ vs $c_{\mathrm{th}} = 1.0$, $\mathrm{rel\_err} \approx 0.047$, $R^{2} \approx 0.999996$ (meets gates)  
Documentation: [rd_front_speed_validation.md](Prometheus_VDM/derivation/reaction_diffusion/rd_front_speed_validation.md:1)  
Script: [rd_front_speed_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:1)  
Sweep: [rd_front_speed_sweep.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_front_speed_sweep.py:1)

Linear dispersion about $\phi \approx 0$ (periodic, linearized RD) [PROVEN]

$$
\sigma_d(m) = r - \frac{4D}{\Delta x^{2}} \sin^{2}\!\left(\frac{\pi m}{N}\right)
$$

(RD-5)

$$
\sigma(k) = r - D k^{2}, \qquad k = \frac{2\pi m}{L}
$$

(RD-6)

Representative defaults: median rel. error $\approx 1.45\times 10^{-3}$, $R^{2}_{\text{array}} \approx 0.99995$ (meets gates)  
Documentation: [rd_dispersion_validation.md](Prometheus_VDM/derivation/reaction_diffusion/rd_dispersion_validation.md:1)  
Script: [rd_dispersion_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:1)

Consolidated plan and acceptance gates:  
[rd_validation_plan.md](Prometheus_VDM/derivation/reaction_diffusion/rd_validation_plan.md:1)

Status log and edits:  
[CORRECTIONS.md](Prometheus_VDM/derivation/CORRECTIONS.md:1)

## Stability and fixed points (RD)

For $r>0$, $\phi=0$ is dynamically unstable.

Homogeneous fixed point:

$$
\phi^{\star} = \frac{r}{u} = 1 - \frac{\beta}{\alpha} \qquad (r = \alpha - \beta,\; u = \alpha)
$$

(RD-7)

Optional cubic term $-\lambda\, \phi^{3}$ stabilizes large-amplitude regimes; off by default in canonical validations.

## Discrete → Continuum & Kinetics

Diffusion mapping (see also RD-3):

$$
D = J a^{2} \quad \text{or} \quad D = \tfrac{J}{z} a^{2}
$$

(RD-3′)

EFT kinetic normalization (quarantined branch; see also EFT-1):

$$
c^{2} = 2 J a^{2} \quad \text{or} \quad c^{2} = \kappa a^{2},\; \kappa = 2J
$$

(EFT-1′)

References:  
[discrete_to_continuum.md](Prometheus_VDM/derivation/foundations/discrete_to_continuum.md:1),  
[kinetic_term_derivation.md](Prometheus_VDM/derivation/effective_field_theory/kinetic_term_derivation.md:1)

## Scope boundaries and quarantine (policy)

- Canonical baseline is RD (first-order in time).  
- All EFT/KG (second-order in time) statements are quarantined to the EFT docs and labeled [PLAUSIBLE]/[FUTURE WORK].  
- Effective mass is parameter-dependent. Example only:

$$
(\alpha,\beta) = (0.25, 0.10): \quad m_{\mathrm{eff}} = \sqrt{\alpha - \beta} = \sqrt{0.15} \approx 0.387
$$

(EFT-EX)

EFT references:  
- [effective_field_theory_approach.md](Prometheus_VDM/derivation/effective_field_theory/effective_field_theory_approach.md:1)  
- [fum_voxtrium_mapping.md](Prometheus_VDM/derivation/effective_field_theory/fum_voxtrium_mapping.md:1)

## Reproducibility and outputs

- Figures → derivation/code/outputs/figures/  
- Logs → derivation/code/outputs/logs/  
- Filenames: <script>_<UTC timestamp>.png/json

fum_rt parity (independent runners; same metrics schema)  
- Front-speed mirror: [rd_front_speed_runner.py](Prometheus_VDM/fum_rt/physics/rd_front_speed_runner.py:1)  
- Dispersion mirror: [rd_dispersion_runner.py](Prometheus_VDM/fum_rt/physics/rd_dispersion_runner.py:1)

## Design principles (condensed)

- Single canonical model for baseline physics claims (RD)  
- Every nontrivial statement maps to a scriptable check with acceptance criteria (tolerance + $R^{2}$ gate)  
- Provenance and scope separation: EFT content retained for future work and explicitly labeled

## At-a-glance defaults (validated runs)

- Front-speed: N=1024, L=200, D=1.0, r=0.25, T=80, cfl=0.2, seed=42, x0=-60, level=0.1, fit 0.6-0.9  
- Dispersion: N=1024, L=200, D=1.0, r=0.25, T=10, cfl=0.2, seed=42, amp0=1e-6, record=80, m_max=64, fit 0.1-0.4

## Memory steering and system notes

- Memory-steering derivations and runtime integrations are tracked separately and must reference RD canonical terms when mapping to dynamics.  
  See: [memory_steering.md](Prometheus_VDM/derivation/memory_steering/memory_steering.md:1)  
- Runtime parity and plots reside under fum_rt/core/* and fum_rt/physics/* with explicit comments when driven by proven physics

## Finite-domain EFT modes (quarantined)

- Finite-tube mode problem and energy scans adapt the EFT branch with bounded potentials and mass-matrix positivity  
- Doc: [finite_tube_mode_analysis.md](Prometheus_VDM/derivation/tachyon_condensation/finite_tube_mode_analysis.md:1)

## Archive / informal content

- Non-normative transcripts or exploratory notes are labeled

## Licensing and citation

- The dual-license banner applies (see header).  
- Cite this overview and the specific validation documents when reusing claims or reproducing results.

## Appendix: Quick Links

- Front speed: [rd_front_speed_validation.md](Prometheus_VDM/derivation/reaction_diffusion/rd_front_speed_validation.md:1),  
  [rd_front_speed_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:1)  
- Dispersion: [rd_dispersion_validation.md](Prometheus_VDM/derivation/reaction_diffusion/rd_dispersion_validation.md:1),  
  [rd_dispersion_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:1)  
- Plan: [rd_validation_plan.md](Prometheus_VDM/derivation/reaction_diffusion/rd_validation_plan.md:1)  
- Status: [CORRECTIONS.md](Prometheus_VDM/derivation/CORRECTIONS.md:1)

