# -*- coding: utf-8 -*-
"""
VDM Common Plotting Helpers

Purpose
- Provide reusable plotting utilities for notebooks and runners.
- Save artifacts and logs via canonical io_paths routing.
- Avoid heavy dependencies; rely on matplotlib and stdlib.

Artifacts
- Figures: Derivation/code/outputs/figures/{domain}/[failed_runs/]{timestamp}_{slug}.{ext}
- Logs:    Derivation/code/outputs/logs/{domain}/[failed_runs/]{timestamp}_{slug}.{json|csv}

Usage (in notebooks)
- Ensure repository root is on sys.path, then:

    from Derivation.code.common.plotting import setup_style, plot_time_series, heatmap, animate_lines, save_csv_table, save_json_log

Compliance
- JSON: indent=2, sort_keys=True
- CSV: writeheader() then rows
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence, Mapping, Any, Optional
import json
import csv

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.figure import Figure
from matplotlib.axes import Axes

# Canonical IO helpers
# Prefer the runtime "common" package path; fall back to local io_paths for direct execution.
try:
    from common.io_paths import (
        figure_path_ext,
        media_path,
        log_path,
    )
except Exception:  # pragma: no cover - notebook / ad-hoc fallback
    import sys as _sys
    from pathlib import Path as _Path
    _sys.path.append(str(_Path(__file__).resolve().parents[1]))
    from io_paths import (  # type: ignore
        figure_path_ext,
        media_path,
        log_path,
    )

def setup_style(context: str = "paper") -> None:
    """
    Configure a consistent matplotlib style.

    context: "paper" | "talk" | "notebook"
    """
    base = {
        "figure.dpi": 140,
        "savefig.dpi": 140,
        "axes.grid": True,
        "grid.linestyle": ":",
        "grid.alpha": 0.4,
        "axes.titlesize": "medium",
        "axes.labelsize": "medium",
        "legend.frameon": False,
        "legend.fontsize": "small",
        "font.size": 11.0,
        "lines.linewidth": 1.6,
        "lines.markersize": 4.5,
    }
    if context == "talk":
        base.update({
            "font.size": 13.0,
            "axes.titlesize": "large",
            "axes.labelsize": "large",
            "lines.linewidth": 2.2,
        })
    elif context == "notebook":
        base.update({
            "font.size": 12.0,
        })
    mpl.rcParams.update(base)


def save_fig(fig: Figure, domain: str, slug: str, ext: str = "png", failed: bool = False) -> Path:
    """
    Save a matplotlib figure using canonical routing.
    Returns the saved Path.
    """
    path = figure_path_ext(domain, slug, ext=ext, failed=failed)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    return path


def plot_time_series(
    t: np.ndarray,
    ys: Sequence[np.ndarray],
    labels: Optional[Sequence[str]] = None,
    xlabel: str = "t",
    ylabel: str = "",
    title: str = "",
    domain: str = "metriplectic",
    slug: str = "timeseries",
    failed: bool = False,
) -> Path:
    """
    Plot one or more time series y_i(t) and save a PNG.
    Returns the saved Path.
    """
    setup_style("paper")
    fig, ax = plt.subplots()
    if labels is None:
        labels = [f"s{i}" for i in range(len(ys))]
    for y, lab in zip(ys, labels):
        ax.plot(t, y, label=lab)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    if labels:
        ax.legend()
    p = save_fig(fig, domain, slug, ext="png", failed=failed)
    plt.close(fig)
    return p


def heatmap(
    Z: np.ndarray,
    xlabel: str = "",
    ylabel: str = "",
    title: str = "",
    cmap: str = "viridis",
    colorbar_label: Optional[str] = None,
    domain: str = "metriplectic",
    slug: str = "heatmap",
    failed: bool = False,
) -> Path:
    """
    Render a matrix heatmap and save a PNG.
    Returns the saved Path.
    """
    setup_style("paper")
    fig, ax = plt.subplots()
    im = ax.imshow(Z, aspect="auto", origin="lower", cmap=cmap)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    cbar = fig.colorbar(im, ax=ax)
    if colorbar_label:
        cbar.set_label(colorbar_label)
    p = save_fig(fig, domain, slug, ext="png", failed=failed)
    plt.close(fig)
    return p


def save_csv_table(
    rows: Sequence[Mapping[str, Any]],
    domain: str,
    slug: str,
    failed: bool = False,
) -> Path:
    """
    Write a CSV table with canonical routing. Returns the saved Path.

    rows: sequence of dict-like objects. Fieldnames = union of keys across rows (sorted).
    """
    path = log_path(domain, slug, failed=failed, type="csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    # Union of keys across rows
    fieldnames: list[str] = sorted({k for r in rows for k in r.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})
    return path


def save_json_log(
    data: Mapping[str, Any],
    domain: str,
    slug: str,
    failed: bool = False,
) -> Path:
    """
    Write a JSON log (indent=2, sort_keys=True). Returns the saved Path.
    """
    path = log_path(domain, slug, failed=failed, type="json")
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    return path


def animate_lines(
    t: np.ndarray,
    y_series: Sequence[np.ndarray],
    labels: Optional[Sequence[str]] = None,
    xlabel: str = "t",
    ylabel: str = "",
    title: str = "",
    fps: int = 20,
    domain: str = "metriplectic",
    slug: str = "animation",
    failed: bool = False,
) -> Path:
    """
    Create a simple line animation y_i(t) and save as GIF via Pillow writer.
    Returns the saved Path.
    """
    setup_style("paper")
    fig, ax = plt.subplots()
    if labels is None:
        labels = [f"s{i}" for i in range(len(y_series))]
    lines = [ax.plot([], [], label=lab)[0] for lab in labels]

    # Axis limits
    t_min = float(np.nanmin(t)) if len(t) else 0.0
    t_max = float(np.nanmax(t)) if len(t) else 1.0
    y_min = float(np.nanmin([np.nanmin(y) for y in y_series])) if y_series else -1.0
    y_max = float(np.nanmax([np.nanmax(y) for y in y_series])) if y_series else 1.0
    pad = 0.05 * (y_max - y_min + 1e-12)
    ax.set_xlim(t_min, t_max)
    ax.set_ylim(y_min - pad, y_max + pad)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend()

    def init():
        for ln in lines:
            ln.set_data([], [])
        return lines

    def update(i: int):
        ti = t[: i + 1]
        for ln, y in zip(lines, y_series):
            ln.set_data(ti, y[: i + 1])
        return lines

    frames = int(len(t))
    interval_ms = int(1000 / max(1, fps))
    anim = FuncAnimation(fig, update, init_func=init, frames=frames, interval=interval_ms, blit=True)
    p = media_path(domain, slug, ext="gif", failed=failed)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        writer = PillowWriter(fps=fps)
        anim.save(str(p), writer=writer)
    finally:
        plt.close(fig)
    return p


__all__ = [
    "setup_style",
    "save_fig",
    "plot_time_series",
    "heatmap",
    "save_csv_table",
    "save_json_log",
    "animate_lines",
]
