#!/usr/bin/env python3
"""VDM Nexus — CanonSync CLI skeleton (Task 0.3.3).

Produces a read-only ingestion plan for canonical anchors referenced by
Nexus.  The command reads `nexus_canon_config.v1.json`, resolves each
anchor via :mod:`canon_paths`, and reports metadata (exists, size, hash,
last commit).  No files are written; this is scaffolding for future
indexing tooling.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from canon_paths import CanonPathError, CanonResolver

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "resources" / "nexus_canon_config.v1.json"


def _load_config(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"canon config not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    anchors = data.get("anchors")
    if not isinstance(anchors, list):
        raise ValueError("config anchors must be a list")
    return data


def _build_plan(resolver: CanonResolver, config: Dict[str, Any]) -> Dict[str, Any]:
    anchors: List[Dict[str, Any]] = []
    for entry in config.get("anchors", []):
        target = entry.get("path")
        label = entry.get("label") or entry.get("id")
        record: Dict[str, Any] = {
            "id": entry.get("id"),
            "label": label,
            "path": target,
            "summary": entry.get("summary"),
        }
        if not isinstance(target, str) or not target.strip():
            record["error"] = "missing canonical path"
            anchors.append(record)
            continue
        try:
            resolved, fragment = resolver.resolve(target)
        except CanonPathError as exc:
            record["error"] = str(exc)
            anchors.append(record)
            continue

        metadata = resolver.metadata(resolved)
        record.update(
            {
                "resolved_path": _relative_to_repo(resolver, metadata.path),
                "fragment": fragment,
                "exists": metadata.exists,
                "size_bytes": metadata.size_bytes,
                "sha256": metadata.sha256,
                "file_last_commit": metadata.last_commit,
            }
        )
        anchors.append(record)

    return {
        "config_path": str(config.get("config_path")),
        "config_id": config.get("set_id"),
        "config_version": config.get("set_version"),
        "repo_root": str(resolver.repo_root),
        "repo_head": resolver.git_head(),
        "anchors": anchors,
    }


def _relative_to_repo(resolver: CanonResolver, path: Path) -> str:
    try:
        return str(path.relative_to(resolver.repo_root))
    except ValueError:
        return str(path)


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a read-only canon ingestion plan for Nexus"
    )
    parser.add_argument("--repo-root", help="Explicit repository root (defaults to resolver search)")
    parser.add_argument(
        "--config",
        help="Path to canon config JSON (default: resources/nexus_canon_config.v1.json)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON plan to stdout")
    args = parser.parse_args(argv)

    resolver = CanonResolver.from_sources(args.repo_root)
    config_path = Path(args.config) if args.config else DEFAULT_CONFIG
    config_data = _load_config(config_path)
    config_data["config_path"] = str(config_path)
    plan = _build_plan(resolver, config_data)

    if args.json:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return 0

    print("[NEXUS][CANON-SYNC] Generated read-only plan")
    print(f"  repo_root: {plan['repo_root']}")
    print(f"  repo_head: {plan['repo_head'] or '(unknown)'}")
    print(f"  config: {plan['config_path']}")
    print(f"  anchors: {len(plan['anchors'])}")
    for anchor in plan["anchors"]:
        label = anchor.get("label") or anchor.get("id") or "(unknown)"
        if anchor.get("error"):
            print(f"    - {label}: ERROR — {anchor['error']}")
            continue
        status = "OK" if anchor.get("exists") else "MISSING"
        resolved = anchor.get("resolved_path")
        if anchor.get("fragment"):
            resolved = f"{resolved}#{anchor['fragment']}"
        print(f"    - {label}: {status}")
        print(f"        path: {resolved}")
        print(f"        last_commit: {anchor.get('file_last_commit') or '(none)'}")
        if anchor.get("sha256"):
            print(f"        sha256: {anchor['sha256']}")
        if anchor.get("size_bytes") is not None:
            print(f"        size: {anchor['size_bytes']} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
