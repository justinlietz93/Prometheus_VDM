from __future__ import annotations

import os
import time
from typing import List, Dict, Any

from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State  # type: ignore
import plotly.graph_objects as go

# Reuse existing lightweight filesystem utilities (no heavy scans)
from fum_rt.frontend.utilities.fs_utils import list_runs
from fum_rt.frontend.controllers.charts_controller import compute_dashboard_figures as _compute_dashboard_figures
from fum_rt.frontend.models.series import SeriesState as _SeriesState
# Optional: reuse controller to hook components incrementally
from fum_rt.frontend.controllers.charts_controller import compute_dashboard_figures as _compute_dashboard_figures
from fum_rt.frontend.models.series import SeriesState as _SeriesState


def _abs(path: str) -> str:
    try:
        return path if os.path.isabs(path) else os.path.abspath(path)
    except Exception:
        return path


def _file_stat(path: str) -> Dict[str, Any]:
    """
    Cheap file stat: no full read, only exists/size/mtime.
    """
    try:
        if not os.path.exists(path):
            return {"exists": False, "size": 0, "mtime": 0.0}
        return {
            "exists": True,
            "size": os.path.getsize(path) if os.path.isfile(path) else 0,
            "mtime": os.path.getmtime(path),
        }
    except Exception:
        return {"exists": False, "size": 0, "mtime": 0.0}


def _dir_stat(path: str) -> Dict[str, Any]:
    """
    Cheap dir stat: exists, dir mtime, count of subdirs (first-level).
    Avoids walking recursively; bounded and cheap.
    """
    try:
        if not os.path.isdir(path):
            return {"exists": False, "mtime": 0.0, "dirs": 0}
        try:
            mt = os.path.getmtime(path)
        except Exception:
            mt = 0.0
        try:
            cnt = sum(1 for n in os.listdir(path) if os.path.isdir(os.path.join(path, n)))
        except Exception:
            cnt = 0
        return {"exists": True, "mtime": mt, "dirs": cnt}
    except Exception:
        return {"exists": False, "mtime": 0.0, "dirs": 0}


def _runs_options(root: str) -> List[Dict[str, str]]:
    """
    Options for run-dir dropdown. Uses list_runs(root) which returns absolute paths,
    sorted by mtime desc (cheap).
    """
    try:
        runs = list_runs(root)
    except Exception:
        runs = []
    return [{"label": os.path.basename(p.rstrip(os.path.sep)) or p, "value": p} for p in runs]


def build_debug_app(runs_root: str) -> Dash:
    """
    Minimal, surgical debug UI:
    - No charts, no complex callbacks
    - Only polls a selected run_dir and reports file sizes/mtimes
    - Designed to isolate UI overhead vs backend/logging issues
    """
    app = Dash(
        __name__,
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
    )
    app.title = "FUM Debug UI"

    rr_abs = _abs(runs_root) or _abs("runs")
    runs_opts = _runs_options(rr_abs)
    default_run = runs_opts[0]["value"] if runs_opts else ""

    # Layout: runs root input + refresh button, run-dir dropdown, poll interval, component toggles, stats and graphs
    app.layout = html.Div(
        [
            html.H3("FUM Debug UI - Minimal"),
            html.Div(
                [
                    html.Label("Runs root"),
                    dcc.Input(id="dbg-runs-root", type="text", value=rr_abs, style={"width": "100%"}),
                    html.Button("Refresh", id="dbg-refresh", n_clicks=0),
                ],
                style={"display": "grid", "gap": "8px", "maxWidth": "640px"},
            ),
            html.Div(
                [
                    html.Label("Run directory"),
                    dcc.Dropdown(
                        id="dbg-run-dir",
                        options=runs_opts,
                        value=default_run,
                        style={"minWidth": "360px"},
                    ),
                ],
                style={"display": "grid", "gap": "8px", "maxWidth": "640px", "marginTop": "8px"},
            ),
            html.Div(
                [
                    html.Label("Polling"),
                    dcc.Checklist(
                        id="dbg-poll-enabled",
                        options=[{"label": "Enable polling", "value": "on"}],
                        value=["on"],
                        inline=True,
                    ),
                    dcc.Slider(
                        id="dbg-poll-ms",
                        min=250,
                        max=5000,
                        step=250,
                        value=1000,
                        tooltip={"always_visible": False},
                    ),
                ],
                style={"display": "grid", "gap": "8px", "maxWidth": "640px", "marginTop": "8px"},
            ),
            html.Div(
                [
                    html.Label("Components"),
                    dcc.Checklist(
                        id="dbg-components",
                        options=[
                            {"label": "Tiny chart: file sizes", "value": "file_sizes"},
                            {"label": "Controller charts (dashboard + discovery)", "value": "controller_charts"},
                        ],
                        value=["file_sizes"],
                        inline=False,
                    ),
                ],
                style={"display": "grid", "gap": "8px", "maxWidth": "960px", "marginTop": "8px"},
            ),
            html.Div(
                [
                    html.Label("Controller settings"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Status URL"),
                                    dcc.Input(id="dbg-ctrl-status-url", type="text", value="http://127.0.0.1:8787/status/snapshot", style={"width": "100%"}),
                                ],
                                style={"minWidth": "280px"},
                            ),
                            html.Div(
                                [
                                    html.Label("Status timeout (s)"),
                                    dcc.Input(id="dbg-ctrl-status-timeout", type="number", value=0.2, min=0.05, step=0.05),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Label("Points cap (maxp)"),
                                    dcc.Input(id="dbg-ctrl-points-cap", type="number", value=800, min=50, step=50),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Label("Series cap"),
                                    dcc.Input(id="dbg-ctrl-series-cap", type="number", value=4, min=1, step=1),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Label("Decimate to N points (0=off)"),
                                    dcc.Input(id="dbg-ctrl-decimate", type="number", value=400, min=0, step=50),
                                ]
                            ),
                        ],
                        className="row",
                    ),
                ],
                style={"display": "grid", "gap": "8px", "maxWidth": "960px", "marginTop": "8px"},
            ),
            # Graphs (rendered empty unless enabled via dbg-components)
            html.Div(
                [
                    dcc.Graph(id="dbg-fig", figure=go.Figure(), style={"minHeight": "220px"}),
                    dcc.Graph(id="dbg-fig-dashboard", figure=go.Figure(), style={"minHeight": "360px"}),
                    dcc.Graph(id="dbg-fig-discovery", figure=go.Figure(), style={"minHeight": "300px"}),
                ],
                style={"display": "grid", "gap": "16px", "maxWidth": "1200px"},
            ),
            dcc.Interval(id="dbg-interval", interval=1000, n_intervals=0, disabled=False),
            html.Hr(),
            html.Pre(id="dbg-stats", children="Waiting for data..."),
            dcc.Store(id="dbg-state"),
        ],
        style={"padding": "10px", "fontFamily": "sans-serif"},
    )

    # Callbacks
    @app.callback(
        Output("dbg-run-dir", "options", allow_duplicate=True),
        Output("dbg-run-dir", "value", allow_duplicate=True),
        Input("dbg-refresh", "n_clicks"),
        State("dbg-runs-root", "value"),
        prevent_initial_call=True,
    )
    def on_refresh_runs(_n, root):
        r = (_abs(root or "")).strip()
        if not r:
            raise Exception("Runs root is empty")
        opts = _runs_options(r)
        val = opts[0]["value"] if opts else ""
        return opts, val

    @app.callback(
        Output("dbg-interval", "interval", allow_duplicate=True),
        Output("dbg-interval", "disabled", allow_duplicate=True),
        Input("dbg-poll-ms", "value"),
        Input("dbg-poll-enabled", "value"),
        prevent_initial_call=True,
    )
    def on_poll_config(ms, enabled_vals):
        try:
            interval = int(ms) if ms else 1000
        except Exception:
            interval = 1000
        disabled = ("on" not in (enabled_vals or []))
        return max(250, interval), disabled

    @app.callback(
        Output("dbg-stats", "children", allow_duplicate=True),
        Input("dbg-interval", "n_intervals"),
        State("dbg-run-dir", "value"),
        State("dbg-runs-root", "value"),
        prevent_initial_call=False,
    )
    def on_tick(_n, rd, rr):
        t0 = time.perf_counter()

        rr_abs_local = _abs((rr or "").strip())
        rd_local = (rd or "").strip()
        if rd_local and not os.path.isabs(rd_local):
            # Normalize run_dir against runs_root (defensive)
            rd_abs = _abs(os.path.join(rr_abs_local, rd_local))
        else:
            rd_abs = rd_local

        # Resolve key file stats in the selected run
        events_path = os.path.join(rd_abs, "events.jsonl") if rd_abs else ""
        utd_path = os.path.join(rd_abs, "utd_events.jsonl") if rd_abs else ""
        phase_path = os.path.join(rd_abs, "phase.json") if rd_abs else ""

        rr_stat = _dir_stat(rr_abs_local) if rr_abs_local else {"exists": False, "mtime": 0.0, "dirs": 0}
        rd_exists = os.path.isdir(rd_abs) if rd_abs else False
        events_stat = _file_stat(events_path) if rd_abs else {"exists": False, "size": 0, "mtime": 0.0}
        utd_stat = _file_stat(utd_path) if rd_abs else {"exists": False, "size": 0, "mtime": 0.0}
        phase_stat = _file_stat(phase_path) if rd_abs else {"exists": False, "size": 0, "mtime": 0.0}

        # Also surface a cheap "top N" run dirs snapshot for verification (labels only)
        try:
            runs_list = list_runs(rr_abs_local)[:6]
        except Exception:
            runs_list = []

        dt_ms = int((time.perf_counter() - t0) * 1000.0)
        now_s = time.strftime("%Y-%m-%d %H:%M:%S")

        # Produce a compact, human-readable diagnostics block (no heavy formatting)
        lines = []
        lines.append(f"[{now_s}] server_callback_ms={dt_ms}")
        lines.append(f"runs_root_abs={rr_abs_local}")
        lines.append(f"runs_root_exists={rr_stat.get('exists')} subdirs={rr_stat.get('dirs')} mtime={rr_stat.get('mtime'):.3f}")
        lines.append(f"run_dir={rd_abs}")
        lines.append(f"run_dir_exists={rd_exists}")
        lines.append(f"events.jsonl exists={events_stat['exists']} size={events_stat['size']} mtime={events_stat['mtime']:.3f}")
        lines.append(f"utd_events.jsonl exists={utd_stat['exists']} size={utd_stat['size']} mtime={utd_stat['mtime']:.3f}")
        lines.append(f"phase.json exists={phase_stat['exists']} size={phase_stat['size']} mtime={phase_stat['mtime']:.3f}")
        lines.append("runs_head:")
        for p in runs_list:
            lines.append(f"  - {p}")
        try:
            _c_ms = int(getattr(on_controller_figs, "_last_ms", -1))
        except Exception:
            _c_ms = -1
        lines.append(f"controller_dt_ms={_c_ms}")
        return "\n".join(lines)

    # Minimal figure: file size over time (isolates Plotly/dash overhead)
    @app.callback(
        Output("dbg-fig", "figure", allow_duplicate=True),
        Input("dbg-interval", "n_intervals"),
        State("dbg-components", "value"),
        State("dbg-run-dir", "value"),
        State("dbg-runs-root", "value"),
        prevent_initial_call=False,
    )
    def on_fig(_n, comps, rd, rr):
        comps = comps or []
        if "file_sizes" not in comps:
            return go.Figure()

        # Resolve absolute run_dir
        rr_abs_local = _abs((rr or "").strip())
        rd_local = (rd or "").strip()
        if rd_local and not os.path.isabs(rd_local):
            rd_abs = _abs(os.path.join(rr_abs_local, rd_local))
        else:
            rd_abs = rd_local

        events_path = os.path.join(rd_abs, "events.jsonl") if rd_abs else ""
        utd_path = os.path.join(rd_abs, "utd_events.jsonl") if rd_abs else ""

        e_stat = _file_stat(events_path) if rd_abs else {"exists": False, "size": 0}
        u_stat = _file_stat(utd_path) if rd_abs else {"exists": False, "size": 0}

        series = getattr(on_fig, "_series", {"t": [], "events": [], "utd": []})
        t = series["t"]; ev = series["events"]; ut = series["utd"]
        t.append(len(t) + 1)
        ev.append(int(e_stat.get("size", 0)))
        ut.append(int(u_stat.get("size", 0)))

        # Keep small ring buffer to bound memory/CPU
        if len(t) > 256:
            t[:] = t[-256:]; ev[:] = ev[-256:]; ut[:] = ut[-256:]
        setattr(on_fig, "_series", series)

        fig = go.Figure()
        if ev:
            fig.add_trace(go.Scatter(x=t, y=[x / 1e6 for x in ev], name="events.jsonl MB", mode="lines"))
        if ut:
            fig.add_trace(go.Scatter(x=t, y=[x / 1e6 for x in ut], name="utd_events.jsonl MB", mode="lines"))

        fig.update_layout(
            template="plotly_dark",
            margin=dict(l=30, r=10, t=30, b=30),
            xaxis_title="Tick",
            yaxis_title="Size (MB)",
            legend=dict(orientation="h"),
        )
        return fig

    # Controller charts (reuse production controller with small, bounded UI knobs)
    @app.callback(
        Output("dbg-fig-dashboard", "figure", allow_duplicate=True),
        Output("dbg-fig-discovery", "figure", allow_duplicate=True),
        Input("dbg-interval", "n_intervals"),
        State("dbg-components", "value"),
        State("dbg-run-dir", "value"),
        State("dbg-runs-root", "value"),
        State("dbg-ctrl-status-url", "value"),
        State("dbg-ctrl-status-timeout", "value"),
        State("dbg-ctrl-points-cap", "value"),
        State("dbg-ctrl-series-cap", "value"),
        State("dbg-ctrl-decimate", "value"),
        prevent_initial_call=False,
    )
    def on_controller_figs(_n, comps, rd, rr, status_url, status_timeout, points_cap, series_cap, decimate_to):
        comps = comps or []
        if "controller_charts" not in comps:
            return go.Figure(), go.Figure()

        # Resolve absolute run_dir
        rr_abs_local = _abs((rr or "").strip())
        rd_local = (rd or "").strip()
        if rd_local and not os.path.isabs(rd_local):
            rd_abs = _abs(os.path.join(rr_abs_local, rd_local))
        else:
            rd_abs = rd_local

        # Build UI dict for controller
        try:
            ui = {
                "status_url": str(status_url or "http://127.0.0.1:8787/status/snapshot"),
                "status_timeout": float(status_timeout if status_timeout is not None else 0.2),
                "maxp": int(points_cap if points_cap is not None else 800),
                "series_cap": int(series_cap if series_cap is not None else 4),
                "decimate": int(decimate_to if decimate_to is not None else 400),
            }
        except Exception:
            ui = {
                "status_url": "http://127.0.0.1:8787/status/snapshot",
                "status_timeout": 0.2,
                "maxp": 800,
                "series_cap": 4,
                "decimate": 400,
            }

        # Persist SeriesState between ticks (per-run)
        state = getattr(on_controller_figs, "_state", None)
        if not isinstance(state, _SeriesState) or getattr(state, "run_dir", None) != rd_abs:
            state = _SeriesState(rd_abs or "")
        t0 = time.perf_counter()
        fig1, fig2, new_state = _compute_dashboard_figures(rd_abs or "", state, ui)
        try:
            setattr(on_controller_figs, "_last_ms", int((time.perf_counter() - t0) * 1000.0))
        except Exception:
            pass
        setattr(on_controller_figs, "_state", new_state)
        return fig1, fig2

    return app


if __name__ == "__main__":
    # Environment-driven defaults for manual testing:
    # RUNS_ROOT: override runs root; default to ./runs
    # DASH_HOST / DASH_PORT: debug server bind (default 127.0.0.1:8060)
    rr = os.getenv("RUNS_ROOT", "").strip() or _abs("runs")
    app = build_debug_app(rr)
    host = os.getenv("DASH_HOST", "127.0.0.1")
    try:
        port = int(os.getenv("DASH_PORT", "8060"))
    except Exception:
        port = 8060
    # No debug reloader to avoid duplicate callbacks; UI is already minimal
    app.run(host=host, port=port, debug=False)