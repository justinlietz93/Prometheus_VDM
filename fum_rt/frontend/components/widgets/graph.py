"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

from dash import dcc


def graph(id: str, height: int = 420, width: str = "100%"):
    """
    Primitive graph widget (lego block).
    Used by higher-level components to compose chart cards.
    """
    return dcc.Graph(id=id, style={"height": f"{int(height)}px", "width": width})