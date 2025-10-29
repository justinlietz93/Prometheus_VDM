#!/usr/bin/env python3
"""VDM Nexus — Canon Resolver Printer (Task 0.3.2).

Print commit metadata for core canon anchors while guaranteeing that
all paths resolve inside the Derivation/ tree.  This script is read-only
and honours the repository root precedence (CLI > env `VDM_REPO_ROOT` >
filesystem traversal).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from canon_paths import CanonPathError, CanonResolver

DEFAULT_TARGETS = [
    "Derivation/AXIOMS.md#vdm-ax-a0",
    "Derivation/EQUATIONS.md#vdm-e-033",
    "Derivation/VALIDATION_METRICS.md#kpi-front-speed-rel-err",
]


def _relative_to_repo(resolver: CanonResolver, path: Path) -> str:
    try:
        return str(path.relative_to(resolver.repo_root))
    except ValueError:
        return str(path)


def resolve_targets(resolver: CanonResolver, targets: List[str]) -> Dict[str, Any]:
    repo_head = resolver.git_head() or ""
    entries: List[Dict[str, Any]] = []
    for target in targets:
        entry: Dict[str, Any] = {"target": target}
        try:
            resolved, fragment = resolver.resolve(target)
        except CanonPathError as exc:
            entry["error"] = str(exc)
            entry["exists"] = False
            entries.append(entry)
            continue

        metadata = resolver.metadata(resolved)
        entry.update(
            {
                "resolved_path": _relative_to_repo(resolver, metadata.path),
                "fragment": fragment,
                "exists": metadata.exists,
                "size_bytes": metadata.size_bytes,
                "sha256": metadata.sha256,
                "file_last_commit": metadata.last_commit,
            }
        )
        entries.append(entry)
    return {"repo_head": repo_head, "repo_root": str(resolver.repo_root), "entries": entries}


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print canonical file locations and commit metadata"
    )
    parser.add_argument("--repo-root", help="Explicit repository root (defaults to resolver search)")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    parser.add_argument("--targets", nargs="*", default=None, help="Override target paths")
    args = parser.parse_args(argv)

    resolver = CanonResolver.from_sources(args.repo_root)
    targets = args.targets if args.targets else DEFAULT_TARGETS
    result = resolve_targets(resolver, targets)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    print("== VDM Nexus — Canon Resolver ==")
    print(f"Repo root: {result['repo_root']}")
    print(f"Repo HEAD: {result['repo_head']}")
    for entry in result["entries"]:
        target = entry["target"]
        if entry.get("error"):
            print(f"- {target}: ERROR — {entry['error']}")
            continue
        status = "FOUND" if entry.get("exists") else "MISSING"
        resolved = entry.get("resolved_path", "?")
        fragment = entry.get("fragment")
        if fragment:
            resolved = f"{resolved}#{fragment}"
        print(f"- {target}: {status}")
        print(f"    resolved: {resolved}")
        print(f"    last_commit: {entry.get('file_last_commit','') or '(none)'}")
        if entry.get("sha256"):
            print(f"    sha256: {entry['sha256']}")
        if entry.get("size_bytes") is not None:
            print(f"    size: {entry['size_bytes']} bytes")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
