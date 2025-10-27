#!/usr/bin/env python3
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.

PTA-band correlation proxy harness for the cosmology router."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable, List, Sequence, Tuple

_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from fum_rt.core.cosmology import HorizonActivityEvent  # noqa: E402
from fum_rt.physics.harness_logging import (  # noqa: E402
    enrich_payload,
    hash_file,
    hash_jsonable,
)
from fum_rt.physics.vacuum_demographics_harness import (  # noqa: E402
    TimelinePoint,
    load_horizon_tape,
)


@dataclass(frozen=True)
class CorrelationConfig:
    """Immutable snapshot of PTA correlation harness parameters."""

    window: float
    tau: float
    min_points: int

    def as_dict(self) -> dict:
        return {
            "window": self.window,
            "tau": self.tau,
            "min_points": self.min_points,
        }


@dataclass(frozen=True)
class CorrelationSample:
    """Single correlation measurement evaluated at a timeline point."""

    time_myr: float
    redshift: float
    correlation: float
    contributing_events: int


def _ensure_monotonic_timeline(timeline: Sequence[TimelinePoint]) -> None:
    previous = None
    for point in timeline:
        if previous is not None and point.t_myr < previous:
            raise ValueError("timeline must be non-decreasing in cosmic time")
        previous = point.t_myr


def _event_local_span(event: HorizonActivityEvent, window: float) -> float:
    return max(0.0, min(window, float(event.dt_ret)))


def _active_event_stream(
    events: Sequence[HorizonActivityEvent],
    timeline: Sequence[TimelinePoint],
    window: float,
) -> Iterable[Tuple[TimelinePoint, List[Tuple[HorizonActivityEvent, float]]]]:
    sorted_events = sorted(events, key=lambda e: e.t)
    active: Deque[HorizonActivityEvent] = deque()
    event_idx = 0
    for point in timeline:
        current_time = float(point.t_myr)
        while event_idx < len(sorted_events) and sorted_events[event_idx].t <= current_time:
            active.append(sorted_events[event_idx])
            event_idx += 1
        while active and current_time - float(active[0].t) > _event_local_span(active[0], window):
            active.popleft()
        contributions: List[Tuple[HorizonActivityEvent, float]] = []
        for event in active:
            dt = current_time - float(event.t)
            if dt < -1e-9:
                raise ValueError("correlation evaluation encountered future event")
            local_span = _event_local_span(event, window)
            if dt <= local_span:
                contributions.append((event, dt))
        yield point, contributions


def compute_correlation_series(
    events: Sequence[HorizonActivityEvent],
    timeline: Sequence[TimelinePoint],
    *,
    window: float,
    tau: float,
    min_points: int,
) -> List[CorrelationSample]:
    if window <= 0.0:
        raise ValueError("window must be positive")
    if tau <= 0.0:
        raise ValueError("tau must be positive")
    if min_points < 1:
        raise ValueError("min_points must be at least 1")
    _ensure_monotonic_timeline(timeline)
    samples: List[CorrelationSample] = []
    decay = max(tau, 1e-9)
    for point, contributions in _active_event_stream(events, timeline, window):
        weights_sum = 0.0
        weighted_mean = 0.0
        weighted_values: List[Tuple[float, float]] = []
        for event, dt in contributions:
            weight = math.exp(-dt / decay)
            weights_sum += weight
            weighted_mean += weight * float(event.dotA)
            weighted_values.append((weight, float(event.dotA)))
        if weights_sum <= 0.0 or len(weighted_values) < min_points:
            correlation = 0.0
        else:
            mean = weighted_mean / weights_sum
            variance = sum(w * (value - mean) ** 2 for w, value in weighted_values) / weights_sum
            correlation = variance
        samples.append(
            CorrelationSample(
                time_myr=float(point.t_myr),
                redshift=float(point.redshift),
                correlation=correlation,
                contributing_events=len(weighted_values),
            )
        )
    return samples


def evaluate_series(samples: Sequence[CorrelationSample], *, min_coverage: float) -> Tuple[str, dict]:
    if not samples:
        return "NEEDS_RECAL", {"reason": "no timeline samples provided"}
    total = len(samples)
    supported = sum(1 for sample in samples if sample.contributing_events > 0)
    sufficient = sum(1 for sample in samples if sample.contributing_events >= 2)
    max_corr = max(sample.correlation for sample in samples)
    mean_corr = sum(sample.correlation for sample in samples) / total
    coverage = supported / total if total else 0.0
    strong_coverage = sufficient / total if total else 0.0
    status = "PASS" if strong_coverage >= min_coverage else "NEEDS_RECAL"
    metrics = {
        "status": status,
        "coverage": coverage,
        "strong_coverage": strong_coverage,
        "min_required": min_coverage,
        "max_correlation": max_corr,
        "mean_correlation": mean_corr,
        "samples": total,
    }
    return status, metrics


def build_payload(
    *,
    config: CorrelationConfig,
    samples: Sequence[CorrelationSample],
    metrics: dict,
    figure_path: str | None,
) -> dict:
    table = [
        {
            "t_myr": sample.time_myr,
            "redshift": sample.redshift,
            "correlation": sample.correlation,
            "contributing_events": sample.contributing_events,
        }
        for sample in samples
    ]
    payload = {
        "config": config.as_dict(),
        "metrics": metrics,
        "timeline": table,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    if figure_path:
        payload.setdefault("outputs", {})
        payload["outputs"]["figure"] = figure_path
    return payload


def render_correlation_figure(samples: Sequence[CorrelationSample], figure_path: str, *, status: str) -> None:
    if not figure_path:
        return
    os.makedirs(os.path.dirname(os.path.abspath(figure_path)), exist_ok=True)
    import matplotlib

    matplotlib.use("Agg", force=True)
    import matplotlib.pyplot as plt  # type: ignore

    zs = [sample.redshift for sample in samples]
    corr = [sample.correlation for sample in samples]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(zs, corr, marker="o", linestyle="-", color="tab:purple", label="PTA correlation proxy")
    ax.set_xlabel("Redshift z")
    ax.set_ylabel("Variance proxy")
    ax.set_title(f"PTA-band correlation ({status})")
    ax.invert_xaxis()
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(figure_path, dpi=150)
    plt.close(fig)


def evaluate_pta_correlation(
    events: Sequence[HorizonActivityEvent],
    timeline: Sequence[TimelinePoint],
    config: CorrelationConfig,
    *,
    figure_path: str | None = None,
    min_coverage: float = 0.6,
) -> dict:
    samples = compute_correlation_series(
        events,
        timeline,
        window=config.window,
        tau=config.tau,
        min_points=config.min_points,
    )
    status, metrics = evaluate_series(samples, min_coverage=min_coverage)
    if figure_path:
        render_correlation_figure(samples, figure_path, status=status)
    payload = build_payload(
        config=config,
        samples=samples,
        metrics=metrics,
        figure_path=figure_path,
    )
    payload["metrics"]["status"] = status
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="PTA-band correlation proxy harness")
    parser.add_argument("--tape", type=str, default="synthetic", help="path to JSON tape payload or 'synthetic'")
    parser.add_argument("--window", type=float, default=120.0, help="local correlation window (Myr)")
    parser.add_argument("--tau", type=float, default=60.0, help="exponential decay scale (Myr)")
    parser.add_argument("--min-points", type=int, default=2, help="minimum contributing events required for a variance sample")
    parser.add_argument("--coverage", type=float, default=0.6, help="minimum fraction of samples with >=min-points events")
    parser.add_argument("--outdir", type=str, default=None, help="base output directory")
    parser.add_argument("--figure", type=str, default=None, help="override figure path")
    parser.add_argument("--log", type=str, default=None, help="override JSON log path")
    args = parser.parse_args()

    events, timeline = load_horizon_tape(args.tape)
    config = CorrelationConfig(window=args.window, tau=args.tau, min_points=args.min_points)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    timestamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    default_base = os.path.abspath(os.path.join(os.path.dirname(__file__), "outputs"))
    base_outdir = os.path.abspath(args.outdir) if args.outdir else default_base
    fig_dir = os.path.join(base_outdir, "figures")
    log_dir = os.path.join(base_outdir, "logs")
    os.makedirs(fig_dir, exist_ok=True)
    os.makedirs(log_dir, exist_ok=True)
    figure_path = args.figure if args.figure else os.path.join(fig_dir, f"{script_name}_{timestamp}.png")
    log_path = args.log if args.log else os.path.join(log_dir, f"{script_name}_{timestamp}.json")

    payload = evaluate_pta_correlation(
        events,
        timeline,
        config,
        figure_path=figure_path,
        min_coverage=args.coverage,
    )

    tape_descriptor = {
        "events": [
            {
                "t": event.t,
                "x": list(event.x),
                "dotA": event.dotA,
                "horizon_id": event.horizon_id,
                "dt_ret": event.dt_ret,
            }
            for event in events
        ],
        "timeline": [
            {"t_myr": point.t_myr, "redshift": point.redshift}
            for point in timeline
        ],
    }
    hashes = {"horizon_tape": hash_jsonable(tape_descriptor)}
    if args.tape and args.tape != "synthetic":
        hashes["tape_file"] = hash_file(os.path.abspath(args.tape))

    metrics = payload.get("metrics", {})
    min_required = metrics.get("min_required", args.coverage)
    gates = {
        "strong_coverage": metrics.get("strong_coverage", 0.0) >= min_required,
        "timeline_nonempty": bool(payload.get("timeline")),
    }
    seeds = {
        "tape": "synthetic_fixed"
        if not args.tape or args.tape == "synthetic"
        else "external",
    }

    payload = enrich_payload(
        payload,
        script_name=script_name,
        gates=gates,
        seeds=seeds,
        hashes=hashes,
        outputs={
            "figure": os.path.abspath(figure_path),
            "log": os.path.abspath(log_path),
        },
        inputs={
            "tape": args.tape or "synthetic",
            "window_myr": args.window,
            "tau_myr": args.tau,
            "min_points": args.min_points,
            "coverage_gate": args.coverage,
        },
    )

    with open(log_path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)

    summary = {
        "log": payload["outputs"].get("log"),
        "figure": payload["outputs"].get("figure"),
        "status": payload["metrics"].get("status"),
        "gates": payload["gates"],
        "strong_coverage": payload["metrics"].get("strong_coverage", 0.0),
        "samples": payload["metrics"].get("samples", 0),
        "all_passed": payload["gate_summary"].get("all_passed", False),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
