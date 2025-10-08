<!-- DOC-GUARD: CANONICAL -->
# VDM Algorithms & Execution Flows (Auto-compiled)

**Scope:** Single source of truth for implemented algorithms and control flows in this repository.  
**Rules:** Pseudocode + references only. Link to math/values elsewhere (EQUATIONS/CONSTANTS/SYMBOLS/UNITS).  
**MathJax:** Only inline `$...$` inside comments when needed.

**Legend:** This file is **PSEUDOCODE** (illustrative).
• Normative math: `derivation/EQUATIONS.md`.  
• Numbers: `derivation/CONSTANTS.md`.
• Symbols/units: `derivation/SYMBOLS.md`, `derivation/UNITS_NORMALIZATION.md`.  
• Canon map: `CANON_MAP.md`.  

**Per Item Identifier Template:**
• Type: RUNTIME|INSTRUMENT|POLICY|EXPERIMENT  
• Binding: PSEUDOCODE
• State: none|read-only|writes state  
• Dependencies: (short)
• Notes: (short)

---

## Core Update Loops

#### VDM-A-001 — Runtime Main Loop (Nexus Tick Loop)  <a id="vdm-a-001"></a>
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
> DEBT: Overlapping scout flags; defaults conflict—unify or validate toggles.
> DEBT: Status HTTP lacks auth/TLS; keep localhost default, gate optional token auth.

---

#### VDM-A-002 — Connectome Step (Void-Equation Driven Topology Update)  <a id="vdm-a-002"></a>

> Type: RUNTIME • Binding: PSEUDOCODE • State: writes state • Dependencies: `delta_re_vgsp`, `delta_gdsp` (EQUATIONS TODO)
> **STATUS:** **BROKEN / WRONG** — docs claim “no dense path,” but the code includes and can execute a **dense scan** branch.

**Context:** `fum_rt/core/connectome.py:272-313` • Commit: `7498744` • Module: `core/connectome`

**Role:** Apply one update tick driven by Void Equations: structural growth/rewiring via alias sampling and node field updates.

**Inputs:**

- Symbols: $\alpha$ (ReLU($\Delta\alpha$)), $\omega$ ($\Delta\omega$), $W$ — see `SYMBOLS.md`
- Constants: `CONSTANTS.md#const-alpha`, `CONSTANTS.md#const-beta`, `threshold`, `lambda_omega`
- Params: `t` (time), `domain_modulation`, `sie_drive` (SIE valence gate), `use_time_dynamics`

**Depends on equations:**

- TODO: add anchor for `delta_re_vgsp`, `delta_gdsp` in `EQUATIONS.md`

**Pseudocode (as implemented — with broken bits marked):**

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
- **Dense mode:** vectorized NumPy (**validation only in intent, but present in code**) — **⚠ WRONG relative to “no dense path” policy**

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

## Local Agent/Walker Policies

#### VDM-A-003 — Void Scout Runner (Per-Tick Scout Executor)  <a id="vdm-a-003"></a>
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
> DEBT: Scout flag/knob overlap — unify or validate toggles (see ledger §8).

---

#### VDM-A-004 — Cold Scout (Coldness-Driven Walker)  <a id="vdm-a-004"></a>
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

#### VDM-A-005 — Alias Sampling (Vose's Method)  <a id="vdm-a-005"></a>
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

#### VDM-A-006 — RE-VGSP Learning Step (Three-Factor Synaptic Plasticity)  <a id="vdm-a-006"></a>

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
- `total_reward (r)`: `float` — fold into `domain_modulation` (bounded gain)
- `plv ∈ [0,1]`: `float` — choose **one**: scale `phase_sens` *or* multiply `domain_modulation`
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

#### VDM-A-007 — GDSP Adaptive Thresholds (Structural Plasticity Gating)  <a id="vdm-a-007"></a>
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

- Internal state only (thresholds, histories, counters)

> DEBT: Tests absent for threshold adaptation / activity damping; add regression coverage.  

---

## I/O Pipelines & Data Products Generation

#### VDM-A-008 — Fluid Dynamics Walker (LBM Telemetry Agent)  <a id="vdm-a-008"></a>
>
> Type: INSTRUMENT • Binding: PSEUDOCODE • State: read-only • Dependencies: bilinear interp/div/vort (EQUATIONS TODO) • Notes: publishes petitions

**Context:** derivation/code/physics/fluid_dynamics/telemetry/walkers.py:57-100 • Commit: 7498744 • Module: physics/fluid_dynamics/telemetry

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

#### VDM-A-009 — Advisory Policy (Fluids Telemetry Feedback)  <a id="vdm-a-009"></a>
>
> Type: POLICY • Binding: PSEUDOCODE • State: none • Dependencies: none • Notes: advisory only; caller applies or ignores

**Context:** derivation/code/physics/fluid_dynamics/telemetry/walkers.py:162-219 • Commit: 7498744 • Module: physics/fluid_dynamics/telemetry

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

## Initialization / Reset / Checkpoint / Restore

#### VDM-A-010 — Checkpoint Save (Periodic Snapshot with Retention)  <a id="vdm-a-010"></a>
>
> Type: RUNTIME • Binding: PSEUDOCODE • State: writes files • Dependencies: none • Notes: periodic snapshot + retention

**Context:** fum_rt/runtime/helpers/checkpointing.py:16-50 • Commit: 7498744 • Module: runtime/helpers

**Role:** Save checkpoint and run retention policy when configured; mirrors original behavior.

**Inputs:**

- nx: Nexus-like object (connectome, adc, logger, run_dir, checkpoint_every, checkpoint_keep)
- step: current tick index

**Depends on equations:**

- (none; IO operation only)

**Pseudocode:**

```text
SAVE CHECKPOINT:
  IF checkpoint_every > 0 AND (step % checkpoint_every == 0) AND step > 0:
    - path = save_checkpoint(run_dir, step, connectome, fmt, adc)
                                                             # checkpointing.py:23
    - Log: "checkpoint_saved" with path and step            # checkpointing.py:31

RETENTION:
  IF checkpoint_keep > 0:
    - summary = prune_checkpoints(run_dir, keep=checkpoint_keep, last_path=path)
                                                             # checkpointing.py:36
    - Log: "checkpoint_retention" with summary              # checkpointing.py:38
```

**Preconditions:**

- nx.run_dir exists and is writable
- nx.connectome is serializable (HDF5 or NPZ format)

**Postconditions/Invariants:**

- Checkpoint file written to run_dir/ckpt_<step>.{h5,npz}
- Oldest checkpoints pruned to keep only last N

**Concurrency/Ordering:**

- Single-threaded; called from main loop
- Pruning is atomic (filesystem operations)

**Failure/Backoff hooks:**

- Try-except on save_checkpoint (log error, continue)      # checkpointing.py:43
- Try-except on prune_checkpoints (silent no-op)           # checkpointing.py:40

**Emits/Side effects:**

- Files: run_dir/ckpt_<step>.{h5,npz}
- Logs: checkpoint_saved, checkpoint_retention, checkpoint_error

---

#### VDM-A-011 — Lattice Boltzmann Collision (D2Q9 BGK)  <a id="vdm-a-011"></a>
>
> Type: RUNTIME • Binding: PSEUDOCODE • State: writes state • Dependencies: f_eq, void dynamics (EQUATIONS TODO) • Notes: local collision step (BGK)

**Context:** derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:150-250 • Commit: 7498744 • Module: physics/fluid_dynamics/fluids

**Role:** D2Q9 Lattice Boltzmann Method collision step (BGK operator) with optional VDM void dynamics coupling.

**Inputs:**

- f: populations [9, ny, nx] (distribution functions)
- rho, ux, uy: macroscopic fields (density, velocity)
- tau: relaxation time (viscosity control)
- void_enabled: bool (VDM coupling flag)
- void_gain: float (void modulation strength)

**Depends on equations:**

- TODO: add anchor for f_eq (equilibrium distribution) in EQUATIONS.md
- TODO: add anchor for universal_void_dynamics in EQUATIONS.md

**Pseudocode:**

```text
MACROSCOPIC FIELDS:
  - rho = sum_i(f[i])  (density)                            # lbm2d.py:165
  - ux = sum_i(c_ix * f[i]) / rho  (x-velocity)             # lbm2d.py:166
  - uy = sum_i(c_iy * f[i]) / rho  (y-velocity)             # lbm2d.py:167
  - Clamp rho >= rho_floor                                  # lbm2d.py:169
  - IF u_clamp: clamp |u| <= u_clamp                        # lbm2d.py:171

VOID DYNAMICS (optional):
  IF void_enabled:
    - delta_W = universal_void_dynamics(W, t, domain_mod, use_time_dynamics)
                                                             # lbm2d.py:175
    - W = clip(W + delta_W, 0, 1)                           # lbm2d.py:176
    - omega_eff = omega * (1 + void_gain * (W - 0.5))       # lbm2d.py:177
  ELSE:
    - omega_eff = omega  (no void modulation)               # lbm2d.py:179

EQUILIBRIUM:
  - FOR each direction i:
      u_dot_c = ux*c_ix + uy*c_iy                           # lbm2d.py:183
      u_sq = ux^2 + uy^2                                    # lbm2d.py:184
      f_eq[i] = w[i] * rho * (1 + u_dot_c/CS2 + (u_dot_c)^2/(2*CS2^2) - u_sq/(2*CS2))
                                                             # lbm2d.py:185

COLLISION (BGK):
  - f = f - omega_eff * (f - f_eq)                          # lbm2d.py:188

FORCING (optional):
  IF fx != 0 or fy != 0:
    - FOR each direction i:
        F_i = w[i] * (c_i - u) · F / CS2                    # lbm2d.py:192
        f[i] += F_i                                         # lbm2d.py:193
```

**Preconditions:**

- f initialized to equilibrium or valid distributions
- rho, ux, uy consistent with f (sum_i f[i] = rho, etc.)
- tau > 0.5 (stability constraint)

**Postconditions/Invariants:**

- Mass conserved: sum_i(f[i]) = rho
- Momentum conserved (with forcing): sum_i(c_i *f[i]) = rho* u + dt * F

**Concurrency/Ordering:**

- Vectorized NumPy (parallel on multi-core)
- Collision is local (no communication between cells)

**Failure/Backoff hooks:**

- rho clamping to rho_floor (avoid division by zero)       # lbm2d.py:169
- velocity clamping to u_clamp (Mach control)              # lbm2d.py:171

**Emits/Side effects:**

- Updates f in-place (populations)
- Updates rho, ux, uy (macroscopic fields)
- Updates W (VDM void field) if void_enabled

---

## Control Plane / Gating / Budget Schedulers

#### VDM-A-012 — Phase Control Polling  <a id="vdm-a-012"></a>
>
> Type: POLICY • Binding: PSEUDOCODE • State: writes runtime params • Dependencies: none • Notes: external phase.json polling (optional)

**Context:** fum_rt/runtime/phase.py (called from loop/main.py:550) • Commit: 7498744 • Module: runtime/phase

**Role:** Poll external phase.json file for dynamic control plane updates (optional; silent no-op if absent).

**Inputs:**

- nx: Nexus-like object (run_dir, phase profiles, dom_mod, etc.)

**Depends on equations:**

- (none; control plane only)

**Pseudocode:**

```text
POLL CONTROL:
  - path = run_dir / "phase.json"                           # phase.py:?
  IF path exists:
    - Load JSON: {"profile": str}                           # phase.py:?
    - IF profile in nx._phase_profiles:
        - Apply profile: nx._apply_phase_profile(prof)      # phase.py:?
        - Update: nx.dom_mod, nx.hz, etc.                   # phase.py:?
    - Log: "phase_update" with profile name                 # phase.py:?
```

**Preconditions:**

- nx.run_dir exists
- nx._phase_profiles dict initialized (default or custom)

**Postconditions/Invariants:**

- nx.dom_mod, nx.hz updated if profile found
- No changes if file absent or profile unknown

**Concurrency/Ordering:**

- Called once per tick from main loop
- File read is atomic (OS-level)

**Failure/Backoff hooks:**

- Try-except on file read (silent no-op)
- Try-except on JSON parse (silent no-op)

**Emits/Side effects:**

- Logs: phase_update (if profile applied)

---

<!-- markdownlint-disable MD033 -->
## Physics Integrators & QC — Metriplectic

### VDM-A-013 — Metriplectic Step — Strang JMJ Composition  <a id="vdm-a-013"></a>
>
> Type: RUNTIME • Binding: PSEUDOCODE • State: writes state • Dependencies: J-step, DG M-step • Notes: symmetric second-order

**Context:** Derivation/code/physics/metriplectic/compose.py:33-47 • Commit: HEAD • Module: physics/metriplectic

**Role:** Apply one Strang composition step combining conservative J and dissipative M: J(Δt/2) → M(Δt) → J(Δt/2).

**Inputs:**

- W: state vector/field
- dt, dx: timestep and grid spacing
- params: includes c for J; D, r, u and DG tolerances for M

**Depends on equations:**

- [VDM-E-014](EQUATIONS.md#vdm-e-014) — Continuum Klein-Gordon form (J branch context)
- [VDM-E-015](EQUATIONS.md#vdm-e-015) — RD gradient-flow form (M branch context)
- [VDM-E-026](EQUATIONS.md#vdm-e-026) — Discrete Gradient Lyapunov step (DG monotonicity)

**Pseudocode:**

```text
INPUT: W, dt, dx, params
W1 = J_step(W, 0.5*dt, dx, params)
W2 = M_step_DG(W1, dt, dx, params)      # robust Newton/backtracking
W3 = J_step(W2, 0.5*dt, dx, params)
RETURN W3
```

**Preconditions:**

- J_step and M_step_DG available; params carry required coefficients

**Postconditions/Invariants:**

- Single full step advanced; DG monotonicity enforced inside M

**Concurrency/Ordering:** sequential

**Failure/Backoff hooks:**

- DG M-step returns convergence stats; caller may react

---

### VDM-A-014 — J-only Reversibility Check (Metriplectic QC)  <a id="vdm-a-014"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: read-only (on diagnostics) • Dependencies: J-step • Notes: measures time-reversal and L2 norm drift

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:91-140 • Commit: HEAD • Module: physics/metriplectic

**Role:** Validate spectral J-step time-reversal and L2 stability by advancing dt then reversing −dt and comparing to initial state; log caps and bounds.

**Inputs:**

- StepSpec (grid N, dx; dt_sweep for min dt); params (seed_scale; strict/cap tolerances)

**Depends on equations:**

- [VDM-E-014](EQUATIONS.md#vdm-e-014) — Continuum Klein-Gordon form
- [VDM-E-047](EQUATIONS.md#vdm-e-047) — Continuum energy density (Hamiltonian)

**Pseudocode:**

```text
W0 ← rng_field(N, seed_scale, seed=17)
W1 = J_step(W0, dt)
W2 = J_step(W1, -dt)
rev_err = ||W2 - W0||_∞
L2 drifts = | ||W1||_2 - ||W0||_2 |, | ||W2||_2 - ||W0||_2 |
passes_strict = (rev_err <= tol_rev_strict) ∧ (L2 drifts <= tol_l2)
cap_ok        = (rev_err <= tol_rev_cap)    ∧ (L2 drifts <= tol_l2)
log JSON with errors, tolerances, FFT roundoff bound; route failed artifacts if !passes_strict
```

**Preconditions:** dt = min(dt_sweep); J_step configured

**Postconditions:** Diagnostics logged; no state persisted

**Emits/Side effects:** JSON log under outputs/logs/metriplectic

---

### VDM-A-015 — Lyapunov Per-Step Series (M-only / JMJ)  <a id="vdm-a-015"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: read-only (on diagnostics) • Dependencies: DG Lyapunov L_h • Notes: check ΔL_h ≤ 0 per step

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:142-190 • Commit: HEAD • Module: physics/metriplectic

**Role:** Evolve for 20 steps using selected scheme (m_only or jmj) and verify discrete Lyapunov decreases monotonically within tolerance.

**Inputs:**

- StepSpec (scheme, grid, params); dt = min(dt_sweep)

**Depends on equations:**

- [VDM-E-016](EQUATIONS.md#vdm-e-016) — RD Lyapunov functional (continuum)
- [VDM-E-092](EQUATIONS.md#vdm-e-092) — Discrete Lyapunov functional (grid form)

**Depends on equations:**

- [VDM-E-090](EQUATIONS.md#vdm-e-090) — Two-grid error metric and log–log fit

**Pseudocode:**

```text
W ← rng_field(N, seed_scale, 123)
L_prev = L_h(W)
series = []
repeat k=1..20:
  W = step(W, dt)               # scheme: m_only or jmj
  L_now = L_h(W)
  series.append(ΔL = L_now - L_prev)
  L_prev = L_now
violations = count(ΔL > tol_pos)
log JSON + PNG (ΔL vs step); route failed if violations>0
```

**Postconditions:** series and violations logged; figure saved

---

### VDM-A-016 — Two-Grid Error Sweep (M-only / JMJ)  <a id="vdm-a-016"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: read-only • Dependencies: two_grid_error_inf • Notes: log-log fit slope and R²

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:58-118 • Commit: HEAD • Module: physics/metriplectic

**Role:** For each dt in sweep and across seeds, compute inf-norm two-grid error and fit slope p and R² on log-log axes; gate by thresholds.

**Inputs:** StepSpec (scheme, grid, params, dt_sweep, seeds)

**Depends on equations:**

- [VDM-E-090](EQUATIONS.md#vdm-e-090) — Two-grid error metric and log–log fit

**Pseudocode:**

```text
step = select_stepper(scheme)
for seed in seeds:
  W0 = rng_field(...)
  for dt in dt_sweep:
    e = ||Φ_dt(W0) - Φ_{dt/2}( Φ_{dt/2}(W0) )||_∞
    append e under dt
med(dt) = median over seeds
if scheme==j_only and med≈0: slope=0, R2=1 (trivial)
else: fit y=log med, x=log dt via least squares → slope,R2
failed_gate = (slope < slope_min) or (R2 < gate_R2)
emit PNG/CSV/JSON; route failed if gate fails
```

**Emits:** figure_path/log_path under outputs/*/metriplectic (tag-aware)

---

### VDM-A-017 — Small-Δt Sweep with Newton Stats (JMJ)  <a id="vdm-a-017"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: read-only • Dependencies: m_only_step_with_stats • Notes: aggregates DG Newton iterations/backtracks

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:192-263 • Commit: HEAD • Module: physics/metriplectic

**Role:** Repeat two-grid sweep on smaller Δt set while capturing per-step DG Newton statistics from the middle M-step; fit slope and R²; log CSVs.

**Depends on equations:**

- [VDM-E-091](EQUATIONS.md#vdm-e-091) — Strang composition defect

**Pseudocode:**

```text
dt_vals_small = params.dt_sweep_small or [0.02,0.01,0.005,0.0025,0.00125]
for seed, dt in grid(seeds, dt_vals_small):
  step_with_stats: J(½dt) → M(dt, capture {iters,residual,backtracks,converged}) → J(½dt)
  e = two_grid_error_inf(step_with_stats, W0, dt)
accumulate medians; fit slope,R2; gate (slope≥2.9,R2≥0.999)
emit PNG + JSON + two CSVs (errors, Newton stats)
```

---

### VDM-A-018 — Strang Defect Diagnostic (JMJ vs MJM)  <a id="vdm-a-018"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: read-only • Dependencies: jmj_strang_step, mjm_strang_step • Notes: proxy for commutator strength

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:265-316 • Commit: HEAD • Module: physics/metriplectic

**Role:** Measure ||Φ^JMJ_Δt − Φ^MJM_Δt||_∞ vs Δt, fit slope (~3 expected) and R²; emit PNG/CSV/JSON.

**Depends on equations:**

- [VDM-E-090](EQUATIONS.md#vdm-e-090) — Two-grid error metric and log–log fit
- [VDM-E-092](EQUATIONS.md#vdm-e-092) — Discrete Lyapunov functional (grid form)

**Pseudocode:**

```text
for seed, dt in grid(seeds, dt_vals):
  W_jmj = JMJ_step(W0, dt)
  W_mjm = MJM_step(W0, dt)
  def_err = ||W_jmj - W_mjm||_∞
median per dt → fit log-log slope,R2; log artifacts
```

---

### VDM-A-019 — Robustness v5 Grid (Param Sweep Aggregator)  <a id="vdm-a-019"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: read-only • Dependencies: VDM-A-016, VDM-A-015 • Notes: pass-rate across (D,r,u,N)

**Context:** Derivation/code/physics/metriplectic/run_metriplectic.py:318-371 • Commit: HEAD • Module: physics/metriplectic

**Role:** Evaluate a small grid of tuples for slope/R² and Lyapunov violations; pass if ≥80% tuples meet all gates; log per-tuple CSV.

**Pseudocode:**

```text
for tup in tuples:
  local_spec = override(grid.N, params.{D,r,u})
  sw = two_grid_sweep(local_spec)
  ly = lyapunov_check(local_spec)
  ok = (sw.slope≥2.9) ∧ (sw.R2≥0.999) ∧ (ly.violations==0)
pass_rate = (#ok)/(#tuples); emit JSON+CSV; route failed if pass_rate<0.8
```

---

## Physics Validation — Cosmology

### VDM-A-020 — FRW Continuity Residual QC (Dust Control)  <a id="vdm-a-020"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: writes artifacts • Dependencies: finite-diff • Notes: machine-precision identity under synthetic dust

**Context:** Derivation/code/physics/cosmology/run_frw_balance.py:1-118 • Commit: HEAD • Module: physics/cosmology

**Role:** Compute residual r(t)=d/dt(ρ a^3)+w ρ d/dt(a^3) with w=0 (dust), report RMS and gate; emit PNG/CSV/JSON with pass/fail routing.

**Inputs:** FRWSpec {rho,a,t,tol_rms,tag}

**Depends on equations:**

- [VDM-E-093](EQUATIONS.md#vdm-e-093) — FRW continuity residual (dust) and RMS

**Pseudocode:**

```text
res = gradient(rho*a^3, t) + w * rho * gradient(a^3, t)   # w=0
rms = sqrt(mean(res^2))
passed = (rms <= tol_rms)
emit PNG(res vs t), CSV(t,rho,a,res), JSON({rms,passed});
if !passed: emit CONTRADICTION_REPORT and route to failed_runs/
```

**Pre/Post:** deterministic synthetic baseline; double precision; artifacts pinned

---

## Physics Validation — Collapse / Memory Steering

### VDM-A-021 — A6 Scaling Collapse (Junction Logistic Universality)  <a id="vdm-a-021"></a>
>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: writes artifacts • Dependencies: run_junction_logistic • Notes: envelope metric gate

**Context:** Derivation/code/physics/collapse/run_a6_collapse.py:1-154 • Commit: HEAD • Module: physics/collapse

**Role:** Generate P(A) curves for multiple Θ, reparameterize X=Θ Δm, compute envelope E(X) across curves and env_max; gate by threshold and emit artifacts.

**Inputs:** A6Spec {tuples:[{theta, delta_m_values, trials}], tag}

**Depends on equations:**

- [VDM-E-067](EQUATIONS.md#vdm-e-067) — Logistic junction choice probability
- [VDM-E-094](EQUATIONS.md#vdm-e-094) — Scaling-collapse envelope and env_max

**Pseudocode:**

```text
for tup in tuples:
  X, P = run_junction_logistic(theta, delta_m_values, trials)
  store curves
Xc, Ymin, Ymax = compute_envelope(curves, nbins)
envelope = Ymax - Ymin; env_max = max(envelope)
passed = (env_max <= 0.02)
emit PNG overlay + envelope band; CSV(Xc,Ymin,Ymax,envelope); JSON(log)
if !passed: CONTRADICTION_REPORT and failed_runs/
```

**Helper (compute_envelope):** build shared X-grid over intersection range; interp each curve; take pointwise min/max.

---

<!-- BEGIN AUTOSECTION: ALGO-INDEX -->
<!-- Tool-maintained list of [VDM-A-###](#vdm-a-###) anchors for quick lookup -->
- [VDM-A-001](#vdm-a-001) — Runtime Main Loop (Nexus Tick Loop)
- [VDM-A-002](#vdm-a-002) — Connectome Step (Void-Equation Driven Topology Update)
- [VDM-A-003](#vdm-a-003) — Void Scout Runner (Per-Tick Scout Executor)
- [VDM-A-004](#vdm-a-004) — Cold Scout (Coldness-Driven Walker)
- [VDM-A-005](#vdm-a-005) — Alias Sampling (Vose's Method)
- [VDM-A-006](#vdm-a-006) — RE-VGSP Learning Step (Three-Factor Synaptic Plasticity)
- [VDM-A-007](#vdm-a-007) — GDSP Adaptive Thresholds (Structural Plasticity Gating)
- [VDM-A-008](#vdm-a-008) — Fluid Dynamics Walker (LBM Telemetry Agent)
- [VDM-A-009](#vdm-a-009) — Advisory Policy (Fluids Telemetry Feedback)
- [VDM-A-010](#vdm-a-010) — Checkpoint Save (Periodic Snapshot with Retention)
- [VDM-A-011](#vdm-a-011) — Lattice Boltzmann Collision (D2Q9 BGK)
- [VDM-A-012](#vdm-a-012) — Phase Control Polling
- [VDM-A-013](#vdm-a-013) — Metriplectic Step — Strang JMJ Composition
- [VDM-A-014](#vdm-a-014) — J-only Reversibility Check (Metriplectic QC)
- [VDM-A-015](#vdm-a-015) — Lyapunov Per-Step Series (M-only / JMJ)
- [VDM-A-016](#vdm-a-016) — Two-Grid Error Sweep (M-only / JMJ)
- [VDM-A-017](#vdm-a-017) — Small-Δt Sweep with Newton Stats (JMJ)
- [VDM-A-018](#vdm-a-018) — Strang Defect Diagnostic (JMJ vs MJM)
- [VDM-A-019](#vdm-a-019) — Robustness v5 Grid (Param Sweep Aggregator)
- [VDM-A-020](#vdm-a-020) — FRW Continuity Residual QC (Dust Control)
- [VDM-A-021](#vdm-a-021) — A6 Scaling Collapse (Junction Logistic Universality)
<!-- END AUTOSECTION: ALGO-INDEX -->

## Change Log

- 2025-10-08 • add VDM-A-013..021 (metriplectic integrators & QC; FRW residual QC; A6 collapse) • HEAD
- 2025-10-03 • initial algorithms extracted • 7498744

<!-- markdownlint-enable MD033 -->
