from __future__ import annotations

import os
import dash
from typing import Any, Dict, List
from dash import Input, Output, State  # noqa: F401

from fum_rt.frontend.utilities.fs_utils import read_json_file, write_json_file
from fum_rt.frontend.utilities.profiles import (
    assemble_profile as _assemble_profile,
    checklist_from_bool as _checklist_from_bool,
)


def register_profile_callbacks(app, profiles_dir: str, default_profile: Dict[str, Any]):
    """
    Profile management callbacks:
      - Save current UI config to a named profile under profiles_dir
      - Load a selected profile into the UI config controls

    IDs preserved to match existing layout (fum_live).
    """

    os.makedirs(profiles_dir, exist_ok=True)

    def _list_profiles() -> List[str]:
        try:
            return sorted(
                [
                    os.path.join(profiles_dir, f)
                    for f in os.listdir(profiles_dir)
                    if f.endswith(".json")
                ]
            )
        except Exception:
            return []

    @app.callback(
        Output("profile-path", "options"),
        Output("profile-save-status", "children"),
        Input("save-profile", "n_clicks"),
        State("profile-name", "value"),
        State("cfg-neurons", "value"),
        State("cfg-k", "value"),
        State("cfg-hz", "value"),
        State("cfg-domain", "value"),
        State("cfg-use-time-dynamics", "value"),
        State("cfg-sparse-mode", "value"),
        State("cfg-threshold", "value"),
        State("cfg-lambda-omega", "value"),
        State("cfg-candidates", "value"),
        State("cfg-walkers", "value"),
        State("cfg-hops", "value"),
        State("cfg-status-interval", "value"),
        State("cfg-bundle-size", "value"),
        State("cfg-prune-factor", "value"),
        State("cfg-stim-group-size", "value"),
        State("cfg-stim-amp", "value"),
        State("cfg-stim-decay", "value"),
        State("cfg-stim-max-symbols", "value"),
        State("cfg-speak-auto", "value"),
        State("cfg-speak-z", "value"),
        State("cfg-speak-hysteresis", "value"),
        State("cfg-speak-cooldown-ticks", "value"),
        State("cfg-speak-valence-thresh", "value"),
        State("cfg-b1-half-life-ticks", "value"),
        State("cfg-viz-every", "value"),
        State("cfg-log-every", "value"),
        State("cfg-checkpoint-every", "value"),
        State("cfg-checkpoint-keep", "value"),
        State("cfg-duration", "value"),
        prevent_initial_call=True,
    )
    def on_save_profile(
        _n,
        name,
        neurons,
        k,
        hz,
        domain,
        use_td,
        sparse_mode,
        threshold,
        lambda_omega,
        candidates,
        walkers,
        hops,
        status_interval,
        bundle_size,
        prune_factor,
        stim_group_size,
        stim_amp,
        stim_decay,
        stim_max_symbols,
        speak_auto,
        speak_z,
        speak_hyst,
        speak_cd,
        speak_val,
        b1_hl,
        viz_every,
        log_every,
        checkpoint_every,
        checkpoint_keep,
        duration,
    ):
        name = (name or "").strip()
        if not name:
            return [{"label": os.path.basename(p), "value": p} for p in _list_profiles()], "Provide a profile name."
        data = _assemble_profile(
            neurons,
            k,
            hz,
            domain,
            use_td,
            sparse_mode,
            threshold,
            lambda_omega,
            candidates,
            walkers,
            hops,
            status_interval,
            bundle_size,
            prune_factor,
            stim_group_size,
            stim_amp,
            stim_decay,
            stim_max_symbols,
            speak_auto,
            speak_z,
            speak_hyst,
            speak_cd,
            speak_val,
            b1_hl,
            viz_every,
            log_every,
            checkpoint_every,
            checkpoint_keep,
            duration,
            default_profile,
        )
        path = os.path.join(profiles_dir, f"{name}.json")
        ok = write_json_file(path, data)
        status = f"Saved profile to {path}" if ok else f"Error writing {path}"
        return [{"label": os.path.basename(p), "value": p} for p in _list_profiles()], status

    @app.callback(
        Output("cfg-neurons", "value"),
        Output("cfg-k", "value"),
        Output("cfg-hz", "value"),
        Output("cfg-domain", "value"),
        Output("cfg-use-time-dynamics", "value"),
        Output("cfg-sparse-mode", "value"),
        Output("cfg-threshold", "value"),
        Output("cfg-lambda-omega", "value"),
        Output("cfg-candidates", "value"),
        Output("cfg-walkers", "value"),
        Output("cfg-hops", "value"),
        Output("cfg-status-interval", "value"),
        Output("cfg-bundle-size", "value"),
        Output("cfg-prune-factor", "value"),
        Output("cfg-stim-group-size", "value"),
        Output("cfg-stim-amp", "value"),
        Output("cfg-stim-decay", "value"),
        Output("cfg-stim-max-symbols", "value"),
        Output("cfg-speak-auto", "value"),
        Output("cfg-speak-z", "value"),
        Output("cfg-speak-hysteresis", "value"),
        Output("cfg-speak-cooldown-ticks", "value"),
        Output("cfg-speak-valence-thresh", "value"),
        Output("cfg-b1-half-life-ticks", "value"),
        Output("cfg-viz-every", "value"),
        Output("cfg-log-every", "value"),
        Output("cfg-checkpoint-every", "value"),
        Output("cfg-checkpoint-keep", "value"),
        Output("cfg-duration", "value"),
        Output("profile-save-status", "children", allow_duplicate=True),
        Input("load-profile", "n_clicks"),
        Input("profile-path", "value"),
        Input("profile-file-selected-label", "children"),
        prevent_initial_call=True,
    )
    def on_load_profile(_n, path, _sel_label):
        if not path:
            raise dash.exceptions.PreventUpdate
        data = read_json_file(path) or {}

        def g(k, dv):
            v = data.get(k, dv)
            return v if v is not None else dv

        return (
            g("neurons", default_profile["neurons"]),
            g("k", default_profile["k"]),
            g("hz", default_profile["hz"]),
            g("domain", default_profile["domain"]),
            _checklist_from_bool(bool(g("use_time_dynamics", default_profile["use_time_dynamics"]))),
            _checklist_from_bool(bool(g("sparse_mode", default_profile["sparse_mode"]))),
            g("threshold", default_profile["threshold"]),
            g("lambda_omega", default_profile["lambda_omega"]),
            g("candidates", default_profile["candidates"]),
            g("walkers", default_profile["walkers"]),
            g("hops", default_profile["hops"]),
            g("status_interval", default_profile["status_interval"]),
            g("bundle_size", default_profile["bundle_size"]),
            g("prune_factor", default_profile["prune_factor"]),
            g("stim_group_size", default_profile["stim_group_size"]),
            g("stim_amp", default_profile["stim_amp"]),
            g("stim_decay", default_profile["stim_decay"]),
            g("stim_max_symbols", default_profile["stim_max_symbols"]),
            _checklist_from_bool(bool(g("speak_auto", default_profile["speak_auto"]))),
            g("speak_z", default_profile["speak_z"]),
            g("speak_hysteresis", default_profile["speak_hysteresis"]),
            g("speak_cooldown_ticks", default_profile["speak_cooldown_ticks"]),
            g("speak_valence_thresh", default_profile["speak_valence_thresh"]),
            g("b1_half_life_ticks", default_profile["b1_half_life_ticks"]),
            g("viz_every", default_profile["viz_every"]),
            g("log_every", default_profile["log_every"]),
            g("checkpoint_every", default_profile["checkpoint_every"]),
            g("checkpoint_keep", default_profile["checkpoint_keep"]),
            g("duration", default_profile["duration"]),
            f"Loaded profile: {path}",
        )