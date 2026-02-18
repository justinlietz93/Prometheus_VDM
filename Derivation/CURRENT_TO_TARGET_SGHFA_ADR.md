<!-- DOC-GUARD: CANONICAL -->
# ADR — Current → Target Architecture Migration for VDM Falsification Pipeline

Date: 2026-02-18  
Status: Proposed  
Decision Scope: `Derivation/` pipeline governance and execution architecture

## 1) Context

This ADR records the current implementation state of the VDM experiment pipeline and defines the target migration to a standards-governed, hexagonal falsification architecture. The target must preserve existing domain behavior while making proposal→approval→prediction→execution→validation→contradiction reporting fully enforceable and auditable.

Canon references (anchors only): [A4](../Derivation/AXIOMS.md#vdm-ax-a4), [A5](../Derivation/AXIOMS.md#vdm-ax-a5), [A7](../Derivation/AXIOMS.md#vdm-ax-a7), [VDM-A-013](../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-013), [VDM-A-022](../Derivation/z.CANONICAL_Algorithms/00_ALGORITHMS.md#vdm-a-022), [kpi-kg-energy-osc-slope](../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md#kpi-kg-energy-osc-slope), [schema-kg-energy-osc](../Derivation/z.CANONICAL_Schemas/00_SCHEMAS.md#schema-kg-energy-osc), [schema-qfum-metrics-json](../Derivation/z.CANONICAL_Schemas/00_SCHEMAS.md#schema-qfum-metrics-json).

## 2) Current State Inventory (As-Is)

### 2.1 Workflow and orchestration

- Domain runners live under `Derivation/code/physics/{domain}/`.
- Output routing is centralized in `Derivation/code/common/io_paths.py` (pass/fail routing to normal vs `failed_runs`).
- Run lifecycle rows are persisted through `Derivation/code/common/data/results_db.py`:
  - `begin_run` / `begin_real_run` / `begin_preflight_run`
  - `log_metrics`, `add_artifacts`, `end_run_success`, `end_run_failed`
  - tamper-evident `row_hash` per row.

### 2.2 Proposal / preregistration / approval touchpoints

- Approval manifests: `Derivation/code/physics/*/APPROVAL*.json`.
- Prereg manifests: `Derivation/code/physics/*/PRE-REGISTRATION*.json`.
- Runtime approval enforcement:
  - `Derivation/code/common/authorization/approval.py` (`should_enforce_approval`, `check_tag_approval`).
  - DB-backed HMAC approval keys, script-scoped policy message `domain:script:tag`.
- Approval administration:
  - `Derivation/code/common/authorization/approve_tag.py`
  - `Derivation/code/common/authorization/README.md`.
- Proposal/prereg provenance stamping:
  - `Derivation/code/common/provenance/stamp_proposal.py`
  - Optional strong provenance checks in approval gate when `require_provenance=true`.

### 2.3 Validation gates / falsification logic

- Domain and shared gate helpers:
  - `Derivation/code/common/validation_gate_helpers/*`
  - `Derivation/code/common/instrument_helpers/*`
  - e.g., `Derivation/code/physics/metriplectic/echo_gates.py` for G1–G4.
- Gates are applied in runner-specific logic; gate failures commonly mark run status failed and route artifacts to `failed_runs`.
- KPI definitions are canonized in [00_VALIDATION_METRICS](../Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md) but many runners still embed threshold logic directly.

### 2.4 Provenance / hash tracking

- Repo-wide provenance:
  - `tools/provenance/generate_manifest.py` → `PROVENANCE_manifest.json`
  - CI workflow `.github/workflows/provenance-index-and-hash.yml`.
- Per-run provenance receipts helper:
  - `Derivation/code/common/provenance/run_receipts.py`
  - includes git/tree hash, salted hash, hardware receipts, seeds.
- Results rows include row-level hash-chain primitives (`row_hash`) but no cross-artifact hash-chain ledger.

### 2.5 Schemas and data products

- Schema files exist under domain folders (`schemas/*.schema.json`) and canonical schema registry [00_SCHEMAS](../Derivation/z.CANONICAL_Schemas/00_SCHEMAS.md).
- Data products are indexed canonically in [00_DATA_PRODUCTS](../Derivation/z.CANONICAL_Data_Products/00_DATA_PRODUCTS.md), while runners often perform lightweight/manual schema checks.

### 2.6 Governance and CI automation

- `.github/workflows/preflight-push.yml`: preflight smoke test execution.
- `.github/workflows/derivation-guard.yml`: CHRONICLES + canon policy check.
- `.github/workflows/provenance-index-and-hash.yml`: provenance artifact generation.
- `.pre-commit-config.yaml`: derivation guard hook.
- Note: workflows reference `VDM_Nexus/scripts/*`, but this path is absent in current repository checkout.

## 3) Gaps vs Target SGHFA

1. **Architecture boundaries not explicit or enforced as ports/adapters** (hexagonal boundaries are implied, not codified).
2. **Contradiction reporting is fragmented** (fail status exists, but no standardized contradiction artifact contract).
3. **No mandatory pre-run prediction envelope contract** in a single canonical adapter API.
4. **Schema enforcement is uneven** (many runs rely on local checks instead of strict centralized validator adapters).
5. **Provenance chain is not end-to-end artifact-level** (row hash exists, but figures/logs/specs not consistently hash-linked as one run chain).
6. **Approval enforcement scope stops at run start** (no explicit promotion gate for downstream publication/registry insertion).
7. **Canon anchor binding is policy, not machine-enforced in all runtime logic** (thresholds still duplicated in code in places).

## 4) Target State — Standards-Governed Hexagonal Falsification Architecture

Target properties:

- Domain-native clean architecture with explicit inbound/outbound ports for:
  - ProposalDocument intake
  - ApprovalArtifact verification
  - PredictionEnvelope registration
  - ValidationGate execution
  - ContradictionReporter publication
  - ProvenanceLedger write/verify.
- All gates, metrics, constants, equations reference canonical anchors only.
- Every run yields deterministic, schema-validated, hash-chain linked artifacts (PNG + CSV + JSON minimum).
- Contradiction path is first-class: fail routes trigger contradiction report JSON + quarantine registration.
- Promotion/publication requires post-run policy checks (approval validity, schema validity, provenance completeness, gate verdicts).

## 5) Delta / Migration Plan

1. **Create contracts package** under `Derivation/code/common` for SGHFA interfaces:
   - `ProposalDocument`, `ApprovalArtifact`, `PredictionEnvelope`, `ValidationVerdict`, `ContradictionReport`, `ProvenanceReceipt`.
2. **Add centralized adapters**:
   - approval adapter wrapping existing `authorization/approval.py`
   - provenance adapter wrapping `run_receipts.py` + manifest tools
   - validation adapter wrapping `validation_gate_helpers`.
3. **Introduce run state machine**:
   - `proposed -> approved -> predicted -> executed -> validated -> (passed|contradicted) -> archived`.
4. **Add contradiction reporter helper**:
   - standardized JSON contradiction artifact, linked to failed run row and quarantined artifacts.
5. **Enforce prediction-before-execution policy**:
   - no begin_real_run unless a prediction envelope with hash exists for the tag.
6. **Harden schema gate**:
   - required JSON Schema validation at run ingress and summary egress.
7. **Complete hash-chain**:
   - include artifact hashes (figure/log/csv/spec/proposal/prereg/schema) in final run receipt.
8. **Canon binding enforcement**:
   - lints/checks that threshold/equation identifiers are anchor references in metadata fields.
9. **CI enforcement uplift**:
   - fail when derivation-guard script path missing; add explicit SGHFA contract tests.

## 6) Consequences

### Positive

- Stronger falsifiability and auditability.
- Lower ambiguity in run legitimacy and contradiction handling.
- Better separation of domain physics from policy/infrastructure concerns.

### Costs / constraints

- Additional adapter and contract maintenance overhead.
- Existing runners will need incremental migration to new port contracts.
- Stricter policy enforcement may quarantine currently “informational-only” runs.

### Risk controls

- Migrate per domain with compatibility shims over `results_db` and `io_paths`.
- Keep existing approval DB model as backend; only change orchestration boundaries.

