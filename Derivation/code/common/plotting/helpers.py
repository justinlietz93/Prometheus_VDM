from __future__ import annotations
from typing import Sequence, Callable, Optional, Tuple, Dict, Any, List
import numpy as np
import matplotlib.pyplot as plt

from .types import PlotSpec
from .core import apply_style, get_fig_ax, save_figure, write_sidecar, sanitize_for_log
from common.io_paths import build_slug


def _slug(spec: PlotSpec) -> str:
    return build_slug(spec.name, spec.tag)


def _stats_xy(x: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    return {
        "x": {"shape": list(x.shape), "min": float(np.nanmin(x)), "max": float(np.nanmax(x))},
        "y": {"shape": list(y.shape), "min": float(np.nanmin(y)), "max": float(np.nanmax(y))},
    }


def plot_line(x: Sequence[float], y: Sequence[float], spec: PlotSpec, *, failed: bool = False):
    apply_style(spec.style)
    fig, ax = get_fig_ax(spec.size)

    x_arr = np.asarray(x)
    y_arr = np.asarray(y)

    if spec.logx:
        x_arr = sanitize_for_log(x_arr)
        ax.set_xscale("log")
    if spec.logy:
        y_arr = sanitize_for_log(y_arr)
        ax.set_yscale("log")

    ax.plot(x_arr, y_arr, label=spec.title or spec.name)

    if spec.title:
        ax.set_title(spec.title)
    if spec.xlabel:
        ax.set_xlabel(spec.xlabel)
    if spec.ylabel:
        ax.set_ylabel(spec.ylabel)
    if spec.legend:
        ax.legend()

    if spec.tight:
        fig.tight_layout()

    path = save_figure(spec.domain, _slug(spec), fig, failed=failed)
    write_sidecar(path, spec.__dict__, _stats_xy(x_arr, y_arr))
    return path, (fig, ax)


def plot_scatter(x: Sequence[float], y: Sequence[float], spec: PlotSpec, *, failed: bool = False):
    apply_style(spec.style)
    fig, ax = get_fig_ax(spec.size)

    x_arr = np.asarray(x)
    y_arr = np.asarray(y)
    ax.scatter(x_arr, y_arr, s=10, alpha=0.8)

    if spec.title:
        ax.set_title(spec.title)
    if spec.xlabel:
        ax.set_xlabel(spec.xlabel)
    if spec.ylabel:
        ax.set_ylabel(spec.ylabel)

    if spec.tight:
        fig.tight_layout()

    path = save_figure(spec.domain, _slug(spec), fig, failed=failed)
    write_sidecar(path, spec.__dict__, _stats_xy(x_arr, y_arr))
    return path, (fig, ax)


essential_cmaps = {"viridis", "plasma", "inferno", "magma", "cividis"}


def plot_image(img2d: np.ndarray, spec: PlotSpec, *, failed: bool = False):
    apply_style(spec.style)
    fig, ax = get_fig_ax(spec.size)

    im = ax.imshow(img2d, cmap=spec.cmap, origin="lower", aspect="auto")
    plt.colorbar(im, ax=ax)

    if spec.title:
        ax.set_title(spec.title)
    if spec.xlabel:
        ax.set_xlabel(spec.xlabel)
    if spec.ylabel:
        ax.set_ylabel(spec.ylabel)

    if spec.tight:
        fig.tight_layout()

    path = save_figure(spec.domain, _slug(spec), fig, failed=failed)
    stats = {"img": {"shape": list(img2d.shape), "min": float(np.nanmin(img2d)), "max": float(np.nanmax(img2d))}}
    write_sidecar(path, spec.__dict__, stats)
    return path, (fig, ax)


def plot_heatmap(X: np.ndarray, Y: np.ndarray, Z: np.ndarray, spec: PlotSpec, *, failed: bool = False):
    apply_style(spec.style)
    fig, ax = get_fig_ax(spec.size)

    pc = ax.pcolormesh(X, Y, Z, cmap=spec.cmap, shading="auto")
    plt.colorbar(pc, ax=ax)

    if spec.title:
        ax.set_title(spec.title)
    if spec.xlabel:
        ax.set_xlabel(spec.xlabel)
    if spec.ylabel:
        ax.set_ylabel(spec.ylabel)

    if spec.tight:
        fig.tight_layout()

    path = save_figure(spec.domain, _slug(spec), fig, failed=failed)
    stats = {
        "X": {"shape": list(X.shape), "min": float(np.nanmin(X)), "max": float(np.nanmax(X))},
        "Y": {"shape": list(Y.shape), "min": float(np.nanmin(Y)), "max": float(np.nanmax(Y))},
        "Z": {"shape": list(Z.shape), "min": float(np.nanmin(Z)), "max": float(np.nanmax(Z))},
    }
    write_sidecar(path, spec.__dict__, stats)
    return path, (fig, ax)


def plot_multi_panel(panels: List[Callable[[plt.Axes], None]], spec: PlotSpec, *, failed: bool = False, ncols: int = 2):
    apply_style(spec.style)
    import math
    n = len(panels)
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=spec.size)
    axes = np.array(axes).reshape(-1)

    for i, panel in enumerate(panels):
        ax = axes[i]
        panel(ax)

    # Hide any unused axes
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    if spec.title:
        fig.suptitle(spec.title)

    if spec.tight:
        fig.tight_layout()

    path = save_figure(spec.domain, _slug(spec), fig, failed=failed)
    write_sidecar(path, spec.__dict__, {"panels": n})
    return path, (fig, axes)
