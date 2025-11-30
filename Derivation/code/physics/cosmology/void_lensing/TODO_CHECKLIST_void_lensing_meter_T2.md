# T2 Void Lensing Cross-Correlation Meter v1 – TODO Checklist

This checklist is the domain-level control file for the T2 void-lensing meter scaffold.
Treat the proposal as the contract and keep items in sequential order.

## Canon anchors

- [`T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md`](Derivation/Cosmology/Void_Lensing/T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md:1)
- [`T0_Unification_Program_Spec_v1.md`](Derivation/Unification/T0_Unification_Program_Spec_v1.md:1)
- [`authorization/README.md`](Derivation/code/common/authorization/README.md:1)
- [`io_paths.py`](Derivation/code/common/io_paths.py:1)
- [`domain_setup/README.md`](Derivation/code/common/domain_setup/README.md:1)

## Tasks

- [x] 1. Discovery / contract verification for `void_lensing_meter-v1`
  - Read proposal §5.1.0–5.1.4 and record required metrics, schema keys, gate thresholds, and JSON paths.
  - Confirm variables and pass/fail metrics in `PRE-REGISTRATION.json` match proposal text.
- [ ] 2. Create `Derivation/code/physics/cosmology/void_lensing/` scaffold
  - Add `README.md`, `APPROVAL.json`, `schemas/`, `specs/`, and `meter.py` skeleton consistent with domain setup rules.
  - Ensure no heavy physics logic or artifact-writing side effects are implemented at import time.
- [ ] 3. Implement `T2_void_lensing_meter_v1.py` runner skeleton
  - Wire CLI (`--spec`, `--dry-run`), config loading, provenance, and approval checks; call a stub orchestration layer.
- [ ] 4. Implement `meter.run_meter(kappa_map, void_catalog, config) -> dict` API stub
  - Ensure the returned metrics dict exposes all keys required by `void_lensing_meter-v1.schema.json`.
- [ ] 5. Add backend loader stubs under `backends/` for AKRA, DESY3 DPS, and mocks
  - Define pure interface functions with docstrings and TODO markers; no I/O at import.
- [ ] 6. Implement `void_lensing_meter_gates.py` structure-only gate functions
  - Check presence and basic types for `R2_wall`, `A_sh`, `AUROC_sh`, `beta_interface`, `beta_uncertainty`, `beta_bias`, `SNR`, `B_mode_residual`, `n_voids`.
- [ ] 7. Create APPROVAL and PRE-REGISTRATION JSON manifests
  - Mirror the exact fields, paths, allowed tags, variables, and pass/fail thresholds from the proposal.
- [ ] 8. Create spec JSONs and output schema stub
  - `specs/void_lensing_meter-mocks-v1.json`
  - `specs/void_lensing_meter-data-v1.json`
  - `schemas/void_lensing_meter-v1.schema.json` (minimum properties + required list per proposal).
- [ ] 9. Add scaffold tests under `Derivation/code/tests/cosmology/void_lensing/`
  - Import runner, meter, and gates; run a dry-run path on a minimal spec and validate JSON structure.
- [ ] 10. Session notes + handoff
  - Update [`T2_void_lensing_meter_v1_scaffold.md`](memory-bank/roo_sessions/T2_void_lensing_meter_v1_scaffold.md) with files created, gate status (G1–G5), and next steps.