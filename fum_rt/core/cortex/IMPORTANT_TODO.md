# TODO

* **You already have spikes.** The scouts/maps produce `SpikeEvent`s and the tick logs summarize them (e.g., `evt_exc_head`, `evt_inh_head`, `evt_heat_head`, `evt_*_count`). I incorrectly implied otherwise.
* **Walkers matter.** In your design they’re not passive samplers; they publish findings (heat/cold/trail/frontier/salience), tag nodes/edges for GDSP, and their field measurements are part of the control loop. Saying “don’t attach spiking to walkers” was a bad take for your system.
* **`td_signal`** in your logs travels with `sie_td_error`, so it’s a TD-style control channel (not “total decay”). That was my misread.

Thanks for calling this out.

---

## What to do now (with the logs you already have)

Below are analyses that produce **non-boring, model-specific** insights using exactly what’s in `events.jsonl` and `utd_events.jsonl`—no new instrumentation, no dense scans.

## 1) Hotspot dynamics & frontier churn

**Goal:** find stable hubs, reactivation latencies, and boundary reshaping.

* From each tick, take `evt_heat_head` and `evt_exc_head` (lists of `[neuron_id, score]`).
* Per neuron:

  * **Dwell time:** number of ticks it appears in `heat_head`.
  * **Reactivation latency:** time from last appearance in `cold_head` to next appearance in `heat_head` (distribution per neuron).
* From `adc_territories / adc_boundaries / adc_cycle_hits`:

  * **Boundary churn rate:** Δ in `adc_boundaries` per tick; correlate with spikes and with any `b1_spike` consolidation events.

**Delivers:** a ranked table of persistent “structural” neurons, a histogram of cold→hot latencies (novelty rebounds), and how ADC frontier movement co-varies with spiking bursts.

## 2) EI balance & control coupling

**Goal:** quantify how system control channels shape activity.

* Construct per-tick features: `vt_walkers`, `vt_coverage`, `td_signal`, `sie_valence_01`, `evt_exc_count`, `evt_inh_count`, `evt_heat_count`, `evt_trail_count`.
* Compute:

  * **EI ratio:** `evt_exc_count / (evt_inh_count + 1)`.
  * **Lag correlations / VAR Granger:** `{vt_*, td_signal, sie_valence_01}` → `{EI ratio, evt_*_count}` with BH-FDR control.
  * **Response curves:** bin `vt_coverage` and plot median `evt_exc_count` (and EI ratio) vs coverage.

**Delivers:** concrete lead/lag relationships (e.g., coverage and walkers leading excitation) and operating curves that explain *when* your system tips into high-activity regimes.

## 3) Memory consolidation precursors

**Goal:** find what predicts **`b1_spike=true`** (loop closure / fragment consolidation).

* Around each tick with `b1_spike=true`, compute pre/post deltas (±K ticks) for `evt_memory_head` aggregates (sum of values), `evt_*_count`, `vt_*`, `td_signal`, `sie_valence_01`.
* Train a simple logistic model with lagged features to see which signals **precede** consolidation.

**Delivers:** a short list of leading indicators (e.g., memory build-up + rising td_signal) that you can watch in real time.

## 4) Emission-aligned analysis (`events.jsonl` ↔ `utd_events.jsonl`)

**Goal:** understand the internal “signature” of text output.

* Align streams by tick index (`evt_t`) or timestamp window.
* For each emission window (emission tick ±K):

  * Summarize changes in `vt_coverage`, `vt_walkers`, `td_signal`, `sie_valence_01`, `evt_*_count`.
  * Count which neuron IDs recur in `heat_head` right before emissions (top-K “speaker-adjacent” neurons).
* Fit a lightweight classifier to predict “emit at t” from lagged `{vt_*, td_signal, sie_valence_01, evt_*_count}`.

**Delivers:** a compact “will-speak soon” signature and the subgraph (by neuron IDs) most often active before speech.

## 5) Co-activation communities (no spikes needed)

**Goal:** recover structure without pre→post edges.

* Build a binary presence matrix **N × T** where entry (i,t)=1 if neuron *i* is in `heat_head` or `exc_head` at tick *t* (use an IDF-like weight if you want).
* Compute pairwise Jaccard or PMI; run community detection (e.g., Louvain) on that similarity graph.

**Delivers:** functional assemblies that co-activate across ticks; plot them as communities and track their activation over time (and vs emissions).

---

## If you can stomach **one** tiny log tweak (later)

You said you’ll park implementation changes as TODOs; here are two **surgical** ones that don’t require dense scans:

1. **Spike sample per tick**
   At the end of a tick, serialize **up to K** spike triples (reservoir sample) already seen by the scouts/maps:

```json
"spike_sample": [[node, sign, amp], ...]  // K≈500–2000
```

This unlocks a spike raster without touching substrate scans.

2. **Walker observation patch**
   When a walker publishes its trail, optionally attach any spikes it *observed* along the trail:

```json
"trail_obs": {"spikes":[[node, sign, amp], ...], "frontiers":[...], "salience":[...]}
```

This respects your design (walkers announce findings) and keeps spikes tied to measurement context.

> You **do not** need to add a “walker spiked? yes/no” flag; walkers don’t fire. But letting a walker message carry the *spikes it observed* preserves the very coupling you care about.

---

## Quick key–meaning recap (from your logs)

* **`vt_walkers` / `vt_coverage`** – number of active walkers and fraction of graph touched this tick.
* **`evt_heat_head` / `evt_exc_head` / `evt_inh_head`** – top-K neuron IDs with scores (heat = “any spike/energy”; exc/inh = signed spike content).
* **`evt_*_count`** – per-tick counts over all neurons for that class of event.
* **`evt_cold_head`** – neurons quiet for a while (good targets for novelty/reactivation analysis).
* **`evt_memory_head` / `evt_memory_dict`** – per-neuron memory weights that often ramp before consolidation.
* **`adc_*`** – territory and boundary stats for your frontier detector.
* **`b1_*`** – complexity/cycle metrics; `b1_spike=true` marks consolidation/loop-closure events.
* **`td_signal`, `sie_valence_01`, `sie_td_error`** – control/reward channels from SIE; td is a TD-like signal, valence is total reward proxy.

