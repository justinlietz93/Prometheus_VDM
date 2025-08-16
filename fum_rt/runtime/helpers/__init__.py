"""
Runtime helpers package (modularized).

Transitional re-exports:
- During migration away from the monolith [runtime_helpers.py](../runtime_helpers.py), we re-export
  its functions here to provide a stable import path:
    from fum_rt.runtime.helpers import process_messages, emit_status_and_macro, ...
- New helpers live as separate modules under this package (e.g., maps_ws.py).
"""

from __future__ import annotations

# New, modular helpers
from .maps_ws import maybe_start_maps_ws  # re-export
from .macro_board import register_macro_board  # re-export (modular)

# Transitional re-exports from the legacy monolith for compatibility
try:
    from fum_rt.runtime.runtime_helpers import (  # type: ignore
        maybe_load_engram,
        derive_start_step,
        process_messages,
        maybe_smoke_tests,
        maybe_auto_speak,
        emit_status_and_macro,
        maybe_visualize,
        save_tick_checkpoint,
    )
except Exception:
    # Provide no-op fallbacks to avoid import failures during partial migrations

    def maybe_load_engram(*args, **kwargs):  # type: ignore
        return None

    def derive_start_step(*args, **kwargs):  # type: ignore
        return 0

    def process_messages(*args, **kwargs):  # type: ignore
        return 0, set(), set(), {}

    def maybe_smoke_tests(*args, **kwargs):  # type: ignore
        return None

    def maybe_auto_speak(*args, **kwargs):  # type: ignore
        return None

    def emit_status_and_macro(*args, **kwargs):  # type: ignore
        return None

    def maybe_visualize(*args, **kwargs):  # type: ignore
        return None

    def save_tick_checkpoint(*args, **kwargs):  # type: ignore
        return None

__all__ = [
    # New helpers
    "maybe_start_maps_ws",
    # Transitional re-exports
    "register_macro_board",
    "maybe_load_engram",
    "derive_start_step",
    "process_messages",
    "maybe_smoke_tests",
    "maybe_auto_speak",
    "emit_status_and_macro",
    "maybe_visualize",
    "save_tick_checkpoint",
]