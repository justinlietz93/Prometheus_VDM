from __future__ import annotations

"""
File Picker Common Callback Registrar (package-scoped)

Shared callback logic:
- Navigation (root/up/open-dir)
- Tree render (bounded IO; no recursion)
- Breadcrumbs
- Status computation (dir vs file)
- File click and Confirm

Design:
- Bounded IO (single-directory listings only)
- No scans in core/ or maps/ (enforced in controllers)
"""

import os
from typing import List
import os

import dash
from dash import html, Input, Output, State, ALL, no_update

# Widgets
from fum_rt.frontend.components.widgets.file_picker import _modal_styles as _fp_modal_styles
from fum_rt.frontend.components.widgets.file_tree import dir_row as _w_dir_row, file_row as _w_file_row
from fum_rt.frontend.components.widgets.file_breadcrumbs import breadcrumbs as _w_breadcrumbs

# Controllers (bounded IO + guards)
from fum_rt.frontend.controllers.file_picker_controller import (
    clamp_to_root as _ctl_clamp,
    list_dir as _ctl_list_dir,
    next_children as _ctl_next_children,
)

# Controller helpers for ctx parsing and status formatting
from fum_rt.frontend.controllers.file_picker_ctx import get_trigger_id_obj as _get_ctx_obj
from fum_rt.frontend.controllers.file_picker_status import (
    file_status_text as _file_status_text,
    directory_status_text as _dir_status_text,
)
# ---------- helpers ----------
def _truncate_middle(name: str, max_len: int = 48) -> str:
    """
    Truncate a filename with a middle ellipsis, preserving the extension.
    Format target: 'Start … End.ext' (spaces around ellipsis; extension always visible)
    """
    try:
        s = str(name)
    except Exception:
        return name
    if len(s) <= max_len:
        return s
    base, ext = os.path.splitext(s)
    # Reserve for ' … ' and extension
    ell = " … "
    reserve = len(ell) + len(ext)
    if max_len <= reserve + 2:
        # Extreme constraint: keep 1 char of base then ellipsis then ext
        head_len = max(1, max_len - reserve)
        return base[:head_len] + ell + ext
    remain = max_len - reserve
    left = remain // 2
    right = remain - left
    return base[:left] + ell + base[-right:] + ext


def register_file_picker_common(app, prefix: str, target_id: str, project_root: str) -> None:
    """
    Register navigation, list population, cancel, file click, and confirm callbacks
    for a file-picker instance. The 'open' callbacks (static/dynamic) are provided by registrars.

    Args:
      app: Dash app
      prefix: ID prefix for this instance
      target_id: Component id whose options/value will be updated on Confirm
      project_root: Absolute repository root for global clamp
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
    last_action_store = f"{prefix}-last-action"

    def _clamp_to_project(path: str) -> str:
        return _ctl_clamp(path, project_root)

    # Cancel -> hide modal
    @app.callback(
        Output(mid, "style", allow_duplicate=True),
        Output(mid, "className", allow_duplicate=True),
        Input(cancel_btn, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_cancel(_n):
        # Hide modal and drop the 'modal-open' class (pure CSS governs grid pinning)
        style = _fp_modal_styles()
        return style, "fum-modal"

    # Preserve modal-open class during in-modal interactions (feed/nav/file)
    # Rationale: some layouts may re-render subtrees during navigation, which can drop className on the modal root.
    # This guard reasserts "fum-modal modal-open" whenever the user interacts with the tree/breadcrumbs (nav/file),
    # ensuring CSS :has(.fum-modal.modal-open) locks background scroll and disables background interactions.
    @app.callback(
        Output(mid, "className", allow_duplicate=True),
        Input(last_action_store, "data"),
        prevent_initial_call=True,
    )
    def _keep_modal_open_class(last_action):
        if last_action in ("nav", "file"):
            return "fum-modal modal-open"
        return no_update
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
        Input(last_action_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_render(tree_data, selected_dir, exts, file_sel, last_action, root):
        # Resolve root and selected directory (clamped to project root)
        try:
            rabs_in = os.path.abspath((root or "").strip()) if root else None
        except Exception:
            rabs_in = None
        rabs = _clamp_to_project(rabs_in or project_root)
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

        def _build(path: str, depth: int):
            label = os.path.basename(path) or path
            node = nodes.get(path, {})
            expanded = bool(node.get("expanded"))
            is_sel = os.path.abspath(path) == s
            tree_children.append(_w_dir_row(prefix, path, label, depth, expanded, is_sel))
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
                        tree_children.append(_w_file_row(prefix, fpath, depth, (file_sel or "").strip() == fpath))

        start_root = rabs or s
        if start_root:
            if start_root not in nodes:
                nodes[start_root] = {"expanded": True, "subdirs": [], "files": []}
            _build(start_root, 0)

        cwd_label_text = f"cwd: {s}" if s and os.path.isdir(s) else "cwd: (missing)"

        # Breadcrumbs based on root and selected directory (widgetized)
        try:
            base = os.path.abspath((rabs or s) or "")
            sel = os.path.abspath(s or base)
            crumbs = _w_breadcrumbs(prefix, base, sel)
        except Exception:
            crumbs = []

        # Metadata statusbar — centralized with robust gating (only show file when it belongs to the selected dir)
        fsel = (file_sel or "").strip()
        try:
            s_abs = os.path.abspath(s) if s else ""
            fsel_abs = os.path.abspath(fsel) if fsel else ""
            fsel_dir_abs = os.path.abspath(os.path.dirname(fsel_abs)) if fsel_abs else ""
        except Exception:
            s_abs, fsel_abs, fsel_dir_abs = "", "", ""
        if (last_action == "file") and fsel_abs and os.path.isfile(fsel_abs) and (fsel_dir_abs == s_abs):
            status_text = _file_status_text(fsel_abs)
        else:
            status_text = _dir_status_text(s, exts=(exts or []), hide_dotfiles=True)
        return tree_children, cwd_label_text, crumbs, status_text

    # Tree toggle: expand/collapse one node; cache listing on expand (one directory at a time)
    @app.callback(
        Output(tree_store, "data", allow_duplicate=True),
        Output(sel_dir_store, "data", allow_duplicate=True),
        Output(file_sel_store, "data", allow_duplicate=True),
        Output(f"{prefix}-last-action", "data", allow_duplicate=True),
        Output(status_div, "children", allow_duplicate=True),
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
            return no_update, no_update, no_update, no_update
        target = (obj.get("path", "") or "").strip()
        if not target:
            return no_update, no_update, no_update, no_update

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
        # Also clear any existing file selection on folder toggle so status shows folder metadata
        return tree, p, "", "nav", _dir_status_text(p, exts=(exts or []), hide_dotfiles=True)

    # Breadcrumb click -> select directory (clamped)
    @app.callback(
        Output(sel_dir_store, "data", allow_duplicate=True),
        Output(f"{prefix}-last-action", "data", allow_duplicate=True),
        Input({"role": f"{prefix}-crumb", "path": ALL}, "n_clicks"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def on_crumb_click(_clicks, root):
        ctx = dash.callback_context
        obj = _get_ctx_obj(ctx)
        if not isinstance(obj, dict) or obj.get("role") != f"{prefix}-crumb":
            return no_update, no_update
        target = (obj.get("path", "") or "").strip()
        if not target:
            return no_update, no_update
        r = (root or "").strip()
        if r:
            return _ctl_clamp(target, r), "nav"
        return target, "nav"

    # Sync selected-dir when legacy cwd changes (Root/Up)
    @app.callback(
        Output(sel_dir_store, "data", allow_duplicate=True),
        Output(file_sel_store, "data", allow_duplicate=True),
        Output(f"{prefix}-last-action", "data", allow_duplicate=True),
        Input(cwd_store, "data"),
        State(root_store, "data"),
        prevent_initial_call=True,
    )
    def sync_selected_dir(cwd, root):
        c = (cwd or "").strip()
        r = (root or "").strip()
        if not c:
            return no_update, no_update, no_update
        c = _clamp_to_project(c)
        if r:
            r = _clamp_to_project(r)
            return _ctl_clamp(c, r), "", "nav"
        return c, "", "nav"

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
        Output(f"{prefix}-last-action", "data", allow_duplicate=True),
        Output(sel_store, "data", allow_duplicate=True),
        Output(sel_label, "children", allow_duplicate=True),
        Input({"role": f"{prefix}-file", "path": ALL}, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_explorer_click(_file_clicks):
        ctx = dash.callback_context

        # Parse triggering id; avoid strict n_clicks gating which can be None or string in some Dash versions
        obj = _get_ctx_obj(ctx)
        if not isinstance(obj, dict) or obj.get("role") != f"{prefix}-file":
            return no_update, no_update, no_update, no_update, no_update, no_update
        fpath = (obj.get("path", "") or "").strip()
        if not fpath:
            return no_update, no_update, no_update, no_update, no_update, no_update
        # Persist selection into stores so Confirm has a reliable fallback
        from os.path import basename
        bname = basename(fpath)
        # Preview selection (file_sel_store) and persist selected-path silently for Confirm fallback.
        # Do NOT update the compact strip label yet; that only updates on Confirm.
        return no_update, fpath, no_update, "file", fpath, no_update

    # Confirm selection -> set stores, hide modal, and update target value
    @app.callback(
        Output(sel_store, "data"),
        Output(sel_label, "children"),
        Output(status_div, "children", allow_duplicate=True),
        Output(mid, "style", allow_duplicate=True),
        Output(mid, "className", allow_duplicate=True),
        Output(target_id, "options", allow_duplicate=True),
        Output(target_id, "value", allow_duplicate=True),
        Input(confirm_btn, "n_clicks"),
        State(file_sel_store, "data"),
        State(sel_dir_store, "data"),
        State(target_id, "options"),
        State(sel_store, "data"),
        prevent_initial_call=True,
    )
    def on_confirm(_n, file_sel, sel_dir, options, sel_data):
        # Primary source: file selected by clicking in explorer
        fsel = (file_sel or "").strip()
        # Fallback to last persisted selection (set on click) if primary missing
        if not fsel:
            fsel = (sel_data or "").strip()
        c = (sel_dir or "").strip()
        if not fsel:
            return no_update, no_update, "Select a file.", no_update, no_update, no_update, no_update
        path = fsel if os.path.isabs(fsel) else (os.path.abspath(os.path.join(c, fsel)) if c else os.path.abspath(fsel))
        bname = os.path.basename(path)
        base_only, ext = os.path.splitext(bname)
        # Separate display widths:
        # - Compact strip renders base and extension separately so extension stays visible
        # - Dropdown options keep middle-ellipsis string
        label_option = _truncate_middle(bname, max_len=40)
        label_children = [
            html.Span(
                base_only,
                style={
                    "minWidth": 0,
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "whiteSpace": "nowrap",
                    "display": "block",
                    "flex": 1,
                },
            ),
            html.Span(ext, style={"flex": "0 0 auto"}),
        ]

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
                        # Preserve any existing label; otherwise keep as-is
                        lbl = o.get("label", v)
                        new_options.append({"label": lbl, "value": v})
            if path not in vals:
                new_options.append({"label": label_option, "value": path})
        except Exception:
            new_options = [{"label": label_option, "value": path}]

        status = f"Selected: {path}"
        style = _fp_modal_styles()  # hidden (default)
        # Remove the open-class so CSS rule no longer pins/locks the layout
        return path, label_children, status, style, "fum-modal", new_options, path