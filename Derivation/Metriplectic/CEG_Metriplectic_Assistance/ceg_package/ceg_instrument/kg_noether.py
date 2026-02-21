#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


KG Noether invariant utilities (self-contained, local imports only).
"""
from __future__ import annotations

from typing import Dict, Any, List, Tuple

import numpy as np

from .kg_ops import spectral_grad, spectral_laplacian


def stiffness(phi: np.ndarray, dx: float, c: float, m: float) -> np.ndarray:
    """K phi = -c² Δ_h phi + m² phi (periodic spectral)."""
    return -(c * c) * spectral_laplacian(phi, dx) + (m * m) * phi


def verlet_step_with_half(
    phi: np.ndarray, pi: np.ndarray, dt: float, dx: float, c: float, m: float
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """One Störmer-Verlet step returning (phi_new, pi_half, pi_new)."""
    lap_phi = spectral_laplacian(phi, dx)
    pi_half = pi + 0.5 * dt * ((c * c) * lap_phi - (m * m) * phi)
    phi_new = phi + dt * pi_half
    lap_phi_new = spectral_laplacian(phi_new, dx)
    pi_new = pi_half + 0.5 * dt * ((c * c) * lap_phi_new - (m * m) * phi_new)
    return phi_new, pi_half, pi_new


__all__ = ["stiffness", "verlet_step_with_half"]
