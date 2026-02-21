# Published Run Logs

These are the actual artifacts from the preregistered T4 CEG experiment (2025-11-04).

## assisted_echo_run.json

Full run output from `run_assisted_echo()`. Contains:

- `ceg_summary` — per-λ aggregate: `{median, mean, n}`
- `gate_ledger_per_seed` — 12 entries, each with G1–G4 gate results
- `gate_ledger_summary` — aggregate pass rates (all 100%)
- `per_seed` — full per-seed baseline/assisted errors, work summaries, telemetry
- `telemetry_rows` — per-step traces (forward, baseline, assisted)

## ceg_summary.csv

| lambda | median_ceg | mean_ceg | n |
|--------|-----------|---------|---|
| 0      | 0.0       | 0.0     | 12 |
| 0.1    | 0.01246   | 0.01211 | 12 |
| 0.2    | 0.02369   | 0.02346 | 12 |
| 0.3    | 0.03466   | 0.03425 | 12 |
| 0.5    | 0.05455   | 0.05378 | 12 |

## Gate Results (from the JSON)

- **G1 (Noether J-drift)**: ALL PASS — max drift = 4.6e-17 (tol: 1.6e-11)
- **G2 (H-theorem)**: ALL PASS — all delta_sigma_min > 0
- **G3 (Energy match)**: ALL PASS — max rel_diff = 1.4e-16 (tol: 1e-4)
- **G4 (Strang defect)**: ALL PASS — R² ≥ 0.99997, slope ≈ 2.94
- **G5 (CEG positive)**: PASS — median_max = 0.0546 ≥ 0.05

## Original Filenames

- `20251104_123411_assisted_echo__assisted-echo-t4-prereg-v1c.json`
- `20251104_123412_assisted_echo_ceg_summary__assisted-echo-t4-prereg-v1c.csv`

## Provenance

- Commit: `c63d13f3de38483f867219b1d2ef10330fca7156`
- Spec: `assisted_echo.v1c.json` (N=256, dx=1.0, dt=0.02, seeds=12, λ∈{0, 0.1, 0.2, 0.3, 0.5}, budget=1e-2)
