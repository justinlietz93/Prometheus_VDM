"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime retention policy seam (Phase B): pure helper for checkpoint pruning.

Goals:
- Mirror Nexus inline retention logic exactly (move-only).
- No logging or external IO besides file deletions.
- Return a small summary dict so callers can decide how/what to log.

Usage pattern (as in Nexus today, adapted to this helper):
    path = save_checkpoint(run_dir, step, connectome, fmt=fmt, adc=adc)
    summary = prune_checkpoints(run_dir, keep=checkpoint_keep, last_path=path)
    # optional: logger.info("checkpoint_retention", extra={"extra": summary})

Behavior:
- If keep is falsy or <= 0, no action (returns {"kept": 0, "removed": 0, "ext": ext}).
- Determines extension from last_path.
- Keeps the most recent <= keep checkpoints based on numeric step parsed from filenames.
- Files are expected to be named "state_<step><ext>" as produced by the legacy saver.
"""

import os
from typing import Dict, Optional


def prune_checkpoints(run_dir: str, keep: int, last_path: Optional[str] = None) -> Dict[str, int | str]:
    """
    Enforce rolling checkpoint retention in run_dir using the same rules as Nexus.

    Parameters:
        run_dir: directory where checkpoints reside (e.g., runs/<timestamp>)
        keep: number of newest checkpoints to keep (0 disables pruning)
        last_path: the full path returned by the last save_checkpoint call (to derive extension)

    Returns:
        A summary dict: {"kept": int, "removed": int, "ext": str}
    """
    kept = int(max(0, int(keep))) if keep is not None else 0

    # Determine extension (e.g., ".h5" or ".npz")
    if isinstance(last_path, str) and last_path:
        ext = os.path.splitext(last_path)[1].lower()
    else:
        # Fallback: prefer ".h5" if present, else ".npz", else empty
        ext = ""
        try:
            candidates = [fn for fn in os.listdir(run_dir) if fn.startswith("state_")]
            if any(fn.endswith(".h5") for fn in candidates):
                ext = ".h5"
            elif any(fn.endswith(".npz") for fn in candidates):
                ext = ".npz"
        except Exception:
            pass

    if kept <= 0 or not isinstance(run_dir, str) or not run_dir:
        return {"kept": 0, "removed": 0, "ext": ext}

    files = []
    try:
        for fn in os.listdir(run_dir):
            if not fn.startswith("state_"):
                continue
            if ext and not fn.endswith(ext):
                continue
            # Extract numeric step: "state_<step><ext>"
            try:
                if ext:
                    step_str = fn[6:-len(ext)]
                else:
                    step_str = fn[6:]
                s = int(step_str)
                files.append((s, fn))
            except Exception:
                # Skip files that do not match the expected pattern
                continue
    except Exception:
        return {"kept": kept, "removed": 0, "ext": ext}

    if len(files) <= kept:
        return {"kept": kept, "removed": 0, "ext": ext}

    files.sort(key=lambda x: x[0], reverse=True)
    to_delete = files[kept:]
    removed = 0
    for _, fn in to_delete:
        try:
            os.remove(os.path.join(run_dir, fn))
            removed += 1
        except Exception:
            # Best-effort deletion; continue pruning others
            continue

    return {"kept": kept, "removed": removed, "ext": ext}


__all__ = ["prune_checkpoints"]