from __future__ import annotations

import os
from dash import Input, Output, State, no_update  # noqa: F401
from fum_rt.frontend.utilities.profiles import safe_int as _safe_int, safe_float as _safe_float
from fum_rt.frontend.utilities.fs_utils import read_json_file, write_json_file
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
        prof = {
            "phase": int(_safe_int(phase, 0)),
            "speak": {
                "speak_z": float(_safe_float(s_z, default_profile["speak_z"])),
                "speak_hysteresis": float(_safe_float(s_h, default_profile["speak_hysteresis"])),
                "speak_cooldown_ticks": int(_safe_int(s_cd, default_profile["speak_cooldown_ticks"])),
                "speak_valence_thresh": float(_safe_float(s_vt, default_profile["speak_valence_thresh"])),
            },
            "connectome": {
                "walkers": int(_safe_int(c_w, default_profile["walkers"])),
                "hops": int(_safe_int(c_h, default_profile["hops"])),
                "bundle_size": int(_safe_int(c_b, default_profile["bundle_size"])),
                "prune_factor": float(_safe_float(c_pf, default_profile["prune_factor"])),
                "threshold": float(_safe_float(c_thr, default_profile.get("threshold", 0.15))),
                "lambda_omega": float(_safe_float(c_lw, default_profile.get("lambda_omega", 0.10))),
                "candidates": int(_safe_int(c_cand, default_profile.get("candidates", 64))),
            },
            "sie": {"novelty_idf_gain": float(_safe_float(s_idf, 1.0))},
        }
        ok = write_json_file(os.path.join(run_dir, "phase.json"), prof)
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
        try:
            obj = read_json_file(os.path.join(rd, "phase.json")) or {}
            if not isinstance(obj, dict):
                obj = {}
            obj["load_engram"] = p
            ok = write_json_file(os.path.join(rd, "phase.json"), obj)
            return f"Queued load_engram: {p}" if ok else "Error writing phase.json"
        except Exception as e:
            return f"Error: {e}"

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
        state = getattr(notify_engram_events, "_state", None)
        if state is None or state.get("run_dir") != rd:
            state = {"run_dir": rd, "events_size": 0}
            setattr(notify_engram_events, "_state", state)
        ev_path = os.path.join(rd, "events.jsonl")
        recs, new_size = tail_jsonl_bytes(ev_path, state["events_size"])
        state["events_size"] = new_size
        msg = None
        for rec in recs:
            if not isinstance(rec, dict):
                continue
            name = str(
                rec.get("event_type") or rec.get("event") or rec.get("message") or rec.get("msg") or rec.get("name") or ""
            ).lower()
            extra = rec.get("extra") or rec.get("meta") or {}
            if name == "engram_loaded":
                engram_path = extra.get("path") or extra.get("engram") or rec.get("path")
                msg = f"Engram loaded: {engram_path}" if engram_path else "Engram loaded."
            elif name == "engram_load_error":
                err = extra.get("err") or extra.get("error") or rec.get("error")
                engram_path = extra.get("path") or extra.get("engram") or rec.get("path")
                if err and engram_path:
                    msg = f"Engram load error: {err} ({engram_path})"
                elif err:
                    msg = f"Engram load error: {err}"
                else:
                    msg = "Engram load error."
        return msg if msg else no_update