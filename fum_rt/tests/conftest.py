"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Pytest configuration: ensure repo root on sys.path so 'import fum_rt' works when running tests directly.
No heavy imports; minimal stdlib only.
"""

import os as _os
import sys as _sys
from pathlib import Path as _Path

def _project_root(start: _Path | None = None) -> _Path:
    cur = (start or _Path(__file__)).resolve().parent
    for _ in range(10):
        if (cur / "fum_rt").is_dir():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    # Fallback: two parents up from this file
    return (start or _Path(__file__)).resolve().parents[2]

# Put repository root on sys.path if missing
try:
    _root = _project_root()
    _root_str = str(_root)
    if _root_str not in _sys.path:
        _sys.path.insert(0, _root_str)
except Exception:
    pass