# Data Files

## assisted-echo-t4-prereg-v1c.json
Machine-readable run log containing:
- `ceg_summary`: median/mean CEG per λ value
- `gate_ledger_per_seed`: per-seed gate outcomes (G1–G4)
- `dt`, `grid`, `params`: experiment configuration

## ceg_summary.csv
| Column | Description |
|--------|-------------|
| lambda | Assistance strength (0 = baseline, 0.5 = max tested) |
| median_ceg | Median CEG across 12 seeds |
| mean_ceg | Mean CEG across 12 seeds |
| n | Number of seeds |
