#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
import re
from typing import List, Tuple

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def find_latest_ceg_csv() -> Path:
    """
    Find the latest assisted_echo CEG summary CSV for tag 'assisted-echo-t4-prereg-v1c'
    under outputs/logs/metriplectic. Falls back to a known explicit path if pattern search fails.
    """
    base = Path("Derivation/code/outputs/logs/metriplectic")
    pattern = re.compile(r"^\d{8}_\d{6}_assisted_echo_ceg_summary__assisted-echo-t4-prereg-v1c\.csv$")
    candidates: List[Path] = []
    if base.exists():
        for p in base.iterdir():
            if p.is_file() and pattern.match(p.name):
                candidates.append(p)
    if candidates:
        # filenames start with sortable timestamp YYYYMMDD_HHMMSS; lexicographic max is latest
        return sorted(candidates, key=lambda p: p.name)[-1]
    # Fallback to the known path from the successful run
    fallback = base / "20251030_194555_assisted_echo_ceg_summary__assisted-echo-t4-prereg-v1c.csv"
    return fallback


def load_ceg_series(csv_path: Path) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    lambdas: List[float] = []
    medians: List[float] = []
    means: List[float] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lam = float(row["lambda"])
                med = float(row["median_ceg"])
                mean = float(row["mean_ceg"])
            except Exception:
                # Skip malformed rows
                continue
            lambdas.append(lam)
            medians.append(med)
            means.append(mean)
    # sort by lambda
    idx = np.argsort(np.array(lambdas))
    return np.array(lambdas)[idx], np.array(medians)[idx], np.array(means)[idx]


def main() -> int:
    out_path = Path("Derivation/Metriplectic/vdm_echo_landscape_v2.png")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    csv_path = find_latest_ceg_csv()
    if not csv_path.exists():
        # Emit a minimal JSON error and return nonzero
        print(json.dumps({"error": "CSV not found", "expected": str(csv_path)}))
        return 2

    lambdas, med, mean = load_ceg_series(csv_path)
    if lambdas.size == 0:
        print(json.dumps({"error": "CSV empty or unreadable", "csv": str(csv_path)}))
        return 3

    # Gate threshold from prereg (dimensionless)
    threshold = 0.05

    # Build the conceptual landscape: CEG vs lambda
    fig, ax = plt.subplots(figsize=(7.0, 4.5), dpi=150)

    # Plot median and mean CEG
    ax.plot(lambdas, med, "o-", color="#1f77b4", label="median CEG")
    ax.plot(lambdas, mean, "s--", color="#ff7f0e", alpha=0.7, label="mean CEG")

    # Threshold line and PASS region shading
    ax.axhline(threshold, color="k", linestyle=":", linewidth=1.0, label=f"gate threshold = {threshold:.2f}")
    # Shade region above threshold to indicate PASS
    y_max = float(max(np.max(med), np.max(mean)))
    ax.fill_between([np.min(lambdas), np.max(lambdas)], threshold, max(threshold, y_max) + 0.01, color="#d0ffd0", alpha=0.4, zorder=-5)

    # Annotate points with values (compact)
    for x, y in zip(lambdas, med):
        ax.annotate(f"{y:.3f}", (x, y), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8, color="#1f77b4")

    # Axes labels and aesthetics
    ax.set_xlabel("λ (per-step assistance budget factor)")
    ax.set_ylabel("Echo Gain, CEG (dimensionless)")
    ax.set_title("VDM Assisted Echo Landscape v2: CEG vs λ (median ± mean)")
    ax.grid(True, which="both", linestyle="--", alpha=0.35)
    ax.legend(loc="lower right", frameon=True)

    # Ticks and limits
    x_pad = 0.02*(np.max(lambdas)-np.min(lambdas) if np.max(lambdas) > np.min(lambdas) else 1.0)
    ax.set_xlim(np.min(lambdas) - x_pad, np.max(lambdas) + x_pad)
    ax.set_ylim(0.0, max(0.06, y_max) + 0.01)

    fig.tight_layout()
    fig.savefig(out_path, facecolor="white")
    plt.close(fig)

    summary = {
        "figure": str(out_path),
        "csv": str(csv_path),
        "median_max": float(np.max(med)),
        "lambdas": list(map(float, lambdas.tolist()))
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())