"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import os
import math
import numpy as np
import pytest

if not os.getenv("VDM_TEST_VDM_EQUATIONS"):
    pytest.skip("Skipping vdm_equations tests unless VDM_TEST_VDM_EQUATIONS=1", allow_module_level=True)

from Derivation.code.common.vdm_equations import (
    PotentialParams,
    RDParams,
    Vp,
    Vpp,
    rd_reaction,
    logistic_exact_step,
    dispersion_continuum,
    kpp_front_speed,
    kg_c2_from_lattice,
    stabilized_vacuum,
    effective_mass_squared,
)


def test_kpp_front_speed_identity():
    D, r = 1.0, 0.25
    c = kpp_front_speed(D, r)
    assert math.isclose(c, 2.0 * math.sqrt(D * r))  # nosec B101


def test_dispersion_continuum_linear():
    D, r = 2.0, 0.5
    k = np.array([0.0, 0.1, 1.0])
    sig = dispersion_continuum(k, D, r)
    np.testing.assert_allclose(sig, r - D * k * k)


def test_logistic_exact_small_dt_matches_euler():
    r, u = 0.25, 0.25
    W0, dt = 0.1, 1e-6
    W1_exact = logistic_exact_step(W0, dt, r, u)
    W1_euler = W0 + dt * rd_reaction(W0, r, u)
    assert math.isclose(W1_exact, W1_euler, rel_tol=0, abs_tol=1e-10)  # nosec B101


def test_potential_derivatives_consistency():
    p = PotentialParams(alpha=0.25, beta=0.10, lam=0.0)
    phi = 0.2
    # V'' = d/dφ V' numerically
    eps = 1e-6
    dVp_num = (Vp(phi + eps, p) - Vp(phi - eps, p)) / (2 * eps)
    dVp_ana = Vpp(phi, p)
    assert math.isclose(dVp_num, dVp_ana, rel_tol=1e-6, abs_tol=1e-6)  # nosec B101


def test_kg_c2_mapping():
    assert math.isclose(kg_c2_from_lattice(J=0.5, a=1.0, convention="per-site"), 1.0)  # nosec B101
    assert math.isclose(kg_c2_from_lattice(J=0.5, a=1.0, convention="per-edge"), 1.0)  # nosec B101


def test_stabilized_vacuum_and_mass_small_lambda():
    p = PotentialParams(alpha=0.25, beta=0.10, lam=1e-6)
    v = stabilized_vacuum(p)
    assert v > 0  # nosec B101
    m2 = effective_mass_squared(p)
    assert m2 > 0  # nosec B101
