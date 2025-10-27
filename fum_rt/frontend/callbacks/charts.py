"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
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
        State("charts-series-custom-map", "data"),
        State("charts-series-defaults", "data"),
        prevent_initial_call=False,
    )
    def update_figs(_n, run_dir, proc_status, ui_state, series_tab, custom_map, defaults):
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

        # Series visibility toggle to preserve layout and axes:
        # - "__add__": do nothing (user is creating a new tab)
        # - "all": show all traces
        # - default labeled tab: show that single trace (others legendonly)
        # - custom tab (in custom_map): show listed traces (others legendonly)
        try:
            tab = (series_tab or "").strip()
            # Default: ensure everything visible
            for tr in fig1.data:
                try:
                    tr.visible = True
                except Exception:
                    continue

            if tab and tab.lower() != "all" and tab != "__add__":
                names = None
                if isinstance(custom_map, dict) and tab in custom_map:
                    v = custom_map.get(tab)
                    if isinstance(v, (list, tuple)):
                        names = {str(x) for x in v if isinstance(x, str) and x.strip()}

                if not names:
                    names = {tab}

                matched = 0
                for tr in fig1.data:
                    try:
                        nm = getattr(tr, "name", "")
                        if nm in names:
                            tr.visible = True
                            matched += 1
                        else:
                            tr.visible = "legendonly"
                    except Exception:
                        continue

                # If nothing matched (e.g., label mismatch), revert to all visible
                if matched == 0:
                    for tr in fig1.data:
                        try:
                            tr.visible = True
                        except Exception:
                            continue
        except Exception:
            pass

        setattr(update_figs, "_state", new_state)
        return fig1

# -- Series tabs (+) flow: add custom tabs and map them to multiple series
def register_series_tabs_plus(app):
    from dash import dcc  # local import

    def _build_children(defaults: list[str] | None, cmap: dict | None):
        defaults = [str(x) for x in (defaults or [])]
        cmap = dict(cmap or {})
        kids = [
            dcc.Tab(label="All", value="all", className="fum-tab", selected_className="fum-tab--selected")
        ]
        for lbl in defaults:
            kids.append(dcc.Tab(label=lbl, value=lbl, className="fum-tab", selected_className="fum-tab--selected"))
        # Append custom tabs in insertion order
        for lbl in cmap.keys():
            if lbl and lbl not in defaults and lbl not in ("all", "__add__"):
                kids.append(dcc.Tab(label=lbl, value=lbl, className="fum-tab", selected_className="fum-tab--selected"))
        kids.append(dcc.Tab(label="+", value="__add__", className="fum-tab add", selected_className="fum-tab--selected add"))
        return kids

    # Toggle visibility of '+' controls vs series picker based on active tab
    @app.callback(
        Output("charts-add-controls", "style"),
        Output("charts-series-custom-controls", "style"),
        Input("charts-series-tabs", "value"),
        State("charts-series-defaults", "data"),
        prevent_initial_call=False,
    )
    def _toggle_plus_controls(active, defaults):
        hide = {"display": "none", "minWidth": "0", "gap": "6px"}
        show_add = {"display": "grid", "gridTemplateColumns": "1fr auto auto", "gap": "6px", "minWidth": "0"}
        show_picker = {"display": "grid", "gap": "6px", "minWidth": "0"}
        a = (active or "").strip()
        if a == "__add__":
            return show_add, hide
        if a.lower() == "all" or a in (defaults or []):
            return hide, hide
        # Custom tab: show picker
        return hide, show_picker

    # Create a new custom tab when user confirms name (Enter/blur due to debounce=True)
    @app.callback(
        Output("charts-series-tabs", "children"),
        Output("charts-series-tabs", "value"),
        Output("charts-series-custom-map", "data"),
        Output("charts-add-name", "value"),
        Input("charts-add-name", "value"),
        State("charts-series-defaults", "data"),
        State("charts-series-custom-map", "data"),
        State("charts-series-tabs", "value"),
        prevent_initial_call=True,
    )
    def _create_on_name(name, defaults, cmap, active):
        defaults = list(defaults or [])
        cmap = dict(cmap or {})
        a = (active or "").strip()
        nm = (name or "").strip()
        # Only act when '+' tab is active and a non-empty, non-conflicting name is provided
        if a != "__add__" or not nm or nm in defaults or nm in cmap or nm in ("all", "__add__"):
            return no_update, active, no_update, name
        cmap[nm] = []  # start with no series selected; user can pick via picker
        children = _build_children(defaults, cmap)
        return children, nm, cmap, ""

    # When switching tabs, sync the picker value to the custom map for that tab
    @app.callback(
        Output("charts-series-picker", "value"),
        Input("charts-series-tabs", "value"),
        State("charts-series-custom-map", "data"),
        prevent_initial_call=True,
    )
    def _sync_picker(tab, cmap):
        tab = (tab or "").strip()
        cmap = dict(cmap or {})
        if tab in cmap:
            vals = cmap.get(tab) or []
            if isinstance(vals, list):
                return [v for v in vals if isinstance(v, str)]
        return []

    # Update the map when picker changes for a custom tab
    @app.callback(
        Output("charts-series-custom-map", "data"),
        Input("charts-series-picker", "value"),
        State("charts-series-tabs", "value"),
        State("charts-series-custom-map", "data"),
        prevent_initial_call=True,
    )
    def _update_map(selected, tab, cmap):
        tab = (tab or "").strip()
        cmap = dict(cmap or {})
        if not tab or tab in ("all", "__add__"):
            return no_update
        if not isinstance(selected, list):
            return no_update
        cmap[tab] = [str(v) for v in selected if isinstance(v, str)]
        return cmap