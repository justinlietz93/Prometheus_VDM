#!/usr/bin/env python3
"""
Preflight test for the instrumented CEG harness.

This test runs a small, deterministic EchoSpec via the harness and asserts
structure and that the diagnostics key is present. It intentionally does not
require positive CEG (that is for gated/main-run validation).
"""
from __future__ import annotations

from Derivation.code.physics.metriplectic.instrumented_ceg import run_ceg_harness
from Derivation.code.physics.metriplectic.assisted_echo import EchoSpec


def test_ceg_harness_preflight_smoke():
    spec = EchoSpec(
        grid={"N": 24, "dx": 1.0},
        params={"c": 1.0, "m": 0.0, "m_lap_operator": "spectral", "D": 1.0, "r": 0.0, "u": 0.0},
        dt=0.01,
        steps=1,
        seeds=[0],
        lambdas=[0.0, 1.0],
        budget=0.0,
        tag="preflight",
    )

    out = run_ceg_harness(spec, write_artifacts=False)
    assert isinstance(out, dict)
    assert "diagnostics" in out and isinstance(out["diagnostics"], dict)
    # ensure ceg_summary exists (structure)
    assert "ceg_summary" in out and isinstance(out["ceg_summary"], dict)
