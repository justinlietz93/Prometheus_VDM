"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Core seam: temporary adapter that forwards to existing Nexus internals without changing behavior.

Phase B goal:
- Define a stable Core API now to avoid rework later.
- Do NOT move logic yet; keep Nexus as source of truth.
- These methods either delegate to existing functions or act as explicit stubs.

Seam policy:
- This module must not import from fum_rt.io.* or fum_rt.runtime.* to keep core isolated.
- Only depend on fum_rt.core.* and the Nexus-like object passed at construction.
"""

from typing import Any, Dict, Optional
from fum_rt.core.metrics import compute_metrics
from fum_rt.core.memory import load_engram as _load_engram_state, save_checkpoint as _save_checkpoint


class CoreEngine:
    """
    Temporary adapter (seam) to the current runtime.

    - step(): intentionally left unimplemented to avoid duplicating the run-loop logic.
    - snapshot(): exposes a minimal, safe snapshot using current metrics.
    - engram_load(): pass-through to the legacy loader.
    - engram_save(): pass-through to the legacy saver (saves into run_dir; path argument is advisory).
    """

    def __init__(self, nexus_like: Any) -> None:
        """
        nexus_like: an instance exposing the attributes currently used by the runtime:
          - connectome, adc, run_dir, checkpoint_format (optional), logger (optional), _phase (optional)
        """
        self._nx = nexus_like

    def step(self, dt_ms: int, ext_events: list) -> None:
        """
        Seam-only placeholder. The orchestrator still drives per-tick behavior inside Nexus.
        Introduced now to freeze the API; implementation will be wired after migration with parity checks.
        """
        raise NotImplementedError("CoreEngine.step seam is defined but not active; orchestrator retains control.")

    def snapshot(self) -> Dict[str, Any]:
        """
        Build a minimal state snapshot via current compute_metrics without mutating the model.
        Adds common context fields used by Why providers when available.
        """
        nx = self._nx
        m = compute_metrics(nx.connectome)
        # Attach minimal, non-intrusive context
        try:
            m["t"] = int(getattr(nx, "_emit_step", 0))
        except Exception:
            pass
        try:
            m["phase"] = int(getattr(nx, "_phase", {}).get("phase", 0))
        except Exception:
            pass
        return m

    def engram_load(self, path: str) -> None:
        """
        Pass-through to the existing engram loader with ADC included when available.
        Mirrors the call used in Nexus, preserving logs/events and behavior.
        """
        nx = self._nx
        _load_engram_state(str(path), nx.connectome, adc=getattr(nx, "adc", None))
        # Optional: let the caller log; we keep core side-effect free except the actual load.

    def engram_save(self, path: Optional[str] = None, step: Optional[int] = None, fmt: Optional[str] = None) -> str:
        """
        Pass-through to the existing checkpoint saver. Saves into nx.run_dir using the legacy naming scheme.
        Arguments:
          - path: advisory only (ignored by the legacy saver, which chooses its own path under run_dir)
          - step: when None, the caller should provide an explicit step; if missing, a safe default is used (0)
          - fmt: optional override for format (e.g., 'h5' or 'npz'); defaults to nx.checkpoint_format or 'h5'

        Returns:
          The filesystem path returned by the legacy saver.
        """
        nx = self._nx
        use_step = int(step if step is not None else getattr(nx, "_emit_step", 0))
        use_fmt = str(fmt if fmt is not None else getattr(nx, "checkpoint_format", "h5") or "h5")
        return _save_checkpoint(nx.run_dir, use_step, nx.connectome, fmt=use_fmt, adc=getattr(nx, "adc", None))


__all__ = ["CoreEngine"]