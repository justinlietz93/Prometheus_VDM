# VDM 1000-neuron scale-free / heavy-tail / Gini analysis (reproducible)

**Input:** `1000_neurons_events.zip`

This run window (from `events.jsonl` timestamps) is:
- start UTC: `2025-08-15T13:11:01.988265Z`
- end UTC: `2025-08-16T10:07:28.290496Z`

Hashes (anti-tamper anchors):
- zip sha256: `78083cddfc9b849c6131541f3e928a77036a5d7066a9a490d8f3e15444857d74`
- state_394860.h5 sha256: `e637892e51ef7b3c1fd3fdb1c1cc919de1946960510f7e96f20975bd049d3827`
- events.jsonl sha256: `83b0705f1829f25638c24099384061199797e6f6804fb8a78d15b49f33913585`
- utd_events.jsonl sha256: `a7043249bced1a0be35bb90293f0ceead30b9c5d41263356ef26de3589c740cf`

## Outputs

This folder is intentionally kept **separate** because it contains key results (Gini + heavy-tail fingerprints).

Organized layout:

- `scripts/` — runnable analysis scripts
- `tables/` — CSV outputs (CCDFs, tail-fit grids/summaries, Gini metrics)
- `figures/` — PNG plots (CCDF/rank/Lorenz, fit diagnostics)
- `metadata/` — JSON provenance/summaries

Key outputs (now located under `tables/` / `figures/`):

- `tables/tail_fit_summary_degrees.csv`: best tail fit for out/in/total degree
- `tables/tail_fit_grid_*.csv`: scan over xmin (for transparency)
- `figures/*_ccdf_loglog.png`, `figures/*_rank_loglog.png`, `figures/*_lorenz.png`
- `figures/out_degree_ccdf_with_tail_fit.png`: CCDF with fitted tail overlay

## Reproduce
```bash
python run_scale_free_analysis_1k.py --zip 1000_neurons_events.zip --outdir out_scale_free --n_boot 500 --seed 0
```
