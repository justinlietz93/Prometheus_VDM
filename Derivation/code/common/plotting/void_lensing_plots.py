from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, Sequence, Tuple

import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle


def plot_void_lensing_mocks_grid_profiles(
    all_runs: Sequence[Mapping[str, Any]],
    parameters: Mapping[str, Any],
    out_path: Path,
) -> None:
    """
    Render κ(x) overlays for representative synthetic void-lensing mocks
    across a (backend, z_bin) grid.

    Color encodes backend; marker encodes z-bin.
    The output path is expected to be produced by common.io_paths.figure_path.
    """
    if not all_runs:
        return

    # Group first representative run for each (backend, z_bin) cell.
    groups: Dict[Tuple[str, Tuple[float, float]], Mapping[str, Any]] = {}
    for run in all_runs:
        config = run.get("config", {})
        metrics = run.get("metrics", {})

        backend = str(metrics.get("backend", config.get("backend", "UNKNOWN")))
        z_bin = metrics.get("z_bin", config.get("z_bin", [0.0, 0.0]))
        z_list = list(z_bin)
        if len(z_list) < 2:
            z_list = (z_list + [0.0, 0.0])[:2]
        z_min, z_max = float(z_list[0]), float(z_list[1])

        key = (backend, (z_min, z_max))
        if key not in groups:
            groups[key] = run

    if not groups:
        return

    x_wall_range = parameters.get("x_wall_range", [0.8, 1.2])
    x_bg_range = parameters.get("x_bg_range", [2.5, 4.0])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))

    # Build deterministic mappings: backend → color, z-bin → marker.
    unique_backends = sorted({backend for backend, _ in groups.keys()})
    unique_z_bins = sorted({zb for _, zb in groups.keys()}, key=lambda zb: zb[0])

    default_colors = plt.rcParams.get("axes.prop_cycle", None)
    if default_colors is not None:
        color_list = default_colors.by_key().get("color", ["C0", "C1", "C2", "C3"])
    else:
        color_list = ["C0", "C1", "C2", "C3"]
    color_cycle = cycle(color_list)
    backend_colors: Dict[str, str] = {}
    for backend in unique_backends:
        backend_colors[backend] = next(color_cycle)

    marker_sequence = ["o", "s", "^", "D", "v", "P", "X"]
    marker_cycle = cycle(marker_sequence)
    zbin_markers: Dict[Tuple[float, float], str] = {}
    for zb in unique_z_bins:
        zbin_markers[zb] = next(marker_cycle)

    # Deterministic ordering by backend then z_min.
    for (backend, (z_min, z_max)), run in sorted(
        groups.items(), key=lambda kv: (kv[0][0], kv[0][1][0])
    ):
        metrics = run.get("metrics", {})
        profile = metrics.get("profile", {})

        x = np.asarray(profile.get("x", []), dtype=float)
        kappa = np.asarray(profile.get("kappa", []), dtype=float)
        kappa_err = np.asarray(profile.get("kappa_err", []), dtype=float)
        if x.size == 0 or kappa.size == 0:
            continue

        color = backend_colors.get(backend, "C0")
        marker = zbin_markers.get((z_min, z_max), "o")
        label = f"{backend}, z=[{z_min:.2f},{z_max:.2f}]"
        ax.errorbar(
            x,
            kappa,
            yerr=kappa_err,
            fmt=marker,
            color=color,
            ms=3,
            alpha=0.8,
            label=label,
        )

    # Wall and background regions behind the data.
    ax.axvspan(
        x_wall_range[0],
        x_wall_range[1],
        color="#cccccc",
        alpha=0.2,
        label="wall fit region",
        zorder=0,
    )
    ax.axvspan(
        x_bg_range[0],
        x_bg_range[1],
        color="#eeeeee",
        alpha=0.2,
        label="background region",
        zorder=0,
    )

    ax.set_xlabel("x = r / R_v")
    ax.set_ylabel("κ(x)")
    ax.set_title("Synthetic void-lensing profiles across backend/z-bin grid")
    ax.legend(loc="best", fontsize=7)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)