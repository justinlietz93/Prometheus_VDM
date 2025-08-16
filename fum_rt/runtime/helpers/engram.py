"""
Runtime helper: engram load and start-step derivation.

Behavior:
- maybe_load_engram(nx, path): loads engram state into connectome (and ADC if present), logs outcome.
- derive_start_step(nx, path): derives starting tick index based on provided path or existing state_* files.

This module provides the real implementations migrated from the legacy runtime_helpers monolith.
"""

from __future__ import annotations

from typing import Any, Optional
import os
import re

from fum_rt.core.memory import load_engram as _load_engram_state


def maybe_load_engram(nx: Any, load_engram_path: Optional[str]) -> None:
    """
    If a path is provided, load the engram into nx.connectome (and nx.adc when present),
    logging the result into nx.logger for UI confirmation. Mirrors legacy behavior.
    """
    if not load_engram_path:
        return
    try:
        _load_engram_state(str(load_engram_path), nx.connectome, adc=getattr(nx, "adc", None))
        try:
            nx.logger.info("engram_loaded", extra={"extra": {"path": str(load_engram_path)}})
        except Exception:
            pass
    except Exception as e:
        try:
            nx.logger.info("engram_load_error", extra={"extra": {"err": str(e), "path": str(load_engram_path)}})
        except Exception:
            pass


def derive_start_step(nx: Any, load_engram_path: Optional[str]) -> int:
    """
    Derive starting step to continue numbering after resume, avoiding retention deleting
    new snapshots. Mirrors original logic including filename parsing and fallback scan.

    Policy:
    - If load_engram_path points to a state file named like state_<step>.(h5|npz), return step+1
    - Else scan nx.run_dir for the highest state_<step>.(h5|npz) and return highest+1
    - Else return 0
    """
    try:
        s: Optional[int] = None
        lp = str(load_engram_path) if load_engram_path else None
        if lp and os.path.isfile(lp):
            base = os.path.basename(lp)
            m = re.search(r"state_(\d+)\.(h5|npz)$", base)
            if m:
                s = int(m.group(1))
        if s is None:
            max_s = -1
            for fn in os.listdir(nx.run_dir):
                if not fn.startswith("state_"):
                    continue
                m2 = re.search(r"state_(\d+)\.(h5|npz)$", fn)
                if m2:
                    ss = int(m2.group(1))
                    if ss > max_s:
                        max_s = ss
            if max_s >= 0:
                s = max_s
        return int(s) + 1 if s is not None else 0
    except Exception:
        return 0


__all__ = ["maybe_load_engram", "derive_start_step"]