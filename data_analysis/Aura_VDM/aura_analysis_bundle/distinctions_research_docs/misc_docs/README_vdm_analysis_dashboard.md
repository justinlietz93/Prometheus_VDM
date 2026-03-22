# VDM Analysis Dashboard

**Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.**

A unified Plotly Dash analysis dashboard for Void Dynamics Model simulation data.
Drop a `utd_events.jsonl.zip` in the browser and all 15 analysis sections render automatically.

---

## Requirements

Python 3.9+

```bash
pip install dash dash-bootstrap-components plotly pandas numpy scipy scikit-learn statsmodels
```

> `statsmodels` is optional but required for Granger causality. All other sections work without it.

---

## Running

```bash
python vdm_analysis_dashboard.py
```

Default: `http://localhost:8051`

### Options

| Flag | Default | Description |
|---|---|---|
| `--port` | `8051` | Port to serve on |
| `--host` | `0.0.0.0` | Bind address (`127.0.0.1` for local only) |
| `--debug` | off | Enable Dash hot-reload |

```bash
# Examples
python vdm_analysis_dashboard.py --port 8080
python vdm_analysis_dashboard.py --host 127.0.0.1 --debug
```

---

## Input Data

### Required
| File | Format | Description |
|---|---|---|
| `utd_events.jsonl.zip` | zip containing a `.jsonl` | Status + say events from the VDM runtime |

### Expected JSONL event types
The parser reads two event types:

**`type: "text"` / `payload.type: "status"`** — per-tick scalar telemetry. Expected fields:
```
t, neurons, phase, active_edges, vt_coverage, vt_entropy, connectome_entropy,
cohesion_components, b1_z, adc_territories, sie_total_reward, sie_v2_reward_mean,
sie_valence_01, sie_v2_valence_01, ute_text_count
```
Missing fields are silently skipped — the dashboard degrades gracefully.

**`type: "macro"` / `macro: "say"`** — utterance events used for event-triggered averages, emission microstructure, and motor gate analysis.

### Multiple neuron runs
If the zip contains multiple neuron counts, the dashboard automatically selects the **largest run** (most ticks) for all analysis. The SIE Memory vs N panel in the Network section still plots all runs.

---

## Upload

1. Open `http://localhost:8051` in your browser
2. Click the upload bar or drag-and-drop your zip file
3. Status bar confirms: `✓ filename.zip | N ticks | M say events`
4. All sections render — scroll down or use the left sidebar to jump to a section

The sidebar has 15 anchors:

```
○  Overview          ↔  Cross-Correlation    ⚡  Event-Triggered
→  Granger           ◉  Macrostate           ∩  MIP / Integration
⬡  Network           Φ  PCI-like             I  Predictive MI
~  Rolling Stats     ♫  Spectral             Σ  TC / O-info
🧠  Bio Neural        ⚖  Scale-Free           ▦  Regimes
```

---

## Analysis Sections

### Overview
- Summary cards: tick count, tick range, say rate, active channel count
- Z-scored timeseries overlay of all internal channels

### Cross-Correlation
- Full cross-correlation matrix across all internal channels (±80 lag)
- PCA state-space speed vs `input_text_words`
- PCA state-space speed vs `has_input`

### Event-Triggered Averages
- Mean ± SEM locked to `did_say` events for: `connectome_entropy`, `vt_coverage`, `active_edges`, `sie_v2_valence_01`
- Window: ±80 ticks

### Granger Causality
- Causal density bar (top 20 directed pairs, −log₁₀ p)
- Significance heatmaps split by epoch: `E1_low_entropy_baseline`, `E2_high_entropy_plateau`, `E3_mid`
- Lag: 5 ticks, F-test p-value

### Macrostate
- k=4 MiniBatch KMeans on first 5 PCA components
- Macrostate trajectory colored by state
- Stationary distribution bar per epoch

### MIP / Integration
- Sliding-window Total Correlation (TC), Dual TC (DTC), O-information — linear and log scale
- Minimum Information Partition: singleton variable count histogram (which channel is most isolated most often)
- Window: 256 ticks, stride: 64

### Network
- Phase portrait: PC1 × PC2 colored by tick (captures attractor geometry)
- LZ complexity of PC1 sign — sliding window timeseries
- Degree proxy CCDF with power-law MLE fit (uses `active_edges` as proxy)
- SIE memory (autocorr lag-1) vs neuron count N

### PCI-like (ΦLZ)
- Timeseries: LZ complexity × permutation entropy on PC1
- Box plot by epoch
- Say-event windows vs matched control windows

### Predictive MI
- Gaussian MI between PC1(t) and PC1(t+lag) — decay curve up to lag 50

### Rolling Statistics
- Rolling autocorr (lag-1) and rolling variance for `connectome_entropy`, `sie_v2_valence_01`, `active_edges`
- Window: 300 ticks

### Spectral
- Welch PSD 1/f^β slope bar for all channels
- Log-log PSD fit scatter for `connectome_entropy` and `sie_v2_valence_01`
- Reference line at β=1 (pink noise)

### TC / O-information
- Total correlation (TC) timeseries
- O-information timeseries — positive = redundancy-dominated, negative = synergy-dominated

### Biological Neural
- Avalanche size CCDF with power-law fit (threshold: 75th percentile of `active_edges`)
- PSD of `connectome_entropy`
- Free energy landscape: F(H) = −log P(H)
- Order parameters timeseries (z-scored overlay)
- Fisher information speed: ‖ΔΨ‖₂ in state space

### Scale-Free / Heavy Tail
- Gini coefficient per metric (inequality of distribution)
- Tail fit grid: 4 xmin values × CCDF + power-law fit

### Regimes
- All-ticks phase overlay: entropy colored by `phase`
- Emission microstructure: inter-say-event interval histogram

---

## Epoch Assignment

Epochs are assigned automatically from `connectome_entropy` quantiles:

| Label | Condition |
|---|---|
| `E1_low_entropy_baseline` | entropy ≤ 33rd percentile |
| `E3_mid` | 33rd < entropy < 67th percentile |
| `E2_high_entropy_plateau` | entropy ≥ 67th percentile |

This matches the naming convention in the original analysis scripts.

---

## Extending

**Add a new figure:** write a `fig_*` function returning a `go.Figure`, call `sfig()` for base layout, then add it to the relevant `section()` block in `render_dashboard()`.

**Add a new section:** add an entry to `NAV_ITEMS`, create a `section("anchor_id", "TITLE", [...])` block, and append it to the returned `html.Div` list at the bottom of `render_dashboard()`.

**Change theme:** all colors are defined at the top of the file under `# THEME`. `BG`, `PANEL`, `SURFACE`, `ACCENT`, `PALETTE` are the main knobs.

---

## Known Limitations

- Granger and MIP are computed on upload — for very long runs (>50k ticks) expect 10–30s render time
- H5 snapshot files (topology metrics) are not yet loaded via the UI — add a second `dcc.Upload` and a parser for `state_*.h5` to enable hub recurrence and Laplacian spectrum panels
- All computation runs in the Dash callback thread; for production use, move heavy analysis to a background worker (e.g. `celery` or `multiprocessing`)
