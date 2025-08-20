# Fluids Limit (Reduction to Navier–Stokes)

>
> Author: Justin K. Lietz  
> Date: August 9, 2025
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.<br>
> Commercial use requires written permission from Justin K. Lietz.
> 
> See LICENSE file for full terms.

Purpose
- Show that the framework admits a regime whose macroscopic dynamics obey Navier–Stokes (NS). Provide:
  1) An operational construction via a kinetic/Lattice–Boltzmann (LBM) sector that yields NS with identified viscosity.
  2) A structural reduction template from conserved fields, symmetries, and constitutive closure.

Status and Scope
- RD sector remains canonical (validated Fisher–KPP front speed). Fluids is an additional, scoped sector with its own derivation and benchmarks. Claims are restricted to this file and its benchmarks.

---

## Part I — Operational reduction via kinetic/LBM

### I.1 Discrete kinetic model (D2Q9 BGK)
Let f_i(x, t) be particle populations with discrete velocities c_i and weights w_i. One BGK time step (dx = dt = 1 in lattice units):
f_i(x + c_i Δt, t + Δt) − f_i(x, t) = −(Δt/τ) [ f_i(x, t) − f_i^eq(ρ, v) ].

Macroscopic fields:
ρ = Σ_i f_i, ρ v = Σ_i c_i f_i.

Equilibrium (second order in v):
f_i^eq = w_i ρ [ 1 + (c_i·v)/c_s^2 + (c_i·v)^2/(2 c_s^4) − v^2/(2 c_s^2) ],
with lattice sound speed c_s fixed by {c_i, w_i} (D2Q9: c_s^2 = 1/3).

Implementation plan
- Module: [lbm2d.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1)
- Supports: periodic boundaries, bounce‑back no‑slip walls, simple forcing hook, viscosity ν = c_s^2(τ − 1/2).

### I.2 Chapman–Enskog expansion (sketch)
Introduce small Knudsen ε and expand f_i = f_i^(0) + ε f_i^(1) + ···, with ∂_t = ε ∂_{t1} + ε^2 ∂_{t2} and ∇ = ε ∇_1.
- O(ε): mass and momentum conservation.
- O(ε^2): Newtonian viscous stress.
In the incompressible scaling:
∂_t v + (v·∇)v = −∇p/ρ + ν ∇^2 v + f, ∇·v = 0,
with kinematic viscosity ν = c_s^2 (τ − Δt/2).

Conclusion
- The kinetic/LBM sector reduces to incompressible NS with explicit ν.

### I.3 Embedding in this repository
- New module: [lbm2d.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1) (D2Q9 BGK).
- Benchmarks using shared logging/figure style:
  - Taylor–Green vortex: [taylor_green_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1)
  - Lid‑driven cavity: [lid_cavity_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:1)
- Acceptance thresholds: see [BENCHMARKS_FLUIDS.md](Prometheus_FUVDM/BENCHMARKS_FLUIDS.md:1).

---

## Part II — Structural reduction from conserved fields

### II.1 Fields and symmetries
Introduce mass density ρ(x, t), momentum g = ρ v (and energy/entropy if thermal). Impose:
- Galilean invariance; spatial isotropy; frame objectivity.
- Local balances:
  ∂_t ρ + ∇·(ρ v) = 0,
  ∂_t g + ∇·(g ⊗ v) = −∇p + ∇·τ + ρ f.

### II.2 Constitutive closure (gradient expansion)
Assume rapid local equilibration → Newtonian stress at leading order:
τ = η (∇v + ∇v^T) + (ζ − 2η/3)(∇·v) I + O(|∇v|^2).
With isothermal, incompressible closure (∇·v = 0, ρ = ρ_0), obtain standard NS with ν = η/ρ_0.

### II.3 Parameter identification
From microparameters (e.g., collision time τ in LBM, lattice units) identify:
- ν = c_s^2(τ − Δt/2) (LBM sector), or
- ν = η/ρ_0 (continuum closure).
Higher‑order terms become negligible in long‑time/long‑wavelength scaling.

Conclusion
- Under hydrodynamic scaling, the conserved‑field sector reduces to NS.

---

## Part III — Benchmarks and Acceptance

Benchmarks
1) Taylor–Green vortex (2‑D periodic): energy E(t) = E0 exp(−2 ν k^2 t). Fit ν from decay and match input ν within threshold.
2) Lid‑driven cavity: centerline profiles at Re ∈ {100, 400, 1000} converge with grid; divergence norm small.
3) Divergence control: report ‖∇·v‖_2 over time; require grid‑convergent decrease.

Acceptance thresholds (double precision)
- Taylor–Green: |ν_fit − ν_th| / ν_th ≤ 5% at baseline grid (≥ 256^2).
- Lid‑driven cavity: max_t ‖∇·v‖_2 ≤ 1e−6.
- Convergence under grid refinement consistent with scheme order.
- JSON includes passed boolean, key metrics, figure path, timestamp.
Details in [BENCHMARKS_FLUIDS.md](Prometheus_FUVDM/BENCHMARKS_FLUIDS.md:1).

---

## Relation to the existing RD path

- RD Fisher–KPP front speed (canonical RD check) remains unchanged; see:
  - Validation: [rd_front_speed_validation.md](rd_front_speed_validation.md:1)
  - Experiment: [rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py:1)
- Fluids claims are restricted to this sector and its benchmarks; the sectors live side‑by‑side to preserve scope discipline.

---

## Deliverables and Paths (for implementation)

- Derivation: this file.
- Module: [lbm2d.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1) (D2Q9 BGK).
- Benchmarks:
  - [taylor_green_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1)
  - [lid_cavity_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:1)
- Acceptance: [BENCHMARKS_FLUIDS.md](Prometheus_FUVDM/BENCHMARKS_FLUIDS.md:1)
- Outputs:
  - Figures → derivation/code/outputs/figures/fluid_dynamics/
  - Logs → derivation/code/outputs/logs/fluid_dynamics/
  - JSON includes metrics and passed boolean.

Notes
- The RD sector remains canonical; fluids is additive. Public phrasing should reflect that the framework contains a fluids sector that reduces to NS (LBM route) and passes standard benchmarks within stated tolerances.