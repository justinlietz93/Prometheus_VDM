#!/usr/bin/env python3
"""
Lightweight preflight smoke test for assisted_echo runner.

This test runs a tiny EchoSpec via the public `run_assisted_echo` function and
verifies that results contain expected keys and that the gate ledger is present.
It intentionally uses small sizes and the in-memory runner to avoid writing
artifacts to disk.
"""
from __future__ import annotations

from pathlib import Path
import json
import numpy as np

from Derivation.code.physics.metriplectic.assisted_echo import EchoSpec, run_assisted_echo


def test_assisted_echo_preflight_smoke():
    spec = EchoSpec(
        grid={"N": 16, "dx": 1.0},
        params={"c": 1.0, "m": 0.0, "m_lap_operator": "spectral", "D": 1.0, "r": 0.0, "u": 0.0},
        dt=0.01,
        steps=1,
        seeds=[0],
        lambdas=[0.0, 1.0],
        budget=0.0,
        tag="preflight"
    )

    out = run_assisted_echo(spec)
    # Basic structure
    assert isinstance(out, dict)
    assert "per_seed" in out and isinstance(out["per_seed"], list)
    assert "ceg_summary" in out and isinstance(out["ceg_summary"], dict)

    # Gate ledger presence
    assert "gate_ledger_per_seed" in out
    assert isinstance(out["gate_ledger_per_seed"], list)
    # Each gate entry should have 'gates' list and each gate has a 'passed' boolean
    for entry in out["gate_ledger_per_seed"]:
        assert "gates" in entry and isinstance(entry["gates"], list)
        for g in entry["gates"]:
            assert "gate" in g and "passed" in g

    # summary present
    assert "gate_ledger_summary" in out and isinstance(out["gate_ledger_summary"], dict)
