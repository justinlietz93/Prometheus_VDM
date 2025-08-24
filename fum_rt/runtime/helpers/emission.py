"""
Runtime helper: status emission and macro board status.

- Emits open UTD status payload every status_every ticks.
- Emits a 'status' macro when valence is high (mirrors legacy behavior).

Imports typing + telemetry builder only; no IO side effects besides UTD emits.
"""

from __future__ import annotations

from typing import Any, Dict

from fum_rt.runtime.telemetry import status_payload as _telemetry_status


def emit_status_and_macro(nx: Any, m: Dict[str, Any], step: int) -> None:
    """
    Emit open UTD status payload and, when valence is high, a 'status' macro.
    Mirrors the inline Nexus logic.
    """
    if (int(step) % int(getattr(nx, "status_every", 1))) != 0:
        return

    # Open UTD status
    try:
        payload = _telemetry_status(nx, m, int(step))
        score = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
        nx.utd.emit_text(payload, score=score)
    except Exception:
        pass

    # Macro board status
    try:
        val = float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0)))
        if val >= 0.6:
            nx.utd.emit_macro(
                "status",
                {
                    "t": int(step),
                    "neurons": int(getattr(nx, "N", 0)),
                    "cohesion_components": int(m.get("cohesion_components", 0)),
                    "vt_coverage": float(m.get("vt_coverage", 0.0)),
                    "vt_entropy": float(m.get("vt_entropy", 0.0)),
                    "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
                    "active_edges": int(m.get("active_edges", 0)),
                    "homeostasis_pruned": int(m.get("homeostasis_pruned", 0)),
                    "homeostasis_bridged": int(m.get("homeostasis_bridged", 0)),
                    "ute_in_count": int(m.get("ute_in_count", 0)),
                    "ute_text_count": int(m.get("ute_text_count", 0)),
                },
                score=val,
            )
    except Exception:
        pass


__all__ = ["emit_status_and_macro"]