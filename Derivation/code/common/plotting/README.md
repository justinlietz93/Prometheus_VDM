# plotting/ - generic plotting helpers

Purpose

- Provide reusable plotting functions that work across experiments.
- Route all figure saves through `common/io_paths` to honor approval/quarantine policy.

Contents

- `types.py`: `PlotSpec` dataclass with domain, name, tag, labels, style, and flags.
- `core.py`: style application, figure creation, saving, and sidecar writing.
- `helpers.py`: `plot_line`, `plot_scatter`, `plot_image`, `plot_heatmap`, `plot_multi_panel`.

Usage

- Import from experiments:
  - `from common.plotting import PlotSpec, plot_line`
  - Build `spec = PlotSpec(domain="metriplectic", name="dispersion", tag="KG-dispersion-v1", xlabel="k [1/m]", ylabel="ω [rad/s]")`
  - `path, (fig, ax) = plot_line(x, y, spec, failed=engineering_only)`

Notes

- Sidecar JSON is written alongside the PNG with plot metadata and data stats.
- Slug building (name + optional tag) is centralized via `common/io_paths.build_slug`.
- Keep domain-specific visualization logic in domain code; add small helpers here only when broadly useful.
