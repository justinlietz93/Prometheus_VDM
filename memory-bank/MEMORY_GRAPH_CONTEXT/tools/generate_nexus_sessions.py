#!/usr/bin/env python3
import os
import json
import hashlib
import datetime
import argparse
import pathlib
import subprocess


def canon_sha256(obj):
    s = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(s).hexdigest()


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")


def get_repo_head(repo_root=None):
    try:
        if repo_root is None:
            # repo root assumed to be project root (three parents up from this script)
            repo_root = str(pathlib.Path(__file__).resolve().parents[3])
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return None


def build_envelope(set_id, version, chunk_type, payload, now, source, scope="session", tags=None, part=1, total_parts=1):
    if tags is None:
        tags = ["kg-lite", chunk_type, "nexus", "session"]
    chunk_id = f"{set_id}@{version}:{chunk_type}"
    env = {
        "set_id": set_id,
        "set_version": version,
        "chunk_type": chunk_type,
        "chunk_id": chunk_id,
        "scope": scope,
        "updated": now,
        "source": source,
        "content_sha256": canon_sha256(payload),
        "part": part,
        "total_parts": total_parts,
        "tags": tags,
        "payload": payload,
    }
    return env


def main():
    ap = argparse.ArgumentParser(description="Generate KG-Lite envelopes for a Nexus session dataset.")
    ap.add_argument("--set-id", default="nexus-sessions", help="Dataset id (directory name under MEMORY_GRAPH_CONTEXT)")
    ap.add_argument("--version", default="1.0", help="Dataset version string")
    ap.add_argument("--agent", default="roo", help="Agent name")
    ap.add_argument("--role", default="Physicist", help="Agent role")
    args = ap.parse_args()

    base = f"memory-bank/MEMORY_GRAPH_CONTEXT/{args.set_id}"
    chunks_dir = f"{base}/chunks"
    os.makedirs(chunks_dir, exist_ok=True)
    os.makedirs("memory-bank/logs", exist_ok=True)

    now = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    repo_head = get_repo_head()
    source = f"agent:{args.agent};mode:{args.role};workflow:VDM_Nexus_KG-Lite"
    if repo_head:
        source += f";repo_head:{repo_head}"

    # Meta
    meta_payload = {
        "dataset": args.set_id,
        "version": args.version,
        "session_utc": now,
        "agent": args.agent,
        "role": args.role,
        "policy": "external-agent-only; no in-repo memory impl inside VDM_Nexus",
        "links": [
            "memory-bank/MEMORY_GRAPH_STANDARDS.md#6a-kg-lite-chunk-envelope-and-branching"
        ],
        "notes": "Session dataset for logging Nexus workflow context using KG-Lite envelopes."
    }

    # Signals (key session memories and next actions)
    signals = [
        {
            "id": "sig:kg-lite-adoption",
            "text": "Use KG-Lite memory during workflows; log important context like the flat memory-bank but in chunked KG-Lite.",
            "labels": ["nexus", "kg-lite", "policy", "session"],
            "acceptance_test": {
                "policy.external_agent_only": True,
                "determinism.content_sha256": True
            },
            "source": "memory-bank/MEMORY_GRAPH_STANDARDS.md",
            "created_utc": now
        },
        {
            "id": "sig:nexus-todos-7-13",
            "text": "Proceed with Nexus TODO items 7–13: static policy mapping; privacy/retention; PathRAG microservice; plugin integration + E2E; docs; CI checks; jsonschema target.",
            "labels": ["nexus", "todo", "kg-lite"],
            "acceptance_test": {
                "todo.7.mapped_to_policy": "pending",
                "todo.8.retention_enforced": "pending",
                "todo.9.pathrag_service": "pending",
                "todo.10.nexus_plugin_e2e": "pending",
                "todo.12.ci_checks": "pending",
                "todo.13.jsonschema_ci": "pending"
            },
            "source": "VDM_Nexus/TODO_CHECKLIST.md",
            "created_utc": now
        },
        {
            "id": "sig:nexus-ci-workflow-added",
            "text": "Added Nexus-only CI compile workflow at .github/workflows/nexus-ci.yml; builds VDM_Nexus with -DNEXUS_BUILD_TESTS=ON; no Derivation writes.",
            "labels": ["nexus", "workflow", "build", "kg-lite"],
            "acceptance_test": {
                "ci.workflow_present": True,
                "ci.nexus_build_compiles": "pending"
            },
            "source": ".github/workflows/nexus-ci.yml",
            "created_utc": now
        },
        {
            "id": "sig:derivation-guard-policy-enforced",
            "text": "Derivation pre-commit/CI guard enforcing CHRONICLES + canon policy configured; stricter than nexus gate.",
            "labels": ["nexus", "policy", "canon", "kg-lite"],
            "acceptance_test": {
                "guard.precommit_configured": True,
                "guard.ci_workflow_present": "pending"
            },
            "source": "VDM_Nexus/scripts/precommit_derivation_guard.py",
            "created_utc": now
        }
    ]
    signals_payload = {"signals": signals}

    # Edges (relation ontology + links)
    edges_payload = {
        "relation_ontology": [
            "implements", "depends_on", "validates", "supports", "contradicts", "has_artifact"
        ],
        "edges": [
            {"from": "sig:kg-lite-adoption", "to": "doc:MEMORY_GRAPH_STANDARDS", "rel": "implements", "weight": 0.9},
            {"from": "sig:nexus-todos-7-13", "to": "doc:VDM_Nexus_TODO", "rel": "depends_on", "weight": 0.8},
            {"from": "sig:nexus-ci-workflow-added", "to": "doc:VDM_Nexus_CI", "rel": "implements", "weight": 0.9},
            {"from": "sig:derivation-guard-policy-enforced", "to": "doc:Derivation_Guard_Policy", "rel": "implements", "weight": 0.9}
        ]
    }

    # Retrieval policy (defaults declared in the standards)
    retrieval_policy_payload = {
        "path_prune_alpha": 0.8,
        "path_threshold": 0.2,
        "min_novelty": 0.55,
        "notes": "Defaults per MEMORY_GRAPH_STANDARDS §6A retrieval_policy."
    }

    written = []

    # Write chunks
    for chunk_type, payload in [
        ("meta", meta_payload),
        ("signals", signals_payload),
        ("edges", edges_payload),
        ("retrieval_policy", retrieval_policy_payload),
    ]:
        env = build_envelope(args.set_id, args.version, chunk_type, payload, now, source)
        out_path = f"{chunks_dir}/{chunk_type}.json"
        write_json(out_path, env)
        written.append({
            "chunk_id": env["chunk_id"],
            "sha256": env["content_sha256"],
            "path": out_path,
            "chunk_type": chunk_type
        })

    # Index envelope
    index_payload = {
        "set_id": args.set_id,
        "set_version": args.version,
        "chunks": [
            {
                "chunk_id": w["chunk_id"],
                "content_sha256": w["sha256"],
                "path": w["path"],
                "chunk_type": w["chunk_type"]
            } for w in written
        ],
        "counts": {
            "chunk_count": len(written),
            "signals": len(signals_payload.get("signals", [])),
            "edges": len(edges_payload.get("edges", []))
        }
    }
    index_env = build_envelope(args.set_id, args.version, "index", index_payload, now, source)
    index_path = f"{base}/{args.set_id}.index.json"
    write_json(index_path, index_env)

    # Audit line (append-only)
    audit = {
        "op": "write_kg_lite_dataset",
        "dataset": args.set_id,
        "version": args.version,
        "created_utc": now,
        "chunks": {w["chunk_id"]: w["sha256"] for w in written},
        "index_sha256": index_env["content_sha256"],
        "counts": index_payload["counts"]
    }
    with open("memory-bank/logs/memory_audit.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(audit, sort_keys=True) + "\n")

    # Summary
    print("Created KG-Lite dataset:", args.set_id)
    print("Index:", index_path)
    for w in written:
        print("Chunk:", w["chunk_type"], "path=", w["path"], "sha256=", w["sha256"])
    print("Audit appended to memory-bank/logs/memory_audit.jsonl")


if __name__ == "__main__":
    main()