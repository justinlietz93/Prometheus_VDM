Here’s the updated, single plan—**move all internals to `core/`** and make metrics **void-dynamics only** (event-driven from walkers + cold-scout seekers). No whole-connectome scans in the hot path; a tiny auditor remains optional/low-cadence.

---

## Status (2025-08-15)

- [x] Phase A — Move-only migration (modularization and façade)
  - Façade: [nexus.py](fum_rt/nexus.py); main loop: [run_loop()](fum_rt/runtime/loop.py:40)
  - Telemetry and fold: [macro_why_base()](fum_rt/runtime/telemetry.py:19), [status_payload()](fum_rt/runtime/telemetry.py:48), [tick_fold()](fum_rt/runtime/telemetry.py:99)
  - Control-plane/retention/helpers/emitters extracted: [phase.py](fum_rt/runtime/phase.py), [retention.py](fum_rt/runtime/retention.py), [runtime_helpers.py](fum_rt/runtime/runtime_helpers.py), [initialize_emitters()](fum_rt/runtime/emitters.py:23)
- [x] Phase B — Core seam locked
  - Core engine seam: [engine.py](fum_rt/core/engine.py), methods [snapshot()](fum_rt/core/engine.py:53), [engram_load()](fum_rt/core/engine.py:71), [engram_save()](fum_rt/core/engine.py:80)
  - Core signals seam and B1: [signals.py](fum_rt/core/signals.py), [apply_b1_detector()](fum_rt/core/signals.py:218)
  - Optional event-driven metrics reducers in core with runtime adapters: [proprioception/events.py](fum_rt/core/proprioception/events.py), [observations_to_events()](fum_rt/runtime/events_adapter.py:22), [adc_metrics_to_event()](fum_rt/runtime/events_adapter.py:96)
- [ ] Phase C — Event-folded reducers in core (replace scans)
- [ ] Phase D — Cold-scout walkers (core/cortex)
- [ ] Phase E — Orchestrator uses engine.step(); remove legacy math from Nexus
- [ ] Optional — Auditor (rare, budgeted)
- [ ] CI guards — core boundary and runtime NumPy checks
- [ ] Acceptance — golden-run parity, A/B IDF (k=0.0 vs 0.2), KS tests

# Phase A — Move-only migration (no logic change)

* Create:

  ```
  fum_rt/runtime/{orchestrator.py, phase.py, telemetry.py, retention.py, state.py}
  fum_rt/nexus.py   # thin façade re-exporting Nexus
  ```
* Copy current Nexus logic into `runtime/*` and delegate.
* **Golden run parity:** 2–3k ticks; `why` blobs byte-for-byte; first 200 macro lines identical; tick P50/P99 ±2%.

---

# Phase B — Lock the `core/` seam (adapters now, logic move later)

* Introduce a single API the runtime talks to:

```python
# core/engine.py
class CoreEngine:
    def step(self, dt_ms: int, ext_events: list) -> None: ...
    def snapshot(self) -> dict: ...   # numbers only: {b1_z, sie_valence_01, cohesion_components, vt_coverage, vt_entropy, ...}
    def engram_load(self, path: str) -> None: ...
    def engram_save(self, path: str) -> None: ...
```

* Stub pure functions (temporarily forwarding to existing math) in `core/signals.py`:

```python
def compute_b1_z(state) -> float: ...
def sie_valence(state, dstate) -> float: ...
def compute_cohesion(state) -> int: ...
def compute_vt_metrics(state) -> tuple[float, float]: ...
```

**Boundary rule:** `runtime/*` → may import `core/*`. `core/*` → import only `core/*` + numeric libs. **No** `core/* → io/*` or `runtime/*`.

---

# Phase C — Put the brain in `core/` (void-only, event-driven)

Move internals module-by-module; replace scans with incremental folding from **walker/bus events**. Parity after each PR.

## Folder ownership

* **core/substrate**: void/field equations, integrators, tensors/buffers.
* **core/cortex**: connectome/topology, walker scheduling, **ΔB1 detector math**, motif hooks.
* **core/neuroplasticity**: **SIE v2** (novelty, habituation, TD/HSI → valence scalar \[0..1]).
* **core/proprioception**: **event-folded** metrics (cohesion, VT coverage/entropy), **ADC** (bus → estimates).
* **core/primitives**: pure kernels/utils.
* **core/memory**: engram load/save (.h5).

## Event schema (from learners + scouts; O(1) to fold)

```
{kind:"delta",       b1:Δb1, novelty:…, hab:…, td:…, hsi:…}     # when ΔW occurs
{kind:"vt_touch",    token:t}                                   # feature/lex touch
{kind:"edge_on",     u, v} | {kind:"edge_off", u, v}            # active edge on/off
{kind:"motif_enter", id} | {kind:"motif_exit", id}
# new, from cold-scouts (read-only):
{kind:"probe_visit", tile, sample_ids:[...]}                    # VT samples
{kind:"probe_edge",  u, v}                                      # boundary cohesion
{kind:"probe_frontier", tile, neighbor}
{kind:"probe_checksum", tile, checksum}
```

## Incremental reducers (no scans)

* **ΔB1 z (cortex):** Welford streaming mean/var; `z = (x-μ)/sqrt(σ²+ε)` per tick/event.
* **SIE valence (neuroplasticity):** compute at write sites (ΔW); EWMA to scalar `[0..1]`.
* **VT coverage/entropy (proprioception):** Count-Min Sketch + head exact counts; update on `vt_touch` / `probe_visit`.
* **Cohesion (proprioception):** global Union-Find; `union(u,v)` on `edge_on`/`probe_edge`; mark “dirty” on `edge_off` and let auditor reconcile occasionally.
* **ADC (proprioception/adc.py):** fold **only** announce-bus events; never read raw W.

`CoreEngine.snapshot()` returns numbers only; `runtime/telemetry.py` packs them into `why`.

---

# Phase D — Cold-Scout walkers (replace scanning with seekers)

Add **read-only** walker species in `core/cortex` to explore stale space and feed metrics.

## Cold map (per tile/chunk metadata)

* `last_update_t`, `last_probe_t`, `dirty_count`, `checksum`, `frontier_edges`.
* Coldness:

```
cold_score = α*(t_now - last_update_t) +
             β*(t_now - last_probe_t) +
             γ*dirty_count +
             δ*(checksum_changed ? 1 : 0)
```

## Scout roles (read-only; no learning writes)

* **Scouts**: move up the coldness gradient; emit `probe_*` events.
* **Frontier scouts**: traverse boundary edges to reconcile cross-tile connectivity.
* **Sentinels**: blue-noise reseeding to avoid blind spots.

## Scheduler (bounded)

* Step budget ≤ 1–3% of tick time; K scouts; TTL 50–200 steps each.
* Priority = most-cold tiles; preempt/resume next tick if over budget.

**Result:** hot path = event folding only; “scanner” reduced to rare auditor (low cadence, budgeted micro-slices).

---

# Phase E — Cut pass-throughs and finalize boundaries

* Orchestrator loop: control poll → `engine.step()` → `telemetry.collect(engine.snapshot())` → (maybe) speak → retention sweep.
* Delete legacy math from Nexus; keep UTE/UTD, emitters, CLI outside core.

---

## Optional — Auditor (rare, budgeted)

* Triggers: drift between incremental vs last audit > ε, stalest tiles, idle.
* Budget: e.g., 300–1000 μs/tick; epoch snapshot; idempotent reconcile.

---

# Acceptance criteria (every step)

* **Parity:** `why` keys/values identical on the golden scenario; first 200 macro lines identical.
* **Perf:** tick P50/P99 within ±2%; no stalls > 5 ms from scouts/auditor.
* **Isolation:** `core/*` imports contain **no** `io.*` or `runtime.*`.
* **No hot-path scans:** only event folding; auditor disabled or <0.1% of ticks.
* **Metrics health:** cohesion/VT/ΔB1/valence from events within ε of auditor when it runs.

---

# Interface & snippets (so implementation is trivial)

**Core seam stays tiny:**

```python
# runtime/orchestrator.py (loop shape)
m_events = bus.drain()               # announce events
engine.step(dt_ms, m_events)         # fold events; update void & scouts
m = telemetry.collect(engine.snapshot())
self._maybe_speak(m)                 # unchanged gate policy outside core
```

**Incremental folding example:**

```python
# core/proprioception/reducers.py
def on_vt_touch(token): cms.update(token); head[token]+=1
def on_edge_on(u,v): uf.union(u,v)
def on_delta(b1, nov, hab, td, hsi): welford.update(b1); valence.update(nov,hab,td,hsi)
```

**Scout step (read-only):**

```python
# core/cortex/scout.py
def step_scout(s):
    emit_probe_visit(s.tile, sample_ids(s.tile))
    for (u,v) in sample_edges(s.tile): emit_probe_edge(u,v)
    for nb in frontier_neighbors(s.tile): emit_probe_frontier(s.tile, nb)
    mark_last_probe(s.tile); s.ttl -= 1
    s.tile = argmax_neighbor_coldness(s.tile)  # or Levy hop
```

---

## Import & channel invariants (enforced)

* `core/*` never writes JSON/logs (engram I/O only).
* `runtime/telemetry.py` alone builds `why`.
* Emitters (macro/TTY/thought) are sinks; never read back into core.
* Grep check:

  ```
  rg -n 'from\s+fum_rt\.(io|runtime|nexus)' fum_rt/core
  ```

---

## Feature flags & knobs

* `ENABLE_SCOUTS=1` (default 0), `SCOUT_BUDGET_US`, `SCOUT_K`, `SCOUT_TTL`,
* `COLD_WEIGHTS={α,β,γ,δ}`, `COLD_THRESHOLD=τ`,
* `AUDITOR_INTERVAL_TICKS` (large; rare).

---

### TL;DR

* **Migrate first**, lock the `CoreEngine` seam.
* **Move internals into `core/`** with **event-driven reducers** (fold walker/bus events).
* **Add cold-scout walkers** to explore stale areas; **no whole-graph scans** in the hot path.
* Keep a **tiny auditor** as a safety net.
* Prove parity at each step.
