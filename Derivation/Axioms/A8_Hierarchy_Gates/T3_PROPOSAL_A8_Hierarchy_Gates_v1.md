# T3 (Smoke) - A8 Two‑Gate Hierarchy Test (N(L)~log L & E_exc~L^{d-1})

> Created Date:  2025-11-18  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {salted_hash}  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI).

## 3. Abstract

Proposed in this document is a preregistered **Two‑Gate Test** of the A8 hierarchy claim: (P1) logarithmic interface depth $N(L)\sim \log(L/\lambda)$ and (P2) boundary‑law excess energy $E_{\mathrm{exc}}(L)\propto L^{d-1}$. Both must pass jointly. The instrument defines detectors, regressions, and null‑model comparisons (AIC/BIC) and publishes artifacts per gate discipline.

## 4. Background & Scientific Rationale

A8’s geometric necessity links tachyonic genesis to hierarchy. Testing both N(L) and energy‑law together distinguishes VDM from scale‑free fractal nulls that can mimic one metric alone.

## 5. Intellectual Merit and Procedure

(1) Importance: decisive geometry signature; (2) Impacts: constrains ΛCDM‑style descriptive models; (3) Approach: predeclared detectors, bootstrap CIs, and null comparisons.

## 5.1 Experimental Setup and Diagnostics

- **Detectors:** interface counters and energy aggregators with threshold sweeps; report detector‑sensitivity scans.  
- **Fits:** (i) depth vs log L (slope near 1), (ii) log E_exc vs log L (slope α ≈ d−1).  
- **Acceptance (joint):** slope_N within [0.9, 1.1] **and** |α − (d−1)| ≤ 0.1 with R² ≥ 0.98; AIC/BIC prefer boundary‑law over volume‑law nulls.

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "A8 Two-Gate Hierarchy Test",
  "tier_grade": "T3",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H_N", "statement": "N(L) grows logarithmically with L.", "direction": "increase" },
    { "id": "H_E", "statement": "E_exc scales as L^{d-1}.", "direction": "increase" }
  ],
  "variables": {
    "independent": ["L", "detector thresholds", "dimension d", "seeds"],
    "dependent": ["slope_N", "α_energy", "R2", "ΔAIC", "ΔBIC"],
    "controls": ["masking", "binning", "finite-size correction"]
  },
  "pass_fail": [
    { "metric": "slope_N", "operator": "between", "threshold": [0.9, 1.1], "unit": "" },
    { "metric": "α_energy", "operator": "between", "threshold": ["d-1-0.1", "d-1+0.1"], "unit": "" },
    { "metric": "R2", "operator": ">=", "threshold": 0.98, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/hierarchy/specs/a8-two-gate.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

## 5.2 Experimental runplan

Multi‑L domains and seeds; publish slopes, CIs, and model‑selection stats; failure emits CONTRADICTION_REPORT with detector sensitivity scan.
