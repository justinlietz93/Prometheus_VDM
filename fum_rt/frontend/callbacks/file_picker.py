from __future__ import annotations

"""
Dash callbacks for the reusable file picker component.

Design goals:
- Bounded IO: list one directory at a time (no recursive scans)
- Themed modal overlay visibility toggled via style (preserves dark theme)
- Reusable registrations:
    - register_file_picker_static: fixed root
    - register_file_picker_engram: dynamic root = run-dir if set, else runs-root (fallback param as last resort)
- Integration strategy: picker writes chosen absolute path into a target component's 'value' prop
  (e.g., hidden dcc.Input with id='feed-path', 'profile-path', 'rc-load-engram-path') so existing callbacks keep working.

No scans in core/ or maps/ directories. Only shallow os.listdir() on the chosen cwd.
"""

import os
from typing import List, Tuple

import dash
from dash import html, Input, Output, State, ALL, no_update
from fum_rt.frontend.components.widgets.file_picker import _modal_styles as _fp_modal_styles


def _safe_list(path: str, exts: List[str] | None) -> Tuple[List[str], List[str]]:
    """
    Return (subdirs, files) for a directory, filtered by exts when provided.
    - subdirs: immediate child folders (names only)
    - files: immediate child files (names only), filtering by allowed extensions when provided
    """
    try:
        names = os.listdir(path)
    except Exception:
        return [], []
    subdirs = []
    files = []
    allow_all = not exts
    lowered_exts = [e.lower() for e in (exts or [])]
    for n in names:
        full = os.path.join(path, n)
        if os.path.isdir(full):
            subdirs.append(n)
        else:
            if allow_all or any(n.lower().endswith(e) for e in lowered_exts):
                files.append(n)
    subdirs.sort()
    files.sort()
    return subdirs, files


def _clamp_to_root(path: str, root: str) -> str:
    """
    Ensure 'path' does not escape 'root'. If it does, clamp to root.
    """
    try:
        root_abs = os.path.abspath(root)
        path_abs = os.path.abspath(path)
        common = os.path.commonpath([root_abs, path_abs])
        return path_abs if common == root_abs else root_abs
    except Exception:
        return os.path.abspath(root)


def _register_common(app, prefix: str, target_id: str) -> None:
    """
    Register navigation, list population, cancel, and confirm callbacks for a file-picker instance.
    The 'open' callback is registered by static/dynamic functions.
    """
    mid = f"{prefix}-modal"
    root_store = f"{prefix}-root"
    cwd_store = f"{prefix}-cwd"
    exts_store = f"{prefix}-exts"
    dirs_dd = f"{prefix}-dirs"
    files_dd = f"{prefix}-files"
    cwd_label = f"{prefix}-cwd-label"
    status_div = f"{prefix}-status"
    up_btn = f"{prefix}-up-btn"
    root_btn = f"{prefix}-root-btn"
    open_dir_btn = f"{prefix}-open-dir-btn"
    cancel_btn = f"{prefix}-cancel-btn"
    confirm_btn = f"{prefix}-confirm-btn"
    sel_store = f"{prefix}-selected-path"
    sel_label = f"{prefix}-selected-label"
    dir_sel_store = f"{prefix}-dir-sel"
    file_sel_store = f"{prefix}-file-sel"

    # Cancel -> hide modal
    @app.callback(
        Output(mid, "style", allow_duplicate=True),
        Input(cancel_btn, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_cancel(_n):
        style = _fp_modal_styles()
        # Keep 'display' as defined by component default (hidden)
        return style

    # Navigate to root
    @app.callback(
        Output(cwd_store, "data", allow_duplicate=True),
        Input(root_btn, "n_clicks"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_root(_n, root):
        r = (root or "").strip()
        return os.path.abspath(r) if r else no_update

    # Navigate up
    @app.callback(
        Output(cwd_store, "data", allow_duplicate=True),
        Input(up_btn, "n_clicks"),
        State(cwd_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_up(_n, cwd, root):
        c = (cwd or "").strip()
        r = (root or "").strip()
        if not c or not r:
            return no_update
        parent = os.path.dirname(os.path.abspath(c))
        return _clamp_to_root(parent, r)

    # Open selected subfolder
    @app.callback(
        Output(cwd_store, "data", allow_duplicate=True),
        Input(open_dir_btn, "n_clicks"),
        State(dir_sel_store, "data"),
        State(cwd_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_open_dir(_n, sel, cwd, root):
        s = (sel or "").strip()
        c = (cwd or "").strip()
        r = (root or "").strip()
        if not s or not c:
            return no_update
        cand = os.path.join(c, s)
        if os.path.isdir(cand):
            return _clamp_to_root(cand, r or cand)
        return no_update

    # Populate lists whenever cwd or exts or selection changes (render actual explorer lists + crumbs)
    @app.callback(
        Output(f"{prefix}-dirs-list", "children"),
        Output(f"{prefix}-files-list", "children"),
        Output(cwd_label, "children"),
        Output(f"{prefix}-crumbs", "children"),
        Input(cwd_store, "data"),
        Input(exts_store, "data"),
        Input(dir_sel_store, "data"),
        Input(file_sel_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_cwd_changed(cwd, exts, dir_sel, file_sel, root):
        c = (cwd or "").strip()
        if not c or not os.path.isdir(c):
            return [], [], "cwd: (missing)", []

        subdirs, files = _safe_list(c, (exts or []))

        def _item(name: str, is_dir: bool, selected: bool):
            base_style = {
                "display": "flex",
                "alignItems": "center",
                "gap": "8px",
                "padding": "6px 8px",
                "borderRadius": "6px",
                "cursor": "pointer",
                "width": "100%",
                "textAlign": "left",
                "background": "rgba(106,160,194,0.18)" if selected else "transparent",
                "border": "1px solid rgba(35,49,64,0.0)" if not selected else "1px solid var(--border)",
            }
            role = f"{prefix}-dir" if is_dir else f"{prefix}-file"
            icon = "📁" if is_dir else "📄"
            return html.Button(
                [html.Span(icon, style={"width": "1.2em"}), html.Span(name, style={"overflow":"hidden","textOverflow":"ellipsis"})],
                id={"role": role, "name": name},
                n_clicks=0,
                style=base_style,
            )

        dir_children = [_item(d, True, d == (dir_sel or "")) for d in subdirs]
        file_children = [_item(f, False, f == (file_sel or "")) for f in files]

        # Build breadcrumbs relative to root (clamped)
        try:
            rabs = os.path.abspath((root or "").strip()) if root else os.path.abspath(c)
            cabs = os.path.abspath(c)
            cabs = _clamp_to_root(cabs, rabs)
            rel = os.path.relpath(cabs, rabs)
        except Exception:
            rabs, cabs, rel = os.path.abspath(c or "."), os.path.abspath(c or "."), "."

        crumbs = []

        def _crumb_btn(label: str, path: str):
            return html.Button(
                label,
                id={"role": f"{prefix}-crumb", "path": path},
                n_clicks=0,
                style={
                    "background": "transparent",
                    "border": "none",
                    "color": "#9ab8d1",
                    "cursor": "pointer",
                    "padding": "2px 4px",
                },
            )

        root_label = os.path.basename(rabs) or rabs
        crumbs.append(_crumb_btn(root_label, rabs))
        if rel and rel != ".":
            cur = rabs
            for part in rel.split(os.sep):
                cur = os.path.join(cur, part)
                crumbs.append(html.Span("›", style={"opacity": 0.6, "padding": "0 2px"}))
                crumbs.append(_crumb_btn(part, cur))

        return dir_children, file_children, f"cwd: {cabs}", crumbs

    # Breadcrumb click -> navigate to that directory (clamped to root)
    @app.callback(
        Output(cwd_store, "data", allow_duplicate=True),
        Input({"role": f"{prefix}-crumb", "path": ALL}, "n_clicks"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_crumb_click(_clicks, root):
        ctx = dash.callback_context
        if not getattr(ctx, "triggered", None):
            return no_update
        try:
            import json
            tid = ctx.triggered[0]["prop_id"].split(".")[0]
            obj = json.loads(tid)
            target = (obj.get("path", "") or "").strip()
        except Exception:
            return no_update
        if not target:
            return no_update
        r = (root or "").strip()
        if r:
            return _clamp_to_root(target, r)
        return target

    # Click handlers for directory/file items in explorer lists
    @app.callback(
        Output(dir_sel_store, "data"),
        Output(file_sel_store, "data"),
        Input({"role": f"{prefix}-dir", "name": ALL}, "n_clicks"),
        Input({"role": f"{prefix}-file", "name": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_explorer_click(_dir_clicks, _file_clicks):
        ctx = dash.callback_context
        if not getattr(ctx, "triggered", None):
            return no_update, no_update
        try:
            import json
            tid = ctx.triggered[0]["prop_id"].split(".")[0]
            obj = json.loads(tid)
            role = obj.get("role", "")
            name = (obj.get("name", "") or "").strip()
        except Exception:
            return no_update, no_update
        if not name:
            return no_update, no_update
        if role == f"{prefix}-dir":
            # Select directory; keep file selection unchanged
            return name, ""
        if role == f"{prefix}-file":
            # Select file; keep directory selection unchanged
            return no_update, name
        return no_update, no_update

    # Confirm selection -> set stores, hide modal, and update target value
    @app.callback(
        Output(sel_store, "data"),
        Output(sel_label, "children"),
        Output(status_div, "children"),
        Output(mid, "style", allow_duplicate=True),
        Output(target_id, "value"),
        Input(confirm_btn, "n_clicks"),
        State(file_sel_store, "data"),
        State(cwd_store, "data"),
        prevent_initial_call=True,
    )
    def on_confirm(_n, file_name, cwd):
        f = (file_name or "").strip()
        c = (cwd or "").strip()
        if not f or not c:
            # no selection; keep modal open
            return no_update, no_update, "Select a file.", no_update, no_update
        path = os.path.abspath(os.path.join(c, f))
        label = os.path.basename(path)
        status = f"Selected: {path}"
        style = _fp_modal_styles()  # hidden (default)
        return path, label, status, style, path


def register_file_picker_static(app, prefix: str, root: str, exts: List[str] | None, target_id: str) -> None:
    """
    Register a file-picker with a fixed root.
    """
    mid = f"{prefix}-modal"
    root_store = f"{prefix}-root"
    cwd_store = f"{prefix}-cwd"
    exts_store = f"{prefix}-exts"
    open_btn = f"{prefix}-open-btn"

    # Open -> show modal and initialize stores
    @app.callback(
        Output(mid, "style", allow_duplicate=True),
        Output(root_store, "data"),
        Output(cwd_store, "data", allow_duplicate=True),
        Output(exts_store, "data"),
        Input(open_btn, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_open(_n):
        r = os.path.abspath(root or "")
        style = _fp_modal_styles()
        style["display"] = "flex"
        return style, r, r, list(exts or [])

    _register_common(app, prefix, target_id)


def register_file_picker_engram(
    app,
    prefix: str,
    exts: List[str] | None,
    target_id: str,
    fallback_root: str,
) -> None:
    """
    Register a file-picker whose root = current run-dir if available, else runs-root, else fallback_root.
    """
    mid = f"{prefix}-modal"
    root_store = f"{prefix}-root"
    cwd_store = f"{prefix}-cwd"
    exts_store = f"{prefix}-exts"
    open_btn = f"{prefix}-open-btn"

    # Open -> compute root dynamically from run-dir / runs-root
    @app.callback(
        Output(mid, "style", allow_duplicate=True),
        Output(root_store, "data"),
        Output(cwd_store, "data", allow_duplicate=True),
        Output(exts_store, "data"),
        Input(open_btn, "n_clicks"),
        State("run-dir", "value"),
        State("runs-root", "value"),
        prevent_initial_call=True,
    )
    def on_open_dynamic(_n, run_dir, runs_root):
        candidates = []
        rd = (run_dir or "").strip()
        rr = (runs_root or "").strip()
        if rd and os.path.isdir(rd):
            candidates.append(rd)
        if rr and os.path.isdir(rr):
            candidates.append(rr)
        if fallback_root:
            candidates.append(fallback_root)
        # choose the first existing directory
        for cand in candidates:
            if cand and os.path.isdir(cand):
                r = os.path.abspath(cand)
                style = _fp_modal_styles()
                style["display"] = "flex"
                return style, r, r, list(exts or [])
        # fallback: still open but with empty root/cwd
        style = _fp_modal_styles()
        style["display"] = "flex"
        return style, "", "", list(exts or [])

    _register_common(app, prefix, target_id)