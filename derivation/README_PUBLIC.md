# Void Dynamics (FUVDM) - Derivation Papers (Public Overview)

This folder provides a public, paper-only view of the Void Dynamics program. It summarizes the theory and validation write-ups for review by physicists, applied mathematicians, and scientifically minded engineers. No source code is included.

## What this is
- A small set of derivation papers that establish a clean baseline physics slice using reaction-diffusion (RD).
- Additional documents that explore a future, quarantined effective field theory (EFT) branch, clearly labeled as future work.
- Each paper separates what is proven from what is plausible or speculative and, where applicable, includes acceptance criteria for simple numerical checks.

## Why it relates to AI (brief)
- The project studies how simple, local rules yield stable, interpretable global behavior under resource constraints.
- This design philosophy is relevant to AI systems that favor locality, event-driven updates, and transparent evaluation instead of opaque heuristics.
- "Memory steering" (covered separately) frames slow routing bias and retention/decay as structured influences over faster dynamics, an analogy for directing computation without black-box shortcuts.

## What's inside (papers)
- Program overview and banner:
  - [FUVDM_Overview.md](./FUVDM_Overview.md)
- Foundations:
  - [discrete_to_continuum.md](./foundations/discrete_to_continuum.md)
  - [continuum_stack.md](./foundations/continuum_stack.md)
- Reaction-Diffusion (canonical baseline):
  - [rd_front_speed_validation.md](./reaction_diffusion/rd_front_speed_validation.md)
  - [rd_dispersion_validation.md](./reaction_diffusion/rd_dispersion_validation.md)
  - [rd_validation_plan.md](./reaction_diffusion/rd_validation_plan.md)
- Memory Steering (slow routing bias; separate layer):
  - [memory_steering.md](./memory_steering/memory_steering.md)
- Finite-domain EFT modes (quarantined future work):
  - [finite_tube_mode_analysis.md](./tachyon_condensation/finite_tube_mode_analysis.md)
- Change log / scoping notes:
  - [CORRECTIONS.md](./CORRECTIONS.md)

## What's not included
- Source code, executables, or private runtime harnesses.
- Logs/figures or any artifacts sufficient to reconstruct proprietary implementations.
- Drafts outside the derivation index above.

## How to read these papers
- Each file follows a consistent structure: Purpose, Assumptions/Parameters, Discrete law, Continuum limit, PDE/Action/Potential, Fixed points and stability, Dispersion, Conservation/Lyapunov, Numerical plan + acceptance, Results, Open questions.
- Claim labels:
  - [PROVEN] = sign/dimension/limit checks plus a minimal numerical test that passes stated tolerances.
  - [PLAUSIBLE] = future work with rationale; quarantined until derivation + checks are complete.
  - [SPECULATIVE] = exploratory; not used for baseline claims.

## Licensing and scope
- These materials are shared for academic review and discussion. Commercial use requires prior written permission. See the project's license notice in the distribution or parent repository materials.
- The scope stays within theoretical physics and simulation. Broad cosmological claims are withheld or clearly labeled until backed by derivation + numeric checks.

## Citations
- When referencing specific results, cite the overview and the relevant validation paper, for example:
  - [FUVDM_Overview.md](./FUVDM_Overview.md)
  - [rd_front_speed_validation.md](./reaction_diffusion/rd_front_speed_validation.md)
  - [rd_dispersion_validation.md](./reaction_diffusion/rd_dispersion_validation.md)

## Contact
- For scope questions or clarifications about acceptance criteria, refer to the headers in the overview and topic files listed above. If you are reading this as part of a paper-only bundle, the maintainer's contact is provided alongside the distribution materials.
