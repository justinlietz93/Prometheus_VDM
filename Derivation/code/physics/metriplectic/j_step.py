#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


J-step (conservative) for metriplectic composition.

Implements an exact periodic advection update via spectral phase rotation:
    W(x, t + dt) = W(x - c dt, t)
This update is unitary (L2-preserving), volume-preserving, and reversible.

Note: This surrogate J-step serves as a symplectic-like conservative flow for a
single field W, avoiding the need for explicit (phi, pi) pairs while preserving
quadratic invariants. It composes cleanly with the dissipative DG M-step.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np


# Ensure code root on sys.path so imports like common.io_paths resolve when used elsewhere
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))


def j_step_spectral_periodic(W: np.ndarray, dt: float, dx: float, c: float) -> np.ndarray:
    """Exact periodic advection by distance c*dt using spectral phase shift.

    Parameters:
    - W: state array (shape: (N,))
    - dt: time step (float)
    - dx: grid spacing (float)
    - c: advection speed (float)

    Returns: W at time t+dt under W_t + c W_x = 0 with periodic BC.
    """
    if dt == 0.0 or c == 0.0:
        return W.copy()
    N = W.size
    # Physical wavenumbers (rad/unit length)
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    phase = np.exp(-1j * k * (c * dt))
    W_hat = np.fft.fft(W)
    Wn1 = np.fft.ifft(W_hat * phase).real
    return Wn1


__all__ = ["j_step_spectral_periodic"]
