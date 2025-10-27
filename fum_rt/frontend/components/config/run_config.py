"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
Run Config components (relocated to components/config).

All element IDs are preserved to avoid breaking existing callbacks.

Exports:
- run_config_card(): assembled card
- section_* helpers from .sections for fine-grained composition

Author: Justin K. Lietz
"""

from typing import Dict, Any, List
from dash import html

from .sections import (
    section_core_params,
    section_modes,
    section_structure_traversal,
    section_stimulus,
    section_speak_b1,
    section_viz_logs_checkpoints,
    section_profile_io,
    section_process_actions,
)


def run_config_card(
    default_profile: Dict[str, Any],
    domain_options: List[Dict[str, str]],
    profile_options: List[Dict[str, str]],
):
    """
    Run configuration & process card (modular assembly).
    All element IDs preserved to match existing callbacks.
    """
    return html.Div(
        [
            html.H4("Run configuration & process"),
            section_core_params(default_profile, domain_options),
            section_modes(default_profile),
            section_structure_traversal(default_profile),
            section_stimulus(default_profile),
            section_speak_b1(default_profile),
            section_viz_logs_checkpoints(default_profile),
            section_profile_io(profile_options),
            section_process_actions(),
        ],
        className="card",
    )


__all__ = [
    "run_config_card",
    "section_core_params",
    "section_modes",
    "section_structure_traversal",
    "section_stimulus",
    "section_speak_b1",
    "section_viz_logs_checkpoints",
    "section_profile_io",
    "section_process_actions",
]