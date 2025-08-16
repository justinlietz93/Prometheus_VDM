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

Separation policy:
- This module must not import from fum_rt.io.* or fum_rt.runtime.* to keep core isolated.
- Only depend on fum_rt.core.* and the Nexus-like object passed at construction.
"""

from typing import Any, Dict, Optional, Tuple

from fum_rt.core.metrics import compute_metrics
from fum_rt.core.memory import (
    load_engram as _load_engram_state,
    save_checkpoint as _save_checkpoint,
)
from fum_rt.core.proprioception.events import EventDrivenMetrics as _EvtMetrics
from fum_rt.core.cortex.scouts import VoidColdScoutWalker as _VoidScout, ColdMap as _ColdMap
from fum_rt.core.cortex.maps.heatmap import HeatMap as _HeatMap
from fum_rt.core.cortex.maps.excitationmap import ExcitationMap as _ExcMap
from fum_rt.core.cortex.maps.inhibitionmap import InhibitionMap as _InhMap
from fum_rt.core.signals import (
    compute_active_edge_density as _sig_density,
    compute_td_signal as _sig_td,
    compute_firing_var as _sig_fvar,
)

# Local helpers (telemetry-only; remain inside core boundary)
from .maps_frame import stage_maps_frame
from .evt_snapshot import build_evt_snapshot


class CoreEngine:
    """
    Temporary adapter (seam) to the current runtime.

    - step(): folds event-driven reducers (no IO/logging) and stages maps/frame for telemetry.
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
        # Public alias for tests and adapters that expect a public handle
        try:
            self.nx = self._nx  # test convenience: allows eng.nx access
        except Exception:
            pass
        # Event-driven stack (lazy-initialized)
        self._evt_metrics: Optional[_EvtMetrics] = None
        self._void_scout: Optional[_VoidScout] = None
        self._cold_map: Optional[_ColdMap] = None
        self._heat_map: Optional[_HeatMap] = None
        self._exc_map: Optional[_ExcMap] = None
        self._inh_map: Optional[_InhMap] = None
        self._last_evt_snapshot: Dict[str, Any] = {}

    # ---- Event-driven fold and telemetry staging ----
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

        # latest tick observed this step (from ext events or scout)
        latest_tick = None
        collected_events: list = []

        # 1) fold external events (already core BaseEvent subclasses from runtime adapter)
        try:
            for ev in (ext_events or []):
                try:
                    # accept any object exposing 'kind' attribute (duck-typed BaseEvent)
                    if hasattr(ev, "kind"):
                        self._evt_metrics.update(ev)
                        collected_events.append(ev)
                        # update cold-map on node touches/endpoints when possible
                        if getattr(self, "_cold_map", None) is not None:
                            try:
                                kind = getattr(ev, "kind", "")
                                t_ev = getattr(ev, "t", None)
                                if t_ev is not None:
                                    if kind == "vt_touch":
                                        token = getattr(ev, "token", None)
                                        if isinstance(token, int) and token >= 0:
                                            self._cold_map.touch(int(token), int(t_ev))
                                    elif kind == "edge_on":
                                        u = getattr(ev, "u", None)
                                        v = getattr(ev, "v", None)
                                        if isinstance(u, int) and u >= 0:
                                            self._cold_map.touch(int(u), int(t_ev))
                                        if isinstance(v, int) and v >= 0:
                                            self._cold_map.touch(int(v), int(t_ev))
                            except Exception:
                                pass
                        # track latest tick seen
                        try:
                            tv = getattr(ev, "t", None)
                            if tv is not None:
                                if latest_tick is None or int(tv) > int(latest_tick):
                                    latest_tick = int(tv)
                        except Exception:
                            pass
                except Exception:
                    continue
        except Exception:
            pass

        # 2) fold VOID cold-scout reads (read-only traversal)
        try:
            if getattr(self, "_void_scout", None) is not None:
                # Prefer explicit tick from external events; fallback to predicted next tick.
                tick_hint = None
                try:
                    if ext_events:
                        # Pick the last event with a valid 't' (most recent)
                        for _e in reversed(ext_events):
                            tv = getattr(_e, "t", None)
                            if tv is not None:
                                tick_hint = int(tv)
                                break
                except Exception:
                    tick_hint = None
                if tick_hint is None:
                    try:
                        # Use next tick relative to last emitted step (updated later in runtime loop)
                        tick_hint = int(getattr(self._nx, "_emit_step", -1)) + 1
                    except Exception:
                        tick_hint = 0
                C = getattr(getattr(self, "_nx", None), "connectome", None)
                for _ev in self._void_scout.step(C, int(tick_hint)) or []:
                    try:
                        self._evt_metrics.update(_ev)
                        collected_events.append(_ev)
                        # update cold-map for scout-generated events
                        if getattr(self, "_cold_map", None) is not None:
                            try:
                                kind = getattr(_ev, "kind", "")
                                if kind == "vt_touch":
                                    token = getattr(_ev, "token", None)
                                    if isinstance(token, int) and token >= 0:
                                        self._cold_map.touch(int(token), int(tick_hint))
                                elif kind == "edge_on":
                                    u = getattr(_ev, "u", None)
                                    v = getattr(_ev, "v", None)
                                    if isinstance(u, int) and u >= 0:
                                        self._cold_map.touch(int(u), int(tick_hint))
                                    if isinstance(v, int) and v >= 0:
                                        self._cold_map.touch(int(v), int(tick_hint))
                            except Exception:
                                pass
                    except Exception:
                        continue
                # update latest tick from scout pass
                try:
                    if latest_tick is None or int(tick_hint) > int(latest_tick):
                        latest_tick = int(tick_hint)
                except Exception:
                    pass
        except Exception:
            pass

        # 2.5) fold heat/excitation/inhibition maps with collected events (telemetry-only)
        try:
            try:
                fold_tick = int(latest_tick) if latest_tick is not None else int(getattr(self._nx, "_emit_step", -1)) + 1
            except Exception:
                fold_tick = 0
            if getattr(self, "_heat_map", None) is not None:
                try:
                    self._heat_map.fold(collected_events, int(fold_tick))
                except Exception:
                    pass
            if getattr(self, "_exc_map", None) is not None:
                try:
                    self._exc_map.fold(collected_events, int(fold_tick))
                except Exception:
                    pass
            if getattr(self, "_inh_map", None) is not None:
                try:
                    self._inh_map.fold(collected_events, int(fold_tick))
                except Exception:
                    pass
        except Exception:
            pass

        # 2.75) stage maps/frame payload for UI bus (header JSON + Float32 LE payload)
        try:
            stage_maps_frame(
                nx=self._nx,
                heat_map=self._heat_map,
                exc_map=self._exc_map,
                inh_map=self._inh_map,
                fold_tick=int(
                    latest_tick
                    if latest_tick is not None
                    else (int(getattr(self._nx, "_emit_step", -1)) + 1)
                ),
            )
        except Exception:
            pass

        # 3) refresh cached evt snapshot
        try:
            self._last_evt_snapshot = build_evt_snapshot(
                evt_metrics=self._evt_metrics,
                cold_map=self._cold_map,
                heat_map=self._heat_map,
                exc_map=self._exc_map,
                inh_map=self._inh_map,
                latest_tick=(
                    int(latest_tick)
                    if latest_tick is not None
                    else (int(getattr(self._nx, "_emit_step", -1)) + 1)
                ),
                nx=self._nx,
            )
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
                self._void_scout = _VoidScout(
                    budget_visits=max(0, sv), budget_edges=max(0, se), seed=seed
                )
            except Exception:
                self._void_scout = None
        # Cold-map reducer
        if getattr(self, "_cold_map", None) is None:
            try:
                ck = int(getattr(self._nx, "cold_head_k", 256))
            except Exception:
                ck = 256
            try:
                hl = int(getattr(self._nx, "cold_half_life_ticks", 200))
            except Exception:
                hl = 200
            try:
                seed = int(getattr(self._nx, "seed", 0))
            except Exception:
                seed = 0
            try:
                self._cold_map = _ColdMap(
                    head_k=max(8, ck), half_life_ticks=max(1, hl), keep_max=None, seed=seed
                )
            except Exception:
                self._cold_map = None
        # Heat/Excitation/Inhibition reducers (mirror cold-map settings; telemetry-only)
        try:
            hk = int(getattr(self._nx, "cold_head_k", 256))
        except Exception:
            hk = 256
        try:
            hl2 = int(getattr(self._nx, "cold_half_life_ticks", 200))
        except Exception:
            hl2 = 200
        try:
            seed = int(getattr(self._nx, "seed", 0))
        except Exception:
            seed = 0
        if getattr(self, "_heat_map", None) is None:
            try:
                self._heat_map = _HeatMap(
                    head_k=max(8, hk), half_life_ticks=max(1, hl2), keep_max=None, seed=seed + 1
                )
            except Exception:
                self._heat_map = None
        if getattr(self, "_exc_map", None) is None:
            try:
                self._exc_map = _ExcMap(
                    head_k=max(8, hk), half_life_ticks=max(1, hl2), keep_max=None, seed=seed + 2
                )
            except Exception:
                self._exc_map = None
        if getattr(self, "_inh_map", None) is None:
            try:
                self._inh_map = _InhMap(
                    head_k=max(8, hk), half_life_ticks=max(1, hl2), keep_max=None, seed=seed + 3
                )
            except Exception:
                self._inh_map = None

    # --- Connectome interface (single entrypoint for runtime) ---
    def stimulate_indices(self, indices, amp: float = 0.05) -> None:
        try:
            self._nx.connectome.stimulate_indices(list(indices), amp=float(amp))
        except Exception:
            pass

    def step_connectome(
        self,
        t: float,
        domain_modulation: float = 1.0,
        sie_gate: float = 0.0,
        use_time_dynamics: bool = True,
    ) -> None:
        try:
            self._nx.connectome.step(
                t,
                domain_modulation=float(domain_modulation),
                sie_drive=float(sie_gate),
                use_time_dynamics=bool(use_time_dynamics),
            )
        except Exception:
            pass

    def compute_metrics(self) -> Dict[str, Any]:
        try:
            return compute_metrics(self._nx.connectome)
        except Exception:
            return {}

    def snapshot_graph(self):
        try:
            return self._nx.connectome.snapshot_graph()
        except Exception:
            return None

    # --- Numeric helpers (wrap core.signals) ---
    def compute_active_edge_density(self) -> Tuple[int, float]:
        try:
            N = int(getattr(self._nx, "N", 0))
        except Exception:
            N = 0
        try:
            return _sig_density(getattr(self._nx, "connectome", None), N)
        except Exception:
            return 0, 0.0

    def compute_td_signal(
        self, prev_E: int | None, E: int, vt_prev: float | None = None, vt_last: float | None = None
    ) -> float:
        try:
            return float(_sig_td(prev_E, E, vt_prev, vt_last))
        except Exception:
            return 0.0

    def compute_firing_var(self):
        try:
            return _sig_fvar(getattr(self._nx, "connectome", None))
        except Exception:
            return None

    def get_homeostasis_counters(self) -> Tuple[int, int]:
        try:
            pruned = int(getattr(self._nx.connectome, "_last_pruned_count", 0))
            bridged = int(getattr(self._nx.connectome, "_last_bridged_count", 0))
            return pruned, bridged
        except Exception:
            return 0, 0

    def get_findings(self) -> Dict[str, Any]:
        try:
            f = getattr(self._nx.connectome, "findings", None)
            return dict(f) if isinstance(f, dict) else {}
        except Exception:
            return {}

    def get_last_sie2_valence(self) -> float:
        try:
            return float(getattr(self._nx.connectome, "_last_sie2_valence", 0.0))
        except Exception:
            return 0.0

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

    def engram_save(
        self, path: Optional[str] = None, step: Optional[int] = None, fmt: Optional[str] = None
    ) -> str:
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
        use_fmt = str(
            fmt if fmt is not None else getattr(nx, "checkpoint_format", "h5") or "h5"
        )
        return _save_checkpoint(
            nx.run_dir, use_step, nx.connectome, fmt=use_fmt, adc=getattr(nx, "adc", None)
        )


__all__ = ["CoreEngine"]