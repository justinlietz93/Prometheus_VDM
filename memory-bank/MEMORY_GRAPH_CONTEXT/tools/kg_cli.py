#!/usr/bin/env python3
"""
VDM Memory-Bank — KG-Lite CRUD CLI with PathRAG indexing
Low-verbosity, file-backed knowledge graph operations.

Scope:
- Stores entities/relations/indexes under memory-bank/MEMORY_GRAPH_CONTEXT/
- No external services; pure local JSON with deterministic formatting
- Read-only to Derivation/; does not modify canonical physics content
- Recreates MCP memory tool functionality for entities/relations, plus PathRAG optimizations

Data files (created on demand):
- Entities:   memory-bank/MEMORY_GRAPH_CONTEXT/entities/kg-entities.v1.json
- Relations:  memory-bank/MEMORY_GRAPH_CONTEXT/relations/kg-relations.v1.json
- PathRAG idx memory-bank/MEMORY_GRAPH_CONTEXT/indexes/kg-pathrag-index.v1.json

Entity record (minimal):
{
  "name": "VDM_Nexus_Approval_CLI",
  "type": "ScriptTool",
  "observations": [
    "Path: [approval_cli.py](VDM_Nexus/scripts/approval_cli.py:1)",
    "Docs: [scripts/README.md](VDM_Nexus/scripts/README.md:41)"
  ]
}

Relation record (minimal):
{
  "from": "EntityA",
  "to": "EntityB",
  "relationType": "wraps"
}

PathRAG index entry (derived):
{
  "path": "vdm_nexus/scripts/approval_cli.py",
  "segments": ["vdm_nexus","scripts","approval_cli.py"],
  "entities": ["VDM_Nexus_Approval_CLI"]
}

CLI examples (low verbosity by default; add --json for JSON output):
  # Add entity with two observations
  python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py entities add \
    --name VDM_Nexus_Approval_CLI \
    --type ScriptTool \
    --obs "Path: [approval_cli.py](VDM_Nexus/scripts/approval_cli.py:1)" \
    --obs "Docs: [scripts/README.md](VDM_Nexus/scripts/README.md:41)"

  # List entities containing 'approval' in name or observations
  python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py entities list --query approval

  # Add relation
  python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py relations add \
    --from VDM_Nexus_Approval_CLI --to Canonical_Approve_Tag_CLI --type wraps

  # Build PathRAG index from entity observations
  python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py index build

  # Query PathRAG by path substring
  python3 memory-bank/MEMORY_GRAPH_CONTEXT/tools/kg_cli.py pathrag search --path VDM_Nexus/scripts/approval_cli.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Root (repo-relative)
REPO_ROOT = Path(".").resolve()

# File locations (repo-relative)
ENTITIES_PATH = REPO_ROOT / "memory-bank" / "MEMORY_GRAPH_CONTEXT" / "entities" / "kg-entities.v1.json"
RELATIONS_PATH = REPO_ROOT / "memory-bank" / "MEMORY_GRAPH_CONTEXT" / "relations" / "kg-relations.v1.json"
INDEX_PATH = REPO_ROOT / "memory-bank" / "MEMORY_GRAPH_CONTEXT" / "indexes" / "kg-pathrag-index.v1.json"

# Markdown link extraction for PathRAG: [label](relative/path:line)
RE_MD_LINK = re.compile(r"\\[[^\\]]*\\]\\(([^)]+)\\)")

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

def read_json(path: Path, default: Any) -> Any:
    try:
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default

def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def normalize_path(p: str) -> str:
    # Accept "VDM_Nexus/scripts/approval_cli.py:1" and strip ":line"
    base = p.split(":", 1)[0].strip()
    # Normalize separators and lowercase for index keys (case-insensitive)
    return str(Path(base)).replace("\\\\", "/").lower()

def segments_for(p_norm: str) -> List[str]:
    return [seg for seg in p_norm.split("/") if seg]

def extract_paths_from_observation(obs: str) -> List[str]:
    paths: List[str] = []
    for m in RE_MD_LINK.finditer(obs):
        target = m.group(1)
        if target:
            paths.append(normalize_path(target))
    return paths

# ----------------------------
# Entities CRUD
# ----------------------------

def load_entities() -> Dict[str, Any]:
    default = {
        "set_id": "kg-entities",
        "set_version": "1.0",
        "updated_utc": now_iso(),
        "entities": []
    }
    data = read_json(ENTITIES_PATH, default)
    # Normalize schema keys if missing
    data.setdefault("set_id", "kg-entities")
    data.setdefault("set_version", "1.0")
    data.setdefault("updated_utc", now_iso())
    data.setdefault("entities", [])
    return data

def save_entities(data: Dict[str, Any]) -> None:
    data["updated_utc"] = now_iso()
    write_json(ENTITIES_PATH, data)

def entity_index(data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    idx: Dict[str, Dict[str, Any]] = {}
    for e in data.get("entities", []):
        name = e.get("name", "")
        if name:
            idx[name] = e
    return idx

def cmd_entities_add(args: argparse.Namespace) -> int:
    data = load_entities()
    idx = entity_index(data)
    name = args.name
    if name in idx and not args.upsert:
        print(f"KG: entity exists: {name}", file=sys.stderr)
        return 1
    rec = idx.get(name, {"name": name, "type": args.type or "Unknown", "observations": []})
    if args.type:
        rec["type"] = args.type
    obs = rec.get("observations", [])
    for o in (args.obs or []):
        if o not in obs:
            obs.append(o)
    rec["observations"] = obs
    if name not in idx:
        data["entities"].append(rec)
    save_entities(data)
    if args.json:
        print(json.dumps({"ok": True, "entity": rec}, indent=2, sort_keys=True))
    else:
        print(f"KG: added/updated entity '{name}' (obs={len(rec['observations'])})")
    return 0

def cmd_entities_update(args: argparse.Namespace) -> int:
    data = load_entities()
    idx = entity_index(data)
    name = args.name
    if name not in idx:
        print(f"KG: entity not found: {name}", file=sys.stderr)
        return 1
    rec = idx[name]
    if args.type:
        rec["type"] = args.type
    if args.set_obs is not None:
        # replace entire observations array
        rec["observations"] = list(args.set_obs)
    else:
        # append
        obs = rec.get("observations", [])
        for o in (args.obs or []):
            if o not in obs:
                obs.append(o)
        rec["observations"] = obs
    save_entities(data)
    if args.json:
        print(json.dumps({"ok": True, "entity": rec}, indent=2, sort_keys=True))
    else:
        print(f"KG: updated entity '{name}'")
    return 0

def cmd_entities_delete(args: argparse.Namespace) -> int:
    data = load_entities()
    before = len(data.get("entities", []))
    data["entities"] = [e for e in data.get("entities", []) if e.get("name") != args.name]
    after = len(data.get("entities", []))
    save_entities(data)
    # Also purge relations that reference this entity
    rel = load_relations()
    rel_before = len(rel.get("relations", []))
    rel["relations"] = [
        r for r in rel.get("relations", [])
        if r.get("from") != args.name and r.get("to") != args.name
    ]
    if len(rel.get("relations", [])) != rel_before:
        save_relations(rel)
    if args.json:
        print(json.dumps({"ok": True, "removed": before - after, "relations_removed": rel_before - len(rel.get("relations", []))}, indent=2, sort_keys=True))
    else:
        print(f"KG: deleted entity '{args.name}' (relations purged: {rel_before - len(rel.get('relations', []))})")
    return 0

def cmd_entities_list(args: argparse.Namespace) -> int:
    data = load_entities()
    items = data.get("entities", [])
    q = (args.query or "").strip().lower()
    if q:
        def match(e: Dict[str, Any]) -> bool:
            if q in (e.get("name","").lower()):
                return True
            if q in (e.get("type","").lower()):
                return True
            for o in e.get("observations", []):
                if q in o.lower():
                    return True
            return False
        items = [e for e in items if match(e)]
    payload = {"count": len(items), "entities": items} if args.json else None
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for e in items:
            print(f"- {e.get('name')} [{e.get('type')}] (obs={len(e.get('observations',[]))})")
        print(f"KG: {len(items)} entity(ies)")
    return 0

# ----------------------------
# Relations CRUD
# ----------------------------

def load_relations() -> Dict[str, Any]:
    default = {
        "set_id": "kg-relations",
        "set_version": "1.0",
        "updated_utc": now_iso(),
        "relations": []
    }
    return read_json(RELATIONS_PATH, default)

def save_relations(data: Dict[str, Any]) -> None:
    data["updated_utc"] = now_iso()
    write_json(RELATIONS_PATH, data)

def cmd_relations_add(args: argparse.Namespace) -> int:
    ents = load_entities()
    names = {e.get("name") for e in ents.get("entities", [])}
    if not args.force:
        missing = [n for n in [args.from_, args.to] if n not in names]
        if missing:
            print(f"KG: missing entity(ies): {', '.join(missing)} (use --force to add anyway)", file=sys.stderr)
            return 1
    rel = load_relations()
    rec = {"from": args.from_, "to": args.to, "relationType": args.type}
    # avoid duplicates
    for r in rel.get("relations", []):
        if r.get("from")==args.from_ and r.get("to")==args.to and r.get("relationType")==args.type:
            if args.json:
                print(json.dumps({"ok": True, "relation": r, "skipped": "exists"}, indent=2, sort_keys=True))
            else:
                print("KG: relation exists (skipped)")
            return 0
    rel["relations"].append(rec)
    save_relations(rel)
    if args.json:
        print(json.dumps({"ok": True, "relation": rec}, indent=2, sort_keys=True))
    else:
        print(f"KG: added relation {args.from_} -[{args.type}]-> {args.to}")
    return 0

def cmd_relations_delete(args: argparse.Namespace) -> int:
    rel = load_relations()
    before = len(rel.get("relations", []))
    rel["relations"] = [
        r for r in rel.get("relations", [])
        if not (r.get("from")==args.from_ and r.get("to")==args.to and (args.type is None or r.get("relationType")==args.type))
    ]
    after = len(rel.get("relations", []))
    save_relations(rel)
    if args.json:
        print(json.dumps({"ok": True, "removed": before - after}, indent=2, sort_keys=True))
    else:
        print(f"KG: deleted {before - after} relation(s)")
    return 0

def cmd_relations_list(args: argparse.Namespace) -> int:
    rel = load_relations()
    items = rel.get("relations", [])
    if args.filter_from:
        items = [r for r in items if r.get("from")==args.filter_from]
    if args.filter_to:
        items = [r for r in items if r.get("to")==args.filter_to]
    if args.filter_type:
        items = [r for r in items if r.get("relationType")==args.filter_type]
    if args.json:
        print(json.dumps({"count": len(items), "relations": items}, indent=2, sort_keys=True))
    else:
        for r in items:
            print(f"- {r.get('from')} -[{r.get('relationType')}]-> {r.get('to')}")
        print(f"KG: {len(items)} relation(s)")
    return 0

# ----------------------------
# PathRAG index
# ----------------------------

def build_pathrag_index() -> Dict[str, Any]:
    ents = load_entities()
    idx: Dict[str, Dict[str, Any]] = {}
    for e in ents.get("entities", []):
        name = e.get("name", "")
        for obs in e.get("observations", []):
            for p in extract_paths_from_observation(obs):
                entry = idx.setdefault(p, {"path": p, "segments": segments_for(p), "entities": []})
                if name and name not in entry["entities"]:
                    entry["entities"].append(name)
    entries = sorted(idx.values(), key=lambda x: (len(x["segments"]), x["path"]))
    payload = {
        "set_id": "kg-pathrag-index",
        "set_version": "1.0",
        "updated_utc": now_iso(),
        "entries": entries
    }
    return payload

def cmd_index_build(args: argparse.Namespace) -> int:
    payload = build_pathrag_index()
    write_json(INDEX_PATH, payload)
    if args.json:
        print(json.dumps({"ok": True, "entries": len(payload.get("entries", [])), "path": str(INDEX_PATH)}, indent=2, sort_keys=True))
    else:
        print(f"KG: PathRAG index built — entries={len(payload.get('entries', []))} → {INDEX_PATH}")
    return 0

def load_index() -> Dict[str, Any]:
    return read_json(INDEX_PATH, {"entries": []})

def cmd_pathrag_search(args: argparse.Namespace) -> int:
    q = normalize_path(args.path)
    idx = load_index()
    items = []
    for entry in idx.get("entries", []):
        p = entry.get("path", "")
        if q in p:
            items.append(entry)
    if args.json:
        print(json.dumps({"count": len(items), "matches": items}, indent=2, sort_keys=True))
    else:
        for it in items:
            print(f"- {it.get('path')}  ⇢  entities={','.join(it.get('entities',[]))}")
        print(f"KG: {len(items)} match(es)")
    return 0

# ----------------------------
# CLI wiring
# ----------------------------

def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="VDM Memory-Bank KG-Lite CRUD with PathRAG")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # entities
    e = sub.add_parser("entities", help="Entity operations")
    e_sub = e.add_subparsers(dest="op", required=True)

    e_add = e_sub.add_parser("add", help="Add entity (or upsert with --upsert)")
    e_add.add_argument("--name", required=True)
    e_add.add_argument("--type", default=None)
    e_add.add_argument("--obs", action="append", help="Observation (repeatable)")
    e_add.add_argument("--upsert", action="store_true", help="Insert or update if exists")
    e_add.add_argument("--json", action="store_true")
    e_add.set_defaults(func=cmd_entities_add)

    e_upd = e_sub.add_parser("update", help="Update entity")
    e_upd.add_argument("--name", required=True)
    e_upd.add_argument("--type", default=None)
    e_upd.add_argument("--obs", action="append", help="Append observation (repeatable)")
    e_upd.add_argument("--set-obs", action="append", help="Replace observations with given list (repeatable)")
    e_upd.add_argument("--json", action="store_true")
    e_upd.set_defaults(func=cmd_entities_update)

    e_del = e_sub.add_parser("delete", help="Delete entity (and purge referencing relations)")
    e_del.add_argument("--name", required=True)
    e_del.add_argument("--json", action="store_true")
    e_del.set_defaults(func=cmd_entities_delete)

    e_list = e_sub.add_parser("list", help="List entities")
    e_list.add_argument("--query", help="Substring filter (case-insensitive)")
    e_list.add_argument("--json", action="store_true")
    e_list.set_defaults(func=cmd_entities_list)

    # relations
    r = sub.add_parser("relations", help="Relation operations")
    r_sub = r.add_subparsers(dest="op", required=True)

    r_add = r_sub.add_parser("add", help="Add relation")
    r_add.add_argument("--from", dest="from_", required=True)
    r_add.add_argument("--to", dest="to", required=True)
    r_add.add_argument("--type", required=True, help="Relation type")
    r_add.add_argument("--force", action="store_true", help="Allow if entities are missing")
    r_add.add_argument("--json", action="store_true")
    r_add.set_defaults(func=cmd_relations_add)

    r_del = r_sub.add_parser("delete", help="Delete relation(s)")
    r_del.add_argument("--from", dest="from_", required=True)
    r_del.add_argument("--to", dest="to", required=True)
    r_del.add_argument("--type", help="If omitted, delete all relations between from→to")
    r_del.add_argument("--json", action="store_true")
    r_del.set_defaults(func=cmd_relations_delete)

    r_list = r_sub.add_parser("list", help="List relations")
    r_list.add_argument("--filter-from", help="Filter by source")
    r_list.add_argument("--filter-to", help="Filter by target")
    r_list.add_argument("--filter-type", help="Filter by relationType")
    r_list.add_argument("--json", action="store_true")
    r_list.set_defaults(func=cmd_relations_list)

    # index build
    ix = sub.add_parser("index", help="Index management")
    ix_sub = ix.add_subparsers(dest="op", required=True)
    ix_build = ix_sub.add_parser("build", help="Build PathRAG index from entity observations")
    ix_build.add_argument("--json", action="store_true")
    ix_build.set_defaults(func=cmd_index_build)

    # pathrag search
    pr = sub.add_parser("pathrag", help="Path-based retrieval")
    pr_sub = pr.add_subparsers(dest="op", required=True)
    pr_search = pr_sub.add_parser("search", help="Search PathRAG index by path substring")
    pr_search.add_argument("--path", required=True, help="Path (repo-relative substring ok)")
    pr_search.add_argument("--json", action="store_true")
    pr_search.set_defaults(func=cmd_pathrag_search)

    args = ap.parse_args(argv)
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))