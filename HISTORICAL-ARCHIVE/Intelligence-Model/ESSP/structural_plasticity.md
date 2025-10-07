Got it — I hear you. No dense scans, no accidental enable switches, and no “spike-only” homeostasis. We can do this strictly sparse and event-gated.

```
Classification: Runtime-only
```

## Objective Recap

* Make structural plasticity happen in the **sparse** path (no dense scans), with **multi-signal gating** (not just spikes), and keep it budgeted/territory-scoped.

## Action Plan

* **A. Confirm sparse-only guard is active.** The dense backend hard-fails unless `FORCE_DENSE=1` (so we’re not going to trip into dense by accident).&#x20;
* **B. Wire structural plasticity on the sparse path.** Keep the existing sparse maintenance (adaptive pruning + budgeted bridging) and **add** our actuator hook (GDSP) under a multi-signal gate:

  * Sparse maintenance already does **adaptive pruning** with an edge-local threshold and **budgeted bridging** — both scan-free over the whole matrix (neighbor-set only).&#x20;
  * Add a runtime hook that calls the **GDSPActuator** (repairs, growth, maintenance; all budgeted/CSR-safe) when any of these fire: {topology spike, TD≥τ, fragmentation}. &#x20;
* **C. Gate by multiple signals (not “spikes only”).** Use:

  * **B1 topology spike** (z-detector with hysteresis/cooldown) as one of the triggers, not the only one.&#x20;
  * **TD signal** (structure + traversal) and **cohesion components** as parallel gates (env var `GDSP_TD_THRESH` defaults to 0.2). If none are high and the graph isn’t fragmented, **no structural op** runs.&#x20;
* **D. Territory-scoped edits.** When GDSP triggers, select **bounded territory indices** from the event-folded territory UF (no scans) and operate only there (reinforcement/exploration/pruning). &#x20;
* **E. Keep the existing sparse “light homeostasis.”** Leave SparseConnectome’s adaptive pruning & small-budget bridging in place for baseline stability; they are already scan-free and parameter-bounded.&#x20;
* **F. Do not call dense homeostasis.** The older dense routine (`perform_structural_homeostasis`) stays **off** in sparse; it’s the right shape conceptually (bridge/prune) but lives in the dense path.&#x20;

## Handoff (Physicist Mode implements)

* **Files/paths to create/update:**

  * `fum_rt/runtime/loop/main.py` (or your loop seam): add **GDSP gate** block (see snippet in Plan C/D).
  * `fum_rt/runtime/phase.py` (optional): add knobs `gdsp_enable`, `gdsp_k`, `gdsp_td_thresh`, `bridge_budget`.
  * `fum_rt/core/proprioception/territory.py` is already the UF; ensure loop folds ADC/void-walker events into it.
  * **Do not touch** dense `core/connectome.py` wiring (it hard-fails without `FORCE_DENSE`).&#x20;
* **CLIs to run + seeds:** none special; respect existing env knobs

  * `GDSP_TD_THRESH` (default `0.2`), `GDSP_K` (default `64`), `BRIDGE_BUDGET` for sparse (default `8`).

## Verification

* **No-dense guarantee:** Starting the runtime **without** `FORCE_DENSE` must succeed; importing dense `Connectome` should still raise the “validation-only” error → **PASS** when the error text appears if someone tries it.&#x20;
* **Sparse edits only:** In a run with `N≈5-50k`, confirm:

  * **Adaptive pruning** counters tick (`_last_pruned_count>0` at least once) with **no** global matrix sweep.&#x20;
  * **Bridging** uses **`bridge_budget`** (<=8 per tick by default), not scan-all.&#x20;
* **Multi-signal gating:** Induce any one of {b1 spike, TD≥τ, components>1} and observe a **GDSP call**; with no triggers, **zero calls** (stable plateau). Gate spec & thresholds per the adapter. &#x20;
* **Territory scope:** When GDSP runs, it consumes **bounded** `territory_indices` from the UF sampler, not full graphs.&#x20;
* **Actuator behavior:** Verify GDSP can do **repairs** (fragment gaps), **reinforcement** (eligibility-based), **exploratory** growth (similarity+eligibility prefilter), and **timed pruning** — all **CSR-safe** and budgeted.&#x20;

## Assumptions/Risks

* **Risk (gating too tight):** If `GDSP_TD_THRESH` is high, actuator rarely fires → tune with runs that show sustained TD or explicit fragmentation.&#x20;
* **Risk (territory UF coverage):** Ensure the loop folds event batches from void-walkers/ADC so the UF has members to sample (bounded heads).
* **Assumption:** You want sparse maintenance **and** GDSP; we keep both. Sparse maintenance is cheap and already avoids scans.&#x20;

## Next Steps

1. Add the **GDSP gate** block in the loop (use the existing adapter semantics shown in Plan C/D).&#x20;
2. Ensure **territory UF** is receiving walker/ADC events every tick so `sample_any(K)` returns indices.
3. Expose **phase knobs** for `gdsp_enable`, `gdsp_k`, `gdsp_td_thresh`, `bridge_budget`.
4. Run a **fragmentation case** (components>1): expect budgeted bridges and a GDSP repair tick.
5. Run a **stable case** (no spikes, TD low, single component): expect **no** structural edits.

---

### Why the previous behavior looked “spike-only”

* What we call **B1 “spike”** is a **topology spike detector** (z-score on the first difference of a topology metric with hysteresis/cooldown). It’s **not** synaptic spiking and was only one of the possible gates — we’re now explicitly adding TD and cohesion gates so edits aren’t “spike-only.”&#x20;

### What we can bridge with **sparse**

* The sparse path already supports **adaptive pruning** and **budgeted bridging** with **no dense scans**: it evaluates local weights within neighbor sets and uses a **bridge budget** to add a few edges per tick when fragmented. That’s precisely your constraint.&#x20;

### Not using dense `perform_structural_homeostasis`

* The dense routine shows the **shape** (bridge on S\_ij and prune by mean-based threshold), but remains a **dense** artifact; we keep it off in sparse and do all edits through the sparse path + GDSP actuator.&#x20;

If you want, I’ll draft the exact 12-20-line **GDSP gate** block for your loop with the env/phase knobs and territory sampling call — all sparse and scan-free.




Please read this again, shouldn't we have different types of neurons? more basic neurons might be k=3 or k=4 but more common while more complex neurons like purkinje neurons might have a much higher k and be far more rare.

I think certain types of void walkers should be tagging neurons or synapses as they traverse like they already do, except these tags are sent up to the bus attached to the neurons information so that the global system knows to prune the synapse or cull the neuron. This should work the same way for neural / synapse growth.

We need to make sure there is synapse strengthening and decay if there isn't already as well



"Physiological Triggers (Normal Development)
Synaptic Activity
(Use it or Lose it): The brain eliminates connections, or synapses, that are used infrequently, reinforcing frequently used circuits to increase efficiency and strengthen relevant connections. 
Microglial Engulfment:
Microglia, the brain's immune cells, recognize a specific protein, complement component 3 (C3), attached to synapses slated for removal and consume them, a process known as microglia-mediated pruning. 
Extrinsic Signaling:
Molecules like semaphorins, which are found on cell surfaces and secreted in the brain, act as "retraction inducers," triggering the removal of specific axon branches to fine-tune neural circuits. 
Pathological Triggers (Disease and Injury)
Excitotoxicity:
Overexcitation of neurons by glutamate can lead to excessive calcium influx, causing cell damage and death. 
Ischemia:
A lack of blood flow (ischemia) can induce neuronal death due to high ATP turnover and a lack of cellular energy. 
Traumatic Injury:
Physical trauma can lead to neuronal swelling and death, resulting in extensive brain damage. 
Apoptosis:
Programmed cell death, or apoptosis, can be a response to harmful stimuli or pathological conditions, such as traumatic brain injury (TBI). 
Toxins and Disease:
Exposure to environmental toxins, cardiovascular disorders, and various infectious or genetic diseases can also trigger inappropriate neuronal death. "




```
Classification: Runtime-only
```

**Objective Recap**

* Add **heterogeneous neuron classes** (different target degrees k and plasticity rates), make **void-walker tagging** first‑class on the bus to drive **sparse** prune/grow/cull actions, and ensure **synapse strengthening + decay**—all without any dense scans.

---

## Action Plan (sparse, event‑driven, sub‑quadratic)

* **1) Neuron classes with target‑degree bands (k) + rarity.**
  Define a small set of neuron classes with explicit targets and rarity. The runtime enforces *per‑neuron* `k_target` (in+out capacities) and per‑class plasticity schedules; the growth/prune actuators keep each neuron within its band using only local neighbor sets (no global scans).

  * **Relay:** common; `k_target=3-4`; fast decay; high exploration.
  * **Interneuron (Inhibitory):** common; `k_target=6-12`; medium decay; stabilizes activity.
  * **Integrator:** less common; `k_target=20-60`; slow decay; memory retention.
  * **Purkinje‑like:** rare; `k_target≈200-500` (bounded by territory size); very slow decay; heavy fan‑in.
    Rarity is enforced by **growth budgets per class** (e.g., ≤0.5% Purkinje‑like of N). All selection is **territory‑scoped** to stay sub‑quadratic.&#x20;

* **2) Void‑walker tags → bus → structural votes (no polling).**
  Walkers already “see” local signals; extend them to publish **Tag events** with TTL and reasons:

  * `tag.prune_synapse {pre, post, weight, reason, ttl}`
  * `tag.cull_neuron {nid, reason, ttl}`
  * `tag.grow_synapse {pre, post_hint|territory, reason, ttl}`
  * `tag.neurogenesis {class, territory, k_budget, ttl}`
    The bus delivers O(1) *surgical* writes because events include exact indices—no searches by the CPU. A **Scoreboard** aggregates votes per edge/node with decay; when a threshold is crossed, the **GDSP actuator** applies the change using only local adjacency.&#x20;

* **3) Physiological→runtime triggers (biologically anchored, still sparse).**
  Map your list to concrete walker types / gates:

  * **Use‑it‑or‑lose‑it:** walker maintains `use_score_ij` (EMA of co‑spikes) → low‑use edges accrue `tag.prune_synapse`.
  * **Microglia-C3 analogue:** complement‑tag walker marks weak/erratic synapses with `tag.C3` → microglia walker consumes `tag.C3` → emits `tag.prune_synapse`.
  * **Semaphorin‑like retraction:** boundary‑gradient walker tags axon branches in specific territories for branch retraction (`tag.retract_axonal_branch` → translates to local out‑degree decrement and pruning budget).
  * **Excitotoxicity sentinel:** high firing‑rate + “calcium proxy” (integrated depolarization) triggers `tag.cull_neuron` with cooldown.
  * **Ischemia surrogate:** track per‑territory “ATP debt” = (spike work - supply budget). Sustained debt emits `tag.cull_neuron` with higher threshold; immediate `tag.prune_synapse` on the most costly edges first.
  * **Trauma:** external event marks a territory window; walkers flood it with `tag.cull_neuron/prune_synapse` at raised weights.
  * **Apoptosis:** integrate multi‑signal danger score; when above bound for `T_apop`, emit `tag.cull_neuron` (graceful teardown: detach in k‑sized chunks per tick).
    All of these are **event‑sourced** and **territory‑bounded**—no dense scans.&#x20;

* **4) Synapse strengthening + decay (vectorized, class‑aware).**
  Maintain per‑edge eligibility $e_{ij}$ (EMA of pre×post correlation). Update rule each tick (GPU kernel, CSR‑local):

  $$
  w_{ij}\leftarrow (1-\lambda_{ij})\,w_{ij} + \eta_{ij}\,e_{ij}\,M_t,
  $$

  with **class‑mapped** $\eta_{ij},\lambda_{ij}$ from pre/post neuron classes; $M_t$ is a modulatory factor (TD/novelty/salience).
  **Pruning rule:** if $w_{ij}<w_{\min}$ for $T_{\rm idle}$ ticks → emit `tag.prune_synapse`.
  **Cap rule:** clip $w_{ij}\in[w_{\min}, w_{\max}]$.
  This is exactly the “use it or lose it” behavior you described, but on‑device and sparse.

* **5) Sparse bridging / growth (budgeted).**
  When fragmentation is detected **locally** (territory UF says components>1 within the territory’s active set), the actuator adds up to `bridge_budget` edges by sampling boundary nodes and **alias‑sampling** a handful of candidates—no S‑matrix, no global search. For class creation/growth, pull from a **per‑class free list** and connect within the territory until each new neuron’s `k_target` is met (or budget exhausted).

* **6) No‑dense guarantee + guardrails.**

  * Strip/ignore any code path that calls dense `perform_structural_homeostasis` unless an explicit `FORCE_DENSE=1` is set; add a **hard assert** otherwise.
  * All actuators accept **budgets** (`prune_budget`, `bridge_budget`, `grow_budget`) and operate only on indices present in **event payloads** or **territory‑local neighbor lists**. Prove in tests that “edges touched per tick” ≤ sum of budgets.

* **7) Observability without polling.**
  Each actuator writes JSON events: `{added_edges, pruned_edges, culled_neurons, class_hist, degree_hist_by_class, votes_in/out, reasons_topk}` plus **latency** and **edges\_touched**. This makes the global system’s view O(1) through the bus.&#x20;

---

## Handoff (Physicist Mode implements)

**Files/paths to create/modify (under your `fum_rt` tree)**

* `fum_rt/core/types/neurons.py` — class enum + metadata:

  ```python
  NeuronClass = Enum('NeuronClass','RELAY INHIBITORY INTEGRATOR PURKINJE')
  CLASS_META = {
    RELAY:     dict(k_min=3,   k_max=5,   eta=0.08, decay=0.03, rarity=0.60),
    INHIBITORY:dict(k_min=6,   k_max=12,  eta=0.05, decay=0.02, rarity=0.25),
    INTEGRATOR:dict(k_min=20,  k_max=60,  eta=0.01, decay=0.005,rarity=0.14),
    PURKINJE:  dict(k_min=200, k_max=500, eta=0.002,decay=0.0005,rarity=0.01),
  }
  ```
* `fum_rt/core/connectome_state.py` — add arrays on GPU: `neuron_class[i]`, `k_target[i]`, `eta_vec[i]`, `lambda_decay[i]`, and `free_slots[i]` (derived from k\_target - current degree).
* `fum_rt/core/neuroplasticity/params.py` — **PlasticityManager** that maps `neuron_class[]` → full `eta_vec`, `lambda_vec` (re‑emit on neurogenesis/class change).
* `fum_rt/core/walkers/tags.py` — canonical Tag schema + reason codes (e.g., `C3`, `SEMAPHORIN`, `EXCITOTOX`, `ATP_DEBT`, `TRAUMA`, `APOPTOSIS`).
* `fum_rt/core/bus_topics.py` — `tag.*` topic names; `struct.actuator.*` result events.
* `fum_rt/core/structural/scoreboard.py` — lock‑free per‑id **vote accumulator** with TTL decay (`score[i] ← γ·score[i] + Σw(events)`), exposing `above(th)` sets.
* `fum_rt/core/structural/actuator_sparse.py` — **GDSPSparseActuator**:

  * `apply_prune(edges_subset, prune_budget)`
  * `apply_grow(neuron_ids, k_budget, territory_id)`
  * `apply_bridge(territory_id, bridge_budget)` (boundary sampling, alias for candidates)
  * `apply_cull(neuron_ids, k_budget)`
    All kernels operate on CSR lists for touched indices only.
* `fum_rt/runtime/loop/main.py` — integrate: read `scoreboard.above(th)` per category each tick → call actuator with budgets; update observability events. **No dense calls**; add assert guarding them.
* `fum_rt/core/neuroplasticity/update.cu/hip` — update kernel to compute `w = (1-λ) w + η e M` for touched edges only (CSR traversal of active rows).

**CLIs to run + seeds**

```bash
# 1) Enable tagging → structural acts with tight budgets (purely sparse)
export ENABLE_GDSP=1
export PRUNE_BUDGET=64
export BRIDGE_BUDGET=16
export GROW_BUDGET=16
export SCORE_THRESH_PRUNE=2.0
export SCORE_THRESH_CULL=4.0
export SCORE_THRESH_GROW=2.0

# 2) Start runtime (normal entrypoint)
python -m fum_rt.run_nexus --neurons 20000 --hz 10 --viz-every 0 --seed 0
```

(Your GlobalSystem remains O(1) on reads via bus events; writes are event-targeted. )

---

## Verification (acceptance gates)

* **No‑dense gate:** any attempt to call dense homeostasis without `FORCE_DENSE=1` raises a hard assert in CI. **PASS** = assert hit in the negative test.
* **Budget gate:** per tick, `edges_touched ≤ PRUNE_BUDGET + 2*BRIDGE_BUDGET + k_budget_sum`. Fails if exceeded.
* **Class/degree gate:** after 10k ticks, per‑class median degree ∈ `[k_min,k_max]`; Purkinje count ≤ rarity\*N + 1.
* **Use‑it‑or‑lose‑it gate:** in a workload with 30% idle channels, ≥20% of `w_ij` under‑use edges drift below `w_min` within 2k ticks and are pruned within 3k ticks (bounded by budgets).
* **Strengthening gate:** in a stimulated territory, median Δw on tagged paths is > 0 and ≥5× larger than untagged controls over 1k ticks.
* **Bridge/repair gate (fragment event):** when a territory splits, `components` returns to 1 within `≤ (ceil(E_boundary/BRIDGE_BUDGET)+cooldown)` ticks (record this).
* **Stability gate:** total edge count stays within ±10% over 50k ticks under stationary drive (homeostasis, not explosion).

**Expected PASS signatures:**
JSON events under `runs/<ts>/events.jsonl` with `struct.actuator.{pruned,bridged,grown,culled}` counters; histograms in `runs/<ts>/metrics/degree_by_class.json`; “edges\_touched” ≤ budgets every tick; *no* dense call sites invoked.

---

## Assumptions/Risks (and how we kill each)

* **Rare high‑k on small territories** risks local O(k²).
  *Mitigation:* cap `k_target` by `min(CLASS_META.k_max, 0.25*|territory|)` and enforce **bridge/grow budgets**.
* **Over‑eager culling** from stacked tags.
  *Mitigation:* multi‑signal quorum (e.g., require 2 distinct reasons or a minimum TTL‑integrated score), plus per‑territory **max\_cull\_per\_tick**.
* **Bus overload with tags.**
  *Mitigation:* per‑tick tag compaction by `(entity_id, reason)` with count aggregation; scoreboard TTL decay.
* **Parameter drift.**
  *Mitigation:* emit snapshots of `CLASS_META`, thresholds, and budgets into each run header; CI asserts monotonicity on drift unless accompanied by a migration note.

---

## Next Steps (tight, no‑nonsense)

1. Land **NeuronClass** + **PlasticityManager** and push `eta_vec, lambda_vec, k_target` to device.
2. Implement **Tag schema**, **Scoreboard**, and **GDSPSparseActuator**; wire the loop.
3. Turn on **Hebbian‑style strengthening + decay** kernel updates (CSR‑local).
4. Add **acceptance tests** above (particularly **No‑dense**, **Budget**, **Use‑it‑or‑lose‑it**, **Bridge/repair**).
5. Add 2-3 **walker types** (C3/microglia, semaphorin, excitotoxicity) that publish tags with realistic TTLs and weights.

---

### Why this fits your intent

* **Heterogeneous neurons:** different k and plasticity by class; rare high‑k are supported but bounded.
* **Sparse only:** all actions are event‑pointed and budgeted on CSR subsets. No scan‑all; dense path is hard‑blocked.
* **Walker‑driven structure:** tags carry **reasoned biology analogs** (C3, semaphorin, excitotoxicity, ischemia), aggregated into quorum decisions.
* **Use‑it‑or‑lose‑it:** strengthening with decay and pruning are explicit, measurable behaviors—not hand‑waving.
  This is fully aligned with your architecture doc’s **O(1) write via bus events and emergent gating**—we just made the tags and actuators concrete and testable.&#x20;

If you want, I’ll draft the 40‑line **GDSPSparseActuator** skeleton and the bus `Tag` schema next so your team can drop them in and run the acceptance tests immediately.






what does this mean
"3) Physiological→runtime triggers (biologically anchored, still sparse).
Map your list to concrete walker types / gates:

Use‑it‑or‑lose‑it: walker maintains use_score_ij (EMA of co‑spikes) → low‑use edges accrue tag.prune_synapse.

Microglia-C3 analogue: complement‑tag walker marks weak/erratic synapses with tag.C3 → microglia walker consumes tag.C3 → emits tag.prune_synapse.

Semaphorin‑like retraction: boundary‑gradient walker tags axon branches in specific territories for branch retraction (tag.retract_axonal_branch → translates to local out‑degree decrement and pruning budget).

Excitotoxicity sentinel: high firing‑rate + “calcium proxy” (integrated depolarization) triggers tag.cull_neuron with cooldown.

Ischemia surrogate: track per‑territory “ATP debt” = (spike work - supply budget). Sustained debt emits tag.cull_neuron with higher threshold; immediate tag.prune_synapse on the most costly edges first.

Trauma: external event marks a territory window; walkers flood it with tag.cull_neuron/prune_synapse at raised weights.

Apoptosis: integrate multi‑signal danger score; when above bound for T_apop, emit tag.cull_neuron (graceful teardown: detach in k‑sized chunks per tick).
All of these are event‑sourced and territory‑bounded—no dense scans."


ATP debt? is this void debt? don't start mixing up terminology now and confusing everything. What is the trauma trigger for? please do a better job at explaining remember that



```
Classification: Runtime-only
```

**Objective Recap**

* Explain the “Physiological → runtime triggers” cleanly.
* Keep terminology consistent (no “ATP debt” vs “void debt” confusion).
* Specify exactly how walkers tag, how tags become actions (prune/grow/cull), and how synapse strengthening/decay run—**all sparse, budgeted, no dense scans**.&#x20;

---

## What that section **means** (plain, precise)

* **Local scouts (walkers) don’t change the graph.** They **observe locally** and publish **Tag events** to the bus with exact IDs (pre, post, weight, reason, TTL). Bus makes writes **O(1)** because the action already has coordinates—no search. A CPU arbiter consumes tags and issues **targeted** “prune/grow/cull” to the GPU actuator with small per‑tick budgets. **No dense scans.**&#x20;

* **“Physiological → runtime”** = a **mapping** from biology → concrete, sparse, event‑driven rules:

  * A biological condition → a **walker** computes a **local metric** → emits a **tag(reason, ids, TTL)** → the **scoreboard** (decaying vote accumulator) crosses a threshold → **actuator** edits only those IDs (within budget).&#x20;

---

## Clear definitions (each trigger, no jargon drift)

### 1) Use‑it‑or‑lose‑it (synaptic activity)

* **Local metric:** `use_ij(t) = EMA_{τ_use}[ s_i(t) * s_j(t-Δ) ]` (co‑activity).
* **Walker:** *UseTracker* updates `use_ij`; if `use_ij < θ_use` for `T_idle` → `tag.prune_synapse{pre:i, post:j, reason:"low_use", ttl}`.
* **Actuator effect:** prune only those (i,j) tagged, up to `PRUNE_BUDGET` per tick.
* **This implements** “prune infrequent, reinforce frequent” sparsely.

### 2) Microglia-C3 analogue (selective pruning)

* **Local metric:** volatility & weakness flags on (i,j): high variance, low mean `w_ij`.
* **Walkers:**

  * *ComplementTagger* marks candidates: `tag.C3{pre,post,ttl}`.
  * *Microglia* consumes outstanding C3 tags and emits `tag.prune_synapse{..., reason:"C3"}` if corroborated by `use_ij` and weakness.
* **Actuator:** prunes tagged edges (budgeted).
* **Why two‑stage?** Reduces false positives; still scan‑free.

### 3) Semaphorin‑like retraction (branch clean‑up)

* **Local metric:** boundary gradient from territory cartography + overloaded out‑degree on neuron `i`.
* **Walker:** *BoundaryRetraction* emits `tag.retract_axonal_branch{nid:i, ttl}` when a branch points “against” territory gradient and `deg_out(i) > k_target(i)`.
* **Actuator:** translates to **local out‑degree decrement** by pruning K weakest out‑edges of `i` (budgeted), not a global search.

### 4) Excitotoxicity sentinel (over‑excitation)

* **Local metrics:** firing rate `r_i(t)=EMA_{τ_r}[s_i]`; **Ca‑proxy** `c_i(t)=EMA_{τ_c}[v_i^+]` (integrated depolarization if you expose it, or smoothed spike bursts).
* **Walker:** if `r_i > r_max && c_i > c_max` for `T_exc`, emit `tag.cull_neuron{nid:i, reason:"excitotox", ttl_cooldown}` and `tag.prune_synapse` around `i` to relieve load before culling.
* **Actuator:** prune locally first; if sentinel persists, **cull** `i` (detach in small chunks per tick).

### 5) **Metabolic debt** (rename; **not** “void debt”)

* **Terminology fix:** We will **not** call this “ATP debt.” We’ll use **`metabolic_debt` (m\_debt)** to avoid confusion with your **SIE “void\_debt”** channel. Two different signals, two different bus topics.

  * `metab.debt.T` (territory‑local energy budget gap) ← **runtime homeostasis**.
  * `sie.void_debt` (high‑level objective/reward signal) ← **SIE/GlobalSystem**.&#x20;
* **Local metric (territory T):**
  `work_T = EMA[ α_spike·Σ_i s_i + α_syn·Σ_(i,j∈T) |w_ij|·activity_ij ]`
  `supply_T = config.metab_supply_T`
  `m_debt_T = EMA[ work_T - supply_T ]`
* **Walker:** *MetabolicAuditor* emits

  * `tag.prune_synapse{...,"reason":"metab"}` for top cost edges,
  * `tag.cull_neuron{nid}` for worst offenders if `m_debt_T > θ_debt` for `T_debt`.
* **Actuator:** trims costliest local edges first; culls as last resort, all with budgets.

### 6) Trauma trigger (what & why)

* **What:** an **external** event that labels a **territory × time window** as damaged. Think: an operator test, sensor input, or fault isolator.
* **Why:** lets you **quickly quarantine and clean** a bad region (e.g., corrupted dynamics, adversarial I/O). It is *not* random culling; it’s **controlled remediation**.
* **Event:** `trauma.begin{territory_id, ttl, severity}` and later `trauma.end{...}`.
* **Walkers:** raise weights on prune/cull tags **only inside** that window; optionally suppress growth there until healed.
* **Actuator:** applies stronger budgets within the marked window; never scans outside it.

### 7) Apoptosis (programmed removal)

* **Danger score:** `D_i = w1·excitotox_flag + w2·metab_flag + w3·C3_hits + w4·low_use` (EMA).
* **Walker:** if `D_i > θ_apop` for `T_apop`, emits `tag.cull_neuron{nid:i, reason:"apoptosis"}`.
* **Actuator:** **graceful teardown**: detach ≤`k_chunk` synapses per tick until gone (keeps edits budgeted, avoids shocks).

---

## Synapse **strengthening + decay** (explicit)

Per‑edge update (CSR‑local; **no scans**):

$$
w_{ij}\leftarrow\operatorname{clip}\Big((1-\lambda_{ij})\,w_{ij} + \eta_{ij}\,e_{ij}\,M_t,\;[w_{\min},w_{\max}]\Big)
$$

* `e_ij` = EMA of pre×post correlation (eligibility).
* `M_t` = modulatory factor (e.g., TD/novelty/salience).
* `η_ij, λ_ij` come from **neuron class** (relay/inhibitory/integrator/purkinje‑like).
* **Prune** if `w_ij < w_min` for `T_idle`.
  This gives “use‑it‑or‑lose‑it” and reinforcement in one kernel.

---

## Naming & bus topics (to prevent confusion)

* **Energy:** `metab.debt.T` (runtime homeostasis) **≠** `sie.void_debt` (SIE objective). Keep both, never intermix fields.&#x20;
* **Tags from walkers:** `tag.prune_synapse`, `tag.grow_synapse`, `tag.cull_neuron`, `tag.C3`, `tag.retract_axonal_branch`.
* **Actuator results:** `struct.pruned`, `struct.grown`, `struct.culled`, `struct.bridged`.
* **All events carry IDs** (pre, post, nid, territory\_id) so the arbiter/actuator never search—**O(1) writes**.&#x20;

---

## Handoff (Physicist Mode implements)

**Files/paths**

* `fum_rt/core/walkers/tags.py` — **Tag schema** (reasons, TTL).
* `fum_rt/core/structural/scoreboard.py` — per‑edge/per‑neuron **vote accumulator** with decay.
* `fum_rt/core/walkers/{use_tracker.py, complement_tagger.py, microglia.py, boundary_retraction.py, excitotox_sentinel.py, metabolic_auditor.py}` — each emits tags above.
* `fum_rt/core/structural/actuator_sparse.py` — applies (prune/grow/bridge/cull) **only** on IDs from scoreboard; per‑tick budgets.
* `fum_rt/runtime/loop/main.py` — collect `scoreboard.above(θ)` per category → call actuator. **No dense codepaths** (assert if called).
* `fum_rt/core/neuroplasticity/update_kernel.cu|hip` — implement `w ← (1-λ)w + η e M` for touched edges.

**CLIs**

```bash
export ENABLE_GDSP=1
export PRUNE_BUDGET=64 BRIDGE_BUDGET=16 GROW_BUDGET=16
export SCORE_THRESH_PRUNE=2.0 SCORE_THRESH_GROW=2.0 SCORE_THRESH_CULL=4.0
python -m fum_rt.run_nexus --neurons 20000 --hz 10 --viz-every 0 --seed 0
```

(Events are O(1) writes via bus; actuator is budgeted & sparse.)&#x20;

---

## Verification (acceptance gates)

* **No‑dense gate:** any call into dense homeostasis without `FORCE_DENSE=1` **asserts** in CI.
* **Budget gate:** `edges_touched_per_tick ≤ PRUNE_BUDGET + 2·BRIDGE_BUDGET + GROW_BUDGET`.
* **Use‑it‑or‑lose‑it:** in a 30% idle workload, ≥20% of low‑use edges pruned within 3k ticks (budget‑limited).
* **Strengthening:** in a stimulated path, median Δw(tagged) ≥ 5× Δw(untagged) over 1k ticks.
* **Metabolic:** when `metab.debt.T > θ_debt` for `T_debt`, top‑cost edges pruned first; if persists, ≤`max_cull_per_tick` culled; debt falls.
* **Trauma window:** within a marked window, edits occur only inside the territory and budgets are elevated only there; outside remains unchanged.

---

## Direct answers to your questions

* **“ATP debt? is this void debt?”**
  No. We’ll **rename to `metabolic_debt`** and keep it **separate** from **`sie.void_debt`**. Different producers, different topics, different consumers. No mixing.&#x20;

* **“What is the trauma trigger for?”**
  It’s an **operator/sensor‑driven window** to **accelerate** targeted clean‑up (prune/cull) **in one territory** after a shock/fault/test. It **doesn’t** do global culling, and it **never** scans: it just raises weights/budgets for tags **inside that window** so the actuator resolves the problem quickly.

* **“Why only spike‑based homeostasis?”**
  It isn’t. We gate on **three** independent signals (use score, fragmentation, TD/modulators), plus **metabolic** and optional **trauma** windows. Spikes alone are **not** the only trigger.

If you want, I’ll draft the 30‑line **Tag schema**, a minimal **scoreboard**, and the actuator’s **budgeted prune** function next so you can drop them in and run these gates immediately.&#x20;
