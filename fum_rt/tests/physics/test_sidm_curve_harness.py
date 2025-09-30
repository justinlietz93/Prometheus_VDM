from __future__ import annotations

import json

from fum_rt.core.cosmology import GrainScatteringShim
from fum_rt.physics.sidm_curve_harness import (
    ACCEPTANCE_BANDS,
    DEFAULT_GRID,
    build_payload,
    evaluate_curve,
    generate_curve,
    parse_velocity_grid,
    render_curve_figure,
)


def test_parse_velocity_grid_deduplicates_and_sorts() -> None:
    velocities = parse_velocity_grid("50, 10, 50, 30")
    assert velocities == [10.0, 30.0, 50.0]


def test_sidm_curve_analysis_pass_and_plot(tmp_path) -> None:
    shim = GrainScatteringShim(
        r_star=0.5,
        mass_scale=1.0,
        v_scale=150.0,
        alpha=2.0,
        sigma_floor=1e-3,
        sigma_ceiling=10.0,
    )
    velocities = parse_velocity_grid(DEFAULT_GRID)
    curve = generate_curve(shim, velocities)
    analysis = evaluate_curve(curve)
    assert analysis["status"] == "PASS"
    assert analysis["within_bands"]
    assert analysis["monotone"]
    assert len(analysis["details"]) == len(velocities)

    figure_path = tmp_path / "sidm.png"
    render_curve_figure(curve, str(figure_path), status=analysis["status"])
    assert figure_path.exists()

    payload = build_payload(
        shim=shim,
        curve=curve,
        analysis=analysis,
        figure_path=str(figure_path),
        velocity_grid=velocities,
        timestamp="2025-09-30T00:00:00Z",
    )
    json.dumps(payload)  # ensure serializable
    assert payload["analysis"]["status"] == "PASS"
    assert len(payload["acceptance_bands"]) == len(ACCEPTANCE_BANDS)


def test_sidm_curve_analysis_flags_out_of_band() -> None:
    shim = GrainScatteringShim(
        r_star=1.5,
        mass_scale=0.02,
        v_scale=400.0,
        alpha=1.0,
        sigma_floor=1e-3,
        sigma_ceiling=100.0,
    )
    velocities = parse_velocity_grid("10,30,60")
    curve = generate_curve(shim, velocities)
    analysis = evaluate_curve(curve)
    assert analysis["status"] == "NEEDS_RECAL"
    assert not analysis["within_bands"]
    assert analysis["details"][0]["within_band"] is False
