# Proposal: Wave Poynting-Meter Instrument v1 (Thermodynamic Routing — Photonic Track)

Author: Justin K. Lietz  
Proposed Tag: thermo-routing-v2-wave-meter

Last updated: 2025-10-13  
Commit: 9c27e65

## Abstract

We propose a J-only scalar-wave instrument that measures field energy flow using a Poynting-analog flux meter over a frozen channel map $V(x,y)$. This instrument is a prerequisite for any photonic-style routing claims. We will certify it in three phases (A→C): energy/flux consistency in a closed box, open-port power accounting, then routing tests with a frozen channel map. No routing claims are made until A and B gates pass.

## Background and Equations

We evolve a scalar field $(\phi,\pi)$ on a 2D grid with a frozen potential $V(x,y)$:

- Dynamics (J-only; symplectic leapfrog):
  
  $$\partial_t \phi = \pi,\quad \partial_t \pi = c^2 \nabla^2 \phi - V\,\phi.$$

- Energy density and Poynting-analog flux:
  
  $$e = \tfrac12\left(\pi^2 + c^2\,|\nabla\phi|^2 + V\,\phi^2\right),\quad \mathbf{s} = -\,\pi\,c^2\,\nabla\phi.$$

- Outlet powers (for open-port phases):
  
  $$F_A(t) = \int_{\Gamma_A} \mathbf{s}\cdot\mathbf{n}\,\mathrm{d}\ell,\quad F_B(t) = \int_{\Gamma_B} \mathbf{s}\cdot\mathbf{n}\,\mathrm{d}\ell.$$

Discretization uses centered differences and a staggered (leapfrog) time step to preserve energy to $\mathcal{O}(\Delta t^2)$, as previously certified in our KG J-only tests.

## Compliance and Provenance (pre-registered)

- Frozen map: $V(x,y)$ immutable at runtime (hash receipts at start/end).
- Probe-limit: instrument is read-only w.r.t. $V$; no actuators present.
- Determinism: seeded, single-thread receipts (BLAS/FFT thread counts).
- Artifacts minimum: each run emits ≥1 PNG + 1 CSV + 1 JSON via common IO.
- Approvals: default-deny; tag must be explicitly approved before any scientific runs.

## Phased Gates (A → C)

### Phase A — Meter Bring-up (closed box; no outlets)

1. Energy conservation (J-only, $V=\mathrm{const}$; periodic or reflecting walls):  
Gate: $$\max_t \frac{|E(t)-E(0)|}{E(0)} \le 10^{-6}$$ over ≥100 periods; time-reversal error ≤ $10^{-12}$.

2. Local balance check (frozen $V$ ⇒ RHS = 0):  
Balance law: $$\partial_t e + \nabla\cdot\mathbf{s} = -\tfrac12 (\partial_t V) \phi^2.$$  
Gate: with frozen $V$, $$\|\partial_t e + \nabla\cdot\mathbf{s}\|_{L^2} \le 10^{-6}$$ per step.

3. Plane-wave calibration (uniform medium):  
Gate: $$\|\langle\mathbf{s}\rangle - \mathbf{s}_{\text{analytic}}\|/\|\mathbf{s}_{\text{analytic}}\| \le 0.5\%,$$ and grid/time refinement halves the error (2nd order).

### Phase B — Open-Port Optics (uniform $V$)

1. Power accounting with two outlets (absorber/PML):  
Gate: $$\frac{\mathrm{d}}{\mathrm{d}t}\sum e = -\int_{\Gamma_A\cup\Gamma_B} \mathbf{s}\cdot\mathbf{n}\,\mathrm{d}\ell$$ holds within ≤1%; absorber loss quantified and ≤2%.

2. Symmetry null (symmetric geometry, centered source):  
Gate: $$\left|\bar F_A-\bar F_B\right|/(\bar F_A+\bar F_B) \le 1\%.$$

3. Port-closure ablation:  
Gate: closed-port flux < $10^{-6}$ of open-port flux.

### Phase C — Channel Map Engaged (frozen $V(x,y)$)

1. Map immutability & determinism receipts: identical hashes; bitwise determinism pass.

1. Routing claim (photonic): wavepacket or CW source, measure late-window averages $\bar F_{A,B}$.  

KPIs & Gates:

- Routing efficiency: $$\eta = \frac{\bar F_A}{\bar F_A + \bar F_B}.$$ CI excludes 0.5 by preregistered margin if map favors A.  
- Map null: replace $V$ by its $y$-average; bias collapses to within 1% of symmetry.  
- Grid/time independence: doubling resolution, halving $\Delta t$ changes $\eta$ by ≤2%.

1. RJ is diagnostic only (spectrum-shape sanity); no gate.

## Experimental Design

- Grid: $(N_x, N_y)$ with spacing $a$; centered differences; leapfrog time integration.  
- BCs: periodic (A) and reflecting or absorbing/PML (B).  
- Sources: plane wave (A3) and compact wavepacket (B,C).  
- Measurements: $E(t)$, $\|\partial_t e + \nabla\cdot\mathbf{s}\|_{L^2}$, outlet powers $F_{A,B}(t)$.

## Implementation Plan (no execution until approved)

- Runner: `Derivation/code/physics/thermo_routing/wave_flux_meter/run_wave_flux_meter_v1.py`  
- Schema: `Derivation/code/physics/thermo_routing/wave_flux_meter/wave-flux-meter-summary-v1.schema.json`  
- Proposed tag: `thermo-routing-v2-wave-meter`  
- Approvals manifest: add `thermo-routing-v2-wave-meter` with schema path, approved_by: Justin K. Lietz, and script-scoped approval key via `approve_tag.py`.

## Artifact Policy

Each run produces at minimum:

- PNG: energy/flux traces or maps  
- CSV: metrics (E drift, balance residuals, power accounting)  
- JSON: summary with compliance receipts and gates

## Risks and Mitigations

- Stability/CFL: enforce $\Delta t \le C a / c$; monitor energy drift across refinements.  
- Absorbers: quantify and report absorber loss (B4).  
- Discretization error: demonstrate 2nd-order convergence (A3).

## Reproducibility

- Map hash receipts; single-thread BLAS/FFT receipts; deterministic seeds; commit hash.  
- All artifacts via common IO; quarantine unapproved runs.

## References

- L. D. Landau and E. M. Lifshitz, Electrodynamics of Continuous Media.  
- J. D. Jackson, Classical Electrodynamics (Poynting vector and energy flow).  
- Standard scalar wave energy and flux formulations (e.g., acoustics texts).
