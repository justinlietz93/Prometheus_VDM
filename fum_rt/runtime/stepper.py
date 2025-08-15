from __future__ import annotations

"""
Runtime stepper: compute one tick worth of core signals and advance the connectome.

Behavior:
- Mirrors Nexus inline logic exactly (move-only extraction).
- No logging or IO here. Pure computation + state updates on the nx object.
"""

from typing import Any, Dict, Tuple

from fum_rt.core.metrics import compute_metrics
from fum_rt.core.signals import (
    compute_active_edge_density as _comp_density,
    compute_td_signal as _comp_td,
    compute_firing_var as _comp_fvar,
)


def compute_step_and_metrics(nx: Any, t: float, step: int, idf_scale: float = 1.0) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Compute density/TD/firing_var, derive SIE drive, step connectome, and build metrics.

    Returns (metrics_dict, sie_drive_dict) where sie_drive_dict matches Nexus.sie.get_drive(..) result.
    """
    m: Dict[str, Any] = {}
    drive: Dict[str, Any] = {}

    # 1) density from active edges
    try:
        E, density = _comp_density(getattr(nx, "connectome", None), int(getattr(nx, "N", 0)))
    except Exception:
        E, density = 0, 0.0

    # 2) TD-like signal from topology change + VT entropy delta
    try:
        prev_E = getattr(nx, "_prev_active_edges", E)
        vte_prev = getattr(nx, "_prev_vt_entropy", None)
        vte_last = getattr(nx, "_last_vt_entropy", None)
        td_signal = _comp_td(prev_E, E, vte_prev, vte_last)
        nx._prev_active_edges = E
    except Exception:
        td_signal = 0.0

    # 3) firing variability (HSI proxy)
    try:
        firing_var = _comp_fvar(getattr(nx, "connectome", None))
    except Exception:
        firing_var = None

    # 4) SIE drive
    try:
        drive = nx.sie.get_drive(
            W=None,
            external_signal=float(td_signal),
            time_step=int(step),
            firing_var=firing_var,
            target_var=0.15,
            density_override=density,
            novelty_idf_scale=float(idf_scale),
        )
        sie_drive = float(drive.get("valence_01", 1.0))
    except Exception:
        drive = {"valence_01": 1.0}
        sie_drive = 1.0

    # Prefer SIE v2 when available
    try:
        sie2 = float(getattr(getattr(nx, "connectome", None), "_last_sie2_valence", 0.0))
    except Exception:
        sie2 = 0.0
    sie_gate = max(0.0, min(1.0, max(sie_drive, sie2)))

    # 5) advance connectome
    try:
        nx.connectome.step(
            t,
            domain_modulation=float(getattr(nx, "dom_mod", 1.0)),
            sie_drive=sie_gate,
            use_time_dynamics=bool(getattr(nx, "use_time_dynamics", True)),
        )
    except Exception:
        pass

    # 6) metrics (scan-based, parity-preserving)
    try:
        m = compute_metrics(nx.connectome)
    except Exception:
        m = {}

    # Attach structural homeostasis and TD diagnostics
    try:
        m["homeostasis_pruned"] = int(getattr(nx.connectome, "_last_pruned_count", 0))
        m["homeostasis_bridged"] = int(getattr(nx.connectome, "_last_bridged_count", 0))
        m["active_edges"] = int(E)
        m["td_signal"] = float(td_signal)
        m["novelty_idf_scale"] = float(idf_scale)
        if firing_var is not None:
            m["firing_var"] = float(firing_var)
    except Exception:
        pass

    # Attach traversal findings
    try:
        findings = getattr(nx.connectome, "findings", None)
        if findings:
            m.update(findings)
    except Exception:
        pass

    # Expose sie_gate
    try:
        m["sie_gate"] = float(sie_gate)
    except Exception:
        pass

    # Update VT entropy history for next tick's TD proxy
    try:
        nx._prev_vt_entropy = getattr(nx, "_last_vt_entropy", None)
        nx._last_vt_entropy = float(m.get("vt_entropy", 0.0))
    except Exception:
        pass

    return m, drive


__all__ = ["compute_step_and_metrics"]