# VDM Wiring Audit — ADC, Gates, and Single-Writer (Read-Only)

**Mission**: Map how ADC (territories), gates (b1/hysteresis), and GDSP (single writer) are wired in the current code. Evidence-only report of current implementation patterns.

## 1) ADC Presence & API

### Files/Classes/Functions Defining ADC/Territories:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/core/adc.py:96 | class ADC | create/update/query | "Active Domain Cartography — incremental, void-faithful reducer" |
| fum_rt/core/adc.py:64 | class Territory | data structure | "Coarse concept regions indexed by (domain_hint, coverage_id)" |
| fum_rt/core/adc.py:137 | ADC._territory_for() | create | "key = (str(domain_hint or ''), int(cov_id))" |
| fum_rt/core/adc.py:110 | ADC.update_from() | update | "for o in observations: if kind == 'region_stat'" |
| fum_rt/core/adc.py:123 | ADC.get_metrics() | query | "return {'adc_territories': int(terr_count)}" |

### Territory Creation/Update/Query APIs:

**Creation**: `ADC._territory_for(domain_hint, cov_id)` creates territories with composite key `(domain_hint, coverage_id)` at line 137-144. New territories get sequential ID `self._id_seq += 1`.

**Updates**: `ADC.update_from(observations)` processes Observation events at line 110-121. Territory reinforcement via `Territory.reinforce()` at line 73-78 with EWMA stats (w_mean/var, s_mean), mass accumulation, confidence boost.

**Queries**: `ADC.get_metrics()` at line 123-133 returns territory count, boundary count, cycle hits. No direct territory lookup API exposed.

## 2) Territory Signals & Priors

### Territory Priors/Budgets/Gains Definition:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/core/adc.py:97 | ADC.__init__(r_attach=0.25) | growth bias | "r_attach: float = 0.25, ttl_init: int = 120" |
| fum_rt/core/adc.py:150 | add_mass calculation | edit weight | "add_mass = max(1.0, float(len(o.nodes)))" |
| fum_rt/core/adc.py:151 | add_conf = 0.02 | confidence gain | "add_conf = 0.02" |
| fum_rt/core/adc.py:70-71 | Territory EWMA alpha | learning rate | "w_stats: _EWMA = field(default_factory=lambda: _EWMA(alpha=0.15))" |

### Walker/Scoreboard Access:

**Unknown** (looked in fum_rt/core/cortex/void_walkers/runner.py, fum_rt/runtime/loop/main.py). No direct evidence of walkers reading territory priors. Walkers emit Observation events but don't consume territory budgets/gains.

Territory priors appear to be internal to ADC module - no external API for walkers to read growth bias or edit weights.

## 3) Boundary Updates

### Publishers and Topics:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/core/adc.py:155 | ADC._accumulate_boundary() | publisher | "boundary_probe: update boundary signal" |
| fum_rt/core/announce.py:49 | cut_strength field | signal payload | "Boundary-specific signal (strength of cut)" |
| fum_rt/runtime/loop/main.py:485 | bus.publish(_o) | event transport | "if bus is not None: bus.publish(_o)" |

### Update Frequency and TTLs:

**Frequency**: Per-tick via `ADC.update_from()` at line 110. Each boundary_probe observation triggers immediate boundary update.

**TTL**: Boundaries have TTL initialized to `ttl_init=120` at line 87, decays by 1 per `_decay()` call (line 200-201). Boundaries with `ttl <= 0` and weak cut_strength get garbage collected.

### Consumers:

**Unknown** (looked in fum_rt/runtime/loop/main.py, fum_rt/core/neuroplasticity/gdsp.py). No evidence of boundary consumers. Boundary data appears to be contained within ADC module only.

**Timer/Cron**: No boundary recompute timers found. Updates are event-driven only via walker announcements.

**Scoreboard**: No scoreboard implementation found in codebase search. The event-sourced structural plasticity plan mentions scoreboard concept but no implementation exists.

## 4) Gating (b1 + hysteresis + refractory)

### B1 Computation and Thresholds:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/core/void_b1.py:76 | class VoidB1Meter | b1 computation | "Streaming surrogate for B1 with Euler-rank estimate" |
| fum_rt/core/void_b1.py:374 | update_void_b1() | entry point | "Module-level helper to update and return topology packet" |
| fum_rt/core/void_b1.py:85 | alpha = _alpha_from_half_life | smoothing | "EMA half-life for void_b1 smoothing" |
| fum_rt/core/signals.py:60 | apply_b1_detector() | gating logic | "z = det.update(b1_value, tick=int(step))" |

### Hysteresis and Refractory:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/runtime/loop/main.py:300 | hysteresis parameter | threshold control | "hysteresis = float(getattr(det, 'hysteresis', 1.0))" |
| fum_rt/core/signals.py:67 | b1_spike detection | refractory gate | "m['b1_spike'] = bool(z.get('spike', False))" |
| fum_rt/runtime/loop/main.py:197 | b1_spike gating | GDSP trigger | "if not (b1_spike or abs(td) >= td_thr or comp > 1)" |

### UTD/UTE Integration:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/io/utd.py:9 | class UTD | output system | "Universal Transduction Decoder" |
| fum_rt/io/ute.py:4 | class UTE | input system | "Universal Temporal Encoder" |
| fum_rt/nexus.py:162 | self.ute = UTE() | integration | Nexus instantiates UTE/UTD |
| fum_rt/nexus.py:163 | self.utd = UTD() | integration | Run directory output sink |

**UTD Externalization**: UTD found as output system (fum_rt/io/utd.py) but no evidence of externalization checks reading b1 gates. No pointer discipline or taskness hooks connecting gating to UTD emission found.

## 5) GDSP as Single Writer

### Patch Operations:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/core/neuroplasticity/gdsp.py:25 | class GDSPActuator | single writer | "Goal-Directed Structural Plasticity actuator" |
| fum_rt/core/neuroplasticity/gdsp.py:118 | _grow_connection_across_gap() | connect op | "Bridge a topological gap by adding single best edge" |
| fum_rt/core/neuroplasticity/gdsp.py:242 | _prune_connections_in_locus() | cut op | "W[global_row, global_col] = 0" |
| fum_rt/core/neuroplasticity/gdsp.py:447 | run_gdsp_synaptic_actuator() | entry point | "Legacy-compatible wrapper (emergent-only trigger)" |

### Budget Accounting:

| File:Line | Symbol | Role | Evidence |
|-----------|--------|------|----------|
| fum_rt/core/neuroplasticity/gdsp.py:103 | bridge_budget_nodes | node budget | "bridge_budget_nodes: int = 128" |
| fum_rt/core/neuroplasticity/gdsp.py:103 | bridge_budget_pairs | pair budget | "bridge_budget_pairs: int = 2048" |
| fum_rt/core/neuroplasticity/gdsp.py:149 | k1 = min(len(comp1_nodes), self._bridge_nodes) | budget enforcement | "Sample bounded node sets" |

### Counterfactual Pre-check:

**Unknown** (looked in fum_rt/core/neuroplasticity/gdsp.py). No evidence of counterfactual pre-checks before applying patch operations. Operations appear to execute directly without rollback capability.

## 6) Mutation Bypass Scan

### Non-GDSP Mutations:

| File:Line | Symbol | Kind | Via GDSP? | Expected? |
|-----------|--------|------|-----------|-----------|
| fum_rt/core/neuroplasticity/gdsp.py:175 | W.tolil() | weight | Y | Y |
| fum_rt/core/neuroplasticity/gdsp.py:176 | W[global_row, global_col] = 0 | weight | Y | Y |
| fum_rt/core/neuroplasticity/gdsp.py:177 | W.tocsr() | topology | Y | Y |

**Search Results**: No non-GDSP mutations found in current codebase scan. All weight/topology mutations appear to go through GDSPActuator methods. No direct NetworkX mutations, index_put_, or scatter_ operations detected.

**Note**: Growth arbiter found in fum_rt/core/fum_growth_arbiter.py with void debt accumulation, but no topology mutations - only neuron count decisions.

## 7) Dataflow: Territory → Gate → GDSP

### Concrete Call Paths:

```
[ADC] fum_rt/core/adc.py:110 update_from(observations)
  ↓
[Gate] fum_rt/core/signals.py:60 apply_b1_detector(metrics)
  ↓  
[GDSP] fum_rt/runtime/loop/main.py:197 _maybe_run_gdsp(nx, metrics, step)
```

**Evidence**:
- fum_rt/runtime/loop/main.py:414: ADC metrics computed via `nx.adc.get_metrics()`
- fum_rt/runtime/loop/main.py:462: B1 detector applied via `_apply_b1d(nx, metrics, step)`  
- fum_rt/runtime/loop/main.py:197: GDSP triggered by `b1_spike or abs(td) >= td_thr`

**ASCII Flow**:
```
Walkers → Observations → ADC.update_from() → territory stats
                                   ↓
B1Meter.update() → void_b1 → apply_b1_detector() → b1_spike
                                   ↓
_maybe_run_gdsp() → GDSPActuator.run() → synaptic edits
```

**Missing Links**: No direct territory stats → gate influence found. Territory data doesn't feed into b1 calculation or GDSP budgets.

## 8) Runtime Flags & Telemetry

### Environment Variables:

| Flag | Purpose | File:Line | Evidence |
|------|---------|-----------|----------|
| ENABLE_GDSP | Enable GDSP actuator | fum_rt/runtime/loop/main.py:173 | "if not _truthy(os.getenv('ENABLE_GDSP', '0'))" |
| GDSP_TD_THRESH | TD error threshold | fum_rt/runtime/loop/main.py:190 | "td_thr = float(os.getenv('GDSP_TD_THRESH', '0.2'))" |
| GDSP_T_PRUNE | Pruning timer | fum_rt/runtime/loop/main.py:237 | "T_prune = int(os.getenv('GDSP_T_PRUNE', '100'))" |
| GDSP_PRUNE_THRESHOLD | Prune weight limit | fum_rt/runtime/loop/main.py:241 | "pruning_threshold = float(os.getenv('GDSP_PRUNE_THRESHOLD', '0.01'))" |

### Current Logs Emitted:

| Metric | File:Line | Evidence |
|--------|-----------|----------|
| adc_territories | fum_rt/core/adc.py:130 | "adc_territories': int(terr_count)" |
| adc_boundaries | fum_rt/core/adc.py:131 | "adc_boundaries': int(bnd_count)" |
| b1_spike | fum_rt/core/signals.py:67 | "m['b1_spike'] = bool(z.get('spike', False))" |
| void_b1 | fum_rt/core/void_b1.py:280 | "'void_b1': [0,1]" |

### Missing Logs:

- Territory boundary update events (no TTL/boundary change telemetry)
- GDSP budget consumption tracking (bridge_budget usage not logged)
- Gate refractory hits (hysteresis state transitions not recorded)
- Δenergy per GDSP commit (no energy accounting found)

## 9) Wiring Gaps (Ranked)

| File:Line | Gap Description | Severity | Minimal Fix |
|-----------|-----------------|----------|-------------|
| fum_rt/core/adc.py:123 | No territory→walker API | High | Add get_territories() method |
| fum_rt/runtime/loop/main.py:197 | Territory data unused in GDSP gating | High | Pass territory_indices to GDSP |
| fum_rt/core/adc.py:155 | Boundary data isolated | Med | Expose boundary metrics to scoreboard |
| fum_rt/core/signals.py:31 | B1 ignores territory structure | Med | Territory-weighted B1 computation |
| fum_rt/core/neuroplasticity/gdsp.py:447 | No counterfactual checks | Low | Add pre-check validation |

## 10) Speculative Synthesis (allowed here only)

**Likely Intended Wiring**:

• ADC territories should bias walker attention through territory-scoped seeding and budget allocation
• Territory priors (growth bias, edit weights) should influence walker exploration policies and step budgets  
• Boundary strength should feed into gate computation as additional topological signal beyond raw B1
• Gates should enforce task/pointer discipline by blocking GDSP operations during high cognitive load
• Territory budgets should constrain GDSP operations to prevent destructive global edits
• Scoreboard should accumulate walker events within territory boundaries for localized decision making
• GDSP should operate within territory masks to preserve inter-territory structure
• Territory TTL decay should drive exploratory walker dispatch to under-sampled regions
• Boundary updates should trigger rebalancing of walker allocation across territory interfaces  
• Gate hysteresis should prevent rapid GDSP oscillations during territory boundary stabilization

**Critical Changes for Self-Organization**:

• Wire territory metrics into walker budget allocation (high ROI, restores morphology-driven exploration)
• Add territory-scoped GDSP budgets and masks (medium ROI, prevents destructive global edits)  
• Integrate boundary strength into B1 gate computation (medium ROI, improves topological sensitivity)

**Architecture Intent**: ADC provides spatial organization, gates provide temporal discipline, GDSP provides structural adaptation - but current wiring lacks the feedback loops to enable coordinated self-organization across these three subsystems.