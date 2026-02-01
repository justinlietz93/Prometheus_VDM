# Key results (1000-neuron connectome)

## Input provenance
- zip: `1000_neurons_events.zip`
- `events.jsonl` time window (UTC): **2025-08-15T13:11:01.988265Z → 2025-08-16T10:07:28.290496Z**
- state hash (sha256): `e637892e51ef7b3c1fd3fdb1c1cc919de1946960510f7e96f20975bd049d3827`

## Graph size
- nodes: **1000**
- edges: **23838**

## Degree inequality (Gini)
- out_degree Gini: **0.408956**
- in_degree  Gini: **0.408956**

## Heavy-tail tail-fit fingerprint (dossier-style: min tail fraction 0.30)
These rows come from `tail_fit_detailed_selected.csv`:

| label        |   xmin |   alpha |       ks |   n_tail |   tail_decades_log10 |   gini_full |
|:-------------|-------:|--------:|---------:|---------:|---------------------:|------------:|
| out_degree   |     13 | 1.84041 | 0.196253 |      308 |             0.942961 |    0.408956 |
| in_degree    |     13 | 1.84041 | 0.196253 |      308 |             0.942961 |    0.408956 |
| total_degree |     26 | 1.85424 | 0.19212  |      308 |             0.942961 |    0.408956 |

**Interpretation:** degrees are strongly skewed (Gini ~0.409). A power-law tail approximation at **xmin≈13** yields **alpha≈1.84** over ~0.94 decades with ~30.8% of nodes in the tail.

**Caveat:** model comparisons in `tail_fit_detailed_selected.csv` indicate the tail is often fit better by a **lognormal** than a pure power law (common in finite-size networks). The distribution is still **heavy-tailed / scale-free-adjacent** as a quantitative fingerprint.

