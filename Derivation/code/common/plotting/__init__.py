"""Generic plotting helpers for VDM experiments.

Usage examples:
    from common.plotting import PlotSpec, plot_line
    fig_path, (fig, ax) = plot_line(x, y, PlotSpec(domain="metriplectic", tag="KG-dispersion-v1", name="dispersion", xlabel="k [1/m]", ylabel="ω [rad/s]", title="KG dispersion"))

This package routes saves via common.io_paths so quarantine/approval is honored automatically (based on env policy).
"""

from .types import PlotSpec
from .helpers import plot_line, plot_scatter, plot_image, plot_heatmap, plot_multi_panel
