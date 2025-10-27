#!/usr/bin/env python3
"""
VDM Nexus — Canon Resolver Printer (Task 0.3.2)

Purpose:
- Resolve canonical files under ../Derivation and print commit metadata for manual validation.
- Read-only operation. Does not modify Derivation/.

Targets (default):
- Derivation/AXIOMS.md
- Derivation/EQUATIONS.md
- Derivation/VALIDATION_METRICS.md

Printed metadata per target:
- exists: true/false
- repo_head: repository HEAD commit (git rev-parse HEAD)
- file_last_commit: last commit that changed this file (git log -n 1 --pretty=%H -- path), if tracked
- sha256: content hash if file exists
- size_bytes: file size if file exists

Usage:
  python VDM_Nexus/scripts/nexus_resolver_print.py
  python VDM_Nexus/scripts/nexus_resolver_print.py --json
  python VDM_Nexus/scripts/nexus_resolver_print.py --targets Derivation/EQUATIONS.md Derivation/VALIDATION_METRICS.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any


DEFAULT_TARGETS = [
    "Derivation/AXIOMS.md",
    "Derivation/EQUATIONS.md",
    "Derivation/VALIDATION_METRICS.md",
]


def run(cmd: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def git_repo_head() -> str:
    cp = run(["git", "rev-parse", "HEAD"])
    return (cp.stdout or "").strip() if cp.returncode == 0 else ""


def git_file_last_commit(path: str) -> str:
    cp = run(["git", "log", "-n", "1", "--pretty=%H", "--", path])
    return (cp.stdout or "").strip() if cp.returncode == 0 else ""


def sha256_of_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def resolve_targets(targets: List[str]) -> Dict[str, Any]:
    repo_head = git_repo_head()
    out: Dict[str, Any] = {"repo_head": repo_head, "entries": []}
    for t in targets:
        p = Path(t)
        entry: Dict[str, Any] = {"path": t, "exists": p.exists()}
        entry["repo_head"] = repo_head
        entry["file_last_commit"] = git_file_last_commit(t)
        if p.exists() and p.is_file():
            entry["size_bytes"] = p.stat().st_size
            try:
                entry["sha256"] = sha256_of_file(p)
            except Exception as e:
                entry["sha256_error"] = str(e)
        out["entries"].append(entry)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Print canonical file locations and commit metadata")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--targets", nargs="*", default=None, help="Override target paths")
    args = parser.parse_args()

    targets = args.targets if args.targets else DEFAULT_TARGETS
    result = resolve_targets(targets)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("== VDM Nexus — Canon Resolver ==")
        print(f"Repo HEAD: {result['repo_head']}")
        for e in result["entries"]:
            print(f"- {e['path']}: {'FOUND' if e['exists'] else 'MISSING'}")
            print(f"    last_commit: {e.get('file_last_commit','')}")
            if e.get("exists") and "sha256" in e:
                print(f"    sha256: {e['sha256']}")
                print(f"    size: {e.get('size_bytes','?')} bytes")

    # This script does not enforce PASS/FAIL; it prints metadata for manual validation.
    # Exit 0 always, to serve as an informational resolver.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())