# DeGrand–DeTar Upgrade Map for VDM

Scope: This note maps concrete documentation upgrades into VDM canon inspired by the lattice QCD practice distilled by DeGrand & DeTar. It records anchors only and avoids duplicating equations or numbers. Book reference:

- [Lattice Methods for Quantum Chromodynamics — DeGrand & DeTar (PDF)](../../../Derivation/References/Lattice-Field-Theory_&_Discrete-Action-Principles/Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf)

This file is a navigator. Authoritative definitions and gates live at the anchors below.

## Changes landed (anchors)

- HMC acceptance and ΔH QC KPIs → [00_VALIDATION_METRICS.md](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)
  - Acceptance vs stepsize: [kpi-hmc-acceptance-vs-stepsize](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize)
  - ΔH histogram diagnostics: [kpi-hmc-deltaH-hist](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-deltah-hist)
- Chain UQ discipline → [00_VALIDATION_METRICS.md](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)
  - τ_int: [kpi-tau-int](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-tau-int)
  - τ-aware binning: [kpi-binning-adequacy](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-binning-adequacy)
  - Correlated χ² with SVD truncation: [kpi-correlated-chi2-svd](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-correlated-chi2-svd)
  - Resample CI stability (jackknife/bootstrap): [kpi-resample-ci-stability](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-resample-ci-stability)
- Scale‑program/RG collapse KPI → [kpi-rg-collapse](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-rg-collapse)
- Formal definitions supporting the KPIs → [00_EQUATIONS.md](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md)
  - HMC accept rule and ΔH: [VDM-E-130](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-130), [VDM-E-131](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-131)
  - τ_int and τ‑aware binning: [VDM-E-132](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-132), [VDM-E-133](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-133)
  - Correlated χ² + SVD cutoff: [VDM-E-134](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-134)
  - Blocked jackknife/bootstrap: [VDM-E-135](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-135)
  - RG blocking operator and scaling map: [VDM-E-136](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-136)
- Algorithms/pseudocode adapters → [00_ALGORITHMS.md](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md)
  - HMC leapfrog + Metropolis: [VDM-A-030](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-030)
  - RHMC outline (rational approximants + multishift): [VDM-A-031](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-031)
  - CG/BiCGStab adapters: [VDM-A-032](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-032), [VDM-A-033](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-033)
  - Even–odd (red–black) preconditioning: [VDM-A-034](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-034)
  - Multishift CG: [VDM-A-035](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-035)
  - RG blocking utility: [VDM-A-036](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-036)
- RESULTS authoring checklists extended → [RESULTS_PAPER_STANDARDS.md](../../../Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md)

## Validation gates (summary — refer to KPIs for thresholds)

- Acceptance vs stepsize (leapfrog): thresholds defined at [kpi-hmc-acceptance-vs-stepsize](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize).
- ΔH histogram diagnostics: definitions at [kpi-hmc-deltaH-hist](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-deltah-hist).
- τ_int reporting and ESS: definitions at [kpi-tau-int](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-tau-int).
- τ‑aware binning and CI stability: definitions at [kpi-binning-adequacy](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-binning-adequacy).
- Correlated χ² with SVD cutoff sweep: thresholds at [kpi-correlated-chi2-svd](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-correlated-chi2-svd).
- RG collapse envelope (A6): thresholds at [kpi-rg-collapse](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-rg-collapse).

## Axiom linkages

- A4 (Dual generators, J ⊕ M): Use HMC acceptance scaling and ΔH diagnostics as reversibility/volume‑preservation instruments for J‑flows. See [AXIOMS.md](../../../Derivation/AXIOMS.md).
- A6 (Scale program): Use RG blocking operator and envelope gate to demonstrate scale collapse. See [AXIOMS.md](../../../Derivation/AXIOMS.md).

No numbers are duplicated here; the normative definitions and thresholds live at the linked anchors.

## Implementation notes and non-goals

- These changes are documentation and KPI‑level only. Code helpers (τ_int estimators, blocked resampling, SVD‑regularized fits, HMC runners) will be proposed separately under [code/common](../../../Derivation/code/common) with io_paths routing and artifact schemas.
- RHMC and solver adapters remain framework‑neutral; multishift CG and even–odd preconditioning are recorded as patterns to implement under AMD‑friendly stacks.
- All artifacts must follow RESULTS standards: one PNG + one CSV + one JSON per figure, with seeds and commit hash in captions.

## Provenance and future work

- This mapping is derived from established lattice practices (DeGrand & DeTar) and is consistent with VDM’s metriplectic discipline.
- Next patches will add cross‑links inside [AXIOMS.md](../../../Derivation/AXIOMS.md) sections A4 and A6 to these KPIs, and propose minimal helper implementations.

## Actionable subsections (navigator — do-first patches)

Principle: add links and gates only; do not duplicate equations or numbers. Canon owns definitions. Each item lists canon anchors to update/read and the expected artifacts per run. Use [Derivation/code/common/io_paths.py](../../../Derivation/code/common/io_paths.py) for routing and [Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md](../../../Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md) for artifact minima.

1) HMC exactness for J-flows (A4)  

- Canon anchors:  
  - Equations: [Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-130](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-130), [Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-131](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-131)  
  - KPIs: [Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize), [Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-deltah-hist](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-hmc-deltah-hist)  
  - Algorithms: [Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-030](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-030), [Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-031](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-031)  
- Actions: instrument acceptance(ε) vs stepsize and ΔH hist per trajectory; require reversible/volume-preserving proposal tested via round-trip residuals (log JSON).  
- Artifacts (per sweep): 1 PNG panel (α vs ε + ΔH hist), 1 CSV (ε, α, moments), 1 JSON (moments, seeds, commit).

2) Chain UQ: τ_int, τ-aware binning, ESS (A7)  

- Canon anchors:  
  - Equations: [Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-132](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-132), [Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-133](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-133)  
  - KPIs: [Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-tau-int](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-tau-int), [Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-binning-adequacy](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-binning-adequacy)  
- Actions: compute τ_int with standard windowing; enforce B ≥ 2·τ_int auto-binning; report ESS = N/(2τ_int) and CI stability under B→2B.  
- Artifacts: 1 PNG (CI vs bin-size), 1 CSV (bin, mean, CI), 1 JSON (τ_int, ESS, seeds, commit).

3) Correlated fits with SVD truncation  

- Canon anchors:  
  - Equations: [Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-134](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-134)  
  - KPIs: [Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-correlated-chi2-svd](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-correlated-chi2-svd)  
- Actions: fit with full covariance; sweep SVD cutoff; report χ²/dof and parameter drift vs cutoff; pick knee-region window.  
- Artifacts: 1 PNG (χ²/dof vs cutoff), 1 CSV (cutoff, χ²/dof, params), 1 JSON (eigs, window, seeds, commit).

4) Jackknife/bootstrap with blocking  

- Canon anchors:  
  - Equations: [Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-135](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-135)  
  - KPIs: [Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-resample-ci-stability](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-resample-ci-stability)  
- Actions: choose block length J ≥ τ_int; emit jackknife and bootstrap CIs; verify CI-width stability across J ∈ {τ_int, 2τ_int}.  
- Artifacts: 1 PNG (CI vs J), 1 CSV (J, CI_low, CI_high), 1 JSON (J rule, seeds, commit).

5) Scale program: RG blocking and scaling collapse (A6)  

- Canon anchors:  
  - Equations: [Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-136](../../../Derivation/z.CANONICAL_Equations/00_EQUATIONS.md#vdm-e-136)  
  - KPI: [Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-rg-collapse](../../../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-rg-collapse)  
- Actions: apply block-spin/field operator at s ∈ {2,4}; rescale to dimensionless axes; compute collapse envelope E_max vs reference; assert gate thresholds from canon.  
- Artifacts: 1 PNG (collapse + envelope), 1 CSV (t, z_s, ref), 1 JSON (E_max, seeds, commit).

6) Sparse solvers and preconditioning (software practice)  

- Canon anchors:  
  - Algorithms: [Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-032](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-032), [Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-033](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-033), [Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-034](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-034), [Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-035](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-035)  
- Actions: record CG/BiCGStab iteration counts, residual trends, and even–odd speedups; optional multishift timing table.  
- Artifacts: 1 PNG (residual vs iter), 1 CSV (iter, residual, precond flag), 1 JSON (tols, precond, seeds, commit).

7) RHMC for fractional-power actions  

- Canon anchors:  
  - Algorithms: [Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-031](../../../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-031)  
  - KPIs: reuse HMC acceptance/ΔH gates  
- Actions: switch to RHMC when metric-side functionals require fractional powers; verify acceptance scaling mirrors HMC shape; log rational approximant degree and multishift details.  
- Artifacts: 1 PNG (acceptance vs ε), 1 CSV (ε, α), 1 JSON (approx spec, seeds, commit).

8) AXIOMS cross-links (no duplication)  

- A4 (dual generators, reversibility/volume preservation): [Derivation/AXIOMS.md](../../../Derivation/AXIOMS.md) — reference HMC gates as instruments for J-only flows.  
- A6 (scale program): [Derivation/AXIOMS.md](../../../Derivation/AXIOMS.md) — reference RG blocking and collapse envelope gate.

Provenance  

- Source text: [Derivation/References/Lattice-Field-Theory_&_Discrete-Action-Principles/Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf](../../../Derivation/References/Lattice-Field-Theory_&_Discrete-Action-Principles/Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf)  
- This navigator remains anchor-only and defers to canon for normative content and thresholds.
