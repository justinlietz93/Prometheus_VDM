# Proposal: KG ⊕ RD Metriplectic Experiment (Two-Field)

Date: 2025-10-06
Owner: Justin K. Lietz

## Goal

Establish a metriplectic composition for a coupled two-field system with:

- J (conservative): Klein-Gordon (KG) field with symplectic integrator and Noether currents.
- M (dissipative): Reaction-diffusion (RD) field via Discrete-Gradient (DG) step (existing).
- Composition: Strang (JMJ) with clear, falsifiable gates.

## Why now

The metriplectic chapter for 1D RD is frozen: M-only obeys the H-theorem exactly and JMJ shows commutator-limited order. Moving upstream to KG⊕RD introduces real conservative structure (Noether currents) to test the theory at higher fidelity.

## Minimal scope (MVP)

- 1D periodic grid; reuse I/O, artifact hygiene, and seed/median infra.
- Implement KG J-only step (symplectic, e.g., velocity Verlet or leapfrog) with:
  - Reversibility check: advance Δt then -Δt.
  - Noether currents (energy/momentum) drift checks.
- Reuse RD DG for M-only (existing), with Lyapunov monotonicity.
- Compose JMJ for the coupled system; measure order via two-grid medians and report Strang defect when helpful.

## Gates (hard where meaningful)

- J-only (KG):
  - Reversibility: ∥W₂-W₀∥∞ ≤ c·ε_mach·√N (log measured c).
  - Noether drifts: |ΔE|, |ΔP| within cap scaling with ε_mach·T (log constants).
- M-only (RD DG):
  - H-theorem: ΔL_h ≤ 0 per step (violations = 0).
  - Two-grid slope: report (expect ~3 as in RD); R² ≥ 0.999.
- JMJ (KG⊕RD):
  - H-theorem: ΔL_h ≤ 0 per step (violations = 0).
  - Noether: report drift magnitudes (expected small but not zero under dissipation).
  - Two-grid slope: observational; document commutator limitations (expect ~2.6-3 depending on coupling strength).

## Plan of work

1. Scaffold KG J-only step
   - Implement velocity Verlet/leapfrog for KG in `physics/kg/`.
   - Add `j_step` wrapper for KG into `metriplectic/compose.py` (parallel to spectral J).
   - Add Noether energy/momentum calculators; wire reversibility + Noether checks.
2. Integrate with existing harness
   - Extend `run_metriplectic.py` to support KG⊕RD mode and artifact paths `outputs/{figures,logs}/kg_metriplectic`.
   - Reuse seed/median, two-grid, defect diagnostics, and Lyapunov series.
3. Run a minimal sweep
   - N=256, seeds=10, dt = [0.02, 0.01, 0.005, 0.0025].
   - Record gates and artifacts; update a new RESULTS file `derivation/kg_metriplectic/RESULTS_KG_plus_RD.md`.

## Risks & notes

- Higher-order composition beyond Strang is constrained by the Sheng-Suzuki barrier; we’ll report commutator limits rather than "force" higher order.
- Ensure stability for KG time step; document CFL-like constraints.
- Keep thresholds explicit and logged; do not silently weaken.

## Deliverables

- New KG module with J-only step and Noether diagnostics.
- Updated harness with KG⊕RD mode and artifact hygiene.
- RESULTS document with pinned artifacts, gates, and a concise theory primer.
