# 1. T5 (Pilot) — Gravity Regression — Weak‑Field VDM vs SPARC/Lensing Suites

> Created Date:  2025-11-18
> Commit: 5581b2050f15ea05ac6f81b3905c646c3d4dd239
> Salted provenance: {salted_hash}
> Proposer contact(s):  (<justin@neuroca.ai>)
> License: See LICENSE
> Short summary (one sentence TL;DR):  T5 pilot gravity‑regression pack comparing weak‑field VDM against SPARC rotation curves and lensing suites using preregistered datasets, $\Delta\mathrm{AIC}$/$\Delta\mathrm{BIC}$ and $\Delta\ln Z$–based model selection, under locality/LIV gates.

## 2. List of proposers and associated institutions/companies

Justin K. Lietz (PI).

## 3. Abstract

Proposed in this document is a preregistered **regression pack** that confronts VDM weak‑field predictions with standard galaxy rotation curves (SPARC) and strong/weak lensing cases. The meter uses standardized likelihoods, cross‑validation, and model selection (AIC/BIC, Bayes factors) to test whether VDM matches or exceeds ΛCDM baselines without violating locality/Lorentz gates.

## 4. Background & Scientific Rationale

VDM posits emergent gravity signatures from its field structure. A unified, reproducible regression pack is needed to test claims against public benchmark datasets using the same meters and gates.

## 5. Intellectual Merit and Procedure

(1) Importance: clamps gravitational phenomenology; (2) Impacts: either supports or falsifies VDM gravity without ad‑hoc species; (3) Approach: visibility‑plane lensing meters and rotation‑curve fits under shared discipline.

## 5.1 Experimental Setup and Diagnostics

- **Inputs:** curated SPARC galaxy subset (rotation curves with quality flags), preregistered strong‑ and weak‑lensing targets, and priors on nuisance parameters (distance, inclination, PSF/beam, mass‑to‑light ratios).
- **Diagnostics:** hold‑out predictive performance (oos_RMSE), residual structure diagnostics, $\Delta\mathrm{AIC}$/$\Delta\mathrm{BIC}$ vs. $\Lambda$ CDM/MOND baselines, $\Delta\ln Z$ (Bayes factors), and null predictions respected (e.g., no LIV or pathological potentials).
- **Acceptance (gates):** (G1) $\Delta\mathrm{AIC} \le 0$ vs. $\Lambda$CDM on preregistered rotation‑curve sets (tie/beat); (G2) decisive evidence on at least one lensing case ($\Delta\ln Z \ge +5$); (G3) no locality/LIV gate violations from core meters (using FRW and metriplectic meters in [`T2_PROPOSAL_Metriplectic_Instruments_v1.md`](Derivation/Metriplectic/Metriplectic_Instruments/T2_PROPOSAL_Metriplectic_Instruments_v1.md)).

### 5.1.1 Pre-Run Config Requirements

- **Approvals:**
  - `Derivation/code/physics/gravity_regression/APPROVAL.json` — gravity-regression approval manifest mapping allowed tags to schemas and this proposal path; must be present and approved before any artifact-writing runs.
- **Pre-registration manifest:**
  - `Derivation/code/physics/gravity_regression/PRE-REGISTRATION.json` — preregistration manifest including proposal title, tier grade, commit, salted provenance, hypotheses, variables, pass/fail metrics, and spec references for gravity-regression runs.
- **Schemas:**
  - `Derivation/code/physics/gravity_regression/schemas/gravity-regression.v1.schema.json` — JSON Schema for run specs and summary logs, including fields for orbit logs and connectome metrics as defined in [`00_DATA_PRODUCTS.md`](Derivation/z.CANONICAL_Data_Products/00_DATA_PRODUCTS.md:1250).
- **Specs:**
  - `Derivation/code/physics/gravity_regression/specs/gravity-regression.v1.json` — run-spec files referenced in `spec_refs` below; define dataset selections, model families, prior choices, hyperparameters, and seeds.
- **Data products:**
  - Orbit-log and connectome-metric outputs must conform to the canonical `gravity_regression orbit logs` and `gravity_regression connectome metrics` entries in [`00_DATA_PRODUCTS.md`](Derivation/z.CANONICAL_Data_Products/00_DATA_PRODUCTS.md:1250).

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
  "spec_refs": ["Derivation/code/physics/gravity_regression/specs/gravity-regression.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

### Minimal spec example (gravity-regression.v1)

The file `Derivation/code/physics/gravity_regression/specs/gravity-regression.v1.json` must contain at least one spec entry of the following shape (keys aligned with §5.1 and the PRE-REG `variables` block):

```json
{
  "run_name": "gravity-regression-baseline",
  "version": "1.0.0",
  "tag": "gravity-regression.v1",
  "schema_ref": "Derivation/code/physics/gravity_regression/schemas/gravity-regression.v1.schema.json",
  "parameters": {
    "rotation_curve_dataset": "sparc-baseline-v1",
    "lensing_dataset": "b1938+666-pinch-v1",
    "model_families": ["vdm-weakfield", "lcdm", "mond"],
    "fit_hyperparameters": {
      "optimizer": "adam",
      "learning_rate": 0.01,
      "max_steps": 10000
    },
    "priors": {
      "distance": "gaussian:mu=0,sigma=1",
      "inclination": "uniform:0-90",
      "mlr": "lognormal:mu=0,sigma=0.3"
    },
    "masking": "default",
    "psf_beam": "instrument-default",
    "distance_priors": "catalog-default"
  },
  "seeds": [0, 1, 2]
}
```

This is a **minimal illustrative spec**, not a canonical choice of datasets or priors. Actual production specs:

- Must use dataset identifiers and nuisance priors consistent with the gravity-regression pack and `00_DATA_PRODUCTS.md`.
- May include additional fields (e.g., cross-validation fold definitions, likelihood variants) as long as they remain compatible with `gravity-regression.v1.schema.json`.
- Must be validated by `gravity-regression.v1.schema.json` and the gravity_regression `APPROVAL.json` gate before any artifact-writing runs.

## 5.2 Experimental runplan

1. **Dataset registry and specs.** Build a registry of SPARC galaxies and lensing systems with quality flags and data sources; write preregistered spec files (`gravity-regression.v1.json`) enumerating datasets, model families, priors, and seeds.
2. **Instrument QC (pack-level).** Use the `vdm_gravity_regression_pack` orbit and graph scripts to validate meters on synthetic and calibration cases, emitting orbit logs and connectome metrics per the `gravity_regression` data-product definitions.
3. **Rotation-curve fits.** For each SPARC system, fit VDM vs ΛCDM/MOND baselines under identical likelihoods and priors; compute ΔAIC/ΔBIC and out-of-sample RMSE via cross-validation splits; log metrics to JSON/CSV.
4. **Lensing fits.** For each preregistered lensing system, run the gravity-regression CLI with VDM and baseline models using the prereg specs; compute ΔlnZ and inspect residual structure and null predictions (e.g., no LIV).
5. **Aggregation and gates.** Aggregate metrics across samples; apply the PRE-REG pass/fail rules (ΔAIC, ΔlnZ, and any additional KPIs registered in the schema); on PASS, publish RESULTS_* with numbered figures and artifacts (PNG+CSV+JSON via `io_paths`); on FAIL, route all artifacts to `failed_runs/` with a CONTRADICTION_REPORT capturing datasets, seeds, and violating metrics.

## 6. Personnel

Justin K. Lietz will design and maintain the gravity-regression pack, select datasets and priors, and interpret model-comparison diagnostics under the weak-field emergent-gravity program. Neuroca provides computational infrastructure, CI integration, and code review to ensure that the implementation matches this proposal, the tier standards, and the validation metrics.

## 7. References

- [`Derivation/Gravity_Regression/vdm_gravity_regression_pack/README.md`](Derivation/Gravity_Regression/vdm_gravity_regression_pack/README.md) — gravity-regression pack description, CLI patterns, and internal module layout.
- [`Derivation/Unification/T0_Unification_Program_Spec_v1.md`](Derivation/Unification/T0_Unification_Program_Spec_v1.md:535) — weak-field gravity program (M5) and its link to gravity-regression meters and gates.
- [`Derivation/Gravity/B1938+666_Pinch_Visibility-Plane_Lensing/T4_PROPOSAL_NFW_for_the_B1938+666_Pinch_v1.md`](Derivation/Gravity/B1938+666_Pinch_Visibility-Plane_Lensing/T4_PROPOSAL_NFW_for_the_B1938+666_Pinch_v1.md) — preregistered NFW vs VDM lensing comparison whose meters and datasets this pack will reuse and extend.
- [`Derivation/z.CANONICAL_Data_Products/00_DATA_PRODUCTS.md`](Derivation/z.CANONICAL_Data_Products/00_DATA_PRODUCTS.md:1250) — canonical definitions for `gravity_regression orbit logs` and `gravity_regression connectome metrics`.
- [`Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md`](Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md) — global KPIs and meter gates (FRW, causality, metriplectic identity) that constrain model choices and numerical implementations.
