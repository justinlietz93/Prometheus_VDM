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


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Generate salted provenance hashes for files")
    p.add_argument("files", nargs="+", help="Files to hash")
    p.add_argument("--salt", help="Hex salt to use (applied to all files). If omitted, salt is generated.")
    p.add_argument("--single-salt", action="store_true", help="Use a single random salt for all files (ignored if --salt is provided)")
    p.add_argument("--salt-bytes", type=int, default=16, help="Number of random salt bytes when generating (default: 16)")
    p.add_argument("--text", action="store_true", help="Emit human-readable text instead of JSON")

    args = p.parse_args(argv)

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
