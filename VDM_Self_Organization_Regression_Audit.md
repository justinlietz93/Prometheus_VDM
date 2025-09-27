# VDM Self-Organization Regression — Single-File Audit

Mission: Identify exactly why the current code no longer produces the demo morphologies
("nucleus + dendrites + sparse bridges") and list the smallest fixes. Evidence only.

## 1) Golden Demo Recipe

**Original demo config found in:**
- File: `derivation/supporting_work/external_references/logs/FUM_Demo_run_log_20250731.txt:3`
- Quote: "Initialized a k-NN graph with 8000 synapses (k=8)"
- File: `derivation/supporting_work/external_references/logs/FUM_Demo_run_log_20250731.txt:8`
- Quote: "Avg. Weight Magnitude: 0.1502 (Target: ~0.15)"

**Golden parameters extracted:**
- k-NN substrate: k=8, N=1000 (inferred from 8000 synapses), seed=42 (from substrate code)
- Threshold: ~0.15 (target weight magnitude)
- E/I ratio: 0.81/0.19 (Target: 0.80/0.20)
- Tau_m: mean=19.97, std=1.38
- V_thresh: mean=-54.96, std=1.46
- Initial sparsity: 0.9920

**Original stimuli config:**
- File: `derivation/supporting_work/external_references/logs/FUM_Demo_run_log_20250731.txt:26-29`
- Total stimuli: 1000, Type distribution: {'graph': 341, 'math': 320, 'logic': 339}
- Expression depth: 3.00, Graph density: 0.4611

**Missing:** Original seed value, exact hysteresis params, TTL values, bridge budgets

## 2) Current Runtime Knobs

**Thresholds (activation/deactivation):**
- File: `fum_rt/core/sparse_connectome.py:52`
- Quote: "threshold: float = 0.15" (default on/off threshold)
- File: `fum_rt/runtime/loop/main.py:182`
- Quote: "td_thr = float(os.getenv("GDSP_TD_THRESH", "0.2"))" (GDSP trigger threshold)

**GDSP Budgets:**
- File: `fum_rt/core/neuroplasticity/gdsp.py:117`
- Quote: "bridge_budget_nodes: int = 128, bridge_budget_pairs: int = 2048"
- File: `fum_rt/core/sparse_connectome.py:300`
- Quote: "B = int(getattr(self, "bridge_budget", 8))" (bridge budget per tick)

**Fragmentation Audit:**
- File: `fum_rt/core/sparse_connectome.py:278`
- Quote: "_budget = int(_os.getenv("FRAG_AUDIT_EDGES", "200000"))"

**RNG Seeding:**
- File: `fum_rt/core/substrate/substrate.py:25`
- Quote: "self.rng = np.random.default_rng(seed=42)" (hardcoded seed)
- File: `fum_rt/core/neuroplasticity/gdsp.py:120`
- Quote: "self._rng = np.random.default_rng(int(rng_seed))" (GDSP uses separate seed)

**Refractory periods:**
- File: `fum_rt/core/substrate/substrate.py:49`
- Quote: "refractory_period_np = np.full(num_neurons, 5.0)" (5ms refractory)

**Locality masks:**
- File: `fum_rt/core/sparse_connectome.py:64`
- Quote: "candidates: int = 64" (neighborhood selection size)

## 3) Single-Writer Authority

**Functions that mutate topology/weights/state:**

| File:Line | Symbol | Kind | Via GDSP? |
|-----------|--------|------|-----------|
| sparse_connectome.py:275 | step() | topology | N |
| sparse_connectome.py:300-350 | bridging logic | topology | N |
| neuroplasticity/gdsp.py:222 | trigger_homeostatic_repairs | topology | Y |
| neuroplasticity/gdsp.py:295 | _grow_connection_across_gap | topology | Y |
| neuroplasticity/gdsp.py:342 | _execute_reinforcement_growth | topology | Y |
| neuroplasticity/gdsp.py:386 | _execute_exploratory_growth | topology | Y |
| neuroplasticity/gdsp.py:463 | trigger_maintenance_pruning | topology | Y |
| substrate/substrate.py:186 | apply_intrinsic_plasticity | state | N |
| void_dynamics_adapter.py | delta_re_vgsp, delta_gdsp | weights | N |

**Authority concern:** Multiple non-GDSP writers (sparse_connectome bridging, substrate IP, void dynamics) operate outside GDSP coordination.

## 4) Locality & Dense Ops

**High severity (tick-path):**
- File: `fum_rt/core/void_b1.py:195`
- Dense fallback for small-N: "_update_dense()" - uses masks, acceptable for validation only

**Medium severity (maintenance):**
- File: `fum_rt/core/sparse_connectome.py:372`
- Quote: "self._maybe_audit_frag(int(_budget))" - bounded edge scanning with budget=200000

**Low severity:**
- Most operations use adjacency lists or streaming over active edges
- No obvious all-nodes loops in tick path identified

## 5) Gates & Hysteresis

**b1 computation:**
- File: `fum_rt/core/void_b1.py:195`
- b1 computed via sparse sampling or dense fallback for small N
- File: `fum_rt/runtime/loop/main.py:173`
- Quote: "b1_spike = bool(metrics.get("b1_spike", metrics.get("evt_b1_spike", False)))"

**On/off thresholds:**
- File: `fum_rt/core/sparse_connectome.py:52`
- Threshold=0.15 for edge activation (W[i]*W[j] > threshold)
- No explicit hysteresis mechanism found - **POTENTIAL CHATTER RISK**

**Refractory windows:**
- File: `fum_rt/core/substrate/substrate.py:49`
- Fixed 5.0ms refractory period
- File: `fum_rt/core/substrate/substrate.py:150-186`
- Intrinsic plasticity adjusts thresholds but no hysteresis

**Signs of never-on:** Threshold comparison may be too restrictive without proper scaling

## 6) Queues & Budgets

**GDSP budgets present:**
- File: `fum_rt/core/neuroplasticity/gdsp.py:117-120`
- bridge_budget_nodes=128, bridge_budget_pairs=2048 per component bridging
- No backpressure or drop tracking found

**Bridge budget per tick:**
- File: `fum_rt/core/sparse_connectome.py:300`
- B=8 symmetric bridges per tick with attempts cap B*64=512

**Audit budget:**
- File: `fum_rt/core/sparse_connectome.py:278`
- 200000 edges audit budget with best-effort refresh

**No explicit queue overflow handling detected**

## 7) RNG & Attachment

**Seeding policy:**
- File: `fum_rt/core/substrate/substrate.py:25`
- Hardcoded seed=42 for substrate initialization
- File: `fum_rt/core/sparse_connectome.py:51`
- Connectome uses configurable seed parameter
- **INCONSISTENCY:** Different RNG streams may cause reproducibility issues

**Attachment rules:**
- File: `fum_rt/core/sparse_connectome.py:86-124`
- Alias sampler for candidate selection ~ ReLU(Δalpha)
- File: `fum_rt/core/sparse_connectome.py:325-360`
- Top-k selection by void affinity S_ij for preferential attachment

**Preferential attachment present:** Degree/field-weighted via void affinity scoring

## 8) Visualization vs Structure

**Layout independence confirmed:**
- No layout-dependent morphology generation found
- File: `fum_rt/core/sparse_connectome.py:439`
- snapshot_graph() creates NetworkX for visualization only
- Structure determined by adjacency lists, not layout positions

**No frame-time global layout calls in tick path**

## 9) Minimal Morphology Metrics (available now)

**Degree sketch:** Missing - no binned degree distribution function found
**Clustering sample:** Missing - no clustering coefficient sampling found  
**Path sample:** Missing - no path length sampling found
**Laplacian trace:** Missing - no Laplacian eigenvalue probing found

**Available metrics:**
- File: `fum_rt/core/sparse_connectome.py:387-430`
- connected_components(), cyclomatic_complexity(), active_edge_count()
- File: `fum_rt/core/void_b1.py:195-377`
- void_b1, euler_rank, triangles_per_edge via update_void_b1()

**How to run:** Set environment variables, call connectome.step() - no specific flags found

## 10) Probable Break Points (ranked)

**1. Missing Hysteresis (HIGH)**
- File: `fum_rt/core/sparse_connectome.py:52`
- Description: Single threshold without hysteresis causes edge chatter
- Severity: High - prevents stable morphology formation
- Fix: Add on_threshold=0.15, off_threshold=0.12 with state memory
- Evidence: No hysteresis logic found in activation check

**2. RNG Inconsistency (HIGH)**  
- File: `fum_rt/core/substrate/substrate.py:25` vs sparse_connectome.py:51
- Description: Hardcoded seed=42 vs configurable seed breaks reproducibility
- Severity: High - affects demo replication
- Fix: Use consistent seeding strategy across components
- Evidence: seed=42 hardcoded in substrate, configurable in connectome

**3. GDSP Disabled by Default (HIGH)**
- File: `fum_rt/runtime/loop/main.py:172`
- Description: ENABLE_GDSP defaults to "0", disabling structural plasticity
- Severity: High - no growth/pruning without GDSP
- Fix: Change default to "1" or ensure demo scripts set ENABLE_GDSP=1
- Evidence: "if not _truthy(os.getenv("ENABLE_GDSP", "0"))"

**4. Bridge Budget Too Low (MEDIUM)**
- File: `fum_rt/core/sparse_connectome.py:300`
- Description: Bridge budget=8 per tick may be too low for nucleus formation
- Severity: Medium - limits component connectivity  
- Fix: Increase bridge_budget to 16-32 per tick
- Evidence: Original demo had "sparse bridges" - current budget may prevent this

**5. TD Threshold Too High (MEDIUM)**
- File: `fum_rt/runtime/loop/main.py:182`  
- Description: GDSP_TD_THRESH=0.2 may be too high for triggering
- Severity: Medium - prevents GDSP activation
- Fix: Lower to 0.1 or make adaptive
- Evidence: High threshold with no triggering evidence in logs

**6. Missing k-NN Initialization (LOW)**
- File: Import error for fum_initialization.create_knn_graph
- Description: k-NN graph creation function not found
- Severity: Low - substrate may not initialize properly
- Fix: Implement or fix import path for create_knn_graph
- Evidence: Import statements present but file missing

## 11) Speculative Synthesis (allowed here only)

**Historical working mechanism reconstruction:**

• **Local Growth Engine:** GDSP exploratory growth created dendritic branching through territory-scoped reinforcement and exploration based on eligibility traces and similarity scoring

• **Sparsification Balance:** Maintenance pruning of weak synapses (T_prune=100, threshold=0.01) balanced against bridge formation to maintain sparse connectivity while preventing fragmentation

• **Nucleus Formation:** Multiple components bridged via void-affinity sampler created dense central regions, with bridge_budget controlling connection rate between components  

• **Preferential Attachment:** Alias sampling ~ ReLU(Δalpha) with top-k void affinity S_ij selection created hub formation and degree-weighted growth patterns

• **Hysteresis Stability:** Edge activation hysteresis (likely on=0.15, off=0.12) prevented chatter and allowed stable morphology persistence across ticks

• **Component Cohesion:** b1_spike triggers and component count >1 activated homeostatic repairs, maintaining network connectivity while allowing modular structure

• **Stimulation Drive:** External stimuli (1000 diverse patterns) provided directional growth signals via deterministic symbol→group drive with decay (_stim_decay=0.90)

• **Field Dynamics:** Void dynamics (delta_gdsp, delta_re_vgsp) modulated connection weights based on domain_modulation and temporal dynamics

• **Critical Thresholds:** TD signal threshold (likely 0.1) and b1 persistence >0.9 triggered different plasticity modes (growth vs pruning)

• **RNG Coordination:** Consistent seeding across substrate (seed=42) and connectome enabled reproducible morphology emergence

**Top 3 knobs for fastest restoration:**

1. **Enable GDSP by default** (ENABLE_GDSP=1) - restores all structural plasticity
2. **Add activation hysteresis** (on_threshold=0.15, off_threshold=0.12) - stabilizes morphology
3. **Lower TD threshold** (GDSP_TD_THRESH=0.1) and increase bridge budget (16-32) - enables growth triggering and connectivity

The original "nucleus + dendrites + sparse bridges" morphology likely emerged from the interaction of component bridging (nucleus), exploratory growth (dendrites), and balanced pruning (sparsification), all stabilized by hysteresis and driven by consistent stimulation patterns.