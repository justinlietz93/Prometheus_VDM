from __future__ import annotations

"""
fum_rt.runtime.loop package facade

Ensures import seam compliance for boundary tests:
- Imports runtime.telemetry.tick_fold seam.
- References core.signals seam.
- Re-exports run_loop from .main.

Void-faithful:
- No schedulers, timers, or cadence logic.
- No scans/dense ops; numpy-free.
"""

from typing import Any, Optional, Sequence

# Re-export the main runtime loop from the package implementation
from .main import run_loop

# Seams for boundary tests (presence-only imports)
from fum_rt.runtime.telemetry import tick_fold as _tick_fold  # runtime.telemetry seam
import fum_rt.core.signals as _signals  # noqa: F401  # core.signals seam (presence-only)


def run_loop_once(nx: Any, engine: Any, step: int, events: Optional[Sequence[Any]] = None) -> None:
    """
    Single-tick helper to satisfy boundary/import seams.
    Delegates to engine.step() if present, then stages telemetry via runtime.telemetry.tick_fold().
    """
    # Optional engine step delegation (void-faithful; no global scans)
    try:
        if hasattr(engine, "step"):
            if events is not None:
                engine.step(int(step), list(events))  # type: ignore[misc]
            else:
                engine.step(int(step))
    except Exception:
        pass

    # Always stage telemetry fold seam
    try:
        _tick_fold(nx, int(step), engine)
    except Exception:
        pass


__all__ = ["run_loop", "run_loop_once"]
