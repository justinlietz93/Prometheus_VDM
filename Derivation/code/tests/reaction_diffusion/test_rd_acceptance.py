#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.


Acceptance guards for RD canonical validations.

These tests directly call simulation helpers (no file I/O) and assert the same acceptance gates as the reproducible scripts:
- Front speed: rel_err <= 0.05 and R^2 >= 0.98
- Dispersion: med_rel_err <= 0.10 and r2_array >= 0.98
"""

import os, sys
import numpy as np

# Ensure repository root on sys.path for imports when running directly
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from Prometheus_VDM.derivation.code.physics.reaction_diffusion.rd_front_speed_experiment import run_sim as rd_run_front
from Prometheus_VDM.derivation.code.physics.reaction_diffusion.rd_dispersion_experiment import run_linear_sim as rd_run_lin, analyze_dispersion as rd_analyze

def test_front_speed_acceptance_default():
    N = 1024; L = 200.0; D = 1.0; r = 0.25; T = 80.0; cfl = 0.2; seed = 42
    level = 0.1; x0 = -60.0; fit_frac = (0.6, 0.9); noise_amp = 0.0
    data = rd_run_front(N, L, D, r, T, cfl, seed, level=level, x0=x0, fit_frac=fit_frac, noise_amp=noise_amp)
    # Acceptance gates (same as script)
    assert np.isfinite(data["r2"]) and data["r2"] >= 0.98, f"Front-speed R^2 gate failed: R2={data['r2']}"
    assert np.isfinite(data["rel_err"]) and data["rel_err"] <= 0.05, f"Front-speed rel_err gate failed: rel_err={data['rel_err']}"
    assert np.isfinite(data["c_meas"]) and data["c_meas"] > 0, "Expected positive pulled-front speed"

def test_dispersion_acceptance_default():
    N = 1024; L = 200.0; D = 1.0; r = 0.25; T = 10.0; cfl = 0.2; seed = 42
    sim = rd_run_lin(N, L, D, r, T, cfl, seed, amp0=1e-6, record_slices=80)
    analysis = rd_analyze(sim, D, r, L, m_max=64, fit_frac=(0.1, 0.4))
    # Acceptance gates (same as script)
    assert np.isfinite(analysis["med_rel_err"]) and analysis["med_rel_err"] <= 0.10, f"Dispersion med_rel_err gate failed: {analysis['med_rel_err']}"
    assert np.isfinite(analysis["r2_array"]) and analysis["r2_array"] >= 0.98, f"Dispersion r2_array gate failed: {analysis['r2_array']}"

if __name__ == "__main__":
    # Light self-check
    test_front_speed_acceptance_default()
    test_dispersion_acceptance_default()
    print("RD acceptance guards passed.")