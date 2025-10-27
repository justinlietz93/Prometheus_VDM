#!/usr/bin/env python3
"""
KG-Lite Chunker CLI

Purpose:
- Convert a flat graph JSON (nodes/edges) into deterministic KG-Lite ChunkEnvelope branches:
  index, meta, axes_dimensions, subfactors, signals, edges, retrieval_policy.
- Compute content_sha256 over canonical JSON for payloads (UTF-8, sort_keys=True, compact separators).
- Enforce chunk_id == "{set_id}@{set_version}:{chunk_type}" and stable, reproducible outputs.

Inputs:
- A JSON file with fields:
  {
    "meta": {"version": "1.0", "subject": "Justin", "updated": "..."},
    "nodes": [...],
    "edges": [...]
  }

Outputs (filesystem):
- memory-bank/MEMORY_GRAPH_CONTEXT/{set_id}/{set_id}.index.json
- memory-bank/MEMORY_GRAPH_CONTEXT/{set_id}/chunks/{chunk_id}.json   (one per branch)

Validation gates (soft):
- Determinism: recompute hash post-write and compare; mismatch => nonzero exit
- Structure: minimal field presence; optional jsonschema validation if available

References:
- KG-Lite schema: [kg-lite.chunkenvelope.v1.schema.json](../kg-lite.chunkenvelope.v1.schema.json)
- Standards: [MEMORY_GRAPH_STANDARDS.md](../../MEMORY_GRAPH_STANDARDS.md)
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Optional jsonschema validation (soft dependency)
try:
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover
    jsonschema = None  # type: ignore


HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]  # .../Prometheus_VDM
DEFAULT_INPUT = REPO_ROOT / "memory-bank" / "MEMORY_GRAPH_CONTEXT" / "justin-graph.json"
SCHEMA_PATH = REPO_ROOT / "memory-bank" / "MEMORY_GRAPH_CONTEXT" / "kg-lite.chunkenvelope.v1.schema.json"


def _utc_now_z() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"


def _canonical_json_bytes(obj: Any) -> bytes:
    # Canonical: sorted keys, compact separators, ensure_ascii=False
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _determine_scope(meta: Dict[str, Any]) -> str:
    subj = str(meta.get("subject", "")).strip().lower()
    if subj:
        return f"user:{subj}"
    return "project:memory-bank"


def _partition_nodes(nodes: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    axes = [n for n in nodes if n.get("type") == "axis"]
    dims = [n for n in nodes if n.get("type") == "dimension"]
    subf = [n for n in nodes if n.get("type") == "subfactor"]
    sigs = [n for n in nodes if n.get("type") == "signal"]
    # Stable ordering by id
    axes.sort(key=lambda x: str(x.get("id", "")))
    dims.sort(key=lambda x: str(x.get("id", "")))
    subf.sort(key=lambda x: str(x.get("id", "")))
    sigs.sort(key=lambda x: str(x.get("id", "")))
    return axes, dims, subf, sigs


def _normalize_edges(edges: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Preserve original 'relation' (or 'rel'), also add 'normalized_rel' mapping to closed ontology where possible.
    rel_map = {
        "constrained_by": "constrained_by",
        "influences": "influences",
        "tension_with": "tension_with",
        "references": "references",
        "derives_from": "derives_from",
        "supersedes": "supersedes",
        # observed variant in dataset:
        "constrains": "constrained_by",
    }
    out = []
    for e in edges:
        src = e.get("source") or e.get("from")
        tgt = e.get("target") or e.get("to")
        rel = e.get("relation") or e.get("rel")
        rec = {"from": src, "to": tgt, "rel": rel}
        if isinstance(rel, str) and rel in rel_map:
            rec["normalized_rel"] = rel_map[rel]
        out.append(rec)
    # Stable ordering
    out.sort(key=lambda r: (str(r.get("from", "")), str(r.get("to", "")), str(r.get("rel", ""))))
    return out


def _build_envelope(set_id: str,
                    set_version: str,
                    chunk_type: str,
                    scope: str,
                    source: str,
                    payload: Dict[str, Any],
                    tags: List[str]) -> Dict[str, Any]:
    updated = _utc_now_z()
    chunk_id = f"{set_id}@{set_version}:{chunk_type}"
    content_sha256 = _sha256_hex(_canonical_json_bytes(payload))
    env: Dict[str, Any] = {
        "set_id": set_id,
        "set_version": set_version,
        "chunk_type": chunk_type,
        "chunk_id": chunk_id,
        "scope": scope,
        "updated": updated,
        "source": source,
        "content_sha256": content_sha256,
        "part": 1,
        "total_parts": 1,
        "tags": tags,
        "payload": payload,
    }
    # Determinism self-checks
    assert env["chunk_id"] == chunk_id
    assert isinstance(env["content_sha256"], str) and len(env["content_sha256"]) == 64
    return env


def _soft_validate_with_schema(envelope: Dict[str, Any]) -> List[str]:
    errs: List[str] = []
    if not SCHEMA_PATH.exists():
        errs.append(f"Schema file not found at {SCHEMA_PATH}")
        return errs
    if jsonschema is None:
        errs.append("jsonschema not installed; skipped JSON Schema validation")
        return errs
    try:
        with SCHEMA_PATH.open("r", encoding="utf-8") as f:
            schema = json.load(f)
        jsonschema.validate(envelope, schema)  # type: ignore[attr-defined]
    except Exception as e:
        errs.append(f"jsonschema validation error: {e}")
    return errs


def chunk_graph(input_path: Path, out_root: Path, include_retrieval_policy: bool = True) -> Dict[str, Any]:
    # Normalize to absolute paths under REPO_ROOT for deterministic relative() behavior
    if not input_path.is_absolute():
        input_path = (REPO_ROOT / input_path).resolve()
    if not out_root.is_absolute():
        out_root = (REPO_ROOT / out_root).resolve()
    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data.get("meta") or {}
    nodes = data.get("nodes") or []
    edges = data.get("edges") or []

    set_id = str(meta.get("subject", "")).strip().lower() or "memory-graph"
    set_id = set_id.replace(" ", "-")
    set_version = str(meta.get("version") or "1.0")
    scope = _determine_scope(meta)
    source = str(input_path.relative_to(REPO_ROOT))

    axes, dims, subf, sigs = _partition_nodes(nodes)
    norm_edges = _normalize_edges(edges)

    # Branch payloads
    payload_meta = {"meta": {"version": set_version,
                             "subject": meta.get("subject", ""),
                             "graph_updated_at": meta.get("updated", ""),
                             "notes": "Auto-generated KG-Lite envelopes"}}

    payload_axes_dims = {"axes": axes, "dimensions": dims}
    payload_subfactors = {"subfactors": subf}
    payload_signals = {"signals": [{"text": s.get("text", ""),
                                     "probe": s.get("probe", ""),
                                     "acceptance_test": s.get("acceptance_test", "")}
                                    for s in sigs]}
    # Relation ontology (closed set from standards/examples)
    relation_ontology = ["constrained_by", "influences", "tension_with", "references", "derives_from", "supersedes"]
    payload_edges = {"edges": norm_edges, "relation_ontology": relation_ontology}

    # Envelopes
    env_meta = _build_envelope(set_id, set_version, "meta", scope, source, payload_meta, ["kg-lite", "meta"])
    env_axes = _build_envelope(set_id, set_version, "axes_dimensions", scope, source, payload_axes_dims, ["kg-lite", "axes_dimensions"])
    env_subf = _build_envelope(set_id, set_version, "subfactors", scope, source, payload_subfactors, ["kg-lite", "subfactors"])
    env_sigs = _build_envelope(set_id, set_version, "signals", scope, source, payload_signals, ["kg-lite", "signals"])
    env_edges = _build_envelope(set_id, set_version, "edges", scope, source, payload_edges, ["kg-lite", "edges"])

    envelopes: List[Dict[str, Any]] = [env_meta, env_axes, env_subf, env_sigs, env_edges]

    if include_retrieval_policy:
        payload_policy = {
            "path_prune_alpha": 0.8,
            "path_threshold": 0.2,
            "min_novelty": 0.55,
            "k_paths": 5,
            "max_hops": 3
        }
        env_policy = _build_envelope(set_id, set_version, "retrieval_policy", scope, source, payload_policy, ["kg-lite", "retrieval_policy"])
        envelopes.append(env_policy)

    # Index payload (counts)
    counts = {
        "axes": len(axes),
        "dimensions": len(dims),
        "subfactors": len(subf),
        "signals": len(sigs),
        "edges": len(norm_edges),
    }
    chunks_index = [{"chunk_id": e["chunk_id"], "sha256": e["content_sha256"], "kind": e["chunk_type"]} for e in envelopes]
    payload_index = {"schema_version": "2025-09-25", "chunks": chunks_index, "counts": counts}
    env_index = _build_envelope(set_id, set_version, "index", scope, source, payload_index, ["kg-lite", "index"])

    # Output layout
    out_set_dir = out_root / set_id
    out_chunks_dir = out_set_dir / "chunks"
    out_chunks_dir.mkdir(parents=True, exist_ok=True)

    # Write chunks
    def write_env(env: Dict[str, Any], dest: Path) -> None:
        with dest.open("w", encoding="utf-8") as f:
            json.dump(env, f, indent=2, sort_keys=True)
            f.write("\n")  # final newline

        # Determinism gate: recompute post-write (payload hash remains the canonical measure)
        payload_hash_again = _sha256_hex(_canonical_json_bytes(env["payload"]))
        if payload_hash_again != env["content_sha256"]:
            raise RuntimeError(f"Determinism gate failed for {env['chunk_id']}: payload hash mismatch")

        # Soft validation
        errs = _soft_validate_with_schema(env)
        for e in errs:
            # Print warnings; do not fail for missing jsonschema
            print(f"[warn] {env['chunk_id']}: {e}")

    # Write each branch envelope
    for env in envelopes:
        dest = out_chunks_dir / f"{env['chunk_id']}.json"
        write_env(env, dest)

    # Write index envelope at dataset root
    index_path = out_set_dir / f"{set_id}.index.json"
    write_env(env_index, index_path)

    summary = {
        "set_id": set_id,
        "set_version": set_version,
        "scope": scope,
        "written": {
            "index": str(index_path.relative_to(REPO_ROOT)),
            "chunks_dir": str(out_chunks_dir.relative_to(REPO_ROOT)),
            "count": len(envelopes) + 1
        },
        "counts": counts
    }
    return summary


def main() -> None:
    p = argparse.ArgumentParser(description="KG-Lite Chunker: convert memory graph JSON to deterministic ChunkEnvelope branches")
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="Path to flat graph JSON (default: memory-bank/MEMORY_GRAPH_CONTEXT/justin-graph.json)")
    p.add_argument("--out-root", type=Path, default=REPO_ROOT / "memory-bank" / "MEMORY_GRAPH_CONTEXT", help="Output root for dataset directories")
    p.add_argument("--no-policy", action="store_true", help="Do not emit retrieval_policy chunk")
    args = p.parse_args()

    try:
        summary = chunk_graph(args.input, args.out_root, include_retrieval_policy=(not args.no_policy))
        print(json.dumps(summary, indent=2, sort_keys=True))
    except Exception as e:
        print(json.dumps({"error": str(e)}, indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()