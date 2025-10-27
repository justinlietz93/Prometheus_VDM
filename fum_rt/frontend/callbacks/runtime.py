"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import os
from dash import Input, Output, State, no_update  # noqa: F401
from fum_rt.frontend.controllers.runtime_controller import (
    build_phase_update,
    update_phase_json,
    queue_load_engram,
    parse_engram_events_for_message,
)
from fum_rt.frontend.utilities.tail import tail_jsonl_bytes


def register_runtime_callbacks(app, default_profile):
    """
    Runtime-level controls:
      - Apply phase/runtime tuning -> phase.json
      - Queue load_engram into phase.json
      - Surface engram load events from events.jsonl
    """

    @app.callback(
        Output("phase-status", "children"),
        Input("apply-phase", "n_clicks"),
        State("run-dir", "value"),
        State("phase", "value"),
        State("rc-speak-z", "value"),
        State("rc-speak-hysteresis", "value"),
        State("rc-speak-cooldown", "value"),
        State("rc-speak-valence", "value"),
        State("rc-walkers", "value"),
        State("rc-hops", "value"),
        State("rc-bundle-size", "value"),
        State("rc-prune-factor", "value"),
        State("rc-threshold", "value"),
        State("rc-lambda-omega", "value"),
        State("rc-candidates", "value"),
        State("rc-novelty-idf-gain", "value"),
        prevent_initial_call=True,
    )
    def on_apply_phase(
        _n,
        run_dir,
        phase,
        s_z,
        s_h,
        s_cd,
        s_vt,
        c_w,
        c_h,
        c_b,
        c_pf,
        c_thr,
        c_lw,
        c_cand,
        s_idf,
    ):
        if not run_dir:
            return "Select a run directory."
        update = build_phase_update(
            default_profile,
            phase,
            s_z,
            s_h,
            s_cd,
            s_vt,
            c_w,
            c_h,
            c_b,
            c_pf,
            c_thr,
            c_lw,
            c_cand,
            s_idf,
        )
        ok = update_phase_json(run_dir, update)
        return "Applied" if ok else "Error writing phase.json"

    @app.callback(
        Output("phase-status", "children", allow_duplicate=True),
        Input("rc-load-engram-btn", "n_clicks"),
        State("run-dir", "value"),
        State("rc-load-engram-path", "value"),
        State("rc-load-engram-input", "value"),
        prevent_initial_call=True,
    )
    def on_load_engram_now(_n, run_dir, path, path_text):
        rd = (run_dir or "").strip()
        if not rd:
            return "Select a run directory."
        p = ((path or path_text) or "").strip()
        if not p:
            return "Enter engram path."
        ok, norm = queue_load_engram(rd, p)
        return f"Queued load engram: {norm}" if ok else "Error writing phase.json"

    @app.callback(
        Output("phase-status", "children", allow_duplicate=True),
        Input("poll", "n_intervals"),
        State("run-dir", "value"),
        prevent_initial_call=True,
    )
    def notify_engram_events(_n, run_dir):
        rd = (run_dir or "").strip()
        if not rd:
            return no_update

        # UI responsiveness guard:
        # - By default we avoid any file IO here (large events.jsonl can be 100s of MB).
        # - Opt-in tailing only when DASH_ENGRAM_EVENT_TAIL is explicitly enabled.
        try:
            _disable_io = str(os.getenv("DASH_DISABLE_FILE_IO", "1")).strip().lower() in ("1", "true", "yes", "on")
        except Exception:
            _disable_io = True
        try:
            _engram_tail_on = str(os.getenv("DASH_ENGRAM_EVENT_TAIL", "0")).strip().lower() in ("1", "true", "yes", "on")
        except Exception:
            _engram_tail_on = False
        if _disable_io and not _engram_tail_on:
            return no_update

        state = getattr(notify_engram_events, "_state", None)
        if state is None or state.get("run_dir") != rd:
            state = {"run_dir": rd, "events_size": 0}
            setattr(notify_engram_events, "_state", state)

        ev_path = os.path.join(rd, "events.jsonl")
        recs, new_size = tail_jsonl_bytes(ev_path, state["events_size"])
        state["events_size"] = new_size
        msg = parse_engram_events_for_message(recs)
        return msg if msg else no_update