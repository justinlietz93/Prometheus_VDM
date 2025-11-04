"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

"""
Runtime main loop (extracted from Nexus.run for modularization).

Behavior:
- Mirrors the original Nexus while-loop exactly (move-only).
- No logging configuration or finalization here; caller handles setup/teardown.
- Operates directly on the passed 'nx' Nexus-like object to preserve state and IO wiring.

Inputs:
- nx: Nexus-like instance (provides ute/utd/connectome/adc/etc.)
- t0: float timestamp at loop start (time.time())
- step: starting tick index (int)
- duration_s: optional max wall-clock seconds to run

Returns:
- last step index (int) after the loop completes/breaks
"""

from typing import Any, Dict, Set, Tuple, Optional
import time
import os

from fum_rt.runtime.stepper import compute_step_and_metrics as _compute_step_and_metrics
from fum_rt.runtime.telemetry import tick_fold as _tick_fold
from fum_rt.runtime.events_adapter import (
    observations_to_events as _obs_to_events,
    adc_metrics_to_event as _adc_event,
)
from fum_rt.core.engine import CoreEngine as _CoreEngine
from fum_rt.core.proprioception.events import EventDrivenMetrics as _EvtMetrics, BiasHintEvent as _BiasHintEvent
from fum_rt.core.cortex.scouts import VoidColdScoutWalker as _VoidScout
from fum_rt.core.signals import apply_b1_detector as _apply_b1d
from fum_rt.runtime.helpers.ingest import process_messages as _process_messages
from fum_rt.runtime.helpers.smoke import maybe_smoke_tests as _maybe_smoke_tests
from fum_rt.runtime.helpers.emission import emit_status_and_macro as _emit_status_and_macro
from fum_rt.runtime.helpers.viz import maybe_visualize as _maybe_visualize
from fum_rt.runtime.helpers.checkpointing import save_tick_checkpoint as _save_tick_checkpoint
from fum_rt.runtime.helpers import maybe_start_maps_ws as _maybe_start_maps_ws
from fum_rt.runtime.helpers.status_http import (
    maybe_start_status_http as _maybe_start_status_http,
)
from fum_rt.runtime.helpers.redis_out import (
    maybe_publish_status_redis as _maybe_publish_status_redis,
    maybe_publish_maps_redis as _maybe_publish_maps_redis,
)

# Void-faithful scout runner (stateless, per-tick; no schedulers)
from fum_rt.core.cortex.void_walkers.runner import run_scouts_once as _run_scouts_once
from fum_rt.core.cortex.void_walkers.void_heat_scout import HeatScout
from fum_rt.core.cortex.void_walkers.void_ray_scout import VoidRayScout
from fum_rt.core.cortex.void_walkers.void_memory_ray_scout import MemoryRayScout
from fum_rt.core.cortex.void_walkers.void_frontier_scout import FrontierScout
from fum_rt.core.cortex.void_walkers.void_cycle_scout import CycleHunterScout
from fum_rt.core.cortex.void_walkers.void_sentinel_scout import SentinelScout
# Also expose the remaining scouts for full coverage (9 walkers)
from fum_rt.core.cortex.void_walkers.void_cold_scout import ColdScout
from fum_rt.core.cortex.void_walkers.void_excitation_scout import ExcitationScout
from fum_rt.core.cortex.void_walkers.void_inhibition_scout import InhibitionScout
# Memory/trail steering fields (owner + adapter view)
from fum_rt.core.cortex.maps.memorymap import MemoryMap
from fum_rt.core.cortex.maps.trailmap import TrailMap
from fum_rt.core.memory import MemoryField

# ---------- Optional Learning/Actuator Adapters (default-off, safe) ----------
def _truthy(x) -> bool:
    try:
        if isinstance(x, (int, float)):
            return bool(x)
        s = str(x).strip().lower()
        return s in ("1", "true", "yes", "on", "y", "t")
    except Exception:
        return False

# Development strictness gate: raise swallowed exceptions when enabled
STRICT = _truthy(os.getenv("VOID_STRICT", "0"))


def _maybe_run_revgsp(nx: Any, metrics: Dict[str, Any], step: int) -> None:
    """
    Best-effort adapter to call RE-VGSP adapt_connectome if available and enabled.
    - Enabled via ENABLE_REVGSP=1 (default off).
    - Auto-detects compatible substrate (nx.substrate or nx.connectome with expected fields).
    - Filters kwargs to the function signature to avoid mismatches.
    - Silent no-op on any error or incompatibility.
    """
    import os, inspect  # local to avoid module-level dependency
    if not _truthy(os.getenv("ENABLE_REVGSP", "0")):
        return

    # Use current in-repo implementation only (void-faithful, budgeted)
    try:
        from fum_rt.core.neuroplasticity.revgsp import RevGSP as _RevGSP  # type: ignore
        _adapt = _RevGSP().adapt_connectome  # method-compatible wrapper
    except Exception:
        return

    # Pick a substrate-like object
    s = getattr(nx, "substrate", None)
    if s is None:
        s = getattr(nx, "connectome", None)
    if s is None:
        return

    # Build candidate kwargs and filter by signature
    try:
        sig = inspect.signature(_adapt)
        allowed = set(sig.parameters.keys())
    except Exception:
        allowed = set()

    # Sources for signals
    total_reward = float(metrics.get("sie_total_reward", 0.0))
    plv = metrics.get("evt_plv", None)  # optional; may be absent
    latency = getattr(nx, "network_latency_estimate", None)
    if latency is None:
        latency = {"max": float(getattr(nx, "latency_max", 0.0)), "error": float(getattr(nx, "latency_err", 0.0))}

    # Possible kwargs (include aliases so legacy and new signatures both work)
    eta_val = float(os.getenv("REV_GSP_ETA", getattr(nx, "rev_gsp_eta", 1e-3)))
    lam_val = float(os.getenv("REV_GSP_LAMBDA", getattr(nx, "rev_gsp_lambda", 0.99)))
    twin_ms = int(os.getenv("REV_GSP_TWIN_MS", "20"))
    candidates = {
        "substrate": s,
        "spike_train": getattr(nx, "recent_spikes", None),
        "spike_phases": getattr(nx, "spike_phases", None),
        # legacy name
        "learning_rate": eta_val,
        # new wrapper name
        "base_lr": eta_val,
        "lambda_decay": lam_val,
        "total_reward": total_reward,
        "plv": plv,
        # legacy name (if any)
        "network_latency_estimate": latency,
        # new wrapper name
        "network_latency": latency,
        "time_window_ms": twin_ms,
    }
    # Filter None values and restrict to signature
    kwargs = {k: v for k, v in candidates.items() if v is not None and (not allowed or k in allowed)}

    # If the function requires args we didn't provide, it will raise - catch and noop.
    try:
        _adapt(**kwargs)
    except Exception:
        # Silent by design; adapter is optional and must not disrupt runtime parity.
        return


def _maybe_run_gdsp(nx: Any, metrics: Dict[str, Any], step: int) -> None:
    """
    Best-effort adapter to call GDSP synaptic actuator if available and enabled.
    - Enabled via ENABLE_GDSP=1 (default off).
    - Emergent triggers only (no fixed cadence): activates on b1_spike, |td_signal| >= GDSP_TD_THRESH, or cohesion_components > 1.
    - Requires a substrate-like object with the expected sparse fields; else no-op.
    - Executes homeostatic repairs (if repair_triggered present), growth (when territory provided),
      and maintenance pruning with T_prune and pruning_threshold.
    """
    import os  # local import
    if not _truthy(os.getenv("ENABLE_GDSP", "0")):
        return

    # Emergent gating only (no fixed cadence or schedulers)
    try:
        td = float(metrics.get("td_signal", 0.0))
    except Exception:
        td = 0.0
    b1_spike = bool(metrics.get("b1_spike", metrics.get("evt_b1_spike", False)))
    try:
        comp = int(metrics.get("cohesion_components", metrics.get("evt_cohesion_components", 1)))
    except Exception:
        comp = 1
    try:
        td_thr = float(os.getenv("GDSP_TD_THRESH", "0.2"))
    except Exception:
        td_thr = 0.2
    if not (b1_spike or abs(td) >= td_thr or comp > 1):
        return

    # Use current in-repo implementation only (void-faithful, budgeted/territory-scoped)
    try:
        from fum_rt.core.neuroplasticity.gdsp import GDSPActuator as _GDSP  # type: ignore
        _gdsp = _GDSP()
        _run_gdsp = _gdsp.run
    except Exception:
        return

    # Substrate or connectome compatibility check (sparse CSR fields)
    s = getattr(nx, "substrate", None)
    if s is None:
        s = getattr(nx, "connectome", None)
    if s is None:
        return

    def _has(obj, name: str) -> bool:
        return hasattr(obj, name)

    # Required fields for GDSP to operate safely
    required = ("synaptic_weights", "persistent_synapses", "synapse_pruning_timers", "eligibility_traces", "firing_rates")
    if not all(_has(s, r) for r in required):
        return

    # Build reports (best-effort from current metrics)
    comp = int(metrics.get("cohesion_components", metrics.get("evt_cohesion_components", 1)))
    b1_spike = bool(metrics.get("b1_spike", metrics.get("evt_b1_spike", False)))
    try:
        b1_z = float(metrics.get("b1_z", metrics.get("evt_b1_z", 0.0)))
    except Exception:
        b1_z = 0.0
    # Heuristic placeholder for persistence (bounded): adapter only
    b1_persistence = max(0.0, min(1.0, abs(b1_z) / 10.0))

    introspection_report = {
        "component_count": comp,
        "b1_persistence": b1_persistence,
        "repair_triggered": b1_spike,
        # locus_indices optional; omitted by default
    }
    sie_report = {
        "total_reward": float(metrics.get("sie_total_reward", 0.0)),
        "td_error": float(metrics.get("td_signal", 0.0)),
        "novelty": float(metrics.get("vt_entropy", metrics.get("evt_vt_entropy", 0.0))),
    }

    # Territory indices from event-folded UF if available (bounded; no scans)
    territory_indices = None
    try:
        terr = getattr(nx, "_territories", None)
        if terr is not None:
            k_sel = int(os.getenv("GDSP_K", "64"))
            sel = terr.sample_any(int(max(0, k_sel)))
            if isinstance(sel, list) and sel:
                territory_indices = sel
    except Exception:
        territory_indices = None
    # If triggers fired but no indices, emit a lightweight BiasHintEvent (telemetry-only; optional consumers)
    try:
        if territory_indices is None:
            bus = getattr(nx, "bus", None)
            if bus is not None:
                try:
                    _o = _BiasHintEvent(kind="bias_hint", t=int(step), region="unknown", nodes=tuple(), ttl=2)
                    bus.publish(_o)
                except Exception:
                    pass
    except Exception:
        pass

    # Pruning parameters
    try:
        T_prune = int(os.getenv("GDSP_T_PRUNE", "100"))
    except Exception:
        T_prune = 100
    try:
        pruning_threshold = float(os.getenv("GDSP_PRUNE_THRESHOLD", "0.01"))
    except Exception:
        pruning_threshold = 0.01

    try:
        _run_gdsp(
            substrate=s,
            introspection_report=introspection_report,
            sie_report=sie_report,
            territory_indices=territory_indices,
            T_prune=T_prune,
            pruning_threshold=pruning_threshold,
        )
    except Exception:
        # Silent failure to preserve parity
        return


def run_loop(nx: Any, t0: float, step: int, duration_s: Optional[int] = None) -> int:
    """
    Execute the main tick loop on the provided Nexus-like object.
    """
    try:
        # Lazy-init CoreEngine seam (telemetry-only additions; parity preserved)
        if getattr(nx, "_engine", None) is None:
            try:
                nx._engine = _CoreEngine(nx)
            except Exception:
                nx._engine = None

        # Lazy-init VOID cold scout (enabled by default; disable via ENABLE_COLD_SCOUTS=0)
        if getattr(nx, "_void_scout", None) is None:
            _sc_flag = str(os.getenv("ENABLE_COLD_SCOUTS", os.getenv("ENABLE_SCOUTS", "1"))).lower()
            if _sc_flag in ("1", "true", "yes", "on"):
                try:
                    _sv = int(os.getenv("SCOUT_VISITS", str(getattr(nx, "scout_visits", 16))))
                except Exception:
                    _sv = 16
                try:
                    _se = int(os.getenv("SCOUT_EDGES", str(getattr(nx, "scout_edges", 8))))
                except Exception:
                    _se = 8
                try:
                    _seed = int(getattr(nx, "seed", 0))
                except Exception:
                    _seed = 0
                try:
                    nx._void_scout = _VoidScout(budget_visits=max(0, _sv), budget_edges=max(0, _se), seed=_seed)
                except Exception:
                    nx._void_scout = None

        # Lazy-init event-driven metrics aggregator (enabled by default; disable via ENABLE_EVENT_METRICS=0)
        if getattr(nx, "_evt_metrics", None) is None:
            _evtm_flag = str(os.getenv("ENABLE_EVENT_METRICS", "1")).lower()
            if _evtm_flag in ("1", "true", "yes", "on"):
                try:
                    det = getattr(nx, "b1_detector", None)
                    z_spike = float(getattr(det, "z_spike", 1.0)) if det is not None else 1.0
                    hysteresis = float(getattr(det, "hysteresis", 1.0)) if det is not None else 1.0
                    half_life = int(getattr(nx, "b1_half_life_ticks", 50))
                    seed = int(getattr(nx, "seed", 0))
                    nx._evt_metrics = _EvtMetrics(
                        z_half_life_ticks=max(1, half_life),
                        z_spike=z_spike,
                        hysteresis=hysteresis,
                        seed=seed,
                    )
                except Exception:
                    nx._evt_metrics = None

        # Start maps WebSocket forwarder if enabled (idempotent; safe no-op on error)
        try:
            _maybe_start_maps_ws(nx)
        except Exception:
            pass

        # Start status HTTP endpoint (always; idempotent; safe no-op on error)
        try:
            _maybe_start_status_http(nx, force=True)
        except Exception:
            pass

        # Ensure connectome publishes Observations to the runtime bus for ADC/cycles/B1
        # Without this attachment, cycle_hit/region_stat announcements never reach tick_fold(),
        # leaving adc_cycle_hits at 0 -> complexity_cycles stays 0 -> b1_z remains flatlined.
        try:
            C = getattr(nx, "connectome", None)
            b = getattr(nx, "bus", None)
            if C is not None and b is not None:
                setattr(C, "bus", b)
        except Exception:
            pass

        while True:
            # micro-profiler: high-resolution clock
            try:
                _pc = time.perf_counter
            except Exception:
                _pc = time.time
            _t0 = _pc()
            tick_start = time.time()

            # 1) ingest
            msgs = nx.ute.poll()
            ute_in_count = len(msgs)
            ute_text_count, stim_idxs, tick_tokens, tick_rev_map = _process_messages(nx, msgs)

            # inject the accumulated stimulation before the learning step
            if stim_idxs:
                try:
                    nx.connectome.stimulate_indices(sorted(stim_idxs), amp=float(getattr(nx, "stim_amp", 0.05)))
                except Exception:
                    pass

            # Control plane: poll external phase control (file: runs/<ts>/phase.json)
            try:
                nx._poll_control()
            except Exception:
                pass

            # 2) SIE drive + update connectome
            # use wall-clock seconds since start as t
            t = time.time() - t0
            _t1 = _pc()

            # IDF novelty is composer/telemetry-only; keep dynamics neutral per safe pattern
            idf_scale = 1.0

            # Compute step and scan-based metrics (parity-preserving)
            m, drive = _compute_step_and_metrics(nx, t, step, idf_scale=idf_scale)

            # Optional: Online learner (RE-VGSP) and structural actuator (GDSP) - default OFF
            try:
                _maybe_run_revgsp(nx, m, int(step))
            except Exception:
                pass
            try:
                _maybe_run_gdsp(nx, m, int(step))
            except Exception:
                pass

            # 3) telemetry fold (bus drain + ADC + optional event metrics + B1)
            void_topic_symbols: Set[Any] = set()
            _t2 = _pc()
            try:
                m, vts = _tick_fold(
                    nx,
                    m,
                    drive,
                    float(m.get("td_signal", 0.0)),  # td_signal produced by stepper
                    int(step),
                    tick_rev_map,
                    obs_to_events=_obs_to_events,
                    adc_event=_adc_event,
                    apply_b1=_apply_b1d,
                )
                try:
                    if isinstance(vts, set):
                        void_topic_symbols |= vts
                except Exception:
                    pass
            except Exception:
                pass

            # 3a) Fold cohesion territories (event-folded union-find; no scans)
            try:
                terr = getattr(nx, "_territories", None)
                if terr is None:
                    try:
                        from fum_rt.core.proprioception.territory import TerritoryUF as _TerrUF  # lazy import
                        head_k = 512
                        try:
                            import os as _os
                            head_k = int(_os.getenv("TERRITORY_HEAD_K", str(head_k)))
                        except Exception:
                            head_k = 512
                        nx._territories = _TerrUF(head_k=int(max(8, head_k)))
                        terr = nx._territories
                    except Exception:
                        terr = None
                if terr is not None:
                    batch = getattr(nx, "_last_obs_batch", None)
                    if batch:
                        try:
                            terr.fold(batch)
                        except Exception:
                            pass
            except Exception:
                pass

            # 3b) Fold VOID cold-scout events into event-driven metrics (if aggregator present and no CoreEngine)
            try:
                if getattr(nx, "_engine", None) is None:
                    evtm = getattr(nx, "_evt_metrics", None)
                    scout = getattr(nx, "_void_scout", None)
                    if evtm is not None and scout is not None:
                        _evs = []
                        try:
                            _evs = scout.step(nx.connectome, int(step)) or []
                        except Exception:
                            _evs = []
                        for _ev in _evs:
                            try:
                                evtm.update(_ev)
                            except Exception:
                                pass
                        try:
                            _evsnap2 = evtm.snapshot()
                            if isinstance(_evsnap2, dict):
                                # Merge event-driven metrics without overriding canonical scan-based fields.
                                for _k, _v in _evsnap2.items():
                                    try:
                                        # Preserve existing B1 detector outputs from apply_b1 in the canonical keys.
                                        if str(_k).startswith("b1_") and _k in m:
                                            continue
                                        m[f"evt_{_k}"] = _v
                                    except Exception:
                                        continue
                        except Exception:
                            pass
            except Exception:
                pass
            # 3c) CoreEngine folding and snapshot merge (evt_* only; preserve canonical fields)
            try:
                eng = getattr(nx, "_engine", None)
                if eng is not None:
                    # Collect core events from drained observations and ADC metrics
                    evs = []
                    # Scouts: event-only, run once per tick under micro-budget (no schedulers)
                    try:
                        # Prepare bounded map heads for local routing (no scans)
                        maps_for_scouts = {}
                        try:
                            hm = getattr(eng, "_heat_map", None)
                            if hm is not None:
                                ms = hm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            em = getattr(eng, "_exc_map", None)
                            if em is not None:
                                ms = em.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            im = getattr(eng, "_inh_map", None)
                            if im is not None:
                                ms = im.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            cm = getattr(eng, "_cold_map", None)
                            if cm is not None:
                                ms = cm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        # Memory and Trail steering fields (bounded; no scans)
                        try:
                            mm = getattr(eng, "_memory_map", None)
                            if mm is not None:
                                ms = mm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass
                        try:
                            tm = getattr(eng, "_trail_map", None)
                            if tm is not None:
                                ms = tm.snapshot() or {}
                                if isinstance(ms, dict):
                                    maps_for_scouts.update(ms)
                        except Exception:
                            pass

                        # Seeds from recent stimulation (bounded)
                        try:
                            _seed_cap = int(os.getenv("SCOUT_SEEDS_MAX", "64"))
                        except Exception:
                            _seed_cap = 64
                        try:
                            seeds = sorted({int(s) for s in (stim_idxs or []) if isinstance(s, int)})[: max(0, _seed_cap)]
                        except Exception:
                            seeds = []

                        # Budgets (bounded)
                        try:
                            sv = int(os.getenv("SCOUT_VISITS", str(getattr(nx, "scout_visits", 16))))
                        except Exception:
                            sv = 16
                        try:
                            se = int(os.getenv("SCOUT_EDGES", str(getattr(nx, "scout_edges", 8))))
                        except Exception:
                            se = 8
                        try:
                            ttlv = int(os.getenv("SCOUT_TTL", "64"))
                        except Exception:
                            ttlv = 64
                        budget = {
                            "visits": max(0, sv),
                            "edges": max(0, se),
                            "ttl": max(1, ttlv),
                            "tick": int(step),
                            "seeds": list(seeds),
                        }

                        # Per-tick micro time budget across all scouts (µs)
                        try:
                            max_us = int(os.getenv("SCOUTS_MAX_US", "2000"))
                        except Exception:
                            max_us = 2000

                        scouts_list = []
                        # Per-scout env toggles (void-faithful; default on)
                        if _truthy(os.getenv("ENABLE_SCOUT_HEAT", "1")):
                            scouts_list.append(HeatScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_COLD", "1")):
                            scouts_list.append(ColdScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_EXC", "1")):
                            scouts_list.append(ExcitationScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_INH", "1")):
                            scouts_list.append(InhibitionScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_VOIDRAY", "1")):
                            scouts_list.append(VoidRayScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_MEMRAY", "1")):
                            scouts_list.append(MemoryRayScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_FRONTIER", "1")):
                            scouts_list.append(FrontierScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_CYCLE", "1")):
                            scouts_list.append(CycleHunterScout())
                        if _truthy(os.getenv("ENABLE_SCOUT_SENTINEL", "1")):
                            scouts_list.append(SentinelScout())

                        scout_evs = _run_scouts_once(
                            getattr(nx, "connectome", None),
                            scouts_list,
                            maps=maps_for_scouts,
                            budget=budget,
                            bus=None,        # do not publish directly; fold via engine below
                            max_us=max_us,
                        ) or []
                        if scout_evs:
                            evs.extend(scout_evs)
                    except Exception:
                        pass
                    try:
                        batch = getattr(nx, "_last_obs_batch", None)
                        if batch is not None:
                            for _ev in _obs_to_events(batch) or []:
                                evs.append(_ev)
                    except Exception:
                        pass
                    try:
                        adc_metrics = getattr(nx, "_last_adc_metrics", None)
                        if isinstance(adc_metrics, dict):
                            evs.append(_adc_event(adc_metrics, int(step)))
                    except Exception:
                        pass
                    # Step the core engine with events (telemetry-only; no behavior change)
                    # Ensure memory field/map/trail exist (single owner; views only) and fold events
                    try:
                        # Owner field (physics): single source of truth for m[i]
                        if getattr(eng, "_memory_field", None) is None:
                            try:
                                seed_m = int(getattr(nx, "seed", 0))
                            except Exception:
                                seed_m = 0
                            try:
                                hk = int(getattr(nx, "cold_head_k", 256))
                            except Exception:
                                hk = 256
                            try:
                                eng._memory_field = MemoryField(head_k=max(8, hk), seed=seed_m)
                                # Attach to connectome for local, O(1) reads via getters
                                try:
                                    C = getattr(nx, "connectome", None)
                                    if C is not None:
                                        setattr(C, "_memory_field", eng._memory_field)
                                except Exception as e:
                                    if STRICT:
                                        raise
                            except Exception as e:
                                if STRICT:
                                    raise
                        # View adapter (bounded head/dict for scouts/UI)
                        if getattr(eng, "_memory_map", None) is None:
                            try:
                                hk = int(getattr(nx, "cold_head_k", 256))
                            except Exception:
                                hk = 256
                            eng._memory_map = MemoryMap(field=getattr(eng, "_memory_field", None), head_k=max(8, hk))
                            try:
                                C = getattr(nx, "connectome", None)
                                if C is not None:
                                    setattr(C, "_memory_map", eng._memory_map)
                            except Exception as e:
                                if STRICT:
                                    raise
                        # Trail map (short half-life, repulsion)
                        if getattr(eng, "_trail_map", None) is None:
                            try:
                                hk = int(getattr(nx, "cold_head_k", 256))
                            except Exception:
                                hk = 256
                            try:
                                hl2 = int(getattr(nx, "cold_half_life_ticks", 200))
                            except Exception:
                                hl2 = 200
                            eng._trail_map = TrailMap(head_k=max(8, hk), half_life_ticks=max(1, int(max(1, hl2 // 4))), seed=int(getattr(nx, "seed", 0)) + 5)
                        # Fold current events into memory/trail (bounded; no scans)
                        try:
                            # Prefer owner field for folding; MemoryMap remains a delegating view
                            mf = getattr(eng, "_memory_field", None)
                            mm = getattr(eng, "_memory_map", None)
                            if mm is not None and mf is not None:
                                try:
                                    # Ensure view delegates to owner
                                    if getattr(mm, "field", None) is None:
                                        setattr(mm, "field", mf)
                                except Exception:
                                    pass
                            if mf is not None:
                                mf.fold(evs, int(step))
                            elif mm is not None:
                                # Proxy mode: fold via map if owner missing
                                mm.fold(evs, int(step))
                        except Exception as e:
                            if STRICT:
                                raise
                        try:
                            tm = getattr(eng, "_trail_map", None)
                            if tm is not None:
                                tm.fold(evs, int(step))
                        except Exception as e:
                            if STRICT:
                                raise
                    except Exception as e:
                        if STRICT:
                            raise

                    try:
                        dt_ms = int(max(1, float(getattr(nx, "dt", 0.1)) * 1000.0))
                    except Exception:
                        dt_ms = 100
                    try:
                        eng.step(dt_ms, evs)
                    except Exception:
                        pass
                    # Merge engine snapshot under evt_* without overriding canonical fields
                    try:
                        esnap = eng.snapshot()
                        if isinstance(esnap, dict):
                            for _k, _v in esnap.items():
                                try:
                                    # Preserve existing B1 detector outputs from apply_b1 in the canonical keys.
                                    if str(_k).startswith("b1_") and _k in m:
                                        continue
                                    if str(_k).startswith("evt_"):
                                        m[_k] = _v
                                    else:
                                        m[f"evt_{_k}"] = _v
                                except Exception:
                                    continue
                    except Exception:
                        pass
            except Exception:
                pass

            # Attach SIE top-level fields and components (parity)
            try:
                m["sie_total_reward"] = float(drive.get("total_reward", 0.0))
                m["sie_valence_01"] = float(drive.get("valence_01", 0.0))
            except Exception:
                pass
            # Homeostasis counters from sparse maintenance/bridging (telemetry-only)
            try:
                m["homeostasis_pruned"] = int(getattr(nx.connectome, "_last_pruned_count", 0))
                m["homeostasis_bridged"] = int(getattr(nx.connectome, "_last_bridged_count", 0))
            except Exception:
                pass
            comps = drive.get("components", {})
            try:
                items = comps.items() if isinstance(comps, dict) else []
                for k, v in items:
                    try:
                        m[f"sie_{k}"] = float(v)
                    except Exception:
                        try:
                            m[f"sie_{k}"] = int(v)
                        except Exception:
                            m[f"sie_{k}"] = str(v)
            except Exception:
                pass

            # Intrinsic SIE v2 (computed inside connectome)
            try:
                m["sie_v2_reward_mean"] = float(getattr(nx.connectome, "_last_sie2_reward", 0.0))
                m["sie_v2_valence_01"] = float(getattr(nx.connectome, "_last_sie2_valence", 0.0))
            except Exception:
                pass

            # current phase (control plane)
            try:
                m["phase"] = int(getattr(nx, "_phase", {}).get("phase", 0))
            except Exception:
                m["phase"] = 0

            # Emitter contexts
            m["t"] = step
            m["ute_in_count"] = int(ute_in_count)
            m["ute_text_count"] = int(ute_text_count)

            # Spool stats (Zip spooler) - expose in status snapshot (UI can show back-pressure)
            try:
                utd = getattr(nx, "utd", None)
                writer = getattr(utd, "_writer", None)
                stats = None
                # Prefer direct stats(); also handle nested writer._writer
                if writer is not None and hasattr(writer, "stats"):
                    stats = writer.stats()  # type: ignore[attr-defined]
                elif writer is not None and hasattr(writer, "_writer") and hasattr(writer._writer, "stats"):
                    try:
                        stats = writer._writer.stats()  # type: ignore[attr-defined]
                    except Exception:
                        stats = None
                if isinstance(stats, dict):
                    # Namespaced to avoid collisions
                    m["utd_spool"] = {
                        "buffer_bytes": int(stats.get("buffer_bytes", 0)),
                        "zip_bytes": int(stats.get("zip_bytes", 0)),
                        "zip_entries": int(stats.get("zip_entries", 0)),
                        "ring_bytes": int(stats.get("ring_bytes", 0)),
                    }
            except Exception:
                pass

            try:
                nx._emit_step = int(step)
                # include canonical valence fields for convenience
                m["sie_valence_01"] = float(m.get("sie_valence_01", m.get("sie_total_reward", 0.0)))
                nx._emit_last_metrics = dict(m)
            except Exception:
                pass

            # Optional one-shot smoke tests
            try:
                _maybe_smoke_tests(nx, m, int(step))
            except Exception:
                pass

            # Append history and trim
            nx.history.append(m)
            try:
                max_keep = 20000  # keep at most 20k ticks
                trim_to = 10000   # trim down to 10k when exceeding
                if len(nx.history) > max_keep:
                    nx.history = nx.history[-trim_to:]
            except Exception:
                pass

            # Periodically persist learned lexicon
            try:
                if (step % max(100, int(getattr(nx, "status_every", 1)) * 10)) == 0:
                    nx._save_lexicon()
            except Exception:
                pass

            # Autonomous speaking (delegated)
            try:
                _maybe_auto_speak = None
                # lazy import to avoid cycle (modularized helpers)
                from fum_rt.runtime.helpers import maybe_auto_speak as _maybe_auto_speak
                if _maybe_auto_speak is not None:
                    _maybe_auto_speak(nx, m, int(step), tick_tokens, void_topic_symbols)
            except Exception:
                pass

            # Structured tick log (batchable via LOG_EVERY to reduce I/O)
            try:
                _log_every_env = os.getenv("LOG_EVERY", None)
                if _log_every_env is not None:
                    nx.log_every = int(max(1, int(_log_every_env)))
            except Exception:
                pass
            if (step % int(getattr(nx, "log_every", 1))) == 0:
                try:
                    nx.logger.info("tick", extra={"extra": m})
                except Exception as e:
                    # fallback serialization and retry
                    try:
                        safe = {}
                        for kk, vv in m.items():
                            try:
                                if isinstance(vv, (float, int, str, bool)) or vv is None:
                                    safe[kk] = vv
                                else:
                                    safe[kk] = float(vv)
                            except Exception:
                                safe[kk] = str(vv)
                        nx.logger.info("tick", extra={"extra": safe})
                    except Exception:
                        try:
                            print("[nexus] tick_log_error", str(e), flush=True)
                        except Exception:
                            pass

            # Status payload + macro emission (delegated)
            try:
                _emit_status_and_macro(nx, m, int(step))
            except Exception:
                pass

            # Visualization (delegated)
            try:
                _maybe_visualize(nx, int(step))
            except Exception:
                pass

            # Redis Streams publish (optional, bounded; no schedulers)
            try:
                _maybe_publish_status_redis(nx, m, int(step))
            except Exception:
                pass
            try:
                _maybe_publish_maps_redis(nx, int(step))
            except Exception:
                pass

            # Checkpointing + retention (delegated)
            try:
                _save_tick_checkpoint(nx, int(step))
            except Exception:
                pass

            # micro-profiler finalize
            try:
                _t3 = _pc()
                nx.prof = {
                    "step": float(_t1 - _t0) if True else 0.0,
                    "fold": float(_t2 - _t1) if True else 0.0,
                    "metrics": float(_t3 - _t2) if True else 0.0,
                    "tick": float(_t3 - _t0) if True else 0.0,
                }
            except Exception:
                pass

            # 4) pacing
            step += 1
            elapsed = time.time() - tick_start
            sleep = max(0.0, float(getattr(nx, "dt", 0.1)) - elapsed)
            time.sleep(sleep)

            if duration_s is not None and (time.time() - t0) > duration_s:
                try:
                    nx.logger.info("nexus_duration_reached", extra={"extra": {"duration_s": int(duration_s)}})
                except Exception:
                    pass
                break
    finally:
        return int(step)


__all__ = ["run_loop"]