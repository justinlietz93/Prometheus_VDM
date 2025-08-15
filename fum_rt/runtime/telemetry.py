from __future__ import annotations

"""
Runtime telemetry packaging seam (Phase B).

Goals:
- Provide small, behavior-preserving builders for 'why' and 'status' payloads.
- Keep core numeric only; this module formats dicts but performs no logging or IO.
- Mirror existing Nexus packaging exactly to ensure byte-for-byte parity.

Policy:
- May import typing and stdlib only.
- No imports from io.* emitters; no file or JSON writes here.
"""

from typing import Any, Dict


def macro_why_base(nx: Any, metrics: Dict[str, Any], step: int) -> Dict[str, Any]:
    """
    Build the base 'why' dict used for macro emissions (before any caller-specific fields).
    Mirrors the inline block in Nexus: uses current metrics with explicit numeric casts.

    Caller may extend with additional telemetry fields, e.g. novelty_idf, composer_idf_k.
    """
    m = metrics or {}
    try:
        phase = int(getattr(nx, "_phase", {}).get("phase", 0))
    except Exception:
        try:
            phase = int(m.get("phase", 0))
        except Exception:
            phase = 0

    return {
        "t": int(step),
        "phase": phase,
        "b1_z": float(m.get("b1_z", 0.0)),
        "cohesion_components": int(m.get("cohesion_components", 0)),
        "vt_coverage": float(m.get("vt_coverage", 0.0)),
        "vt_entropy": float(m.get("vt_entropy", 0.0)),
        "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
        "sie_valence_01": float(m.get("sie_valence_01", 0.0)),
        "sie_v2_valence_01": float(m.get("sie_v2_valence_01", m.get("sie_valence_01", 0.0))),
    }


def status_payload(nx: Any, metrics: Dict[str, Any], step: int) -> Dict[str, Any]:
    """
    Build the open UTD status payload.
    Mirrors the inline block from Nexus with identical keys and casts.
    """
    m = metrics or {}
    try:
        phase = int(m.get("phase", int(getattr(nx, "_phase", {}).get("phase", 0))))
    except Exception:
        phase = 0

    return {
        "type": "status",
        "t": int(step),
        "neurons": int(getattr(nx, "N", 0)),
        "phase": phase,
        "cohesion_components": int(m.get("cohesion_components", 0)),
        "vt_coverage": float(m.get("vt_coverage", 0.0)),
        "vt_entropy": float(m.get("vt_entropy", 0.0)),
        "connectome_entropy": float(m.get("connectome_entropy", 0.0)),
        "active_edges": int(m.get("active_edges", 0)),
        "homeostasis_pruned": int(m.get("homeostasis_pruned", 0)),
        "homeostasis_bridged": int(m.get("homeostasis_bridged", 0)),
        "b1_z": float(m.get("b1_z", 0.0)),
        "adc_territories": int(m.get("adc_territories", 0)),
        "adc_boundaries": int(m.get("adc_boundaries", 0)),
        "sie_total_reward": float(m.get("sie_total_reward", 0.0)),
        "sie_valence_01": float(m.get("sie_valence_01", 0.0)),
        "sie_v2_reward_mean": float(m.get("sie_v2_reward_mean", 0.0)),
        "sie_v2_valence_01": float(m.get("sie_v2_valence_01", 0.0)),
        "ute_in_count": int(m.get("ute_in_count", 0)),
        "ute_text_count": int(m.get("ute_text_count", 0)),
    }


__all__ = ["macro_why_base", "status_payload"]