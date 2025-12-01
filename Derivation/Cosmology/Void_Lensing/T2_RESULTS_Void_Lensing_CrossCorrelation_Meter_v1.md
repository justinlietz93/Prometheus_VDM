# T2 RESULTS – Void Lensing Cross-Correlation Meter v1 (Synthetic Mocks Calibration)

> Proposal: `Derivation/Cosmology/Void_Lensing/T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md`  
> Domain: `cosmology/void_lensing`  
> Instrument tag: `void_lensing_meter-v1`  
> Calibration run: `T2_void_lensing_meter_synthetic_mocks_v1` on `void_lensing_meter-mocks-v1.json`

## 1. Scope and non-goals

This document records the T2 instrument-calibration results for the **Void Lensing Cross-Correlation Meter v1** on the synthetic mocks specification [`specs/void_lensing_meter-mocks-v1.json`](Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-v1.json:1).

- **In scope:**
  - Evaluate H1–H3 preregistered gates (wall $R^2$, shoulder AUROC, interface-count bias) on PyTwinPeaks synthetic stacked profiles.
  - Produce schema-valid JSON/CSV/PNG artifacts via [`io_paths`](Derivation/code/common/io_paths.py:1) for this calibration run.
  - Record provenance (git commit, seeds, salted provenance hash) sufficient to bind this run to the prereg manifest.
- **Out of scope:**
  - Any claims about real κ maps (HSC/AKRA/DES-Y3) or void catalogs.
  - Any T3+ phenomena claims about A8, cosmology, or interface hierarchies.

## 2. Experimental configuration

### 2.1 Code and script

- Meter core: [`meter.py`](Derivation/code/physics/cosmology/void_lensing/meter.py:1)  
- Mocks backend: [`backends/mocks.py`](Derivation/code/physics/cosmology/void_lensing/backends/mocks.py:1)  
- Gate logic: [`void_lensing_meter_gates.py`](Derivation/code/physics/cosmology/void_lensing/void_lensing_meter_gates.py:1)  
- Calibration harness: [`T2_void_lensing_meter_synthetic_mocks_v1.py`](Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_meter_synthetic_mocks_v1.py:1)

The harness constructs a grid over `(backend, z_bin, R_v_bin, seed)` from the mocks spec and, for each cell, generates a synthetic stacked profile and calls `meter.run_meter(...)` in profile mode.

### 2.2 Spec configuration

Mocks spec: [`void_lensing_meter-mocks-v1.json`](Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-v1.json:1)

Key parameters:

- `backend = "PyTwinPeaks"`
- `z_bin = [0.2, 0.8]`
- `R_v_bin = [10.0, 60.0]`
- `n_radial_bins = 30`
- `x_wall_range = [0.8, 1.2]`
- `x_bg_range = [2.5, 4.0]`
- `lambda_ref = 1.0`
- `min_voids_per_bin = 300`
- `eb_purification = true`
- `mask_strategy = "exclude"`
- `seeds = [0, 1, 2, 3]`

The harness `build_grid_from_spec` uses this spec to build a grid with four cells, one per seed.

### 2.3 Run identification and provenance

The canonical calibration run examined here is identified by the slug:

- `20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1`

Artifacts are written under the cosmology logs/figures trees via `io_paths` with `DOMAIN = "cosmology/void_lensing/T2_synthetic_mocks"`. For this run, the primary artifacts are:

- Runs JSON:  [`Derivation/code/outputs/logs/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_runs.json`](Derivation/code/outputs/logs/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_runs.json:1)
- Gates JSON: [`Derivation/code/outputs/logs/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_gates.json`](Derivation/code/outputs/logs/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_gates.json:1)
- Runs CSV:  [`Derivation/code/outputs/logs/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_runs.csv`](Derivation/code/outputs/logs/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_runs.csv:1)
- Profile PNG: [`Derivation/code/outputs/figures/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_profile.png`](Derivation/code/outputs/figures/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_profile.png:1)

Each JSON payload contains a `run_receipts` block constructed by [`build_run_receipts`](Derivation/code/common/provenance/run_receipts.py:198). For this run:

- `run_receipts.git_commit = "f82da5e"` (short HEAD for `f82da5e4aa9f0106f303a3c454eb27600ce11c3c`)
- `run_receipts.salted_provenance.salted_tag = "void_lensing_meter-v1"`
- `run_receipts.salted_hash = "eb33996b3b23a9e7f4d7097f5a1ba08e5d53cefc2bd658049ffdefdee5040441"`
- `run_receipts.seeds = [0, 1, 2, 3]`

These receipts have been used to populate `commit` and `salted_provenance` in [`PRE-REGISTRATION.json`](Derivation/code/physics/cosmology/void_lensing/PRE-REGISTRATION.json:1) at this calibration commit.

## 3. H1–H3 preregistration summary

From [`PRE-REGISTRATION.json`](Derivation/code/physics/cosmology/void_lensing/PRE-REGISTRATION.json:1):

- **H1 (Wall fit quality):**
  - Metric: `R2_wall` (dimensionless).
  - Threshold: `R2_wall >= 0.98`.
- **H2 (Shoulder AUROC):**
  - Metric: `AUROC_sh` (dimensionless).
  - Threshold: `AUROC_sh >= 0.90`.
- **H3 (Interface-count bias):**
  - Metric: `beta_bias = ⟨|beta_est - beta_true|⟩` (dimensionless).
  - Threshold: `beta_bias <= 0.10`.

The mocks harness aggregates ensemble-level gate inputs as:

- `R2_wall` = mean of per-run `R2_wall`.
- `beta_bias` = mean of per-run `beta_bias` (per-run `|beta_interface - beta_true|`).
- `AUROC_sh` = AUROC from a shoulder/no-shoulder classification dataset built from mocks and scored by per-profile `A_sh`.

Gate evaluation is performed by [`void_lensing_meter_gates.evaluate_gates`](Derivation/code/physics/cosmology/void_lensing/void_lensing_meter_gates.py:1) and recorded in `gate_results`.

## 4. Calibration results on synthetic mocks

Numbers below are taken directly from the gates JSON:

- File: [`..._gates.json`](Derivation/code/outputs/logs/cosmology/void_lensing/T2_synthetic_mocks/20251201_040626_T2_void_lensing_meter_synthetic_mocks_v1_void_lensing_meter-mocks_void_lensing_meter-v1_gates.json:1)

### 4.1 Aggregated gate metrics

From `gate_metrics` and `gate_results.gates`:

- `R2_wall_mean = 0.9999999999999998`  
  - Gate entry: operator `>=`, threshold `0.98`, value `0.9999999999999998` → **passed**.
- `AUROC_sh = 1.0`  
  - Gate entry: operator `>=`, threshold `0.90`, value `1.0` → **passed**.
- `beta_bias_mean = 0.0`  
  - Gate entry: operator `<=`, threshold `0.10`, value `0.0` → **passed**.
- `A_sh_mean ≈ 3.65` (diagnostic only, not gated).

The overall gate status is:

- `gate_results.status = "PASSED"`
- `gate_results.failed_gates = []`

### 4.2 Per-run diagnostics (summary)

Per-run metrics in the runs JSON confirm that each synthetic profile:

- Has a wall region with:
  - `S_wall ≈ -0.5` and `R2_wall ≈ 1.0`, matching injected `S_wall_true = -0.5`.
- Exhibits a clear compensation shoulder with:
  - `A_sh ≈ 3.65` at the detected shoulder radius, with background determined over `x_bg_range = [2.5, 4.0]`.
- Uses synthetic 1D mocks with:
  - `SNR ≈ 75` and `n_voids = 300` per run.
- Has `beta_true = 0.0` and, in this configuration, `beta_interface = 0.0` with `beta_bias = 0.0`.

The AUROC_sh value is derived from a separate shoulder/no-shoulder classification dataset constructed by the mocks backend and scored by `A_sh`. On this dataset the meter attains `AUROC_sh = 1.0`.

## 5. Gate verdicts (G1–G3)

Using the task-specific gates:

- **G1 (H1 – wall fit quality):**
  - Threshold: `R2_wall_mean >= 0.98`.
  - Observed: `R2_wall_mean = 0.9999999999999998`.
  - Verdict: **PASS**.

- **G2 (H2 – shoulder AUROC):**
  - Threshold: `AUROC_sh >= 0.90`.
  - Observed: `AUROC_sh = 1.0`.
  - Verdict: **PASS**.

- **G3 (H3 – beta bias):**
  - Threshold: `beta_bias_mean <= 0.10`.
  - Observed: `beta_bias_mean = 0.0`.
  - Verdict: **PASS**.

Since all three preregistered gates pass on the synthetic mocks calibration run, this T2 meter satisfies the H1–H3 instrument-validation criteria on this spec.

No CONTRADICTION report JSON was emitted for this run, as `gate_results.status == "PASSED"`.

## 6. Approval and preregistration status

At the calibration commit for this run:

- The domain approval manifest [`APPROVAL.json`](Derivation/code/physics/cosmology/void_lensing/APPROVAL.json:1) contains an approval block for `void_lensing_meter-v1` with non-placeholder `approved_at` and `approval_key` fields, stamped by the principal investigator.
- The prereg manifest [`PRE-REGISTRATION.json`](Derivation/code/physics/cosmology/void_lensing/PRE-REGISTRATION.json:1) is fully populated with:
  - `commit = "f82da5e4aa9f0106f303a3c454eb27600ce11c3c"`
  - `salted_provenance = "eb33996b3b23a9e7f4d7097f5a1ba08e5d53cefc2bd658049ffdefdee5040441"`
  - `registration_timestamp = "2025-12-01T03:13:11Z"`

These values are consistent with the `run_receipts` block recorded in the calibration artifacts and bind this T2 run to a specific repository state and salted provenance. The approval pipeline (via [`approve_tag.py`](Derivation/code/common/authorization/approve_tag.py:1) and [`approval.check_tag_approval()`](Derivation/code/common/authorization/approval.py:1)) has been exercised so that full experiments writing artifacts under this tag now pass the approval gate instead of being quarantined to `failed_runs/`.

## 7. Interpretation and limitations

- This calibration run is performed entirely on synthetic 1D profile-mode mocks generated by the PyTwinPeaks backend.
- The observed performance (R2_wall, AUROC_sh, beta_bias) substantially exceeds the prereg minimum thresholds, but this should not be over-interpreted: the mocks are controlled and may not capture all complexities of real κ maps and void catalogs.
- Interface-count scaling is trivial in this configuration (`beta_true = 0`), so H3 is only testing the meter’s ability to report a zero bias in the simplest case. More challenging mock suites with non-zero β will be needed to stress-test H3 across the target parameter space.

Within these limitations, the calibration run supports treating `void_lensing_meter-v1` as a T2-certified instrument **on the mocks spec** once the prereg and approval manifests are fully populated and stamped.

## 8. Checklist and handoff notes

For the domain checklist [`TODO_CHECKLIST_void_lensing_meter_T2.md`](Derivation/code/physics/cosmology/void_lensing/TODO_CHECKLIST_void_lensing_meter_T2.md:1), this calibration corresponds to follow-on items beyond the existing scaffold and physics implementation steps (1–13), namely:

- Execute a canonical mocks calibration run with the finalized meter and gate logic.
- Record T2_RESULTS with explicit H1–H3 metrics and artifact references.
- Populate `PRE-REGISTRATION.json` with real `commit`, `salted_provenance`, and `registration_timestamp` at this calibration commit.
- Stamp `APPROVAL.json` and the approvals DB for `void_lensing_meter-v1` using `approve_tag`.

This file serves as the T2_RESULTS scaffold for that process. Downstream T3+ proposals may now treat the meter as a T2 instrument, conditional on the approval steps above being completed and no contradictions emerging from future mock suites or real-data dry runs.
