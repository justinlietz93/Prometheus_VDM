#!/usr/bin/env python3
"""Stamp a proposal and its preregistration with canonical salted provenance.

Usage:
  python Derivation/code/common/provenance/stamp_proposal.py --proposal PATH --prereg PATH [--salt-bytes N]

What it does:
 - Reads the prereg JSON and finds the first spec reference (spec_refs[0]).
 - If prereg already contains a structured `salted_provenance` with items, uses the first item.
 - Otherwise computes base SHA256 for the spec, generates a random salt (default 16 bytes), computes salted_sha256 = sha256(base:salt), and writes a structured `salted_provenance` object into prereg.
 - Computes prereg manifest SHA256 and then inserts (or replaces) a canonical "Salted Provenance" header line into the proposal file.

This helper ensures the proposal header and prereg are canonical for the approval gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        while True:
            b = f.read(1024 * 1024)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def compute_salted(base_hex: str, salt_hex: str) -> str:
    return hashlib.sha256(f"{base_hex}:{salt_hex}".encode("utf-8")).hexdigest()


def build_salted_provenance_for_spec(spec_path: Path, salt_bytes: int = 16) -> dict:
    base = sha256_file(spec_path)
    size = spec_path.stat().st_size
    salt_hex = secrets.token_hex(salt_bytes)
    salted = compute_salted(base, salt_hex)
    return {
        "schema": "vdm.provenance.salted_hash.v1",
        "generated_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "salt_bytes": int(salt_bytes),
        "single_salt": True,
        "salt_hex": salt_hex,
        "items": [
            {
                "path": str(spec_path),
                "size": int(size),
                "base_sha256": base,
                "salt_hex": salt_hex,
                "salted_sha256": salted,
            }
        ],
    }


def insert_or_replace_header(proposal_path: Path, salted_sha256: str, salt_hex: str, prereg_manifest: str) -> None:
    txt = proposal_path.read_text(encoding="utf-8")
    header_line = f"Salted Provenance: spec salted_sha256={salted_sha256}; salt_hex={salt_hex}; prereg_manifest_sha256={prereg_manifest}"

    import re

    # replace existing line if present
    m = re.search(r"Salted\s+Provenance:.*prereg_manifest_sha256=[0-9a-fA-F]{64}", txt)
    if m:
        txt = txt[: m.start()] + header_line + txt[m.end():]
    else:
        # Try to insert after the commit line (first occurrence of 'Commit')
        lines = txt.splitlines()
        inserted = False
        for i, ln in enumerate(lines):
            if "Commit" in ln:
                # insert after this line as a quoted block for readability
                lines.insert(i + 1, f"> {header_line}  ")
                inserted = True
                break
        if not inserted:
            # Prepend
            lines.insert(0, f"> {header_line}  ")
        txt = "\n".join(lines) + "\n"

    proposal_path.write_text(txt, encoding="utf-8")


def main(argv: Optional[list[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--proposal", required=True, help="Path to proposal markdown file")
    p.add_argument("--prereg", required=True, help="Path to preregistration JSON file")
    p.add_argument("--salt-bytes", type=int, default=16, help="Bytes of random salt to generate")
    args = p.parse_args(argv)
    try:
        stamp(args.proposal, args.prereg, salt_bytes=args.salt_bytes)
        return 0
    except Exception:
        return 1


def stamp(proposal: str | Path, prereg: str | Path, *, salt_bytes: int = 16) -> Dict[str, Any]:
    """Public function: stamp a proposal/prereg. Returns a dict summary.

    This raises exceptions on fatal errors so callers can handle them.
    """
    proposal = Path(proposal)
    prereg = Path(prereg)
    if not proposal.exists():
        raise FileNotFoundError(f"proposal not found: {proposal}")
    if not prereg.exists():
        raise FileNotFoundError(f"prereg not found: {prereg}")

    # Load prereg
    pdata = json.loads(prereg.read_text(encoding="utf-8"))

    prov = pdata.get("salted_provenance")
    use_existing = False
    if isinstance(prov, dict) and prov.get("items"):
        # Validate first item is non-placeholder; otherwise recompute
        it0_try = prov["items"][0]
        size0 = int(it0_try.get("size") or 0)
        base0 = str(it0_try.get("base_sha256") or "")
        salted0 = str(it0_try.get("salted_sha256") or "")
        salt_hex0 = str(it0_try.get("salt_hex") or "")
        if size0 > 0 and base0 and salted0 and salt_hex0:
            salted_sha256 = salted0
            salt_hex = salt_hex0
            use_existing = True
    if not use_existing:
        # Need to compute from spec_refs
        spec_refs = pdata.get("spec_refs") or pdata.get("specs") or []
        if not spec_refs or not isinstance(spec_refs, list):
            raise ValueError("prereg has no spec_refs to compute provenance from")
        # resolve spec path relative to prereg
        spec_path = Path(spec_refs[0])
        if not spec_path.is_absolute():
            spec_path = (prereg.parent / spec_path).resolve()
        if not spec_path.exists():
            raise FileNotFoundError(f"spec referenced by prereg not found: {spec_path}")
        newprov = build_salted_provenance_for_spec(spec_path, salt_bytes=salt_bytes)
        pdata["salted_provenance"] = newprov
        # write prereg back
        prereg.write_text(json.dumps(pdata, indent=2) + "\n", encoding="utf-8")
        it0 = newprov["items"][0]
        salted_sha256 = it0["salted_sha256"]
        salt_hex = it0["salt_hex"]

    # compute prereg manifest sha
    manifest = sha256_file(prereg)

    # Insert header into proposal
    insert_or_replace_header(proposal, salted_sha256, salt_hex, manifest)

    return {"proposal": str(proposal), "prereg": str(prereg), "salted_sha256": salted_sha256, "salt_hex": salt_hex, "prereg_manifest": manifest}


if __name__ == "__main__":
    raise SystemExit(main())
