# ADR: Prometheus_VDM Current Pipeline → Standards-Governed Hexagonal Falsification Architecture (SGHFA)

- **Status:** Proposed
- **Date:** 2026-02-18
- **Deciders:** Repository maintainers and domain approvers
- **Scope:** `Derivation/` canon + `Derivation/code/` experiment pipeline + governance automation

## 1) Context

Prometheus_VDM already has substantial falsification-oriented machinery:

- Canon registries are centralized under `Derivation/z.CANONICAL_*` (symbols, equations, algorithms, constants, schemas, data products, validation metrics, proposals, results).
- Experiment domains under `Derivation/code/physics/*` commonly include `APPROVAL.json`, pre-registration JSON, spec JSON, schema JSON, run scripts, and output routing.
- Runtime approval checks, provenance receipts, quarantine routing, results database logging, and contradiction-report emissions are already present.
- CI automation exists for derivation guard, provenance index/hash generation, and preflight smoke tests.

However, implementation is uneven across domains and not yet fully expressed as a strict domain-native clean/hexagonal architecture with complete policy enforcement.

## 2) Current Architecture / Workflow Inventory (As-Is)

## 2.1 Core workflow as implemented now

| Stage | Current implementation touchpoints | Current behavior |
|---|---|---|
| Proposal + Pre-registration authoring | `Derivation/*/PROPOSAL_*.md`, `Derivation/code/physics/*/PRE-REGISTRATION*.json`, scaffold templates in `Derivation/code/common/domain_setup/` | Proposal and prereg artifacts are expected and scaffoldable; consistency quality varies by domain. |
| Approval materialization | `Derivation/code/physics/*/APPROVAL*.json`, `Derivation/code/common/authorization/approve_tag.py` | HMAC approval keys are generated/managed via approvals DB; script-scoped approval is supported. |
| Run admission gate | `Derivation/code/common/authorization/approval.py::check_tag_approval` | Enforces tag membership, approver identity, schema existence/shape, proposal/prereg provenance checks (when required), and approval-key match. |
| Run execution | Domain runners in `Derivation/code/physics/*/*.py` | Numerical runs generate metrics/artifacts, often gated pass/fail decisions and quarantine behavior. |
| Validation/falsification | Domain-specific gate helpers + runner gate blocks | KPIs and pass/fail logic are present, often with per-gate metrics and aggregate ledgers; contradiction paths are emitted in several domains. |
| Provenance receipts | `Derivation/code/common/provenance/run_receipts.py` | Captures `git_commit`, `tree_hash`, salted hash, IEEE-754 flag, seeds, hardware, gate outcomes. |
| Artifact/log routing | `Derivation/code/common/io_paths.py` | Approved/unapproved policy can force quarantine (`failed_runs`) and optionally hard-block. |
| Persistent run ledger | `Derivation/code/common/data/results_db.py` | Per-domain SQLite, per-experiment tables, lifecycle status, JSON payloads, row-hash tamper evidence. |
| Governance automation | `.github/workflows/*.yml`, `.pre-commit-config.yaml` | Preflight smoke tests, derivation guard, and provenance manifest/index automation on push. |

## 2.2 Validation and falsification logic inventory

- **Gate expression style:** mix of pure helper functions (`common/validation_gate_helpers/*`) and inline runner logic.
- **Gate outputs:** generally boolean pass/fail + metric dicts; some runners aggregate pass-rates and thresholds.
- **Contradiction reporting:** implemented in multiple runners using explicit `CONTRADICTION_REPORT*` logs, but no single cross-domain contradiction artifact contract.
- **Schema usage:** many domains publish schemas and specs; enforcement against schema/tag is strongest in approval checks and selected tests.

## 2.3 Provenance, hashing, and traceability inventory

- **Repo-level provenance:** workflow generates `PROVENANCE_manifest.json` and distributed `PROVENANCE_index.json` files.
- **Run-level receipts:** canonical receipt helper computes run receipts with salted hash and hardware metadata.
- **Proposal/prereg salted provenance:** stamp helper + approval checker support salted provenance line and prereg hash consistency checks.
- **DB hash-chain surrogate:** row-level SHA-256 (`row_hash`) supports tamper-evident row integrity, but no explicit append-linked hash chain across all run artifacts.

## 2.4 Canonical markdown enforcement inventory

- Strong canonical registry exists (`Derivation/z.CANONICAL_*`, `CANON_STANDARDS.md`).
- Most code references canon by anchor in docstrings/comments, but there is limited automated enforcement that every executable threshold/value is loaded via canonical anchor resolution.
- Some helper modules still carry in-code defaults/thresholds and formula implementations directly.

## 2.5 File/directory division of responsibilities (as-is)

- `Derivation/z.CANONICAL_*`: canonical physics/program metadata registries.
- `Derivation/code/common/authorization`: approvals, keying, policy checks.
- `Derivation/code/common/provenance`: proposal/prereg stamping + run receipts.
- `Derivation/code/common/data`: run databases + preflight logging.
- `Derivation/code/common/validation_gate_helpers`: pure KPI gate evaluators.
- `Derivation/code/common/instrument_helpers`: meter/observable computations.
- `Derivation/code/physics/*`: domain runners, specs, approvals, schemas.
- `Derivation/code/tests/*`: preflight and domain test suites.
- `.github/workflows/*`: CI governance automation.


## 2.6 Instrument certification + helper-library integration (explicit inventory)

Observed in current repository:

- Instrument certification scaffolding and policy exist in `Derivation/code/common/certified_instruments/`, domain `APPROVAL*.json`, and proposal/prereg artifacts, but enforcement depth is domain-dependent.
- Shared helper libraries already define separations:
  - computation/meters: `Derivation/code/common/instrument_helpers/*`
  - validation decisions: `Derivation/code/common/validation_gate_helpers/*`
  - artifact routing: `Derivation/code/common/io_paths.py`
  - plotting helpers: `Derivation/code/common/plotting/*`
- Several runners still perform mixed responsibilities inline (compute + gate + artifact generation inside one script) rather than importing each responsibility from dedicated helper modules.
- Approval runtime enforcement is SQLite-backed (`VDM_APPROVAL_DB`) through `Derivation/code/common/authorization/approval.py`, with CLI administration in `approve_tag.py`.

## 2.7 Parameter authority + test input source of truth (explicit inventory)

Observed policy and behavior:

- Pre-registration/spec manifests are intended to carry run parameters and test inputs (`PRE-REGISTRATION*.json`, `specs/*.json`, schema refs).
- In practice, many runners still accept CLI flags that can alter numerical parameters directly, which weakens strict prereg authority unless wrapper policy forbids overrides.
- Current tests include preflight smoke tests and domain tests, but not all pipelines enforce "parameters/test inputs only from prereg/spec" as a hard gate.

## 3) Gap Analysis vs Target Requirements

## 3.1 Enforced domain-native clean architecture

**Strengths now**
- Practical separation exists (common helpers vs domain runners).
- Many gate helpers are pure and side-effect free.
- Existing helper families already indicate intended separation (instrument helpers, validation-gate helpers, plotting, IO path routing).

**Gaps**
- No hard architectural boundary checker for presentation/application/domain/infrastructure layer imports.
- Domain model contracts (ProposalDocument, ApprovalArtifact, PredictionEnvelope, etc.) are implicit JSON conventions, not strongly typed ports/contracts enforced repo-wide.
- Several scripts are monolithic and mix orchestration, physics, validation, artifact generation, and persistence concerns.
- Rule "validation gates and artifact generation must be separate helper tools imported by runners" is not universally enforced.

## 3.2 Provenance and hash-chain completeness

**Strengths now**
- Repo manifest/tree hash and per-run receipts exist.
- Row hashes in SQLite provide row integrity signals.

**Gaps**
- No mandatory artifact-level hash manifest per run covering every emitted figure/log/schema/spec used.
- No explicit chain linking proposal → prereg → approval → prediction envelope → run outputs → contradiction report.
- Receipt presence checks are implemented in some runners, not uniformly enforced across all domains.

## 3.3 Preregistration, approval, contradiction automation completeness

**Strengths now**
- Approval DB + script-scoped HMAC check are robust.
- Contradiction artifacts exist in multiple domains.
- Approval enforcement is SQLite-backed and integrated with runtime policy checks.

**Gaps**
- Contradiction report schema and publication routing are not standardized across all domains.
- Approval/prereg requirements still partially optional or bypassable per runner/policy flags.
- Prediction envelope as a required pre-run artifact is not uniformly explicit.
- "Parameters and test inputs must come only from prereg/spec" is not yet universally hard-enforced.

## 3.4 Reference-only canon (anchor-only values/math) in code

**Strengths now**
- Canon standards documents and anchor references are widespread.

**Gaps**
- Thresholds/constants are still frequently duplicated in executable code.
- No universal loader/registry forcing numeric retrieval from canonical anchor-indexed sources.
- CI lacks a strict “no duplicated canon constants/equations in code” gate.

## 4) Target State: Standards-Governed Hexagonal Falsification Architecture

Target architecture (SGHFA) for VDM falsification package:

1. **Proposal-driven workflow mandatory**: no run without ProposalDocument + prereg + approval artifact + prediction envelope.
2. **Hexagonal domain core** with explicit ports/contracts:
   - PredictorPort
   - ApprovalPort
   - ValidationGatePort
   - ProvenancePort
   - ContradictionReporterPort
   - ArtifactRegistryPort
3. **Canonical anchor registry as executable dependency**:
   - all equations/constants/thresholds resolved by anchor IDs from canonical registries.
4. **End-to-end provenance chain**:
   - hash-linked artifact graph from proposal to final results.
5. **Automated contradiction handling**:
   - schema-bound contradiction reports, quarantine routing, and machine-readable public index.
6. **Governance hard gates**:
   - import-boundary checks, file-size policy, coverage floor, schema validation, provenance completeness checks in CI.

## 5) Delta / Migration Plan (Current → Target)

1. **Introduce explicit contracts package**
   - Add domain contracts for ProposalDocument, ApprovalArtifact, PredictionEnvelope, GateEvaluation, ContradictionReport, ProvenanceReceipt, ArtifactManifest.

2. **Create canonical-anchor resolver service**
   - Central service to load constants/equations/thresholds by anchor IDs from `Derivation/z.CANONICAL_*`.
   - Deprecate hard-coded duplicate thresholds in runners.

3. **Standardize pre-run pipeline orchestration**
   - Single orchestration flow: proposal → prereg → approval → prediction envelope → run.
   - Enforce universal use via a shared execution pipeline adapter.
   - Forbid direct parameter overrides except those explicitly declared in prereg/spec contracts.

4. **Unify validation gate registry**
   - Register every gate with gate-id, canon anchors, schema, and pass criteria.
   - Require runner gate calls through registry-backed interfaces only.
   - Require gate implementation in helper modules, not inline in runners.

5. **Implement artifact hash manifest + hash-chain**
   - Per-run artifact manifest including SHA-256 for all inputs/outputs.
   - Parent hash pointer ties each stage artifact to predecessor.

6. **Normalize contradiction reporting**
   - Single contradiction JSON schema + required publication location/index.
   - Mandatory contradiction artifact on any gate/provenance failure.
   - Artifact rendering/serialization logic must be helper-driven and imported by runner entrypoints.

7. **Strengthen CI governance**
   - Add architecture import-lint.
   - Add file-size check (<500 LOC target policy for new/refactored files).
   - Add coverage checks (unit/contract/e2e target ≥85%).
   - Add canon-link/static-threshold duplication scanner.

8. **Backfill legacy domains incrementally**
   - Migrate highest-activity domains first (`metriplectic`, `cosmology`, `thermo_routing`), then remaining domains.

## 6) Consequences

## Positive
- Stronger scientific rigor and replayability.
- Better falsification integrity (explicit prediction-before-run contract).
- Higher trust via complete provenance and contradiction transparency.
- Easier contributor onboarding through stable contracts and architecture boundaries.

## Costs / Risks
- Upfront refactor and migration cost across many legacy runners.
- Additional CI strictness may temporarily increase failed builds until legacy compliance is reached.
- Contributor workflow becomes more formal and less permissive.

## New constraints imposed
- No execution without prereg + approval + prediction envelope.
- No direct hard-coded canon values in runner logic.
- No unregistered gate logic in production runs.
- No artifact without hash/provenance receipt registration.
