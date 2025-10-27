#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Taylor-Green viscosity recovery unit test (fluid_dynamics domain).

Pathing rule:
- Tests live under derivation/code/tests/<domain>/
- This test checks that ν_fit recovered from E(t) decay matches ν_th within 5% at 256x256.

No figures/logs are written; this is a fast numeric check.
"""

import sys, math
import numpy as np
from pathlib import Path

# Ensure repo root on sys.path for absolute imports
_THIS = Path(__file__).resolve()
for p in [_THIS] + list(_THIS.parents):
    if p.name == "Prometheus_VDM":
        root = str(p.parent)
        if root not in sys.path:
            sys.path.insert(0, root)
        break

from Prometheus_VDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig


def _init_tg(sim: LBM2D, U0: float, k: float):
    nx, ny = sim.nx, sim.ny
    x = (np.arange(nx, dtype=float) + 0.5) / nx
    y = (np.arange(ny, dtype=float) + 0.5) / ny
    X, Y = np.meshgrid(x, y)
    sim.ux[:, :] =  U0 * np.cos(k * X) * np.sin(k * Y)
    sim.uy[:, :] = -U0 * np.sin(k * X) * np.cos(k * Y)
    sim._set_equilibrium()


def _energy(ux: np.ndarray, uy: np.ndarray) -> float:
    return 0.5 * float(np.mean(ux**2 + uy**2))


def test_taylor_green_viscosity_recovery():
    # Baseline grid/params consistent with acceptance doc
    nx = 256
    ny = 256
    tau = 0.8                # => nu_th = (tau-0.5)/3 = 0.1
    U0  = 0.05
    k   = 2.0 * math.pi

    cfg = LBMConfig(nx=nx, ny=ny, tau=tau, periodic_x=True, periodic_y=True)
    sim = LBM2D(cfg)
    _init_tg(sim, U0, k)

    steps = 3000
    sample_every = 30

    ts, Es = [], []
    for n in range(steps + 1):
        if n % sample_every == 0:
            sim.moments()
            ts.append(float(n))
            Es.append(_energy(sim.ux, sim.uy))
        sim.step(1)

    ts = np.asarray(ts, dtype=float)
    Es = np.asarray(Es, dtype=float)

    # Fit log E(t) with robust minimal guard (avoid underflow-only samples)
    mask = Es > (float(Es.max()) * 1e-12)
    ts_fit = ts[mask] if np.any(mask) else ts
    Es_fit = Es[mask] if np.any(mask) else Es
    assert ts_fit.size >= 3, f"Insufficient TG samples for fit: {ts_fit.size}"

    slope, intercept = np.polyfit(ts_fit, np.log(Es_fit + 1e-300), 1)

    # Correct inversion: K^2 = k^2 (1/nx^2 + 1/ny^2)
    K2 = (k * k) * ((1.0 / (nx * nx)) + (1.0 / (ny * ny)))
    nu_fit = float(-slope / (2.0 * K2))
    nu_th  = (1.0 / 3.0) * (tau - 0.5)
    rel_err = abs(nu_fit - nu_th) / (abs(nu_th) + 1e-12)

    # Acceptance (baseline)
    assert rel_err <= 0.05, f"TG ν mismatch: nu_fit={nu_fit:.6g}, nu_th={nu_th:.6g}, rel_err={rel_err:.3%}"