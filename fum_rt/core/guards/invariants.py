from __future__ import annotations

"""
fum_rt.core.guards.invariants

Physics ↔ code guard helpers (CI/runtime-safe, no IO, no scans).

Purpose
- Provide minimal, deterministic checks that connect implementation to physics notes.
- Intended for CI tests and optional runtime warnings (callers decide policy).

Included
- check_site_constant_of_motion: sample-based drift check of a simple constant-of-motion proxy Q_FUM.
- compute_memory_groups: expose dimensionless memory steering groups from MemoryField.

Notes
- Q_FUM here uses a conservative, implementation-agnostic proxy over the on-site state vector W:
    Q_i = 0.5 * W_i^2 + α * W_i + β
  The exact analytical form depends on the chosen on-site law; callers can tune (alpha, beta) and tolerances.
- Sampling is caller-controlled and bounded; no global scans required.

Void-faithful
- Pure numeric helpers; no external imports beyond typing/math/statistics.
- O(#samples) time; callers pass bounded samples (e.g., 256–2048 indices).
"""

from typing import Dict, Iterable, Optional, Sequence, Tuple
import math


def _percentile(xs: Sequence[float], p: float) -> float:
    if not xs:
        return 0.0
    if p <= 0.0:
        return float(min(xs))
    if p >= 1.0:
        return float(max(xs))
    xs_sorted = sorted(float(v) for v in xs)
    i = int(math.floor(p * (len(xs_sorted) - 1)))
    return float(xs_sorted[max(0, min(len(xs_sorted) - 1, i))])


def check_site_constant_of_motion(
    W_prev: Sequence[float],
    W_curr: Sequence[float],
    *,
    alpha: float = 0.0,
    beta: float = 0.0,
    dt: float = 1.0,
    samples: Optional[Iterable[int]] = None,
    tol_abs: float = 1e-6,
    tol_p99: float = 1e-5,
) -> Dict[str, float | int | bool]:
    """
    Sample-based constant-of-motion proxy drift check.

    Definitions (per-site):
      Q_prev = 0.5 * W_prev^2 + alpha * W_prev + beta
      Q_curr = 0.5 * W_curr^2 + alpha * W_curr + beta
      dQ = (Q_curr - Q_prev)

    Returns dict with:
      {
        "count": int,          # number of sampled sites evaluated
        "dQ_mean": float,
        "dQ_p95": float,
        "dQ_p99": float,
        "dQ_max": float,
        "pass_abs": bool,      # max |dQ| <= tol_abs
        "pass_p99": bool,      # p99 |dQ| <= tol_p99
      }

    Notes
    - This is a conservative drift check. Tighten tolerances as your on-site ODE is finalized.
    - dt is accepted for API symmetry; current proxy is discrete in time and uses raw differences.
    """
    try:
        n_prev = len(W_prev)
        n_curr = len(W_curr)
    except Exception:
        return {"count": 0, "dQ_mean": 0.0, "dQ_p95": 0.0, "dQ_p99": 0.0, "dQ_max": 0.0, "pass_abs": False, "pass_p99": False}
    if n_prev <= 0 or n_prev != n_curr:
        return {"count": 0, "dQ_mean": 0.0, "dQ_p95": 0.0, "dQ_p99": 0.0, "dQ_max": 0.0, "pass_abs": False, "pass_p99": False}

    idxs: Iterable[int]
    if samples is None:
        # bounded default: first min(1024, N)
        k = min(1024, n_prev)
        idxs = range(k)
    else:
        idxs = samples

    dqs_abs: list[float] = []
    s = 0.0
    c = 0
    for i in idxs:
        try:
            ii = int(i)
            if ii < 0 or ii >= n_prev:
                continue
            wp = float(W_prev[ii])
            wc = float(W_curr[ii])
            q_prev = 0.5 * wp * wp + alpha * wp + beta
            q_curr = 0.5 * wc * wc + alpha * wc + beta
            dq = q_curr - q_prev
            dqs_abs.append(abs(float(dq)))
            s += float(dq)
            c += 1
        except Exception:
            continue

    if c <= 0:
        return {"count": 0, "dQ_mean": 0.0, "dQ_p95": 0.0, "dQ_p99": 0.0, "dQ_max": 0.0, "pass_abs": False, "pass_p99": False}

    dQ_mean = float(s) / float(c)
    dQ_p95 = _percentile(dqs_abs, 0.95)
    dQ_p99 = _percentile(dqs_abs, 0.99)
    dQ_max = float(max(dqs_abs)) if dqs_abs else 0.0

    return {
        "count": int(c),
        "dQ_mean": float(dQ_mean),
        "dQ_p95": float(dQ_p95),
        "dQ_p99": float(dQ_p99),
        "dQ_max": float(dQ_max),
        "pass_abs": bool(dQ_max <= float(tol_abs)),
        "pass_p99": bool(dQ_p99 <= float(tol_p99)),
    }


def compute_memory_groups(field: object) -> Dict[str, float]:
    """
    Read dimensionless memory steering groups from MemoryField (if present).

    Expected MemoryField properties (read-only):
      - Theta   (steering coefficient placeholder; walkers use it when applicable)
      - D_a     (write gain, γ in dimensionless units)
      - Lambda  (decay, δ)
      - Gamma   (one-edge smoothing, κ)

    Returns dict: {"mem_Theta":..., "mem_Da":..., "mem_Lambda":..., "mem_Gamma":...}
    Missing properties default to 0.0.
    """
    def _get(obj: object, name: str) -> float:
        try:
            return float(getattr(obj, name, 0.0))
        except Exception:
            return 0.0

    return {
        "mem_Theta": _get(field, "Theta"),
        "mem_Da": _get(field, "D_a") if hasattr(field, "D_a") else _get(field, "Da"),
        "mem_Lambda": _get(field, "Lambda"),
        "mem_Gamma": _get(field, "Gamma"),
    }


__all__ = ["check_site_constant_of_motion", "compute_memory_groups"]