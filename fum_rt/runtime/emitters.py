from __future__ import annotations

"""
Runtime emitters initialization (MacroEmitter, ThoughtEmitter).

Behavior:
- Mirrors Nexus inline initialization exactly:
  * MacroEmitter path priority: $UTD_OUT or utd.path or <run_dir>/utd_events.jsonl
  * ThoughtEmitter enabled only when ENABLE_THOUGHTS in ("1","true","yes","on")
    path priority: $THOUGHT_OUT or <run_dir>/thoughts.ndjson
- Returns (macro_emitter_or_None, thought_emitter_or_None)
- No logging or file writes here (pure construction).
"""

from typing import Any, Callable, Optional, Tuple
import os

# IO-layer actuators (allowed in runtime layer)
from fum_rt.io.actuators.macros import MacroEmitter
from fum_rt.io.actuators.thoughts import ThoughtEmitter


def initialize_emitters(
    utd: Any,
    run_dir: str,
    why_provider: Callable[[], dict],
) -> Tuple[Optional[MacroEmitter], Optional[ThoughtEmitter]]:
    """
    Create MacroEmitter and ThoughtEmitter with legacy-equivalent configuration.
    """
    macro: Optional[MacroEmitter] = None
    thoughts: Optional[ThoughtEmitter] = None

    # Macro emitter (write-only; respects UTD_OUT if set)
    try:
        out_path = os.getenv("UTD_OUT") or getattr(utd, "path", None) or os.path.join(run_dir, "utd_events.jsonl")
        macro = MacroEmitter(path=str(out_path), why_provider=why_provider)
    except Exception:
        macro = None

    # Introspection Ledger (emit-only), behind feature flag ENABLE_THOUGHTS
    try:
        if str(os.getenv("ENABLE_THOUGHTS", "0")).lower() in ("1", "true", "yes", "on"):
            th_path = os.getenv("THOUGHT_OUT") or os.path.join(run_dir, "thoughts.ndjson")
            thoughts = ThoughtEmitter(path=str(th_path), why=why_provider)
    except Exception:
        thoughts = None

    return macro, thoughts


__all__ = ["initialize_emitters"]