from __future__ import annotations
from pathlib import Path
from typing import Tuple, Dict, Any
import json
import math

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from common.io_paths import figure_path


def apply_style(style: str = "light") -> None:
    if style == "dark":
        plt.style.use("dark_background")
    else:
        plt.style.use("default")
    plt.rcParams.update({
        "figure.dpi": 100,
        "savefig.dpi": 160,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "font.size": 11,
    })


def get_fig_ax(size=(6.4, 4.0)) -> Tuple[Figure, Axes]:
    fig, ax = plt.subplots(figsize=size)
    return fig, ax


def sanitize_for_log(arr):
    # Avoid log(<=0)
    import numpy as np
    a = np.asarray(arr)
    eps = 1e-30
    return np.where(a <= 0, eps, a)


def save_figure(domain: str, slug: str, fig: Figure, *, failed: bool) -> Path:
    path = figure_path(domain, slug, failed=failed)
    fig.savefig(path, bbox_inches="tight")
    return path


def write_sidecar(path: Path, spec: Dict[str, Any], stats: Dict[str, Any]) -> None:
    sidecar = path.with_suffix(".json")
    payload = {"plot": spec, "stats": stats}
    sidecar.write_text(json.dumps(payload, indent=2), encoding="utf-8")
