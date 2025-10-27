"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
from __future__ import annotations

import math
from typing import List

from fum_rt.physics.pta_correlation_harness import (
    CorrelationConfig,
    compute_correlation_series,
    evaluate_pta_correlation,
)
from fum_rt.physics.vacuum_demographics_harness import (
    TimelinePoint,
    default_horizon_tape,
)


def test_compute_correlation_series_respects_locality() -> None:
    events, timeline = default_horizon_tape()
    samples = compute_correlation_series(
        events,
        timeline,
        window=180.0,
        tau=90.0,
        min_points=1,
    )
    assert len(samples) == len(timeline)
    previous_time = -math.inf
    for sample in samples:
        assert sample.time_myr >= previous_time
        assert sample.contributing_events >= 0
        previous_time = sample.time_myr


def test_evaluate_pta_correlation_flags_insufficient_coverage() -> None:
    events, timeline = default_horizon_tape()
    config = CorrelationConfig(window=60.0, tau=30.0, min_points=3)
    payload = evaluate_pta_correlation(
        events,
        timeline,
        config,
        figure_path=None,
        min_coverage=0.9,
    )
    assert payload["metrics"]["status"] == "NEEDS_RECAL"
    assert payload["metrics"]["strong_coverage"] < 0.9


def test_compute_correlation_series_requires_monotonic_timeline() -> None:
    events, timeline = default_horizon_tape()
    reversed_timeline: List[TimelinePoint] = list(reversed(timeline))
    try:
        compute_correlation_series(
            events,
            reversed_timeline,
            window=120.0,
            tau=60.0,
            min_points=1,
        )
    except ValueError as exc:
        assert "timeline" in str(exc)
    else:  # pragma: no cover - defensive in case the guard regresses
        raise AssertionError("expected ValueError for non-monotonic timeline")
