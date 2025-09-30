"""Tests for the vacuum demographics harness."""

from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from fum_rt.physics import vacuum_demographics_harness as harness


def test_eta_zero_matches_baseline(tmp_path: Path) -> None:
    events, timeline = harness.default_horizon_tape()
    config = harness.HarnessConfig(
        epsilon=5e-3,
        local_radius=1.0,
        max_events=64,
        rho_lambda=6.0e-27,
        eta=0.0,
        residual_tol=1e-8,
        position=(0.0, 0.0, 0.0),
        budget=None,
    )
    figure_path = tmp_path / "residuals.png"
    payload = harness.evaluate_vacuum_demographics(
        events,
        timeline,
        config,
        figure_path=str(figure_path),
    )
    assert payload["metrics"]["status"] == "PASS"
    assert math.isclose(payload["metrics"]["max_abs"], 0.0, abs_tol=1e-12)
    assert figure_path.exists()
    assert all(math.isclose(row["w_residual"], 0.0, abs_tol=1e-12) for row in payload["timeline"])


def test_large_eta_triggers_recalibration(tmp_path: Path) -> None:
    events, timeline = harness.default_horizon_tape()
    config = harness.HarnessConfig(
        epsilon=2.0,
        local_radius=1.0,
        max_events=64,
        rho_lambda=6.0e-27,
        eta=0.5,
        residual_tol=1e-4,
        position=(0.0, 0.0, 0.0),
        budget=None,
    )
    payload = harness.evaluate_vacuum_demographics(events, timeline, config)
    assert payload["metrics"]["status"] == "NEEDS_RECAL"
    assert payload["metrics"]["max_abs"] > config.residual_tol


def test_load_tape_from_json(tmp_path: Path) -> None:
    tape_path = tmp_path / "custom_tape.json"
    tape_payload = {
        "events": [
            {
                "t": 100,
                "x": [0.0, 0.0, 0.0],
                "dotA": 1.5e-6,
                "horizon_id": "bh_a",
                "dt_ret": 30.0,
            },
            {
                "t": 200,
                "x": [0.1, 0.0, 0.0],
                "dotA": -1.0e-6,
                "horizon_id": "bh_b",
                "dt_ret": 45.0,
            },
        ],
        "timeline": [
            {"t_myr": 300.0, "redshift": 2.5},
            {"t_myr": 150.0, "redshift": 4.0},
        ],
    }
    tape_path.write_text(json.dumps(tape_payload), encoding="utf-8")
    events, timeline = harness.load_horizon_tape(str(tape_path))
    assert len(events) == 2
    assert isinstance(events[0], harness.HorizonActivityEvent)
    assert timeline[0].t_myr == pytest.approx(150.0)
    assert timeline[1].t_myr == pytest.approx(300.0)

