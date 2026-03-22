# Pending/thin Family 7 distinctions — direct package update

This package addresses four distinctions in the current inventory that were either explicitly marked pending or were still too thinly explained:

- D7.2 — Micro-transition eigenvalue spectrum
- D7.4 — Rolling variance/autocorrelation structure
- D7.5 — Long-lag predictive MI structure
- D7.9 — Node embedding / bridge-core structure

## D7.2 — Micro-transition eigenvalue spectrum
The 25-state micro-transition matrix has one stationary mode at 1.0 and five non-stationary modes with eigenvalues:

- 0.9833 (τ ≈ 59.3 ticks)
- 0.9623, 0.9623 (τ ≈ 26.0 ticks)
- 0.9312, 0.9312 (τ ≈ 14.0 ticks)

This is not a one-timescale Markov blur. The spectrum has a clear ladder of slow modes, meaning microstate memory decays across multiple distinct timescales.

The transition rows are also sticky rather than diffuse: mean self-transition probability is 0.750, with the most self-persistent microstates above 0.89.

## D7.4 — Rolling variance/autocorrelation structure
The entropy-channel rolling statistics are regime-shaped, not uniform:

- E1 mean rolling variance = 0.102
- E2 mean rolling variance = 0.000904
- E3 mean rolling variance = 0.034

At the E2→E3 boundary, the entropy channel shows the strongest joint variance/autocorrelation jump:

- pre-boundary variance mean = 0.000669
- post-boundary variance mean = 0.138
- pre-boundary lag-1 AC = 0.920
- post-boundary lag-1 AC = 0.992

The PCA-speed channel behaves differently: variance and autocorrelation rise across both major boundaries, indicating a shift into a higher-energy / more persistent processing mode rather than a single narrow critical signature.

## D7.5 — Long-lag predictive MI structure
Restricting to the 100–600 tick window to avoid the trivial near-lag peak, the strongest local predictive-MI peaks are:

- E1: lag 151, MI 0.378
- E2: lag 281, MI 0.095
- E3: lag 111, MI 1.041

E3 also carries a ladder of additional long-lag peaks at 291, 361, 521, and 571 ticks. That means the late regime does not just predict the near future better; it preserves multiple long-range predictive horizons simultaneously.

## D7.9 — Node embedding / bridge-core structure
Per-neuron embedding metrics show that community identity explains far more variance in routing-like properties than in raw degree:

- participation η² peaks at 0.458 (t=17220)
- convergence-score η² peaks at 0.166 (t=17220)
- row-weight η² peaks at 0.373 (t=17220)
- out-degree η² stays tiny (≤ 0.0043)

So the community system differentiates routing phenotype much more than simple connection count.

Using the two available graph-signature mapping tables, a low-cost bridge subset in the middle snapshot can be isolated directly. Taking the lowest-cost 10% of matches on both 17160→17220 and 17220→17280 yields an overlap of **160 nodes** in state 17220 (3.2% of the snapshot). This bridge core is **not** a frozen hub caste:

- out-degree mean = 9.62 vs 20.07 in the rest (d = -0.46)
- pagerank mean = 0.000107 vs 0.000203 (d = -0.47)
- participation mean = 0.732 vs 0.708 (d = +0.20)

So the structurally persistent subset looks more like connective tissue than like a permanent ruling class of hubs.
