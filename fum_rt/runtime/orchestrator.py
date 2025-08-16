"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime orchestrator seam (Phase B): move-only adapter that preserves behavior.

Goals:
- Freeze the orchestrator-facing API now with a clean core boundary.
- Do NOT change behavior: default run-path delegates to the existing Nexus.run().
- Provide pass-throughs to the CoreEngine seam for snapshot/engram ops.
- Keep IO/emitters/telemetry packaging out of core; this module does not serialize JSON.

Policy:
- This module may import core.* but must not import io.* emitters directly.
- The actual per-tick logic remains inside Nexus until Phase C/D migration.
"""

from typing import Any, Dict, List, Optional

from fum_rt.core.engine import CoreEngine


class Orchestrator:
    """
    Thin façade over the existing Nexus instance.

    Behavior:
    - run(): delegates 1:1 to Nexus.run() to guarantee parity.
    - step(): defined to lock the seam; calls CoreEngine.step() (which is a placeholder for now).
    - snapshot(): returns a minimal numeric snapshot from CoreEngine (used by telemetry packagers).
    - read_bus(): drains announce-bus events from the underlying Nexus (for ADC folds at higher layers).
    - engram_load/save(): pass-through to CoreEngine helpers which call legacy functions internally.
    """

    def __init__(self, nexus_like: Any, engine: Optional[CoreEngine] = None) -> None:
        """
        nexus_like: current Nexus instance (source of truth during migration)
        engine: optional CoreEngine; if None, constructed with nexus_like
        """
        self._nx = nexus_like
        self._engine = engine or CoreEngine(nexus_like)

    # Phase A: default orchestration delegates to the current Nexus loop for exact parity.
    def run(self, duration_s: Optional[int] = None) -> None:
        """
        Execute the main loop using the existing Nexus implementation.
        This preserves timing, pacing, logging, checkpointing, and emission behavior exactly.
        """
        return self._nx.run(duration_s=duration_s)

    # Phase B seam: defined but not active in the default path until internals migrate.
    def step(self, dt_ms: int, ext_events: Optional[List[Any]] = None) -> None:
        """
        Single-tick step via CoreEngine (seam). Not used in the default run-path yet.
        Exists to lock the API; implementation will be wired in Phase C without behavior changes.
        """
        return self._engine.step(dt_ms=int(dt_ms), ext_events=list(ext_events or []))

    def snapshot(self) -> Dict[str, Any]:
        """
        Numeric snapshot for telemetry packaging (outside core).
        Safe and read-only; never mutates the model.
        """
        return self._engine.snapshot()

    def read_bus(self, max_items: int = 2048) -> List[Any]:
        """
        Drain announcement bus from the underlying Nexus for ADC folding at higher layers.
        This keeps ADC I/O inside the runtime layer and core strictly numeric.
        """
        try:
            bus = getattr(self._nx, "bus", None)
            if bus is None:
                return []
            return list(bus.drain(max_items=int(max_items)) or [])
        except Exception:
            return []

    def engram_load(self, path: str) -> None:
        """
        Load an engram via CoreEngine pass-through (calls legacy loader internally).
        """
        return self._engine.engram_load(path)

    def engram_save(self, step: Optional[int] = None, fmt: Optional[str] = None) -> str:
        """
        Save a checkpoint via CoreEngine pass-through (calls legacy saver internally).
        Returns the saved filesystem path.
        """
        return self._engine.engram_save(step=step, fmt=fmt)


__all__ = ["Orchestrator"]