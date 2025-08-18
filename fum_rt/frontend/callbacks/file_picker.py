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

# Project root clamp: prevent navigation above repo root
PROJECT_ROOT = os.path.abspath(os.getenv("FUM_PROJECT_ROOT", "/mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs"))

def _clamp_to_project(path: str) -> str:
    return _clamp_to_root(path, PROJECT_ROOT)


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
    sel_dir_store = f"{prefix}-selected-dir"
    tree_store = f"{prefix}-tree-store"

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
        return _clamp_to_project(os.path.abspath(r)) if r else no_update

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

    # Render a single tree (folders + files) with breadcrumbs; bounded IO (no scans here)
    @app.callback(
        Output(f"{prefix}-dirs-list", "children"),
        Output(cwd_label, "children"),
        Output(f"{prefix}-crumbs", "children"),
        Input(tree_store, "data"),
        Input(sel_dir_store, "data"),
        Input(exts_store, "data"),
        Input(file_sel_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_render(tree_data, selected_dir, exts, file_sel, root):
        # Resolve root and selected directory (clamped to project root)
        try:
            rabs_in = os.path.abspath((root or "").strip()) if root else None
        except Exception:
            rabs_in = None
        rabs = _clamp_to_project(rabs_in or PROJECT_ROOT)
        s_in = (selected_dir or "").strip()
        s = os.path.abspath(s_in) if s_in else rabs
        s = _clamp_to_root(s, rabs)

        # Build tree UI from cached nodes only (no os.listdir here)
        nodes = {}
        try:
            if isinstance(tree_data, dict):
                nodes = dict(tree_data.get("nodes") or {})
                if rabs is None and tree_data.get("root"):
                    rabs = tree_data.get("root")
        except Exception:
            nodes = {}

        allow_all = not exts
        lowered_exts = [e.lower() for e in (exts or [])]

        tree_children = []

        def _tree_dir_row(path: str, name: str, depth: int, expanded: bool, is_selected: bool):
            chevron = "▾" if expanded else "▸"
            icon = "📁"
            return html.Div(
                html.Button(
                    [html.Span(chevron, style={"width": "1em"}), html.Span(icon, style={"width": "1.2em"}), html.Span(name, style={"overflow":"hidden","textOverflow":"ellipsis"})],
                    id={"role": f"{prefix}-tree-dir", "path": path},
                    n_clicks=0,
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "6px",
                        "padding": "4px 6px",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "width": "100%",
                        "textAlign": "left",
                        "background": "rgba(106,160,194,0.18)" if is_selected else "transparent",
                        "border": "1px solid rgba(35,49,64,0.0)" if not is_selected else "1px solid var(--border)",
                        "marginLeft": f"{depth * 12}px",
                    },
                )
            )

        def _tree_file_row(file_path: str, depth: int, selected: bool):
            fname = os.path.basename(file_path)
            return html.Div(
                html.Button(
                    [html.Span("•", style={"width": "1em", "opacity": 0.7}), html.Span("📄", style={"width": "1.2em"}), html.Span(fname, style={"overflow":"hidden","textOverflow":"ellipsis"})],
                    id={"role": f"{prefix}-file", "path": file_path, "name": fname},
                    n_clicks=0,
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "gap": "6px",
                        "padding": "4px 6px",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "width": "100%",
                        "textAlign": "left",
                        "background": "rgba(106,160,194,0.18)" if selected else "transparent",
                        "border": "1px solid rgba(35,49,64,0.0)" if not selected else "1px solid var(--border)",
                        "marginLeft": f"{(depth + 1) * 12}px",
                    },
                )
            )

        def _build(path: str, depth: int):
            label = os.path.basename(path) or path
            node = nodes.get(path, {})
            expanded = bool(node.get("expanded"))
            is_sel = os.path.abspath(path) == s
            tree_children.append(_tree_dir_row(path, label, depth, expanded, is_sel))
            if expanded:
                # Render subdirectories first
                for child in (node.get("subdirs") or []):
                    try:
                        ch = os.path.join(path, child)
                    except Exception:
                        continue
                    _build(ch, depth + 1)
                # Then render files belonging to this directory (cached)
                files_all = node.get("files") or []
                for f in files_all:
                    try:
                        fpath = os.path.join(path, f)
                    except Exception:
                        continue
                    if allow_all or any(f.lower().endswith(e) for e in lowered_exts):
                        tree_children.append(_tree_file_row(fpath, depth, (file_sel or "").strip() == fpath))

        start_root = rabs or s
        if start_root:
            if start_root not in nodes:
                nodes[start_root] = {"expanded": True, "subdirs": [], "files": []}
            _build(start_root, 0)

        cwd_label_text = f"cwd: {s}" if s and os.path.isdir(s) else "cwd: (missing)"

        # Breadcrumbs based on root and selected directory
        crumbs = []
        try:
            base = os.path.abspath((rabs or s) or "")
            sel = os.path.abspath(s or base)
            if base:
                root_label = os.path.basename(base) or base
                crumbs.append(html.Button(
                    root_label,
                    id={"role": f"{prefix}-crumb", "path": base},
                    n_clicks=0,
                    style={"background":"transparent","border":"none","color":"#9ab8d1","cursor":"pointer","padding":"2px 4px"},
                ))
                if sel and sel != base:
                    rel = os.path.relpath(sel, base)
                    cur = base
                    for part in rel.split(os.sep):
                        cur = os.path.join(cur, part)
                        crumbs.append(html.Span("›", style={"opacity": 0.6, "padding": "0 2px"}))
                        crumbs.append(html.Button(
                            part,
                            id={"role": f"{prefix}-crumb", "path": cur},
                            n_clicks=0,
                            style={"background":"transparent","border":"none","color":"#9ab8d1","cursor":"pointer","padding":"2px 4px"},
                        ))
        except Exception:
            pass

        return tree_children, cwd_label_text, crumbs

    # Tree toggle: expand/collapse one node; cache listing on expand (one directory at a time)
    @app.callback(
        Output(tree_store, "data", allow_duplicate=True),
        Output(sel_dir_store, "data", allow_duplicate=True),
        Input({"role": f"{prefix}-tree-dir", "path": ALL}, "n_clicks"),
        State(tree_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_tree_toggle(_clicks, tree_data, root):
        ctx = dash.callback_context
        if not getattr(ctx, "triggered", None):
            return no_update, no_update
        try:
            import json
            tid = ctx.triggered[0]["prop_id"].split(".")[0]
            obj = json.loads(tid)
            target = (obj.get("path", "") or "").strip()
        except Exception:
            return no_update, no_update
        if not target:
            return no_update, no_update

        r = (root or "").strip()
        rabs0 = os.path.abspath(r) if r else os.path.abspath(target)
        rabs = _clamp_to_project(rabs0)

        # Initialize tree structure if needed
        tree = tree_data if isinstance(tree_data, dict) else {}
        if not tree:
            tree = {"root": rabs, "nodes": {}}
        nodes = tree.get("nodes") or {}
        tree["root"] = tree.get("root") or rabs

        # Clamp and toggle
        p = _clamp_to_root(target, rabs)
        node = dict(nodes.get(p) or {})
        toggled = not bool(node.get("expanded"))
        node["expanded"] = toggled
        if toggled and (not node.get("subdirs") or not node.get("files")):
            # Bounded IO: only list this node's direct children once on expansion
            subdirs, files_all = _safe_list(p, None)
            node["subdirs"] = subdirs or []
            node["files"] = files_all or []
        nodes[p] = node
        tree["nodes"] = nodes
        return tree, p

    # Breadcrumb click -> select directory (clamped)
    @app.callback(
        Output(sel_dir_store, "data", allow_duplicate=True),
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

    # Sync selected-dir when legacy cwd changes (Root/Up)
    @app.callback(
        Output(sel_dir_store, "data", allow_duplicate=True),
        Input(cwd_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def sync_selected_dir(cwd, root):
        c = (cwd or "").strip()
        r = (root or "").strip()
        if not c:
            return no_update
        c = _clamp_to_project(c)
        if r:
            r = _clamp_to_project(r)
            return _clamp_to_root(c, r)
        return c

    # Click handlers for files inside the tree
    @app.callback(
        Output(dir_sel_store, "data"),
        Output(file_sel_store, "data"),
        Input({"role": f"{prefix}-file", "path": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_explorer_click(_file_clicks):
        ctx = dash.callback_context
        if not getattr(ctx, "triggered", None):
            return no_update, no_update
        try:
            import json
            tid = ctx.triggered[0]["prop_id"].split(".")[0]
            obj = json.loads(tid)
            fpath = (obj.get("path", "") or "").strip()
        except Exception:
            return no_update, no_update
        if not fpath:
            return no_update, no_update
        # Do not change selected directory here; only set the selected file path
        return no_update, fpath

    # Confirm selection -> set stores, hide modal, and update target value
    @app.callback(
        Output(sel_store, "data"),
        Output(sel_label, "children"),
        Output(status_div, "children"),
        Output(mid, "style", allow_duplicate=True),
        Output(target_id, "value"),
        Input(confirm_btn, "n_clicks"),
        State(file_sel_store, "data"),
        State(sel_dir_store, "data"),
        prevent_initial_call=True,
    )
    def on_confirm(_n, file_sel, sel_dir):
        fsel = (file_sel or "").strip()
        c = (sel_dir or "").strip()
        if not fsel:
            return no_update, no_update, "Select a file.", no_update, no_update
        path = fsel if os.path.isabs(fsel) else os.path.abspath(os.path.join(c, fsel)) if c else os.path.abspath(fsel)
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
        r = _clamp_to_project(os.path.abspath(root or ""))
        style = _fp_modal_styles()
        style["display"] = "flex"
        return style, r, r, list(exts or [])

    # Initialize tree and selection on open (static)
    @app.callback(
        Output(f"{prefix}-selected-dir", "data", allow_duplicate=True),
        Output(f"{prefix}-tree-store", "data", allow_duplicate=True),
        Input(open_btn, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_open_init(_n):
        r = _clamp_to_project(os.path.abspath(root or ""))
        subdirs, files_all = _safe_list(r, None)
        tree = {"root": r, "nodes": {r: {"expanded": True, "subdirs": subdirs or [], "files": files_all or []}}}
        return r, tree

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
        # choose the first existing (clamped) directory
        for cand in candidates:
            if not cand:
                continue
            r_candidate = _clamp_to_project(os.path.abspath(cand))
            if os.path.isdir(r_candidate):
                r = r_candidate
                style = _fp_modal_styles()
                style["display"] = "flex"
                return style, r, r, list(exts or [])
        # fallback: open at project root
        style = _fp_modal_styles()
        style["display"] = "flex"
        return style, PROJECT_ROOT, PROJECT_ROOT, list(exts or [])

    # Initialize tree and selection on open (dynamic)
    @app.callback(
        Output(f"{prefix}-selected-dir", "data", allow_duplicate=True),
        Output(f"{prefix}-tree-store", "data", allow_duplicate=True),
        Input(open_btn, "n_clicks"),
        State("run-dir", "value"),
        State("runs-root", "value"),
        prevent_initial_call=True,
    )
    def on_open_init_dynamic(_n, run_dir, runs_root):
        candidates = []
        rd = (run_dir or "").strip()
        rr = (runs_root or "").strip()
        if rd and os.path.isdir(rd):
            candidates.append(rd)
        if rr and os.path.isdir(rr):
            candidates.append(rr)
        if fallback_root:
            candidates.append(fallback_root)
        for cand in candidates:
            if not cand:
                continue
            r = _clamp_to_project(os.path.abspath(cand))
            if os.path.isdir(r):
                subdirs, files_all = _safe_list(r, None)
                tree = {"root": r, "nodes": {r: {"expanded": True, "subdirs": subdirs or [], "files": files_all or []}}}
                return r, tree
        r = PROJECT_ROOT
        subdirs, files_all = _safe_list(r, None)
        tree = {"root": r, "nodes": {r: {"expanded": True, "subdirs": subdirs or [], "files": files_all or []}}}
        return r, tree

    _register_common(app, prefix, target_id)