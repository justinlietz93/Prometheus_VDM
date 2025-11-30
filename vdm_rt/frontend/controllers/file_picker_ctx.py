"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
File Picker Dash Context Helpers

Atomic helper(s) to robustly parse Dash callback_context for pattern-matched components.
"""

from typing import Optional, Dict, Any


def get_trigger_id_obj(ctx) -> Optional[Dict[str, Any]]:
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
        import json  # local import to keep dependency surface minimal
        if getattr(ctx, "triggered", None):
            tid_s = ctx.triggered[0]["prop_id"].rsplit(".", 1)[0]
            return json.loads(tid_s)
    except Exception:
        return None
    return None