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
from fum_rt.core.proprioception.events import EventDrivenMetrics as _EvtMetrics
from fum_rt.core.cortex.scouts import VoidColdScoutWalker as _VoidScout


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
        # Event-driven stack (lazy-initialized)
        self._evt_metrics = None
        self._void_scout = None
        self._last_evt_snapshot: Dict[str, Any] = {}

    def step(self, dt_ms: int, ext_events: list) -> None:
        """
        Fold provided core events and cold-scout events into event-driven reducers.
        Pure core; no IO/logging. Read-only against connectome.
        """
        # lazy init local reducers and VOID scout
        try:
            self._ensure_evt_init()
        except Exception:
            pass

        if getattr(self, "_evt_metrics", None) is None:
            return

        # 1) fold external events (already core BaseEvent subclasses from runtime adapter)
        try:
            for ev in (ext_events or []):
                try:
                    # accept any object exposing 'kind' attribute (duck-typed BaseEvent)
                    if hasattr(ev, "kind"):
                        self._evt_metrics.update(ev)
                except Exception:
                    continue
        except Exception:
            pass

        # 2) fold VOID cold-scout reads (read-only traversal)
        try:
            if getattr(self, "_void_scout", None) is not None:
                tick = int(getattr(self._nx, "_emit_step", 0))
                for _ev in self._void_scout.step(getattr(self, "_nx", None).connectome, tick) or []:
                    try:
                        self._evt_metrics.update(_ev)
                    except Exception:
                        continue
        except Exception:
            pass

        # 3) refresh cached evt snapshot
        try:
            self._last_evt_snapshot = dict(self._evt_metrics.snapshot() or {})
        except Exception:
            self._last_evt_snapshot = {}

    def _ensure_evt_init(self) -> None:
        """
        Initialize event-driven reducers (EventDrivenMetrics) and VOID scout lazily
        using configuration exposed by the nexus-like object when available.
        """
        # reducers
        if getattr(self, "_evt_metrics", None) is None:
            try:
                det = getattr(self._nx, "b1_detector", None)
                z_spike = float(getattr(det, "z_spike", 1.0)) if det is not None else 1.0
                hysteresis = float(getattr(det, "hysteresis", 1.0)) if det is not None else 1.0
                half_life = int(getattr(self._nx, "b1_half_life_ticks", 50))
                seed = int(getattr(self._nx, "seed", 0))
                self._evt_metrics = _EvtMetrics(
                    z_half_life_ticks=max(1, half_life),
                    z_spike=z_spike,
                    hysteresis=hysteresis,
                    seed=seed,
                )
            except Exception:
                self._evt_metrics = None
        # VOID scout
        if getattr(self, "_void_scout", None) is None:
            try:
                sv = int(getattr(self._nx, "scout_visits", 16))
            except Exception:
                sv = 16
            try:
                se = int(getattr(self._nx, "scout_edges", 8))
            except Exception:
                se = 8
            try:
                seed = int(getattr(self._nx, "seed", 0))
            except Exception:
                seed = 0
            try:
                self._void_scout = _VoidScout(budget_visits=max(0, sv), budget_edges=max(0, se), seed=seed)
            except Exception:
                self._void_scout = None

    def snapshot(self) -> Dict[str, Any]:
        """
        Build a minimal state snapshot via current compute_metrics without mutating the model.
        Adds common context fields used by Why providers when available.
        Also merges cached event-driven metrics under an 'evt_' prefix to preserve canonical fields.
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
        # Merge event-driven snapshot without overriding canonical keys
        try:
            evs = getattr(self, "_last_evt_snapshot", None)
            if isinstance(evs, dict):
                for k, v in evs.items():
                    try:
                        # preserve existing canonical b1_* if present
                        if str(k).startswith("b1_") and k in m:
                            continue
                        m[f"evt_{k}"] = v
                    except Exception:
                        continue
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