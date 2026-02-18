<!-- DOC-GUARD: CANONICAL -->
# STANDARDS_GOVERNED_HEXAGONAL_FALSIFICATION_ARCHITECTURE

## 1) Purpose & Vision

This standard defines the mandatory architecture for VDM experiment pipelines: proposal-driven, preregistered, externally approved, prediction-anchored, provenance-logged, gate-validated, and contradiction-reporting by construction.

All measurable claims must map to canon anchors and unit-consistent observables. Canon references: [A0](../Derivation/AXIOMS.md#vdm-ax-a0), [A4](../Derivation/AXIOMS.md#vdm-ax-a4), [A5](../Derivation/AXIOMS.md#vdm-ax-a5), [A7](../Derivation/AXIOMS.md#vdm-ax-a7), [kpi-kg-energy-osc-slope](../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-kg-energy-osc-slope), [schema-kg-energy-osc](../Derivation/z.CANONICAL_Schemas/00_SCHEMAS.md#schema-kg-energy-osc), [schema-qfum-metrics-json](../Derivation/z.CANONICAL_Schemas/00_SCHEMAS.md#schema-qfum-metrics-json), [VDM-A-022](../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-022).

## 2) Inviolable Principles

1. **Proposal-first execution**: no real run without proposal + prereg + approval artifact.
2. **Prediction-before-run**: every run must carry a hashed `PredictionEnvelope`.
3. **Canon anchor discipline**: code/docs must reference equations/constants/metrics via canonical anchors; no duplicated normative math/thresholds.
4. **Provenance chain completeness**: proposal, prereg, spec, schema, logs, figures, CSVs, and summaries must be hash-linked.
5. **Automated contradiction reporting**: any gate failure emits a contradiction report and quarantines artifacts.
6. **Determinism and reproducibility**: IEEE-754 double precision, seed logging, commit hash logging, environment receipts.
7. **Layer boundaries enforced**: domain core must not depend directly on infrastructure adapters.

## 3) Mandatory Clean Architecture (VDM Physics Naming)

All new and migrated domains SHALL follow these layers:

- `experiment_control/`
  - CLI/API entrypoints, argument parsing, run intents.
- `execution_pipeline/`
  - orchestration state machine and policy sequencing.
- `theory_core/`
  - physics kernels, numerics, meters, domain rules.
- `validation_gateways/`
  - KPI gate adapters and verdict aggregation.
- `provenance_ledger/`
  - hashing, receipts, manifest linkage, run lineage.
- `artifact_registry/`
  - IO routing, schema validation, storage registration.
- `governance_ports/`
  - approval, prereg, canon-anchor policy interfaces.

### Required domain contracts

- `Predictor`: builds/loads `PredictionEnvelope`.
- `ApprovalAuthority`: verifies `ApprovalArtifact` against proposal/prereg/schema and DB key policy.
- `ValidationGate`: evaluates KPI thresholds and emits machine-verifiable verdicts.
- `ProvenanceRecorder`: records run-level and artifact-level hashes.
- `ContradictionReporter`: emits contradiction artifacts and quarantine linkage.

## 4) Canonical Workflow Specification

| Step | Required Artifact | Enforced Checks | Output |
|---|---|---|---|
| Proposal | `ProposalDocument` | Exists, canonical location, prereg linkage | proposal hash |
| Approval | `ApprovalArtifact` | tag allowed, approved_by, approval_key, schema path | approval verdict |
| Prediction | `PredictionEnvelope` | pre-run timestamp + hash + expected gate bands | prediction hash |
| Run | run handle | deterministic seeds, commit hash, spec/schema refs | raw artifacts |
| Validation | `ValidationVerdict` | KPI gates per canon anchors | pass/fail verdict |
| Contradiction | `ContradictionReport` | generated if any mandatory gate fails | quarantine + report |
| Archive | `ProvenanceReceipt` | full hash-chain completeness and schema conformity | publishable record |

Minimum artifacts per non-headless run: **1 PNG + 1 CSV + 1 JSON** routed via `Derivation/code/common/io_paths.py`.

## 5) Data / Artifact Contracts

Required classes (logical contracts; implementation language may vary):

- `ProposalDocument`
  - `proposal_path`, `proposal_sha256`, `canon_refs[]`
- `ApprovalArtifact`
  - `domain`, `tag`, `approved_by`, `approved_at`, `approval_key`, `schema_ref`
- `PredictionEnvelope`
  - `tag`, `hypothesis_ref`, `predicted_metrics[]`, `gate_threshold_refs[]`, `prediction_sha256`
- `RunArtifactSet`
  - `figure_paths[]`, `csv_paths[]`, `json_paths[]`, `artifact_hashes{}`
- `ValidationVerdict`
  - `gate_results[]`, `overall_pass`, `failed_gate_ids[]`
- `ContradictionReport`
  - `run_id`, `failed_gate_ids[]`, `observed_vs_predicted`, `quarantine_paths[]`
- `ProvenanceReceipt`
  - `git_commit`, `tree_hash`, `seed_list`, `schema_refs[]`, `hash_chain[]`

## 6) Enforcement Rules

1. **Approval gate** must run before `begin_real_run`.
2. **Prediction envelope** must exist and be hash-registered before execution.
3. **Schema validation** required at:
   - input spec ingest,
   - output summary emission.
4. **Gate failure policy**:
   - set run status failed,
   - write contradiction JSON,
   - route artifacts to quarantine (`failed_runs`).
5. **Promotion policy**:
   - only `overall_pass=true` + complete provenance receipts may be promoted to canonical results registries.

## 7) Governance & Quality Bar

Mandatory standards for all architecture components:

- Import boundary checks (hexagonal layering).
- File size target `<500 LOC` per core module where practical.
- Contract/unit/e2e coverage target `>=85%` for migrated SGHFA adapters.
- Canon-link enforcement in docs and metadata.
- Structured logging of seeds, hashes, gate outcomes, and approval provenance.

## 8) Customization Hooks (Extensions)

To add a new metric, validator, or schema:

1. Register metric and threshold references in canonical registry anchors.
2. Add/extend schema under domain `schemas/` with versioned name.
3. Add/extend `ApprovalArtifact` mapping in `APPROVAL*.json`.
4. Add or update `PredictionEnvelope` fields for new KPI expectations.
5. Implement `ValidationGate` adapter and contradiction semantics.
6. Add policy and contract tests.
7. Update CHRONICLES attestation.

No extension may bypass proposal/approval/prediction/provenance/contradiction requirements.

## 9) Contributor Compliance Procedure

1. Confirm proposal + prereg + approval exists for tag.
2. Execute through approved runner path using common IO/provenance helpers.
3. Emit required artifacts and schema-validated summary.
4. Verify all mandatory gates.
5. If failed, emit contradiction report and quarantine outputs.
6. Update registries/chronicles for canonical-impacting changes.

## 10) Glossary

- **ApprovalArtifact**: Signed/hashed approval binding domain+script+tag to an approver and schema.
- **PredictionEnvelope**: Pre-run, immutable declaration of expected measurable outcomes and gates.
- **ValidationGate**: Deterministic check mapping observable metrics to pass/fail verdict.
- **ContradictionReport**: Machine-readable artifact documenting failed predictions/gates and quarantine rationale.
- **ProvenanceReceipt**: Structured run-level evidence chain (hashes, commit, environment, seeds).
- **Quarantine**: Storage path and status for non-promotable failed/engineering runs.
- **Promotion**: Transition of outputs into canonical results registries after full compliance.
- **Hexagonal boundary**: Separation of domain core from infrastructure through explicit ports/adapters.

