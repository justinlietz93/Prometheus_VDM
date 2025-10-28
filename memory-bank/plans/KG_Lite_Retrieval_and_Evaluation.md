# KG‑Lite Retrieval Policy and Evaluation Protocol
Status: In Progress
Owner: Memory Graph (memory-bank/)
Scope Guard: Out of Nexus. No VDM_Nexus code or policy changes. This plan defines external-agent responsibilities only.

Purpose
- Relocate and formalize any notions of:
  - PathRAG retrieval policy
  - Signal schema ownership
  - MCP writebacks (if any)
  - Evaluation protocol for retrieval outputs
- Ensure all of the above live under memory-bank/ per standards and are not implemented or referenced as Nexus responsibilities.

Canonical Standards and Anchors
- KG‑Lite envelopes and branches: [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:188)
- Determinism gates (chunk_id, content_sha256): [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:226)
- Retrieval policy branch semantics: [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:240)
- Allowed relation verbs: [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:85)
- Directory conventions (chunked datasets under MEMORY_GRAPH_CONTEXT): [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:265)
- Testing and validation (audit, lint, snapshots): [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:369)

Ownership and Boundaries
- Signal schema (e.g., vdm.nexus.signal.v1.schema.json) resides under memory-bank/ and is versioned with KG‑Lite datasets. Nexus does not define or validate signal schema beyond read-only display of artifacts.
- Retrieval policy (PathRAG) lives as a dataset branch under KG‑Lite retrieval_policy. Nexus must not implement retrievers or issue path queries; any exploration is performed by external tools that operate on KG‑Lite JSON.
- MCP writebacks (if any) are an external-agent concern. Nexus remains read-only and shall not perform graph writes or policy enforcement beyond its own informational gate.

Retrieval Policy (PathRAG) Parameters
- Parameters are stored in the retrieval_policy branch payload of the dataset and validated against the KG‑Lite schema:
  - path_prune_alpha ∈ [0,1] (default ~0.8)
  - path_threshold ∈ [0,1] (default ~0.2)
  - min_novelty ∈ [0,1] (default ~0.55)
- Reference: retrieval policy branch per [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:240)

Evaluation Protocol (Instrument-Level, T2)
- Objective: Provide a meter for retrieval quality over a fixed KG‑Lite snapshot. No novel claims; instrument only.
- Inputs:
  - A KG‑Lite dataset root with index + edges + signals + retrieval_policy
  - A curated set of (start_node_id, goal_node_id) queries with ground-truth or proxy labels
- Required Artifacts per run (append-only under memory-bank/):
  - 1 JSON log with configuration, seeds, commit hash, and summary metrics (indent=2, sort_keys=True)
  - 1 CSV log with per-query outputs (csv.DictWriter with header)
  - ≥1 PNG figure (e.g., score distributions, precision–recall-like curves)
- Metrics (report only; no project-wide gates implied here):
  - Path success rate given threshold
  - Score calibration diagnostics (e.g., reliability plot vs human-weak labels)
  - Sensitivity to path_prune_alpha and min_novelty (sweeps)
- Validation discipline:
  - Lint all JSON against schemas (if provided); reject invalid writes
  - Emit audit lines with sha256 of payloads; snapshot results to memory-bank/graph/snapshots/ per [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:369)

Signal Schema (Reference Location)
- Schema lives under memory-bank/MEMORY_GRAPH_CONTEXT/schemas/ and is referenced from dataset envelopes. Example anchor (if present):
  - [vdm.nexus.signal.v1.schema.json](memory-bank/MEMORY_GRAPH_CONTEXT/schemas/vdm.nexus.signal.v1.schema.json:1)
- Signals should include fields to support policy mapping as exemplified in standards: text/probe/acceptance_test/source per [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:238)

MCP Integration Policy
- If external agents expose MCP tools for CRUD operations:
  - Use only create_entities/create_relations/add_observations consistent with [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:329)
  - All writes must be mirrored to disk KG‑Lite envelopes and pass determinism gates; MCP is an overlay, not the source of truth
  - Audit every batch write to memory-bank/logs with sha256 of payload

Provenance and Determinism
- Always compute content_sha256 over canonical JSON (UTF‑8, sorted keys) and verify chunk_id construction per [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:226)
- Use timezone-aware UTC timestamps (ISO‑8601 Z)

Separation From Nexus (Non-Negotiable)
- VDM_Nexus shall not:
  - auto-inject thresholds into UI from memory graph
  - ship or validate signal schemas
  - perform MCP writebacks or graph mutations
  - implement evaluation protocol code or invoke PathRAG retrievers
- Any mention of these responsibilities in Nexus docs is historical and must be considered superseded by this plan.

Execution Checklist
- [ ] Create or verify KG‑Lite retrieval_policy schema under memory-bank/MEMORY_GRAPH_CONTEXT/schemas/
- [ ] Provide example dataset with retrieval_policy branch and signals/edges (index enumerates counts)
- [ ] Implement instrument: memory-bank/tools/retrieval_eval.py (warn-only; no external claims)
- [ ] Emit JSON/CSV/PNG artifacts under memory-bank/ with audit lines and snapshots
- [ ] Document dataset-level acceptance in memory-bank/logs and update memory-bank/progress.md with a brief run summary

References
- Standards: [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md:188)
- Dataset index exemplar: [nexus-sessions.index.json](memory-bank/MEMORY_GRAPH_CONTEXT/nexus-sessions/nexus-sessions.index.json:1)