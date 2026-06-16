#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Echo metrics for CEG measurement.
"""
from __future__ import annotations

import numpy as np

from .kg_ops import spectral_grad


def h_energy_norm_delta(phi_a: np.ndarray, pi_a: np.ndarray, phi_b: np.ndarray, pi_b: np.ndarray, dx: float, c: float, m: float) -> float:
    dphi = (phi_a - phi_b)
    dpi = (pi_a - pi_b)
    g = spectral_grad(dphi, dx)
    e2 = float(np.sum(dpi * dpi + (c * c) * (g * g) + (m * m) * (dphi * dphi)) * dx)
    return float(np.sqrt(max(e2, 0.0)))


def ceg(baseline_err: float, assisted_err: float) -> float:
    if baseline_err <= 0.0:
        return 0.0
    x = (baseline_err - assisted_err) / baseline_err
    return float(max(0.0, min(1.0, x)))
