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

from fum_rt.runtime.stepper import compute_step_and_metrics as _compute_step_and_metrics
from fum_rt.runtime.telemetry import tick_fold as _tick_fold
from fum_rt.runtime.events_adapter import (
    observations_to_events as _obs_to_events,
    adc_metrics_to_event as _adc_event,
)
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