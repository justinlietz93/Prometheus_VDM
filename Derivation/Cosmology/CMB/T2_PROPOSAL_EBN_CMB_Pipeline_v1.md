# 1. T2 (Instrument) — EBN‑CMB‑ISW+Lens Pipeline (A8→Boltzmann→CMB/LSS)

> Created Date:  2025-11-18
> Commit: bc12095fea0e0add986fe5469585da0287da5104
> Salted provenance: {salted_hash}
> Proposer contact(s):  (<justin@neuroca.ai>)
> License: See LICENSE
> Short summary (one sentence TL;DR):  T2 instrument wiring A8 hierarchy outputs into a reproducible Boltzmann pipeline that produces CMB/LSS observables under FRW balance gates and $\Delta\chi^2$ fit‑quality envelopes against $\Lambda$CDM.

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

This section answers the canonical 5.1 questions for the EBN‑CMB‑ISW+Lens pipeline.

### 5.1.a Known, required parameters (keys and units)

The **EBN‑CMB runner** (tag `ebn-cmb.v1`) is parameterized by:

- **A8 generator parameters**
  - $\lambda$ — interface scale (comoving length; see [`00_UNITS_NORMALIZATION.md`](Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md:1)).
  - `hierarchy parameters` — dimensionless parameters controlling A8 hierarchy depth, tilt, and spectrum shape (referenced by key in the spec and defined in the A8 generator domain).
- **Cosmological background**
  - $\Omega_b$ — baryon density parameter (dimensionless).
  - $\Omega_c$ — cold dark matter density parameter (dimensionless).
  - $H_0$ — Hubble parameter at $z=0$ [km/s/Mpc or normalized units].
  - $\tau$ — optical depth to reionization (dimensionless).
  - Additional standard background parameters as required by the Boltzmann solver (e.g., $\Omega_\Lambda$, $n_s$).
- **Numerical and analysis controls**
  - `ℓ_max` — maximum multipole included in the analysis.
  - `masking` — mask choice/label for sky cuts (if applicable).
  - `beam/noise models` — identifiers or parameters for beam transfer functions and noise models.
  - `seeds` — integer RNG seeds for A8 spectrum generation and synthetic simulations.

These parameters are declared in `Derivation/code/cosmology/specs/ebn-cmb.v1.json` with units and default values documented and enforced via the schema in §5.1.1.

### 5.1.b Diagnostics needed (list and count) and how they are measured

- **Inputs (summary):**
  - A8 generator parameters (interface scale $\lambda$, hierarchy depth control, tilt parameters).
  - Cosmological background $(\Omega_b,\Omega_c,H_0,\tau,\dots)$.
- **Diagnostics:**
  - FRW balance (dust) RMS $\le 10^{-6}$ for generated backgrounds.
  - Internal consistency checks of the EBN→Boltzmann mapping (e.g., energy conservation and normalization).
  - CMB peak positions and heights within preregistered envelopes relative to $\Lambda$CDM.
  - Lensing amplitude diagnostics (e.g., $A_L$‑like parameters).
  - ISW cross‑checks (e.g., correlation with large‑scale structure tracers, where applicable).
- **Minimum diagnostic artifacts per spec:**
  - 1 PNG: CMB TT/TE/EE spectra with residuals vs. $\Lambda$CDM and FRW residual plots.
  - 1 CSV: tabulated outputs (multipole $\ell$, $C_\ell$, residuals, fit metrics).
  - 1 JSON: run log with FRW metrics (RMS residual), $\Delta\chi^2$ vs. $\Lambda$CDM, peak offset diagnostics, lensing amplitude metrics, and gate verdicts.

### 5.1.c Other equipment and new tools/scripts

- **Unplanned equipment (hardware):**
  - Standard Linux compute nodes (CPU and/or GPU) capable of running the chosen Boltzmann code (e.g., CLASS/CAMB) and the A8 generator.
  - No special physical instrumentation is required beyond compute resources; if external data access (Planck/DES/etc.) requires particular storage or access policies, these are documented at the domain level rather than here.

- **New software/tools required (paths):**
  - Spectrum generator and pipeline harness:
    - `Derivation/code/physics/cosmology/ebn_cmb_pipeline.py` (or equivalent runner, to be implemented to match this proposal).
  - Specs and schemas:
    - `Derivation/code/cosmology/specs/ebn-cmb.v1.json` — defines parameter grids, seeds, and tags.
    - `Derivation/code/cosmology/schemas/ebn-cmb.schema.json` — JSON Schema for spectrum JSON, Boltzmann configuration, and meter outputs.
  - Preflight tests:
    - `Derivation/code/tests/cosmology/` — preflight runners to validate FRW QC and pipeline wiring without writing artifacts.

### 5.1.d Required parameters and defaults (list keys and units)

At minimum, each spec entry for `ebn-cmb.v1` must provide:

- `lambda` (float; interface scale; comoving length).
- `hierarchy_params` (object; domain‑specific keys controlling A8 hierarchy).
- `Omega_b`, `Omega_c`, `H0`, `tau` (floats; standard cosmological parameters).
- `ell_max` (int; maximum multipole).
- `masking` (string; mask identifier).
- `beam_model`, `noise_model` (strings or structured objects referencing beam/noise definitions).
- `seeds` (array[int]; one or more RNG seeds).

Defaults and allowed ranges are defined in `ebn-cmb.v1.json` and enforced by `ebn-cmb.schema.json`.

- **Acceptance (gates):**
  - (G1) FRW balance gate passes (dust FRW continuity RMS $\le 10^{-6}$ for generated backgrounds).
  - (G2) Fit quality meets preregistered $\Delta\chi^2$/$\Delta\mathrm{AIC}$ envelope vs. $\Lambda$CDM on Planck‑class spectra.
  - (G3) Null tests (isotropy/lensing consistency) pass.

### 5.1.1 Pre-Run Config Requirements

- **Required config and metadata (cosmology domain):**
  - `Derivation/code/physics/cosmology/APPROVAL.json`
  - `Derivation/code/physics/cosmology/schemas/ebn-cmb.schema.json`
  - `Derivation/code/physics/cosmology/specs/ebn-cmb.v1.json`

These files encode the approval policy, preregistration manifest, schemas, and run specs for EBN‑CMB runs.

#### APPROVALS.json

The approvals manifest at `Derivation/code/physics/cosmology/APPROVAL.json` must, at minimum, follow this pattern (values may be extended as needed):

```json
{
  "preflight_name": "ebn-cmb-preflight",
  "description": "Approval manifest stating that the EBN-CMB preflight runner must pass before real runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real EBN-CMB experiments that write artifacts, this T2_PROPOSAL_EBN_CMB_Pipeline_v1.md must be reviewed and approved."
},
{
  "pre_registered": true,
  "proposal": "Derivation/Cosmology/CMB/T2_PROPOSAL_EBN_CMB_Pipeline_v1.md",
  "allowed_tags": [
    "ebn-cmb.v1"
  ],
  "schema_dir": "Derivation/code/physics/cosmology/schemas",
  "approvals": {
    "ebn-cmb.v1": {
      "schema": "Derivation/code/physics/cosmology/schemas/ebn-cmb.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto generated timestamp",
      "approval_key": "auto generated hashed key"
    }
  }
}
```

- **Approvals manifest:** `Derivation/code/physics/cosmology/APPROVAL.json` — enforces preregistration and approval before cosmology runs that write artifacts; see authorization policy in [`Derivation/code/common/authorization/README.md`](Derivation/code/common/authorization/README.md:1).
- **Pre-registration manifest:** `Derivation/code/physics/cosmology/PRE-REGISTRATION.json` — records proposal title, tier grade, commit, salted provenance, hypotheses, variables, gates, and spec references for this EBN‑CMB pipeline.
- **Schemas:** `Derivation/code/physics/cosmology/schemas/ebn-cmb.schema.json` — JSON Schema for spectrum JSON, Boltzmann solver configuration, and meter outputs.
- **Specs:** `Derivation/code/physics/cosmology/specs/ebn-cmb.v1.json` — run‑spec files referenced in `spec_refs`; each spec defines parameters, seeds, and tags for A8→spectrum→Boltzmann→CMB/LSS runs.

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

### Minimal spec example (ebn-cmb.v1)

The file `Derivation/code/physics/cosmology/specs/ebn-cmb.v1.json` must contain at least one spec entry of the following shape (keys and units as in §5.1.a–d):

```json
{
  "run_name": "ebn-cmb-baseline",
  "version": "1.0.0",
  "tag": "ebn-cmb.v1",
  "schema_ref": "Derivation/code/physics/cosmology/schemas/ebn-cmb.schema.json",
  "parameters": {
    "lambda": 80.0,
    "hierarchy_params": {
      "depth": 3,
      "tilt": 0.03
    },
    "Omega_b": 0.049,
    "Omega_c": 0.262,
    "H0": 67.4,
    "tau": 0.054,
    "ell_max": 2500,
    "masking": "planck-common-v1",
    "beam_model": "planck-hm-v1",
    "noise_model": "planck-hm-v1"
  },
  "seeds": [1, 2, 3]
}
```

This is a **minimal illustrative example**, not a canonical choice of cosmological parameters. Actual production specs:

- Must use units consistent with [`00_UNITS_NORMALIZATION.md`](Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md:1) and cosmology‑domain units conventions.
- May include additional keys (e.g., dataset identifiers, likelihood options, nuisance parameters) as long as they remain compatible with `ebn-cmb.schema.json`.
- Must be validated by `ebn-cmb.schema.json` and the cosmology `APPROVAL.json` gate before any artifact‑writing runs.

## 5.2 Experimental runplan

This section describes how the resources in §5.1 are employed to answer the scientific questions, along with runtime estimates and success/failure actions.

1. **Spectrum generation and FRW QC (A8→FRW).**
   - For each spec entry, generate a primordial spectrum from the A8 hierarchy model using the parameters $(\lambda,\text{hierarchy parameters})$.
   - Construct the corresponding FRW background $(\Omega_b,\Omega_c,H_0,\tau,\dots)$ and run the FRW continuity meter on the background.
   - Gate on FRW RMS residuals $\le 10^{-6}$; any failures are logged and treated as preflight failures.

2. **Boltzmann propagation (FRW→CMB/LSS).**
   - Feed the A8 spectrum and FRW background into the Boltzmann solver (CLASS/CAMB or equivalent).
   - Compute CMB TT/TE/EE spectra, lensing spectra, and ISW observables as specified in the spec.

3. **CMB/LSS diagnostics and gating.**
   - Compute:
     - $\Delta\chi^2_{\text{vs}\,\Lambda\text{CDM}}$ and $\Delta\mathrm{AIC}$ relative to a reference $\Lambda$CDM model.
     - Peak positions/heights and `peak_offsets` metrics.
     - Lensing amplitude diagnostics (`lensing_A`) and, where applicable, ISW cross‑checks.
   - Apply acceptance gates:
     - FRW RMS: $\text{RMS}_{\text{FRW}} \le 10^{-6}$.
     - Fit envelope: $\Delta\chi^2_{\text{vs}\,\Lambda\text{CDM}} \le 0$ (or stricter envelope as declared).
     - Peak and lensing metrics within preregistered bands defined in the spec/schema.

4. **Cartesian product of independent variables and runtime estimate.**
   - Specs enumerate a Cartesian product over:
     - $(\lambda,\text{hierarchy parameters})$, $(\Omega_b,\Omega_c,H_0,\tau)$, `ℓ_max`, `masking`, `beam/noise models`, and `seeds`.
   - For each combination, the pipeline A8→spectrum JSON→Boltzmann solver→CMB/LSS meters is executed.
   - Estimated runtime:
     - Per configuration: order of minutes on a modern CPU or GPU (dominated by Boltzmann solves).
     - Total compute budget: a few GPU‑hours or $\lesssim\mathcal{O}(10^2)$ CPU‑hours, depending on the size of the Cartesian product; exact counts are encoded in the specs and summarized in JSON logs.

5. **Success plan.**
   - On PASS (all gates for a given tag satisfied):
     - Emit a RESULTS document (e.g., `T2_RESULTS_EBN_CMB_Pipeline_v1.md`) with:
       - Numbered figures (PNG) showing spectra, residuals, FRW QC, and lensing/ISW metrics.
       - CSV tables of $(\ell,C_\ell,\text{residuals})$ and FRW residuals.
       - JSON logs containing all metrics, spec references, and gate outcomes.
     - Tag the commit with a signed preregistration tag referencing the proposal path, specs, and salted provenance.

6. **Failure plan.**
   - On FAIL (any gate violated for a tag):
     - Route artifacts via `io_paths.py` to a `failed_runs/` subdirectory in the cosmology domain.
     - Emit a CONTRADICTION_REPORT JSON summarizing:
       - Which metrics (FRW RMS, $\Delta\chi^2$, `peak_offsets`, `lensing_A`) violated thresholds.
       - The spec entries and seeds associated with the failures.
     - No T2 certification or tier escalation is claimed for that configuration/tag until a revised proposal and rerun pass.

This runplan fulfills the template’s 5.2 requirements: it specifies the Cartesian product, approximate runtime and compute budget, and clear success/failure and publication actions consistent with [`RESULTS_PAPER_STANDARDS.md`](Derivation/Templates/RESULTS_PAPER_STANDARDS.md:1).

## 6. Personnel

Justin K. Lietz will design the A8→CMB/LSS pipeline, implement and review the spectrum generator and Boltzmann interfaces, and interpret diagnostics under the cosmology and A8 programs. Neuroca provides computational infrastructure, CI integration, and code review to ensure that implementations match this proposal, the tier standards, and the validation metrics.

## 7. References

- `Derivation/Unification/T0_Unification_Program_Spec_v1.md` — cosmology pipeline and meter program (L7; FRW, CMB/LSS, and hierarchy cross‑gates).
- `Derivation/Axioms/T8-A8_Milestones.md` and `Derivation/Axioms/T8-A8_Gaps.md` — A8 hierarchy milestones and literature‑backed gaps for EBN‑CMB‑ISW+Lens and EBN‑Analog‑Horizon.
- `Derivation/Cosmology/PROPOSAL_FRW_Balance_v1.md` — FRW continuity balance proposal defining the RMS gate used here as a precheck.
- `Derivation/Cosmology/RESULTS_FRW_Continuity_Residual_Quality_Check.md` — FRW Residual T4 results.
- `Derivation/Cosmology/CMB/T3_PROPOSAL_CMB_Hemispherical_Asymmetry_Test_v1.md` and `Derivation/Cosmology/T4_PROPOSAL_Single_Axis_Portal_Modulation_Against_CMB_Power_Tensor_v1.md` — prior CMB proposals that share cosmology meters, masks, and anomaly posture with this pipeline.
- `Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md` — FRW continuity RMS residual, ΛCDM residual, and other KPIs referenced as acceptance gates in this proposal.
