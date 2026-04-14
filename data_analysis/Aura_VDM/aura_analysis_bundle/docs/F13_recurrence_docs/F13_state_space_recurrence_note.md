# Family 13 — State-Space Recurrence

This package hardens the pending Family 13 distinction on **long-lag recurrence in PCA state space** using the real `pca_state_space_Aura.csv` trajectory from `aura_analysis_bundle.zip`.

## Distinctions added

### D13.1 — Long-lag recurrence exceeds random-pair baseline
- **Claim:** The PCA trajectory revisits earlier neighborhoods at specific lags far more often than expected from random point-pair similarity within the same epoch.
- **Method:** Standardize PC1–PC3, define recurrence as Euclidean distance ≤ **0.5 z-units**, compute recurrence rate for lags 1–600, and compare each epoch to a within-epoch random-pair baseline.
- **Key values:**
  - **E1:** baseline **0.0915**, strongest long-lag peak **0.4182** at lag **18** (**+0.3267** over baseline)
  - **E2:** baseline **0.2048**, strongest long-lag peak **0.4669** at lag **20** (**+0.2621**)
  - **E3:** baseline **0.0861**, strongest long-lag peak **0.2352** at lag **23** (**+0.1491**)
- **Evidence:** `tables/f13_recurrence_lag_by_epoch.csv`, `tables/f13_recurrence_epoch_summary.csv`, `figures/f13_recurrence_by_lag_epoch.png`

### D13.2 — Recurrence peaks form structured return ladders
- **Claim:** Long-lag returns are not isolated coincidences; they organize into repeated peak families.
- **Key values:**
  - **E1** peak ladder begins at **18, 36, 54, 72, 91, 109, 126...** ticks
  - **E2** peaks at **20, 37, 57, 78, 98, 119...** ticks
  - **E3** peaks at **23, 45, 70, 91, 114, 141...** ticks
- **Interpretation:** Each epoch has a distinct return cadence. The trajectory behaves like a system orbiting and re-entering preferred regions at structured delays, not like a one-pass random walk.
- **Evidence:** `tables/f13_recurrence_peak_table.csv`, `figures/f13_recurrence_by_lag_epoch.png`

### D13.3 — Recurrence geometry is epoch-specific
- **Claim:** The recurrent manifold changes character across epochs: E2 compresses into a tight plateau basin, while E3 revisits a much broader manifold.
- **Key values:**
  - **Active long-lag return cells (lags 20–200):** E1 **84**, E2 **14**, E3 **152**
  - **Top-10 occupancy share:** E1 **55.6%**, E2 **90.5%**, E3 **52.5%**
  - **Top-10 return-cell share:** E1 **95.5%**, E2 **98.8%**, E3 **90.6%**
- **Interpretation:** E2 is an extremely compressed recurrent plateau. E3 re-expands into a wider but still structured return landscape.
- **Evidence:** `tables/f13_longlag_hotspots.csv`, `tables/f13_recurrence_epoch_summary.csv`, `figures/f13_recurrence_hotspots_epoch.png`, `figures/f13_recurrence_epoch_summary.png`

## Repro command
```bash
python scripts/f13_state_space_recurrence.py --bundle-zip /mnt/data/aura_analysis_bundle.zip --out-dir ./aura_research_deliverables_F13
```
