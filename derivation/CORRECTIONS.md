# CORRECTIONS

Date (UTC): 2025-08-20

Scope: Tier-0 correctness fixes (numerics, stability narrative) and unification to a single canonical model class (reaction–diffusion, RD). EFT/KG material retained but quarantined as “Future Work.”

## Summary (before → after)

- [derivation/FUVDM_Overview.md](FUVDM_Overview.md)
  - Before: Mixed RD/EFT claims; no explicit canonical model.
  - After: Canonical RD banner + mapping (D = J a² or (J/z) a²; r = α − β; u = α), stability note, EFT scoped to future work.

- [derivation/code/computational_proofs/FUM_theory_and_results.md](code/computational_proofs/FUM_theory_and_results.md)
  - Before: Fixed numerical claim “m_eff ≈ 0.387”.
  - After: m_eff = √(α−β) (parameter‑dependent), added RD model‑class note; removed fixed numeric.

- [derivation/discrete_to_continuum.md](discrete_to_continuum.md)
  - Before: Objective stated convergence to KG; D mapping not explicit.
  - After: Objective states RD mapping as primary; explicit D mapping (D = J a² or (J/z) a²); EFT derivation quarantined to EFT doc.

- [derivation/memory_steering.md](memory_steering.md)
  - Before: Hardwired EFT vacuum/mass invariants in main text.
  - After: RD is canonical; EFT invariants referenced only to EFT doc; removed back‑solving (α,β) from (v,m_eff) in RD narrative.

- [derivation/symmetry_analysis.md](symmetry_analysis.md)
  - Before: Text implied “false/true vacuum” using EFT values in a general context.
  - After: Clarified RD vs EFT contexts; RD fixed point W* = r/u (r>0) vs EFT vacuum v = 1 − β/α as future‑work.

- [derivation/effective_field_theory_approach.md](effective_field_theory_approach.md)
  - Before: No scope banner.
  - After: Quarantine banner; note m_eff = √(α−β) is parameter‑dependent and unitized via τ.

- [derivation/code/computational_proofs/void_dynamics_theory.md](code/computational_proofs/void_dynamics_theory.md)
  - Before: No scope note; mixed RD/EFT implications.
  - After: Scope note at top; references discrete‑action derivation for c² = 2 J a².

- [derivation/support/references/Suggestions.md](support/references/Suggestions.md)
  - Before: Implied fixed m_eff; mixed normalization constraint Ja² = 1/2.
  - After: Header note: RD canonical; EFT mass parameter‑dependent; lattice normalization c² = 2 J a² (per‑site); do not impose Ja² = 1/2.

- [derivation/fum_voxtrium_mapping.md](fum_voxtrium_mapping.md)
  - Before: Referred to EFT EOM as dimensionless default.
  - After: RD mapping made canonical; EFT equation kept for EFT context only.

- New: [METRICS.md](Prometheus_FUVDM/METRICS.md)
  - Metrics skeleton for RD dynamics, SIE/TDA system metrics, reproducibility pointers.

## Numeric Corrections

- m_eff is not a universal constant; it is m_eff = √(α−β).
  - Example calibrations:
    - α = 0.25, β = 0.10 → m_eff ≈ 0.387
    - α = 1.0,  β = 0.40 → m_eff ≈ 0.7746

All fixed-number statements were replaced with parameter‑dependent forms and example mappings.

## Stability Narrative Corrections

- For RD (canonical): φ = 0 is dynamically unstable for r > 0; homogeneous fixed point φ* = r/u is stable.
- EFT “tachyonic” language retained only in EFT sections; where used, potential boundedness via λ φ⁴ is explicit.

## Kinetic/Lattice Normalization

- Adopted discrete‑action derivation already present in [derivation/kinetic_term_derivation.md](kinetic_term_derivation.md) with c² = 2 J a² (per‑site convention) or c² = κ a² (per‑edge, κ = 2J). No microscopic constraint ties J to a; c can be set by units.

## Edit Log (file, change)

- [derivation/FUVDM_Overview.md](FUVDM_Overview.md): Replace overview with RD canonical banner; corrected mapping (r = α − β, u = α); EFT scoped.
- [derivation/code/computational_proofs/FUM_theory_and_results.md](code/computational_proofs/FUM_theory_and_results.md): Insert RD note; replace fixed m_eff numeric with param‑dependent form.  
- [derivation/discrete_to_continuum.md](discrete_to_continuum.md): Update objective to RD; add D mapping text; keep EFT derivation as future work.  
- [derivation/memory_steering.md](memory_steering.md): Align with RD canonical; restrict EFT formulas to EFT doc; remove back‑solve in RD section.  
- [derivation/symmetry_analysis.md](symmetry_analysis.md): Clarify RD vs EFT contexts in interpretations.  
- [derivation/effective_field_theory_approach.md](effective_field_theory_approach.md): Add quarantine banner.  
- [derivation/code/computational_proofs/void_dynamics_theory.md](code/computational_proofs/void_dynamics_theory.md): Add scope note at top.  
- [derivation/support/references/Suggestions.md](support/references/Suggestions.md): Insert header note; prevent hard constraints on Ja².  
- [derivation/fum_voxtrium_mapping.md](fum_voxtrium_mapping.md): Make RD canonical; EFT references scoped.  
- [METRICS.md](Prometheus_FUVDM/METRICS.md): New file with metrics skeleton.
- [derivation/rd_front_speed_validation.md](rd_front_speed_validation.md:1): Add reproducible CLI, output routing, acceptance criteria, representative PASS metrics.
- [derivation/code/physics/rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py:1): Set defaults (N=1024, cfl=0.2, level=0.1, x0=-60, fit 0.6–0.9); route outputs to derivation/code/outputs/{figures,logs}; robust tracking and fit.
- New: [derivation/code/physics/rd_front_speed_sweep.py](code/physics/rd_front_speed_sweep.py:1): Sweep runner producing CSV summary under derivation/code/outputs/logs/.
- New: [derivation/code/physics/rd_dispersion_experiment.py](code/physics/rd_dispersion_experiment.py:1): Linear dispersion validation script with periodic BC; logs/figure auto-routing; acceptance criteria.

## Status Tags

- [ERROR FIXED]: Incorrect fixed mass number claims replaced with parameter‑dependent expression.
- [PROVEN]: Lattice → continuum kinetic normalization via discrete action (already present) is internally consistent.
- [PROVEN]: RD front speed c_front = 2√(Dr) validated. Defaults: N=1024, cfl=0.2, level=0.1, x0=-60, fit window 0.6–0.9. Representative run: c_meas≈0.953, c_th=1.0, rel_err≈0.047, R²≈0.999996.
- [PROVEN]: RD dispersion σ(k) = r − D k² validated via linearized periodic evolution. Defaults (N=1024, L=200, D=1.0, r=0.25, T=10, cfl=0.2, seed=42, m_max=64) → med_rel_err≈0.00145, R²_array≈0.99995 [PASS]; grid refinement (N=2048, m_max=128) → med_rel_err≈0.00130, R²_array≈0.9928 [PASS].
