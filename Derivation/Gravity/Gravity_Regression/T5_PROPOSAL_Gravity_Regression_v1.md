# T5 (Pilot) - Gravity Regression — Weak‑Field VDM vs SPARC/Lensing Suites

> Created Date:  2025-11-18  
> Commit: 5581b2050f15ea05ac6f81b3905c646c3d4dd239  
> Salted provenance: {salted_hash}  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI).

## 3. Abstract

Proposed in this document is a preregistered **regression pack** that confronts VDM weak‑field predictions with standard galaxy rotation curves (SPARC) and strong/weak lensing cases. The meter uses standardized likelihoods, cross‑validation, and model selection (AIC/BIC, Bayes factors) to test whether VDM matches or exceeds ΛCDM baselines without violating locality/Lorentz gates.

## 4. Background & Scientific Rationale

VDM posits emergent gravity signatures from its field structure. A unified, reproducible regression pack is needed to test claims against public benchmark datasets using the same meters and gates.

## 5. Intellectual Merit and Procedure

(1) Importance: clamps gravitational phenomenology; (2) Impacts: either supports or falsifies VDM gravity without ad‑hoc species; (3) Approach: visibility‑plane lensing meters and rotation‑curve fits under shared discipline.

## 5.1 Experimental Setup and Diagnostics

- **Inputs:** curated SPARC subset; preregistered lensing targets; priors on nuisance parameters.  
- **Diagnostics:** hold‑out predictive performance; residual structure; ΔAIC/ΔBIC; ΔlnZ; null predictions respected.  
- **Acceptance (gates):** (G1) ΔAIC ≤ 0 vs ΛCDM on prereg sets (tie/beat); (G2) decisive evidence on at least one lensing case (ΔlnZ ≥ +5); (G3) no locality/LIV gate violations from core meters.

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "Gravity Regression — Weak-Field VDM vs Baselines",
  "tier_grade": "T5",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H_RC", "statement": "VDM rotation-curve fits meet or beat ΛCDM (ΔAIC ≤ 0).", "direction": "decrease" },
    { "id": "H_LENS", "statement": "At least one lensing case shows ΔlnZ ≥ +5 for VDM.", "direction": "increase" }
  ],
  "variables": {
    "independent": ["galaxy id", "lensing system id", "fit hyperparameters", "priors"],
    "dependent": ["ΔAIC", "ΔBIC", "ΔlnZ", "oos_RMSE"],
    "controls": ["masking", "PSF/beam", "distance priors"]
  },
  "pass_fail": [
    { "metric": "ΔAIC", "operator": "<=", "threshold": 0.0, "unit": "" },
    { "metric": "ΔlnZ", "operator": ">=", "threshold": 5.0, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/gravity/specs/gravity-regression.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

## 5.2 Experimental runplan

Define dataset registry → prereg configs → fit suites with CV → publish RESULTS with numeric captions and artifacts; failure triggers CONTRADICTION_REPORT with dataset seeds and diagnostics.
