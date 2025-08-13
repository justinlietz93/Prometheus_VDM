from __future__ import annotations

import os
import dash
from typing import Any, Dict, Tuple
from dash import Input, Output, State, no_update  # noqa: F401 (bound at runtime)

from fum_rt.frontend.utilities.profiles import assemble_profile as _assemble_profile, safe_int as _safe_int, safe_float as _safe_float
from fum_rt.frontend.utilities.fs_utils import latest_checkpoint


def register_process_callbacks(app, runs_root: str, manager, default_profile: Dict[str, Any]):
    """
    Process lifecycle callbacks:
      - Start New Run
      - Resume Selected Run
      - Stop Managed Run
    Depends on:
      - manager: ProcessManager instance
      - runs_root: initial runs root (UI may update manager later)
      - default_profile: dict of defaults for assembling profiles
    """

    def _start_or_resume(profile: Dict[str, Any]) -> Tuple[str, Any]:
        ok, msg = manager.start(profile)
        if not ok:
            return f"Start failed:\n{msg}", no_update
        rd = profile.get("run_dir") or msg
        cmd_echo = " ".join(manager.last_cmd or [])
        status = (
            f"Started.\nrun_dir={rd}\n"
            f"checkpoint_every={profile.get('checkpoint_every')} keep={profile.get('checkpoint_keep')}\n"
            f"cmd: {cmd_echo}\n"
            f"launch_log: {manager.launch_log}"
        )
        return status, rd or no_update

    @app.callback(
        Output("proc-status", "children", allow_duplicate=True),
        Output("run-dir", "value", allow_duplicate=True),
        Input("start-run", "n_clicks"),
        State("runs-root", "value"),
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
        State("rc-load-engram-path", "value"),
        State("rc-load-engram-input", "value"),
        prevent_initial_call=True,
    )
    def on_start_run(
        n_start,
        root,
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
        load_engram_path,
        load_engram_input,
    ):
        if not n_start:
            raise dash.exceptions.PreventUpdate
        if root:
            try:
                manager.set_runs_root(root)
            except Exception:
                pass

        profile = _assemble_profile(
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

        lep = (load_engram_input or load_engram_path)
        if lep:
            profile["load_engram"] = lep
            # Adopt the folder as run_dir so the whole bundle (events, lexicon, macro board) is reused.
            try:
                p = str(lep).strip()
                if p:
                    adopt_dir = p if os.path.isdir(p) else os.path.dirname(p)
                    if adopt_dir:
                        profile["run_dir"] = adopt_dir
            except Exception:
                pass

        return _start_or_resume(profile)

    @app.callback(
        Output("proc-status", "children", allow_duplicate=True),
        Output("run-dir", "value", allow_duplicate=True),
        Input("resume-run", "n_clicks"),
        State("runs-root", "value"),
        State("run-dir", "value"),
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
        State("rc-load-engram-path", "value"),
        State("rc-load-engram-input", "value"),
        prevent_initial_call=True,
    )
    def on_resume_run(
        n_resume,
        root,
        run_dir,
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
        load_engram_path,
        load_engram_input,
    ):
        if not n_resume:
            raise dash.exceptions.PreventUpdate
        if root:
            try:
                manager.set_runs_root(root)
            except Exception:
                pass

        rd = (run_dir or "").strip()
        if not rd or not os.path.isdir(rd):
            return "Select an existing run directory to resume.", no_update

        profile = _assemble_profile(
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
        profile["run_dir"] = rd

        lep = (load_engram_input or load_engram_path)
        if not lep:
            lep = latest_checkpoint(rd)
        if lep:
            profile["load_engram"] = lep

        ok, msg = manager.start(profile)
        if not ok:
            return f"Resume failed:\n{msg}", no_update

        cmd_echo = " ".join(manager.last_cmd or [])
        status = (
            f"Resumed.\nrun_dir={rd}\n"
            f"load_engram={profile.get('load_engram','')}\n"
            f"cmd: {cmd_echo}\n"
            f"launch_log: {manager.launch_log}"
        )
        return status, rd

    @app.callback(
        Output("proc-status", "children", allow_duplicate=True),
        Input("stop-run", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_stop_run(n_stop):
        if not n_stop:
            raise dash.exceptions.PreventUpdate
        ok, msg = manager.stop()
        return "Stopped." if ok else msg