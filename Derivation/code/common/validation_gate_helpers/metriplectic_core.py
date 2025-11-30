#!/usr/bin/env python3
"""
Metriplectic validation gates (KG J-only, Lyapunov, degeneracy).

This module provides **pure**, side-effect-free helpers that evaluate the
metriplectic KPIs / gates used by:

- `T2_Metriplectic_Instruments_v1` runner
  [`T2_Metriplectic_Instruments_v1.py`](../../physics/metriplectic/T2_Metriplectic_Instruments_v1.py)

Scope in this first pass:

- KG J-only locality cone **speed gate**:
  - Inputs: measured cone speed `v`, reference `c`, tolerance `eps`,
    regression quality `R2`, minimum acceptable `R2_min`.
  - Output: `(passed, metrics)` where `metrics` echoes all scalars needed
    for JSON receipts and further analysis.

Notes:

- Thresholds (`eps`, `R2_min`, etc.) are **not** hard-coded canon here;
  callers must pass the thresholds taken from the relevant spec /
  schema / VALIDATION_METRICS entry. This keeps canonical numbers
  anchored in the registries, not in code.
- No plotting or file I/O lives here; runners are responsible for
  artifact routing via `Derivation/code/common/io_paths.py`.

See also:

- Canon KPIs/gates registry:
  `Derivation/z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md`
- Equations registry (KG branch, cone structure):
  `Derivation/z.CANONICAL_Equations/00_EQUATIONS.md`
"""

from __future__ import annotations

from typing import Dict, Tuple


def gate_kg_cone_speed(
    *,
    v: float,
    c: float,
    eps: float,
    R2: float,
    R2_min: float,
) -> Tuple[bool, Dict[str, float]]:
    """
    Gate helper for the KG J-only locality cone speed instrument.

    This evaluates the joint gate:

      - speed constraint:   v <= c (1 + eps)
      - fit quality:        R2 >= R2_min

    where:
      - v      : measured cone-front speed from R(t) fit (units of c)
      - c      : reference branch speed (from KG parameters)
      - eps    : allowed fractional slack on c (e.g. 0.02)
      - R2     : coefficient of determination of the R(t) fit
      - R2_min : minimum acceptable R^2 (e.g. 0.999)

    Returns
    -------
    passed : bool
        True iff both the speed and R^2 constraints are satisfied.
    metrics : dict
        Dictionary suitable for JSON receipts, containing:

        - "v"         : measured speed
        - "c"         : reference speed
        - "eps"       : fractional slack
        - "speed_max" : c (1 + eps)
        - "slack"     : speed_max - v
        - "R2"        : fit coefficient of determination
        - "R2_min"    : minimum required R^2
        - "passed"    : same as the returned `passed` flag

    Implementation details
    ----------------------
    - This helper is intentionally minimal and does **not** know anything
      about how v and R2 were computed (discrete KG scheme, grid, etc.).
      It only applies the canonical inequality checks.
    - All inputs are treated as Python floats; callers are responsible
      for ensuring IEEE-754 double precision at the runtime level.
    """
    speed_max = c * (1.0 + eps)
    slack = speed_max - v

    passed_speed = bool(v <= speed_max)
    passed_R2 = bool(R2 >= R2_min)
    passed = bool(passed_speed and passed_R2)

    metrics: Dict[str, float] = {
        "v": float(v),
        "c": float(c),
        "eps": float(eps),
        "speed_max": float(speed_max),
        "slack": float(slack),
        "R2": float(R2),
        "R2_min": float(R2_min),
        "passed": bool(passed),
    }
    return passed, metrics


def gate_kg_energy_osc_scaling(
    *,
    p: float,
    p_min: float,
    p_max: float,
    R2: float,
    R2_min: float,
    rel_AH_min_dt: float,
    rel_AH_max: float,
) -> Tuple[bool, Dict[str, float]]:
    """Gate helper for the KG J-only energy oscillation scaling meter.

    Conditions
    ----------
    - p_min <= p <= p_max
    - R2 >= R2_min
    - rel_AH_min_dt <= rel_AH_max
    """
    passed_p = bool(p_min <= p <= p_max)
    passed_R2 = bool(R2 >= R2_min)
    passed_rel = bool(rel_AH_min_dt <= rel_AH_max)
    passed = bool(passed_p and passed_R2 and passed_rel)

    metrics: Dict[str, float] = {
        "p": float(p),
        "p_min": float(p_min),
        "p_max": float(p_max),
        "R2": float(R2),
        "R2_min": float(R2_min),
        "rel_AH_min_dt": float(rel_AH_min_dt),
        "rel_AH_max": float(rel_AH_max),
        "passed_p": bool(passed_p),
        "passed_R2": bool(passed_R2),
        "passed_rel_AH": bool(passed_rel),
        "passed": bool(passed),
    }
    return passed, metrics


def gate_metriplectic_lyapunov(
    *,
    delta_Lh_max: float,
    delta_Lh_max_allowed: float,
    slope: float,
    slope_min: float,
    R2: float,
    R2_min: float,
) -> Tuple[bool, Dict[str, float]]:
    """Gate helper for metriplectic Lyapunov monitor and two-grid scaling.

    Conditions
    ----------
    - delta_Lh_max <= delta_Lh_max_allowed (typically 0.0)
    - slope >= slope_min (e.g. 2.9 for Strang-2)
    - R2 >= R2_min
    """
    passed_Lh = bool(delta_Lh_max <= delta_Lh_max_allowed)
    passed_slope = bool(slope >= slope_min)
    passed_R2 = bool(R2 >= R2_min)
    passed = bool(passed_Lh and passed_slope and passed_R2)

    metrics: Dict[str, float] = {
        "delta_Lh_max": float(delta_Lh_max),
        "delta_Lh_max_allowed": float(delta_Lh_max_allowed),
        "slope": float(slope),
        "slope_min": float(slope_min),
        "R2": float(R2),
        "R2_min": float(R2_min),
        "passed_Lh": bool(passed_Lh),
        "passed_slope": bool(passed_slope),
        "passed_R2": bool(passed_R2),
        "passed": bool(passed),
    }
    return passed, metrics


def gate_metriplectic_degeneracy(
    *,
    g1: float,
    g2: float,
    eps: float,
) -> Tuple[bool, Dict[str, float]]:
    """Gate helper for metriplectic degeneracy residuals.

    Conditions
    ----------
    - g1 <= eps
    - g2 <= eps
    """
    passed_g1 = bool(g1 <= eps)
    passed_g2 = bool(g2 <= eps)
    passed = bool(passed_g1 and passed_g2)

    metrics: Dict[str, float] = {
        "g1": float(g1),
        "g2": float(g2),
        "eps": float(eps),
        "passed_g1": bool(passed_g1),
        "passed_g2": bool(passed_g2),
        "passed": bool(passed),
    }
    return passed, metrics


__all__ = [
    "gate_kg_cone_speed",
    "gate_kg_energy_osc_scaling",
    "gate_metriplectic_lyapunov",
    "gate_metriplectic_degeneracy",
]