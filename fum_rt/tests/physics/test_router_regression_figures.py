"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import json
from pathlib import Path

import numpy as np
import pytest

import fum_rt.physics.router_regression_figures as rfig


pytestmark = pytest.mark.filterwarnings("ignore:All-NaN slice encountered")


def test_front_speed_comparison_and_plot(tmp_path):
    config = rfig.FrontSpeedConfig(N=128, L=80.0, T=40.0, seed=7, noise_amp=0.0)
    data = rfig.generate_front_speed_comparison(config)
    assert data["x"].shape == data["snapshots"][0].shape
    if data["x_front_delta"].size:
        assert float(np.max(np.abs(data["x_front_delta"]))) < 1e-8
    figure = tmp_path / "front.png"
    rfig.render_front_speed_figure(data, figure.as_posix())
    assert figure.exists()


def test_dispersion_comparison_and_plot(tmp_path):
    config = rfig.DispersionConfig(N=256, L=80.0, T=6.0, record=32, m_max=16, amp0=1e-4)
    data = rfig.generate_dispersion_comparison(config)
    assert data["k"].shape == data["sigma_base"].shape
    assert float(np.max(np.abs(data["sigma_delta"]))) < 1e-8
    figure = tmp_path / "dispersion.png"
    rfig.render_dispersion_figure(data, figure.as_posix())
    assert figure.exists()


def test_qdrift_comparison_and_plot(tmp_path):
    config = rfig.QDriftConfig(T=5.0, dt=0.005)
    data = rfig.generate_qdrift_comparison(config)
    assert data["t"].ndim == 1
    assert data["delta_Q"].shape == data["t"].shape
    assert float(np.max(np.abs(data["delta_Q"]))) < 1e-12
    figure = tmp_path / "qdrift.png"
    rfig.render_qdrift_figure(data, figure.as_posix())
    assert figure.exists()


def test_build_payload_and_enrich(tmp_path):
    front = rfig.generate_front_speed_comparison(rfig.FrontSpeedConfig(N=96, L=40.0, T=20.0))
    dispersion = rfig.generate_dispersion_comparison(rfig.DispersionConfig(N=192, L=40.0, T=4.0, record=20, m_max=10, amp0=1e-4))
    qdrift = rfig.generate_qdrift_comparison(rfig.QDriftConfig(T=4.0, dt=0.01))
    outputs = {
        "front_figure": (tmp_path / "front.png").as_posix(),
        "dispersion_figure": (tmp_path / "dispersion.png").as_posix(),
        "qdrift_figure": (tmp_path / "qdrift.png").as_posix(),
        "log": (tmp_path / "run.json").as_posix(),
    }
    payload = rfig.build_payload(front, dispersion, qdrift, outputs, "2025-01-02T00:00:00Z")
    enriched = rfig.enrich_payload(
        payload,
        script_name="router_regression_figures",
        gates={"ok": True},
        hashes={"front": rfig.hash_jsonable(front["metrics"])},
        seeds={"seed": 1},
        outputs=outputs,
    )
    log_path = Path(outputs["log"])
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(enriched))
    assert json.loads(log_path.read_text())["outputs"]["log"].endswith("run.json")
