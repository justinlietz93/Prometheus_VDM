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
from fum_rt.core.proprioception.events import EventDrivenMetrics as _EvtMetrics
from fum_rt.core.proprioception.events import EventDrivenMetrics as _EvtMetrics
from fum_rt.core.cortex.scouts import VoidColdScoutWalker as _VoidScout
from fum_rt.core.signals import apply_b1_detector as _apply_b1d
from fum_rt.runtime.runtime_helpers import (
    process_messages as _process_messages,
    maybe_smoke_tests as _maybe_smoke_tests,
    emit_status_and_macro as _emit_status_and_macro,
    maybe_visualize as _maybe_visualize,
    save_tick_checkpoint as _save_tick_checkpoint,
)


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

        while True:
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

            # IDF novelty is composer/telemetry-only; keep dynamics neutral per safe pattern
            idf_scale = 1.0

            # Compute step and scan-based metrics (parity-preserving)
            m, drive = _compute_step_and_metrics(nx, t, step, idf_scale=idf_scale)

            # 3) telemetry fold (bus drain + ADC + optional event metrics + B1)
            void_topic_symbols: Set[Any] = set()
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
            # 3c) CoreEngine folding and snapshot merge (evt_* only; preserve canonical fields)
            try:
                eng = getattr(nx, "_engine", None)
                if eng is not None:
                    # Collect core events from drained observations and ADC metrics
                    evs = []
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
                # lazy import to avoid cycle
                from fum_rt.runtime.runtime_helpers import maybe_auto_speak as _maybe_auto_speak  # type: ignore
                if _maybe_auto_speak is not None:
                    _maybe_auto_speak(nx, m, int(step), tick_tokens, void_topic_symbols)
            except Exception:
                pass

            # Structured tick log
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

            # Checkpointing + retention (delegated)
            try:
                _save_tick_checkpoint(nx, int(step))
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