<!-- DOC-GUARD: REFERENCE -->
# Quantum Gravity Bridge - Proposal (v1)

Author: Justin K. Lietz  
Date: 2025-10-06

## 1. Abstract

We propose an observational bridge program connecting VDM’s gravitational and portal predictions to public cosmology and HEP datasets (Planck, DES, BOSS, LHC/NA64), with gates-first discipline. The immediate aim is to construct reproducible pipelines that (i) propagate VDM-consistent FRW backgrounds and perturbations into linear observables, and (ii) scope dark-photon kinetic-mixing constraints via detector noise budgets and quick Fisher estimates with finite-difference cross-checks. This whitepaper defines acceptance gates, datasets, and artifact standards; it does not claim novel physics, only a disciplined confrontation with data.

## 2. Background & Scientific Rationale

- Motivation: VDM asserts that observed regimes map to RD axioms under explicit conditions. Two near-term observational threads are (a) gravity via FRW continuity and perturbations, and (b) dark-photon portals via kinetic mixing. Public datasets allow stress-tests without new experiments.
- Relevance: A pass/fail pipeline with explicit gates raises the bar over narrative alignment. Even null results (tighter gates) are valuable.
- Prior foundations: FRW continuity (reference to `EQUATIONS.md#vdm-e-0xx`), linear growth/transfer (CLASS/CAMB), portal searches (e.g., NA64, BaBar, LHCb constraints on A′), cosmological limits on extra radiation (Neff) and dark-sector energy injection.

## 3. Scope and Starting Equations (reference-only)

- FRW continuity residual gate: RMS of $d/dt(\rho a^3) + w\,\rho\,d/dt(a^3)$ with dust $w=0$ baseline (see `VALIDATION_METRICS.md#kpi-frw-continuity-rms`).
- Linear perturbations: growth factor D(z), matter power P(k,z), CMB TT/TE/EE spectra via CLASS/CAMB (external tools; this proposal wires inputs/outputs only).
- Dark photons: detector noise PSD models and SNR integration; Fisher information for mixing $\varepsilon$; finite-difference consistency gate (see `VALIDATION_METRICS.md#kpi-dp-fisher-consistency`).

## 4. Experimental Setup and Diagnostics

- Tooling:
  - Cosmology: CLASS or CAMB CLI bindings; results marshalled into JSON/CSV with provenance.
  - Portals: Python analyses for noise budgets and Fisher quick estimates.
- Diagnostics & acceptance gates:
  - FRW: `RMS_FRW ≤ tol_rms` with default `1e-6`; figure + CSV series; CONTRADICTION_REPORT on fail.
  - Dark photons: regime split annotated; Fisher finite-difference relative error ≤ 0.10; figures and JSON logs.
- Artifacts: follow `PAPER_STANDARDS.md`; every figure must have a CSV/JSON sidecar; logs include seeds, commit, environment.

## 5. Experimental Runplan

- Phase A (Gravity):
  1) Reproduce FRW dust sanity (already PASS). 2) Integrate CLASS/CAMB to compute linear observables from FRW+units maps. 3) Produce a minimal P(k,z) and CMB spectra comparison against Planck/DES public curves; gate on pipeline reproducibility and basic χ² sanity (document, no hard χ² gate in v1).
- Phase B (Portals):
  1) Implement noise budget calculator and plot with regime annotations. 2) Implement Fisher quick with finite-difference cross-check. 3) Scope one detector case study and emit artifacts.

## 6. Personnel

Justin K. Lietz - implement pipelines, set gates, produce artifacts, and write up; review acceptance results and adjust thresholds.

## 7. Deliverables & Data Products

- Cosmology:
  - Figures: `derivation/code/outputs/figures/cosmology/frw_continuity_residual__<tag>.png`
  - Logs: `derivation/code/outputs/logs/cosmology/frw_balance__<tag>.json`, CSV series `.../frw_continuity_residual__<tag>.csv`
- Dark photons:
  - Figures: `derivation/code/outputs/figures/dark_photons/noise_budget__<tag>.png`, `.../eft_ladder__<tag>.png`
  - Logs: `derivation/code/outputs/logs/dark_photons/noise_budget__<tag>.{json,csv}`, `.../fisher_eps__<tag>.json`

## 8. Risks and Mitigations

- Cross-domain systematics: maintain partition mapping docs; version datasets and priors.
- External tools drift: pin tool versions and record in provenance.
- Overfitting gates: keep v1 gates structural (residual presence, reproducibility) rather than tight χ² claims.

## 9. References

- CLASS: Blas, Lesgourgues, Tram (2011). CAMB: Lewis, Challinor, Lasenby (2000).
- Dark photons overview: Jaeckel & Ringwald (2010); Alexander et al. (2016) Snowmass; NA64/BaBar/LHCb constraints.
- Cosmology datasets: Planck 2018 results; DES Y3.
