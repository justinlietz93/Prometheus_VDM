# T2 (Instrument) - Metriplectic Instruments: Identity, KG, RD, and FRW Meters (EBN series)

> Created Date:  2025-11-18  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {salted_hash}  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI), Neuroca (compute & instrumentation).

## 3. Abstract

Proposed in this document is the meter suite that turns VDM derivations into machine‑auditable numbers: (i) **KG J‑only dispersion/locality meter**, (ii) **RD meter** (front‑speed & dispersion), (iii) **Metriplectic identity meter** (degeneracy and Lyapunov monotonicity), and (iv) **FRW continuity meter**. Each meter has fixed acceptance gates; runs emit PNG+CSV+JSON artifacts with provenance. This proposal formalizes the meters as reusable T2 instruments.

## 4. Background & Scientific Rationale

Meters operationalize Axiom A4 and A2 claims and gate numerics (discretization = instrument). Prior QC runs for KG, FRW, and metriplectic structure motivate consolidation into a single T2 package.

## 5. Intellectual Merit and Procedure

(1) Importance: establishes standardized instruments for all downstream T3–T7 phenomena.  
(2) Broader impacts: reproducible physics meters with explicit gates.  
(3) Approach: deterministic seeds, double precision, artifact routing, AMD ROCm where applicable.

## 5.1 Experimental Setup and Diagnostics

**KG J‑only meter.** Inputs: grid N, Δt, c, m, seeds. Diagnostics: dispersion fit (ω² vs k²), cone slope v. **Gates:** v ≤ c·(1+0.02); dispersion fit R² ≥ 0.999; Noether drifts ≤ 1e−12.  
**RD meter.** Inputs: D, r, λ (optional); measure c_front and σ(k). **Gates:** |c_obs/(2√(Dr))−1| ≤ 0.05 with R² ≥ 0.98; dispersion median rel‑err ≤ 1e−2.  
**Identity (metriplectic) meter.** Diagnostics: ΔL_h ≤ 0 per step; identity residuals ≤ 1e−12; two‑grid slope ≥ 2.90.  
**FRW meter.** Diagnostics: RMS continuity residual ≤ 1e−6 (dust).

### 5.1.1 Pre-Run Config Requirements

- Approvals manifest per domain; schemas & specs per meter tag.

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "Metriplectic Instruments: KG, RD, Identity, FRW",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H_KG", "statement": "Light-cone speed v is bounded by c within 2% under J-only dynamics.", "direction": "no-change" },
    { "id": "H_RD", "statement": "Front speed equals 2*sqrt(D*r) within 5%.", "direction": "no-change" },
    { "id": "H_ID", "statement": "Discrete Lyapunov decreases monotonically for M-step; degeneracy identities hold to 1e-12.", "direction": "no-change" },
    { "id": "H_FRW", "statement": "FRW continuity residual RMS ≤ 1e-6.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["N", "Δt", "c", "m", "D", "r", "λ", "seeds"],
    "dependent": ["v/c", "R2_disp", "rel_err_front", "ΔL_h", "RMS_FRW"],
    "controls": ["CFL", "BCs", "precision"]
  },
  "pass_fail": [
    { "metric": "v/c", "operator": "<=", "threshold": 1.02, "unit": "" },
    { "metric": "R2_disp", "operator": ">=", "threshold": 0.999, "unit": "" },
    { "metric": "rel_err_front", "operator": "<=", "threshold": 0.05, "unit": "" },
    { "metric": "ΔL_h", "operator": "<=", "threshold": 0.0, "unit": "" },
    { "metric": "RMS_FRW", "operator": "<=", "threshold": 1e-6, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/physics/meters/specs/meters-ebn.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

## 5.2 Experimental runplan

Cartesian products for each meter; AMD ROCm (if GPU) with double precision. Success: publish RESULTS_* with figure+CSV+JSON; failure: CONTRADICTION_REPORT with seeds, commit, thresholds.
