# Cosmology / Void Lensing – T2 Void Lensing Cross-Correlation Meter v1 (Scaffold)

This directory hosts the **T2 (Instrument) – Void Lensing Cross-Correlation Meter v1** scaffold for the cosmology/void_lensing domain.  
At this stage, it contains **only** the experiment skeleton: file layout, APIs, JSON manifests, and gate stubs. No production physics logic or artifact-writing runs are implemented here yet.

The governing scientific contract is the proposal:

- `Derivation/Cosmology/Void_Lensing/T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md`

and all meters follow the policies and metrics declared in:

- `Derivation/Unification/T0_Unification_Program_Spec_v1.md`
- `Derivation/code/common/authorization/README.md`
- `Derivation/code/common/domain_setup/README.md`
- `Derivation/code/common/io_paths.py`

## 1. Scope and non-goals (scaffold-only phase)

**Scope in this phase**

- Define the **file layout** and public APIs for the void-lensing meter.
- Provide **runner**, **meter**, **backend**, and **validation-gate** **stubs** that import cleanly.
- Create `APPROVAL.json`, `PRE-REGISTRATION.json`, **spec JSONs**, and an **output schema JSON** that match the proposal.
- Add minimal tests that:
  - Import the runner, meter, and gate modules.
  - Load a spec JSON.
  - Exercise a dry-run CLI path without touching real κ maps or void catalogs.

**Out of scope in this phase**

- Implementing wall/shoulder/interface physics, stacking, or real diagnostics.
- Ingesting any real κ maps or void catalogs (AKRA, DES-Y3, mocks, etc.).
- Running any T2 experiments or emitting PNG/CSV/JSON artifacts.

All heavy numerics and physics logic will be added only after approval, in later sessions, and must respect the preregistration and meter contracts.

## 2. Planned Python modules

The following Python modules are planned for this directory (paths are relative to `Derivation/code/physics/cosmology/void_lensing/`):

- **Runner (T2 instrument entry point)**  
  - `T2_void_lensing_meter_v1.py`  
    - Purpose: CLI and orchestration only.
    - Responsibilities in scaffold:
      - Parse CLI arguments (`--spec`, `--dry-run`).
      - Load a spec JSON into an in-memory `config` object.
      - Call a thin orchestration layer that:
        - Selects a backend (stub).
        - Calls `meter.run_meter(...)` with placeholder inputs.
        - Passes the returned `metrics` dict into gate-evaluation stubs.
      - Wire in provenance and approvals via:
        - `common.io_paths` (for eventual artifact routing).
        - `common.authorization` (for future approval checks).
      - **No physics, no artifact writes** in this phase.

- **Meter core (instrument API)**  
  - `meter.py`  
    - Public API (as per proposal §5.1.0):

      ```python
      def run_meter(kappa_map, void_catalog, config) -> dict:
          ...
      ```

    - Scaffold behavior:
      - Validate the presence of required config keys where cheap.
      - Return a `metrics` dict with all required keys present:
        - `backend`, `z_bin`, `R_v_bin`
        - `R2_wall`, `S_wall`
        - `A_sh`, `AUROC_sh`
        - `beta_interface`, `beta_uncertainty`, `beta_bias`
        - `SNR`, `B_mode_residual`
        - `n_voids`, `quality_flags`, `profile`
      - Populate metrics with placeholder values (e.g. `0.0`, `0`, empty lists) or explicit `NotImplemented` markers.
      - Perform **no** real stacking, fitting, or interface counting.

- **Backends (data adapters; stubs only at T2 scaffold)**  
  - `backends/akra_hsc_y1.py`
    - Stub `load_kappa_map(source="AKRA_HSC_Y1") -> (kappa_map, metadata)`
  - `backends/desy3_dps.py`
    - Stub `load_kappa_map(source="DESY3_Diffusion") -> (kappa_map, metadata)`
  - `backends/mocks.py`
    - Stub `load_mock_suite(name="PyTwinPeaks" | "Flagship" | "Jiutian", ...)`
  - In this phase, each function:
    - Has a clear docstring describing expected behavior and external pipeline.
    - Either returns `(None, {})` or raises `NotImplementedError`.
    - Performs no real I/O at import and no heavy data handling.

- **Validation gates (structure-only, no physics thresholds yet)**  
  - `void_lensing_meter_gates.py`
    - Planned functions:

      ```python
      def evaluate_gates(results):
          ...

      def summarize_gate_outcomes(gate_results):
          ...
      ```

    - Scaffold responsibilities:
      - Validate that `results` contains the required metric keys with sane Python types.
      - Construct a gate-result structure that marks each gate as `"PENDING_IMPLEMENTATION"`.
      - Do **not** evaluate the numeric preregistered thresholds yet.

## 3. JSON manifests and schemas

Planned JSON artifacts (all under this directory unless noted):

- **Approval manifest**  
  - `APPROVAL.json`
    - Follows the template from the proposal (see §5.1.4 APPROVAL.json block).
    - Must include:
      - A preflight entry (runner name + description).
      - A preregistration block:
        - `pre_registered: true`
        - `proposal`: path to `T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md`
        - `allowed_tags: ["void_lensing_meter-v1"]`
        - `schema_dir`: `Derivation/code/physics/cosmology/void_lensing/schemas`
        - `approvals.void_lensing_meter-v1.schema`: path to `void_lensing_meter-v1.schema.json`
        - `approved_by`, `approved_at`, `approval_key` (placeholders in scaffold).

- **Preregistration manifest**  
  - `PRE-REGISTRATION.json`
    - Mirrors the proposal’s PRE-REGISTRATION example:
      - `proposal_title`, `tier_grade`, `commit`, `salted_provenance`, `contact`
      - `hypotheses` H1–H3:
        - H1: `R2_wall >= 0.98`
        - H2: `AUROC_sh >= 0.90`
        - H3: `|beta_est - beta_true| <= 0.1` (via `beta_bias`)
      - `variables`:
        - `independent`: `["backend", "z_bin", "R_v_bin"]`
        - `dependent`: `["R2_wall", "AUROC_sh", "beta_interface"]`
        - `controls`: as listed in the proposal.
      - `pass_fail` entries for `R2_wall`, `AUROC_sh`, `beta_bias` with exact thresholds.
      - `spec_refs` to the two spec files below.
      - `registration_timestamp` placeholder.

- **Specs (run configuration stubs)**  
  - `specs/void_lensing_meter-mocks-v1.json`
    - Example mock-validation spec, following the proposal’s mock example.
    - Keys:
      - `run_name`, `version`, `tag`, `schema_ref`, `parameters`, `seeds`.
  - `specs/void_lensing_meter-data-v1.json`
    - Example real-data dry-run spec, following the proposal’s data example.
    - Same shape as mocks spec but different `backend`, `z_bin`, `seeds`.

- **Output schema**  
  - `schemas/void_lensing_meter-v1.schema.json`
    - JSON Schema matching the proposal’s `void_lensing_meter-v1` stub:
      - Properties: `backend`, `z_bin`, `R_v_bin`, `R2_wall`, `S_wall`, `A_sh`, `AUROC_sh`, `beta_interface`, `beta_uncertainty`, `beta_bias`, `SNR`, `B_mode_residual`, `n_voids`, `quality_flags`, `profile` with inner `x`, `kappa`, `kappa_err`.
      - `required` list exactly as in the proposal’s schema block.
    - This schema is used both by:
      - The approval system (to tie `tag` → `schema`).
      - Future runtime validation of output JSON logs (once implemented).

## 4. Tests (planned)

Tests will live under:

- `Derivation/code/tests/cosmology/void_lensing/test_void_lensing_meter_scaffold.py`

Initial tests (scaffold phase):

- Import tests:
  - Ensure `T2_void_lensing_meter_v1.py`, `meter.py`, `void_lensing_meter_gates.py`, and backend modules import without side effects.

- Spec + CLI dry-run tests:
  - Load `void_lensing_meter-mocks-v1.json` and `void_lensing_meter-data-v1.json`.
  - Invoke the runner with `--spec PATH --dry-run`:
    - No physics; no artifact writes.
    - Exit code 0 on success.
  - Validate that `schemas/void_lensing_meter-v1.schema.json` is valid JSON and exposes the expected keys.

These tests are **structure-only** and are used to gate the scaffold itself (G1–G3, G5 in the session brief), not the T2 physics gates.

## 5. Checklist linkage

The per-domain checklist for this instrument lives at:

- `Derivation/code/physics/cosmology/void_lensing/TODO_CHECKLIST_void_lensing_meter_T2.md`

That checklist is the authoritative sequence of tasks for bringing this instrument from scaffold to a fully wired T2 meter (including physics, gates, and results writeups). This `README` provides the structural plan that the checklist will drive.
