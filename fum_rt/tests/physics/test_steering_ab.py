"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

"""
fum_rt.tests.physics.test_steering_ab

CI: Steering A/B acceptance tests (void-faithful, pure numeric; no scans).

Scope:
- Softmax steering law P(i→j) ∝ exp(Θ m_j)
- Junction A/B identity: log(P_B / P_A) == Θ * (m_B - m_A)
- Empirical sampling from the softmax matches analytic probabilities

Notes:
- Uses stdlib only; avoids importing heavy core modules.
- Deterministic RNG for stable CI behavior.
"""

import math
import random
from typing import Tuple


def _softmax_two(m_a: float, m_b: float, Theta: float) -> Tuple[float, float]:
    ea = math.exp(float(Theta) * float(m_a))
    eb = math.exp(float(Theta) * float(m_b))
    Z = ea + eb
    if Z == 0.0:
        # Degenerate; return uniform
        return 0.5, 0.5
    return ea / Z, eb / Z


def test_logit_identity_matches_theta_delta_m() -> None:
    """
    For two-branch junction A/B with P ∝ exp(Θ m):
      log(P_B / P_A) == Θ * (m_B - m_A)

    This is an analytic identity; we allow tiny numeric tolerance.
    """
    rng = random.Random(321)
    # Sweep Θ including attraction/repulsion and weak/strong coupling regimes
    thetas = [0.0, 0.25, 1.0, -0.5, 2.0]
    for Theta in thetas:
        for _ in range(256):
            # Sample memory field values within a moderate range
            m_a = rng.uniform(-3.0, 3.0)
            m_b = rng.uniform(-3.0, 3.0)

            p_a, p_b = _softmax_two(m_a, m_b, Theta)
            # Guard against underflow/overflow by clamping probabilities
            p_a = max(1e-15, min(1.0 - 1e-15, p_a))
            p_b = max(1e-15, min(1.0 - 1e-15, p_b))

            left = math.log(p_b / p_a)
            right = float(Theta) * (float(m_b) - float(m_a))

            # Tight relative/absolute tolerances (identity)
            diff = abs(left - right)
            # For Theta==0, left and right should both be ~0; use abs tol
            if Theta == 0.0:
                assert diff <= 1e-12
            else:
                denom = max(1.0, abs(left) + abs(right))
                assert diff <= 1e-12 * denom, f"Theta={Theta}, m_a={m_a}, m_b={m_b}, left={left}, right={right}, diff={diff}"


def test_sampling_matches_softmax_probability() -> None:
    """
    Monte Carlo sanity: sample choices vs. analytic softmax probabilities.

    Draw N trials using the analytic P_B, count frequency of B, and compare
    against P_B with binomial standard deviation tolerance.
    """
    rng = random.Random(12345)
    cases = [
        # (m_a, m_b, Theta, N)
        (0.0, 0.0, 1.0, 2000),   # symmetric
        (0.5, -0.5, 1.0, 4000),  # B disfavored
        (-1.0, 1.0, 0.75, 4000), # B favored
        (1.5, 0.1, -1.25, 5000), # repulsive steering (negative Theta)
    ]
    for m_a, m_b, Theta, N in cases:
        p_a, p_b = _softmax_two(m_a, m_b, Theta)
        # Sample
        count_b = 0
        for _ in range(int(N)):
            u = rng.random()
            if u <= p_b:
                count_b += 1
        freq_b = count_b / float(N)

        # Binomial standard deviation σ = sqrt(p(1-p)/N)
        sigma = math.sqrt(max(1e-15, p_b * (1.0 - p_b)) / float(N))
        # Accept within 5σ to be robust across environments
        assert abs(freq_b - p_b) <= 5.0 * sigma, f"Sampling drift too large: freq={freq_b}, p={p_b}, σ={sigma}, case={(m_a, m_b, Theta, N)}"