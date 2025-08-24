# Fluids Limit (Reduction to Navierâ€“Stokes)

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
- Show that the framework admits a regime whose macroscopic dynamics obey Navierâ€“Stokes (NS). Provide:
  1) An operational construction via a kinetic/Latticeâ€“Boltzmann (LBM) sector that yields NS with identified viscosity.
  2) A structural reduction template from conserved fields, symmetries, and constitutive closure.

Status and Scope
- RD sector remains canonical (validated Fisherâ€“KPP front speed). Fluids is an additional, scoped sector with its own derivation and benchmarks. Claims are restricted to this file and its benchmarks.

---

## Part I â€” Operational reduction via kinetic/LBM

### I.1 Discrete kinetic model (D2Q9 BGK)
Let f_i(x, t) be particle populations with discrete velocities c_i and weights w_i. One BGK time step (dx = dt = 1 in lattice units):
f_i(x + c_i Î”t, t + Î”t) âˆ’ f_i(x, t) = âˆ’(Î”t/Ï„) [ f_i(x, t) âˆ’ f_i^eq(Ï, v) ].

Macroscopic fields:
Ï = Î£_i f_i,â€ƒÏ v = Î£_i c_i f_i.

Equilibrium (second order in v):
f_i^eq = w_i Ï [ 1 + (c_iÂ·v)/c_s^2 + (c_iÂ·v)^2/(2 c_s^4) âˆ’ v^2/(2 c_s^2) ],
with lattice sound speed c_s fixed by {c_i, w_i} (D2Q9: c_s^2 = 1/3).

Implementation plan
- Module: [lbm2d.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1)
- Supports: periodic boundaries, bounceâ€‘back noâ€‘slip walls, simple forcing hook, viscosity Î½ = c_s^2(Ï„ âˆ’ 1/2).

### I.2 Chapmanâ€“Enskog expansion (sketch)
Introduce small Knudsen Îµ and expand f_i = f_i^(0) + Îµ f_i^(1) + Â·Â·Â·, with âˆ‚_t = Îµ âˆ‚_{t1} + Îµ^2 âˆ‚_{t2} and âˆ‡ = Îµ âˆ‡_1.
- O(Îµ): mass and momentum conservation.
- O(Îµ^2): Newtonian viscous stress.
In the incompressible scaling:
âˆ‚_t v + (vÂ·âˆ‡)v = âˆ’âˆ‡p/Ï + Î½ âˆ‡^2 v + f,â€ƒâˆ‡Â·v = 0,
with kinematic viscosity Î½ = c_s^2 (Ï„ âˆ’ Î”t/2).

Conclusion
- The kinetic/LBM sector reduces to incompressible NS with explicit Î½.

### I.3 Embedding in this repository
- New module: [lbm2d.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1) (D2Q9 BGK).
- Benchmarks using shared logging/figure style:
  - Taylorâ€“Green vortex: [taylor_green_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1)
  - Lidâ€‘driven cavity: [lid_cavity_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:1)
- Acceptance thresholds: see [BENCHMARKS_FLUIDS.md](Prometheus_FUVDM/BENCHMARKS_FLUIDS.md:1).

---

## Part II â€” Structural reduction from conserved fields

### II.1 Fields and symmetries
Introduce mass density Ï(x, t), momentum g = Ï v (and energy/entropy if thermal). Impose:
- Galilean invariance; spatial isotropy; frame objectivity.
- Local balances:
  âˆ‚_t Ï + âˆ‡Â·(Ï v) = 0,
  âˆ‚_t g + âˆ‡Â·(g âŠ— v) = âˆ’âˆ‡p + âˆ‡Â·Ï„ + Ï f.

### II.2 Constitutive closure (gradient expansion)
Assume rapid local equilibration â†’ Newtonian stress at leading order:
Ï„ = Î· (âˆ‡v + âˆ‡v^T) + (Î¶ âˆ’ 2Î·/3)(âˆ‡Â·v) I + O(|âˆ‡v|^2).
With isothermal, incompressible closure (âˆ‡Â·v = 0, Ï = Ï_0), obtain standard NS with Î½ = Î·/Ï_0.

### II.3 Parameter identification
From microparameters (e.g., collision time Ï„ in LBM, lattice units) identify:
- Î½ = c_s^2(Ï„ âˆ’ Î”t/2) (LBM sector), or
- Î½ = Î·/Ï_0 (continuum closure).
Higherâ€‘order terms become negligible in longâ€‘time/longâ€‘wavelength scaling.

Conclusion
- Under hydrodynamic scaling, the conservedâ€‘field sector reduces to NS.

---

## Part III â€” Benchmarks and Acceptance

Benchmarks
1) Taylorâ€“Green vortex (2â€‘D periodic): energy E(t) = E0 exp(âˆ’2 Î½ k^2 t). Fit Î½ from decay and match input Î½ within threshold.
2) Lidâ€‘driven cavity: centerline profiles at Re âˆˆ {100, 400, 1000} converge with grid; divergence norm small.
3) Divergence control: report â€–âˆ‡Â·vâ€–_2 over time; require gridâ€‘convergent decrease.

Acceptance thresholds (double precision)
- Taylorâ€“Green: |Î½_fit âˆ’ Î½_th| / Î½_th â‰¤ 5% at baseline grid (â‰¥ 256^2).
- Lidâ€‘driven cavity: max_t â€–âˆ‡Â·vâ€–_2 â‰¤ 1eâˆ’6.
- Convergence under grid refinement consistent with scheme order.
- JSON includes passed boolean, key metrics, figure path, timestamp.
Details in [BENCHMARKS_FLUIDS.md](Prometheus_FUVDM/BENCHMARKS_FLUIDS.md:1).

---

## Relation to the existing RD path

- RD Fisherâ€“KPP front speed (canonical RD check) remains unchanged; see:
  - Validation: [rd_front_speed_validation.md](reaction_diffusion/rd_front_speed_validation.md:1)
  - Experiment: [rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py:1)
- Fluids claims are restricted to this sector and its benchmarks; the sectors live sideâ€‘byâ€‘side to preserve scope discipline.

---

## Deliverables and Paths (for implementation)

- Derivation: this file.
- Module: [lbm2d.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1) (D2Q9 BGK).
- Benchmarks:
  - [taylor_green_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1)
  - [lid_cavity_benchmark.py](Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:1)
- Acceptance: [BENCHMARKS_FLUIDS.md](Prometheus_FUVDM/BENCHMARKS_FLUIDS.md:1)
- Outputs:
  - Figures â†’ derivation/code/outputs/figures/fluid_dynamics/
  - Logs â†’ derivation/code/outputs/logs/fluid_dynamics/
  - JSON includes metrics and passed boolean.

Notes
- The RD sector remains canonical; fluids is additive. Public phrasing should reflect that the framework contains a fluids sector that reduces to NS (LBM route) and passes standard benchmarks within stated tolerances.
