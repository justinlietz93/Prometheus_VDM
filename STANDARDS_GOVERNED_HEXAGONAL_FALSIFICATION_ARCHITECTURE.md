# STANDARDS_GOVERNED_HEXAGONAL_FALSIFICATION_ARCHITECTURE

**Document class:** Canonical standards (living)
**Applies to:** Prometheus_VDM falsification and validation package (`Derivation/` + `Derivation/code/`)
**Intent:** Agency-enforceable architecture standard for scientifically rigorous, reproducible VDM pipelines.

## 1) Purpose and Vision

This standard defines the mandatory architecture and governance model for VDM experiment pipelines.

The purpose is to build and maintain **domain-native, scientifically rigorous, hash/provenance-anchored, proposal/approval-validated, contradiction-reporting, reproducible physics workflows** for VDM and related theories.

Every executable claim must be:

1. Proposed,
2. Pre-registered,
3. Approved,
4. Predicted before execution,
5. Gate-validated,
6. Provenance logged with hashes,
7. Published as pass or contradiction artifact.

## 2) Inviolable Principles

1. **Proposal-first execution**
   - No production run without a ProposalDocument and preregistration.

2. **Approval-gated execution**
   - No production run without ApprovalArtifact verification.

3. **Prediction-before-run discipline**
   - Every run must emit a PredictionEnvelope before compute execution.

4. **Canon anchor authority**
   - Equations, constants, thresholds, schemas, and metrics are referenced by canon anchors only.
   - Program logic must not duplicate authoritative values from canon.

5. **End-to-end provenance and hashing**
   - Every run input/output artifact must be hash-registered.
   - The sequence proposal → prereg → approval → prediction → run → gate result is hash-linked.

6. **Automated contradiction transparency**
   - Any gate or provenance failure produces a ContradictionReport artifact and quarantine routing.

7. **Clean architecture + dependency inversion**
   - Outer layers depend on inner abstractions only.
   - Domain remains framework-independent.

8. **Reproducibility over convenience**
   - Deterministic seeds, schema-validated contracts, and machine-readable receipts are mandatory.

## 2.1) Current-repo alignment (already implemented baseline)

This standard codifies patterns already present in Prometheus_VDM and promotes them to non-optional governance rules:

- SQLite-backed approval enforcement (`VDM_APPROVAL_DB`) and script/tag approval checks.
- Common helper-library usage for IO routing (`io_paths`), plotting, instrument helpers, and validation-gate helpers.
- Spec/prereg-driven run configuration and schema-backed artifacts in governed domain pipelines.
- Contradiction artifact emission and quarantine routing for failed gates/provenance checks.

## 3) Mandatory Clean/Hexagonal Layers (VDM Physics Naming)

Repository modules implementing this standard MUST map to the following logical layers.

## 3.1 `experiment_control/` (Presentation / orchestration interface)

Responsibilities:
- CLI/API entrypoints.
- Accept run requests.
- Trigger pipeline use-cases.
- Zero domain math/business policy in this layer.

Depends on:
- `execution_pipeline` ports only.

## 3.2 `execution_pipeline/` (Application workflows)

Responsibilities:
- Orchestrate stage flow:
  - proposal checks
  - prereg checks
  - approval checks
  - prediction emission
  - execution invocation
  - gate evaluation
  - contradiction/publication routing
- Invoke domain ports, not infrastructure implementations directly.

Depends on:
- `theory_core` contracts/interfaces.

## 3.3 `theory_core/` (Domain model and falsification core)

Responsibilities:
- Domain entities and value objects.
- Contract definitions for predictor, gate, provenance, approval, contradiction handling.
- Policy definitions independent of frameworks/IO.

Depends on:
- nothing outward; pure domain logic.

## 3.4 `infrastructure_adapters/` (Persistence/IO/adapters)

Responsibilities:
- Filesystem artifact storage.
- Database repositories.
- Canon registry readers.
- Hashing/provenance services.
- Reporting publishers.

Implements:
- ports from `theory_core` used by `execution_pipeline`.

## 3.5 `governance_automation/` (Policy enforcement tooling)

Responsibilities:
- CI checks (architecture boundaries, provenance completeness, schema compliance, coverage, canon-link checks).
- Pre-commit guards.
- Security/lint/static analysis policy hooks.

## 4) Domain Contracts (Required)

All production workflows must use explicit, schema-backed contracts.

1. **ProposalDocument**
   - proposal_id
   - title
   - domain
   - hypotheses[]
   - canon_anchor_refs[]
   - proposal_hash

2. **PreRegistrationRecord**
   - prereg_id
   - proposal_id
   - variables, controls, pass_fail criteria
   - spec_refs
   - salted_provenance
   - prereg_hash

3. **ApprovalArtifact**
   - proposal_id / prereg_id / tag
   - approved_by
   - approved_at
   - approval_key
   - script_scope
   - approval_hash

4. **PredictionEnvelope**
   - prediction_id
   - prereg_id + approval_id
   - predicted metric envelopes and thresholds
   - confidence/range metadata
   - prediction_hash

5. **ExecutionReceipt**
   - run_id
   - spec hash
   - git commit
   - tree hash
   - seeds
   - runtime/hardware
   - execution_hash

6. **GateEvaluation**
   - gate_id
   - canon_anchor_refs
   - measured values
   - threshold values
   - passed bool
   - gate_hash

7. **ContradictionReport**
   - run_id
   - failed_gate_ids
   - evidence artifact pointers
   - severity
   - contradiction_hash

8. **ArtifactManifest**
   - all emitted artifacts with content hash + media type + role
   - parent_hash pointer to previous stage manifest

9. **ProvenanceLedgerEntry**
   - stage name
   - actor
   - timestamp
   - input_hashes[]
   - output_hashes[]
   - parent_hash

## 5) Required Ports / Interfaces

The following ports define hexagonal seams and must be consumed through interfaces:

- **PredictorPort**: build prediction envelope from prereg + canon anchors.
- **ApprovalPort**: validate approval artifact, tag/script scope, approver identity.
- **ValidationGatePort**: evaluate registered gate sets and emit GateEvaluation records.
- **ProvenancePort**: compute hashes, assemble ledger entries, verify chain integrity.
- **ArtifactRegistryPort**: persist and index all artifacts.
- **ContradictionReporterPort**: emit contradiction artifacts and publish index updates.
- **CanonResolverPort**: resolve thresholds/constants/equations by canonical anchor IDs.

## 5.1) Existing VDM helper-library integration rules (mandatory)

All production runners MUST use the common helper stack and must not inline these responsibilities:

1. **Instrument certification + meters**
   - Use dedicated instrument helper modules (`Derivation/code/common/instrument_helpers/*` and certified instrument surfaces).
2. **Validation gates**
   - Gate decision logic must live in validation helper modules (`Derivation/code/common/validation_gate_helpers/*`).
   - Runners import gate helpers; runners do not define production gate formulas inline.
3. **Artifact/log path policy**
   - All output routing must use `Derivation/code/common/io_paths.py`.
4. **Plotting generation**
   - Plot/figure composition should be helperized via `Derivation/code/common/plotting/*` or domain helper modules, then imported by runners.
5. **Approval backend**
   - Approval authority is SQLite-backed (`VDM_APPROVAL_DB`) and enforced via `common.authorization.approval`.

## 5.2) Parameter and test-input authority rule (mandatory)

- Authoritative numerical parameters and test inputs come from prereg/spec artifacts only (`PRE-REGISTRATION*.json`, `specs/*.json`, declared schemas).
- CLI flags may select a registered spec, but must not silently override preregistered values unless an approved policy exception is explicitly recorded in the run receipt and approval scope.
- Any extension of parameter surface requires:
  1) prereg/spec schema update,
  2) approval update,
  3) provenance hash-chain update.

## 6) Workflow Specification (Mandatory Sequence)

| # | Stage | Input | Output | Enforcements |
|---|---|---|---|---|
| 1 | Proposal | Proposal draft | ProposalDocument | Canon anchors present, proposal hash created |
| 2 | Preregistration | ProposalDocument | PreRegistrationRecord | Hypotheses/variables/pass-fail schema valid; salted provenance present |
| 3 | Approval | Prereg + script/tag | ApprovalArtifact | Approver policy + key verification + script scope verification |
| 4 | Prediction | Approved prereg | PredictionEnvelope | Prediction created before run, hash-logged |
| 5 | Hash-logged Execution | Prediction + spec | ExecutionReceipt + raw artifacts | Deterministic seed log, run receipts, artifact hashes |
| 6 | Validation Gates | Execution artifacts | GateEvaluation set | All gates mapped to canon anchor refs and threshold contracts |
| 7 | Pass/Contradiction Routing | GateEvaluation | Pass package OR ContradictionReport | Any failure generates contradiction artifact + quarantine |
| 8 | Provenance/Register Publish | All stage outputs | ArtifactManifest + ledger updates | Full chain integrity check; index publish |

## 7) Enforcement Matrix

## 7.1 Proposal / prereg / approval enforcement

- `execution_pipeline` must stop execution on missing ProposalDocument, prereg, or ApprovalArtifact.
- `ApprovalPort` must verify domain, script scope, tag, approver identity, and key material.

## 7.2 Prediction envelope enforcement

- `PredictorPort` output is mandatory precondition for execution.
- No validation comparison is valid without a recorded PredictionEnvelope.

## 7.3 Validation gate enforcement

- Gates must be registered and traceable to canon anchor refs.
- Inline ad-hoc thresholds outside gate contracts are disallowed in production.
- Validation gates must be implemented as helper tools/modules and imported by runners.

## 7.4 Contradiction and quarantine enforcement

- Any failed gate or provenance failure must produce ContradictionReport.
- Contradiction runs are quarantined and indexed.

## 7.5 Provenance/hash enforcement

- Every stage writes hash-bearing artifacts.
- ArtifactManifest must include all artifacts and parent hash pointer.
- Chain break = governance failure.
- Approval method and SQLite approval DB source must be recorded in run receipts for auditability.

## 8) Governance and Quality Requirements

1. **Architecture boundaries**
   - Import rules enforce allowed dependencies only.

2. **File-size discipline**
   - No source file >500 LOC target for new/refactored files.

3. **Coverage requirements**
   - Unit + contract + e2e coverage target ≥85% for governed packages.

4. **Schema and contract validation**
   - All artifacts must validate against declared schemas.
   - Parameters/test inputs must map one-to-one to prereg/spec schemas; undeclared runtime parameters are policy violations.

5. **Canon linkage policy**
   - Code/docs must cite canonical anchors for all equations/thresholds/KPIs.

6. **Provenance policy**
   - Run receipts include commit/tree hash/salted provenance/hardware/seeds/gates.

7. **Commit and CI policy**
   - No merge if architecture/provenance/canon-link checks fail.

8. **Security/policy checks**
   - Linter/static checks/SAST hooks run in CI according to governance profile.

## 9) Customization Hooks (How to Extend Safely)

## 9.1 Add a new metric

1. Add metric definition to canonical validation metric registry.
2. Add or update schema contract for metric output.
3. Implement metric through a registered gate interface.
4. Require approval update for affected run tags.
5. Add tests for gate pass/fail and contradiction path.

## 9.2 Add a new validator/gate

1. Register gate-id + canon anchors + expected fields.
2. Implement in `ValidationGatePort` adapter and dedicated helper module (not runner inline).
3. Ensure contradiction emission on failure.
4. Add CI tests verifying schema and registration consistency.

## 9.3 Add a new artifact schema

1. Define schema and version.
2. Add artifact role to ArtifactManifest contract.
3. Register hash generation and ledger insertion.
4. Update governance checks for schema conformance.

## 9.4 Add a new domain experiment

1. Scaffold proposal/prereg/spec/schema/approval artifacts.
2. Implement runner using pipeline interfaces only.
3. Register domain gates and canon anchors.
4. Validate full workflow including contradiction route.

## 10) Contributor Compliance and Review Procedure

All contributions affecting falsification pipeline behavior must include:

1. Contract impact statement (which artifacts/contracts changed).
2. Canon anchor impact statement.
3. Provenance impact statement.
4. Contradiction handling statement.
5. Tests:
   - unit tests for domain logic
   - contract tests for schemas and ports
   - e2e tests for stage sequence and failure routing.

Reviewers must reject changes that:
- bypass proposal/prereg/approval/prediction sequence,
- hard-code canonical thresholds outside approved canonical sources,
- omit provenance hash registration,
- suppress contradiction artifacts.

## 11) Migration Guidance (Current Repository Adoption)

Adopt SGHFA incrementally:

1. Standardize contracts and ports in shared modules.
2. Wrap existing runners with execution pipeline orchestration.
3. Replace ad-hoc threshold constants with CanonResolverPort lookups.
4. Add mandatory PredictionEnvelope stage before run.
5. Introduce global contradiction schema and registry.
6. Enable CI hard-fail on boundary/provenance/canon-link violations.

## 12) Glossary (VDM Context)

- **Agency-approved run:** Run with validated ApprovalArtifact for script+tag scope.
- **ArtifactManifest:** Hash-indexed list of all run artifacts plus chain pointers.
- **Canon anchor:** Stable identifier in canonical registries for equations/constants/metrics/schemas.
- **ContradictionReport:** Machine-readable failure artifact documenting falsified or policy-breaching outcomes.
- **ExecutionReceipt:** Run-level provenance envelope containing execution and environment facts.
- **Falsification package:** End-to-end machinery that tests a claim against predeclared criteria.
- **GateEvaluation:** Structured pass/fail record for a validation gate and its metrics.
- **Hexagonal architecture:** Ports-and-adapters pattern isolating domain core from infrastructure.
- **PredictionEnvelope:** Pre-run quantitative expectation envelope used for post-run falsification checks.
- **PreRegistrationRecord:** Locked test plan defining hypotheses, variables, and pass/fail rules before execution.
- **ProposalDocument:** Formal statement of what is being tested and why.
- **Provenance ledger:** Ordered, hash-linked history of stage transitions and artifacts.
- **Quarantine routing:** Automatic failed-run artifact placement and indexing for review.

---

**Living-document policy:**
- Update this standard when architecture policy changes.
- Any update must include migration notes and impact on existing runners.
- This document is authoritative for SGHFA compliance in Prometheus_VDM.
