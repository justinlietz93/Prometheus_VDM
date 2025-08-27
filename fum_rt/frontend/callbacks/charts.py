from __future__ import annotations

import plotly.graph_objs as go
from dash import Input, Output, State, no_update, dcc  # noqa: F401 (Dash binds these at runtime)
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
        Input("poll", "n_intervals"),
        Input("run-dir", "value"),
        Input("proc-status", "children"),
        Input("ui-state", "data"),
        Input("charts-series-tabs", "value"),
        prevent_initial_call=False,
    )
    def update_figs(_n, run_dir, proc_status, ui_state, series_tab):
        if not run_dir:
            return go.Figure()

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
        ui = ui_state or {}
        fig1, _fig2, new_state = compute_dashboard_figures(run_dir, state, ui)

        # Optional series filter via tabs on the Dashboard graph; match trace by name.
        try:
            if series_tab and str(series_tab).strip().lower() != "all":
                selected = str(series_tab).strip()
                filt = go.Figure()
                for tr in fig1.data:
                    try:
                        if getattr(tr, "name", "") == selected:
                            filt.add_trace(tr)
                    except Exception:
                        continue
                # Preserve original layout even if only one trace remains
                filt.update_layout(fig1.layout)
                # Fall back to original if no traces matched
                fig1 = filt if len(filt.data) > 0 else fig1
        except Exception:
            # Non-fatal; keep original fig if filter fails
            pass

        setattr(update_figs, "_state", new_state)
        return fig1

# -- Dynamic series tabs: allow user to apply CSV labels to tabs
def _safe_labels(csv_text: str) -> list[str]:
    try:
        raw = (csv_text or "").strip()
        if not raw:
            return []
        return [s.strip() for s in raw.split(",") if s and s.strip()]
    except Exception:
        return []


def register_series_tabs_customization(app):
    from dash import dcc  # local import to avoid issues if not used elsewhere

    @app.callback(
        Output("charts-series-tabs", "children"),
        Output("charts-series-tabs", "value"),
        Input("charts-series-apply", "n_clicks"),
        State("charts-series-input", "value"),
        prevent_initial_call=True,
    )
    def _apply_series_tabs(_n, csv_text):
        labels = _safe_labels(csv_text or "")
        if not labels:
            return no_update, no_update
        # Always include "All" first
        children = [dcc.Tab(label="All", value="all")] + [dcc.Tab(label=l, value=l) for l in labels]
        return children, "all"