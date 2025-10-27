#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
# Non-interference A/B test for read-only walker announcers
# Ensures stepping/sensing walkers does not alter the fluid dynamics.

import numpy as np

# Ensure repo root on sys.path for absolute import 'Prometheus_VDM.*'
import sys, pathlib
_P = pathlib.Path(__file__).resolve()
for _anc in [_P] + list(_P.parents):
    if _anc.name == "Prometheus_VDM":
        _ROOT = str(_anc.parent)
        if _ROOT not in sys.path:
            sys.path.insert(0, _ROOT)
        break

from Prometheus_VDM.derivation.code.physics.fluid_dynamics.fluids.lbm2d import LBM2D, LBMConfig
from Prometheus_VDM.derivation.code.physics.fluid_dynamics.telemetry.walkers import seed_walkers_lid, Walker  # noqa: F401


def run_cavity(nx=48, ny=48, steps=400, tau=0.7, U=0.05, with_walkers=False, walkers=96, seed=1):
    # Deterministic run (LBM2D has no internal RNG in this configuration)
    cfg = LBMConfig(
        nx=nx, ny=ny, tau=tau,
        periodic_x=False, periodic_y=False,
        void_enabled=False,  # avoid any external dynamics; pure BGK baseline
        rho_floor=1e-9,
        u_clamp=0.1,
    )
    sim = LBM2D(cfg)
    sim.set_solid_box(top=False, bottom=True, left=True, right=True)

    # Prepare walkers (read-only)
    walker_list = []
    if with_walkers:
        walker_list = seed_walkers_lid(sim.nx, sim.ny, count=int(walkers), kinds=["div", "swirl", "shear"], seed=int(seed))

    for n in range(steps):
        sim.step(1)
        sim.set_lid_velocity(U)
        sim.moments()
        if with_walkers and walker_list:
            # Pure read-only usage: advect and sense, no bus posting nor policy application
            for w in walker_list:
                w.step(sim, dt=1.0)
                _ = w.sense(sim)

    sim.moments()
    # Return copies to freeze state for comparison
    return np.array(sim.ux, copy=True), np.array(sim.uy, copy=True)


def test_walkers_noninterference_observe_only():
    ux_off, uy_off = run_cavity(with_walkers=False)
    ux_on,  uy_on  = run_cavity(with_walkers=True)
    # Expect exact equality; allow extremely small numeric jitter if any
    diff_u = float(np.max(np.abs(ux_on - ux_off))) if ux_off.size else 0.0
    diff_v = float(np.max(np.abs(uy_on - uy_off))) if uy_off.size else 0.0
    assert diff_u == 0.0 and diff_v == 0.0, f"Read-only walkers changed fields: max|Δux|={diff_u:.3e}, max|Δuy|={diff_v:.3e}"