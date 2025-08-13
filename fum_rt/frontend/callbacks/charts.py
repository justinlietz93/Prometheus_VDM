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
        prevent_initial_call=False,
    )
    def update_figs(_n, run_dir):
        if not run_dir:
            return go.Figure(), go.Figure()

        state = getattr(update_figs, "_state", None)
        fig1, fig2, new_state = compute_dashboard_figures(run_dir, state)
        setattr(update_figs, "_state", new_state)
        return fig1, fig2