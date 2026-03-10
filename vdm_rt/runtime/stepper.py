from __future__ import annotations

from math import sqrt
from typing import Any, Dict, Tuple

from vdm_rt.core.metrics import compute_metrics
from vdm_rt.core.signals import compute_active_edge_density


def _mean(vals):
    n = len(vals)
    return (sum(vals) / n) if n else 0.0


def _var(vals, mu=None):
    n = len(vals)
    if n == 0:
        return 0.0
    m = _mean(vals) if mu is None else mu
    return sum((x - m) * (x - m) for x in vals) / n


def compute_step_and_metrics(nx: Any, step: int) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    m: Dict[str, Any] = {}

    try:
        nx.connectome.step(tick=step)
    except Exception:
        pass

    C = nx.connectome
    m["H"] = float(getattr(C, "_reward_H", 0.0))
    m["dH_dt"] = float(getattr(C, "_reward_dH_dt", 0.0))
    m["S"] = float(getattr(C, "_reward_S", 0.0))
    m["dS_dt"] = float(getattr(C, "_reward_dS_dt", 0.0))
    m["fisher_speed"] = float(getattr(C, "_reward_fisher_speed", 0.0))
    m["boundary_flux"] = float(getattr(C, "_reward_boundary_flux", 0.0))

    phi_curr = [float(x) for x in C.phi_curr.tolist()]
    phi_prev = [float(x) for x in C.phi_prev.tolist()]
    phi_dot = [a - b for a, b in zip(phi_curr, phi_prev)]

    dot_mu = _mean(phi_dot)
    dot_var = _var(phi_dot, dot_mu)
    m["phi_dot_rms"] = float(sqrt(max(0.0, _mean([x * x for x in phi_dot]))))
    m["phi_dot_var"] = float(dot_var)
    m["phi_mean"] = float(_mean(phi_curr))
    m["phi_var"] = float(_var(phi_curr, m["phi_mean"]))

    eta_bond = float(sqrt(2.0 * C.eps_topo * C.kT))
    active_edges = 0
    psi_sum = 0.0
    psi_sq_sum = 0.0
    psi_count = 0
    for i in range(C.N):
        psi = C.psi_curr[i]
        if psi.size:
            for x in psi.tolist():
                fx = float(x)
                if fx > eta_bond:
                    active_edges += 1
                psi_sum += fx
                psi_sq_sum += fx * fx
                psi_count += 1
    m["active_edges"] = int(active_edges)
    m["psi_mean"] = float(psi_sum / max(1, psi_count))
    m["psi_rms"] = float(sqrt(psi_sq_sum / max(1, psi_count)))

    # keep core seam in use for boundary guards
    try:
        E, density = compute_active_edge_density(C, int(getattr(nx, "N", C.N)))
        m["active_edge_density"] = float(density)
        m["active_edges_signal"] = int(E)
    except Exception:
        pass

    try:
        base = compute_metrics(C)
        m["connectome_entropy"] = float(base.get("connectome_entropy", 0.0))
    except Exception:
        pass

    try:
        findings = getattr(C, "findings", None)
        if findings:
            m.update(findings)
    except Exception:
        pass

    m["valence_01"] = float(getattr(C, "_last_sie2_valence", 0.0))
    drive = {"valence_01": m["valence_01"]}
    return m, drive


__all__ = ["compute_step_and_metrics"]
