# VDM Four-Proofs Offline Analysis Pack (structural plasticity)

This pack is **offline-only** analysis using:
- `snapshots_backup.zip` (485 `state_*.h5` snapshots, every 60 ticks; N=1000)
- scalar telemetry slices:
  - `20260204_142311.zip` (ticks ~0–8247)
  - `20260204_144053.zip` (ticks ~8264–16504)
  - `events.jsonl.zip` (ticks ~24910–29176)

It produces paper-ready figures + tables for four “proof-style” claims.

---

## Proof 1 — Dynamic Core / “rotating coalition” (TRQA of hub occupancy)

We define the **dynamic core** as the **Top-20 out-degree hubs** in each snapshot, and compute a **Jaccard recurrence matrix** over time.

**Key result (theta=0.2 recurrence threshold):**
- Recurrence rate RR ≈ 0.061
- Determinism DET ≈ 0.331
- Laminarity LAM ≈ 0.393

See:
- `figures/fig1a_hub_recursion_jaccard_heatmap.png`
- `figures/fig1b_hub_recursion_binary_theta0p2.png`
- `figures/fig1c_hub_recursion_vs_lag.png`
- `tables/rqa_metrics_by_threshold.csv`

Interpretation: the hub-set recurrence is **not a blur**; it has **metastable blocks** (coalitions persist for intervals) and **returns** (off-diagonal recurrence).

---

## Proof 2 — Criticality-adjacent dynamics (PSD + avalanche scaling)

Using `firing_var` as the activity proxy (scalar telemetry), the power spectral density is close to **pink-noise-like** in multiple segments:

- begin β ≈ 1.21
- mid   β ≈ 1.04
- end   β ≈ 1.07

(where PSD ~ 1/f^β; computed as β = -slope in log-log space over f ∈ [1/500, 0.1] 1/tick).

See:
- `figures/fig2_psd_firing_var_mid.png`
- `tables/psd_slopes.csv`

Avalanche scaling (mid segment, threshold at 75th percentile):
- size exponent α_size ≈ 1.46
- duration exponent α_dur ≈ 1.72
- size–duration relation γ ≈ 1.42

See:
- `figures/fig2b_avalanche_size_ccdf_mid.png`
- `tables/avalanche_scaling.csv`

Important: these are **signatures consistent with criticality**; they are not, by themselves, “proof of life”.

---

## Proof 3 — Empirical free-energy landscape + phase switching (bistability)

Define order parameters:
- x = connectome density proxy = **nnz edges**
- y = hierarchy proxy = **Gini(out-degree)**

We reconstruct an empirical landscape **F = -log P(x,y)** (KDE-smoothed).

**Result: two attractor basins** (“bistability”) with centers near:
- Reading-like basin: nnz ≈ 14878, Gini ≈ 0.540
- Dream/Integration-like basin: nnz ≈ 21036, Gini ≈ 0.440

Estimated barrier height along the straight-line path between wells:
- ΔF_barrier ≈ 8.90 (arbitrary units)

See:
- `figures/fig3_free_energy_landscape.png`
- `figures/fig3b_order_params_timeseries.png`
- `tables/free_energy_wells.csv`
- `tables/free_energy_barrier_summary.json`

**Input-coupling check (where input telemetry exists):**
- When `ute_text_count>0`: mean nnz ≈ 14912, mean Gini ≈ 0.540
- When `ute_text_count==0`: mean nnz ≈ 21000, mean Gini ≈ 0.441

And the macro switching is perfectly aligned (in the covered spans):
- D→R transitions: input fraction = 1.00
- R→D transitions: input fraction = 0.00

See:
- `tables/order_params_conditioned_on_input.csv`
- `tables/phase_transition_summary.csv`
- `tables/phase_transition_events.csv`

---

## Proof 4 — Information-geometry “speed” (Fisher-style proxy)

We use the **ADC territory mass distribution** (from each snapshot’s `adc_json`) as a coarse “mass” P_t, then compute:
Hellinger(P_t, P_{t-Δ}) as a statistical-speed proxy.

Result: very high redistribution early, then collapse to low drift:
- 0–6k ticks: mean speed ≈ 0.0117
- 12–18k ticks: mean speed ≈ 0.0007

See:
- `figures/fig4_fisher_speed_adc_mass.png`
- `figures/fig4b_speed_by_epoch.png`
- `tables/fisher_speed_epoch_summary.csv`

---

## Reproducibility

Main script:
- `scripts/run_four_proofs.py`

This pack also includes:
- `tables/*.csv`
- `figures/*.png`
- `SHA256SUMS.csv` (hashes for every output file)

