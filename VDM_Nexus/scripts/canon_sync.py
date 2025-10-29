#!/usr/bin/env python3
"""
VDM Nexus — CanonSync CLI (skeleton)

Read-only helper to surface canonical anchors and prepare for future indexing.
Does not write to Derivation/ or modify repository state.

Usage:
  python VDM_Nexus/scripts/canon_sync.py --print
  python VDM_Nexus/scripts/canon_sync.py --json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "nexus.config.json"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {"error": f"missing config at {CONFIG_PATH}"}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as e:
        return {"error": f"failed to parse config: {e}"}


def main() -> int:
    parser = argparse.ArgumentParser(description="CanonSync (read-only) — print configured anchors")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--print", action="store_true", help="Pretty print to stdout")
    args = parser.parse_args()

    cfg = load_config()
    if args.json:
        print(json.dumps({"config": cfg}, indent=2, sort_keys=True))
    else:
        print("== CanonSync (read-only) ==")
        if "error" in cfg:
            print(f"Config error: {cfg['error']}")
        else:
            canon = cfg.get("canon", {})
            print("Anchors:")
            for k, v in canon.items():
                print(f" - {k}: {v}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
