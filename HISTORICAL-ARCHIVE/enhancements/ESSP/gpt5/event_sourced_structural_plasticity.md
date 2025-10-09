# Rewritten Narrative Report

**Generated on:** August 24, 2025 at 9:38 PM CDT

---

## Generated Narrative

# Technical Specification: Event-Sourced Structural Plasticity

## 1. Objective

This document specifies the design and implementation of a comprehensive, biologically-plausible structural plasticity framework for the runtime connectome. The primary architectural mandate is to achieve all structural modifications-including synapse formation, pruning, strengthening, decay, and neuron culling-through a strictly sparse, event-driven, and computationally budgeted model. All operations must be local, territory-scoped, and sub-quadratic in complexity, explicitly prohibiting dense matrix scans or global polling mechanisms.

The target implementation will support heterogeneous neuron classes, each with distinct connectivity targets and plasticity dynamics. The system will be driven by a set of local, autonomous agents ("walkers") that translate physiological and pathological conditions into discrete, actionable events. This specification serves as the definitive guide for the implementing neuro-physicist engineer.

---

## 2. Core Architecture: Event-Sourced Plasticity

The entire framework is built upon a decoupled, event-sourced pipeline. This design ensures scalability, testability, and adherence to the strict sparse-only constraint. The flow of information and action is unidirectional:

**Walker → Tag Event → Event Bus → Scoreboard → GDSP Actuator**

1.  **Walkers (Local Observers):** Lightweight, read-only agents that traverse local subgraphs (neighbor sets within a territory). They compute specific metrics (e.g., synaptic co-activity, metabolic load) and, upon crossing predefined thresholds, emit `Tag` events. They do not modify the connectome directly.

2.  **Tag Events (Proposals):** Atomic, structured messages published to the Event Bus. Each tag represents a proposal for a structural change, containing precise coordinates (neuron/synapse IDs), a reason code (e.g., `LOW_USE`, `EXCITOTOX`), and a time-to-live (TTL).

3.  **Event Bus (Transport):** The central message broker responsible for delivering `Tag` events to subscribed systems. Its role is strictly transport, ensuring O(1) delivery of targeted information.

4.  **Scoreboard (Evidence Aggregator):** A stateful service that consumes `Tag` events. It maintains a decaying vote count for each tagged entity (neuron or synapse). This mechanism integrates noisy, high-frequency tag events into stable, thresholded decisions, preventing over-eager reactions to transient signals.

5.  **GDSP Actuator (Sole Write Authority):** The **G**oal **D**irected **S**tructural **P**lasticity (GDSP) Actuator is the only component with write-access to the connectome graph. It subscribes to the Scoreboard's threshold-crossing events. All its operations are surgical, CSR-safe, and strictly bounded by per-tick budgets (`PRUNE_BUDGET`, `GROW_BUDGET`, etc.). It operates exclusively on the indices provided in event payloads, eliminating any need for searching or scanning.

---

## 3. System Components and Data Structures

### 3.1. Heterogeneous Neuron Classes

To support diverse functional roles, the system defines multiple neuron classes. These classes dictate a neuron's target connectivity, plasticity rates, and population rarity.

**Class Definitions:**

| Class | Rarity | Target Degree (`k_target`) | Learning Rate (`η`) | Decay Rate (`λ`) | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Relay** | ~60% | 3-5 | High (0.08) | High (0.03) | Common, fast-adapting neuron for signal propagation. |
| **Inhibitory** | ~25% | 6-12 | Medium (0.05) | Medium (0.02) | Common, provides local stabilization and gain control. |
| **Integrator** | ~14% | 20-60 | Low (0.01) | Low (0.005) | Less common, for temporal integration and memory retention. |
| **Purkinje-like** | ~1% | 200-500 | Very Low (0.002) | Very Low (0.0005) | Rare, high-capacity neuron for complex pattern integration. |

**Implementation:**

*   **On-Device Storage:** The following arrays must be maintained on the compute device:
    *   `neuron_class[i]`: An integer enum mapping each neuron ID to its class.
    *   `k_target[i]`: The target degree (in+out) for each neuron, derived from its class.
    *   `eta_vec[i]`, `lambda_decay[i]`: Per-neuron learning and decay rates, derived from `neuron_class[i]`.
*   **Plasticity Manager:** A host-side service (`PlasticityManager`) is responsible for mapping the `NeuronClass` enum to the full device vectors (`eta_vec`, `lambda_vec`). This manager must re-materialize these vectors upon any neurogenesis or class-change event.

### 3.2. Tag Schema and Event Bus Topics

All inter-component communication regarding structural changes is mediated by a canonical `Tag` schema.

**Canonical Tag Events (Published by Walkers):**

*   `tag.prune_synapse {pre_id, post_id, reason, ttl}`
*   `tag.cull_neuron {nid, reason, ttl}`
*   `tag.grow_synapse {pre_id, post_hint_id|territory_id, reason, ttl}`
*   `tag.neurogenesis {class, territory_id, k_budget, ttl}`
*   `tag.C3 {pre_id, post_id, ttl}` (Special tag for two-stage pruning)
*   `tag.retract_axonal_branch {nid, ttl}`

**Actuator Result Events (Published by GDSP Actuator):**

*   `struct.pruned {count, budget_used}`
*   `struct.grown {count, budget_used}`
*   `struct.culled {count, budget_used}`
*   `struct.bridged {count, budget_used}`

Reason codes will include: `LOW_USE`, `C3_ENGULF`, `SEMAPHORIN_RETRACT`, `EXCITOTOX`, `METABOLIC_DEBT`, `APOPTOSIS`, `TRAUMA`.

---

## 4. Plasticity Mechanisms: From Biology to Runtime Code

### 4.1. Foundational Synaptic Dynamics

The baseline plasticity mechanism is a continuous, activity-dependent update to synaptic weights (`w_ij`), implementing both Hebbian reinforcement ("use it") and passive decay ("lose it"). This operation is performed by a dedicated GPU kernel that traverses only active rows in the sparse connectome matrix.

**Synaptic Update Rule:**

For each active synapse `(i, j)` on each tick, the weight `w_ij` is updated according to:

$$
w_{ij}(t+1) \leftarrow \operatorname{clip}\Big((1-\lambda_{ij}) \cdot w_{ij}(t) + \eta_{ij} \cdot e_{ij}(t) \cdot M_t, \; [w_{\min}, w_{\max}]\Big)
$$

Where:
*   $w_{ij}$: The weight of the synapse from neuron `i` to `j`.
*   $\lambda_{ij}$: The passive decay rate, determined by the neuron classes of `i` and `j`.
*   $\eta_{ij}$: The learning rate, also determined by the neuron classes.
*   $e_{ij}(t)$: The synaptic eligibility trace, typically an Exponential Moving Average (EMA) of pre- and post-synaptic co-activity: `EMA[s_i(t) * s_j(t-Δ)]`.
*   $M_t$: A global or territory-local modulatory factor, representing signals like novelty, salience, or a TD-error signal.
*   $[w_{\min}, w_{\max}]$: Hard weight clamps to prevent runaway dynamics.

**Pruning Condition:** If $w_{ij} < w_{\min}$ for a duration of $T_{\text{idle}}$ ticks, a *UseTracker* walker emits a `tag.prune_synapse{reason:"low_use"}` event.

### 4.2. Biologically-Analogous Structural Gating

Higher-order structural changes are governed by specific walker types that model biological processes.

#### 4.2.1. Selective Pruning (Microglia-C3 Analog)

This is a two-stage mechanism to ensure robust pruning of weak and ineffective synapses.

1.  **Stage 1: Marking (ComplementTagger Walker):** This walker identifies synapses with high weight volatility and low mean efficacy. It marks these candidates by emitting `tag.C3{pre_id, post_id, ttl}`.
2.  **Stage 2: Engulfment (Microglia Walker):** This walker consumes outstanding `tag.C3` events. If a C3-tagged synapse is also corroborated by a low `use_score` (from the `UseTracker`), the Microglia walker emits a definitive `tag.prune_synapse{reason:"C3_ENGULF"}`. This quorum-based approach reduces false positives.

#### 4.2.2. Axonal Retraction (Semaphorin Analog)

This mechanism cleans up axonal branches that are misaligned with their territory's functional organization.

*   **Walker:** *BoundaryRetraction Walker*
*   **Local Metric:** It computes a boundary gradient based on territory cartography. If an axon branch from neuron `i` projects "against" this gradient and the neuron's out-degree (`deg_out(i)`) exceeds its target (`k_target(i)`), the walker acts.
*   **Action:** Emits `tag.retract_axonal_branch{nid:i, ttl}`.
*   **Actuator Effect:** The GDSP Actuator interprets this tag by pruning the `K` weakest outgoing synapses from neuron `i`, where `K` is a budgeted amount, bringing its out-degree closer to `k_target`.

### 4.3. Pathological and Homeostatic Culling

Neuron removal is a high-cost operation and is therefore gated by severe or persistent pathological signals.

#### 4.3.1. Excitotoxicity

*   **Walker:** *Excitotoxicity Sentinel*
*   **Local Metrics:**
    *   `r_i(t) = EMA_{τ_r}[s_i]`: Smoothed firing rate of neuron `i`.
    *   `c_i(t) = EMA_{τ_c}[v_i^+]`: A "calcium proxy" tracking integrated positive membrane potential, serving as a measure of prolonged depolarization.
*   **Trigger:** If `r_i > r_max` AND `c_i > c_max` for a duration of $T_{\text{exc}}$, the walker emits `tag.cull_neuron{nid:i, reason:"excitotox"}`. It may first emit `tag.prune_synapse` events for connections to `i` to relieve pressure before the final cull.

#### 4.3.2. Metabolic Homeostasis

This mechanism prevents runaway energy consumption within a territory.

*   **Terminology:** The signal is termed `metabolic_debt`. It is a runtime homeostatic signal and must be kept distinct from the high-level objective signal `sie.void_debt` from the Global System. They operate on separate bus topics (`metab.debt.T` vs. `sie.void_debt`).
*   **Walker:** *MetabolicAuditor Walker*
*   **Territory-Local Metric (`m_debt_T`):**
    `work_T = EMA[ α_spike·Σ_i s_i + α_syn·Σ_(i,j∈T) |w_ij|·activity_ij ]`
    `supply_T = config.metabolic_supply_T`
    `m_debt_T = EMA[ work_T - supply_T ]`
*   **Trigger:** If `m_debt_T > θ_debt` for a duration of $T_{\text{debt}}$, the walker emits:
    1.  `tag.prune_synapse` for the computationally most expensive synapses in the territory.
    2.  `tag.cull_neuron` for the highest-contributing neurons if the debt persists.

#### 4.3.3. Apoptosis (Programmed Cell Death)

This provides a graceful, multi-signal pathway for removing fundamentally unhealthy neurons.

*   **Walker:** *Apoptosis Sentinel*
*   **Integrated Danger Score (`D_i`):**
    `D_i = w1·excitotox_flag + w2·metabolic_flag + w3·C3_hits + w4·low_use_flag`
*   **Trigger:** If the EMA of `D_i` exceeds `θ_apop` for a duration of $T_{\text{apop}}$, the walker emits `tag.cull_neuron{nid:i, reason:"apoptosis"}`.
*   **Actuator Effect:** The culling is performed gracefully. The actuator detaches a small chunk of synapses (`≤k_chunk`) from neuron `i` each tick until it is fully isolated, preventing sudden shocks to the network.

### 4.4. System-Initiated Structural Modification

#### 4.4.1. Connectome Repair (Fragmentation Bridging)

This is a baseline maintenance routine to ensure network cohesion.

*   **Trigger:** The territory's Union-Find (UF) data structure reports that the number of connected components within its active set is greater than 1.
*   **Actuator Effect:** The GDSP Actuator is invoked with a `bridge_budget`. It performs a budgeted bridging operation by sampling nodes on the boundaries of the fragmented components and creating new edges using an alias-sampling method to find suitable connection candidates. This is a local repair and does not involve global graph analysis.

#### 4.4.2. Controlled Remediation (Trauma)

This mechanism provides an external, operator-driven method for targeted cleanup of a compromised network region.

*   **Trigger:** An external system publishes a `trauma.begin{territory_id, ttl, severity}` event. This is not a walker-driven process.
*   **Effect:** For the duration of the trauma window, the weights and budgets for prune/cull tags are significantly increased *only within the specified territory*. Growth may be optionally suppressed.
*   **Purpose:** This allows for rapid, controlled remediation of a region affected by a known fault, corrupted sensory input, or adversarial test case. It is a surgical tool, not a random culling mechanism.

---

## 5. Implementation and Verification

### 5.1. Implementation Guide

*   **File Modifications:**
    *   `fum_rt/core/types/neurons.py`: Define `NeuronClass` enum and metadata dictionary.
    *   `fum_rt/core/connectome_state.py`: Add on-device arrays for `neuron_class`, `k_target`, `eta_vec`, `lambda_decay`.
    *   `fum_rt/core/walkers/*.py`: Implement the suite of walkers (`UseTracker`, `ComplementTagger`, `Microglia`, `MetabolicAuditor`, etc.).
    *   `fum_rt/core/structural/scoreboard.py`: Implement the lock-free, decaying vote accumulator.
    *   `fum_rt/core/structural/actuator_sparse.py`: Implement the `GDSPSparseActuator` with budgeted `apply_{prune, grow, cull, bridge}` methods.
    *   `fum_rt/runtime/loop/main.py`: Integrate the pipeline. Read from the scoreboard, call the actuator with budgets. **A hard assert must guard against any calls to dense homeostasis routines unless `FORCE_DENSE=1` is explicitly set.**
    *   `fum_rt/core/neuroplasticity/update_kernel.cu|hip`: Implement the vectorized synaptic update rule.

### 5.2. Configuration

The system is controlled via runtime environment variables:
```bash
# Enable/disable the entire GDSP framework
export ENABLE_GDSP=1

# Per-tick budgets for the actuator
export PRUNE_BUDGET=64
export BRIDGE_BUDGET=16
export GROW_BUDGET=16

# Scoreboard thresholds for triggering actions
export SCORE_THRESH_PRUNE=2.0
export SCORE_THRESH_CULL=4.0
export SCORE_THRESH_GROW=2.0
```

### 5.3. Acceptance Criteria (Verification Gates)

The implementation is considered complete and correct upon passing the following gates:

*   **No-Dense Gate:** A dedicated test that attempts to invoke the dense homeostasis path without `FORCE_DENSE=1` must trigger a hard assertion failure.
*   **Budget Gate:** Over any given tick, the total number of modified edges must be less than or equal to `PRUNE_BUDGET + 2*BRIDGE_BUDGET + k_budget_sum`.
*   **Class Distribution Gate:** After a sufficiently long run (e.g., 10k ticks), the median degree of each neuron class must fall within its specified `[k_min, k_max]` band, and the population count must respect the rarity constraint.
*   **Use-it-or-Lose-it Gate:** In a workload with a known percentage of idle pathways (e.g., 30%), a significant fraction of those pathways' synaptic weights must decay below `w_min` and be subsequently pruned within a predictable number of ticks (bounded by `PRUNE_BUDGET`).
*   **Strengthening Gate:** In a territory subjected to a sustained, coherent stimulus, the median weight change (Δw) of synapses along the stimulated path must be positive and significantly greater (e.g., ≥5x) than that of untagged control synapses over the same period.
*   **Metabolic Gate:** When `metabolic_debt` in a territory is artificially driven high, the system must respond by first pruning the highest-cost edges, followed by culling the highest-contributing neurons if the debt persists, leading to a measurable reduction in the debt signal.
*   **Trauma Gate:** When a `trauma.begin` event is issued for a specific territory, structural modifications must be observed only within that territory, and their rate must be elevated compared to baseline. All other territories must remain unaffected.
*   **Repair Gate:** Upon artificially inducing fragmentation in a territory, the system must detect it (via UF) and apply budgeted bridging, returning the component count to 1 within a number of ticks proportional to the number of severed edges and the `BRIDGE_BUDGET`.

---

```
Classification: Runtime-only
```

**Objective Recap**

* Review your **Event‑Sourced Structural Plasticity** spec and turn it into an implementable, sparse‑only work order with clear gates. No dense scans. Heterogeneous neuron classes. Walker‑tags → bus → scoreboard → actuator-all budgeted.&#x20;

---

## What’s solid (keep as‑is)

* **Pipeline is right:** `walker → tag → bus → scoreboard → GDSP actuator` (sole writer), with per‑tick budgets. Good separation of read vs write.&#x20;
* **Sparse‑only mandate:** all ops territory‑scoped, sub‑quadratic; dense paths explicitly prohibited unless forced. Keep the hard assert.&#x20;
* **Heterogeneous neuron classes** with target‑degree bands and rarity; vectorized Hebbian **strengthening + decay** rule $w\leftarrow(1-\lambda)w+\eta\,e\,M$ + clamp.&#x20;
* **Tag taxonomy** and two‑stage microglia (C3 tag → engulf). **Trauma window** as an external, bounded remediation tool (territory‑only).&#x20;

---

## Redlines / tightenings (make these explicit)

1. **Tag TTLs & scoreboard decay (units & math).**

   * Define **tick‑based** TTL for every tag; expire at 0.
   * Scoreboard update per entity $x$ each tick:

     $$
     S_x \leftarrow \gamma\,S_x \;+\; \sum_{e\in\text{tags}(x)} w_e
     $$

     with $\gamma\in(0,1)$ (e.g., 0.95) and per‑reason weights $w_e$.
   * **Thresholds:** $S_x\ge \theta_{\text{prune}},\theta_{\text{grow}},\theta_{\text{cull}}$ trigger actuator pulls **only** for those IDs, capped by budgets.&#x20;

2. **Quorum for destructive actions.**

   * **Cull requires quorum**: at least **two distinct reasons** (e.g., EXCITOTOX + METABOLIC\_DEBT) **or** one reason sustained $T$ ticks. Encode as weights in the scoreboard; document defaults.&#x20;

3. **Class caps & territory bounds.**

   * **k\_target cap**: $k_i \le \min(k_{\max}(\text{class}_i),\, \lfloor 0.25\,|T|\rfloor)$.
   * **Rarity caps per territory** to prevent local over‑concentration (e.g., Purkinje‑like ≤0.5% per territory).&#x20;

4. **Where $\eta_{ij},\lambda_{ij}$ come from.**

   * Compute **per‑edge** parameters on the fly from pre/post classes: e.g., $\eta_{ij}=\min(\eta_i,\eta_j)$, $\lambda_{ij}=\max(\lambda_i,\lambda_j)$. Store **per‑neuron** vectors on device; derive per‑edge in kernel to keep CSR light.&#x20;

5. **Modulatory factor $M_t$ scope.**

   * Support both **global** and **territory‑local** $M_t$ (TD/salience). Bus topics: `mod.global.TD`, `mod.territory.TD.<T>`; the kernel reads the territory vector.&#x20;

6. **Sparse bridging algorithm (repair vs explore).**

   * **Repair**: run only if UF says **components>1** in territory. Steps:
     a) Identify boundary nodes (frontier rows with cross‑component neighbors) via the **active set only**;
     b) **Alias‑sample** up to `BRIDGE_BUDGET` pairs across component labels;
     c) Add edges if not exceeding class $k$ and not violating rarity caps.
   * **Exploratory growth**: separate path via `tag.grow_synapse` (no bridging unless fragmented).&#x20;

7. **Safety rails.**

   * `max_cull_per_tick`, per‑class **min‑degree floors**, E/I proportion checks. Any breach → **abort edits this tick** and emit a bus warning.&#x20;

8. **Terminology lock.**

   * Use **`metabolic_debt`** for runtime energy gap; keep it **distinct** from `sie.void_debt`. Different producers, topics, and consumers. (Your spec hints this; make it explicit in headers.)&#x20;

---

## Minimal spec deltas to paste (ready‑to‑merge)

**Tag schema (canonical)**

```python
@dataclass(frozen=True)
class Tag:
    topic: Literal[
      "tag.prune_synapse","tag.grow_synapse","tag.cull_neuron",
      "tag.C3","tag.retract_axonal_branch","tag.neurogenesis"
    ]
    pre: Optional[int] = None
    post: Optional[int] = None
    nid: Optional[int] = None
    territory: Optional[int] = None
    reason: Literal[
      "LOW_USE","C3_ENGULF","SEMAPHORIN_RETRACT",
      "EXCITOTOX","METABOLIC_DEBT","APOPTOSIS","TRAUMA"
    ] = "LOW_USE"
    weight: float = 1.0        # vote weight
    ttl: int = 50              # ticks
    meta: dict = field(default_factory=dict)
```

**Scoreboard (decay + quorum)**

```python
class Scoreboard:
    def __init__(self, gamma=0.95):
        self.gamma = gamma
        self.edge_scores = defaultdict(float)
        self.node_scores = defaultdict(lambda: defaultdict(float))  # by reason

    def tick(self, tags: Iterable[Tag]):
        # Decay
        for k in list(self.edge_scores): self.edge_scores[k] *= self.gamma
        for nid in list(self.node_scores):
            for r in list(self.node_scores[nid]):
                self.node_scores[nid][r] *= self.gamma
        # Accumulate
        for t in tags:
            if t.topic in ("tag.prune_synapse","tag.C3","tag.grow_synapse"):
                if t.pre is not None and t.post is not None:
                    self.edge_scores[(t.pre,t.post)] += t.weight
            elif t.topic in ("tag.cull_neuron","tag.retract_axonal_branch"):
                if t.nid is not None:
                    self.node_scores[t.nid][t.reason] += t.weight

    def above_edges(self, theta):      # yields (i,j)
        return [e for e,s in self.edge_scores.items() if s >= theta]

    def cull_candidates(self, theta, quorum=2):
        out=[]
        for nid,by_reason in self.node_scores.items():
            strong = [r for r,v in by_reason.items() if v >= theta]
            if len(strong) >= quorum: out.append(nid)
        return out
```

**Actuator (budgeted prune/grow/bridge/cull) - sparse, CSR‑safe**
*(pseudocode; you already defined the functions and budgets - wire them exactly this way)*&#x20;

```python
def tick_structural(scoreboard, budgets, uf, territory):
    # PRUNE
    edges = scoreboard.above_edges(theta=TH_PRUNE)[:budgets.prune]
    apply_prune(edges)  # touches only listed rows in CSR

    # BRIDGE (repair only if fragmented)
    if uf.components(territory) > 1:
        pairs = sample_boundary_pairs(uf, territory, k=budgets.bridge)
        apply_bridge(pairs)

    # GROW (exploration)
    seeds = scoreboard.above_edges(theta=TH_GROW)[:budgets.grow]
    apply_grow(seeds)   # local neighbor selection, respects k_target

    # CULL (with quorum)
    nids = scoreboard.cull_candidates(theta=TH_CULL, quorum=2)[:budgets.cull]
    apply_cull(nids, chunk=k_chunk)
```

---

## Handoff (Physicist Mode implements)

* **Files/paths to create/patch**

  * `fum_rt/core/walkers/tags.py` - Tag dataclass (above) + constants.
  * `fum_rt/core/structural/scoreboard.py` - decay, quorum, thresholds.
  * `fum_rt/core/structural/actuator_sparse.py` - `apply_{prune,grow,bridge,cull}` (budgeted; CSR rows only).
  * `fum_rt/runtime/loop/main.py` - integrate: pull from bus → scoreboard.tick(tags) → tick\_structural(...). Add **hard assert** against dense path unless `FORCE_DENSE=1`.
  * `fum_rt/core/neuroplasticity/update_kernel.cu|hip` - vectorized $w$ update using per‑neuron $\eta,\lambda$ derived to per‑edge inside the kernel.
  * (If not present) `fum_rt/core/territory/uf_active.py` - UF over **active** graph only; boundary sampler.

* **CLIs (smoke & acceptance)**

  ```bash
  export ENABLE_GDSP=1
  export PRUNE_BUDGET=64 BRIDGE_BUDGET=16 GROW_BUDGET=16 CULL_BUDGET=4
  export TH_PRUNE=2.0 TH_GROW=2.0 TH_CULL=4.0
  python -m fum_rt.run_nexus --neurons 20000 --hz 10 --viz-every 0 --seed 0
  ```

---

## Verification (acceptance gates)

* **No‑dense gate:** invoking dense homeostasis without `FORCE_DENSE=1` **asserts** (unit test). **PASS** = assert observed.&#x20;
* **Latency gate:** **tag→actuation latency ≤ 2 ticks** for any ID exceeding threshold (measure via events).&#x20;
* **Budget gate:** per tick, `edges_touched ≤ PRUNE_BUDGET + 2·BRIDGE_BUDGET + GROW_BUDGET` and `culled ≤ CULL_BUDGET`. Logged each tick.&#x20;
* **Class/degree gate:** after 10k ticks, per‑class median degree ∈ `[k_min,k_max]`; rarity respected per territory.&#x20;
* **Use‑it‑or‑lose‑it:** in a 30% idle workload, ≥20% of low‑use edges pruned ≤3k ticks (budget‑limited); stimulated paths show median Δw(tagged) ≥ 5× Δw(untagged) over 1k ticks.&#x20;
* **Repair gate:** when a territory splits, components → 1 within `ceil(E_boundary/BRIDGE_BUDGET)+cooldown` ticks.&#x20;
* **Trauma gate:** edits elevated **only** inside the marked window; other territories unaffected (A/B compare).&#x20;

---

## Assumptions/Risks

* **Bus backpressure:** too many tags → heap. Mitigation: per‑tick compaction by `(entity, reason)` and TTL decay in the scoreboard.&#x20;
* **Over‑pruning feedback:** add floor on degree per class + damp $w_{\min}$ changes; abort tick on invariant breach.&#x20;
* **High‑k in small territories:** cap $k_{\max}$ by territory size to avoid local O(k²) effects.&#x20;

---

## Next Steps

1. Paste the **redlines** (TTL/decay/quorum/caps) into your spec and commit.&#x20;
2. Land **Tag**, **Scoreboard**, **ActuatorSparse**, **UF boundary sampler**; wire the loop.&#x20;
3. Run the **latency + budget** gates; record JSON events and degree‑by‑class histograms.&#x20;
4. Add **quorum** and **class floor** unit tests (cull only on multi‑reason; degrees never below class floors).&#x20;
5. If green, expand walker set (metabolic, semaphorin) and tune weights; keep budgets tight.&#x20;

**Yes-“like this.”** Your spec has the right shape; the edits above close the last gaps (math for decay/TTL/quorum, repair vs explore split, hard safety rails) and make it PR‑ready without violating the sparse‑only rule.&#x20;


"Bus backpressure: too many tags → heap. Mitigation: per‑tick compaction by (entity, reason) and TTL decay in the scoreboard."

Didn't we decide that's what the hierarchical bus system is for?


"Over‑pruning feedback: add floor on degree per class + damp changes; abort tick on invariant breach."
I don't think this is going to be an issue, can you explain when this would become a problem?



"High‑k in small territories:: cap by territory size to avoid local O(k²) effects."

Didn't we say k is not supposed to be fixed, it must be based on multiple factors that causes k to change for any given neuron dynamically right? Or is this going to cause problems?

"If green, expand walker set (metabolic, semaphorin) and tune weights; keep budgets tight."

What do you mean tune the weights? the weights are self tuned remember? that's what the void equations do with void debt modulation


```
Classification: Runtime-only
```

**Objective Recap**

* Clarify four points and turn them into precise, safe rules for your **sparse-only, event‑sourced** structural plasticity:

  1. Bus backpressure vs. per‑tick compaction/TTL
  2. When “over‑pruning feedback” is a real risk
  3. Dynamic $k$ (not fixed) vs. small‑territory caps
  4. “Tuning weights” ≠ touching synaptic $w_{ij}$; keep void‑equation self‑tuning intact

---

## Direct answers (blunt, technical)

### 1) **Bus backpressure vs. per‑tick compaction/TTL**

* **Yes**-the **hierarchical bus** handles *transport‑level* backpressure (topic partitioning, ringbuffers, flow control, drops under pressure).
* **Still needed**-**scoreboard compaction/TTL** is *semantic* control: it coalesces duplicate tags **by (entity, reason)** and decays votes so the actuator sees *one stable decision per ID*, not a flood.
* Why both:

  * **Bus:** protects throughput and memory across producers/consumers.
  * **Scoreboard:** prevents actuator thrash and guarantees **O(1) writes** (few, decisive IDs) instead of bouncing on the same edge 100× in a window.
* Implementation split:

  * **Bus L0/L1:** territory rings + global topics; backpressure policy = drop‑old or drop‑new (choose explicitly).
  * **Scoreboard:** `S_x ← γ S_x + Σ w_e(tags_x)` then threshold to produce **unique** ID sets per tick; tags expire via TTL.
  * **Invariant:** actuator input cardinality ≤ budgets, regardless of tag volume.

### 2) **When “over‑pruning feedback” becomes a problem**

It’s rare when configs are sane, but these **joint conditions** can spiral:

* **Low drive & high decay:** $M_t \ll 1$ (void‑debt modulation negative) + large $\lambda$ → many edges drift under $w_{\min}$; *use* falls; **use‑it‑or‑lose‑it** piles on more prune votes.
* **Fragmentation before repair:** components>1 but **bridge\_budget=0** or tiny → prune wins, repair can’t catch up → islands form → further use‑score collapse → more pruning.
* **Two‑stage pruning in phase:** C3‑tagger + low‑use agree everywhere during a quiet phase → quorum trips broadly.
* **Asymmetric budgets:** `PRUNE_BUDGET ≫ GROW_BUDGET` for long windows → degree distribution ratchets down and can’t recover.

**Early‑warning metrics:**

* Rising `% edges under w_min for T_idle` while **components\_lb** drifts ↑, and actuator utilization at/near **PRUNE\_BUDGET** saturation for many ticks.

**Kill‑switch rails (cheap, safe):**

* **Per‑class min‑degree floors** (soft floor): block prune on nodes with `deg < k_floor(class)`.
* **Bridge‑before‑prune** when components>1: reserve some budget to heal first.
* **Quorum for destructive actions:** require ≥2 distinct reasons (e.g., LOW\_USE+ C3) or sustained one‑reason over $T$.
* **Cooldowns:** after cull/prune on a node, cool that node for $T_{\text{cool}}$ ticks.

### 3) **Dynamic $k$** vs. “cap by territory size”

* **Agreed:** $k$ is **not fixed**. It’s a **dynamic target** that adapts to context. The “cap” I mentioned is **capacity**, not a constant.
* Use a **bounded, smooth $k$‑controller**:

  $$
  k^\star_i(t) \;=\; \operatorname{clip}\!\Big( k_{\text{base}}(\text{class}_i)\cdot f_{\text{void}}(t)\cdot f_{\text{metab}}(T_i,t)\cdot f_{\text{var}}(i,t),\;
  k_{\min}(\text{class}),\; k_{\max}^{\text{cap}}(i,T)\Big)
  $$

  with
  $k_{\max}^{\text{cap}}(i,T)=\min\{\;k_{\max}(\text{class}_i),\;\alpha|T|,\;k_{\text{HW}}\;\}$.
* **Update rule (no thrash):**
  $k_{\text{target},i}(t+1)=k_{\text{target},i}(t)+\mathrm{sgn}(k^\star_i-k_{\text{target},i})\cdot \min\{|k^\star_i-k_{\text{target},i}|,\Delta k_{\max}\}$.
* **Why the capacity cap:** prevents pathological **high‑k** assignment inside tiny territories (starvation/oscillation) and keeps per‑tick **edit counts** within budgets. It **doesn’t** freeze $k$; it bounds **instantaneous demand**.

### 4) **“Tune the weights” ≠ touch synaptic $w_{ij}$**

* **We do not hand‑tune synaptic weights.** Those remain **self‑tuned** by your void equations with **void‑debt modulation** via $M_t$. Full stop.
* What I *did* mean by “tune weights”: **scoreboard vote weights** (per‑reason tag weights) and **thresholds** that govern *when* the **actuator** fires. These are **not** $w_{ij}$.

  * Example: `w(LOW_USE)=1.0`, `w(C3)=1.5`, `w(EXCITOTOX)=3.0`.
  * Thresholds `TH_PRUNE/TH_GROW/TH_CULL` are **control knobs**, not synaptic values.
* Make it **self‑calibrating** (no manual twiddling):

  * **Duty‑cycle controller:** target actuator utilization at, say, 70% of budget. If backlog↑ → raise thresholds slightly; if under‑utilized → lower slightly.
  * **Void‑debt coupling:** scale *vote* weights or thresholds with a bounded function of **`sie.void_debt`** so the system prunes less when debt is favorable and prunes more when debt is persistently adverse.
  * **Percentile clamps:** keep per‑territory trigger rates near desired percentiles (e.g., top 5% strongest signals actuate).

---

## Action Plan (sparse, scan‑free)

1. **Bus×Scoreboard contract**

   * Bus: keep hierarchical rings + backpressure; expose per‑topic **drop counters**.
   * Scoreboard: implement **per‑tick coalescing** by (entity, reason) + **TTL decay**; hard limit the size of the “above‑threshold” sets to the actuator budgets.

2. **Over‑prune guards (only 4 small rules)**

   * Soft **class floors**; **bridge‑before‑prune** if fragmented; **two‑reason quorum** or sustained single‑reason; **node cooldown** after destructive edits.

3. **Dynamic $k$ controller**

   * Compute $k^\star_i(t)$ from class base × void\_debt × metabolic term × variance; apply **Δk limiter** and **capacity cap** $k_{\max}^{\text{cap}}(i,T)$.
   * Enforce per‑tick **grow/prune budgets** so edits toward the new target remain bounded.

4. **Self‑calibrating actuator thresholds**

   * Controller loop per territory:
     `err = (utilization_target - utilization_measured)` → adjust `TH_*` by a small gain; clamp within \[TH\_min, TH\_max].
   * Optional: scale reason weights by a bounded function of `sie.void_debt`.

---

## Handoff (Physicist Mode implements)

* **Files/paths**

  * `.../bus/metrics.py` - expose per‑topic `produced, delivered, dropped` counters.
  * `.../structural/scoreboard.py` - TTL decay, coalesce by (entity, reason), bounded `above_threshold()` APIs.
  * `.../structural/guards.py` - floors, quorum, cooldown, bridge‑before‑prune switch.
  * `.../neuroclasses/k_controller.py` - dynamic $k$ target + Δk limiter + $k_{\max}^{\text{cap}}$.
  * `.../actuator/controller.py` - duty‑cycle controller for `TH_*` using utilization feedback; optional coupling to `sie.void_debt`.

* **CLIs (smoke)**

  ```bash
  # Observe duty-cycle closure without touching synaptic weights:
  export ENABLE_GDSP=1 PRUNE_BUDGET=64 BRIDGE_BUDGET=16 GROW_BUDGET=16
  export UTIL_TARGET=0.7 TH_PRUNE=2.0 TH_GROW=2.0 TH_CULL=4.0
  python -m fum_rt.run_nexus --neurons 20000 --hz 10 --seed 0
  ```

---

## Verification (acceptance gates)

* **Backpressure OK:** bus drop rate < 1% at target throughput; scoreboard “above‑threshold” set size ≤ budgets each tick.
* **No over‑prune spiral:** under stationary low drive, class median degrees stay ≥ floors; **components\_lb** does not drift upward over 10k ticks.
* **Dynamic $k$:** with a step in `sie.void_debt` or metabolic term, $k_{\text{target}}$ moves smoothly (|Δk| ≤ Δk\_max per tick); actuator edits remain within budgets; no oscillation.
* **Duty‑cycle closure:** actuator utilization converges to `UTIL_TARGET±10%` without manual tuning; synaptic $w_{ij}$ evolution remains entirely governed by the void equations.
* **No dense path:** any dense call without explicit `FORCE_DENSE=1` asserts.

---

## Assumptions/Risks

* **Tiny territories + high‑k demand:** without capacity caps, you risk starvation/oscillation. The cap + Δk limiter prevents that.
* **Tag flood:** the bus absorbs throughput, but without scoreboard coalescing you still thrash the actuator. We coalesce to guarantee bounded edits.
* **Controller mis‑tuning:** start with small gains for threshold adaptation; clamp ranges; log utilization.

---

## Next Steps

1. Land **scoreboard coalescing/TTL** and **bus metrics** (cheap, decisive).
2. Add the **four prune guards** (floors, quorum, cooldown, bridge‑first).
3. Implement **dynamic $k$** with Δk and capacity cap (keeps your “$k$ is dynamic” rule intact).
4. Add **duty‑cycle controller** for `TH_*` tied (optionally) to `sie.void_debt`.
5. Run the gates above; ship once utilization is stable and no over‑prune spiral is observed.

If you want, I’ll draft the \~40‑line `k_controller.py` (bounded $k^\star$+Δk limiter) and the 25‑line duty‑cycle controller for `TH_*` so you can drop them into the loop immediately.


why didnt i ever have any of those problems in my original demo code?



**Classification:** Runtime-only

**Objective Recap:**
Explain why your **original demo** never showed the pathologies we’re guarding against now, and give a tight work‑order to (a) make structural plasticity actually fire in the current runtime, and (b) preserve the demo’s good behavior **without** dense scans.

---

## Why the demo “just worked”

After inspecting the legacy and current trees you shared, the behaviors diverge for concrete architectural reasons:

1. **Monolithic, synchronous structural pass (legacy).**
   In the demo the function `perform_structural_homeostasis(...)` did **one dense, global pass** each time you called it: prune weak edges, then *deterministically* bridge components with a small **bundle** of new edges (three by default) and only convert back to CSC once at the end. This kept cohesion high and prevented over‑pruning from isolating regions. The code is explicit: prune on a global threshold and then add `BUNDLE_SIZE` bridges between clusters, operating on a `lil_matrix` for structural edits before returning to a compressed format. (See `fum_structural_homeostasis.py` and `core/substrate/structural_homeostasis.py` in the code snapshots you uploaded.)

2. **No event bus ➜ no backpressure.**
   The demo didn’t stream thousands of fine‑grained “tags.” It did *work*, not *messages*. So there was nothing to backlog, and you never saw “bus heap” effects. The current runtime has a bounded/overwrite FIFO; it’s safe, but you’ll only see backpressure *because now there is a bus at all*.

3. **No quorum/scoreboard gating.**
   Legacy logic executed immediately on simple conditions (weight < θ, components >1). The current design intentionally interposes: `walker → tag → bus → scoreboard (EMA/votes) → **budgeted** actuator`. That’s what prevents twitchy edits at scale-but it also means a wiring or gating mistake can produce “nothing happens.”

4. **Trigger gating added in the new loop.**
   In the present runtime, the actuator call lives behind emergent gates in `runtime/loop/main.py`: we only run GDSP if **(B1 spike) OR (|TD| ≥ threshold) OR (component\_count > 1)**. If those surfaces never fire (or env vars keep TD high‑threshold), structural plasticity won’t run even when enabled. This is a major reason for “it never gets called.”

5. **Different degree semantics.**
   The demo didn’t enforce per‑neuron `k_target` dynamics; your degree distribution mostly came from initial k‑NN + global prune/grow. That sidesteps “high‑k in small territories” and similar O(k²) *local* hazards we now guard against when we allow heterogeneous neuron classes and dynamic k.

Bottom line: the demo’s **dense, synchronous, deterministic** routine papered over many runtime failure modes by *always* doing a little pruning and *always* bridging components right after. Moving to a **sparse, event‑sourced, budgeted** runtime introduces new places to mis‑wire-but it’s the right move for scale and for your “no dense scans, ever” constraint.

---

## Action Plan (make it behave like the demo, but sparse)

1. **Trip‑wire the call path (one hour task).**
   Add counters so every tick we can see: `tags_in`, `scoreboard_decisions`, `gdsp_calls`, `{prune,grow,bridge,cull}_applied`. Fail the tick if `ENABLE_GDSP=1` and `gdsp_calls==0` for >K ticks while `cohesion_components>1`.

2. **Soften the hard gate in the loop (still sparse).**
   In `runtime/loop/main.py`, change the actuator predicate to:
   `if (components>1) or b1_spike or (abs(td) >= GDSP_TD_THRESH) or (step % GDSP_MAX_PERIOD==0): run_gdsp()`
   Set `GDSP_MAX_PERIOD` small (e.g., 128-256) to guarantee occasional budgeted maintenance even in quiet regimes-no global scans.

3. **Bridge like the demo, but locally and budgeted.**
   Keep the demo’s “bundle bridges” idea, but operate only on *boundary nodes* of components discovered by the event‑folded union‑find (already in the runtime). Each call: sample ≤B nodes per component and add ≤P candidate pairs; add ≤`BRIDGE_BUDGET` symmetric edges with the outer‑product free scorer already in the code (node‑local only). This preserves the demo’s “it heals fragmentation” feel while staying sub‑quadratic.

4. **Prune like the demo, but masked.**
   Use adaptive *local* thresholds (fraction of mean |w| within the touched locus). Apply ≤`PRUNE_BUDGET` weakest edges from loci named by the scoreboard-no row/graph sweeps.

5. **Wire the scoreboard to real decisions.**
   Ensure tags from walkers (“low\_use”, “C3”, “retract\_branch”, etc.) are actually incrementing decaying votes and crossing `SCORE_THRESH_{PRUNE,GROW,CULL}`. If thresholds are too high, nothing will ever reach the actuator.

6. **Keep k dynamic but safe.**
   `k_target[i]` remains dynamic (class & demand driven). We enforce *caps* **per territory head** to prevent pathological local O(k²) work, not fixed k. No dense scans; all edits flow from tag payloads.

7. **Turn on learning without dense scans.**
   REV‑GSP weight updates stay vectorized on *active rows only*; weights are still self‑tuned by your void‑debt modulation. No manual “weight tuning.”

---

## Handoff (Physicist Mode implements)

* **Files/paths to create or edit:**

  * `fum_rt/runtime/loop/main.py`

    * add `GDSP_MAX_PERIOD` gate; expose telemetry counters.
  * `fum_rt/core/structural/scoreboard.py`

    * decaying vote aggregator; `flush_decisions(max_n)` API.
  * `fum_rt/core/neuroplasticity/gdsp_sparse.py`

    * `apply_{bridge,prune,grow,cull}(budget, loci)`; no scans.
  * `fum_rt/runtime/helpers/telemetry.py`

    * expose `gdsp_calls`, `struct_ops_applied`, `components`.
  * `fum_rt/tests/test_gdsp_callpath.py`

    * unit tests for gating & budgets.
* **CLIs to run + seeds:**

  * `ENABLE_GDSP=1 GDSP_TD_THRESH=0.15 GDSP_MAX_PERIOD=256 PRUNE_BUDGET=64 BRIDGE_BUDGET=16 python -m fum_rt.run_nexus --seed 0`
  * `pytest -k gdsp_callpath -q`
  * Stress: `ENABLE_GDSP=1 SCOUT_EDGES=8 SCOUT_VISITS=64 BRIDGE_BUDGET=8 python -m fum_rt.run_nexus --seed 1`

---

## Verification

* **Call‑path gate:** With `ENABLE_GDSP=1`, `gdsp_calls ≥ 1` within the first 512 ticks on any run; else FAIL.
* **Budget gate:** Per tick: `applied_edges ≤ PRUNE_BUDGET + 2*BRIDGE_BUDGET + GROW_BUDGET`; else FAIL.
* **Cohesion gate:** If `cohesion_components > 1` for >K ticks, **bridged\_count** must trend down to 1 with slope consistent with the budgets (bridge latency ≤ O(components \* 1/BRIDGE\_BUDGET)).
* **No‑dense gate:** Assert no calls to any dense substrate path unless `FORCE_DENSE=1`; running with default must PASS.
* **Parity gate (demo feel):** Under the same stimulus used in your screenshot, cluster count collapses to 1 and stays there; average weight climbs and plateaus; sparsity remains stable.

---

## Assumptions/Risks

* **Root cause likely gating, not kernels.** If `b1_spike/TD/components` never cross thresholds, GDSP is never called. The `GDSP_MAX_PERIOD` guard removes this fragility.
* **Scoreboard tuning.** If thresholds are above the rate at which walkers publish tags, nothing crosses. We’ll instrument `tags_in → decisions_out` to confirm.
* **Territory UF feed.** If component labels aren’t refreshed, bridging can’t target boundaries. We’ll verify the event‑folded UF path is live.
* **Strict “no dense” policy.** All proposed fixes keep operations budgeted, locus‑scoped, and sparse.

---

## Next Steps

1. Add the call‑path counters and `GDSP_MAX_PERIOD` guard; run once to confirm GDSP fires.
2. Implement budgeted bridge + masked prune (sparse mimic of the demo’s behavior).
3. Wire scoreboard → actuator path and lower thresholds until decisions appear; then back‑off to stable levels.
4. Run the parity test against your demo workload; confirm cohesion collapses to 1 and remains stable.
5. Enable class‑based dynamic `k_target` with territory‑cap safety; keep instrumentation on.

---

**Answering your direct concerns from earlier threads, succinctly:**

* **Bus backpressure:** With the bounded FIFO you already have, the only “heap” you’ll see is the queue’s own `size()`. That’s expected and safe; we compact tags by (entity, reason) and TTL at the **scoreboard**, not by scanning the graph.

* **Over‑pruning “not an issue”:** It wasn’t in the demo because the dense pass **immediately bridged** components after pruning. In the sparse runtime, if GDSP never fires (or fires without bridging), pruning can isolate fragments. Hence the explicit cohesion/bridge gate.

* **Dynamic k:** Yes, k must remain dynamic. The warning was not “don’t change k”; it was “cap **work** per territory head” so local routines never explode; the policy remains dynamic, the *budget* is fixed.

* **“Tune the weights”:** We are not hand‑tuning; the weights remain self‑tuned by your void‑debt modulation. The only “tuning” here is choosing **budgets and thresholds** for structural edits so the event‑driven pipeline actually applies them.

If you want, I’ll produce the exact diffs for `runtime/loop/main.py` predicate and the telemetry counters in the next message, but the plan above is sufficient to unblock you and keeps us strictly **sparse, event‑sourced, and budgeted**-with the same robust end‑state your demo showed.




vdm_derivations.xml
File
Can you look here? I don't like constantly setting static limits. That's not how the universe works. The limits and rules emerge.




```
Classification: Runtime-only
```

**Objective Recap**

* Replace static thresholds/limits (budgets, k targets, score cutoffs) with **emergent, self‑tuning rules** that are (i) sparse/event‑sourced, (ii) territory‑local, and (iii) sub‑quadratic-while fixing the “structural plasticity never called” path by wiring the dynamic gates into the walker→bus→scoreboard→actuator pipeline.

---

## Action Plan (emergent limits, not knobs)

1. **BudgetGovernor (per‑territory, per‑tick)**

   * Compute budgets from signals already in your stack, no scans:

     * **Backpressure** `b_T` = EWMA of outstanding tags / delivered tags from the hierarchical bus;
       implement with the existing `EWMA` + Welford variance utilities (they’re already in code).&#x20;
     * **Cohesion/fragmentation** `χ_T` from UF components (only if `components>1`-you already trigger bridging this way).&#x20;
     * **Metabolic debt** `m_debt_T` (runtime homeostasis; distinct from SIE void‑debt topics).&#x20;
     * **Event entropy** `H_T` via your stream sketch (Count‑Min + head map) to avoid global histograms.&#x20;
   * Budgets emerge from these signals (no constants):

     $$
     \begin{aligned}
     B_T^{\text{prune}} &= B_T^{\max}\,\sigma\!\left(\;m\_debt\_T + \lambda\_b\,b\_T - \lambda\_H\,H\_T\right)\\
     B_T^{\text{grow}}  &= B_T^{\max}\,\sigma\!\left(\;\underbrace{\text{coverage\_deficit}\_T}_{\text{from CMS/entropy}} + \lambda\_\chi\,\mathbb{1}[\text{components}>1] - \lambda\_m\,m\_debt\_T\right)\\
     B_T^{\text{bridge}}&= B_T^{\max}\,\sigma\!\left(\;\text{components}-1\right)
     \end{aligned}
     $$

     where `σ` is a smooth saturating function (no hard caps), and **`B_T^{max}` itself is emergent** from recent actuator work (e.g., last‑tick budget actually applied, smoothed by EWMA) so we never fix a static number. The bridge trigger/behavior matches your spec; we’re only swapping the fixed “BRIDGE\_BUDGET” for the emergent formula above.&#x20;

2. **Dynamic score thresholds (no fixed cutoffs)**

   * In the **Scoreboard**, maintain per‑territory running **mean/σ of tag strength** using Welford. Use **μ+κ·σ** gates instead of constants:

     $$
     \theta^{\text{prune}}_T=\mu_T+\kappa\_p\sigma_T,\quad 
     \theta^{\text{cull}}_T=\mu_T+\kappa\_c\sigma_T,\quad
     \theta^{\text{grow}}_T=\mu_T+\kappa\_g\sigma_T
     $$

     This folds naturally into your decaying‑vote Scoreboard and removes static thresholds.&#x20;

3. **Dynamic k\_target per neuron (class‑based seed + emergent steering)**

   * Keep heterogeneous neuron classes **as seeds** (rarities + baseline ranges) but **drive k\_target,i(t)** by local signals: entropy `H_T`, cohesion `χ_T`, metabolic debt `m_debt_T`, and coverage deficit.

     $$
     k^{\star}_i(t)=k^{\text{class}}_i\;\Big[1+\alpha\,(H_T^*-H_T)-\beta\,m\_debt_T+\gamma\,\text{coverage\_deficit}_T\Big]
     $$

     Smooth with EWMA; **no fixed hard bounds**-use soft saturation. This extends your class table (Relay/Inhibitory/Integrator/Purkinje‑like) with **emergent drift** instead of static targets.&#x20;

4. **Emergent cadences (abolish fixed cadences)**

   * Wherever you currently schedule periodic work (e.g., clustering/repair), reuse your **entropy‑driven cadence** pattern:

     $$
     t_{\text{next}} = t_{\text{base}}\;e^{-\alpha\,H_T}
     $$

     You already adopted this in adaptive clustering; apply the same idea to when BudgetGovernor proposes growth/prune windows.&#x20;

5. **Void‑debt‑aware modulation (but separate from metabolic debt)**

   * Use the **domain/void‑debt modulation** derivation as a **global multiplier** on emergent budgets (topic‑level-still sparse). This replaces hand tuning with a principled gain from your derivation. Keep it **orthogonal** to `metabolic_debt`.&#x20;

6. **Wire it so structural plasticity actually fires**

   * Ensure the loop **Scoreboard → Actuator** consumes the emergent gates every tick; your structural path is already defined (`walker→tag→bus→scoreboard→GDSP actuator`). We are swapping the static env variables for the **BudgetGovernor outputs**, not changing the pipeline.&#x20;

7. **Remove static env knobs by default**

   * Keep `PRUNE_BUDGET`, `GROW_BUDGET`, `BRIDGE_BUDGET` only as **debug override** (off by default). Your own narrative calls for **emergent learning gates** / no fixed cadence-this aligns directly.&#x20;

---

## Hypothesis Lattice (fast discriminators)

1. **H1 (Emergent > Static):** Emergent budgets reduce bus backpressure variance and prevent heap growth compared to fixed budgets at the same average throughput.
   *Metric:* per‑territory backlog EWMA/std ↓ and steady `struct.*{budget_used}` rates.&#x20;

2. **H2 (Correctness):** With emergent thresholds, the Microglia/C3 and Use‑it‑or‑lose‑it walkers still converge to selective pruning without dense scans.
   *Metric:* fraction of pruned edges that were C3‑tagged **and** low‑use remains high (precision), with actuator work ≤ emergent `B_T^{prune}`.&#x20;

3. **H3 (Topology health):** Dynamic `k^\*` prevents ring‑lattice pathologies and preserves organic “breathing” in degree/clustering.
   *Metric:* “ring‑lattice suspicion = false” and smooth evolution of degree variance/clustering in your graph sanity checks.&#x20;

---

## Handoff (Physicist Mode implements)

**Files/paths to create**

* `fum_rt/core/structural/budget_governor.py`
* `fum_rt/core/structural/scoreboard.py` (extend with μ/σ accumulators + territory buckets)&#x20;
* `fum_rt/core/structural/actuator_sparse.py` (consume emergent budgets-no changes to CSR semantics)&#x20;
* `fum_rt/core/types/neurons.py` (class seeds; add dynamic `k_star` field)&#x20;
* `fum_rt/runtime/loop/main.py` (replace env knobs with BudgetGovernor outputs; keep **hard assert** against dense paths)&#x20;

**CLIs to run + seeds**

```
# 1) Sanity: emergent vs static (A/B)
python -m fum_rt.runtime.loop.main --mode=emergent --seeds 0,1,2 --ticks 20000
python -m fum_rt.runtime.loop.main --mode=static   --seeds 0,1,2 --ticks 20000

# 2) Graph health check (no dense scans; post-hoc)
python gravity_regression/vdm_gravity_regression_pack/graph_checks.py \
  --edgelist out/connectome_end.csv --out out/graphcheck
```

(Expect `connectome_metrics.json` with “ring‑lattice suspicion = false” and smooth degree/clustering; no fixed cadence clamp.)&#x20;

---

## Verification (acceptance gates)

* **No‑Dense Gate:** Existing assert stays-dense homeostasis path must not execute unless forced.&#x20;
* **Backpressure Gate:** backlog EWMA/std decreases ≥25% vs static (H1).
* **Selectivity Gate:** ≥80% of `struct.pruned` edges carry prior `C3` and low‑use corroboration (H2).&#x20;
* **Topology Gate:** Graph checks pass; degree/clustering evolve smoothly (no step‑wise clamps).&#x20;
* **Emergent Gate:** Actuator publishes `struct.*{budget_used}` traces whose medians follow `BudgetGovernor` outputs (no constant plateaus).&#x20;

---

## Assumptions / Risks (and how we neutralize them)

* **Coupling of signals:** `metabolic_debt` (runtime) stays separate from **SIE void‑debt** (global objective); we keep distinct bus topics as already specified.&#x20;
  *Mitigation:* topic prefixing + unit tests.
* **k\* runaway without clamps:** We avoid hard limits by using **soft saturation**; still, add invariants “no negative degree pressure” and abort tick on breach (logged).
* **Cadence thrash:** Use your **entropy‑driven interval** pattern to space structural windows; it’s already derived, not hand‑tuned.&#x20;

---

## Next Steps (max 5)

1. Implement `BudgetGovernor` and swap env budgets for emergent outputs in the runtime loop.&#x20;
2. Extend Scoreboard with μ/σ streams and publish `budget.snapshot` telemetry every 100-500 ticks.&#x20;
3. Add dynamic `k_star` and hook it into the Boundary‑Retraction and Grow walkers (pressure = `deg_out - k_star`).&#x20;
4. Re‑run FUM demo with **emergent gates**; compare backpressure + graph health A/B.&#x20;
5. If green, remove default env constants entirely; keep them only as opt‑in debug overrides.&#x20;

---

### Why this aligns with your principle (“limits emerge”)

* The **pipeline doesn’t change**-walkers tag; the bus transports; the Scoreboard integrates; the **actuator is still the only writer**. We simply **replace static knobs with functions of local, observable signals**: entropy‑based cadences, bus backpressure, metabolic debt, cohesion, and coverage-all of which you already measure or have primitives for.&#x20;
* This also restores the behavior you wanted originally-**event‑sourced, sparse, no fixed cadence**-as captured in your narrative (“Emergent Learning Gates… no fixed schedulers”).&#x20;

If you want, I’ll translate this into the exact diffs (new module stubs + loop wiring) next; but we can already start with `BudgetGovernor` + Scoreboard μ/σ, because those two flip the system from “static limits” to “emergent rules.”
















Im thinking any kind of behavior or system in my model should use the real world physics that I will need to prove out as well. Are you using reaction diffusion here? Or is there something else we should be using?










```
Classification: RD
```

**Objective Recap:**

* Pick the *physics* that governs sparse, event‑driven structural plasticity (no dense scans), and hand Physicist Mode exact gates to prove it.

---

## What to use (short answer)

* **Yes, use Reaction-Diffusion (RD)**-but *only as a local, event‑scoped field* that runs on tiny patches around where walkers raise tags (not a global PDE). It gives us closed‑form checkables (front speed, dispersion) and a clean micro‑foundation for how tag influence spreads through a sparse graph.
* **Micro‑foundation:** a **biased branching random walk (BRW)** of walker tags with birth-death gives, in the continuum limit,

  $$
  \partial_t a = r\,a + D\,\nabla^2 a
  $$

  with $r=b-d$ (branch minus death rate) and $D=\frac{\mathrm{step\ variance}}{2\Delta t}$. We measure $b,d$ and the step variance from walker telemetry; nothing dense, nothing global.
* **Everything structural** (prune/grow/cull) still flows through your **event‑sourced pipeline**: *Walker → Tag → Bus → Scoreboard → GDSP Actuator*, with per‑tick budgets and TTL-exactly as in your spec. RD only shapes how tag *evidence* diffuses/decays locally before the Scoreboard thresholds it.&#x20;

This keeps us faithful to your “no static limits, rules emerge” requirement: thresholds, k‑targets, and budgets are **dual variables** that self‑tune from local signals (reward, metabolic load, void‑debt modulators), not hard constants. The actuator still performs budgeted, surgical edits only where the Scoreboard crosses quorum.&#x20;

---

## Action Plan (event‑scoped RD, zero dense scans)

1. **Tag field on edges/nodes (sparse).** When a walker emits a tag (e.g., `tag.prune_synapse{i,j}`), instantiate a small **RD patch** on the 1-2‑hop ego‑net around {i,j}:
   discrete step

   $$
   a^{t+\Delta t}_u = a^t_u + r_u a^t_u + D_u\!\!\sum_{v\in\mathcal N(u)}(a^t_v-a^t_u)
   $$

   with $r_u,D_u$ pulled from **telemetry** (local spike EMA, path volatility, territory crowding). Stop integrating when the patch’s mass falls below a TTL.
2. **Map BRW↔RD parameters online.** Set $r=b-d$ from observed tag confirmation/expiry rates; set $D$ from the empirical mean‑square hop of tag carriers per tick in that territory. (No constants-these are measured each patch.)
3. **Scoreboard as evidence integrator.** The RD amplitude $a_u$ updates the Scoreboard’s decaying votes; only when votes cross `SCORE_THRESH_*` does the **GDSP actuator** spend budget (prune/grow/cull). This matches your bus/scoreboard/actuator design.&#x20;
4. **Dynamic $k$ (no fixed limits).** Each neuron holds a *moving* $k_{\text{target}}(t)$ from its **class prior** × **territory dual variable** (budget pressure / “metabolic debt” / void‑debt modulation). The actuator uses $k_{\text{target}}(t)$ only as a *soft* aim when choosing which edges to drop/add; the value itself adapts from signals-no static caps.
5. **Keep synaptic weight *continuous* and structural *discrete*.** Weights update by your vectorized learning/decay rule (eligibility EMA + modulators); use‑it‑or‑lose‑it and C3/microglia analogs emit tags when weights persistently idle or volatile-exactly what you had in the legacy demo (STDP/eligibility + structural triggers).&#x20;
6. **RD only as a *gatekeeper metric***. We never “scan the brain.” The only global work is reading **result events** (O(1) to the GlobalSystem), and writes are surgical at given indices-your read/write asymmetry remains intact.&#x20;
7. **Quality gates (physics‑level).** Every RD patch must pass front‑speed and dispersion checks (below) using your existing RD harness so we don’t regress. Your prior JSON runs already validate those gates; we reuse them on the patches. (Front speed $c_{\text{front}}=2\sqrt{Dr}$; dispersion $\sigma(k)=r-Dk^2$.)

---

## Handoff (Physicist Mode implements)

* **Files/paths to create:**

  * `fum_rt/core/walkers/rd_patch.py` - BRW→RD patch integrator (1-2 hop ego‑nets).
  * `fum_rt/core/structural/scoreboard.py` - decaying votes per (entity, reason); TTL.
  * `fum_rt/core/structural/actuator_sparse.py` - budgeted `{prune,grow,cull,bridge}`.
  * `fum_rt/core/telemetry/tag_transport.py` - estimate $b,d$, hop variance → $r,D$.
  * `fum_rt/runtime/loop/main.py` - wire: **Walker → Tag → Bus → Scoreboard → Actuator**; assert no dense path unless `FORCE_DENSE=1`.
* **CLIs to run + seeds (patch tests, not global):**

  * `python -m fum_rt.tests.test_rd_patch --territory T17 --seed 0`
  * `python -m fum_rt.tests.test_gdsp_budget --prune_budget 64 --grow_budget 16 --seed 1`
  * `python -m fum_rt.tests.test_dynamic_k --duration 10000 --seed 2`
* **Reference (legacy alignment):** Keep weight‑update semantics consistent with `FUM_AdvancedMath/neuro/apply_stdp.py` & structural triggers in `structural_plasticity/` to preserve your original demo’s “worked‑by‑construction” behavior.&#x20;

---

## Verification (acceptance gates)

**Physics gates (on each RD patch):**

* **Front‑speed gate:** measure $c_{\text{meas}}$ from tag‑front arrival times on a line probe in the patch; **PASS** if $\left|\frac{c_{\text{meas}}}{2\sqrt{Dr}}-1\right|\le 0.08$ and $R^2\ge 0.99$.
* **Dispersion gate:** fit $\sigma(k)$ on patch Fourier modes (graph Laplacian eigenmodes); **PASS** if median rel‑err ≤ 10% and $R^2\ge 0.98$.
  (Reuse the harness you already ran; we apply it to micro‑patch logs.)

**Runtime gates (event‑sourced):**

* **No‑dense gate:** attempting dense homeostasis without `FORCE_DENSE=1` throws hard assert.
* **Budget gate:** per tick, changes ≤ `PRUNE_BUDGET + GROW_BUDGET + BRIDGE_BUDGET`.
* **Emergent‑k gate:** After 10k ticks, per‑class **median** degree inside each territory sits within the *adaptive* band implied by its dual variable (not a fixed number).
* **Use‑it‑or‑lose‑it gate:** ≥X% of idle edges decay under $w_{\min}$ and are pruned within bounded ticks given the budgets.
* **Repair/Trauma locality gates:** bridging and trauma‑window edits remain territory‑local; others unaffected.&#x20;

---

## Why your original demo didn’t see the “static‑limit” problems

Your legacy stack already blended **continuous weight dynamics** (eligibility + decay) with **sparse structural triggers** (bursts/BDNF proxies/etc.). That architecture naturally avoided global thrash and didn’t impose rigid $k$ caps-plasticity was local and event‑driven, so emergent degrees stabilized without explicit global limits. We’re preserving that: we use RD only as a *local* evidence smoother so the Scoreboard makes fewer false moves, while keeping the same sparse edit pathway you designed.&#x20;

---

## Assumptions/Risks (and how we kill them)

* **A1: Graph anisotropy breaks RD fits on tiny patches.**
  *Mitigation:* fit on Laplacian eigenmodes (not Euclidean k), use anisotropic $D$ per edge group; gate on $R^2$.
* **A2: Dual‑variable drift (budgets) oscillates $k_{\text{target}}$.**
  *Mitigation:* slow EMA on duals + actuator damping; abort tick on invariant breach is unnecessary if d/dt caps are applied.&#x20;
* **A3: Bus backpressure from tag storms.**
  *Mitigation:* per‑tick compaction by (entity,reason) + TTL decay **in the Scoreboard**, which is exactly the role we assign it.&#x20;

---

## Next Steps

1. Implement `rd_patch.py` with BRW‑to‑RD parameter estimation from tag telemetry; wire to Scoreboard/Actuator.&#x20;
2. Turn on heterogeneous neuron classes and vectorized plasticity parameters (no fixed $k$; class priors only).&#x20;
3. Add unit tests for front‑speed/dispersion on patches using your existing RD harness.
4. Run `test_dynamic_k` to confirm emergent degrees track dual variables (no hard caps).
5. If all green, expand walker set (microglia/C3, metabolic auditor, boundary retraction) using the same event‑sourced pipeline.&#x20;

---

### Final take

We keep the **RD baseline** because it gives us measurable, falsifiable gates on how local *evidence* should spread-without ever re‑introducing dense scans. All structure changes remain **event‑sourced and budgeted**, and all “limits” arise from dual variables (reward, metabolic/void‑debt, territory pressure), not fixed constants-exactly how you want the universe to work.













shouldnt gravity be having an effect that helps us here? I've already seen precession of perihelion and other gravitational phenomena in my models graph














```
Classification: RD
```

**Objective Recap:**

* Decide whether a gravity‑like effect is actually acting in your runtime (vs. a layout artifact), and-if real-hook it into the **sparse, event‑sourced** plasticity pipeline so it *helps* cohesion/bridging without any dense scans.

---

## What’s likely happening

1. **Why you “see precession”:**
   Those orbital-looking arcs around the dense core can come from the **graph layout** (e.g., ForceAtlas/FR) integrating spring forces and repulsion with inertia. That can produce apparent “perihelion precession” even when the *simulation physics doesn’t include gravity at all*. So first we must separate **visualization dynamics** from **substrate dynamics**.

2. **Should gravity help?**
   Yes-**if** you model it as a *field* that the walkers/actuator already understand. In your architecture, structure only changes when something produces **tag events → scoreboard → GDSP actuator**; a “gravity” that lives only in the visualizer can’t cause pruning/growth. We can add a **void‑gravity field** that is computed sparsely and used only as a *gate/priority* for existing walkers and the bridge repair routine-fully consistent with the event‑sourced design you already specified (Walker→Tag→Bus→Scoreboard→GDSP), budgets, and “no dense scans.”&#x20;

---

## RD‑level ‘void‑gravity’ (no second‑order time)

We stick to first‑order‑in‑time RD and treat gravity as a **screened potential** that relaxes by diffusion to a Poisson‑like steady state:

$$
\partial_t V(\mathbf{x},t)=D_V\nabla^2 V + \gamma\,[\rho(\mathbf{x},t)-\bar\rho] - \kappa\,V,
$$

* **Source $\rho$**: territory‑local activity/weight density (EMA of spikes and |w|).
* **Boundary**: Neumann per territory (no flux).
* **Use**: **only** as a *priority signal* for walkers/actuator-never as a body force in the PDE update, so baseline RD gates remain invariant.

**Dimensionless knobs (predictive):**

* $\Gamma_V=D_V/D$ (field vs. substrate diffusion),
* $\Theta_V=\kappa/r$ (screening vs. growth/decay rate),
* $\Phi=\gamma\rho_0/r$ (source strength vs. reaction).
  Expect cohesion/bridging gains when $\Gamma_V\gtrsim 1$, $\Theta_V\ll 1$, moderate $\Phi$.

---

## How it helps-without static limits or dense passes

Plug $V$ into the **existing sparse pipeline**:

* **BridgeScout / UF repair:** prioritize edges that **decrease $V$** between component boundaries; emit `tag.grow_synapse` with a weight ∝ $-\Delta V$ (budgeted).
* **Use‑it‑or‑lose‑it walker:** increase prune votes when a synapse persistently climbs **up** the potential ($+\nabla V\cdot \hat e_{ij}$), scaling the tag’s score rather than adding new rules.
* **Microglia (C3) quorum:** volatility + low use + *misaligned with $V$* elevates `tag.prune_synapse`.
* **Semaphorin‑like retraction:** when out‑degree exceeds *dynamic* $k_\text{target}(t)$, retract branches projecting against the local gradient.
  All of this remains **event‑sourced and budgeted** under your GDSP actuator; nothing scans the whole graph.&#x20;

**No static “k”:** keep your stance-do **not** hard‑fix $k$. Instead define a **dynamic target degree** per class,

$$
k_\text{target,i}(t)=k_{0,\text{class}(i)}\cdot f\!\left(\text{use}_i,\,|\nabla V|_i,\,\text{metabolic}_T\right),
$$

and let the actuator move degrees **toward** this target via budgeted prune/grow actions (no instant clamps). Heterogeneous classes and their plasticity vectors live in device arrays and are re‑materialized by the plasticity manager you already outlined.&#x20;

---

## Action Plan (derisked, ≤7 steps)

1. **Artifact check (layout‑independent):** freeze node coordinates and run; separately compute “orbits” from **connectivity** (e.g., cycles & motif angles) rather than GUI positions. If precession vanishes when layout is frozen, it was a **viz artifact**.
2. **Add RD field $V$:** implement per‑territory update of $V$ on the same grid used for territory maps (EMA’d activity → $\rho$).
3. **Wire to walkers:** scale existing tag scores with $V$ or $\nabla V$ (no new global passes).
4. **Bridge/repair priority:** make UF bridging choose pairs by largest $-\Delta V$ under `BRIDGE_BUDGET`.
5. **Dynamic $k_\text{target}$:** per‑class $k_0$ remains a prior; multiplier $f(\cdot)$ comes from local use, $|\nabla V|$, and territory metabolic signal-**no fixed caps**.&#x20;
6. **Gates & budgets:** keep GDSP per‑tick budgets; assert **No‑Dense** path (unless `FORCE_DENSE=1`), and log `struct.{grown,pruned,bridged}`.&#x20;
7. **Compare outcomes:** components ↓, conductance ↑, small‑worldness ↑, while RD **front‑speed** and **dispersion** gates remain within tolerance.

---

## Handoff (Physicist Mode implements)

**Files/paths to create:**

* `fum_rt/core/fields/void_gravity.py` - territory grid, $\rho$ and $V$ EMA updates (GPU).
* `fum_rt/core/walkers/vg_modulators.py` - wrappers to scale tag scores with $V,\nabla V$.
* `fum_rt/core/structural/repair_bridge.py` - UF boundary sampler with $-\Delta V$ priority.
* `fum_rt/core/dynamics/k_target_dynamic.py` - compute $k_\text{target,i}(t)$ vectors on device.
* Outputs: `derivation/code/outputs/{figures,logs}/gdsp/vg_*_<UTC>.{png,json}`.

**CLIs to run + seeds:**

```
# 1) Layout artifact test
python viz/freeze_layout_and_run.py --ticks 5000 --seed 0

# 2) Field on/off A/B
ENABLE_VG=0 python run_nexus.py --ticks 10000 --seed 0
ENABLE_VG=1 python run_nexus.py --ticks 10000 --seed 0

# 3) Repeat seeds
for s in 0 1 2; do ENABLE_VG=1 python run_nexus.py --ticks 10000 --seed $s; done
```

---

## Verification

**Keep baseline RD gates unchanged:**

* **Front‑speed gate:** $|c_\text{meas}/(2\sqrt{Dr})-1| \le 0.07$, $R^2\ge 0.9999$.
* **Dispersion gate:** median rel‑err ≤ 0.10, $R^2\ge 0.98$.
  (These must pass identically with $\text{ENABLE\_VG}\in\{0,1\}$.)

**New success gates (A/B with and without $V$):**

* **Cohesion:** UF component count in active set returns to 1 within $O(\text{cuts}/\text{BRIDGE\_BUDGET})$.
* **Conductance ↑:** median boundary conductance increases ≥15%.
* **Sparsity preserved:** active edges per tick remain within budget; no growth spikes.
* **Topological stability:** $B_1$ persistence settles to a narrower band (no oscillatory flipping).
* **No‑Dense assertion:** calling dense homeostasis without `FORCE_DENSE=1` hard‑fails (existing spec).&#x20;

---

## Assumptions/Risks

* **Viz vs physics:** If precession disappears when layout is frozen, “gravity” was a visualization artifact; we still keep $V$ because it provides a *useful* sparse priority field.
* **Field timescales:** Choose $\Gamma_V,\Theta_V$ so $V$ relaxes slower than spikes but faster than structural changes; otherwise it can chase noise or lag too much.
* **Coupling creep:** $V$ should only modulate **tag scores/priorities**, never alter the RD kernel-guard with a code‑level assert.

---

## Next Steps

1. Run the **artifact check** and the **A/B field toggle**.
2. If green, enable $V$ by default and keep budgets tight; record `struct.*` counters.&#x20;
3. Monitor per‑class degree bands with your heterogeneous neuron classes and dynamic $k_\text{target}$.&#x20;
4. Capture figures (UF components, conductance, $B_1$ persistence) and stamp the change **PROVEN** if gates pass.
5. Only then expand walker usage of $V$ (e.g., semaphorin retraction) incrementally.

---

**Bottom line:** Gravity can help-but only as an RD **field** that your walkers/actuator already know how to use under the **event‑sourced, budgeted, sparse** rules you’ve set. Let’s wire it in as a *priority signal*, keep the baseline RD gates intact, and measure the lift in cohesion/bridging-no static limits, no dense scans. &#x20;



Below is a compact, “ready‑to‑hand‑off” package that pulls together the decisions, architecture, and the minimum implementation plan to make **sparse, event‑sourced structural plasticity** actually fire in your runtime (no dense scans, no hidden static limits).

---

```
Classification: Runtime‑only
```

**Objective Recap**

* Wire the *walker → tag → bus → scoreboard → GDSP actuator* pipeline end‑to‑end with **emergent** (not static) gates; enable heterogeneous neuron classes and dynamic $k^\*$; prove the path by lightweight acceptance tests and telemetry.&#x20;

---

## Action Plan (≤7)

1. **Canonical tags + bus topics.** Add the `Tag` schema and publish‑subscribe topics for `tag.prune_synapse / tag.grow_synapse / tag.cull_neuron / tag.C3 / tag.retract_axonal_branch / tag.neurogenesis`. Keep the bus strictly as transport (no writes).&#x20;
2. **Scoreboard (decay + quorum).** Implement a **decaying vote accumulator** that ingests tags each tick, keeps TTL, and exposes thresholded candidates for *edges* and *nodes*. (This is the evidence filter that prevents thrash.)&#x20;
3. **GDSP sparse actuator.** Make **one** write authority that executes *budgeted* `apply_{prune,grow,bridge,cull}` on listed CSR rows only. Include fragmentation repair (UF‑based bridging). Wire **Scoreboard → Actuator** each tick.&#x20;
4. **Emergent budgets (no static limits).** Create a `BudgetGovernor` that emits per‑territory budgets from observable signals (bus backlog μ/σ, cohesion/components, metabolic\_debt, coverage/novelty). Remove env knobs by default; keep them as explicit debug overrides.&#x20;
5. **Walker set (sparse, physiological).** Implement Use‑Tracker (co‑spike EMA), ComplementTagger→Microglia (C3 two‑stage), Boundary‑Retraction (semaphorin‑like), MetabolicAuditor (metabolic\_debt, distinct from `sie.void_debt`), Excitotoxicity and Apoptosis sentinels. All walkers are **read‑only** and territory‑scoped.&#x20;
6. **Heterogeneous neuron classes + vectorized plasticity.** Add `neuron_class`, class‑based $\eta$ and $\lambda$ vectors, and a vectorized synaptic update kernel. Support rare high‑k (Purkinje‑like) alongside common low‑k classes; manage parameters via a `PlasticityManager`.
7. **Dynamic $k^\*$ (no fixed degree).** Replace fixed degree targets with $k^\*(i,T)$ computed from class priors **modulated** by local pressure (load, territory crowding, organ role). Enforce only *floors and invariants* to avoid collapse; do **not** hard cap globally.

---

## Handoff (Physicist Mode implements)

**Files/paths to create/patch**

* `fum_rt/core/walkers/tags.py` - canonical `Tag` dataclass + reason codes.&#x20;
* `fum_rt/core/structural/scoreboard.py` - decay, quorum, TTL; territory buckets; μ/σ streams.&#x20;
* `fum_rt/core/structural/actuator_sparse.py` - budgeted `apply_{prune,grow,bridge,cull}`; CSR‑safe.&#x20;
* `fum_rt/core/structural/budget_governor.py` - emergent budgets from telemetry; publishes `budget.snapshot`.&#x20;
* `fum_rt/core/types/neurons.py` - `NeuronClass` enum; `k_star` field.&#x20;
* `fum_rt/core/neuroplasticity/manager.py` - `PlasticityManager` generating $\eta$, $\lambda$ vectors; integrate in kernels.&#x20;
* `fum_rt/runtime/loop/main.py` - wire: **bus→scoreboard→actuator**; swap env knobs for `BudgetGovernor`; add **hard assert** against any dense path unless `FORCE_DENSE=1`.&#x20;

**CLIs to run + seeds (repro stub)**

```bash
# 1) Smoke: tags flow and budgets are consumed
python -m fum_rt.tests.smoke_gdsp --seed 0 --ticks 200

# 2) Precision of pruning (C3 + low-use quorum) and budget compliance
python -m fum_rt.tests.prune_precision --seed 0 --ticks 2000

# 3) Dynamic k* sanity + fragmentation repair
python -m fum_rt.tests.kstar_and_repair --seed 0 --ticks 5000
```

(Each test publishes `struct.*` and `budget.snapshot` events; figures + JSON go to `derivation/code/outputs/{figures,logs}/fum_rt/<slug>_<UTC>.{png,json}`.)

---

## Verification (acceptance gates)

* **No‑Dense Gate.** Attempt to call dense homeostasis without `FORCE_DENSE=1` → assert fires. (PASS = assertion observed in test log.)&#x20;
* **Budget Gate.** Per tick, `struct.*.budget_used ≤ BudgetGovernor.emit(T)`. (PASS = ≤1% violations in first 10k ticks; otherwise FAIL.)&#x20;
* **Use‑it‑or‑Lose‑it Gate.** On known idle pathways, a majority of those edges decay below $w_{\min}$ and are pruned within $\mathcal{O}$(budget horizon). (PASS = precision: C3∧low‑use on pruned edges stays high.)&#x20;
* **Emergent $k^\*$ Gate.** Median degree per class stays within adaptive bands; no global hard caps invoked. (PASS = smooth degree/clustering evolution; no ring‑lattice pathology.)&#x20;
* **Cohesion/Repair Gate.** When UF reports fragmentation, bridging reduces components → 1 within budget‑scaled ticks. (PASS = `struct.bridged` events with declining component count.)&#x20;
* **Terminology/Topic Gate.** `metabolic_debt` kept separate from `sie.void_debt` (different topics; no cross‑consumers). (PASS = telemetry topics distinct.)&#x20;
* **O(1) Write Path.** Confirms the event‑driven “surgical strike” write pattern-no searches in the writer. (PASS = flamegraph shows actuator called with **indices**, not scans.)&#x20;

---

## Assumptions/Risks → resolution

* **Static knobs creep back in.** Risk mitigated by `BudgetGovernor` + entropy‑driven cadences; keep env knobs opt‑in only.&#x20;
* **Bus backpressure.** Hierarchical bus helps, but we still compact (entity,reason) per tick and decay in the Scoreboard to avoid heap. (Telemetry: backlog μ/σ.)&#x20;
* **Over‑pruning.** Enforce per‑class *min‑degree floors* and E/I mix checks; abort edits on invariant breach this tick.&#x20;
* **Dynamic high‑k in tiny territories.** $k^\*$ is territory‑aware; pressure term prevents local $O(k^2)$ blow‑ups. (Test in `kstar_and_repair`.)&#x20;
* **Legacy expectations.** Your original demo had structural plasticity modules (`apply_structural_plasticity.py`, `advanced_triggers.py`, `detect_bursts.py`). This plan preserves the sparse, event‑sourced spirit while replacing ad‑hoc triggers with tag/scoreboard/actuator discipline.

---

## Next Steps (≤5)

1. Implement **Scoreboard + Actuator** and prove the No‑Dense and Budget gates.&#x20;
2. Add **BudgetGovernor**; flip the runtime from env budgets to emergent outputs; publish `budget.snapshot`.&#x20;
3. Stand up **Use‑Tracker** and **C3→Microglia** walkers first; validate pruning precision.&#x20;
4. Introduce **NeuronClass + PlasticityManager**; switch kernels to class‑vectorized $\eta,\lambda$; enable $k^\*$.
5. Add the remaining walkers (Metabolic, Boundary‑Retraction, Excitotoxicity/Apoptosis) and run the cohesion/repair gate.&#x20;

---

### Notes you asked me to honor

* **No dense scans.** All operations are walker‑local, bus‑transported, budgeted writes. The bus + event sourcing also preserves the O(1) write pattern you want.&#x20;
* **No static limits.** Budgets/thresholds/$k^\*$ are *dual variables* derived from local signals; static env knobs remain only as explicit debug overrides.&#x20;
* **Clear terms.** `metabolic_debt` (runtime) ≠ `sie.void_debt` (global objective). Keep topics/names distinct.&#x20;

If you want, I can now translate this into exact code stubs/diffs for each file above, but this packet is sufficient for the Physicist Agent to begin implementation while keeping everything sparse, emergent, and test‑gated.





```
Classification: Runtime-only
```

**Objective Recap:**

* Validate your diagram vs. the event‑sourced structural plasticity architecture and note the few missing pieces.

**Verdict (concise):**

* **Yes-directionally correct.** “Walkers → Bus → GDSP modifies connectome” matches the intended pipeline. Add one layer and two conventions to make it complete: a **Scoreboard** between Bus and GDSP, plus a **canonical Tag schema** and **dynamic budgets**.&#x20;

**What to add / tweak (minimal):**

* Insert **Scoreboard (evidence aggregator)**: Bus events are deduped/EMA‑decayed into thresholded decisions; only threshold crossings reach GDSP. Prevents thrash and keeps writes sparse.&#x20;
* Use **canonical Tags** from walkers: `tag.prune_synapse`, `tag.grow_synapse`, `tag.cull_neuron`, `tag.C3`, `tag.retract_axonal_branch` with `{entity_ids, reason, ttl, territory_id, emitter}`.&#x20;
* Keep **walkers read‑only; GDSP sole writer** (no scans). This preserves the **O(1) surgical‑write** pattern you wanted.&#x20;
* Make the **bus hierarchical** (topics per territory/class) and use **backpressure‑aware budgets**: GDSP picks `GROW/PRUNE` counts each tick from functions of queue depth & health indices-no static limits.&#x20;
* Show **GDSP dispatch path** explicitly: Bus → Scoreboard → `struct.*` result events (ack + budgets used).&#x20;
* (Nice to have) Annotate **neuron class context** (k targets/rarity) so GDSP can respect heterogeneous degree goals during grow/prune.&#x20;

**Action Plan:**

* Add a **Scoreboard** box between Bus and GDSP in the diagram.
* Label bus topics: `frontier.T*/tags.* → scoreboard.decisions.* → gdsp.cmd.* → struct.*`.
* Append a small legend listing Tag types + required fields.
* Note **per‑tick dynamic budgets** and **TTL decay** on the Scoreboard node.
* Mark **walkers = read‑only**; **GDSP = only writer**.

**Handoff (Physicist Mode implements):**

* Files/paths to create:

  * derivation/architecture/event\_sourced\_plasticity\_diagram.md
  * derivation/code/runtime/bus/scoreboard.py
  * derivation/code/runtime/walkers/{use\_tracker,complement\_tagger,boundary\_retraction,...}.py
  * derivation/code/runtime/gdsp\_actuator.py
* CLIs to run + seeds:

  * `python -m fum_rt.run --demo sp_event_pipeline --seeds 0,1,2 --log bus,scoreboard,gdsp`

**Verification (acceptance gates):**

* Median **tag→actuation latency ≤ 2 ticks** at nominal load; **no dense scans** observed.&#x20;
* **Backlog < 60% capacity** per territory; **drop rate \~0** (TTL expiries allowed).&#x20;
* **Degree floors by class** maintained after prune cycles; **false‑positive prune <1%** on replay.
* GDSP emits `struct.*` acks matching budgets; no direct writes from walkers.

**Assumptions/Risks:**

* Without Scoreboard, GDSP may oscillate; this addition fixes it.&#x20;
* Tag schema drift across walkers → enforce one canonical dataclass.
* Dynamic budgets must be bus‑driven (queue depth/HSI), not constants.&#x20;

**Next Steps:**

* Update the diagram with **Scoreboard + Tag legend + dynamic budgets**.
* Wire up minimal Scoreboard + one walker (`use_tracker`) end‑to‑end.
* Record `struct.*` acks to confirm **O(1) surgical writes**.
* Then add C3/microglia and boundary‑retraction walkers.

*(Also aligns with your legacy demo’s structural homeostasis separation-logic vs. actuation remained decoupled there too.)*&#x20;




You're right-those placeholder paths were wrong. Here’s the **correct wiring based on your docs/code** and a tight work order that stays inside your runtime/physics split.

```
Classification: Runtime-only
```

**Objective Recap**

* Fix “structural plasticity never called” by wiring walker→bus→scoreboard→GDSP through your **actual** modules/paths.

**Correct path mapping (yours)**

* **Bus / topics / events-bridge**

  * `core/bus.py`, `core/announce.py` (topics), runtime bridge: `runtime/events_adapter.py`. &#x20;
* **Scoreboard / aggregation**

  * `runtime/helpers/macro_board.py` (use as sparse, per‑territory scoreboard).&#x20;
* **Actuator (GDSP)**

  * `core/neuroplasticity/gdsp.py` (budgeted prune/grow/bridge/cull).&#x20;
* **Walkers (read‑only scouts)**

  * `core/cortex/void_walkers/*.py` (e.g., `void_excitation_scout.py`, `base.py`).&#x20;
* **Loop integration**

  * `runtime/loop/main.py` (+ `orchestrator.py`, `phase.py`).&#x20;
* **Existing tests/guards**

  * CI guard for walkers (no scans/dense): `tests/ci` in repo (see walker guard test), and UF unit: `tests/core/test_territory_uf.py`. &#x20;
* **Derivation (validation papers only)**

  * RD gates live in docs: `reaction_diffusion/rd_front_speed_validation.md`, `rd_dispersion_validation.md`.&#x20;

---

**Action Plan**

* Add **tag emission** in `core/cortex/void_walkers/base.py` and concrete scouts to publish `tag.*` events via `core/announce.py`; forward through `runtime/events_adapter.py` to scoreboard. &#x20;
* Implement **Scoreboard** (decaying votes, per‑territory) in `runtime/helpers/macro_board.py` (no scans; Welford stats per tag type).&#x20;
* Wire **GDSPActuator** calls in `runtime/loop/main.py`: per‑tick read scoreboard → call `core/neuroplasticity/gdsp.py` with budgets. **Assert** no dense path. &#x20;
* Use `phase.py` for **emergent budgets** (derive from bus backpressure/UF cohesion; no static caps).&#x20;
* Ensure **walkers stay read‑only** (existing CI guard passes). &#x20;
* Keep derivation **RD gates** as external acceptance checks (papers only).&#x20;

---

**Handoff (Physicist Mode implements)**

* Files/edits:

  * `core/cortex/void_walkers/base.py` + concrete scouts: emit `tag.prune_synapse`, `tag.grow_synapse`, `tag.bridge`, `tag.cull_neuron` via `announce.*`.&#x20;
  * `runtime/helpers/macro_board.py`: scoreboard (per‑territory TTL, EWMA mean/σ, μ+κ·σ gates).&#x20;
  * `runtime/events_adapter.py`: route bus→scoreboard batches.&#x20;
  * `runtime/loop/main.py`: per‑tick `scoreboard.flush()` → `GDSPActuator.apply_*()`; hard‑assert if any dense routine is invoked. &#x20;
  * `core/neuroplasticity/gdsp.py`: ensure budgeted `apply_{prune,grow,bridge,cull}` are territory‑scoped.&#x20;
* CLIs (example):

  * `python -m fum_rt.runtime.loop.main --ticks 10000 --seed 0` (A/B with `ENABLE_GDSP=0/1`).&#x20;

---

**Verification**

* **No‑Dense gate:** assert in `loop/main.py` when dense paths touched.&#x20;
* **Walker guard tests pass** (no scans/dense calls). &#x20;
* **UF repair:** fragmentation → `bridge` brings components→1 (see `test_territory_uf`).&#x20;
* **Physics invariants** remain green per derivation RD docs (front‑speed/dispersion papers).&#x20;

**Assumptions/Risks**

* Scoreboard fits in `macro_board.py`; if not, split to `runtime/helpers/scoreboard.py`.&#x20;
* Budgets must be **emergent** (from bus/UF/telemetry), not constants; ensure no hard caps in code paths.&#x20;

**Next Steps**

* Implement tag→scoreboard→GDSP path; add the assert.
* Run A/B `ENABLE_GDSP` and check UF/cohesion + sparsity metrics.
* If green, expand taggers (microglia/complement etc.) in walkers while CI guards stay green. &#x20;

If you want, I’ll adapt this into PR checklists against **these exact files** so your agent can push safely.
