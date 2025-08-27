import os
from typing import Any, List, Optional

import pytest
from dash import Dash, html, dcc

from fum_rt.frontend.components.layout import build_layout
from fum_rt.frontend.components.widgets.file_picker import file_picker_overlay
from fum_rt.frontend.components.widgets.blocks import (
    block_container,
    block_panel,
    graph_tabs_single_graph_panel,
)
from fum_rt.frontend.styles.layout import get_layout_css
from fum_rt.frontend.utilities.profiles import get_default_profile


def _flatten(children):
    if children is None:
        return []
    if isinstance(children, (list, tuple)):
        return list(children)
    return [children]


def _find_by_id(root, id_value: str):
    stack = [root]
    while stack:
        node = stack.pop()
        if getattr(node, "id", None) == id_value:
            return node
        if hasattr(node, "children"):
            stack.extend(_flatten(node.children))
    return None


def _collect_ids(root) -> set:
    ids = set()
    stack = [root]
    while stack:
        node = stack.pop()
        nid = getattr(node, "id", None)
        if nid is not None:
            ids.add(nid)
        if hasattr(node, "children"):
            stack.extend(_flatten(node.children))
    return ids


def test_layout_contains_portal_and_grid():
    layout = build_layout(
        runs_root="/tmp",
        runs=[],
        default_run="",
        repo_root="/tmp/repo",
        profiles_dir="/tmp/profiles",
        default_profile=get_default_profile(),
        domain_options=[],
        data_files_options=[],
        profile_options=[],
    )
    assert isinstance(layout, html.Div)
    app_grid = _find_by_id(layout, "app-grid")
    modals_root = _find_by_id(layout, "modals-root")
    assert app_grid is not None, "app-grid div missing"
    assert modals_root is not None, "modals-root div missing"

    # Expect known modal children
    expected = {"feed-file-modal", "profile-file-modal", "engram-file-modal"}
    modal_child_ids = set()
    for child in _flatten(modals_root.children):
        cid = getattr(child, "id", None)
        if cid:
            modal_child_ids.add(cid)
    assert expected.issubset(modal_child_ids)


def test_file_picker_overlay_fixed_and_hidden_initially():
    node = file_picker_overlay("unitfp", "Unit Test Picker")
    assert node.id == "unitfp-modal"
    assert node.className == "fum-modal"
    style = node.style or {}
    assert style.get("position") == "fixed"
    assert style.get("display") == "none"
    assert style.get("width") == "100vw"
    assert style.get("height") == "100vh"
    assert style.get("overflow") == "auto"
    assert style.get("overscrollBehavior") == "contain"
    assert "zIndex" in style and int(style["zIndex"]) >= 9999

    # Ensure panel child exists and stacks above overlay
    inner = _flatten(node.children)[0]
    panel_style = inner.style or {}
    assert int(panel_style.get("zIndex", 0)) >= int(style.get("zIndex", 0))


def test_block_panel_enforces_containment():
    body_child = html.Div("x" * 1000, style={"whiteSpace": "nowrap"})
    panel = block_panel(title="T", children=body_child)
    assert isinstance(panel, html.Div)
    style = panel.style or {}
    assert style.get("minWidth") == 0
    assert style.get("minHeight") == 0
    assert style.get("overflow") == "hidden"
    assert style.get("contain") == "layout paint"
    assert style.get("isolation") == "isolate"

    # body is second child of the panel
    body = _flatten(panel.children)[1]
    bstyle = body.style or {}
    assert bstyle.get("minWidth") == 0
    assert bstyle.get("minHeight") == 0
    assert bstyle.get("overflow") == "hidden"


def test_block_container_grid_and_isolation():
    cont = block_container([html.Div("A"), html.Div("B")], cols=2)
    st = cont.style or {}
    assert st.get("display") == "grid"
    assert "gridTemplateColumns" in st and "repeat" in st["gridTemplateColumns"]
    assert st.get("contain") == "layout paint"
    assert st.get("isolation") == "isolate"


def test_graph_tabs_single_graph_panel_structure():
    panel = graph_tabs_single_graph_panel(prefix="rt", title="Metrics", metrics=["a", "b"])
    ids = _collect_ids(panel)
    assert "rt-data" in ids  # dcc.Store
    assert "rt-tabs" in ids  # dcc.Tabs
    assert "rt-graph" in ids  # dcc.Graph


def test_layout_css_contains_modal_guard_and_grid_rules():
    css = get_layout_css()
    assert "body:has(.fum-modal.modal-open)" in css
    assert "#app-grid" in css


def test_file_picker_registrar_declares_app_grid_style_output():
    # Verify callback wiring includes app-grid.style output (preserved via dash.no_update)
    from fum_rt.frontend.callbacks.file_picker.registrars import register_file_picker_static

    app = Dash(__name__, prevent_initial_callbacks=True, suppress_callback_exceptions=True)
    register_file_picker_static(app, prefix="tfp", root="/tmp", exts=[".txt"], target_id="dummy")

    def _has_app_grid_style(cb_meta: dict) -> bool:
        outputs = cb_meta.get("outputs") or cb_meta.get("output") or cb_meta.get("outputs_list") or []
        if not isinstance(outputs, (list, tuple)):
            outputs = [outputs]
        for out in outputs:
            try:
                if isinstance(out, dict):
                    oid = out.get("id")
                    prop = out.get("property")
                    # Direct dict form
                    if oid == "app-grid" and prop == "style":
                        return True
                    # Nested dict form seen in some Dash versions
                    if isinstance(oid, dict):
                        if oid.get("id") == "app-grid" and (prop == "style" or oid.get("property") == "style"):
                            return True
                else:
                    s = str(out)
                    if "app-grid" in s and ".style" in s:
                        return True
            except Exception:
                continue
        return False

    found = any(_has_app_grid_style(cb) for cb in app.callback_map.values())

    assert found, "Expected a callback output targeting app-grid.style to preserve grid via no_update on open"