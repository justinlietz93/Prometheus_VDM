#!/usr/bin/env python3
"""
Generate salted SHA-256 provenance for one or more files.

For each file:
 - Compute base_sha256 = SHA-256(file contents)
 - Generate or accept a hex salt
 - Compute salted_sha256 = SHA-256(f"{base_sha256}:{salt_hex}") over UTF-8 bytes

Output (default JSON):
{
  "schema": "vdm.provenance.salted_hash.v1",
  "generated_utc": "...Z",
  "salt_bytes": 16,
  "single_salt": true/false,
  "salt_hex": "..." | null,
  "items": [
    {"path": "...", "size": 123, "base_sha256": "...", "salt_hex": "...", "salted_sha256": "..."},
    ...
  ]
}

Examples:
  python tools/provenance/generate_salted_hash.py Derivation/code/physics/metriplectic/specs/assisted_echo.v1.json
  python tools/provenance/generate_salted_hash.py --single-salt --salt-bytes 32 file1.txt file2.txt
  python tools/provenance/generate_salted_hash.py --salt 0123abcd... PRE-REGISTRATION.echo_spec-v1.json
  python tools/provenance/generate_salted_hash.py --text file.txt
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class SaltedItem:
    path: str
    size: int
    base_sha256: str
    salt_hex: str
    salted_sha256: str


def _sha256_file(path: Path, bufsize: int = 1024 * 1024) -> Tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        while True:
            chunk = f.read(bufsize)
            if not chunk:
                break
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


essential_hex = set("0123456789abcdefABCDEF")

def _validate_or_generate_salt(hex_str: Optional[str], nbytes: int) -> str:
    if hex_str is not None:
        # Validate hex
        s = hex_str.strip()
        if len(s) == 0 or any(c not in essential_hex for c in s):
            raise ValueError("--salt must be a non-empty hex string")
        if len(s) % 2 != 0:
            raise ValueError("--salt hex length must be even")
        return s.lower()
    # Generate random salt
    return os.urandom(nbytes).hex()


def _compute_salted(base_hex: str, salt_hex: str) -> str:
    payload = f"{base_hex}:{salt_hex}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _populate_provenance_indexes() -> None:
    """
    Populate Derivation/**/PROVENANCE_index.json with plain SHA-256 indexes.

    For each PROVENANCE_index.json under Derivation/, treat its parent directory
    as a domain root and index all regular files beneath it (excluding the
    PROVENANCE_index.json itself and any PROVENANCE_manifest.json), writing:

    {
      "schema": "vdm.provenance.index.v1",
      "generated_utc": "...Z",
      "root": "Derivation/Domain",
      "items": [
        { "path": "Derivation/Domain/...", "size": 123, "sha256": "..." },
        ...
      ]
    }
    """
    repo_root = Path(__file__).resolve().parents[2]
    deriv_root = repo_root / "Derivation"
    if not deriv_root.exists():
        raise SystemExit(f"[error] Derivation directory not found at {deriv_root}")

    SKIP_DIR_NAMES = {
        ".git",
        "__pycache__",
        ".ipynb_checkpoints",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
    }
    SKIP_FILE_NAMES = {
        ".DS_Store",
        "Thumbs.db",
    }

    def _should_skip_file(path: Path, *, root: Path, exclude_top_level: set[str]) -> bool:
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            return True
        if path.name in SKIP_FILE_NAMES:
            return True
        try:
            rel = path.relative_to(root)
        except ValueError:
            return False
        if rel.parts and rel.parts[0] in exclude_top_level:
            return True
        return False

    # Existing derivation provenance indexes (domain-owned roots)
    targets: List[Tuple[Path, Path, set[str]]] = []
    for idx_path in deriv_root.rglob("PROVENANCE_index.json"):
        targets.append((idx_path, idx_path.parent, set()))

    # Ensure provenance coverage for code + outputs trees.
    # Note: exclude outputs from the code-root index so code changes don't
    # churn whenever run artifacts change.
    code_root = deriv_root / "code"
    if code_root.exists():
        targets.append((code_root / "PROVENANCE_index.json", code_root, {"outputs"}))
        outputs_root = code_root / "outputs"
        if outputs_root.exists():
            targets.append((outputs_root / "PROVENANCE_index.json", outputs_root, set()))

    # Dedupe targets by index path (prefer explicit targets if duplicates exist)
    dedup: dict[Path, Tuple[Path, Path, set[str]]] = {}
    for idx_path, root, exclude_top_level in targets:
        dedup[idx_path.resolve()] = (idx_path, root, exclude_top_level)
    targets = list(dedup.values())
    if not targets:
        print("[provenance-index] no provenance index targets found under Derivation/")
        return

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    for idx_path, domain_root, exclude_top_level in targets:
        items = []
        for pth in domain_root.rglob("*"):
            if not pth.is_file():
                continue
            # Avoid self-references and manifest/provenance recursion
            if pth.name in {"PROVENANCE_index.json", "PROVENANCE_manifest.json"}:
                continue
            if _should_skip_file(pth, root=domain_root, exclude_top_level=exclude_top_level):
                continue
            base_hex, size = _sha256_file(pth)
            rel = pth.relative_to(repo_root).as_posix()
            items.append(
                {
                    "path": rel,
                    "size": int(size),
                    "sha256": base_hex,
                }
            )

        items.sort(key=lambda d: d["path"])
        payload = {
            "schema": "vdm.provenance.index.v1",
            "generated_utc": now,
            "root": domain_root.relative_to(repo_root).as_posix(),
            "items": items,
        }
        idx_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"[provenance-index] wrote {len(items)} entries to {idx_path}")


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Generate salted provenance hashes for files")
    p.add_argument("files", nargs="*", help="Files to hash")
    p.add_argument("--salt", help="Hex salt to use (applied to all files). If omitted, salt is generated.")
    p.add_argument("--single-salt", action="store_true", help="Use a single random salt for all files (ignored if --salt is provided)")
    p.add_argument("--salt-bytes", type=int, default=16, help="Number of random salt bytes when generating (default: 16)")
    p.add_argument("--text", action="store_true", help="Emit human-readable text instead of JSON")
    p.add_argument(
        "--populate-provenance-indexes",
        action="store_true",
        help="Populate Derivation/**/PROVENANCE_index.json with SHA-256 indexes for files under each domain root",
    )

    args = p.parse_args(argv)

    if args.populate_provenance_indexes:
        if args.files:
            raise SystemExit("[error] --populate-provenance-indexes cannot be combined with explicit file arguments")
        _populate_provenance_indexes()
        return 0

    if not args.files:
        p.error("at least one file path is required unless --populate-provenance-indexes is used")

    paths = [Path(x).resolve() for x in args.files]
    for pth in paths:
        if not pth.exists() or not pth.is_file():
            raise SystemExit(f"[error] file not found: {pth}")

    items: List[SaltedItem] = []

    # Determine salt strategy
    global_salt: Optional[str] = None
    if args.salt:
        global_salt = _validate_or_generate_salt(args.salt, args.salt_bytes)
    elif args.single_salt:
        global_salt = _validate_or_generate_salt(None, args.salt_bytes)

    for pth in paths:
        base, size = _sha256_file(pth)
        salt_hex = global_salt if global_salt is not None else _validate_or_generate_salt(None, args.salt_bytes)
        salted = _compute_salted(base, salt_hex)
        items.append(SaltedItem(path=str(pth), size=size, base_sha256=base, salt_hex=salt_hex, salted_sha256=salted))

    if args.text:
        # Human-readable
        print(f"generated_utc: {datetime.now(timezone.utc).isoformat().replace('+00:00','Z')}")
        if global_salt is not None:
            print(f"global_salt_hex: {global_salt}")
        print(f"salt_bytes: {args.salt_bytes}")
        for it in items:
            print(f"\n{it.path}")
            print(f"  size: {it.size}")
            print(f"  base_sha256: {it.base_sha256}")
            print(f"  salt_hex: {it.salt_hex}")
            print(f"  salted_sha256: {it.salted_sha256}")
        return 0

    payload = {
        "schema": "vdm.provenance.salted_hash.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "salt_bytes": int(args.salt_bytes),
        "single_salt": bool(global_salt is not None and args.salt is None and args.single_salt),
        "salt_hex": global_salt if (args.salt or args.single_salt) else None,
        "items": [it.__dict__ for it in items],
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
