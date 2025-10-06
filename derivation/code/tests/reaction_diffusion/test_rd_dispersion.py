#!/usr/bin/env python3
"""
Minimal unit tests for RD dispersion and Laplacians.

Reason: Physics validated via derivation/code/physics scripts; these tests guard formulas and signs.
"""

import os, sys
import numpy as np

# Ensure repository root on sys.path for imports when running directly
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from Prometheus_VDM.derivation.code.physics.rd_dispersion_experiment import laplacian_periodic
from Prometheus_VDM.derivation.code.physics.rd_front_speed_experiment import laplacian_neumann

def test_discrete_dispersion_matches_eigenvalues():
    N = 256
    L = 200.0
    D = 1.0
    r = 0.25
    dx = L / N
    js = np.arange(N, dtype=float)
    m_list = [0, 1, 2, 7, N//4, N//2]
    for m in m_list:
        u = np.exp(1j * 2.0 * np.pi * m * js / N)
        lam = laplacian_periodic(u, dx) / u
        lam_mean = np.mean(lam)
        lam_th = -4.0 * (np.sin(np.pi * m / N) ** 2) / (dx * dx)
        assert np.allclose(lam_mean, lam_th, rtol=1e-12, atol=1e-12), f"λ_m mismatch for m={m}"
        sigma_meas = r + D * lam_mean
        sigma_disc = r - (4.0 * D / (dx * dx)) * (np.sin(np.pi * m / N) ** 2)
        assert np.allclose(sigma_meas, sigma_disc, rtol=1e-12, atol=1e-12), f"σ_d mismatch for m={m}"

def test_neumann_quadratic_second_derivative_is_two():
    N = 201
    L = 2.0
    x = np.linspace(-L/2, L/2, N, endpoint=False)
    dx = x[1] - x[0]
    u = x**2
    lap = laplacian_neumann(u, dx)
    interior = lap[1:-1]
    assert np.max(np.abs(interior - 2.0)) < 1e-10, "Neumann Laplacian on x^2 should be exactly 2 in interior"

if __name__ == "__main__":
    # Lightweight self-check without pytest
    test_discrete_dispersion_matches_eigenvalues()
    test_neumann_quadratic_second_derivative_is_two()
    print("All tests passed.")