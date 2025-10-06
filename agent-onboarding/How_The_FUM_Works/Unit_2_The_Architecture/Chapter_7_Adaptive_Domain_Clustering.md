***Unit 2 - Chapter 7***

# Active Domain Cartography

### The System's Cartographer

For the FUM to understand its own emergent internal structure, it needs a way to periodically map its functional territories. Active Domain Cartography is the system's internal "cartographer," a process that identifies groups of neurons (territories or domains) that have formed functional specializations.

This is a critical Global System utility for two reasons:
1.  **It enables the SIE:** The cluster IDs it generates serve as the discrete "State `S`" that the SIE's value function (`V(S_t)`) and novelty calculation (`N(S)`) depend on.
2.  **It targets GDSP:** The territories become the specific targets for Synaptic Actuator, allowing for precise, performance-driven structural changes.

---
***Section A.***

**A.1. Mechanism: A Multi-Faceted, FUM-Specific Approach**

*   **Integrated Method:** FUM does not use a generic, brute-force clustering metric like the silhouette score. Instead, it employs a combination of constraints and adaptive triggers that are deeply integrated with the system's core architecture, ensuring both efficiency and relevance.
*   **1. Constrained Search Space (Efficiency):** To avoid wasting computational resources searching for an optimal number of territories (`k`) across all possibilities, the system uses FUM-specific parameters, `k_min` and `max_k`, to define a narrow and sensible search space. This makes the process targeted and efficient from the outset.
*   **2. Adaptive Scheduling (Intelligence):** The system does not re-cluster on a fixed, arbitrary schedule. It uses an entropy-based formula (`t_cluster = 100000 * e^(-α * connectome_entropy)`) to decide when to perform this computationally significant task. This means the system intelligently re-territories more frequently during periods of high learning and structural change (high `connectome_entropy`) and less frequently when its internal connectome is stable and well-organized (low `connectome_entropy`).
*   **3. Reactive Adaptation (Performance-Driven):** The system has a built-in, event-driven mechanism to handle novel information that doesn't fit the current cluster structure. If a new input is poorly categorized (e.g., low similarity to all existing cluster centroids), FUM can react in one of two ways:
    *   **Holding Cluster:** It can dynamically create a temporary "holding cluster" to isolate the novel inputs and their associated rewards.
    *   **Bifurcation:** It can trigger an immediate re-clustering with an increased `k` to try and form a new, permanent home for the emergent domain.
*   **Conclusion:** This multi-faceted approach ensures that FUM's understanding of its own structure is always relevant, efficient, and responsive to the demands of its learning environment.

***End of Chapter 7***
