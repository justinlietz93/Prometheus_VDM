# Technical Summary Report

**Generated on:** August 24, 2025 at 11:12 PM CDT

---

## Generated Summary

### **Summary of Technical Specification: Event-Sourced Structural Plasticity**

This document outlines a comprehensive technical specification for a biologically-plausible structural plasticity framework designed for a runtime connectome. The system's core mandate is that all structural modifications—synapse formation, pruning, strengthening, decay, and neuron culling—must be achieved through a strictly sparse, event-driven, and computationally budgeted model. All operations are local, territory-scoped, and sub-quadratic, explicitly prohibiting dense matrix scans or global polling.

#### **1. Core Architecture: Event-Sourced Pipeline**
The framework operates on a unidirectional, decoupled pipeline ensuring scalability and adherence to the sparse-only constraint:
**Walker → Tag Event → Event Bus → Scoreboard → GDSP Actuator**

1.  **Walkers:** Lightweight, read-only agents that traverse local subgraphs, compute metrics (e.g., co-activity, metabolic load), and emit `Tag` events upon crossing thresholds. They do not modify the connectome.
2.  **Tag Events:** Atomic messages representing proposals for structural change (e.g., `tag.prune_synapse`, `tag.cull_neuron`), containing coordinates, a reason code, and a time-to-live (TTL).
3.  **Event Bus:** A message broker for O(1) transport of `Tag` events.
4.  **Scoreboard:** A stateful service that aggregates `Tag` events into decaying vote counts for each entity. It translates high-frequency, noisy signals into stable, thresholded decisions. The update rule per entity *x* each tick is:
    $S_x \leftarrow \gamma\,S_x \;+\; \sum_{e\in\text{tags}(x)} w_e$
    where `γ` is a decay factor (e.g., 0.95) and `w_e` are per-reason weights.
5.  **GDSP (Goal Directed Structural Plasticity) Actuator:** The sole component with write-access to the connectome. It acts only on IDs from the Scoreboard that cross thresholds (e.g., `θ_prune`, `θ_cull`), operating within strict per-tick budgets (`PRUNE_BUDGET`, `GROW_BUDGET`). All operations are surgical and Compressed Sparse Row (CSR)-safe.

---

#### **2. System Components and Data Structures**

*   **Heterogeneous Neuron Classes:** The system defines multiple neuron classes with distinct connectivity targets, plasticity rates, and population rarities. Key parameters are stored in on-device vectors.

| Class | Rarity | Target Degree (`k_target`) | Learning Rate (`η`) | Decay Rate (`λ`) |
| :--- | :--- | :--- | :--- | :--- |
| **Relay** | ~60% | 3-5 | 0.08 | 0.03 |
| **Inhibitory**| ~25% | 6-12 | 0.05 | 0.02 |
| **Integrator** | ~14% | 20-60 | 0.01 | 0.005 |
| **Purkinje-like**| ~1% | 200-500| 0.002 | 0.0005 |

*   **Safety Rails & Dynamic Targets:**
    *   **Target Degree (`k_target`)** is a dynamic target, not fixed, but bounded by a capacity cap to prevent pathological behavior in small territories:
        $k_{\max}^{\text{cap}}(i,T)=\min\{\;k_{\max}(\text{class}_i),\;\alpha|T|,\;k_{\text{HW}}\;\}$.
    *   **Rarity caps** are enforced per-territory to prevent local over-concentration of rare neuron types (e.g., Purkinje-like ≤0.5% per territory).
    *   **Quorum for Culling:** Neuron culling requires a quorum of at least two distinct reason codes (e.g., `EXCITOTOX` + `METABOLIC_DEBT`) or one sustained reason code to trigger.

---

#### **3. Plasticity Mechanisms: From Biology to Runtime**

*   **Foundational Synaptic Dynamics:** A continuous, activity-dependent update rule implements Hebbian reinforcement and passive decay. For each active synapse `(i, j)`:
    $$
    w_{ij}(t+1) \leftarrow \operatorname{clip}\Big((1-\lambda_{ij}) \cdot w_{ij}(t) + \eta_{ij} \cdot e_{ij}(t) \cdot M_t, \; [w_{\min}, w_{\max}]\Big)
    $$
    *   `e_ij`: Eligibility trace (EMA of pre/post co-activity).
    *   `M_t`: Global or territory-local modulatory factor (e.g., TD-error, salience).
    *   `η_ij`, `λ_ij`: Per-edge rates derived on-the-fly from the pre- and post-synaptic neuron classes.

*   **Biologically-Analogous Walkers and Triggers:** Specific walkers translate physiological and pathological conditions into actionable `Tag` events.

| Biological Process | Walker Type | Local Metric(s) | Action (Emitted Tag) |
| :--- | :--- | :--- | :--- |
| **Use-it-or-Lose-it** | `UseTracker` | Low synaptic co-activity (`use_score`) for duration `T_idle`. | `tag.prune_synapse` |
| **Microglia Engulfment** | `ComplementTagger` & `Microglia` | High weight volatility + low efficacy. | Two-stage: `tag.C3` followed by `tag.prune_synapse` upon quorum. |
| **Axonal Retraction** | `BoundaryRetraction` | Axon projecting against territory gradient & `deg_out > k_target`. | `tag.retract_axonal_branch` |
| **Excitotoxicity** | `ExcitotoxicitySentinel` | Sustained high firing rate (`r_i`) & high integrated potential (`c_i`, a calcium proxy). | `tag.cull_neuron` (reason: `excitotox`) |
| **Metabolic Homeostasis** | `MetabolicAuditor` | Sustained territory `metabolic_debt` (`work - supply > θ_debt`). | `tag.prune_synapse` (on high-cost edges), then `tag.cull_neuron`. |
| **Apoptosis** | `ApoptosisSentinel` | Integrated danger score (`D_i`) from multiple pathological flags exceeds `θ_apop`. | `tag.cull_neuron` (reason: `apoptosis`), performed gracefully over several ticks. |

*   **Terminology Lock:** The runtime signal `metabolic_debt` is explicitly distinct from the high-level objective signal `sie.void_debt`. They operate on separate bus topics and serve different purposes (runtime homeostasis vs. global system objective).

*   **System-Initiated Modifications:**
    *   **Connectome Repair:** Triggered when a territory's Union-Find (UF) structure reports fragmentation (components > 1). The actuator performs budgeted bridging by alias-sampling boundary nodes to create new edges.
    *   **Controlled Remediation (Trauma):** An external `trauma.begin` event can mark a specific territory and time window. Within this window, prune/cull tag weights and budgets are elevated to accelerate cleanup of a compromised region without affecting the rest of the network.

---

#### **4. High-Level Design Philosophy and Verification**
The document contrasts the FUM's architecture with that of Large Language Models (LLMs), highlighting a fundamental philosophical difference:
*   **FUM:** A dynamic, self-modifying organism built on local emergence, heterogeneous specialization (neuron classes, functional organs), and efficient, event-driven writes. Intelligence is an emergent property of interacting, specialized parts.
*   **LLMs:** Static, frozen artifacts built on global optimization (backpropagation), homogeneous scale (trillions of identical transformer blocks), and brute-force statistical learning.

**Key Verification Gates (Acceptance Criteria):**
*   **No-Dense Gate:** The system must trigger a hard assertion failure if any dense homeostasis path is invoked without the `FORCE_DENSE=1` flag.
*   **Budget Gate:** The total number of modified edges per tick must remain strictly within the sum of configured budgets (`PRUNE_BUDGET`, `BRIDGE_BUDGET`, etc.).
*   **Class/Degree Gate:** After long runs, neuron class distributions must respect rarity constraints, and median degrees must fall within their specified `k_target` bands.
*   **Functional Gates:** Specific tests must verify use-it-or-lose-it pruning, synaptic strengthening on stimulated pathways, metabolic debt reduction, targeted trauma response, and timely fragmentation repair.

## Key Highlights

* The system's architecture is a strictly sparse, event-driven pipeline (Walker → Tag → Scoreboard → Actuator) where read-only agents propose changes and a single, budgeted component executes them.
* A 'Scoreboard' component aggregates noisy, high-frequency 'Tag' events into stable, actionable decisions using a decaying vote mechanism, translating proposals into policy.
* The connectome is composed of heterogeneous neuron classes, each with distinct, enforced properties like connectivity targets, learning rates, and population rarity.
* Biological processes like 'Use-it-or-Lose-it', excitotoxicity, and metabolic homeostasis are directly modeled as specific computational agents ('Walkers') that trigger structural changes.
* Strict safety rails are enforced, including dynamic connectivity targets, rarity caps for neuron classes per-territory, and quorum requirements for neuron culling to prevent pathological behavior.
* All structural modifications (pruning, growth) are governed by strict, per-tick computational budgets, a core constraint of the design.
* The system features goal-directed repair mechanisms, such as automatically bridging fragmented network sections and accelerating cleanup in externally designated 'trauma' zones.
* The design philosophy is explicitly contrasted with LLMs, focusing on a dynamic, self-modifying organism built on local emergence rather than a static, globally optimized artifact.

## Next Steps & Suggestions

* Create an implementation plan by breaking down the event-sourced pipeline components (Walker, Scoreboard, Actuator) into specific engineering tasks.
* Define the precise data schemas for `Tag Events` and the API contract between the Scoreboard and the GDSP Actuator.
* Develop a simulation to validate the Scoreboard's decay logic and determine optimal threshold values (`θ_prune`, `θ_cull`).
* Schedule a technical review to finalize the neuron class parameters (e.g., Target Degree, Decay Rate) and system budgets.

---

*Powered by AI Content Suite & Gemini*
