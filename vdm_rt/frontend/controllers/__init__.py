"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Controllers for reusable business logic extracted from Dash callbacks.
"""

from .runtime_controller import (
    build_phase_update,
    update_phase_json,
    queue_load_engram,
    parse_engram_events_for_message,
)

__all__ = [
    "build_phase_update",
    "update_phase_json",
    "queue_load_engram",
    "parse_engram_events_for_message",
]