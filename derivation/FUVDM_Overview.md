# FUVDM Overview

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
- Condensed, single-page overview of the Fully Unified Void Dynamics Model (FUVDM): canonical model choice, validated results, mappings, and scope boundaries. All claims below are either [PROVEN] or explicitly marked.

Canonical Model [PROVEN]
- Model class (canonical): first‑order reaction–diffusion (Fisher–KPP family)
- Continuum PDE (1D notation; extends componentwise in higher D):
  ∂t φ = D ∇²φ + r φ − u φ² [ − λ φ³ (optional stabilization) ]
- Discrete schematic (void law near homogeneous state):
  dW/dt = (α − β) W − α W²
- Mapping (discrete → continuum):
  - D = J a² (site Laplacian) or D = (J/z) a² (neighbor‑average form), r = α, u = β.
  - See normalization notes under “Discrete → Continuum & Kinetics.”

What is Proven (numeric validation)
- Front‑speed (pulled front, Fisher–KPP) [PROVEN]
  - Theory: c_front = 2√(D r).
  - Results (defaults): c_meas ≈ 0.953 vs c_th = 1.0, rel_err ≈ 0.047, R² ≈ 0.999996; passes acceptance gates.
  - Documentation: [rd_front_speed_validation.md](rd_front_speed_validation.md)
  - Script: [rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py:1)
  - Sweep: [rd_front_speed_sweep.py](code/physics/rd_front_speed_sweep.py:1)
- Linear dispersion around φ≈0 (periodic, linearized RD) [PROVEN]
  - Theory (discrete primary): σ_d(m) = r − (4D/dx²) sin²(π m/N)
  - Reference (continuum): σ(k) = r − D k² with k = 2π m/L
  - Results: default N=1024 → med_rel_err ≈ 1.45e−3, R²_array ≈ 0.99995; refinement N=2048 → med_rel_err ≈ 1.30e−3, R²_array ≈ 0.9928.
  - Documentation: [rd_dispersion_validation.md](rd_dispersion_validation.md:1)
  - Script: [rd_dispersion_experiment.py](code/physics/rd_dispersion_experiment.py:1)
- Consolidated plan and acceptance gates:
  - [rd_validation_plan.md](rd_validation_plan.md:1)
- Status log with tags and references:
  - [CORRECTIONS.md](computational_proofs/CORRECTIONS.md:1)

Stability and Fixed Points (RD)
- For r > 0, φ = 0 is dynamically unstable; the homogeneous fixed point φ* = r/u is stable.
- Optional cubic −λ φ³ is stabilization for large amplitude regimes and is off by default in the canonical validations.

Discrete → Continuum & Kinetics
- Diffusion mapping (primary): D = J a² (or (J/z) a² depending on neighbor averaging).
- Kinetic/edge normalization note (EFT context only): c² = 2 J a² (per‑site) or c² = κ a² with κ = 2J (per‑edge). This belongs to the second‑order EFT branch and is kept separate from the RD canonical narrative.
- Reference: see kinetic derivation and quarantine notes in status log [CORRECTIONS.md](computational_proofs/CORRECTIONS.md:1).

Scope Boundaries and Quarantine
- Canonical baseline is RD (first‑order in time). All effective field theory (EFT/Klein–Gordon, second‑order time) statements are quarantined to:
  - [effective_field_theory_approach.md](effective_field_theory_approach.md:1)
- Where EFT appears, the mass follows m_eff = √(α − β) (parameter‑dependent). No fixed numeric values are asserted without parameters.
- Do not mix EFT claims into the RD validation narrative.

Reproducibility and Outputs
- Derivation scripts produce:
  - Figures → derivation/code/outputs/figures/
  - Logs → derivation/code/outputs/logs/
  - Filenames: <script>_<UTC timestamp>.{png,json}
- fum_rt parity (independent runners, same metrics schema; rationale annotated in‑file):
  - Front‑speed mirror: [rd_front_speed_runner.py](Prometheus_FUVDM/fum_rt/physics/rd_front_speed_runner.py:1)
  - Dispersion mirror: [rd_dispersion_runner.py](Prometheus_FUVDM/fum_rt/physics/rd_dispersion_runner.py:1)

Design Principles (condensed)
- Single canonical model for all baseline physics claims (RD).
- Every nontrivial statement is mapped to a scriptable check with acceptance criteria (error tolerance and R² gate).
- Provenance and scope separation: EFT content retained for future work and explicitly labeled.

At‑a‑Glance Defaults (validated runs)
- Front‑speed: N=1024, L=200, D=1.0, r=0.25, T=80, cfl=0.2, seed=42, x0=−60, level=0.1, fit 0.6–0.9.
- Dispersion: N=1024, L=200, D=1.0, r=0.25, T=10, cfl=0.2, seed=42, amp0=1e−6, record=80, m_max=64, fit 0.1–0.4.

Memory Steering and Systems Notes
- Memory‑steering derivations and runtime integration are tracked separately and must reference RD canonical terms when mapping to dynamics. See:
  - [memory_steering.md](memory_steering.md:1)
  - Runtime parity and plots reside under fum_rt/core/* and fum_rt/physics/* with explicit comments when driven by proven physics.

Archive / Informal Content
- Informal transcripts or exploratory notes are labeled and non‑normative:
  - Example banner added to voxtrium note: [20250809_voxtrium_message_2.md](voxtrium/20250809_voxtrium_message_2.md:1)

Licensing and Citation
- Dual‑license banner applies (see header). Cite this overview and the specific validation documents when reusing claims or reproducing results.

Next (Roadmap snapshot)
- Navier–Stokes integration plan will follow the same standard: explicit discretization choice, stability (CFL), test observables (energy/variance spectra, decay rates), and a parity mirror under fum_rt/physics with acceptance gates and CHANGE REASON comments.

Appendix: Quick Links
- Front speed: [rd_front_speed_validation.md](rd_front_speed_validation.md:1), [rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py:1)
- Dispersion: [rd_dispersion_validation.md](rd_dispersion_validation.md:1), [rd_dispersion_experiment.py](code/physics/rd_dispersion_experiment.py:1)
- Plan: [rd_validation_plan.md](rd_validation_plan.md:1)
- Status: [CORRECTIONS.md](computational_proofs/CORRECTIONS.md:1)
- Runtime mirrors: [rd_front_speed_runner.py](Prometheus_FUVDM/fum_rt/physics/rd_front_speed_runner.py:1), [rd_dispersion_runner.py](Prometheus_FUVDM/fum_rt/physics/rd_dispersion_runner.py:1)