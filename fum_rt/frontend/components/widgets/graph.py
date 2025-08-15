from __future__ import annotations

from dash import dcc


def graph(id: str, height: int = 420, width: str = "100%"):
    """
    Primitive graph widget (lego block).
    Used by higher-level components to compose chart cards.
    """
    return dcc.Graph(id=id, style={"height": f"{int(height)}px", "width": width})