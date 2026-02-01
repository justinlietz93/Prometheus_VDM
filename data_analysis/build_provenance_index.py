#!/usr/bin/env python3
"""Build a provenance index for data_analysis/.

Generates a single JSON file that recursively lists all regular files under a
root directory with:
  - relative POSIX path
  - SHA-256 of file contents
  - file size (bytes)
  - file mtime in UTC (ISO-8601)

This is intended for integrity/audit and lightweight reproducibility.

Notes
-----
- Excludes the output file itself (to avoid self-reference).
- Uses deterministic ordering by relative path.
- Does not require git; works on any filesystem.

Example
-------
python data_analysis/build_provenance_index.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class IndexedFile:
    path: str
    sha256: str
    size_bytes: int
    mtime_utc: str


def _sha256_file(path: Path, bufsize: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(bufsize)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def _iter_files(root: Path) -> Iterable[Path]:
    for p in root.rglob("*"):
        # Skip dirs and broken symlinks cleanly
        try:
            if not p.is_file():
                continue
        except FileNotFoundError:
            continue
        yield p


def _iso_utc_from_timestamp(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def build_index(root: Path, output: Path) -> dict:
    root = root.resolve()
    output = output.resolve()

    files: List[IndexedFile] = []
    for p in _iter_files(root):
        if p.resolve() == output:
            continue
        rel = p.relative_to(root).as_posix()
        stat = p.stat()
        files.append(
            IndexedFile(
                path=rel,
                sha256=_sha256_file(p).lower(),
                size_bytes=int(stat.st_size),
                mtime_utc=_iso_utc_from_timestamp(stat.st_mtime),
            )
        )

    files_sorted = sorted(files, key=lambda x: x.path)
    total_bytes = sum(f.size_bytes for f in files_sorted)

    return {
        "schema_version": "1.0",
        "root": root.name,
        "generated_at_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "hash_algorithm": "SHA256",
        "total_files": len(files_sorted),
        "total_bytes": int(total_bytes),
        "files": [f.__dict__ for f in files_sorted],
    }


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build a SHA256 provenance index for a directory")
    parser.add_argument(
        "--root",
        type=str,
        default=str(Path(__file__).resolve().parent),
        help="Root directory to index (default: this script's folder)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="PROVENANCE_index.json",
        help="Output JSON filename or path (default: PROVENANCE_index.json under root)",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.exists():
        raise SystemExit(f"[error] root does not exist: {root}")

    output = Path(args.output)
    if not output.is_absolute():
        output = root / output

    payload = build_index(root=root, output=output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "output": str(output),
                "files": payload["total_files"],
                "bytes": payload["total_bytes"],
                "generated_at_utc": payload["generated_at_utc"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
