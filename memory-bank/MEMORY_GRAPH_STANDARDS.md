# MEMORY GRAPH STANDARDS

Version: v1.1 (2025-10-27)
Owner: VDM Nexus
Location: [MEMORY_GRAPH_STANDARDS.md](memory-bank/MEMORY_GRAPH_STANDARDS.md)

## Purpose

- Define strict, interoperable conventions for a project memory knowledge graph so any agent can integrate quickly and safely.
- Standardize ontology, IDs, fields, provenance, trust/tiers, update rules, and query patterns.
- Canon discipline: do not duplicate Derivation; link by anchors such as [VDM-E-###](Derivation/EQUATIONS.md#vdm-e-###).

## Scope

- Applies to all agents/tools writing to or reading from memory-bank/ and the MCP Memory Graph.
- Covers entity/relation schemas, allowed types, field semantics, versioning, security, and query cookbook.

## Non-goals

- Not a data lake; no large binaries. Store pointers and provenance, not bulky artifacts.
- Not a free-text dump; normalize fields to make graph queries fast and deterministic.

---

## 1. Ontology

### 1.1 Node (Entity)

Minimal required fields:

```json
{
  "id": "ulid:01JCS4D2V9G1T9KE3VF1H2Y8XK",
  "type": "Result",
  "name": "KG dispersion R² check",
  "summary": "Fit on J-only KG satisfied R²≥0.999 and v≤1.02c.",
  "labels": ["metriplectic","kg","gate","physics"],
  "source": {
    "uri": "Derivation/code/physics/metriplectic/run_kg_dispersion.py",
    "commit": "e47475d45d2f7a5f29bbabb62ded7ee6cad8f00f",
    "path": "Derivation/code/physics/metriplectic/run_kg_dispersion.py",
    "line": 1
  },
  "provenance": {
    "created_utc": "2025-10-27T17:20:00Z",
    "updated_utc": "2025-10-27T17:20:00Z",
    "author": "agent:nexus",
    "approval": "unreviewed"
  },
  "tier": "T2",
  "trust": 0.85,
  "visibility": "internal",
  "expires_utc": null,
  "emb": null
}
```

Field rules:

- id: ULID lower-case string prefixed with "ulid:". Deterministic alias allowed: "hash:sha256:...".
- type: one of the Allowed Types (see 1.3).
- name: short human title (≤120 chars).
- summary: one-paragraph summary; no multi-MB content; link to files instead.
- labels: snake_case or kebab-case; reuse controlled vocabulary.
- source: file-level pointer; include path and optional line.
- provenance: ISO-8601 Z timestamps; author as "agent:<name>" or "user:<name>".
- tier: one of T0–T9 (see Derivation/TIER_STANDARDS.md).
- trust: 0.0–1.0 scalar; initialize from tier and approvals.
- visibility: public | internal | restricted.
- emb: optional embedding vector metadata; stored separately by key if large.

### 1.2 Edge (Relation)

```json
{
  "from": "ulid:01JCS4D2V9G1T9KE3VF1H2Y8XK",
  "to":   "ulid:01JCS4E5KZ7H1PM4X7D4Q4S5NV",
  "rel":  "validates",
  "weight": 0.9,
  "temporal": {"since": "2025-10-27T17:21:00Z"},
  "notes": "Gate R²≥0.999 satisfied on 3 grids."
}
```

Allowed relation verbs (active voice):

- derives_from, depends_on, validates, measures, supports, contradicts, supersedes, implements,
- proposes, results_in, observes, emits, has_artifact, authored_by, approved_by, located_in, links_to, mentions, version_of, owns.

Semantics:

- rel is lower_snake_case verb.
- weight is optional [0,1].
- temporal.since/until as ISO-8601 Z; optional.

### 1.3 Allowed Entity Types

- Project, Task, ChecklistItem, Proposal, Result, Instrument, Dataset, Run, Artifact,
- Gate, Metric, Claim, Hypothesis, Person, Organization, Tool, Script, File, Mode,
- Decision, Pattern, Context, Policy, Approval, Standard.

---

## 2. Identification and namespacing

- Primary IDs: ULID (base32 crockford) with prefix "ulid:".
- Deterministic alias: "hash:sha256:<hex>" from stable JSON canonicalization of minimal fields.
- Namespaces: use labels to scope (e.g., "vdm", "nexus", "derivation").
- External URIs: store under source.uri; prefer repo-relative paths.

---

## 3. Canon discipline

- Never duplicate canon; link by anchors, e.g. [VDM-E-101](Derivation/EQUATIONS.md#vdm-e-101).
- For equations/constants/units, reference:
  - [SYMBOLS.md](Derivation/SYMBOLS.md)
  - [EQUATIONS.md](Derivation/EQUATIONS.md)
  - [CONSTANTS.md](Derivation/CONSTANTS.md)
  - [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)

---

## 4. Provenance and versioning

- Every write updates provenance.updated_utc.
- Keep append-only audit in memory-bank/logs/memory_audit.jsonl (one JSON per line).
- Approval status: unreviewed | approved | quarantined.
- Quarantine when any referenced gate fails.

---

## 5. Trust, tiers, and priority

- trust ∈ [0,1]; initialize from tier mapping: T0→0.1, T2→0.6, T6→0.85, T9→0.99 (example).
- recency half-life (days): default 30; compute recency = exp(-Δt/hl).
- priority_score = 0.5*trust + 0.3*recency + 0.2*relevancy(tag overlap).

---

## 6. Fields schema (JSON Schema excerpts)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "Entity": {
      "type": "object",
      "required": ["id","type","name","summary","labels","source","provenance","tier","trust","visibility"],
      "properties": {
        "id": {"type":"string","pattern":"^(ulid|hash):"},
        "type": {"type":"string"},
        "name": {"type":"string","maxLength": 200},
        "summary": {"type":"string","maxLength": 2000},
        "labels": {"type":"array","items":{"type":"string"}},
        "source": {
          "type":"object",
          "properties":{"uri":{"type":"string"},"commit":{"type":"string"},"path":{"type":"string"},"line":{"type":"integer"}}
        },
        "provenance": {
          "type":"object",
          "properties":{"created_utc":{"type":"string"},"updated_utc":{"type":"string"},"author":{"type":"string"},"approval":{"type":"string"}}
        },
        "tier": {"type":"string"},
        "trust": {"type":"number","minimum":0.0,"maximum":1.0},
        "visibility": {"type":"string","enum":["public","internal","restricted"]},
        "emb": {"type":["object","null"]}
      }
    },
    "Relation": {
      "type":"object",
      "required":["from","to","rel"],
      "properties":{
        "from":{"type":"string"},
        "to":{"type":"string"},
        "rel":{"type":"string"},
        "weight":{"type":"number","minimum":0.0,"maximum":1.0},
        "temporal":{"type":"object"},
        "notes":{"type":"string","maxLength": 1000}
      }
    }
  }
}
```

---

## 6A. KG‑Lite chunk envelope and branching

Adopt a typed, deterministic chunk envelope to store graph branches explicitly, per the KG‑Lite approach in [kg-lite_Convo.md](memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite_Convo.md:11) with exemplars in [memory-graph-2025-09-25_optimized.md](memory-bank/MEMORY_GRAPH_CONTEXT/memory-graph-2025-09-25_optimized.md:135) and [memory-graph-2025-09-25_faithful.md](memory-bank/MEMORY_GRAPH_CONTEXT/memory-graph-2025-09-25_faithful.md:10).

Schema excerpt (additive to §6):

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "definitions": {
    "ChunkEnvelope": {
      "type": "object",
      "required": ["set_id","set_version","chunk_type","chunk_id","updated","source","content_sha256","part","total_parts","payload"],
      "properties": {
        "set_id": {"type":"string","maxLength":120},
        "set_version": {"type":"string"},
        "chunk_type": {
          "type":"string",
          "enum":["index","meta","axes_dimensions","subfactors","signals","edges","retrieval_policy"]
        },
        "chunk_id": {
          "type":"string",
          "pattern":"^[^@]+@[^:]+:(index|meta|axes_dimensions|subfactors|signals|edges|retrieval_policy)$"
        },
        "scope": {"type":"string"},
        "updated": {"type":"string"},
        "source": {"type":"string"},
        "content_sha256": {"type":"string","pattern":"^[0-9a-f]{64}$"},
        "part": {"type":"integer","minimum":1},
        "total_parts": {"type":"integer","minimum":1},
        "tags": {"type":"array","items":{"type":"string"}},
        "payload": {"type":"object"}
      }
    }
  }
}
```

Determinism gates:

- content_sha256 equals SHA256 of canonical JSON for payload (UTF‑8, sort_keys=true). Reject writes on mismatch.
- chunk_id must equal "${set_id}@${set_version}:${chunk_type}".
- Sharding: if serialized payload length exceeds ~12000 chars, split into parts with identical metadata except 'part'; require 1 ≤ part ≤ total_parts.

Branch semantics (closed set):

- index: manifest with 'chunks' and 'counts' for the dataset; see [memory-graph-2025-09-25_optimized.md](memory-bank/MEMORY_GRAPH_CONTEXT/memory-graph-2025-09-25_optimized.md:135).
- meta: dataset‑level metadata and notes; sege [memory-graph-2025-09-25_optimized.md](memory-bank/MEMORY_GRAPH_CONTEXT/memory-graph-2025-09-25_optimized.md:11).
- axes_dimensions: arrays 'axes' and 'dimensions'; see [memory-graph-2025-09-25_faithful.md](memory-bank/MEMORY_GRAPH_CONTEXT/memory-graph-2025-09-25_faithful.md:97).
- subfactors: array 'subfactors'; see [memory-graph-2025-09-25_faithful.md](memory-bank/MEMORY_GRAPH_CONTEXT/memory-graph-2025-09-25_faithful.md:122).
- signals: array 'signals' with fields including 'text','probe','acceptance_test' for policy mapping; see [justin-graph.json](memory-bank/MEMORY_GRAPH_CONTEXT/justin-graph.json:250).
- edges: 'edges' array plus 'relation_ontology' closed set; see [memory-graph-2025-09-25_faithful.md](memory-bank/MEMORY_GRAPH_CONTEXT/memory-graph-2025-09-25_faithful.md:188).
- retrieval_policy: optional parameters for path‑based retrieval (e.g., path_prune_alpha=0.8, path_threshold=0.2, min_novelty=0.55) per [kg-lite_Convo.md](memory-bank/MEMORY_GRAPH_CONTEXT/kg-lite_Convo.md:91).

Interoperability:

- Represent each ChunkEnvelope as an Entity of type "Artifact"; link from a dataset Entity (type "Project" or "Context") via rel="has_artifact".
- Use only the allowed relation verbs in §1.2; do not invent verbs inside chunk payloads.

## 7. Write policy

- Idempotent writes: treat same (name, source.path, line, type) as upsert on collision.
- Conflict resolution:
  - Prefer higher trust; else newer updated_utc; else longest summary.
- Batching: prefer small atomic batches (≤100 entities).
- No destructive deletes; mark visibility="restricted" + add relation rel="supersedes" from replacement.

---

## 8. Security and privacy

- visibility governs export; redact PII fields at export time.
- Restricted nodes must not leak via derived embeddings; store emb behind restricted key.
- Record author and approval consistently.

---

## 9. Directory conventions (memory-bank/)

- [productContext.md](memory-bank/productContext.md)
- [activeContext.md](memory-bank/activeContext.md)
- [systemPatterns.md](memory-bank/systemPatterns.md)
- [decisionLog.md](memory-bank/decisionLog.md)
- [progress.md](memory-bank/progress.md)
- Graph exports:
  - memory-bank/graph/memory_graph.jsonl (append-only)
  - memory-bank/graph/snapshots/YYYYMMDD_HHMMSS.json
- KG‑Lite datasets (chunked):
  - memory-bank/MEMORY_GRAPH_CONTEXT/{set_id}/chunks/*.json       ← individual [ChunkEnvelope](memory-bank/MEMORY_GRAPH_STANDARDS.md) files
  - memory-bank/MEMORY_GRAPH_CONTEXT/{set_id}/{set_id}.index.json ← dataset index envelope
- Flat KG‑Lite CRUD store (file‑backed; primary on‑disk truth):
  - Entities JSON: [memory-bank/MEMORY_GRAPH_CONTEXT/entities/kg-entities.v1.json](memory-bank/MEMORY_GRAPH_CONTEXT/entities/kg-entities.v1.json:1)
  - Relations JSON: [memory-bank/MEMORY_GRAPH_CONTEXT/relations/kg-relations.v1.json](memory-bank/MEMORY_GRAPH_CONTEXT/relations/kg-relations.v1.json:1)
  - PathRAG index JSON: [memory-bank/MEMORY_GRAPH_CONTEXT/indexes/kg-pathrag-index.v1.json](memory-bank/MEMORY_GRAPH_CONTEXT/indexes/kg-pathrag-index.v1.json:1)
  - Formatting: json.dump(..., indent=2, sort_keys=True); writes are idempotent (§7); no destructive deletes (§7).
- Audit log:
  - memory-bank/logs/memory_audit.jsonl

---

## 10. Query cookbook

Top-k by relevance:

```json
{"op":"topk","k":10,"where":{"labels":["metriplectic","gate"]},"order":"priority_score"}
```

Nearest neighbors to an anchor node:

```json
{"op":"nn","id":"ulid:...","k":15,"metric":"cosine","space":"emb.default"}
```

Find unapproved Results touching EQUATIONS:

```json
{"op":"find","where":{"type":"Result","provenance.approval":"unreviewed","source.path~":"Derivation/EQUATIONS.md"}}
```

Next actionable checklist items for VDM Nexus:

```json
{"op":"find","where":{"type":"ChecklistItem","labels":["nexus"],"status":"pending"},"order":"created_utc"}
```

KG‑Lite: list all available datasets (by index envelopes):

```json
{"op":"find","where":{"type":"Artifact","source.path":"memory-bank/MEMORY_GRAPH_CONTEXT/.+\\.index\\.json$"},"order":"provenance.created_utc"}
```

KG‑Lite: retrieve signals for a dataset (consumer expands payload):

```json
{"op":"open","where":{"type":"Artifact","labels":["kg-lite","signals"],"name":"justin-graph@1.0:signals"}}
```

## 11. Local KG‑Lite CRUD CLI and PathRAG (file‑backed)

- Purpose: Provide a minimal, deterministic, on‑disk knowledge graph interface that mirrors MCP Memory semantics while keeping the canonical store under memory‑bank/.
- Primary store: the flat files in §9 (“Flat KG‑Lite CRUD store”). MCP updates are optional; disk is authoritative.

Tooling:
- CLI: [kg_cli.py](memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py:1)
  - Determinism: json.dump with indent=2, sort_keys=True
  - Scope: never writes under Derivation/; confined to memory‑bank/
  - Allowed verbs: must use the relation ontology in §1.2 (closed set)

MCP → CLI mapping:
- create_entities → entities add
- create_relations → relations add
- delete_entities → entities delete
- delete_relations → relations delete
- read_graph/search_nodes → entities list --query …, relations list …, pathrag search

Examples (low verbosity by default; append --json for JSON):
- Add or upsert an entity:
  - python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py entities add --name VDM_Nexus_Approval_CLI --type ScriptTool --obs "Path: [approval_cli.py](VDM_Nexus/scripts/approval_cli.py:1)" --obs "Docs: [scripts/README.md](VDM_Nexus/scripts/README.md:41)" --upsert
- Add a relation:
  - python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py relations add --from VDM_Nexus_Approval_CLI --to Canonical_Approve_Tag_CLI --type wraps
- List entities by substring:
  - python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py entities list --query approval

PathRAG index:
- Build: python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py index build
- Search by path substring:
  - python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py pathrag search --path VDM_Nexus/scripts/approval_cli.py --json
- Index file: [kg-pathrag-index.v1.json](memory-bank/MEMORY_GRAPH_CONTEXT/indexes/kg-pathrag-index.v1.json:1)
- Extraction rule: parse Markdown links of the form [label](relative/path:line); normalize path; store segments; map back to entities referencing that path.

Policy:
- Idempotent writes and conflict rules per §7
- Security/privacy per §8
- Directory placement per §9
- KG‑Lite chunked datasets remain the interchange format (§6A); the flat CRUD store is for day‑to‑day authoring and retrieval.

Determinism audit of envelopes (pseudo-op; tool computes hash and compares to content_sha256):

```json
{"op":"audit_envelopes","where":{"type":"Artifact","labels":["kg-lite"]},"report":{"mismatches":true,"by_set":true}}
```

---

## 11. Agent integration contract

- Provide capabilities: create_entities, create_relations, add_observations (append-only), read_graph, open_nodes.
- All JSON writes must be compact and valid UTF-8; json.dump(..., indent=2, sort_keys=True).
- Include repo_head and tool version in an observation when performing bulk writes.
- Respect approval and quarantine policies from project standards.

---

## 12. Examples

Entity (ChecklistItem):

```json
{
  "id":"ulid:01JCS5B665AXN6B2N4A1D1D4QY",
  "type":"ChecklistItem",
  "name":"Phase 0 · Task 0.3.1 Static Policy Check",
  "summary":"Enforce zero writes to ../derivation from Nexus scope.",
  "labels":["nexus","policy","static-check"],
  "source":{"path":"VDM_Nexus/scripts/nexus_static_policy_check.py","line":1},
  "provenance":{"created_utc":"2025-10-27T17:22:00Z","updated_utc":"2025-10-27T17:22:00Z","author":"agent:nexus","approval":"approved"},
  "tier":"T2","trust":0.9,"visibility":"public"
}
```

Relation:

```json
{"from":"ulid:01JCS5B665AXN6B2N4A1D1D4QY","to":"ulid:01JCS5D8W3QK8G7HZ4V5F3S7MP","rel":"implements","weight":0.8}
```

Observation (append-only note):

```json
{"entity":"ulid:01JCS5B665AXN6B2N4A1D1D4QY","note":"Policy script merged at e47475d…; no violations in Nexus/."}
```

---

## 13. Testing and validation

- Lint JSON exports with schema above; reject on validation errors.
- Each batch write must be accompanied by an audit line containing counts and sha256 of payload.
- Periodically snapshot graph to memory-bank/graph/snapshots/.

---

## 14. Change control

- Changes to this standard require a ChecklistItem and an Approval entity.
- Update version header and add a changelog entry.

---

## 15. Changelog

- v1.1 (2025-10-27): Add KG‑Lite chunk envelope and branching model; determinism gates; retrieval_policy hook; directory and query updates.
- v1.0 (2025-10-27): Initial standard (ontology, schemas, policies, queries).
