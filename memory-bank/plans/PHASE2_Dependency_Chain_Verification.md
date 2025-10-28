# Phase 2 Plan — Canonical Dependency-Chain Verification (Outside Nexus Scope)

Status: In Progress  
Owner: VDM Core  
Scope guard: No code or policy added under VDM_Nexus/. This plan lives in memory-bank/ and proposes tools under tools/ with CI-only enforcement.

Intent:
- Move from attestation-only (“Dependency-Chain-Reviewed: true”) to automated verification that canon dependencies were reviewed/updated coherently when tracked Derivation/ changes occur.

Out of Scope:
- VDM_Nexus runtime or scripts changing Derivation/. Nexus remains read-only and unaffected by this plan.
- Any alterations to canon numerical content or physics claims herein. This is a process/instrumentation plan.

Key Canon Inputs (read-only):
- Canon map and registries:
  - [CANON_MAP.md](../../Derivation/CANON_MAP.md:1)
  - [EQUATIONS.md](../../Derivation/EQUATIONS.md:1)
  - [VALIDATION_METRICS.md](../../Derivation/VALIDATION_METRICS.md:1)
  - [ROADMAP.md](../../Derivation/ROADMAP.md:1)
  - [SCHEMAS.md](../../Derivation/SCHEMAS.md:1)
  - [SYMBOLS.md](../../Derivation/SYMBOLS.md:1)
  - [UNITS_NORMALIZATION.md](../../Derivation/UNITS_NORMALIZATION.md:1)
  - [OPEN_QUESTIONS.md](../../Derivation/OPEN_QUESTIONS.md:1)
  - [ALGORITHMS.md](../../Derivation/ALGORITHMS.md:1)
  - [CANON_PROGRESS.md](../../Derivation/CANON_PROGRESS.md:1)
- Attestation log:
  - [CHRONICLES.md](../../Derivation/CHRONICLES.md:1)

Policy Baseline (Phase 1 in effect now)
- Enforced by [precommit_derivation_guard.py](../../VDM_Nexus/scripts/precommit_derivation_guard.py:1) with test coverage in [test_precommit_derivation_guard.py](../../VDM_Nexus/scripts/tests/test_precommit_derivation_guard.py:1):
  - If any tracked Derivation/ change, [CHRONICLES.md](../../Derivation/CHRONICLES.md:1) must be in the diff.
  - If change is canon-impacting (heuristic), at least one ALL-CAPS doc must be updated and CHRONICLES contain “Dependency-Chain-Reviewed: true”.

Phase 2 Objective
- Replace the single-line attestation with an automated dependency-chain verification instrument that:
  1) Extracts the dependency graph from [CANON_MAP.md](../../Derivation/CANON_MAP.md:1) (and optionally doc-crosslinks).
  2) Computes changed canon nodes vs base (git diff).
  3) Ensures for each changed node, all required dependent/antecedent nodes are either updated or explicitly acknowledged in CHRONICLES with rationale anchors.
  4) Emits a machine-readable JSON report and a human summary.
  5) Gate mode: warn-only initially (like the Nexus gate), then elevate (CI error) after a burn-in period.

Proposed Artifacts (to be created in Phase 2)
- Validator CLI (repo root tools/, read-only to Derivation/):
  - [canon_chain_validator.py](../../tools/canon_chain_validator.py:1)
- CI integration (warn-only initially):
  - [.github/workflows/canon-chain-guard.yml](../../.github/workflows/canon-chain-guard.yml:1)
- JSON schema for validator output:
  - [canon-chain-report.schema.json](../../tools/schemas/canon-chain-report.schema.json:1)
- Unit tests:
  - [test_canon_chain_validator.py](../../tools/tests/test_canon_chain_validator.py:1)

Functional Requirements
1) Deterministic graph extraction
   - Parse [CANON_MAP.md](../../Derivation/CANON_MAP.md:1) into a directed graph G=(V,E).
   - Accept supplemental edges from explicit anchors among ALL-CAPS docs (e.g., “[VDM-E-###]” links in [EQUATIONS.md](../../Derivation/EQUATIONS.md:1); do not duplicate canon content; only link-count/edge inference).
   - Graph and node IDs: POSIX paths as primary keys; allow anchors (e.g., EQUATIONS.md#vdm-e-###) as sub-nodes for fine-grain mapping.

2) Diff ingestion
   - Input base ref (default origin/main), compute changed files under Derivation/ (mirror logic of [nexus_validate_gate.py](../../VDM_Nexus/scripts/nexus_validate_gate.py:104) and [precommit_derivation_guard.py](../../VDM_Nexus/scripts/precommit_derivation_guard.py:146) exclusions).
   - Classify changes as canon-impacting via rules aligned with [precommit_derivation_guard.py](../../VDM_Nexus/scripts/precommit_derivation_guard.py:81).

3) Chain completeness policy
   - For each changed canon node u, compute A(u) = {ancestors and/or descendants as per CANON_MAP semantics}.
   - Policy options (configurable):
     - “ancestors-only”: ensure all prerequisite docs touched or acknowledged.
     - “descendants-only”: ensure all dependents reconciled or acknowledged.
     - “bidirectional”: require both.
   - Acknowledgement path: if not updated, CHRONICLES must include minimal structured entry with anchors to nodes u and A(u).

4) Output and audit
   - Emit JSON to memory-bank/graph/snapshots/ and memory-bank/logs (append), complying with memory-bank standards:
     - JSON: json.dump(..., indent=2, sort_keys=True)
     - Include repo_head, base_ref, counts, sha256(payload) for audit line.
   - Human-readable summary to stdout.

5) Modes
   - warn-only (default, non-fatal in CI)
   - enforce (exit 1 if violations)

CLI Design (proposed)
- [canon_chain_validator.py](../../tools/canon_chain_validator.py:1)

Usage:
- python tools/canon_chain_validator.py --base origin/main --policy ancestors-only --json --ack-from Derivation/CHRONICLES.md

Flags:
- --base: base ref to diff against (default origin/main)
- --policy: ancestors-only|descendants-only|bidirectional (default ancestors-only)
- --json: print JSON report (also saves to memory-bank/logs/)
- --ack-from: path to CHRONICLES acknowledgment file
- --map-path: override CANON_MAP path (default Derivation/CANON_MAP.md)
- --warn-only: do not exit nonzero on violations
- --exclusion: glob exclusion, repeatable (mirrors defaults in [nexus_validate_gate.py](../../VDM_Nexus/scripts/nexus_validate_gate.py:53))

JSON Report (sketch)
- [canon-chain-report.schema.json](../../tools/schemas/canon-chain-report.schema.json:1)

{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["repo_head","base_ref","policy","changed","violations","graph_sha256","time_utc"],
  "properties": {
    "repo_head": {"type": "string"},
    "base_ref": {"type": "string"},
    "policy": {"type": "string"},
    "changed": {"type": "array","items":{"type":"string"}},
    "violations": {
      "type": "array",
      "items": {
        "type":"object",
        "required":["node","missing_updates","acknowledgements"],
        "properties":{
          "node":{"type":"string"},
          "missing_updates":{"type":"array","items":{"type":"string"}},
          "acknowledgements":{"type":"array","items":{"type":"string"}}
        }
      }
    },
    "graph_sha256": {"type":"string"},
    "time_utc": {"type":"string"}
  }
}

Heuristics and Semantics
- Node set: ALL-CAPS documents are always nodes; additional nodes may be inferred from section-level anchors (optional Phase 2.1).
- Edge semantics: derived strictly from [CANON_MAP.md](../../Derivation/CANON_MAP.md:1); any implicit inference must be conservative.
- Exclusions: mirror [nexus gate](../../VDM_Nexus/scripts/nexus_validate_gate.py:53) and guard.
- Chronicle acknowledgement format (minimally structured) within [CHRONICLES.md](../../Derivation/CHRONICLES.md:1):
  - Acknowledge: {changed: [paths], reviewed: [paths], rationale: "...", date: ISO-8601Z}

Validation Strategy (T2 Instrument)
- Unit tests in [test_canon_chain_validator.py](../../tools/tests/test_canon_chain_validator.py:1)
  - Case 1: Changed EQUATIONS.md; missing review of VALIDATION_METRICS.md (policy ancestors-only) → violation
  - Case 2: Changed run_*.py affecting schemas; CHRONICLES acknowledges dependent docs → pass (warn-only mode should still report)
  - Case 3: Only reference-only paths changed → pass
  - Case 4: Bidirectional policy with mixed acknowledgements → targeted violations
- CI job [.github/workflows/canon-chain-guard.yml](../../.github/workflows/canon-chain-guard.yml:1)
  - Warn-only mode for initial rollout; prints formatted JSON.
  - After burn-in and zero false positives over N merges, flip to enforced.

Operational Notes
- No writes under Derivation/ by validator; it only reads and emits reports under memory-bank/.
- Determinism: Use UTF-8, sorted keys, stable graph serialization for hashing.
- Time: use timezone-aware UTC (datetime.now(timezone.utc).isoformat()) to avoid deprecation.

Roadmap
- Phase 2.0 (this document): Plan and scaffolding; add CLI, schema, tests, CI (warn-only).
- Phase 2.1: Section-level anchors graph; finer granularity with anchors in ALL-CAPS docs.
- Phase 2.2: Elevate to enforce mode after governance approval (Justin K. Lietz).

References
- Guard (enforced): [precommit_derivation_guard.py](../../VDM_Nexus/scripts/precommit_derivation_guard.py:1)
- Gate (warn-only): [nexus_validate_gate.py](../../VDM_Nexus/scripts/nexus_validate_gate.py:1)
- Standards (memory-bank): [MEMORY_GRAPH_STANDARDS.md](../MEMORY_GRAPH_STANDARDS.md:188)

Checklist (Phase 2 tasks)
- [ ] Create validator CLI [canon_chain_validator.py](../../tools/canon_chain_validator.py:1)
- [ ] Implement CANON_MAP parser; emit graph JSON with sha256
- [ ] Implement diff ingestion; exclusions parity with gate/guard
- [ ] Implement chain policy checks (ancestors-only default)
- [ ] Emit JSON report validated against [canon-chain-report.schema.json](../../tools/schemas/canon-chain-report.schema.json:1)
- [ ] Add tests [test_canon_chain_validator.py](../../tools/tests/test_canon_chain_validator.py:1)
- [ ] Add CI workflow [.github/workflows/canon-chain-guard.yml](../../.github/workflows/canon-chain-guard.yml:1) warn-only
- [ ] Governance review to schedule enforcement elevation