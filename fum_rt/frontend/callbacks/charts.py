from __future__ import annotations

import plotly.graph_objs as go
from dash import Input, Output  # noqa: F401 (Dash binds these at runtime)
from fum_rt.frontend.controllers.charts_controller import compute_dashboard_figures
from fum_rt.frontend.models.series import SeriesState  # for type awareness in compute


def register_chart_callbacks(app):
    """
    Register figure update callbacks on the provided Dash app.
    Delegates business logic to controllers.compute_dashboard_figures
    so it can be reused outside Dash (e.g., batch exporters).
    """

    @app.callback(
        Output("fig-dashboard", "figure"),
        Output("fig-discovery", "figure"),
        Input("poll", "n_intervals"),
        Input("run-dir", "value"),
        Input("proc-status", "children"),
        prevent_initial_call=False,
    )
    def update_figs(_n, run_dir, proc_status):
        if not run_dir:
            return go.Figure(), go.Figure()

        # Clear once when process (re)starts or resumes (avoid perpetual resets).
        try:
            last_ps = getattr(update_figs, "_last_proc_status", None)
            if isinstance(proc_status, str) and proc_status != last_ps:
                if ("Resumed." in proc_status) or ("Started." in proc_status):
                    setattr(update_figs, "_state", None)
            setattr(update_figs, "_last_proc_status", proc_status)
        except Exception:
            pass

        state = getattr(update_figs, "_state", None)
        fig1, fig2, new_state = compute_dashboard_figures(run_dir, state)
        setattr(update_figs, "_state", new_state)
        return fig1, fig2