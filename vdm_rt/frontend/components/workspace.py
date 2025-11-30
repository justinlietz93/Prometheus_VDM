"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import os
from typing import List
from dash import html, dcc


def _runs_root_options(runs_root: str):
    """
    Build candidate runs-root dropdown options:
    - current runs_root
    - ./runs
    - ./runs.bak
    Only include those that exist (abs or relative).
    """
    cand = []
    for p in [runs_root, "runs", "runs.bak"]:
        p = (p or "").strip()
        if not p:
            continue
        # Normalize to absolute if relative exists
        abs_p = p if os.path.isabs(p) else os.path.abspath(p)
        try:
            if os.path.isdir(abs_p) and abs_p not in cand:
                cand.append(abs_p)
        except Exception:
            continue
    if not cand and runs_root:
        cand.append(runs_root)
    return [{"label": s, "value": s} for s in cand]


def workspace_card(runs_root: str, runs: List[str], default_run: str):
    """
    Workspace card with runs root controls and run selector.
    IDs preserved to match existing callbacks.

    Changes:
    - Restores a Runs Root dropdown (runs-root-select) alongside the text input.
      A small sync callback in workspace callbacks should update runs-root when the
      dropdown changes.
    """
    return html.Div(
        [
            html.H4("Workspace"),
            html.Label("Runs root (select)"),
            dcc.Dropdown(
                id="runs-root-select",
                options=_runs_root_options(runs_root),
                value=runs_root,
                placeholder="Select runs root...",
                style={"width": "100%"},
            ),
            html.Label("Runs root (edit)"),
            dcc.Input(id="runs-root", type="text", value=runs_root, style={"width": "100%"}),
            html.Div(
                [
                    html.Button("Refresh Runs", id="refresh-runs", n_clicks=0),
                    html.Button("Use Current Run", id="use-current-run", n_clicks=0),
                    html.Button("Use Latest Run", id="use-latest-run", n_clicks=0),
                ],
                className="row tight",
            ),
            html.Label("Run directory"),
            dcc.Dropdown(
                id="run-dir",
                options=[{"label": p, "value": p} for p in runs],
                value=default_run,
            ),
        ],
        className="card",
    )