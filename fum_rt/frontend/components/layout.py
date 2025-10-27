"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

from dash import html, dcc
from fum_rt.frontend.components.widgets.file_picker import file_picker_overlay

from fum_rt.frontend.components.workspace import workspace_card
from fum_rt.frontend.components.runtime_controls import runtime_controls_card
from fum_rt.frontend.components.feed import feed_card
from fum_rt.frontend.components.config.run_config import run_config_card
from fum_rt.frontend.components.charts import charts_card
from fum_rt.frontend.components.chat import chat_card
from fum_rt.frontend.components.perf import perf_card

__all__ = ["build_layout"]


def build_layout(
    runs_root: str,
    runs: List[str],
    default_run: str,
    repo_root: str,  # kept for legacy signature; not used
    profiles_dir: str,  # kept for legacy signature; not used
    default_profile: Dict[str, Any],
    domain_options: List[Dict[str, str]],
    data_files_options: List[Dict[str, str]],
    profile_options: List[Dict[str, str]],
) -> html.Div:
    """
    Construct the full dashboard layout (no callbacks).
    Wrapper around modular cards to preserve legacy build_layout signature.
    IDs preserved to match existing callbacks in fum_live.
    """
    poll_ms_env = os.getenv("DASH_POLL_MS", "1200")
    try:
        poll_ms_val = int(poll_ms_env) if poll_ms_env.strip() != "" else 1200
    except ValueError:
        poll_ms_val = 1200
    poll_interval = max(250, poll_ms_val)
    poll_disabled = poll_ms_val <= 0

    return html.Div(
        [
            html.H3("FUM Live Dashboard (external control)"),
            html.Div(
                [
                    html.Div(
                        [
                            workspace_card(runs_root, runs, default_run),
                            runtime_controls_card(default_profile),
                            perf_card(),
                            feed_card(data_files_options),
                        ],
                        style={"minWidth": "320px", "display": "grid", "gap": "16px"},
                    ),
                    html.Div(
                        [
                            run_config_card(default_profile, domain_options, profile_options),
                            charts_card(),
                            chat_card(),
                        ],
                        style={"minWidth": "400px", "display": "grid", "gap": "16px"},
                    ),
                ],
                id="app-grid",
                className="grid",
            ),
            # Top-level portal root so modals are independent from #app-grid
            html.Div(
                [
                    file_picker_overlay("feed-file", "Select feed file"),
                    file_picker_overlay("profile-file", "Select profile JSON"),
                    file_picker_overlay("engram-file", "Select engram file"),
                ],
                id="modals-root",
            ),
            dcc.Interval(id="poll", interval=poll_interval, n_intervals=0, disabled=poll_disabled),
            dcc.Store(id="chat-state"),
            dcc.Store(id="ui-state"),
        ],
        style={
            "padding": "10px",
            "maxWidth": "1600px",
            "margin": "0 auto",
            "width": "100%",
            "minHeight": "100vh",
            "position": "relative"
        },
    )
