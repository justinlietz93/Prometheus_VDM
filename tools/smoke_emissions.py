#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Smoke emissions verifier.

Purpose:
- Quick, non-invasive verification that a completed run directory has expected artifacts:
  * runs/<ts>/utd_events.jsonl with at least one macro emission (default: 'say'), and optionally 'status'
  * runs/<ts>/events.jsonl with at least one 'tick' record
  * (optional) runs/<ts>/thoughts.ndjson with at least one 'thought' record when ENABLE_THOUGHTS=1

Exit codes:
- 0 on pass
- 1 on failure

Usage:
  python tools/smoke_emissions.py --run runs/2025-08-10_21-00-00
  python tools/smoke_emissions.py --run runs/A --macro say --require-status
  python tools/smoke_emissions.py --run runs/B --require-thoughts

Notes:
- This script only inspects files; it does not run the model.
- It is robust to minor schema differences and ignores malformed lines.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Iterable, Optional


def _read_ndjson(path: str) -> Iterable[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except Exception:
                    continue
                if isinstance(rec, dict):
                    yield rec
    except Exception:
        return []


def _find(path: str, name: str) -> Optional[str]:
    p = os.path.join(path, name)
    return p if os.path.exists(p) else None


def verify_utd(run_dir: str, macro_name: str, require_status: bool) -> tuple[bool, str]:
    p = _find(run_dir, "utd_events.jsonl")
    if not p:
        return False, "missing utd_events.jsonl"

    macro_count = 0
    status_macro = 0
    for rec in _read_ndjson(p):
        try:
            if rec.get("type") == "macro":
                mname = str(rec.get("macro", "")).strip().lower()
                if mname == macro_name:
                    macro_count += 1
                if mname == "status":
                    status_macro += 1
        except Exception:
            continue

    if macro_count <= 0:
        return False, f"no '{macro_name}' macro found in utd_events.jsonl"

    if require_status and status_macro <= 0:
        return False, "no 'status' macro found in utd_events.jsonl (require-status enabled)"

    return True, f"utd ok: {macro_name}={macro_count}, status={status_macro}"


def verify_ticks(run_dir: str) -> tuple[bool, str]:
    p = _find(run_dir, "events.jsonl")
    if not p:
        return False, "missing events.jsonl"

    ticks = 0

    def _get_msg(rec: Dict[str, Any]) -> str:
        # Accept common JSON logger keys. Our runtime uses 'msg' in [get_logger](fum_rt/utils/logging_setup.py:22).
        return str(
            rec.get("message")
            or rec.get("event")
            or rec.get("name")
            or rec.get("type")
            or rec.get("msg")
            or ""
        ).lower()

    for rec in _read_ndjson(p):
        try:
            if _get_msg(rec) == "tick":
                ticks += 1
        except Exception:
            continue

    if ticks <= 0:
        return False, "no 'tick' entries in events.jsonl"
    return True, f"ticks ok: {ticks}"


def verify_thoughts(run_dir: str, require: bool) -> tuple[bool, str]:
    p = _find(run_dir, "thoughts.ndjson")
    if not p:
        return (not require), ("missing thoughts.ndjson" if require else "thoughts absent (ok)")

    count = 0
    for rec in _read_ndjson(p):
        try:
            if str(rec.get("type", "")).lower() == "thought":
                count += 1
        except Exception:
            continue

    if require and count <= 0:
        return False, "no 'thought' entries in thoughts.ndjson (require-thoughts enabled)"
    return True, f"thoughts ok: {count}"


def main():
    ap = argparse.ArgumentParser(description="Smoke emissions verifier for a FUM run directory.")
    ap.add_argument("--run", required=True, help="Path to a run directory (e.g., runs/2025-08-10_21-00-00)")
    ap.add_argument("--macro", default="say", help="Macro name expected at least once (default: say)")
    ap.add_argument("--require-status", action="store_true", help="Require a 'status' macro emission")
    ap.add_argument("--require-thoughts", action="store_true", help="Require at least one 'thought' record in thoughts.ndjson")
    args = ap.parse_args()

    failures: list[str] = []
    messages: list[str] = []

    ok, msg = verify_utd(args.run, macro_name=args.macro, require_status=args.require_status)
    messages.append(msg)
    if not ok:
        failures.append(msg)

    ok, msg = verify_ticks(args.run)
    messages.append(msg)
    if not ok:
        failures.append(msg)

    ok, msg = verify_thoughts(args.run, require=args.require_thoughts)
    messages.append(msg)
    if not ok:
        failures.append(msg)

    print("=== Smoke Emissions Report ===")
    print(f"Run: {args.run}")
    for m in messages:
        print("-", m)

    if failures:
        print("RESULT: FAIL")
        sys.exit(1)
    else:
        print("RESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()