# T2 (Instrument) - EBN‑CMB‑ISW+Lens Pipeline (A8→Boltzmann→CMB/LSS)

> Created Date:  2025-11-18  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {salted_hash}  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI), Neuroca (infrastructure).

## 3. Abstract

Proposed in this document is a T2 instrument that maps **A8 tachyonic‑genesis predictions** into a cosmology pipeline: generate a primordial spectrum from the hierarchical interface model, pass it through a Boltzmann solver (CLASS/CAMB compatible), and produce CMB TT/TE/EE spectra, lensing, and ISW observables. Acceptance gates focus on balance meters (FRW), internal consistency, and a preregistered goodness‑of‑fit envelope relative to ΛCDM, without ad‑hoc components.

## 4. Background & Scientific Rationale

A8 predicts logarithmic hierarchy depth and boundary‑law energy; this instrument operationalizes the translation to cosmological observables. It refines the cosmology program thread by providing a reusable, measurable bridge between A8 outputs and CMB/LSS datasets.

## 5. Intellectual Merit and Procedure

(1) Importance: makes A8 claims testable on CMB/LSS.  
(2) Broader impacts: clarifies whether VDM can meet or exceed ΛCDM fits with fewer assumptions.  
(3) Approach: deterministic spectrum generator → Boltzmann interface → meter outputs with gates.

## 5.1 Experimental Setup and Diagnostics

- **Inputs:** A8 generator parameters (interface scale λ, hierarchy depth control, tilt parameters); cosmological background (Ω_b, Ω_c, H0, τ, etc.).  
- **Diagnostics:** FRW balance (dust) RMS ≤ 1e−6; internal consistency checks; CMB peak positions and heights within preregistered envelopes; lensing amplitude; ISW cross‑checks.  
- **Acceptance (gates):** (G1) FRW balance gate passes; (G2) fit quality meets preregistered Δχ²/ΔAIC envelope vs ΛCDM on Planck‑class spectra; (G3) null tests (isotropy/lensing consistency) pass.

### 5.1.1 Pre-Run Config Requirements

- Approvals manifest and schemas for spectrum JSON and solver configs.

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "EBN-CMB-ISW+Lens Pipeline (A8 to CMB/LSS)",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H_FRW", "statement": "Dust FRW continuity RMS ≤ 1e-6 for generated backgrounds.", "direction": "no-change" },
    { "id": "H_CMB", "statement": "CMB peak positions/heights fall within preregistered envelopes under A8 spectrum.", "direction": "no-change" },
    { "id": "H_LENS", "statement": "Lensing/ISW diagnostics match prereg envelopes without ad-hoc components.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["λ", "hierarchy parameters", "Ω_b", "Ω_c", "H0", "τ", "seeds"],
    "dependent": ["RMS_FRW", "Δχ²_vs_ΛCDM", "peak_offsets", "lensing_A"],
    "controls": ["masking", "ℓ_max", "beam/noise models"]
  },
  "pass_fail": [
    { "metric": "RMS_FRW", "operator": "<=", "threshold": 1e-6, "unit": "" },
    { "metric": "Δχ²_vs_ΛCDM", "operator": "<=", "threshold": 0.0, "unit": "" },
    { "metric": "peak_offsets", "operator": "<=", "threshold": 0.5, "unit": "σ" }
  ],
  "spec_refs": ["Derivation/code/cosmology/specs/ebn-cmb.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

## 5.2 Experimental runplan

A8→spectrum JSON→Boltzmann solver→CMB/LSS meters; AMD CPUs/ROCm where supported; artifacts (PNG+CSV+JSON) routed with commit and salted provenance. Failure emits CONTRADICTION_REPORT.
