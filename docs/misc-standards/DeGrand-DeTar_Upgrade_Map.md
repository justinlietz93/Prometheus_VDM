# DeGrand–DeTar Upgrade Map for VDM

Scope: This note maps concrete documentation upgrades into VDM canon inspired by the lattice QCD practice distilled by DeGrand & DeTar. It records anchors only and avoids duplicating equations or numbers. Book reference:

- [Lattice Methods for Quantum Chromodynamics — DeGrand & DeTar (PDF)](Derivation/References/Lattice-Field-Theory_&_Discrete-Action-Principles/Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf)

This file is a navigator. Authoritative definitions and gates live at the anchors below.

## Changes landed (anchors)

- HMC acceptance and ΔH QC KPIs → [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
  - Acceptance vs stepsize: [kpi-hmc-acceptance-vs-stepsize](Derivation/VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize)
  - ΔH histogram diagnostics: [kpi-hmc-deltaH-hist](Derivation/VALIDATION_METRICS.md#kpi-hmc-deltaH-hist)
- Chain UQ discipline → [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
  - τ_int: [kpi-tau-int](Derivation/VALIDATION_METRICS.md#kpi-tau-int)
  - τ-aware binning: [kpi-binning-adequacy](Derivation/VALIDATION_METRICS.md#kpi-binning-adequacy)
  - Correlated χ² with SVD truncation: [kpi-correlated-chi2-svd](Derivation/VALIDATION_METRICS.md#kpi-correlated-chi2-svd)
  - Resample CI stability (jackknife/bootstrap): [kpi-resample-ci-stability](Derivation/VALIDATION_METRICS.md#kpi-resample-ci-stability)
- Scale‑program/RG collapse KPI → [kpi-rg-collapse](Derivation/VALIDATION_METRICS.md#kpi-rg-collapse)
- Formal definitions supporting the KPIs → [EQUATIONS.md](Derivation/EQUATIONS.md)
  - HMC accept rule and ΔH: [VDM-E-130](Derivation/EQUATIONS.md#vdm-e-130), [VDM-E-131](Derivation/EQUATIONS.md#vdm-e-131)
  - τ_int and τ‑aware binning: [VDM-E-132](Derivation/EQUATIONS.md#vdm-e-132), [VDM-E-133](Derivation/EQUATIONS.md#vdm-e-133)
  - Correlated χ² + SVD cutoff: [VDM-E-134](Derivation/EQUATIONS.md#vdm-e-134)
  - Blocked jackknife/bootstrap: [VDM-E-135](Derivation/EQUATIONS.md#vdm-e-135)
  - RG blocking operator and scaling map: [VDM-E-136](Derivation/EQUATIONS.md#vdm-e-136)
- Algorithms/pseudocode adapters → [ALGORITHMS.md](Derivation/ALGORITHMS.md)
  - HMC leapfrog + Metropolis: [VDM-A-030](Derivation/ALGORITHMS.md#vdm-a-030)
  - RHMC outline (rational approximants + multishift): [VDM-A-031](Derivation/ALGORITHMS.md#vdm-a-031)
  - CG/BiCGStab adapters: [VDM-A-032](Derivation/ALGORITHMS.md#vdm-a-032), [VDM-A-033](Derivation/ALGORITHMS.md#vdm-a-033)
  - Even–odd (red–black) preconditioning: [VDM-A-034](Derivation/ALGORITHMS.md#vdm-a-034)
  - Multishift CG: [VDM-A-035](Derivation/ALGORITHMS.md#vdm-a-035)
  - RG blocking utility: [VDM-A-036](Derivation/ALGORITHMS.md#vdm-a-036)
- RESULTS authoring checklists extended → [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

## Validation gates (summary, see anchors for exact text)

- Acceptance vs stepsize (leapfrog): fit 1−α(ε) on log–log axes; slope p ∈ [3.5, 4.5], R² ≥ 0.98.
- ΔH histograms per ε: center/skew constraints with JSON moments logged.
- τ_int reporting with window rule; ESS = N/(2τ_int).
- τ‑aware binning: B ≥ 2·τ_int and CI‑width stability under B→2B with ≤10% relative change.
- Correlated χ² with SVD cutoff sweep: χ²/dof in [0.7, 1.3] and parameter drift ≤ 0.10σ past knee.
- RG collapse after blocking/rescaling: envelope E_max ≤ 0.02 (A6 gate).

## Axiom linkages

- A4 (Dual generators, J ⊕ M): Use HMC acceptance scaling and ΔH diagnostics as reversibility/volume‑preservation instruments for J‑flows. See [AXIOMS.md](Derivation/AXIOMS.md).
- A6 (Scale program): Use RG blocking operator and envelope gate to demonstrate scale collapse. See [AXIOMS.md](Derivation/AXIOMS.md).

No numbers are duplicated here; the normative definitions and thresholds live at the linked anchors.

## Implementation notes and non-goals

- These changes are documentation and KPI‑level only. Code helpers (τ_int estimators, blocked resampling, SVD‑regularized fits, HMC runners) will be proposed separately under [code/common](Derivation/code/common) with io_paths routing and artifact schemas.
- RHMC and solver adapters remain framework‑neutral; multishift CG and even–odd preconditioning are recorded as patterns to implement under AMD‑friendly stacks.
- All artifacts must follow RESULTS standards: one PNG + one CSV + one JSON per figure, with seeds and commit hash in captions.

## Provenance and future work

- This mapping is derived from established lattice practices (DeGrand & DeTar) and is consistent with VDM’s metriplectic discipline.
- Next patches will add cross‑links inside [AXIOMS.md](Derivation/AXIOMS.md) sections A4 and A6 to these KPIs, and propose minimal helper implementations.