from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import numpy as np
import matplotlib.pyplot as plt

from .core import get_fig_ax


# Small utilities

def format_float(x: float, prec: int = 6) -> str:
    try:
        return f"{float(x):.{prec}g}"
    except Exception:
        return str(x)


# Generic figure: monotonicity with dual-axis delta overlay

def plot_monotonicity_dual_axis(
    *,
    t: Sequence[float],
    y: Sequence[float],
    dy: Sequence[float],
    checkpoints_t: Optional[Sequence[float]] = None,
    window: Optional[Tuple[float, float]] = None,
    title: str = "Monotonicity check",
    xlabel: str = "t",
    ylabel_left: str = "y(t)",
    ylabel_right: str = "Δy(t)",
    legend_labels: Tuple[str, str, str] = ("y(t)", "Δy(t)", "window"),
    callout_lines: Optional[Sequence[str]] = None,
    figsize: Tuple[float, float] = (8, 4.5),
) -> Tuple[plt.Figure, plt.Axes]:
    fig, ax = get_fig_ax(size=figsize)
    t = np.asarray(t, dtype=float)
    y = np.asarray(y, dtype=float)
    dy = np.asarray(dy, dtype=float)

    ax.plot(t, y, color="#222222", lw=1.8, label=legend_labels[0])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel_left)
    ax.grid(True, alpha=0.3)

    axr = ax.twinx()
    axr.plot(t, dy, color="#1f77b4", alpha=0.35, lw=1.0, label=legend_labels[1])
    axr.axhline(0.0, color="#1f77b4", alpha=0.25, lw=0.8)
    axr.set_ylabel(ylabel_right)

    if checkpoints_t is not None:
        for tc in checkpoints_t:
            ax.axvline(float(tc), color="#666666", alpha=0.25, lw=0.6)

    if window is not None:
        t0, t1 = window
        ax.axvspan(float(t0), float(t1), color="#ff7f0e", alpha=0.12, label=legend_labels[2])

    if callout_lines:
        ax.text(
            0.98,
            0.98,
            "\n".join(callout_lines),
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="#cccccc", alpha=0.9),
        )

    lines_left, labels_left = ax.get_legend_handles_labels()
    lines_right, labels_right = axr.get_legend_handles_labels()
    ax.legend(lines_left + lines_right, labels_left + labels_right, loc="lower left", fontsize=9)

    ax.set_title(title)
    return fig, ax


# Generic 2x2 dashboard assembler and panel primitives

def assemble_dashboard_2x2(figsize: Tuple[float, float] = (10, 7.5)) -> Tuple[plt.Figure, np.ndarray]:
    fig, axs = plt.subplots(2, 2, figsize=figsize, constrained_layout=True)
    return fig, axs


def panel_scatter_with_line(
    ax: plt.Axes,
    *,
    x: Sequence[float],
    y: Sequence[float],
    line_x: Optional[Sequence[float]] = None,
    line_y: Optional[Sequence[float]] = None,
    xlabel: str = "x",
    ylabel: str = "y",
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    residual_stats: Optional[Dict[str, Any]] = None,
):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ax.scatter(x, y, s=8, alpha=0.5, label="data")
    if line_x is not None and line_y is not None:
        ax.plot(np.asarray(line_x, dtype=float), np.asarray(line_y, dtype=float), color="#d62728", lw=1.2, label="fit")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    if title:
        tt = title
        if subtitle:
            tt += f"\n{subtitle}"
        ax.set_title(tt)
    if residual_stats:
        ax.text(
            0.02,
            0.98,
            "Res: " + ", ".join([f"{k}={format_float(v)}" for k, v in residual_stats.items()]),
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=8,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#dddddd", alpha=0.9),
        )
    ax.legend(fontsize=9)


def panel_compare_series(
    ax: plt.Axes,
    *,
    t: Sequence[float],
    series: Sequence[Sequence[float]],
    labels: Sequence[str],
    ylabel: str = "value",
    title: Optional[str] = None,
    badge_text: Optional[str] = None,
):
    t = np.asarray(t, dtype=float)
    for s, label in zip(series, labels):
        ax.plot(t, np.asarray(s, dtype=float), lw=1.2, label=label)
    ax.grid(True, alpha=0.3)
    ax.set_xlabel("t")
    ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend(fontsize=9)
    if badge_text:
        ax.text(
            0.98,
            0.05,
            badge_text,
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=9,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc", alpha=0.95),
        )


def panel_timeline_passfail(
    ax: plt.Axes,
    *,
    times: Sequence[float],
    ok: Sequence[bool],
    title: Optional[str] = None,
    xlabel: str = "t (checkpoints)",
):
    times = np.asarray(times, dtype=float)
    ok = np.asarray(ok, dtype=bool)
    for tc, is_ok in zip(times, ok):
        color = "#2ca02c" if is_ok else "#d62728"
        ax.plot([tc, tc], [0, 1], color=color, lw=1.8)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xlabel(xlabel)
    if title:
        ax.set_title(title)
    ax.grid(True, axis="x", alpha=0.3)


def panel_kv_text(
    ax: plt.Axes,
    *,
    title: str,
    lines: Sequence[str],
):
    ax.axis("off")
    ax.text(0.0, 1.0, title + "\n" + "\n".join(lines), ha="left", va="top", fontsize=9)
