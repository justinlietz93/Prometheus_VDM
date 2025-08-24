# FUVDM Overview (Public Render-Friendly)

This document is a GitHub-friendly overview of the derivation papers. It avoids LaTeX and uses plain text/code blocks so equations render reliably on GitHub. For the full math-formatted version, see [FUVDM_Overview.md](./FUVDM_Overview.md).

## What this is
- A plain-text banner of the core equations and mappings.
- A separation of the two layers: RD (proven) vs EFT (future work, quarantined).
- Pointers to the derivation papers you can read on GitHub without special rendering.

## Two-layer model (separated)
1) Canonical RD branch [PROVEN] (first-order in time).
2) EFT/KG branch [PLAUSIBLE] (second-order in time), quarantined until full discrete-action derivation and stability scans.

## Equations banner (ASCII, render-safe)

Discrete on-site law (near homogeneous state):

```
dW_i/dt = (alpha - beta) * W_i
           - alpha * W_i^2
           + J * sum_{j in nbr(i)} (W_j - W_i)
```

Continuum RD PDE (1D notation; extends by components):

```
dphi/dt = D * Laplacian(phi) + r * phi - u * phi^2
# optional stabilization (off by default in baseline): - lambda * phi^3
```

Discrete -> continuum mapping:

```
D = J * a^2                 # site Laplacian
D = (J / z) * a^2           # neighbor-average form
r = alpha - beta
u = alpha
```

EFT branch (kept separate):

```
d^2 phi/dt^2 - c^2 * Laplacian(phi) + dV/dphi = 0
c^2 = 2 * J * a^2          # per-site kinetic normalization
# or equivalently: c^2 = kappa * a^2 with kappa = 2J (per-edge form)
m_eff^2 = d2V/dphi2 evaluated at phi = v
```

## What is proven (numeric checks; RD branch)

Front-speed (Fisher-KPP pulled front):

```
c_front = 2 * sqrt(D * r)
```

Linear dispersion about phi ~ 0 (periodic, linearized RD):

```
sigma_d(m) = r - (4D/dx^2) * sin^2(pi * m / N)
sigma(k)   = r - D * k^2,  where k = 2 * pi * m / L
```

Representative defaults and acceptance gates are documented in the validation papers below.

## Stability and fixed points (RD)

- For r > 0, phi = 0 is dynamically unstable.
- Homogeneous fixed point:

```
phi_star = r / u = 1 - beta/alpha    # using r = alpha - beta, u = alpha
```

## Links (papers readable on GitHub)

- Overview (math-formatted): [FUVDM_Overview.md](./FUVDM_Overview.md)
- Foundations:
  - [discrete_to_continuum.md](./foundations/discrete_to_continuum.md)
  - [continuum_stack.md](./foundations/continuum_stack.md)
- Reaction-Diffusion (canonical baseline):
  - [rd_front_speed_validation.md](./reaction_diffusion/rd_front_speed_validation.md)
  - [rd_dispersion_validation.md](./reaction_diffusion/rd_dispersion_validation.md)
  - [rd_validation_plan.md](./reaction_diffusion/rd_validation_plan.md)
- Memory Steering (separate layer):
  - [memory_steering.md](./memory_steering/memory_steering.md)
- Finite-domain EFT modes (future work, quarantined):
  - [finite_tube_mode_analysis.md](./tachyon_condensation/finite_tube_mode_analysis.md)
- Scope log and edits:
  - [CORRECTIONS.md](./CORRECTIONS.md)

## Safety and scope

- Baseline claims use the RD branch with documented acceptance criteria.
- EFT claims are kept in separate documents and labeled [PLAUSIBLE]/[FUTURE WORK].
- The derivations remain within theoretical physics and simulation; no ML training or proprietary AI algorithms are disclosed.

## How this relates to AI (brief)

- Local, event-driven rules that scale sub-quadratically inspire AI systems that avoid heavy global passes.
- Memory steering frames slow, structured guidance over faster dynamics, an architectural idea for routing compute without black-box shortcuts.
- Acceptance tests (e.g., dispersion, front speed) mirror transparent evaluation practices.

## Citation note

- When referencing results, cite this overview and the specific validation paper you use.
- Example: "Reaction-Diffusion: Front-Speed Validation" and "Reaction-Diffusion: Dispersion Validation".

## Licensing

- Shared for academic review and discussion. Commercial use requires prior written permission.

## Contact

- Questions about scope or acceptance criteria: see file headers in the linked papers or the distribution cover note.