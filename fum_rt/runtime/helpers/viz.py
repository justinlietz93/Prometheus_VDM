"""
Runtime helper: periodic visualization hooks (dashboard and connectome snapshot).

Behavior:
- Mirrors legacy Nexus logic and the original runtime_helpers.maybe_visualize()
- Fail-soft and fully optional; never disrupts runtime
"""

from __future__ import annotations

from typing import Any


def maybe_visualize(nx: Any, step: int) -> None:
    """
    Periodic dashboard and graph snapshot, behavior-preserving.
    """
    try:
        if getattr(nx, "viz_every", 0) and (int(step) % int(nx.viz_every)) == 0 and int(step) > 0:
            try:
                nx.vis.dashboard(nx.history[-max(50, int(nx.viz_every) * 2):])  # last window
                if int(getattr(nx, "N", 0)) <= 10000:
                    G = nx.connectome.snapshot_graph()
                    nx.vis.graph(G, fname='connectome.png')
            except Exception as e:
                try:
                    nx.logger.info("viz_error", extra={"extra": {"err": str(e)}})
                except Exception:
                    pass
    except Exception:
        pass


__all__ = ["maybe_visualize"]