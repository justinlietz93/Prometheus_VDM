#!/usr/bin/env python3
from __future__ import annotations

from typing import Dict, Tuple
import numpy as np

from physics.metriplectic.kg_ops import spectral_grad


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
    # clamp to [0,1] for reporting
    return float(max(0.0, min(1.0, x)))
