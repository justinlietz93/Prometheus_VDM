from __future__ import annotations

"""
File Picker Registrars (package-scoped)

- Static root registrar
- Dynamic (engram) root registrar

Both delegate common behavior to .common.register_file_picker_common
"""

import os
from typing import List

from dash import Output, Input, State, no_update  # type: ignore

from fum_rt.frontend.components.widgets.file_picker import _modal_styles as _fp_modal_styles
from fum_rt.frontend.controllers.file_picker_controller import init_tree as _ctl_init_tree
from .common import register_file_picker_common


def _project_root_default() -> str:
    """
    Resolve a safe project root for clamping.
    Prefers FUM_PROJECT_ROOT; falls back to repository root by relative path.
    """
    try:
        env = os.path.abspath((os.getenv("FUM_PROJECT_ROOT") or "").strip())
        if env and os.path.isdir(env):
            return env
    except Exception:
        pass
    # callbacks/file_picker/ -> callbacks/ -> frontend/ -> .. (repo root)
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def register_file_picker_static(app, prefix: str, root: str, exts: List[str] | None, target_id: str) -> None:
    """
    Register a file-picker with a fixed root (bounded IO).
    """
    project_root = _project_root_default()

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
        Output(f"{prefix}-file-sel", "data", allow_duplicate=True),
        Output(f"{prefix}-last-action", "data", allow_duplicate=True),
        Output("app-grid", "style", allow_duplicate=True),
        Input(open_btn, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_open(_n):
        r0 = os.path.abspath(root or "")
        r = r0 if os.path.isdir(r0) else project_root
        style = _fp_modal_styles()
        style["display"] = "flex"
        # Do not mutate grid inline; CSS handles pinning via :has() and #app-grid rules.
        return style, r, r, list(exts or []), "", "nav", no_update

    # Initialize tree and selection on open (static)
    @app.callback(
        Output(f"{prefix}-selected-dir", "data", allow_duplicate=True),
        Output(f"{prefix}-tree-store", "data", allow_duplicate=True),
        Output(status_div, "children", allow_duplicate=True),
        Input(open_btn, "n_clicks"),
        prevent_initial_call=True,
    )
    def on_open_init(_n):
        r0 = os.path.abspath(root or "")
        r = r0 if os.path.isdir(r0) else project_root
        tree = _ctl_init_tree(r, exts=(exts or []), hide_dotfiles=True)
        try:
            files0 = (tree.get("nodes", {}).get(r, {}) or {}).get("files") or []
            status_text = f"root: {r}  files: {len(files0)}"
        except Exception:
            status_text = f"root: {r}  files: 0"
        return r, tree, status_text

    register_file_picker_common(app, prefix, target_id, project_root)


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
    project_root = _project_root_default()

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
        Output(f"{prefix}-file-sel", "data", allow_duplicate=True),
        Output(f"{prefix}-last-action", "data", allow_duplicate=True),
        Output("app-grid", "style", allow_duplicate=True),
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
            r_candidate = os.path.abspath(cand)
            if os.path.isdir(r_candidate):
                r = r_candidate
                style = _fp_modal_styles()
                style["display"] = "flex"
                return style, r, r, list(exts or []), "", "nav", no_update
        # fallback: open at project root
        style = _fp_modal_styles()
        style["display"] = "flex"
        return style, project_root, project_root, list(exts or []), "", "nav", no_update

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
            r = os.path.abspath(cand)
            if os.path.isdir(r):
                tree = _ctl_init_tree(r, exts=(exts or []), hide_dotfiles=True)
                try:
                    files0 = (tree.get("nodes", {}).get(r, {}) or {}).get("files") or []
                    status_text = f"root: {r}  files: {len(files0)}"
                except Exception:
                    status_text = f"root: {r}  files: 0"
                return r, tree, status_text
        r = project_root
        tree = _ctl_init_tree(r, exts=(exts or []), hide_dotfiles=True)
        try:
            files0 = (tree.get("nodes", {}).get(r, {}) or {}).get("files") or []
            status_text = f"root: {r}  files: {len(files0)}"
        except Exception:
            status_text = f"root: {r}  files: 0"
        return r, tree, status_text

    register_file_picker_common(app, prefix, target_id, project_root)