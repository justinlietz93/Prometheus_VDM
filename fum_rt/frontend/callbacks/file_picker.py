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
from fum_rt.frontend.controllers.file_picker_controller import (
    clamp_to_root as _ctl_clamp,
    list_dir as _ctl_list_dir,
    init_tree as _ctl_init_tree,
    next_children as _ctl_next_children,
)

# Project root clamp: prevent navigation above repo root
PROJECT_ROOT = os.path.abspath(os.getenv("FUM_PROJECT_ROOT", "/mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs"))

def _clamp_to_project(path: str) -> str:
    return _ctl_clamp(path, PROJECT_ROOT)

# Robust Dash ctx parsing helpers (avoid mis-parsing when component set changes)
def _get_ctx_obj(ctx):
    """
    Return the pattern-matched dict id for the triggering component if available.
    Works on newer Dash (ctx.triggered_id) and older (JSON prop_id).
    """
    try:
        tid = getattr(ctx, "triggered_id", None)
        if isinstance(tid, dict):
            return tid
    except Exception:
        pass
    try:
        import json
        tid_s = ctx.triggered[0]["prop_id"].rsplit(".", 1)[0]
        return json.loads(tid_s)
    except Exception:
        return None

def _human_size(n: int) -> str:
    """
    Convert byte count to a human-readable string in MB/GB/TB with 2 decimals.
    """
    try:
        n = int(n)
    except Exception:
        return "0 B"
    units = [("TB", 1024**4), ("GB", 1024**3), ("MB", 1024**2), ("KB", 1024), ("B", 1)]
    for label, factor in units:
        if n >= factor:
            if factor == 1:
                return f"{n} B"
            return f"{n / factor:.2f} {label}"
    return "0 B"

def _sum_filesizes(dir_path: str, filenames: list[str]) -> int:
    """
    Bounded size aggregation for immediate files (non-recursive).
    Respects controller-level guards because 'filenames' should come from list_dir().
    """
    total = 0
    for name in (filenames or []):
        try:
            fp = os.path.join(dir_path, name)
            if os.path.isfile(fp):
                total += os.path.getsize(fp)
        except Exception:
            # Ignore entries causing IO/stat errors
            continue
    return total






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
        return _ctl_clamp(parent, r)

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
            return _ctl_clamp(cand, r or cand)
        return no_update

    # Render a single tree (folders + files) with breadcrumbs; bounded IO (no scans here)
    @app.callback(
        Output(f"{prefix}-dirs-list", "children"),
        Output(cwd_label, "children"),
        Output(f"{prefix}-crumbs", "children"),
        Output(status_div, "children", allow_duplicate=True),
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
        s = _ctl_clamp(s, rabs)

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
                    id={"role": f"{prefix}-file", "path": file_path},
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
                # Then render files belonging to this directory.
                # Use cached node files; if absent, do a bounded one-step listing with ext filter & dotfile hiding.
                files_all = node.get("files") or []
                if (not files_all) and os.path.isdir(path):
                    try:
                        _subdirs_tmp, files_tmp = _ctl_list_dir(path, exts=(exts or []), hide_dotfiles=True)
                        files_all = files_tmp or []
                    except Exception:
                        files_all = []
                for f in files_all:
                    try:
                        fpath = os.path.join(path, f)
                    except Exception:
                        continue
                    # node files are already ext-filtered; keep downstream filter for robustness
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

        # Metadata statusbar
        fsel = (file_sel or "").strip()
        if fsel:
            # File selected: show name and total size
            try:
                fname = os.path.basename(fsel)
                size_b = os.path.getsize(fsel) if os.path.isfile(fsel) else 0
                status_text = f"File: {fname} — Size: {_human_size(size_b)}"
            except Exception:
                status_text = f"File: {os.path.basename(fsel)} — Size: unknown"
        else:
            # Folder selected: show counts and non-recursive total size of visible files
            try:
                subdirs_for_sel, files_for_sel = _ctl_list_dir(s, exts=(exts or []), hide_dotfiles=True) if (s and os.path.isdir(s)) else ([], [])
                folders_n = len(subdirs_for_sel or [])
                files_n = len(files_for_sel or [])
                total_b = _sum_filesizes(s, files_for_sel or [])
                status_text = f"Contains: {folders_n} folders; {files_n} files; Total Size: {_human_size(total_b)}"
            except Exception:
                status_text = "Contains: 0 folders; 0 files; Total Size: 0 B"

        return tree_children, cwd_label_text, crumbs, status_text

    # Tree toggle: expand/collapse one node; cache listing on expand (one directory at a time)
    @app.callback(
        Output(tree_store, "data", allow_duplicate=True),
        Output(sel_dir_store, "data", allow_duplicate=True),
        Input({"role": f"{prefix}-tree-dir", "path": ALL}, "n_clicks"),
        State(tree_store, "data"),
        State(root_store, "data"),
        State(exts_store, "data"),
        prevent_initial_call=True,
    )
    def on_tree_toggle(_clicks, tree_data, root, exts):
        ctx = dash.callback_context
        obj = _get_ctx_obj(ctx)
        if not isinstance(obj, dict) or obj.get("role") != f"{prefix}-tree-dir":
            return no_update, no_update
        target = (obj.get("path", "") or "").strip()
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
        p = _ctl_clamp(target, rabs)
        node = dict(nodes.get(p) or {})
        # Never collapse the root node to avoid "everything disappears" UX
        if os.path.abspath(p) == os.path.abspath(rabs):
            node["expanded"] = True
        else:
            toggled = not bool(node.get("expanded"))
            node["expanded"] = toggled
        if node.get("expanded") and (not node.get("subdirs") or not node.get("files")):
            # Bounded IO: list this node's direct children once on expansion (ext-filtered, dotfiles hidden)
            subdirs, files_all = _ctl_next_children(p, exts=(exts or []), hide_dotfiles=True)
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
        obj = _get_ctx_obj(ctx)
        if not isinstance(obj, dict) or obj.get("role") != f"{prefix}-crumb":
            return no_update
        target = (obj.get("path", "") or "").strip()
        if not target:
            return no_update
        r = (root or "").strip()
        if r:
            return _ctl_clamp(target, r)
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
            return _ctl_clamp(c, r)
        return c

    # Clear stale file selection when directory changes
    @app.callback(
        Output(file_sel_store, "data", allow_duplicate=True),
        Input(sel_dir_store, "data"),
        prevent_initial_call=True,
    )
    def _clear_file_sel_on_dir_change(_sel):
        return ""
    
    # Click handlers for files inside the tree
    @app.callback(
        Output(dir_sel_store, "data"),
        Output(file_sel_store, "data", allow_duplicate=True),
        Output(status_div, "children", allow_duplicate=True),
        Input({"role": f"{prefix}-file", "path": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_explorer_click(_file_clicks):
        ctx = dash.callback_context
        obj = _get_ctx_obj(ctx)
        if not isinstance(obj, dict) or obj.get("role") != f"{prefix}-file":
            return no_update, no_update, no_update
        fpath = (obj.get("path", "") or "").strip()
        if not fpath:
            return no_update, no_update, no_update
        # Do not change selected directory here; only set the selected file path
        base = os.path.basename(fpath) if fpath else ""
        try:
            size_b = os.path.getsize(fpath) if os.path.isfile(fpath) else 0
            status = f"File: {base} — Size: {_human_size(size_b)}"
        except Exception:
            status = f"File: {base} — Size: unknown"
        return no_update, fpath, status

    # Confirm selection -> set stores, hide modal, and update target value
    @app.callback(
        Output(sel_store, "data"),
        Output(sel_label, "children"),
        Output(status_div, "children", allow_duplicate=True),
        Output(mid, "style", allow_duplicate=True),
        Output(target_id, "options", allow_duplicate=True),
        Output(target_id, "value", allow_duplicate=True),
        Input(confirm_btn, "n_clicks"),
        State(file_sel_store, "data"),
        State(sel_dir_store, "data"),
        State(target_id, "options"),
        prevent_initial_call=True,
    )
    def on_confirm(_n, file_sel, sel_dir, options):
        fsel = (file_sel or "").strip()
        c = (sel_dir or "").strip()
        if not fsel:
            return no_update, no_update, "Select a file.", no_update, no_update, no_update
        path = fsel if os.path.isabs(fsel) else (os.path.abspath(os.path.join(c, fsel)) if c else os.path.abspath(fsel))
        label = os.path.basename(path)

        # Ensure Dropdown 'options' contains the selected path to avoid client-side validation blocking the update
        try:
            existing = options if isinstance(options, list) else []
        except Exception:
            existing = []
        try:
            vals = set()
            new_options = []
            for o in existing:
                if isinstance(o, dict):
                    v = o.get("value")
                    if isinstance(v, str) and v not in vals:
                        vals.add(v)
                        new_options.append(o)
            if path not in vals:
                new_options.append({"label": path, "value": path})
        except Exception:
            new_options = [{"label": path, "value": path}]

        status = f"Selected: {path}"
        style = _fp_modal_styles()  # hidden (default)
        return path, label, status, style, new_options, path


def register_file_picker_static(app, prefix: str, root: str, exts: List[str] | None, target_id: str) -> None:
    """
    Register a file-picker with a fixed root.
    """
    mid = f"{prefix}-modal"
    root_store = f"{prefix}-root"
    cwd_store = f"{prefix}-cwd"
    exts_store = f"{prefix}-exts"
    status_div = f"{prefix}-status"
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
        r0 = _clamp_to_project(os.path.abspath(root or ""))
        r = r0 if os.path.isdir(r0) else PROJECT_ROOT
        style = _fp_modal_styles()
        style["display"] = "flex"
        return style, r, r, list(exts or [])

    # Initialize tree and selection on open (static)
    @app.callback(
        Output(f"{prefix}-selected-dir", "data", allow_duplicate=True),
        Output(f"{prefix}-tree-store", "data", allow_duplicate=True),
        Output(status_div, "children", allow_duplicate=True),
        Input(open_btn, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_open_init(_n):
        r0 = _clamp_to_project(os.path.abspath(root or ""))
        r = r0 if os.path.isdir(r0) else PROJECT_ROOT
        tree = _ctl_init_tree(r, exts=(exts or []), hide_dotfiles=True)
        try:
            files0 = (tree.get("nodes", {}).get(r, {}) or {}).get("files") or []
            status_text = f"root: {r}  files: {len(files0)}"
        except Exception:
            status_text = f"root: {r}  files: 0"
        return r, tree, status_text

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
    status_div = f"{prefix}-status"
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
        Output(status_div, "children", allow_duplicate=True),
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
                tree = _ctl_init_tree(r, exts=(exts or []), hide_dotfiles=True)
                try:
                    files0 = (tree.get("nodes", {}).get(r, {}) or {}).get("files") or []
                    status_text = f"root: {r}  files: {len(files0)}"
                except Exception:
                    status_text = f"root: {r}  files: 0"
                return r, tree, status_text
        r = PROJECT_ROOT
        tree = _ctl_init_tree(r, exts=(exts or []), hide_dotfiles=True)
        try:
            files0 = (tree.get("nodes", {}).get(r, {}) or {}).get("files") or []
            status_text = f"root: {r}  files: {len(files0)}"
        except Exception:
            status_text = f"root: {r}  files: 0"
        return r, tree, status_text

    _register_common(app, prefix, target_id)