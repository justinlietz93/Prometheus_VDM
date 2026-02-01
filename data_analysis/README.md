# Data analysis results (organized)

This folder contains analysis outputs intended to be easy to browse and cite.

## Top-level layout

- `tables/` — Primary tabular outputs (CSVs) grouped by analysis family.
- `figures/` — Plots (PNGs) grouped by analysis family.
- `interactive/` — Interactive artifacts (e.g., HTML) grouped by analysis family.
- `metadata/` — Non-tabular metadata (e.g., JSON summaries).
- `bundles/` — Zipped result bundles (typically multi-file exports).

Subprojects kept independent:

- `consciousness_metrics/` — Consciousness-metric dashboard outputs and bundles.
- `regime_analysis/` — Regime-related tables and bundles.
- `vdm_scale_free_1k_analysis/` — Standalone scale-free / heavy-tail / Gini analysis (kept separate because it contains key breakthrough results).

## Where to look first

- If you want *numbers to reproduce plots*: start in `tables/`.
- If you want *final visuals to cite*: start in `figures/`.
- If you want *interactive exploration*: start in `interactive/`.
- If you received a single ZIP from someone: check `bundles/`.

## Provenance / audit

- `PROVENANCE_index.json` — recursively lists every file under `data_analysis/` with SHA256, size, and timestamps for integrity checks.

Regenerate the index (overwrites `PROVENANCE_index.json`):

```bash
python data_analysis/build_provenance_index.py
```

## Folder conventions

Across folders we use consistent substructure when it helps:

- `tables/` contains analysis-family subfolders (e.g., `granger/`, `macro_state/`, `ticks/`).
- `figures/` mirrors the same analysis-family grouping.

Inside the independent subprojects:

- `consciousness_metrics/`
	- `tables/` — dashboard-by-epoch CSVs
	- `figures/` — heatmaps/summary plots
	- `bundles/` — packaged suites/atlases

- `regime_analysis/`
	- `tables/` — regime CSVs
	- `bundles/` — packaged regime analyses

- `vdm_scale_free_1k_analysis/`
	- `scripts/` — runnable Python scripts used for analysis
	- `tables/` — CCDF, tail-fit grids, Gini metrics, etc.
	- `figures/` — Lorenz/CCDF/rank plots and fit diagnostics
	- `metadata/` — JSON provenance/summaries
	- `README.md` / `RESULTS_*.md` — narrative summary and results notes

## Naming conventions (informal)

- Files are typically prefixed by the analysis family (e.g., `granger_*`, `macro_state_*`, `mip_*`, `predictive_MI_*`).
- Epoch-specific outputs include `E1`, `E2`, `E3` in the filename.
