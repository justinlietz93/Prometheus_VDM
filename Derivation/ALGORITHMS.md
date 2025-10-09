<!-- DOC-GUARD: CANONICAL -->
<!-- RULES for maintaining this file are here: /mnt/ironwolf/git/Prometheus_VDM/prompts/algorithms_maintenance.md -->
# VDM Algorithms & Execution Flows (Auto-compiled)

Last updated: 2025-10-09 (commit f1e74a5)

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

#### VDM-A-009 - Advisory Policy (Fluids Telemetry Feedback)  <a id="vdm-a-009"></a>
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

## Change Log

- 2025-10-08 • add VDM-A-013..021 (metriplectic integrators & QC; FRW residual QC; A6 collapse) • HEAD
- 2025-10-03 • initial algorithms extracted • 7498744

<!-- markdownlint-enable MD033 -->

---

### VDM-A-022 - Tube Spectrum and Condensation Harness (Tachyonic Tube v1)  <a id="vdm-a-022"></a>
> Type: EXPERIMENT • Binding: PSEUDOCODE • State: writes artifacts • Dependencies: Bessel evaluations, adaptive quadrature • Notes: QC gates for spectrum coverage and condensation curvature

**Context:** Derivation/code/physics/tachyonic_condensation (runner + solvers) • Commit: f1e74a5

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
