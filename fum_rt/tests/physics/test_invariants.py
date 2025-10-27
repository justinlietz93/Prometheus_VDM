"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
fum_rt.tests.physics.test_invariants

CI tests for physics ↔ code guard helpers:
- Q_FUM (logistic on-site constant of motion) spot-check
- Kinetic normalization equivalence (c^2 from κ vs 2J)
- Memory steering dimensionless groups extraction

Constraints:
- Pure stdlib; no runtime/core heavy imports except the guard helpers under test.
- No scans of core/maps; tests operate on small synthetic arrays only.
"""

import math
import random
from typing import List

from fum_rt.core.guards.invariants import (
    qfum_logistic_value,
    check_qfum_logistic,
    kinetic_c2_from_kappa,
    kinetic_c2_from_J,
    compute_memory_groups,
)


def _logistic_exact_next(w0: float, dt: float, alpha: float, beta: float) -> float:
    """
    Exact solution for dW/dt = (α - β) W - α W^2 = k W (1 - W/K),
    with k = α - β, K = (α - β)/α (α>0).
    """
    a = float(alpha)
    b = float(beta)
    k = a - b
    if not (a > 0.0 and k != 0.0):
        return float(w0)
    K = k / a
    # Avoid singularities by clamping input w0 into (0, K)
    eps = 1e-12
    w0c = max(eps, min(float(w0), K - eps))
    A = (K - w0c) / w0c
    return K / (1.0 + A * math.exp(-k * float(dt)))


def test_qfum_logistic_constant_of_motion_p99() -> None:
    """
    Generate synthetic pairs (W_prev, W_curr) from the exact logistic solution
    and verify the analytic Q_FUM drift is negligible (p99 and max within tight tol).
    """
    alpha = 0.25
    beta = 0.10
    k = alpha - beta
    assert alpha > beta > 0.0
    assert k > 0.0

    # Time span
    t_prev = 10.0  # non-zero start time to exercise t dependence
    dt = 0.7
    t_curr = t_prev + dt

    # Capacity and sampling inside (0.01*K, 0.99*K)
    K = (alpha - beta) / alpha
    lo = 0.01 * K
    hi = 0.99 * K

    rng = random.Random(123)
    n = 512
    w_prev: List[float] = []
    w_curr: List[float] = []
    for _ in range(n):
        w0 = lo + (hi - lo) * rng.random()
        w1 = _logistic_exact_next(w0, dt, alpha, beta)
        w_prev.append(w0)
        w_curr.append(w1)

    # Tight tolerances since we use the exact solution
    res = check_qfum_logistic(
        w_prev,
        w_curr,
        t_prev=t_prev,
        t_curr=t_curr,
        alpha=alpha,
        beta=beta,
        tol_abs=1e-9,
        tol_p99=1e-10,
    )

    # Sanity: structure of result
    assert int(res.get("count", 0)) > 0
    # CI acceptance: p99 drift below tolerance; extremely small max drift
    assert bool(res.get("pass_p99", False)), f"p99 drift failed: {res}"
    assert float(res.get("dQ_max", 0.0)) <= 1e-8, f"max drift too large: {res}"

    # Spot-check a few direct pairs with the scalar helper
    for idx in (0, n // 3, (2 * n) // 3, n - 1):
        q0 = qfum_logistic_value(w_prev[idx], t_prev, alpha=alpha, beta=beta)
        q1 = qfum_logistic_value(w_curr[idx], t_curr, alpha=alpha, beta=beta)
        assert abs(q1 - q0) <= 1e-8


def test_kinetic_normalization_equivalence_kappa_2J() -> None:
    """
    Kinetic normalization sanity:
    c^2 = κ a^2 and c^2 = 2 J a^2. For κ = 2J the two expressions must match.
    """
    # Probe a few scales
    cases = [
        (1.0, 0.5),   # a, J
        (2.0, 0.125),
        (0.25, 3.0),
        (3.0, 1e-3),
    ]
    for a, J in cases:
        kappa = 2.0 * J
        c2_kappa = kinetic_c2_from_kappa(kappa, a)
        c2_J = kinetic_c2_from_J(J, a)
        # Relative tolerance check
        denom = max(1e-12, abs(c2_kappa) + abs(c2_J))
        rel = abs(c2_kappa - c2_J) / denom
        assert rel <= 1e-12, f"Normalization mismatch: κ={kappa}, J={J}, a={a}, c2_kappa={c2_kappa}, c2_J={c2_J}, rel={rel}"


def test_compute_memory_groups_reads_dimensionless_params() -> None:
    """
    Verify telemetry-facing dimensionless memory parameters are read out properly.
    """

    class _FakeField:
        Theta = 1.234
        D_a = 0.5
        Lambda = 0.1
        Gamma = 0.2

    g = compute_memory_groups(_FakeField())
    assert math.isclose(g.get("mem_Theta", 0.0), 1.234, rel_tol=0.0, abs_tol=0.0)
    assert math.isclose(g.get("mem_Da", 0.0), 0.5, rel_tol=0.0, abs_tol=0.0)
    assert math.isclose(g.get("mem_Lambda", 0.0), 0.1, rel_tol=0.0, abs_tol=0.0)
    assert math.isclose(g.get("mem_Gamma", 0.0), 0.2, rel_tol=0.0, abs_tol=0.0)