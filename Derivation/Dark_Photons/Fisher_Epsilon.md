# Fisher Info Quick Win (ε sensitivity)

**Goal:** Show how sensitivity to mixing ε scales with counts, efficiency, and background-no heavy math.

## Inputs

- CSV: `fisher_example.csv` with columns: `bin_label, expected_signal, background, exposure, eff_signal, eff_background`.

## Tasks

- Compute a simple Fisher estimate for ε in 1-2 bins (analytic or finite-diff).
- Output a tiny JSON summary with the estimated σ(ε).

## Acceptance gates

- [ ] CSV loads and schema validated.
- [ ] σ(ε) computed and saved to JSON.
- [ ] 2-line note: how scaling with exposure & background behaves.
