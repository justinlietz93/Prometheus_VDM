"""
Runtime helper: macro board registration on UTD emitter.

Behavior:
- Registers default macros ('status', 'say')
- Loads per-run macro_board.json entries only (no external fallbacks)
"""

from __future__ import annotations

import os
import json
from typing import Any


def register_macro_board(utd: Any, run_dir: str) -> None:
    """
    Register default macros and optional per-run macro_board.json entries on a UTD-like emitter.
    Mirrors legacy behavior:
      - Always register 'status' and 'say'
      - Optionally load runs/<ts>/macro_board.json (dict of name -> meta)
      - Only per-run board can provide metadata/templates to preserve emergent language
    """
    try:
        utd.register_macro("status", {"desc": "Emit structured status payload"})
    except Exception:
        pass
    try:
        utd.register_macro("say", {"desc": "Emit plain text line"})
    except Exception:
        pass

    # Per-run macro_board.json
    try:
        pth = os.path.join(run_dir, "macro_board.json")
        if os.path.exists(pth):
            with open(pth, "r", encoding="utf-8") as fh:
                reg = json.load(fh)
            if isinstance(reg, dict):
                for name, meta in reg.items():
                    try:
                        utd.register_macro(str(name), meta if isinstance(meta, dict) else {})
                    except Exception:
                        pass
    except Exception:
        pass

    # External fallbacks removed by repository policy: macros must originate from per-run files.


__all__ = ["register_macro_board"]