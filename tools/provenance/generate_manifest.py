#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


VDM Provenance Manifest Generator
---------------------------------
Purpose:
  - Create an immutable, machine-verifiable manifest of the repository state:
      * SHA-256 per file
      * Sizes (bytes)
      * Deterministic tree hash over the set
      * Git commit and dirty flag
      * UTC timestamp
  - Optionally pack a release archive (tar.gz) that includes the manifest.

Output:
  - PROVENANCE_manifest.json (default) in the selected root
  - Optional tar.gz archive if --archive is provided

JSON discipline:
  - json.dump(..., indent=2, sort_keys=True)

Exclusions:
  - Skips common build/cache folders by default (see DEFAULT_EXCLUDES),
    and the output files themselves.

Usage examples:
  - python tools/provenance/generate_manifest.py
  - python tools/provenance/generate_manifest.py --root . --output PROVENANCE_manifest.json
  - python tools/provenance/generate_manifest.py --archive VDM_RELEASE.tar.gz

Notes:
  - This tool does not contact external timestamp services. After generating the
    manifest (and optional archive), submit them to a TSA (RFC3161) or OpenTimestamps
    to obtain independent time receipts, and store receipts alongside the artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tarfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

try:
    import subprocess
except Exception:
    subprocess = None  # type: ignore


# Default folders and file names to exclude from hashing/walk
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    ".mypy_cache",
    ".pytest_cache",
    ".cache",
    "__pycache__",
    "build",
    "dist",
    "out",
    "node_modules",
    ".venv",
    "venv",
    "VDM_Nexus/build",
}

DEFAULT_EXCLUDE_FILE_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".o",
    ".obj",
    ".dll",
    ".so",
    ".dylib",
    ".exe",
    ".pdb",
}

DEFAULT_EXCLUDE_FILE_NAMES = {
    # common large artifacts to skip if present at root
    "PROVENANCE_manifest.json",
}


@dataclass
class FileEntry:
    path: str         # relative POSIX path
    size: int         # bytes
    sha256: str       # hex


def _sha256_file(path: Path, bufsize: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(bufsize)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _is_excluded(path: Path,
                 root: Path,
                 exclude_dirs: Iterable[str],
                 exclude_suffixes: Iterable[str],
                 exclude_file_names: Iterable[str],
                 extra_excludes: Iterable[str]) -> bool:
    rel = path.relative_to(root)
    # Directory-based excludes
    for part in rel.parts[:-1]:
        if part in exclude_dirs:
            return True
    # Name/suffix excludes
    name = rel.name
    if name in exclude_file_names:
        return True
    if any(str(rel).startswith(e.rstrip("/")) for e in extra_excludes):
        return True
    if path.is_file():
        if path.suffix.lower() in exclude_suffixes:
            return True
    return False


def _git_meta(root: Path) -> Tuple[Optional[str], Optional[bool]]:
    commit = None
    dirty = None
    if subprocess is None:
        return commit, dirty
    try:
        commit = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        status = subprocess.check_output(
            ["git", "-C", str(root), "status", "--porcelain"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        dirty = len(status.strip()) > 0
    except Exception:
        commit, dirty = None, None
    return commit, dirty


def _build_tree_hash(entries: List[FileEntry]) -> str:
    """
    Deterministic tree hash over (sha256, size, path).
    """
    lines = []
    for e in sorted(entries, key=lambda x: x.path):
        lines.append(f"{e.sha256}  {e.size}  {e.path}")
    blob = ("\n".join(lines) + "\n").encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def _scan_repo(root: Path,
               extra_excludes: Iterable[str],
               verbose: bool = False) -> Tuple[List[FileEntry], int, int]:
    files: List[FileEntry] = []
    total_bytes = 0
    count = 0
    t0 = time.time()

    # Normalize excludes
    extra_excl = list(extra_excludes)

    for p in root.rglob("*"):
        if p.is_dir():
            # Quick directory skip if its name is in exclude set
            if p.name in DEFAULT_EXCLUDE_DIRS:
                # prune: skip walking deeper into this directory
                # rglob cannot be pruned directly; rely on _is_excluded per file
                pass
            continue
        if _is_excluded(
            p,
            root,
            DEFAULT_EXCLUDE_DIRS,
            DEFAULT_EXCLUDE_FILE_SUFFIXES,
            DEFAULT_EXCLUDE_FILE_NAMES,
            extra_excl,
        ):
            continue
        try:
            size = p.stat().st_size
        except FileNotFoundError:
            # File disappeared during walk; skip
            continue
        try:
            digest = _sha256_file(p)
        except PermissionError:
            if verbose:
                print(f"[skip:perm] {p}", file=sys.stderr)
            continue
        rel = p.relative_to(root).as_posix()
        files.append(FileEntry(path=rel, size=size, sha256=digest))
        total_bytes += size
        count += 1
        if verbose and count % 250 == 0:
            dt = time.time() - t0
            rate = count / dt if dt > 0 else 0.0
            print(f"[scan] {count} files ({total_bytes} bytes) @ {rate:.1f} f/s", file=sys.stderr)

    return files, total_bytes, count


def _write_manifest(out_path: Path,
                    root: Path,
                    entries: List[FileEntry],
                    total_bytes: int,
                    count: int,
                    git_commit: Optional[str],
                    git_dirty: Optional[bool]) -> None:
    payload = {
        "schema": "vdm.provenance.manifest.v1",
        "repo_root": str(root.resolve()),
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit,
        "git_dirty": git_dirty,
        "excludes": {
            "dirs": sorted(list(DEFAULT_EXCLUDE_DIRS)),
            "file_suffixes": sorted(list(DEFAULT_EXCLUDE_FILE_SUFFIXES)),
            "file_names": sorted(list(DEFAULT_EXCLUDE_FILE_NAMES)),
        },
        "file_count": count,
        "total_bytes": total_bytes,
        "tree_hash": _build_tree_hash(entries),
        "files": [e.__dict__ for e in entries],
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)


def _make_archive(archive_path: Path, root: Path, manifest_path: Path,
                  entries: List[FileEntry], verbose: bool = False) -> None:
    """
    Create a tar.gz containing:
      - The manifest
      - All files listed in the manifest (relative to root)
    """
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "w:gz") as tar:
        # Add manifest first
        tar.add(manifest_path, arcname=manifest_path.name)
        # Add files deterministically by sorted path
        for e in sorted(entries, key=lambda x: x.path):
            src = root / Path(e.path)
            if not src.exists():
                if verbose:
                    print(f"[archive:missing] {e.path}", file=sys.stderr)
                continue
            tar.add(src, arcname=e.path)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Generate VDM provenance manifest (SHA-256 per file, tree hash, commit, UTC).")
    parser.add_argument("--root", type=str, default=".", help="Repository root (default: .)")
    parser.add_argument("--output", type=str, default="PROVENANCE_manifest.json", help="Manifest output path (relative or absolute).")
    parser.add_argument("--archive", type=str, default=None, help="Optional tar.gz path to pack files + manifest.")
    parser.add_argument("--exclude", action="append", default=[], help="Extra path prefix to exclude (repeatable).")
    parser.add_argument("--verbose", action="store_true", help="Verbose progress to stderr.")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.exists():
        print(f"[error] root does not exist: {root}", file=sys.stderr)
        return 2

    # Ensure we exclude outputs if they fall under the root
    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = (root / output_path).resolve()
    extra_excludes = list(args.exclude)
    # Exclude the manifest and archive files themselves
    try:
        extra_excludes.append(str(output_path.relative_to(root).as_posix()))
    except Exception:
        # If manifest outside root, no need to exclude
        pass
    if args.archive:
        archive_path = Path(args.archive)
        if not archive_path.is_absolute():
            archive_path = (root / archive_path).resolve()
        try:
            extra_excludes.append(str(archive_path.relative_to(root).as_posix()))
        except Exception:
            pass
    else:
        archive_path = None  # type: ignore

    if args.verbose:
        print(f"[start] root={root}", file=sys.stderr)

    # Collect git metadata
    git_commit, git_dirty = _git_meta(root)
    if args.verbose:
        print(f"[git] commit={git_commit} dirty={git_dirty}", file=sys.stderr)

    # Scan repository
    entries, total_bytes, count = _scan_repo(root, extra_excludes=extra_excludes, verbose=args.verbose)

    # Write manifest
    _write_manifest(output_path, root, entries, total_bytes, count, git_commit, git_dirty)
    if args.verbose:
        print(f"[write] manifest={output_path}", file=sys.stderr)

    # Optional archive
    if archive_path:
        _make_archive(archive_path, root, output_path, entries, verbose=args.verbose)
        if args.verbose:
            print(f"[archive] path={archive_path}", file=sys.stderr)

    # Summary to stdout
    print(json.dumps({
        "manifest": str(output_path),
        "archive": str(archive_path) if archive_path else None,
        "files": count,
        "bytes": total_bytes,
    }, indent=2, sort_keys=True))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())