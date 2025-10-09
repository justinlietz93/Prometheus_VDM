#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Dict, Any

import numpy as np

import sys
CODE_ROOT = Path(__file__).resolve().parents[2]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.io_paths import figure_path, log_path, write_log
from memory_steering.memory_steering_experiments import run_junction_logistic


@dataclass
class A6Spec:
    tuples: List[Dict[str, Any]]  # each: {theta: float, delta_m_values: list[float], trials: int}
    tag: str = "A6-collapse-v1"


def compute_envelope(xs: List[np.ndarray], ys: List[np.ndarray], nbins: int = 101) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Interpolate multiple curves onto a common X grid (shared range) and compute min/max/envelope."""
    # Determine shared X range across all curves
    xmin = max(np.min(x) for x in xs if x.size > 0)
    xmax = min(np.max(x) for x in xs if x.size > 0)
    if not np.isfinite(xmin) or not np.isfinite(xmax) or xmax <= xmin:
        return np.array([]), np.array([]), np.array([])
    X = np.linspace(xmin, xmax, nbins)
    Ymin = np.full_like(X, np.nan, dtype=float)
    Ymax = np.full_like(X, np.nan, dtype=float)
    for i, (x, y) in enumerate(zip(xs, ys)):
        if x.size < 2:
            continue
        # ensure monotone x for interpolation
        order = np.argsort(x)
        xi = x[order]
        yi = y[order]
        yi_interp = np.interp(X, xi, yi)
        if i == 0:
            Ymin[:] = yi_interp
            Ymax[:] = yi_interp
        else:
            Ymin = np.minimum(Ymin, yi_interp)
            Ymax = np.maximum(Ymax, yi_interp)
    return X, Ymin, Ymax


def run_a6(spec: A6Spec) -> Dict[str, Any]:
    curves_x: List[np.ndarray] = []
    curves_y: List[np.ndarray] = []
    raw: List[Dict[str, Any]] = []
    for tup in spec.tuples:
        theta = float(tup.get("theta", 2.0))
        delta_m_values = np.asarray(tup.get("delta_m_values", np.linspace(-2.0, 2.0, 17)), dtype=float)
        trials = int(tup.get("trials", 2000))
        X, P = run_junction_logistic(theta=theta, delta_m_values=delta_m_values, trials=trials)
        curves_x.append(np.asarray(X, dtype=float))
        curves_y.append(np.asarray(P, dtype=float))
        raw.append({"theta": theta, "delta_m_values": delta_m_values.tolist(), "trials": trials, "X": X.tolist(), "P": P.tolist()})

    Xc, Ymin, Ymax = compute_envelope(curves_x, curves_y, nbins=121)
    if Xc.size == 0:
        raise RuntimeError("A6 collapse: unable to compute shared X range for envelope")
    envelope = Ymax - Ymin
    env_max = float(np.nanmax(envelope))
    # Gate: max envelope ≤ 0.02
    passed = bool(env_max <= 0.02)

    # Artifacts
    import matplotlib.pyplot as plt
    figp = figure_path("collapse", f"a6_collapse_overlay__{spec.tag}", failed=not passed)
    plt.figure(figsize=(6.4, 4.2))
    # Plot curves
    for X, P in zip(curves_x, curves_y):
        plt.plot(X, P, "o-", alpha=0.7)
    # Envelope band
    plt.fill_between(Xc, Ymin, Ymax, color="#1f77b4", alpha=0.15, label="envelope")
    plt.xlabel("X = Θ Δm")
    plt.ylabel("P(A)")
    plt.title(f"A6 collapse (max envelope ≈ {env_max:.3%})")
    plt.legend(loc="best", fontsize=8)
    plt.tight_layout(); plt.savefig(figp, dpi=150); plt.close()

    # CSV envelope
    csvp = log_path("collapse", f"a6_collapse_envelope__{spec.tag}", failed=not passed, type="csv")
    with csvp.open("w", encoding="utf-8") as f:
        f.write("X,Ymin,Ymax,envelope\n")
        for xi, lo, hi, en in zip(Xc, Ymin, Ymax, envelope):
            f.write(f"{xi},{lo},{hi},{en}\n")

    logj = {"spec": {"tuples": spec.tuples}, "passed": passed, "env_max": env_max, "figure": str(figp), "csv": str(csvp), "raw_curves": raw}
    write_log(log_path("collapse", f"a6_collapse__{spec.tag}", failed=not passed), logj)
    if not passed:
        write_log(log_path("collapse", f"CONTRADICTION_REPORT_a6_collapse__{spec.tag}", failed=True), {
            "reason": "A6 collapse envelope exceeded tolerance",
            "gate": {"max_envelope": "<= 0.02"},
            "metrics": {"env_max": env_max},
            "artifacts": {"figure": str(figp), "csv": str(csvp)}
        })
    return logj


def main():
    import argparse, json
    p = argparse.ArgumentParser(description="A6 scaling collapse runner (junction logistic)")
    p.add_argument("--tuples", type=str, default=None, help="JSON list of parameter tuples; if omitted, use defaults")
    args = p.parse_args()
    if args.tuples:
        tuples = json.loads(args.tuples)
    else:
        tuples = [
            {"theta": 1.5, "delta_m_values": list(np.linspace(-2.0, 2.0, 25)), "trials": 4000},
            {"theta": 2.5, "delta_m_values": list(np.linspace(-2.0, 2.0, 25)), "trials": 4000},
            {"theta": 3.5, "delta_m_values": list(np.linspace(-2.0, 2.0, 25)), "trials": 4000},
        ]
    spec = A6Spec(tuples=tuples)
    out = run_a6(spec)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
