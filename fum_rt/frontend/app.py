"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""

from __future__ import annotations

import os
import dash
from typing import List, Dict, Any

from dash import Dash, dcc, html

from fum_rt.frontend.utilities.fs_utils import list_runs, _list_files
from fum_rt.frontend.services.process_manager import ProcessManager
from fum_rt.frontend.utilities.profiles import get_default_profile
from fum_rt.frontend.styles import get_global_css

from fum_rt.frontend.components.workspace import workspace_card
from fum_rt.frontend.components.runtime_controls import runtime_controls_card
from fum_rt.frontend.components.feed import feed_card
from fum_rt.frontend.components.run_config import run_config_card
from fum_rt.frontend.components.charts import charts_card
from fum_rt.frontend.components.chat import chat_card
from fum_rt.frontend.components.perf import perf_card

from fum_rt.frontend.callbacks.workspace import register_workspace_callbacks
from fum_rt.frontend.callbacks.charts import register_chart_callbacks
from fum_rt.frontend.callbacks.runtime import register_runtime_callbacks
from fum_rt.frontend.callbacks.process import register_process_callbacks
from fum_rt.frontend.callbacks.feed import register_feed_callbacks
from fum_rt.frontend.callbacks.profile import register_profile_callbacks
from fum_rt.frontend.callbacks.logs import register_logs_callbacks
from fum_rt.frontend.callbacks.chat import register_chat_callbacks
from fum_rt.frontend.callbacks.engram import register_engram_callbacks
from fum_rt.frontend.callbacks.perf import register_perf_callbacks
from fum_rt.frontend.callbacks.interval import register_interval_callbacks
from fum_rt.frontend.callbacks.file_picker.registrars import (
    register_file_picker_static,
    register_file_picker_engram,
)


def build_app(runs_root: str) -> Dash:
    """
    Factory for the FUVDM Live Dashboard Dash app.
    - Assembles layout (cards/components)
    - Installs modular callbacks
    - Keeps ProcessManager scoped to the app instance
    """
    # UI throttling and safe startup:
    # - prevent_initial_callbacks avoids callback storms at load
    # - suppress_callback_exceptions allows lazy mounting of tabs/sections
    app = Dash(
        __name__,
        prevent_initial_callbacks=True,
        suppress_callback_exceptions=True,
    )
    app.title = "FUM Live Dashboard"

    # Global theme
    GLOBAL_CSS = get_global_css()
    app.index_string = app.index_string.replace("</head>", f"<style>{GLOBAL_CSS}</style></head>")

    # Workspace context
    runs = list_runs(runs_root)
    default_run = runs[0] if runs else ""

    # Paths (compute repository root from this file so structure works regardless of CWD)
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    PROFILES_DIR = os.path.join(repo_root, "run_profiles")
    os.makedirs(PROFILES_DIR, exist_ok=True)

    # Services
    manager = ProcessManager(runs_root)
    default_profile = get_default_profile()

    # Profile discovery for initial options
    def list_profiles() -> List[str]:
        try:
            return sorted([os.path.join(PROFILES_DIR, f) for f in os.listdir(PROFILES_DIR) if f.endswith(".json")])
        except Exception:
            return []

    # Static dropdowns
    domain_options = [
        {"label": n, "value": n}
        for n in [
            "math_physics",
            "quantum",
            "standard_model",
            "dark_matter",
            "biology_consciousness",
            "cosmogenesis",
            "higgs",
        ]
    ]
    profile_options = [{"label": os.path.basename(p), "value": p} for p in list_profiles()]
    # Data feed files — bound and non-recursive to avoid heavy startup scans
    try:
        DATA_SCAN_MAX = int(os.getenv("DASH_DATA_SCAN_MAX", "300"))
    except Exception:
        DATA_SCAN_MAX = 300
    DATA_EXTS = [".txt", ".jsonl", ".json", ".csv", ".pdf"]
    data_dir = os.path.join(repo_root, "fum_rt", "data")
    os.makedirs(data_dir, exist_ok=True)
    paths = _list_files(data_dir, exts=DATA_EXTS, recursive=False)[: max(0, DATA_SCAN_MAX)]
    data_files_options = [{"label": p, "value": p} for p in paths]

    # Layout
    app.layout = html.Div(
        [
            html.H3("FUVDM Live Dashboard (experimental control)"),
            html.Div(
                [
                    # Left panel
                    html.Div(
                        [
                            workspace_card(runs_root, runs, default_run),
                            runtime_controls_card(default_profile),
                            perf_card(),
                            feed_card(data_files_options),
                        ],
                        style={"minWidth": "320px", "display": "grid", "gap": "16px"},
                    ),
                    # Right panel
                    html.Div(
                        [
                            run_config_card(default_profile, domain_options, profile_options),
                            charts_card(),
                            chat_card(),
                        ],
                        style={"minWidth": "400px", "display": "grid", "gap": "16px"},
                    ),
                ],
                className="grid",
            ),
            # Global UI poll — environment-tunable and disable-able
            # DASH_POLL_MS: >0 interval in ms (default 1200); <=0 disables polling
            dcc.Interval(
                id="poll",
                interval=max(250, int(os.getenv("DASH_POLL_MS", "1200")) if os.getenv("DASH_POLL_MS", "").strip() != "" else 1200),
                n_intervals=0,
                disabled=(int(os.getenv("DASH_POLL_MS", "1200")) if os.getenv("DASH_POLL_MS", "").strip() != "" else 1200) <= 0,
            ),
            dcc.Store(id="chat-state"),
            dcc.Store(id="ui-state"),
        ],
        style={"padding": "10px"},
    )

    # Callbacks (modular)
    # Diagnostic: print Dash/version and callback registration progress
    try:
        print(f"[dash] version={dash.__version__}")
    except Exception:
        pass

    register_workspace_callbacks(app, runs_root, manager)
    print(f"[callbacks] workspace registered; total={len(getattr(app, 'callback_map', {}))}")
    register_chart_callbacks(app)
    print(f"[callbacks] charts registered; total={len(getattr(app, 'callback_map', {}))}")
    register_runtime_callbacks(app, default_profile)
    print(f"[callbacks] runtime registered; total={len(getattr(app, 'callback_map', {}))}")
    register_feed_callbacks(app, manager, repo_root)
    print(f"[callbacks] feed registered; total={len(getattr(app, 'callback_map', {}))}")
    register_process_callbacks(app, runs_root, manager, default_profile)
    print(f"[callbacks] process registered; total={len(getattr(app, 'callback_map', {}))}")
    register_profile_callbacks(app, PROFILES_DIR, default_profile)
    print(f"[callbacks] profile registered; total={len(getattr(app, 'callback_map', {}))}")
    register_logs_callbacks(app, manager)
    print(f"[callbacks] logs registered; total={len(getattr(app, 'callback_map', {}))}")
    register_chat_callbacks(app)
    print(f"[callbacks] chat registered; total={len(getattr(app, 'callback_map', {}))}")
    register_engram_callbacks(app)
    print(f"[callbacks] engram registered; total={len(getattr(app, 'callback_map', {}))}")
    register_perf_callbacks(app)
    print(f"[callbacks] perf registered; total={len(getattr(app, 'callback_map', {}))}")
    register_interval_callbacks(app)
    print(f"[callbacks] interval registered; total={len(getattr(app, 'callback_map', {}))}")

    # File Picker integrations (bounded IO, no recursive scans):
    register_file_picker_static(app, prefix="feed-file", root=data_dir, exts=DATA_EXTS, target_id="feed-path")
    print(f"[callbacks] filepicker feed registered; total={len(getattr(app, 'callback_map', {}))}")
    register_file_picker_static(app, prefix="profile-file", root=PROFILES_DIR, exts=[".json"], target_id="profile-path")
    print(f"[callbacks] filepicker profile registered; total={len(getattr(app, 'callback_map', {}))}")
    register_file_picker_engram(app, prefix="engram-file", exts=[".h5", ".npz"], target_id="rc-load-engram-path", fallback_root=runs_root)
    print(f"[callbacks] filepicker engram registered; total={len(getattr(app, 'callback_map', {}))}")

    print(f"[callbacks] registration complete; total={len(getattr(app, 'callback_map', {}))}")
    return app