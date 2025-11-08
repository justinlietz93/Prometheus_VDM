<!-- DOC-GUARD: CANONICAL -->
# VDM Algorithms & Execution Flows (Auto-compiled)

**Last updated**: 2025-11-05
**Last commit**: 60c5156
**Scope:** Single source of truth for implemented algorithms and control flows in this repository.
**Rules:** Pseudocode + references only. Link to math/values elsewhere (EQUATIONS/CONSTANTS/SYMBOLS/UNITS).
**MathJax:** Only inline `$...$` inside comments when needed.

**Legend:** This file is **PSEUDOCODE** (illustrative).
• Normative math: `Derivation/EQUATIONS.md`.
• Numbers: `Derivation/CONSTANTS.md`.
• Symbols/units: `Derivation/SYMBOLS.md`, `Derivation/UNITS_NORMALIZATION.md`.
• Canon map: `CANON_MAP.md`.

**Per Item Identifier Template:**
• Type: RUNTIME|INSTRUMENT|POLICY|EXPERIMENT  
• Binding: PSEUDOCODE
• State: none|read-only|writes state  
• Dependencies: (short)
• Notes: (short)

---

## Core Update Loops

#### VDM-A-001 - Runtime Main Loop (Nexus Tick Loop)  <a id="vdm-a-001"></a>
>
> Type: RUNTIME • Binding: PSEUDOCODE • State: writes state • Dependencies: none • Notes: agency layer optional; consumes signals only

**Context:** fum_rt/runtime/loop/main.py:283-679 • Commit: 7498744 • Module: runtime/loop

**Role:** Execute the main simulation tick loop on the Nexus-like object, orchestrating all subsystems per tick.

**Inputs:**

- Symbols: $t$ (time), $W$ (node weights) - see `SYMBOLS.md`
- Constants: `CONSTANTS.md#const-alpha`, `CONSTANTS.md#const-beta`
- Runtime params: step (tick index), duration_s (wall-clock limit), t0 (start timestamp)

**Depends on equations:**

- TODO: add anchor for connectome step equations

**Pseudocode:**

```text
INIT:
  - Lazy-init CoreEngine (telemetry seam) if not present
  - Lazy-init VOID cold scout walker (budget_visits, budget_edges from env/config)
  - Lazy-init event-driven metrics aggregator (half_life_ticks, z_spike, hysteresis)
  - Start maps WebSocket forwarder (if enabled)
  - Start status HTTP endpoint
  - Attach connectome announce bus for ADC/cycles/B1 observations
  - Lazy-init memory field and trail map structures (head_k, half_life_ticks)
  - Configure scout roster (HeatScout, VoidRayScout, MemoryRayScout, FrontierScout, 
    CycleHunterScout, SentinelScout, ColdScout, ExcitationScout, InhibitionScout)

LOOP (per tick):
  1. Check duration_s termination condition if provided       # fum_rt/runtime/loop/main.py:539
  2. Poll control plane (external phase.json updates)         # fum_rt/runtime/loop/main.py:550
  3. Compute SIE drive and step connectome                    # via compute_step_and_metrics
     # uses [VDM-E-xxx] for density, TD signal, firing_var   # fum_rt/runtime/stepper.py:29
  4. Run optional RE-VGSP learner (if ENABLE_REVGSP=1)        # fum_rt/runtime/loop/main.py:565
  5. Run optional GDSP structural actuator (if ENABLE_GDSP=1) # fum_rt/runtime/loop/main.py:571
  6. Apply B1 detector on connectome observations             # fum_rt/runtime/loop/main.py:578
  7. Process inbound message queue (UTE stimulation)          # fum_rt/runtime/loop/main.py:587
  8. Run void scouts (bounded micro time budget)              # fum_rt/runtime/loop/main.py:593
     # via run_scouts_once → returns events
  9. Fold events into metrics (tick_fold)                     # fum_rt/runtime/loop/main.py:611
 10. Maybe emit "why" (say text composition) every N ticks    # fum_rt/runtime/loop/main.py:619
 11. Maybe run smoke tests (boundary checks)                  # fum_rt/runtime/loop/main.py:623
 12. Emit status and macro observations (logging, Redis)      # fum_rt/runtime/loop/main.py:627
 13. Save checkpoint if checkpoint_every divides step         # fum_rt/runtime/loop/main.py:631
 14. Maybe visualize (plots, maps publish)                    # fum_rt/runtime/loop/main.py:635
 15. Sleep to match target hz (throttle loop)                 # fum_rt/runtime/loop/main.py:639

TERMINATION:
  - duration_s wall-clock expired OR KeyboardInterrupt        # fum_rt/runtime/loop/main.py:539
```

**Preconditions:**

- nx.connectome, nx.sie, nx.ute, nx.utd must be initialized
- nx.run_dir must exist for checkpoints/logs

**Postconditions/Invariants:**

- Connectome topology and weights updated per tick
- Metrics published to bus/logs/Redis
- Checkpoints saved at configured intervals

**Concurrency/Ordering:**

- Single-threaded per tick; steps are sequential
- WebSocket/HTTP endpoints may run on background threads (idempotent start)

**Failure/Backoff hooks:**

- Try-except wrappers on all subsystem calls (silent no-op on errors when VOID_STRICT=0)
- VOID_STRICT=1 re-raises exceptions for debugging

**Emits/Side effects:**

- Logs: nexus_started, checkpoint_saved, why_emitted, smoke_test results
- Bus: Observations (cycle_hit, region_stat), VTTouchEvent, EdgeOnEvent, SpikeEvent
- Redis: status JSON, maps snapshots (if enabled)
- Files: checkpoints (HDF5 or NPZ), plots (if viz enabled)

**Also implemented at:**

- fum_rt/nexus.py:362 (thin wrapper; delegates to run_loop)

> DEBT: GDSP can fail without logs when STRICT gate disabled; add fail-fast/telemetry path, remove any ability to use dense backend even with env. Sparse only, fail fast.  
> DEBT: Overlapping scout flags; defaults conflict-unify or validate toggles.
> DEBT: Status HTTP lacks auth/TLS; keep localhost default, gate optional token auth.

---

#### VDM-A-002 - Connectome Step (Void-Equation Driven Topology Update)  <a id="vdm-a-002"></a>

> Type: RUNTIME • Binding: PSEUDOCODE • State: writes state • Dependencies: `delta_re_vgsp`, `delta_gdsp` (EQUATIONS TODO)
> **STATUS:** **BROKEN / WRONG** - docs claim “no dense path,” but the code includes and can execute a **dense scan** branch.

**Context:** `fum_rt/core/connectome.py:272-313` • Commit: `7498744` • Module: `core/connectome`

**Role:** Apply one update tick driven by Void Equations: structural growth/rewiring via alias sampling and node field updates.

**Inputs:**

- Symbols: $\alpha$ (ReLU($\Delta\alpha$)), $\omega$ ($\Delta\omega$), $W$ - see `SYMBOLS.md`
- Constants: `CONSTANTS.md#const-alpha`, `CONSTANTS.md#const-beta`, `threshold`, `lambda_omega`
- Params: `t` (time), `domain_modulation`, `sie_drive` (SIE valence gate), `use_time_dynamics`

**Depends on equations:**

- TODO: add anchor for `delta_re_vgsp`, `delta_gdsp` in `EQUATIONS.md`

**Pseudocode (as implemented - with broken bits marked):**

```text
INIT:
  - d_alpha = delta_re_vgsp(W, t, domain_modulation, use_time_dynamics)
  - d_omega = delta_gdsp(W, t, domain_modulation, use_time_dynamics)
  - a  = ReLU(d_alpha) + external_stimulus (with decay)      # core/connectome.py:283
  - om = d_omega                                             # core/connectome.py:284

ALIAS TABLE BUILD (sparse default):
  - Build alias sampler ~ a distribution                      # _build_alias (Vose), core/connectome.py:96

STRUCTURAL PLASTICITY (per node):
  IF structural_mode == "dense" AND N <= 4096:               # ⚠ BROKEN: dense scan exists
    - Compute full affinity S[i,j] = a[i]*a[j] - lambda_omega*|om[i]-om[j]|
    - Extract top-k neighbors per node via argpartition       # core/connectome.py:301
  ELSE:                                                      # sparse alias-sampling (intended production path)
    FOR each node i:
      - Sample s candidates ~ alias table (drop self/dupes)   # core/connectome.py:311
      - For sampled j: w[j] = a[i]*a[j] - lambda_omega*|om[i]-om[j]|
      - Keep top-k by affinity as new neighbors               # core/connectome.py:314

SYMMETRIZE:
  - A_new = A_new OR A_new.T  (undirected graph)              # core/connectome.py:326

NODE FIELD UPDATE:
  - delta_W = universal_void_dynamics(W, t, domain_modulation, use_time_dynamics)
  - delta_W *= sie_drive                                      # core/connectome.py:331
  - W = clip(W + delta_W, 0, 1)                               # core/connectome.py:333

FINALIZE:
  - self.A = A_new                                            # core/connectome.py:335
  - Recompute E from W and A                                  # core/connectome.py:337
```

**Preconditions:**

- `N`, `k`, `threshold`, `lambda_omega`, `candidates` configured
- `W` initialized (node weights in `[0,1]`)
- Env gate: `NO_DENSE_CONNECTOME=1` (tests/CI assert) **(⚠ BROKEN: code still contains a dense branch guarded by runtime flags)**
- Alias sampler functions available (`delta_re_vgsp`, `delta_gdsp`, `universal_void_dynamics`)

**Postconditions/Invariants:**

- `A` symmetric; ~`k` neighbors per node (approx.)
- `W` stays in `[0,1]`
- `E` (edge weights) derived from `W` and `A`

**Concurrency/Ordering:**

- Sparse alias mode: sequential per current pseudocode (rows can be parallelized)
- **Dense mode:** vectorized NumPy (**validation only in intent, but present in code**) - **⚠ WRONG relative to “no dense path” policy**

**Failure/Backoff hooks:**

- External stimulus accumulation wrapped in try/except (silent no-op)

**Emits/Side effects:**

- `self.findings` updated (`vt_visits`, `vt_entropy`, `coverage`)
- Bus events: `cycle_hit` (during void traversal), `region_stat` (end of traversal)

**Also implemented at:**

- `fum_rt/core/sparse_connectome.py` (sparse variant; similar logic)

> **DEBT:** Dense rebuild / dense top-k path exists; violates “no dense path” policy for large `N`.
> **DEBT:** Structural rewiring RNG not plumbed from run seed; wire deterministic RNG.
> **BROKEN / WRONG:** Documentation states *“no dense path whatsoever; void walkers and walker maps only”* while code enables a dense branch under `structural_mode=="dense"` (≤4096).

---

#### VDM-A-010 - Runtime Stepper compute_step_and_metrics  <a id="vdm-a-010"></a>

**Per Item Identifier Template:**
• Type: RUNTIME
• Binding: PSEUDOCODE
• State: writes state
• Dependencies: core.signals, core.metrics
• Notes: Mirrors Nexus inline logic (move-only extraction)

**Context:** fum_rt/runtime/stepper.py:29-133 • Commit: 60c5156 • Module: runtime/stepper

**Role:** Compute density/TD/firing_var, derive SIE drive, advance connectome, and build per-tick metrics.

**Inputs:** link symbols/constants (anchors only)

- Symbols: TODO: add `t`, `step` anchors in `SYMBOLS.md` (see fum_rt/runtime/stepper.py:29)
- Constants/params: domain_modulation (nx.dom_mod), use_time_dynamics (nx.use_time_dynamics)

**Depends on equations:** link anchors only (no math here)

- TODO: add anchors for active-edge density, TD-like signal, firing variability in `EQUATIONS.md`

**Pseudocode (verbatim structure, no new logic):**

```text
INIT:
  m := {} ; drive := {}

DENSITY:
  E, density := compute_active_edge_density(nx.connectome, nx.N)     # core.signals

TD PROXY:
  prev_E := nx._prev_active_edges or E
  vte_prev := nx._prev_vt_entropy ; vte_last := nx._last_vt_entropy
  td_signal := compute_td_signal(prev_E, E, vte_prev, vte_last)      # core.signals
  nx._prev_active_edges := E

FIRING VAR:
  firing_var := compute_firing_var(nx.connectome)                     # core.signals

SIE DRIVE:
  drive := nx.sie.get_drive(W=None, external_signal=td_signal,
                            time_step=step, firing_var=firing_var,
                            target_var=0.15, density_override=density,
                            novelty_idf_scale=idf_scale)
  sie_drive := drive["valence_01"] default 1.0
  sie2 := nx.connectome._last_sie2_valence default 0.0
  sie_gate := max(sie_drive, sie2) ∈ [0,1]

ADVANCE CONNECTOME:
  nx.connectome.step(t, domain_modulation=nx.dom_mod,
                     sie_drive=sie_gate, use_time_dynamics=nx.use_time_dynamics)

METRICS:
  m := core.metrics.compute_metrics(nx.connectome)
  m["homeostasis_pruned"] := nx.connectome._last_pruned_count
  m["homeostasis_bridged"] := nx.connectome._last_bridged_count
  m["active_edges"] := E ; m["td_signal"] := td_signal
  m["novelty_idf_scale"] := idf_scale
  if firing_var is not None: m["firing_var"] := firing_var
  if nx.connectome.findings: m.update(findings)
  m["sie_gate"] := sie_gate

HISTORY:
  nx._prev_vt_entropy := nx._last_vt_entropy
  nx._last_vt_entropy := m.get("vt_entropy", 0.0)

RETURN:
  (m, drive)
```

**Preconditions:**

- nx exposes connectome, sie, N, dom_mod, use_time_dynamics
- core.signals and core.metrics available

**Postconditions/Invariants:**

- Connectome advanced once with sie_gate
- Metrics dict contains structural and TD diagnostics

**Concurrency/Ordering:**

- Single-threaded per tick; pure function aside from nx mutations

**Failure/Backoff hooks:**

- Try/except guards in implementation swallow errors to preserve parity

---

#### VDM-A-011 - Tick Telemetry Fold (bus → ADC → event metrics → B1)  <a id="vdm-a-011"></a>

**Per Item Identifier Template:**
• Type: INSTRUMENT
• Binding: PSEUDOCODE
• State: writes runtime telemetry only (no dynamics)
• Dependencies: bus, ADC, optional EventDrivenMetrics
• Notes: Behavior-preserving seam

**Context:** fum_rt/runtime/telemetry.py:337-650 • Commit: 60c5156 • Module: runtime/telemetry

**Role:** Fold per-tick telemetry: publish neutral delta, drain bus, derive void-topic symbols, update ADC, fold event-driven metrics, and compute complexity proxy with B1 detector.

**Inputs:** link symbols/constants (anchors only)

- Schemas: TODO: add ADC metrics anchors in `SCHEMAS.md` if applicable

**Depends on equations:** link anchors only (no math here)

- Optional: B1 detector references `[VDM-E-###]` if canonized elsewhere

**Pseudocode (verbatim structure, no new logic):**

```text
DELTA PUBLISH (optional):
  if nx._evt_metrics:
    comps := drive.components or {}
    meta := {"b1":0.0, "nov":comps["nov"]|0, "hab":..., "td":td_signal, "hsi":...}
    bus.publish(DynObs(t=step, kind="delta", nodes=[], meta))
    if SYNTH_DELTA_W:
      nodes_sel := first ≤16 from tick_rev_map keys
      dw_val := clip(sign(td_signal)*min(0.05, |td_signal|))
      bus.publish(DynObs(t=step, kind="delta_w", nodes=nodes_sel, meta={"dw":dw_val}))

DRAIN BUS:
  obs_batch := bus.drain(max_items=nx.bus_drain default 2048)
  nx._last_obs_batch := obs_batch
  for obs in obs_batch, map node indices via tick_rev_map → void_topic_symbols

ADC UPDATE:
  adc.update_from(obs_batch) ; adc_metrics := adc.get_metrics()
  nx._last_adc_metrics := adc_metrics

EVENT-DRIVEN METRICS (optional):
  if nx._engine is None and nx._evt_metrics:
    for ev in obs_to_events(obs_batch): evtm.update(ev)
    evtm.update(adc_event(adc_metrics, t=step))
    evsnap := evtm.snapshot(); merge as m["evt_*"] without overriding canonical b1_*

ADC + COMPLEXITY:
  m.update(adc_metrics)
  m["complexity_cycles"] += adc_metrics["adc_cycle_hits"] (if present)

RETURN:
  (m, void_topic_symbols)
```

**Preconditions:**

- nx.bus present; adc optional; evt_metrics optional

**Postconditions/Invariants:**

- m contains merged adc and evt_* fields; canonical fields preserved

**Concurrency/Ordering:**

- Single-threaded per tick; bounded drain and synthesis

**Failure/Backoff hooks:**

- Extensive try/except to keep parity and avoid IO

---

#### VDM-A-012 - CoreEngine.step (Event-Driven Fold + Maps Staging)  <a id="vdm-a-012"></a>

**Per Item Identifier Template:**
• Type: INSTRUMENT
• Binding: PSEUDOCODE
• State: read-only against connectome; updates telemetry caches
• Dependencies: EventDrivenMetrics, VOID scout, map reducers
• Notes: Core seam; no IO/logging

**Context:** fum_rt/core/engine/core_engine.py:82-262 • Commit: 60c5156 • Module: core/engine

**Role:** Fold external events and internal VOID-scout events into event-driven reducers; fold map heads; stage maps_frame payload; refresh cached snapshot.

**Pseudocode (verbatim structure, no new logic):**

```text
ENSURE EVT INIT:
  _ensure_evt_init()

FOLD EXTERNAL EVENTS:
  for ev in ext_events:
    if hasattr(ev,"kind"): evtm.update(ev); collected_events.append(ev)
    update cold_map on vt_touch/edge_on
    track latest_tick from ev.t

FOLD VOID SCOUT EVENTS:
  tick_hint := last ev.t or nx._emit_step+1
  for _ev in void_scout.step(nx.connectome, tick_hint):
    evtm.update(_ev); collected_events.append(_ev)
    update cold_map on vt_touch/edge_on
  latest_tick := max(latest_tick, tick_hint)

FOLD MAPS (telemetry-only):
  fold heat_map, exc_map, inh_map, memory_map, trail_map with collected_events at fold_tick

STAGE FRAME:
  stage_maps_frame(nx, heat_map, exc_map, inh_map, fold_tick)

REFRESH SNAPSHOT:
  _last_evt_snapshot := build_evt_snapshot(..., latest_tick, nx)
```

**Preconditions:**

- nexus-like exposes connectome, b1 config, seed, etc.

**Postconditions/Invariants:**

- No mutation of dynamics; only telemetry caches updated

**Failure/Backoff hooks:**

- Silent no-ops on any error (parity-preserving)

---

#### VDM-A-013 - Optional RE-VGSP Adapter (Learner Hook)  <a id="vdm-a-013"></a>

**Per Item Identifier Template:**
• Type: POLICY
• Binding: PSEUDOCODE
• State: writes state (adapter-controlled)
• Dependencies: fum_rt.core.neuroplasticity.revgsp.RevGSP
• Notes: Enabled via ENABLE_REVGSP=1 (default off)

**Context:** fum_rt/runtime/loop/main.py:88-157 • Commit: 60c5156 • Module: runtime/loop

**Role:** Best-effort call into RevGSP.adapt_connectome with kwargs filtered by signature; silent on error.

**Pseudocode:**

```text
if not ENABLE_REVGSP: return
try import RevGSP; _adapt := RevGSP().adapt_connectome else return
substrate := nx.substrate or nx.connectome or return
sig := inspect.signature(_adapt); allowed := set(sig.parameters)
eta := env REV_GSP_ETA or nx.rev_gsp_eta ; lam := env REV_GSP_LAMBDA or nx.rev_gsp_lambda
twin_ms := env REV_GSP_TWIN_MS or 20
kwargs := {
  "substrate": substrate, "spike_train": nx.recent_spikes, "spike_phases": nx.spike_phases,
  "learning_rate": eta, "base_lr": eta, "lambda_decay": lam, "total_reward": metrics["sie_total_reward"],
  "plv": metrics.get("evt_plv"), "network_latency_estimate": nx.network_latency_estimate or {...},
  "network_latency": same, "time_window_ms": twin_ms
}
kwargs := {k:v for k,v in kwargs if v is not None and (not allowed or k in allowed)}
try _adapt(**kwargs) except: return
```

---

#### VDM-A-014 - Optional GDSP Actuator (Structural Plasticity)  <a id="vdm-a-014"></a>

**Per Item Identifier Template:**
• Type: POLICY
• Binding: PSEUDOCODE
• State: writes state (adapter-controlled)
• Dependencies: fum_rt.core.neuroplasticity.gdsp.GDSPActuator
• Notes: Enabled via ENABLE_GDSP=1 (default off); emergent triggers only

**Context:** fum_rt/runtime/loop/main.py:160-280 • Commit: 60c5156 • Module: runtime/loop

**Role:** Gate structural repairs/growth/pruning based on b1 spike, TD magnitude, and cohesion components; operate on sparse CSR-only substrate.

**Pseudocode:**

```text
if not ENABLE_GDSP: return
td := metrics["td_signal"] default 0.0
b1_spike := metrics["b1_spike"] or metrics["evt_b1_spike"] default False
comp := metrics["cohesion_components"] or metrics["evt_cohesion_components"] default 1
td_thr := env GDSP_TD_THRESH or 0.2
if not (b1_spike or |td| >= td_thr or comp > 1): return

try import GDSPActuator; _run_gdsp := GDSPActuator().run else return
s := nx.substrate or nx.connectome or return
require s has {"synaptic_weights","persistent_synapses","synapse_pruning_timers","eligibility_traces","firing_rates"} else return

introspection_report := {"component_count": comp, "b1_persistence": bounded(|b1_z|/10), "repair_triggered": b1_spike}
sie_report := {"total_reward": metrics["sie_total_reward"], "td_error": metrics["td_signal"], "novelty": metrics["evt_vt_entropy"]|0}
territory_indices := nx._territories.sample_any(K) if available else None
if triggers and not territory_indices: maybe bus.publish(BiasHintEvent(...))

T_prune := env GDSP_T_PRUNE or 100 ; pruning_threshold := env GDSP_PRUNE_THRESHOLD or 0.01
try _run_gdsp(substrate=s, introspection_report, sie_report, territory_indices, T_prune, pruning_threshold) except: return
```

---

#### VDM-A-015 - run_loop_once (Single-Tick Helper)  <a id="vdm-a-015"></a>

**Per Item Identifier Template:**
• Type: RUNTIME
• Binding: PSEUDOCODE
• State: none
• Dependencies: runtime.telemetry.tick_fold
• Notes: Import seam compliance for boundary tests

**Context:** fum_rt/runtime/loop/**init**.py:35-55 • Commit: 60c5156 • Module: runtime/loop

**Role:** Delegate optional engine.step(events) and always stage telemetry via tick_fold for one tick.

**Pseudocode:**

```text
if hasattr(engine,"step"):
  if events: engine.step(step, list(events)) else engine.step(step)
tick_fold(nx, step, engine)
```

---

## Local Agent/Walker Policies

#### VDM-A-003 - Void Scout Runner (Per-Tick Scout Executor)  <a id="vdm-a-003"></a>
>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: read-only • Publishes: bus events; tags on neurons/edges • Notes: traversal metrics only

**Context:** fum_rt/core/cortex/void_walkers/runner.py:38-136 • Commit: 7498744 • Module: core/cortex/void_walkers

**Role:** Execute a bounded batch of read-only scouts exactly once per tick, enforcing micro time budget across all scouts.

**Inputs:**

- connectome: read-only neighbor access (N, neighbors/get_neighbors)
- scouts: sequence of scout instances (HeatScout, ColdScout, etc.)
- maps: dict of map heads (heat_head, cold_head, exc_head, inh_head)
- budget: {"visits": int, "edges": int, "ttl": int, "tick": int, "seeds": list[int]}
- max_us: total microsecond budget per tick

**Depends on equations:**

- (none; read-only traversal only)

**Pseudocode:**

```text
INIT:
  - Ensure max_us >= 0                                       # runner.py:66
  - Compute start_idx = budget["tick"] % len(scouts)        # round-robin fairness, runner.py:76
  - Rotate scout order: scouts[start_idx:] + scouts[:start_idx]
  - per_us = max_us / len(scouts) if not overridden         # runner.py:96

LOOP (over rotated scouts):
  FOR each scout in ordered:
    IF elapsed_us >= max_us: BREAK                          # global time guard, runner.py:103
    - Call scout.step(connectome, bus=None, maps, budget) → events
    - Extend evs with returned events                       # runner.py:112
    IF per_us > 0 AND scout elapsed > per_us:
      - Record over-budget (soft guard; no penalty)         # runner.py:117

PUBLISH:
  - IF evs non-empty AND bus present:
      bus.publish_many(evs)  OR fallback to bus.publish per event
                                                             # runner.py:124

RETURN:
  - list of BaseEvent emitted within budget                 # runner.py:136
```

**Preconditions:**

- scouts must have .step(connectome, bus, maps, budget) method
- connectome must expose neighbors/get_neighbors or adj mapping

**Postconditions/Invariants:**

- Total wall-clock time <= max_us (best-effort; cannot preempt inside scout.step)
- Round-robin fairness over ticks (start_idx rotates)

**Concurrency/Ordering:**

- Stateless per tick; no background threads
- Scouts execute sequentially in rotated order

**Failure/Backoff hooks:**

- Try-except on scout.step (swallow errors, return empty list)
- Try-except on bus.publish_many (swallow errors)

**Emits/Side effects:**

- Bus: VTTouchEvent, EdgeOnEvent, SpikeEvent (via publish_many)

> DEBT: Runner respects mixed flags; clarify single admission gate.
> DEBT: Scout flag/knob overlap - unify or validate toggles (see ledger §8).

---

#### VDM-A-004 - Cold Scout (Coldness-Driven Walker)  <a id="vdm-a-004"></a>
>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: read-only (publishes explore events only) • Priors: minimal/flat • Notes: baseline cartography; complements goal-driven flows

**Context:** fum_rt/core/cortex/void_walkers/void_cold_scout.py:41-55 • Commit: 7498744 • Module: core/cortex/void_walkers

**Role:** Read-only walker that prefers neighbors whose node IDs appear in ColdMap snapshot head (least recently visited nodes).

**Inputs:**

- connectome: read-only neighbor access
- maps: {"cold_head": [[node, score], ...]}
- budget: {"visits": int, "edges": int, "ttl": int, "tick": int, "seeds": list[int]}

**Depends on equations:**

- (none; heuristic traversal only)

**Pseudocode:**

```text
INIT:
  - Extract priority_set = cold_head nodes from maps (cap=max(64, budget_visits*8))
                                                             # void_cold_scout.py:49

STEP (via BaseScout):
  - Inherited from BaseScout.step (base.py:step method)
  - Uses priority_set to bias neighbor selection toward cold nodes
  - Emits VTTouchEvent, EdgeOnEvent within budget

RETURN:
  - list of BaseEvent                                       # base.py signature
```

**Preconditions:**

- maps["cold_head"] exists (optional; empty set if missing)

**Postconditions/Invariants:**

- Emits events only for visited nodes/edges (no writes)

**Concurrency/Ordering:**

- Stateless; safe for concurrent read

**Failure/Backoff hooks:**

- Try-except on map extraction (returns empty set)

**Emits/Side effects:**

- VTTouchEvent (kind="vt_touch", token=node)
- EdgeOnEvent (kind="edge_on", u, v)

**Also implemented at:**

- (similar pattern in void_heat_scout.py, void_excitation_scout.py, void_inhibition_scout.py)

---

#### VDM-A-005 - Alias Sampling (Vose's Method)  <a id="vdm-a-005"></a>
>
> Type: RUNTIME • Binding: PSEUDOCODE • State: none • Dependencies: none • Notes: O(N) build, O(1) draw

**Context:** fum_rt/core/connectome.py:96-127 • Commit: 7498744 • Module: core/connectome

**Role:** Build O(N) alias table for sampling from discrete distribution; O(1) per draw.

**Inputs:**

- p: probability array (unnormalized or normalized)

**Depends on equations:**

- (none; sampling algorithm only)

**Pseudocode:**

```text
BUILD ALIAS TABLE:
  - Normalize p → p / sum(p)                                # connectome.py:108
  - scaled = p * N                                          # connectome.py:115
  - Partition into small (< 1.0) and large (>= 1.0) bins   # connectome.py:116
  - WHILE small and large non-empty:
      s_idx = small.pop()
      l_idx = large.pop()
      prob[s_idx] = scaled[s_idx]
      alias[s_idx] = l_idx
      scaled[l_idx] -= (1.0 - prob[s_idx])                  # connectome.py:121
      IF scaled[l_idx] < 1.0: small.append(l_idx)
      ELSE: large.append(l_idx)                             # connectome.py:123
  - Remaining bins: prob[i] = 1.0                           # connectome.py:126

DRAW SAMPLES:
  - k = random_int(0, N, size=s)                            # connectome.py:133
  - u = random_float(0, 1, size=s)                          # connectome.py:134
  - choose_alias = (u >= prob[k])                           # connectome.py:135
  - out[choose_alias] = alias[k[choose_alias]]              # connectome.py:137
  - RETURN out                                              # connectome.py:138
```

**Preconditions:**

- p.size > 0 and p.sum() > 0

**Postconditions/Invariants:**

- prob.size == alias.size == N
- Draws from alias table reproduce original distribution

**Concurrency/Ordering:**

- Build is O(N); single-threaded
- Draw is O(1) per sample (vectorized for multiple draws)

**Failure/Backoff hooks:**

- If p.sum() <= 0: uniform distribution fallback (p = 1/N)  # connectome.py:110

**Emits/Side effects:**

- None (pure function)

---

## Plasticity / Memory-Steering Procedures

#### VDM-A-006 - RE-VGSP Learning Step (Three-Factor Synaptic Plasticity)  <a id="vdm-a-006"></a>

> Type: RUNTIME • Binding: PSEUDOCODE • State: writes state • Dependencies: `delta_re_vgsp`, `delta_gdsp`, `VoidDebtModulation.get_universal_domain_modulation` • Notes: three-factor rule (values-only on CSR)

**Context:** `Void_Equations.py` (`delta_re_vgsp`, `delta_gdsp`); `Void_Debt_Modulation.py` (`VoidDebtModulation.get_universal_domain_modulation`) • Commit: HEAD

**Role:** Complete RE-VGSP learning step combining local spike-timing memory (eligibility) with a global reward/resonance modulation, applied **only to existing CSR edges**.

**Inputs (binding):**

- `W`: **CSR** weights/state, shape `[n,n]` (operate on `W.data`; `indices/indptr` unchanged; densification forbidden)
- `t`: `int` timestep
- `alpha (η)`, `beta (γ)`: optional overrides; otherwise use values from `CONSTANTS.md`
- `domain_modulation`: `float` from `VoidDebtModulation.get_universal_domain_modulation(domain, …)`
- `f_ref`, `phase_sens`: optional time-modulation knobs (defaults inside `Void_Equations.py`)

**Inputs (adapter-side, not equation parameters):**

- `E` (eligibility traces): **CSR** with **identical sparsity pattern** as `W` (same `indptr/indices`); three-factor scaling via `ΔW *= E.data`
- `total_reward (r)`: `float` - fold into `domain_modulation` (bounded gain)
- `plv ∈ [0,1]`: `float` - choose **one**: scale `phase_sens` *or* multiply `domain_modulation`
- `neuron_polarities ∈ {-1,+1}`: optional row mask applied to **RE-VGSP** update values only
- `spike_data`, `lambda_decay`: used **only** to maintain/update `E`; not passed to `delta_*` (separate pseudocode section handles E updates)

**Depends on code:**

- `Void_Equations.delta_re_vgsp`, `Void_Equations.delta_gdsp` (values computed per existing edge)
- `Void_Debt_Modulation.VoidDebtModulation.get_universal_domain_modulation`

**Pseudocode:**

```text
INPUT: CSR W, int t, floats alpha?, beta?, f_ref?, phase_sens?, domain_modulation
       CSR E (optional, same pattern as W), float total_reward, float plv, vector neuron_polarities? (len n)

1) Compute domain modulation:
   dm_base  := VoidDebtModulation.get_universal_domain_modulation(domain).domain_modulation
   dm_reward := clamp( 1 + k_R * total_reward, dm_min, dm_max )
   dm := dm_base * dm_reward
   # Optionally fold PLV either into phase_sens (preferred) or into dm (choose one)

2) Get learning rates:
   {ALPHA, BETA} := get_universal_constants()   # from Void_Equations if you expose it
   α := (alpha or ALPHA);  β := (beta or BETA)

3) Row/col index views without densifying:
   row := repeat(range(n), diff(W.indptr))   # length = nnz
   col := W.indices                          # length = nnz
   vals := W.data                            # length = nnz

4) Compute deltas per existing edge (values-only):
   d_re := delta_re_vgsp(values=vals, row=row, col=col, t=t,
                         alpha=α, phase_sens=phase_sens, use_time_dynamics=True,
                         domain_modulation=dm)                  # nnz-length
   d_gd := delta_gdsp(values=vals, row=row, col=col, t=t,
                      beta=β, phase_sens=phase_sens, use_time_dynamics=True,
                      domain_modulation=dm)                     # nnz-length

5) Optional polarity mask on RE-VGSP:
   if neuron_polarities:
       d_re := d_re * neuron_polarities[row]

6) Three-factor scaling with eligibility (if provided):
   if E is not None:
       assert E.indptr == W.indptr and E.indices == W.indices
       d := (d_re + d_gd) * E.data
   else:
       d := (d_re + d_gd)

7) Apply update on CSR values (structure unchanged):
   W.data := clip( W.data + d, min_val?, max_val? )

OUTPUT: updated CSR W (same sparsity), optional diagnostics (dm, α, β, norms)
```

**Preconditions:**

- `W` is CSR; `E` (if present) is CSR with **identical pattern**; no densification anywhere
- `neuron_polarities.shape == (n,)` if provided

**Postconditions/Invariants:**

- `W.indptr`/`W.indices` unchanged (no structural rewiring here)
- Value changes bounded by chosen clamps; eligibility decays handled in **separate** E-update pseudocode

**Concurrency/Ordering:**

- Work is **O(nnz)** per tick; row-local slices may be processed in parallel.
- Structural add/remove of edges happens in the connectome/rewiring step, not here.

**Failure/Backoff hooks:**

- If `domain_modulation` lookup fails: use `dm := 1.0` and log a warning
- If `E` pattern mismatches `W`: raise error (do not silently densify) or resync pattern explicitly

**Emits/Side effects:**

- Optional debug: norms of `d_re`, `d_gd`, `d`, effective `(dm, α, β)`, and nnz touched

---

#### VDM-A-007 - GDSP Adaptive Thresholds (Structural Plasticity Gating)  <a id="vdm-a-007"></a>
>
> Type: POLICY • Binding: PSEUDOCODE • State: internal state only • Dependencies: none • Notes: heuristic adaptation; bounds enforced

**Context:** fum_rt/core/neuroplasticity/gdsp.py:38-100 • Commit: 7498744 • Module: core/neuroplasticity

**Role:** Adaptive threshold manager for GDSP structural plasticity triggers (repair, growth, pruning).

**Inputs:**

- sie_report: {"total_reward": float, "td_error": float, "novelty": float}
- b1_persistence: float (B1 detector persistence score)
- Internal state: reward_history, td_error_history, novelty_history (rolling windows)

**Depends on equations:**

- (none; heuristic adaptation only)

**Pseudocode:**

```text
UPDATE AND ADAPT:
  - Append current (total_reward, td_error, novelty) to histories
                                                             # gdsp.py:60
  - Truncate histories to last 100 samples                  # gdsp.py:66
  - Increment timesteps_since_growth                        # gdsp.py:70

STAGNATION GUARD:
  IF timesteps_since_growth > 500 AND b1_persistence <= 0.001:
    - Lower thresholds: reward_threshold *= 0.95            # gdsp.py:74
    - Encourage structural growth                           # gdsp.py:76

ACTIVITY DAMPING:
  IF structural_activity_counter > 20:
    - Raise thresholds: reward_threshold *= 1.05            # gdsp.py:80
    - Dampen excessive structural changes                   # gdsp.py:82
    - Reset activity counter                                # gdsp.py:83

STATISTICAL ADAPTATION (every 50+ samples):
  - r75 = percentile(reward_history, 75)                    # gdsp.py:87
  - td90 = percentile(td_error_history, 90)                 # gdsp.py:88
  - n75 = percentile(novelty_history, 75)                   # gdsp.py:89
  - Exponential moving average toward target percentiles:
      reward_threshold = 0.95*reward_threshold + 0.05*r75   # gdsp.py:95

RECORD ACTIVITY:
  - Increment structural_activity_counter when growth/repair occurs
                                                             # gdsp.py:99
```

**Preconditions:**

- sie_report keys present (defaults to 0.0 if missing)

**Postconditions/Invariants:**

- Thresholds stay within [min, max] bounds
- Histories bounded to last 100 samples

**Concurrency/Ordering:**

- Single-threaded; called once per tick

**Failure/Backoff hooks:**

- None (numerical bounds enforced)

**Emits/Side effects:**

- Internal state (thresholds, histories, counters)

> DEBT: Tests absent for threshold adaptation / activity damping; add regression coverage.  

---

## I/O Pipelines & Data Products Generation

#### VDM-A-008 - Fluid Dynamics Walker (LBM Telemetry Agent)  <a id="vdm-a-008"></a>
>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: read-only • Dependencies: bilinear interp/div/vort (EQUATIONS TODO) • Notes: publishes petitions

**Context:** Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:57-100 • Commit: 7498744 • Module: physics/fluid_dynamics/telemetry

**Role:** Read-only walker that steps using measured velocity field (advection only) and senses local scalar quantities.

**Inputs:**

- sim: object with {ux, uy, solid, nx, ny} (LBM simulation state)
- dt: time step (default 1.0)
- kind: str (scalar type to sense: "div", "swirl", "shear")

**Depends on equations:**

- TODO: add anchor for bilinear interpolation, divergence, vorticity in EQUATIONS.md

**Pseudocode:**

```text
INIT:
  - x, y = initial position (float)                         # walkers.py:66
  - kind = scalar type (e.g., "div", "swirl")               # walkers.py:68

STEP (advection):
  - ux_interp = bilinear(sim.ux, x, y)                      # walkers.py:88
  - uy_interp = bilinear(sim.uy, x, y)                      # walkers.py:89
  - x_new = x + dt * ux_interp                              # walkers.py:90
  - y_new = y + dt * uy_interp                              # walkers.py:91
  - Clamp to interior band [0.5, nx-1.5] x [0.5, ny-1.5]    # walkers.py:94
  - IF solid[y_new, x_new]: jitter inward                   # walkers.py:98
  - Update: x = x_new, y = y_new                            # walkers.py:103

SENSE (local scalar):
  IF kind == "div":
    - ddx_ux = ddx(sim.ux, x, y)                            # walkers.py:113
    - ddy_uy = ddy(sim.uy, x, y)                            # walkers.py:114
    - RETURN ddx_ux + ddy_uy                                # walkers.py:115
  IF kind == "swirl":
    - ddy_ux = ddy(sim.ux, x, y)                            # walkers.py:117
    - ddx_uy = ddx(sim.uy, x, y)                            # walkers.py:118
    - RETURN ddy_ux - ddx_uy  (vorticity)                   # walkers.py:119
  IF kind == "shear":
    - RETURN abs(ddx_uy + ddy_ux)  (shear rate)             # walkers.py:121

POST PETITION:
  - Create Petition(kind, value, x, y, t)                   # walkers.py:16
  - bus.post(Petition)                                      # walkers.py:25
```

**Preconditions:**

- sim.ux, sim.uy are 2D arrays (ny, nx)
- sim.solid is boolean mask (True = solid, False = fluid)

**Postconditions/Invariants:**

- Walker stays inside fluid domain [0.5, nx-1.5] x [0.5, ny-1.5]
- No writes to sim state (read-only)

**Concurrency/Ordering:**

- Stateless per walker; safe for parallel execution

**Failure/Backoff hooks:**

- Try-except on solid check (jitter inward on error)        # walkers.py:97

**Emits/Side effects:**

- Bus: Petition events (kind, value, x, y, t)

---

#### VDM-A-009 - Advisory Policy (Fluids Telemetry Feedback)  <a id="vdm-a-009"></a>
>
> Type: POLICY • Binding: PSEUDOCODE • State: none • Dependencies: none • Notes: advisory only; caller applies or ignores

**Context:** Derivation/code/physics/fluid_dynamics/telemetry/walkers.py:162-219 • Commit: 7498744 • Module: physics/fluid_dynamics/telemetry

**Role:** Map petition summaries (divergence, vorticity) to suggested small nudges to numerical parameters (never injects forces; caller decides).

**Inputs:**

- stats_summary: {"div_p50": float, "div_p90": float, "vort_p50": float, ...}
- params: {"tau": float, "void_gain": float, ...}
- bounds: PolicyBounds (min/max limits for tau, void_gain, etc.)

**Depends on equations:**

- (none; heuristic feedback only)

**Pseudocode:**

```text
SUGGEST:
  - Extract div_p90, vort_p90 from stats_summary             # walkers.py:193
  - Compute div_err = div_p90 - div_target                   # walkers.py:195
  - Compute vort_err = vort_p90 - vort_target                # walkers.py:196

TAU ADJUSTMENT (divergence control):
  IF abs(div_err) > 0.1 * div_target:
    - delta_tau = -sign(div_err) * min(0.005, abs(div_err)*0.01)
                                                             # walkers.py:199
    - tau_new = clamp(tau + delta_tau, bounds.tau_min, bounds.tau_max)
                                                             # walkers.py:200

VOID_GAIN ADJUSTMENT (vorticity control):
  IF abs(vort_err) > 0.1 * vort_target:
    - delta_gain = sign(vort_err) * min(0.02, abs(vort_err)*0.01)
                                                             # walkers.py:204
    - void_gain_new = clamp(void_gain + delta_gain, bounds.void_gain_min, bounds.void_gain_max)
                                                             # walkers.py:205

RETURN:
  - {"tau": tau_new, "void_gain": void_gain_new}            # walkers.py:208
```

**Preconditions:**

- stats_summary keys present (defaults to 0.0 if missing)
- params keys present (no change if missing)
- bounds configured (defaults to PolicyBounds())

**Postconditions/Invariants:**

- Suggested params stay within bounds
- No writes to sim state (advisory only)

**Concurrency/Ordering:**

- Stateless; safe for concurrent calls

**Failure/Backoff hooks:**

- Try-except on dict key access (returns original params)

**Emits/Side effects:**

- None (pure function)

---

<!-- BEGIN AUTOSECTION: ALGO-INDEX -->
<!-- Tool-maintained list of [VDM-A-###](#vdm-a-###) anchors for quick lookup -->
- [VDM-A-001](#vdm-a-001)
- [VDM-A-002](#vdm-a-002)
- [VDM-A-003](#vdm-a-003)
- [VDM-A-004](#vdm-a-004)
- [VDM-A-005](#vdm-a-005)
- [VDM-A-006](#vdm-a-006)
- [VDM-A-007](#vdm-a-007)
- [VDM-A-008](#vdm-a-008)
- [VDM-A-009](#vdm-a-009)
- [VDM-A-010](#vdm-a-010)
- [VDM-A-011](#vdm-a-011)
- [VDM-A-012](#vdm-a-012)
- [VDM-A-013](#vdm-a-013)
- [VDM-A-014](#vdm-a-014)
- [VDM-A-015](#vdm-a-015)
- [VDM-A-022](#vdm-a-022)
<!-- END AUTOSECTION: ALGO-INDEX -->
## Change Log

- 2025-11-05 • algorithms updated • 60c5156
- 2025-10-08 • add VDM-A-013..021 (metriplectic integrators & QC; FRW residual QC; A6 collapse) • HEAD
- 2025-10-03 • initial algorithms extracted • 7498744

<!-- markdownlint-enable MD033 -->

---

### VDM-A-022 - Tube Spectrum and Condensation Harness (Tachyonic Tube v1)  <a id="vdm-a-022"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: writes artifacts • Dependencies: Bessel evaluations, adaptive quadrature • Notes: QC gates for spectrum coverage and condensation curvature

**Context:** Derivation/code/physics/tachyonic_condensation (runner + solvers) • Commit: 09f871a

**Role:** Compute discrete spectrum roots $\kappa_\ell(R)$ at $k=0$ for a finite-radius tube and evaluate condensation energy $E(R)$ with background $E_{\rm bg}(R)$; emit PNG/CSV/JSON artifacts and enforce gates:

- Spectrum coverage gate: $\mathrm{cov}_{\rm phys} \ge 0.95$ (primary KPI), report $\mathrm{cov}_{\rm raw}$.
- Condensation curvature gate: interior minimum $R_\star$ with quadratic coefficient $a>0$ and finite_fraction $\ge 0.80$.

**Depends on equations:**

- [VDM-E-095] Tube secular equation (\\(f_\ell(\kappa)=0\\))
- [VDM-E-096] Coverage metrics ($\\mathrm{cov}_{\\rm phys}$, $\\mathrm{cov}_{\\rm raw}$)
- [VDM-E-097] Condensation energy and background

**Pseudocode (spectrum):**

```text
INPUT: R_sweep, ell_max, (mu,c), tag
FOR each R in R_sweep:
  FOR ell in 0..ell_max:
    scan theta-grid for sign changes of f_ell(kappa(theta))
    if sign-change: bracket -> secant/Newton refine -> record kappa
attempts_phys = count of (R,ell) with any sign-change
successes = number of refined roots
cov_phys = successes/attempts_phys; cov_raw = successes/(len(R_sweep)*(ell_max+1))
emit PNG overview + heatmap; CSV with roots and residual; JSON summary
```

**Pseudocode (condensation):**

```text
INPUT: R_sweep, (mu,c,lambda), E_bg params (sigma, alpha), tag
FOR each R in R_sweep:
  compute unstable modes (m_ell^2<0)
  compute N4_ell via adaptive radial integral with tail
  compute E(R) = E_bg(R) + sum_ell [1/2 m^2 v^2 + 1/4 N4 v^4]
refine around current min; fit quadratic near R_star -> coeff a
finite_fraction = fraction of R with finite E(R)
curvature_ok = (interior min) AND (a>0 or Δ^2E>0)
emit PNG E(R), CSV series, JSON summary
```

**Preconditions:**

- io_paths policy and approvals in effect (quarantine unapproved runs)

**Postconditions:**

- Artifacts saved under `outputs/(figures|logs)/tachyonic_condensation/` with tag and timestamps

**Gates:**

- Spectrum: $\mathrm{cov}_{\rm phys} \ge 0.95$ (PASS in v1: 1.000)
- Condensation: finite_fraction $\ge 0.80$, interior min, $a>0$ (PASS in v1)

---

## Monte Carlo Samplers and Diagnostics

#### VDM-A-030 - HMC Leapfrog + Metropolis Gate  <a id="vdm-a-030"></a>

> Type: RUNTIME • Binding: PSEUDOCODE • State: writes samples (not physics state) • Dependencies: leapfrog(J‑flow), metrics logger  
> Notes: Records ΔH histograms and acceptance vs stepsize for QC (see [VDM-E-130](Derivation/EQUATIONS.md#vdm-e-130), [VDM-E-131](Derivation/EQUATIONS.md#vdm-e-131))

Pseudocode:

```text
INPUT: q0, stepsize ε, n_steps L, mass matrix M (or preconditioner), rng
1) Sample momentum: p0 ~ N(0, M)
2) (q*, p*) := LEAPFROG(q0, p0; ε, L)           # time-reversible, volume-preserving
3) Compute ΔH = H(q*, p*) - H(q0, p0)           # [VDM-E-131]
4) Accept with α = min(1, exp(-ΔH))             # [VDM-E-130]
5) If u ~ U(0,1) < α: q1 := q* else q1 := q0
6) Log per-trajectory: ε, L, ΔH, accepted?, |p|, |∇H| (optional)
7) (QC) Accumulate:
   - α(ε) for acceptance-vs-stepsize fit (1 − α) ~ ε^p, target p≈4 (leapfrog)
   - ΔH histogram moments per ε
RETURN: q1, α, ΔH
```

QC hooks:

- Acceptance-vs-stepsize slope and R² gate: [VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize](Derivation/VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize)  
- ΔH histogram diagnostics: [VALIDATION_METRICS.md#kpi-hmc-deltaH-hist](Derivation/VALIDATION_METRICS.md#kpi-hmc-deltaH-hist)

---

#### VDM-A-031 - RHMC Outline (Rational HMC for Fractional Powers)  <a id="vdm-a-031"></a>

> Type: RUNTIME • Binding: PSEUDOCODE • State: writes samples • Dependencies: multishift CG, leapfrog skeleton  
> Notes: Exactness restored by Metropolis accept/reject; fractional operators via rational approximation

Pseudocode:

```text
INPUT: action with fractional operator A^{-γ}, γ∈(0,1)
1) Approximate A^{-γ} ≈ c0 + Σ_{k=1..K} c_k / (A + σ_k I)     # rational approx
2) Use pseudofermion fields and force terms requiring solves with shifts σ_k
3) Integrate with leapfrog (Sexton–Weingarten splitting if cheap/expensive parts)
4) Solve all shifted systems via Multishift CG (VDM-A-035)
5) Metropolis step with ΔH as in HMC
RETURN: accepted sample, logs for ΔH/α
```

---

## Linear Solvers and Preconditioning

#### VDM-A-032 - Conjugate Gradient (CG) Adapter  <a id="vdm-a-032"></a>

> Type: INSTRUMENT • Binding: PSEUDOCODE • State: none • Dependencies: matrix‑vector multiply A·x

Pseudocode:

```text
INPUT: A (SPD), b, x0, tol, maxiter
1) r0 = b - A x0; p0 = r0; k = 0
2) WHILE k < maxiter AND ||rk||/||b|| > tol:
     αk = (rkᵀ rk) / (pkᵀ A pk)
     x_{k+1} = x_k + αk pk
     r_{k+1} = r_k - αk A pk
     βk = (r_{k+1}ᵀ r_{k+1}) / (r_kᵀ r_k)
     p_{k+1} = r_{k+1} + βk pk
     k = k + 1
RETURN: x_k, k, residual_norm
```

Logging: iterations, final residual, preconditioner tag (if any), timings.

---

#### VDM-A-033 - BiCGStab Adapter  <a id="vdm-a-033"></a>

> Type: INSTRUMENT • Binding: PSEUDOCODE • State: none • Dependencies: matrix‑vector multiply A·x  
> Notes: For non‑symmetric systems

Provide standard BiCGStab iteration with residual/orthogonality checks and early‑exit on stagnation; emit JSON metrics (iter, residuals).

---

#### VDM-A-034 - Even–Odd (Red–Black) Preconditioning  <a id="vdm-a-034"></a>

> Type: INSTRUMENT • Binding: PSEUDOCODE • State: none • Dependencies: lattice parity split  
> Notes: Schur complement reduction; halves effective problem size on bipartite lattices

Pseudocode:

```text
1) Reorder lattice dofs into even (e) and odd (o) sites → block form:
   A = [A_ee  A_eo; A_oe  A_oo]
2) Solve reduced Schur system on (e): (A_ee - A_eo A_oo^{-1} A_oe) x_e = b_e - A_eo A_oo^{-1} b_o
3) Recover x_o = A_oo^{-1} (b_o - A_oe x_e)
4) Use inner solver for A_oo^{-1}(·) (cheap local or diagonal‑dominant part)
```

Emit speedup/conditioning diagnostics (optional).

---

#### VDM-A-035 - Multishift Conjugate Gradient  <a id="vdm-a-035"></a>

> Type: INSTRUMENT • Binding: PSEUDOCODE • State: none • Dependencies: SPD A, set of shifts {σ_k}

Pseudocode:

```text
Solve (A + σ_k I) x^{(k)} = b for all k using shared Krylov subspace:
1) Initialize one CG stream on A; maintain per‑shift recurrences for x^{(k)}
2) Update all shifted solutions each iteration with O(#shifts) extra saxpys
3) Converge when worst residual across shifts ≤ tol
RETURN: {x^{(k)}}, iterations, residuals
```

Logs: shift list, iteration count, residuals per shift.

---

## Scale Program Utilities

#### VDM-A-036 - RG Blocking Operator (Field/Observable)  <a id="vdm-a-036"></a>

> Type: INSTRUMENT • Binding: PSEUDOCODE • State: read-only • Dependencies: kernel B_s  
> Notes: Pairs with A6 envelope gate ([VDM-E-094](Derivation/EQUATIONS.md#vdm-e-094)) and RG KPI ([VALIDATION_METRICS.md#kpi-rg-collapse](Derivation/VALIDATION_METRICS.md#kpi-rg-collapse))

Pseudocode:

```text
INPUT: field φ on lattice, scale s, kernel B_s (e.g., uniform average), Δφ
1) Partition lattice into disjoint s×…×s blocks
2) For each block, compute (B_s φ)(block_center) by kernel (average or specified)
3) Rescale: φ^{(s)} = s^{-Δφ} · (B_s φ)
4) For observables O(φ), define O^{(s)} := O(φ^{(s)}) with appropriate rescaling
5) Emit collapse artifacts: overlay across s, compute envelope E_max
RETURN: φ^{(s)}, O^{(s)}, collapse metrics
```

Artifacts: scaling‑collapse overlay PNG + CSV/JSON (envelope metrics, s, Δφ, kernel tag).

## GENERIC / Metriplectic Adapters and QC

#### VDM-A-037 - VDM-GENERIC Adapter (Constructor + Gates)  <a id="vdm-a-037"></a>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: none (validates) • Dependencies: [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-140), [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-142), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-degeneracy-resid), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg)

Pseudocode:
```text
INPUT: E[q], S[q], L(q), M(q); discretization/context tag; tolerances (eps=1e-12)
CHECKS:
  1) Antisymmetry: ||L + Lᵀ||_∞ ≤ eps
  2) Symmetry & PSD: ||M − Mᵀ||_∞ ≤ eps; xᵀ M x ≥ −eps for random/unit vectors x
  3) Degeneracy residuals:
     g1 := ||L ∇S||_∞ ; g2 := ||M ∇E||_∞      # [VDM-E-142]
     require g1 ≤ eps, g2 ≤ eps                # KPI kpi-degeneracy-resid
  4) Entropy nonnegativity monitor hook registered (σ ≥ 0 per step)  # [VDM-E-143], KPI kpi-entropy-prod-nonneg
EMIT: JSON with {antisym_ok, sym_psd_ok, g1, g2, eps, commit, seed}
RETURN: adapter_handle or raise ValidationError
```

Notes:
- Centralizes GENERIC conformance for any state extension; used by metriplectic runners before execution.


#### VDM-A-038 - Hydrodynamic Poisson Construction (Cookbook Skeleton)  <a id="vdm-a-038"></a>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: none • Dependencies: fluid variable set (ρ, m, ε, …); [Derivation/Complete-Formalisms/CF2_Contact_to_Metriplectic_Evolution.md](Derivation/Complete-Formalisms/CF2_Contact_to_Metriplectic_Evolution.md)

Pseudocode (outline only; math references live in canon):
```text
INPUT: variable taxonomy (scalar densities, vector densities, tensors)
STEPS:
  1) Start from baseline fluid Poisson structure (mass, momentum, energy sectors)
  2) Add scalar/tensor blocks per tensor rank with correct index symmetries (Curie)
  3) Enforce locality and boundary conditions consistent with BC sheet
  4) Verify antisymmetry & Jacobi via VDM-A-039
OUTPUT: L(q) blocks; doc anchors to symbols and equations
```

Notes:
- Construction details (indices, brackets) are referenced; do not duplicate equations in this file.


#### VDM-A-039 - Poisson–Jacobi Identity Tester  <a id="vdm-a-039"></a>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: none • Dependencies: [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-141), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-poisson-jacobi-resid)

Pseudocode:
```text
INPUT: L(q), basis ℬ of smooth test functionals {F,G,H}
FOR all triples (F,G,H)⊂ℬ:
   J := {F,{G,H}_J}_J + {G,{H,F}_J}_J + {H,{F,G}_J}_J     # [VDM-E-141]
ACCUMULATE: e_Jacobi := max_ℬ ||J||_∞
GATE: e_Jacobi ≤ 1e-12 (scaled eps)
EMIT: JSON residuals, histogram optional; figure path if plotted
RETURN: pass/fail
```

Notes:
- Basis ℬ includes linear forms and localized probes to cover product rules.


#### VDM-A-040 - Entropy Production Monitor (M-step H‑theorem)  <a id="vdm-a-040"></a>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: writes logs • Dependencies: [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-143), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg), [Derivation/code/common/io_paths.py](Derivation/code/common/io_paths.py)

Pseudocode:
```text
INPUT: ∇S, M, Δt, run_tag
σ := (∇S)ᵀ M (∇S)                             # [VDM-E-143]
ΔΣ ← ΔΣ + Δt * σ
GATE: σ ≥ −1e-12 and ΔΣ ≥ −1e-12
LOG: CSV row {t, σ, ΔΣ}; JSON summary at end with seeds/commit; PNG σ(t)
RETURN: pass/fail
```

Notes:
- Attach to every M-step and J⊕M composition (JMJ).


#### VDM-A-041 - Curie Principle Compliance Linter  <a id="vdm-a-041"></a>
> Type: POLICY • Binding: PSEUDOCODE • State: none • Dependencies: [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-146), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-curie-compliance)

Pseudocode:
```text
INPUT: declared tensor ranks of state variables; constitutive/M terms
CHECK: all scalarized couplings are rotational invariants (e.g., D:D, tr(D), |∇c|²)
FLAG: any rank mismatch or forbidden scalarization
EMIT: curie_ok boolean + list of flagged terms (JSON)
GATE: curie_ok=true for merge to production runners
```

Notes:
- Applied in review and CI for extended hydrodynamics and structural fields.


#### VDM-A-042 - OQ‑021 Corner Regularization Runner (Skeleton)  <a id="vdm-a-042"></a>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: writes artifacts • Dependencies: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-corner-stress-bound), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-corner-velocity-cap), [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md#kpi-corner-entropy-nondiv), [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-144), [Derivation/EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-145)

Pseudocode:
```text
SETUP: wedge/corner domain; baseline viscous run; extended run with c-field
PARAMS: grid over (Λ, De_c, Pe_c); radii r/L ladder → approach apex
RUN:
  - Use VDM-GENERIC adapter [VDM-A-037] to validate L,M,E,S
  - Attach H-theorem monitor [VDM-A-040]
  - Advance solver; log stress, |v|, σ components
POST:
  - KPI: Corner Stress Boundedness (no blow-up vs r→0)
  - KPI: Corner Velocity Cap + scaling collapse vs Λ·De_c
  - KPI: Corner Entropy Nondivergence (σ, ΔΣ)
ARTIFACTS: figures (overlay/envelope), CSV, JSON (seed, commit, gates)
RETURN: pass/fail per KPI set
```

Notes:
- This runner is the instrumentation target for OQ‑021 under GENERIC discipline.
