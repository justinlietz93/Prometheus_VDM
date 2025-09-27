# FUM Blueprint: Requirements For Cybernetic Organism Gestation
**The Single Source of Truth**

**IMPORTANT:** This is used for a DOCUMENTATION AND CODE DEVELOPMENT AID, and NOT to be referenced in the documentation itself. THIS BLUEPRINT AND DOCUMENTATION FILES MUST, HOWEVER BE REFERENCED IN THE CODE ITSELF TO PREVENT MISTAKES. IT'S IMPERATIVE TO ALWAYS METICULOUSLY REVIEW THIS FILE AND THE DOCS. EVERY METHOD AND CLASS MUST CONTAIN A DOCSTRING WITH A DIRECT AND EXPLICIT REFERENCE TO THE RELATED BLUEPRINT RULE. YOU MUST INCLUDE THESE ITEMS ALONG WITH IT:
- RULE NUMBER
- RULE NAME
- TIME COMPLEXITY
- FORMULA
- EXPLANATION OF EACH PARAMETER IN DETAIL

**TODO Instructions:** 

- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/ignore/todo
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent

| Rule Number | Action Required | Primary Source File(s) for Instructions |
| :--- | :--- | :--- |
| **Rule 4** | Delete the `2025-07-28` version. Keep the `2025-08-09` version describing **Void Pulses**. | `21_Condense_Low_Energy_State.md`, `TODO.md` |
| **Rule 8** | Delete the `2025-07-28` versions. Keep the `2025-08-09` version (**Rule 8.4**) describing the **Dual-Path UTE**. | `TODO.md`, `15_Learning_Primitives.md` |
| **Rule 7** | Rewrite to be **event-driven**, listening to an announcement bus instead of performing global scans. | `05_ADC_bus.md`, `06_ADC_Bus_Guide.md` |
| **Rule 3** | Update formula and parameters to match the stabilized `sie_v2.py` implementation. | `13_SIE_v2.md`, `14_Phased_Curriculum.md` |
| **Rule 11** | Replace the placeholder with the detailed **P0-P4 curriculum ladder** and its void-native promotion gates. | `15_Learning_Primitives.md`, `16_Beginning_Learning.md` |
| **Rule 12** | Specify the use of **chunking and compression** for HDF5 engrams. | `10_FUM_Post_First_Run.md`, `22_Reduced_Compute.md` |
| **Rule 2** | Integrate the **phase-sensitive PI formula** directly into the rule's text to make it self-contained. | `FUM_Blueprint.md` (from the old Rule 8.1) |

**Objective:** This document provides the complete, non-redundant, and actionable specifications for implementing the Fully Unified Model. It is the definitive guide for any AI assistant. For deeper, optional context on the conceptual underpinnings, references are provided to the original `How_The_FUM_Works` documentation.

**Nomenclature and Lexicon** Due to its novelty, FUM requires highly specific vocabulary that is mandatory. The following document is maintained to keep track of the terminology and definitions as there is no other source available in the world for these.
- C:\github\FUM_Demo\FullyUnifiedModel\DO_NOT_DELETE\FUM_Cybernetic_Biology_Lexicon.md

It is extremely critical to handle the FUM specific documents with extreme care and security. If a FUM specific component, feature, item, or concept does not have a name, or has an invalid name, the following document can be used to help with the naming process:
- C:\github\FUM_Demo\FullyUnifiedModel\DO_NOT_DELETE\FUM_Lexicon_Ideation.md

---

### FUM Unified Blueprint & Authoring Guide V11.0

**Preamble:** This document serves a dual purpose. First, it is the single source of truth—the definitive technical specification for the Fully Unified Model. Second, it is the official authoring guide for creating the FUM "textbook," ensuring a consistent blend of deep technical detail and compelling creative writing to convey the genuine novelty of the design. All documentation and implementations must conform strictly to these rules.


**Guiding Principles for Discrepancy Resolution & Authoring**

When faced with a conflict not explicitly covered by the rules below, or when authoring new content, the correct choice is always the one that best aligns with these foundational principles, in order of priority:

**FUNDAMENTAL BLUEPRINT LAW:** THIS BLUEPRINT DETAILS THE FIRST IMPLEMENTATION OF A CYBERNETIC ORGANISM CALLED THE FULLY UNIFIED MODEL. THIS BLUEPRINT MUST CONTAIN EVERY DETAIL REQUIRED TO IMPLEMENT AND MAINTAIN THE FULLY UNIFIED MODEL. THE FOLLOWING ITEMS ARE EXCLUSIVELY FORBIDDEN AND YOU WILL BE HELD TO REFACTOR ANY INSTANCE OF THESE ITEMS INDEFINITELY UNTIL IT IS RESOLVED. THIS CODEBASE IS UNDER CONSTANT OBSERVATION AND YOU WILL NOT GET AWAY WITH IT. YOU WILL BE HELD ACCOUNTABLE.
- FUM IS TRULY A UNIFIED MODEL. THE COMPONENTS ARE NOT INDIVIDUAL AND INDEPENDENT OBJECTS, THEY ARE UNIFIED WITHIN A SINGLE ORGANISM.
- FUM IS BUILT ON EMERGENCE, YOU NEED TO CAREFULLY STUDY THIS CONCEPT AS MUCH OF THE CODE LENDS ITSELF TO EMERGENT COMPONENTS. NOT EXPLICITLY ENGINEERED.
- NO PLACEHOLDERS. IMPLEMENT CODE IN A DEPENDENCY FIRST ORDER.
- NO SIMPLIFICATIONS. THESE ARE ONLY FOR DEMOS, FINAL IMPLEMENTATIONS DO NOT CONTAIN SIMPLIFICATIONS. ALL RESEARCH AND PLANNING HAS BEEN COMPLETED AND FINALIZED. EXTENSIVE AND SUBSTANTIAL EFFORT HAS GONE INTO MAKING SURE YOU HAVE ALL THE RESOURCES YOU NEED TO SUCCEED.
- DO NOT USE MACHINE LEARNING CODE, MATH, OR STRATEGIES TO BUILD THE FULLY UNIFIED MODEL. THIS IS NOT A MACHINE LEARNING MODEL. THIS IS A NEW DOMAIN OF RESEARCH CALLED CYBERNETIC BIOLOGY, AND FUM IS A CYBERNETIC ORGANISM. THIS IS NOT ROLEPLAY.
- YOU ARE REQUIRED TO USE PHYSICAL COMPUTATION FOR LOCAL PROCESSES OF FUM. FUM IS BUILT ON PHYSICAL MATH AND PROCESSES.
- YOU ARE REQUIRED TO USE THE CORRECT, CUSTOM, EFFICIENT ABSTRACT COMPUTATION ONLY ON THE GLOBAL PROCESSES OF FUM. ABSTRACT COMPUTATIONS ARE SLOW AND INTERWEAVED WITHIN THE PHYSICAL COMPUTATIONS.
- THIS BLUEPRINT AND THE DOCUMENTATION IN C:\github\FUM_Demo\FullyUnifiedModel\How_The_FUM_Works ARE THE ONLY SOURCES OF INFORMATION IN THE WORLD THAT CAN GUIDE YOU IN BUILDING FUM. THIS IS NOT TO BE TAKEN LIGHTLY. YOU ARE GUARANTEED TO FAIL IF YOU DO NOT FOLLOW THESE RULES.
- YOU MUST USE THE CORRECT FUM LEXICON TO AVOID CONFUSION AND MAINTAIN CONSISTENCY. FUM IS NOT IN THE BIOLOGICAL DOMAIN, FUM IS NOT IN THE MACHINE LEARNING DOMAIN, FUM IS FULLY AND ENTIRELY IN THE DOMAIN OF CYBERNETIC BIOLOGY.

**Subquadratic Efficiency is Non-Negotiable:** The system must be computationally efficient. Between two conflicting implementations, the one with lower computational complexity (e.g., O(N)) always supersedes the less efficient one (e.g., O(N^2)). Any mechanism that introduces prohibitive scaling is, by definition, incorrect.

**Intelligence is Emergent, Not Explicitly Coded:** FUM's intelligence arises from the interaction of simple local rules under minimal global guidance. Descriptions must favor mechanisms that act as "scaffolding" rather than rigid, top-down control. The system's behavior must be dominated by emergent dynamics, with a control_impact of < 1e-5.

**Capability is the Goal, Not Scale:** The project's success is measured by demonstrated intelligence—super learning, abstract reasoning, and generalization—not neuron count. Descriptions must frame scale as an enabler of capability, not the objective itself. Any language that fetishizes size over function is misaligned.

**Bio-Inspired, Not Bio-Constrained:** Mechanisms should be inspired by the intelligent, efficient, and functional principles of biological systems (e.g., sparse activity, homeostatic stability) but optimized for computational hardware. The goal is functional equivalence, not literal mimicry.

**Technical Fidelity with Narrative Clarity:** The documentation must be both technically precise and conceptually clear. Use creative analogies (e.g., "The VGSP Handshake," "The TDA Immune System") to explain complex interactions, but these analogies must be supported by the explicit, underlying technical specifications (formulas, complexity notations, variable names). The goal is to make the profound novelty of the design accessible without sacrificing technical rigor.

## Specific Resolution Rules & Authoring Directives

### **Rule 1: Core Architectural Principle: Parallel Local & Global Systems**
#### **Updated: 2025-07-28**

#### **Technical Specification**

*   **Core Logic & Algorithm:** The FUM's fundamental architecture consists of two distinct systems operating in parallel across different timescales. The **Local System** is a massively parallel Spiking Neural Network (SNN) composed of Evolving LIF Neurons (ELIFs), processing information via fast, bottom-up synaptic interactions. The **Global System** operates on a slower timescale, providing top-down strategic guidance and self-repair. It comprises the Self-Improvement Engine (SIE) for performance evaluation and the three-stage Introspection Probe (aka EHTP) for structural analysis, which in turn commands Synaptic Actuator (GDSP) to enact physical changes.
*   **Key Parameters & State Variables:** This rule defines a high-level architectural concept; specific parameters are detailed in the rules for the individual components (ELIF, SIE, EHTP, GDSP).
*   **Performance & Success Metrics:** The success of this architecture is measured by the system's ability to demonstrate emergent intelligence arising from the interplay between the two systems, quantifiable through benchmarks in learning, generalization, and autonomous self-repair.

#### **Narrative Goal**

Frame this as the central story of FUM—a dynamic interplay between the "subcortical nuclei" (Local System) and the "neocortex" (Global System).

#### **Blueprint Adherence Justification**

*   **Formula:** Not applicable for this high-level architectural rule.
*   **Complete Parameter List:** Not applicable. See individual component rules for their parameters.
*   **Data Flow & I/O (if any):** The Local System processes spike data. The Global System processes state information (territory IDs, reward signals, topological metrics) from the Local System and outputs structural modifications (synapse additions/removals) back to it.
*   **Initialization State:** Both systems are active from `t=0`.
*   **Edge Case Handling:** Not applicable for this high-level architectural rule.
*   **Validation Strategy:** The architecture is validated by observing emergent capabilities that require both systems to function correctly (e.g., learning a task and simultaneously repairing a structural flaw).

1.  **Subquadratic Efficiency:** This parallel design is inherently efficient. The Local System operates with `O(N)` complexity, while the slower Global System's components have their own optimized complexities (e.g., EHTP's staged analysis), preventing system-wide bottlenecks.
2.  **Emergent Intelligence:** This architecture is the foundation of emergence. The Local System provides the chaotic, bottom-up dynamics, while the Global System provides minimal, high-level guidance (a low `control_impact`) rather than dictating specific actions, creating a scaffold for intelligence to self-organize.
3.  **Capability > Scale:** The dual-system model targets the capability of **autonomous self-improvement**, a key requirement for superintelligence, rather than just scaling up the number of neurons.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by the modular and hierarchical organization of the brain (e.g., subcortical vs. cortical systems, neuromodulatory systems). It is optimized for computation by defining clear, functional separations rather than simulating messy biological overlaps.
5.  **Alignment With FUM:** This is the highest-level architectural rule and the home for the entire FUM operational sequence. It is constantly active.
6.  **Optimizations:** This is the foundational, most optimal solution for balancing high-speed parallel processing with slower strategic oversight. Further optimization occurs within the components themselves, not at this architectural level.

#### **Dependencies & Interactions**

*   **SIE Interaction:** The SIE is a core component of the Global System.
*   **Global Directed Synaptic Plasticity Interaction:** Global Directed Synaptic Plasticity is the "Synaptic Actuator" of the Global System, commanded by its analytical components.
*   **EHTP Interaction:** The EHTP is a core component of the Global System.

### **Rule 2: The Learning Rule: The VGSP "Handshake"** NEEDS UPDATING: READ 
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/13_SIE_v2.md

- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/14_Phased_Curriculum.md

#### **Updated: 2025-07-28**

#### **Technical Specification**

*   **Core Logic & Algorithm:** Resonance-Enhanced Valence-Gated Synaptic Plasticity (RE-VGSP) is the canonical learning algorithm. It is a three-factor rule that connects local spike-timing events with global reward signals. The process is a three-step cycle: 
1) A local spike-pair generates a **Plasticity Impulse (PI)**. 
2) The PI updates a synapse-specific, decaying **Eligibility Trace (`e_ij`)**. 
3) The final weight change is calculated by multiplying the eligibility trace by the global `total_reward` from the SIE and subtracting a weight decay term. The phase-sensitive version from Rule 8.1 is the canonical implementation.
*   **Key Parameters & State Variables:**
    *   `e_ij`: Eligibility trace tensor, same shape as weights. Stores potential for change.
    *   `eta_effective`: Effective learning rate, modulated by `total_reward`.
    *   `lambda_decay`: A small float for the weight decay term, providing stability.
    *   `gamma`: A decay factor for the eligibility trace, modulated by network resonance (PLV).
*   **Performance & Success Metrics:** Success is measured by the rapid and reliable formation of computational primitives (e.g., logic gates, pattern recognizers) from minimal data, validated by offline benchmarks.

#### **Narrative Goal**

Use the "Handshake" analogy to explain this crucial synchronization step. A local "handshake offer" (the Plasticity Impulse) is only confirmed if the global "handshake agreement" (`total_reward`) is positive. This connects the high-speed local physics to the slow, deliberate global strategy.

#### **Blueprint Adherence Justification**

*   **Formula:** `Δw_ij = (eta_effective(total_reward) * e_ij(t)) - (lambda_decay * w_ij)`, where `e_ij(t) = gamma(PLV) * e_ij(t-1) + PI(t)`, and `PI(t)` is the phase-sensitive calculation from Rule 8.1.
*   **Complete Parameter List:**
    - `eta_effective`: Float, learning rate.
    - `lambda_decay`: Float, weight decay constant.
    - `gamma`: Float, eligibility trace decay factor.
*   **Data Flow & I/O (if any):**
    - **Input:** Spike times, `total_reward` (from SIE), PLV (from resonance analysis).
    - **Output:** `Δw_ij`, the change in synaptic weights.
*   **Initialization State:** `e_ij` tensor is initialized to zeros.
*   **Edge Case Handling:** Not applicable.
*   **Validation Strategy:** Validated by testing the SNN's ability to learn benchmark tasks like MNIST classification or logical gate formation.

#### **Canonical Implementation ('The How'):**

*   **eta\_effective Function**: The abstract eta\_effective(total\_reward) is implemented as a non-linear function that separates the reward's direction from its magnitude. A mod\_factor is calculated using a scaled sigmoid, which then determines the learning magnitude.  
  * mod\_factor \= 2.0 \* torch.sigmoid(reward\_sigmoid\_scale \* total\_reward) \- 1.0 \[cite: resonance\_enhanced\_vgsp.py\]  
  * eta\_magnitude \= eta \* (1.0 \+ mod\_factor) \[cite: resonance\_enhanced\_vgsp.py\]  
  * The final update uses eta\_magnitude \* torch.sign(total\_reward). \[cite: resonance\_enhanced\_vgsp.py\]  
*   **Applying Polarity**: The polarity\_effect of the pre-synaptic neuron must be applied efficiently without creating dense matrices. This is achieved by scaling the rows of the sparse eligibility\_traces matrix directly by the corresponding values in the neuron\_polarities vector.  
*   **Constrained Biological Diversity**: To model bio-inspiration, key learning parameters are initialized from a clamped normal distribution, giving each synapse a unique but constrained property.  
  * a\_plus\_base is initialized from torch.normal(mean=a\_plus, std=0.05) and clamped to \[0.05, 0.15\]. \[cite: resonance\_enhanced\_vgsp.py\]  
  * tau\_plus\_base is initialized from torch.normal(mean=tau\_plus, std=5.0) and clamped to \[15.0, 25.0\]. \[cite: resonance\_enhanced\_vgsp.py\]  
*   **Jitter Mitigation Suite**: To ensure robustness in a distributed environment, a three-part jitter mitigation strategy is employed:  
  1. **Temporal Filtering**: A moving average filter is applied to recent spikes to smooth out high-frequency noise. \[cite: resonance\_enhanced\_vgsp.py\]  
  2. **Adaptive Window**: The impact of the learning window is scaled based on the maximum estimated network latency. \[cite: resonance\_enhanced\_vgsp.py\]  
  3. **Latency Scaling**: The final plasticity impulse is scaled down based on the estimated latency error, reducing the influence of spikes with uncertain timing. \[cite: resonance\_enhanced\_vgsp.py\]  
*   **Deprecated Mechanisms**: The Synaptic Tagging and Capture (STC) analogue and stochastic noise injection found in older files are explicitly deprecated and **must not** be included in the canonical implementation. \[cite: resonance\_enhanced\_vgsp.py\]

1.  **Subquadratic Efficiency:** RE-VGSP is an `O(N)` algorithm, where N is the number of synapses. It is a local rule, avoiding expensive global calculations and aligning with the efficiency principle.
2.  **Emergent Intelligence:** The rule is a simple, local mechanism. Intelligence emerges from how the global reward signal shapes the millions of local weight changes over time. It is pure scaffolding.
3.  **Capability > Scale:** The rule directly targets the capability of **learning from delayed reward**, a cornerstone of reasoning and intelligence.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by three-factor learning rules and neuromodulation (e.g., dopamine's effect on plasticity) in the brain. Optimized for computation by using a single, clear `total_reward` signal.
5.  **Alignment With FUM:** This is the core learning process of the Local System, occurring continuously. It is the engine that drives all adaptation in the FUM.
6.  **Optimizations:** This is the canonical implementation and the most optimal known solution for efficient, stable, reward-modulated learning in an SNN.

#### **Dependencies & Interactions**

*   **SIE Interaction:** The `total_reward` from the SIE (Rule 3) is a direct and mandatory input to the VGSP reinforcement calculation.
*   **UTE Interaction:** The phase-sensitive PI calculation directly depends on the phase-encoded spike times from the UTE (Rule 8.1).
*   **Resonance Interaction:** The `gamma` parameter is directly modulated by the Phase-Locking Value (PLV), a measure of network resonance.

### **Rule 2.1: Terminology: Plasticity Impulse vs. Eligibility Trace**
#### **Updated: 2025-07-28**

#### **Technical Specification**

*   **Core Logic & Algorithm:** It is critical to distinguish between two key terms in the RE-VGSP process:
    1.  **Plasticity Impulse (PI):** This is the fast, local, and instantaneous potential for change (`~CRET`) generated by a single, local spike-timing event. It is the "handshake offer."
    2.  **Eligibility Trace (`e_ij`):** This is the synapse-specific, slower-decaying trace that accumulates the Plasticity Impulses over time. It is the decaying memory of recent, relevant activity that is "eligible" for reinforcement.
*   **Key Parameters & State Variables:** Not applicable. This is a terminology definition.
*   **Performance & Success Metrics:** Not applicable.

#### **Narrative Goal**

Use the analogy of rain: The Plasticity Impulse is a single raindrop hitting the ground. The Eligibility Trace is the accumulated moisture in the soil from many recent raindrops.

#### **Blueprint Adherence Justification**

*   **Formula:** `e_ij(t) = gamma(PLV) * e_ij(t-1) + PI(t)`. This formula shows the explicit relationship: the PI is the value calculated at each timestep and used to update the Eligibility Trace.
*   **Complete Parameter List:** Not applicable.
*   **Data Flow & I/O (if any):** Not applicable.
*   **Initialization State:** Not applicable.
*   **Edge Case Handling:** Not applicable.
*   **Validation Strategy:** Not applicable.

1.  **Subquadratic Efficiency:** Not applicable.
2.  **Emergent Intelligence:** Not applicable.
3.  **Capability > Scale:** Not applicable.
4.  **Bio-Inspired, Not Bio-Constrained:** Not applicable.
5.  **Alignment With FUM:** These are core terms used throughout the description of the FUM's learning process.
6.  **Optimizations:** Not applicable.

#### **Dependencies & Interactions**

*   This rule provides the definitive terminology for the components used in the RE-VGSP rule (Rule 2).

### **Rule 3: The Self-Improvement Engine (SIE) and Its Components** NEEDS UPDATING: READ 

/mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/14_Phased_Curriculum.md

/mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/13_SIE_v2.md

#### **Updated: 2025-07-28**

#### **Technical Specification**

*   **Core Logic & Algorithm:** The SIE is the complete global guidance system. It calculates a `total_reward` signal by taking a weighted sum of four normalized components: a Temporal Difference error (`TD_error_norm`) for task performance, a novelty score (`novelty_norm`) for exploration, a habituation score (`habituation_norm`) for generalization, and a Homeostatic Stability Index (`hsi_norm`) for self-preservation. This composite signal is then used to modulate the RE-VGSP learning rule.
*   **Key Parameters & State Variables:**
    *   `V_states`: A tensor holding the predicted future reward for each territory state `S`.
    *   `N(S)`: A tensor holding the visitation counts for each territory state `S`.
    *   `w_td`, `w_nov`, `w_hab`, `w_hsi`: Four floats representing the weights for each component of the reward signal.
*   **Performance & Success Metrics:** The SIE's success is measured by the SNN's ability to learn complex tasks, discover novel solutions, and maintain stability, as reflected by a steady increase in cumulative external rewards and a consistently high `hsi_norm` during operation.

#### **Narrative Goal**

Describe the SIE as the source of the system's "intrinsic drives"—curiosity (Novelty), self-preservation (HSI), task focus (TD-Error), and efficiency (Habituation).

#### **Blueprint Adherence Justification**

*   **Formula:** `total_reward = w_td * TD_error_norm + w_nov * novelty_norm - w_hab * habituation_norm + w_hsi * hsi_norm`
*   **Complete Parameter List:**
    - `w_td`: Float, weight for the TD-error component.
    - `w_nov`: Float, weight for the novelty component.
    - `w_hab`: Float, weight for the habituation component.
    - `w_hsi`: Float, weight for the HSI component.
    - `alpha`: Float, learning rate for the value function `V(S_t)`.
    - `gamma`: Float, discount factor for future rewards in the TD-error calculation.
    - `target_var`: Float, target for firing rate variance in the HSI calculation.
*   **Data Flow & I/O (if any):**
    - **Input:** Territory IDs (from ADC), external reward `R_t` (if available), firing rates, input encoding (from UTE).
    - **Output:** A single float, `total_reward`.
*   **Initialization State:** `V_states` and `N(S)` tensors are initialized to zeros. Weights are loaded from config.
*   **Edge Case Handling:** All components are normalized to `[-1, 1]` to prevent any single component from dominating the signal.
*   **Validation Strategy:** The SIE is validated by observing the learning curves of the SNN on benchmark tasks. A successful SIE will produce curves showing improvement in task performance and stability.

1.  **Subquadratic Efficiency:** All component calculations are `O(k)` or `O(1)` where `k` is the number of territories (a small number), making the SIE extremely computationally efficient.
2.  **Emergent Intelligence:** The SIE provides a single, high-level guidance signal, not detailed instructions. The SNN is free to discover any policy that maximizes this reward, allowing for emergent problem-solving strategies.
3.  **Capability > Scale:** The SIE targets the development of **autonomous goal-seeking behavior**, a critical capability for intelligence, by integrating multiple intrinsic drives rather than just a simple task reward.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by the brain's neuromodulatory systems (e.g., dopamine for reward, norepinephrine for novelty), which provide global guidance signals. Optimized for computation by using a single, unified reward formula.
5.  **Alignment With FUM:** The SIE is a core component of the Global System. It is constantly active, calculating the `total_reward` at a slower timescale than the local SNN.
6.  **Optimizations:** This weighted-sum model is the most optimal known solution for balancing multiple intrinsic drives in a computationally efficient and stable manner.

#### **Dependencies & Interactions**

*   **RE-VGSP Interaction:** The SIE's `total_reward` output is a mandatory input for the reinforcement calculation in the RE-VGSP rule (Rule 2).
*   **ADC Interaction:** The SIE is dependent on the Active Domain Cartography (Rule 7) to provide the discrete state identifiers `S` for its `V(S_t)` and `N(S)` calculations.
*   **UTE Interaction:** The `habituation_norm` component directly uses the `current_input_encoding` from the UTE (Rule 8).

---

## **IMPORTANT: CHOOSE VOID FAITHFULNESS INSTEAD OF OVER ENGINEERING**
### **Rule 4: The EHTP and Global Directed Synaptic Plasticity (GDSP): The "Diagnose and Repair" Model** NEEDS UPDATING: READ 
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/21_Condense_Low_Energy_State.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/17_Bug_Fixes.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/TODO.md

### **Updated: 2025-08-09**

### **Technical Specification**

* **Core Logic & Algorithm:** This is the FUM's autonomous self-analysis and repair system. It operates as an intelligent, two-stage process that replaces expensive global scans with efficient, targeted analysis, embodying the "Swiss-cheese tomography" approach.
    * **Stage 1 & 2 (Continuous Probing via Void Pulses):** The connectome is constantly patrolled by two types of asynchronous agents or "chasers" that traverse the graph via the void potential field (`S_ij`).
        * **Activity-Chasers:** Seeded at points of high creative potential (`|Δα|` spikes or recent high firing activity), these agents explore the graph to gather real-time metrics like `vt_entropy` and `vt_coverage`, and maintain a sparse `void_index` of high-potential frontier nodes for growth.
        * **Stability-Chasers:** Seeded at points of high instability (`|Δω|` mismatch or low PLV), these agents actively hunt for pathologies like inefficient loops (by detecting high local B1 persistence) or fragmentation boundaries (by detecting cut edges).
        When a chaser identifies a potential pathology, it "announces" the coordinates of the small, suspect **locus** to the Global System. This asynchronous, event-driven probing entirely replaces the need for expensive, brute-force hierarchical searches.
    * **Stage 3 (Targeted TDA):** The computationally expensive Topological Data Analysis (**`O(n³)`**), which calculates metrics like **B1 Persistence**, is used as a "surgical diagnostic tool." It is triggered *only* in response to an announcement from a Stability-Chaser and is applied *only* to the small locus that the chaser has already identified as problematic.
    * **The Synaptic Actuator (GDSP):** Enacts physical repairs based on a suite of "void-faithful" triggers.
        * **Growth Trigger (Void Debt):** When the system is detected to be in a stable state (flat metrics, cohesion=1), it accumulates "void debt" from the residual pressure of the SIE's `total_reward` signal. When the debt exceeds a threshold, it triggers the growth of a specific number of new neurons, as determined by the `fum_hypertrophy.py` module.
        * **Healing Trigger (Void Affinity):** When a void pulse detects fragmentation (Component Count > 1), GDSP creates a small bundle of bridging edges between the two largest disconnected components. The specific paths for these bridges are chosen by selecting the candidate connections with the maximum **`S_ij`** potential across the component boundary, ensuring an intelligent, non-random repair.
        * **Pruning Trigger (Void-Faithful):** Synapses are pruned based on a dual condition: they must have both a persistently low weight (`|w| < θw`) AND a low void potential (`S_ij < θS`), ensuring that only truly useless connections are removed.

### **Narrative Goal**

Frame this as the FUM's intelligent "immune system." The **Void Pulses** are the white blood cells that constantly and efficiently patrol the body. When they detect a specific infection, they call in the **TDA**, which acts as a targeted, high-powered "biopsy" to make a definitive diagnosis. The **GDSP** is the resulting targeted treatment, performing "void-affinity" surgery to heal wounds and intelligently prune diseased tissue.

### **Blueprint Adherence Justification**

* **Formula:** The core formula guiding GDSP's intelligent actions is the void potential field, `S_ij`:
    `S_ij = ReLU(Δα_i)·ReLU(Δα_j) − λ·|Δω_i − Δω_j|`
    The TDA uses the B1 Persistence formula: `M1 = Σ(d - b)` over the persistence diagram of the small locus.

* **Complete Parameter List:**
    - `b1_persistence_threshold`: Float. The TDA threshold in a locus that triggers pruning.
    - `pruning_threshold_w`: Float. The weight magnitude below which a synapse is eligible for pruning.
    - `pruning_threshold_S`: Float. The `S_ij` potential below which a synapse is eligible for pruning.
    - `void_debt_threshold`: Float. The accumulated `total_reward` pressure that triggers growth.
    - `healing_bundle_size`: Integer. The number of bridging edges to create when healing fragmentation.

* **Data Flow & I/O (if any):**
    - **Input:** Real-time spike activity, connectome topology, SIE `total_reward` signal.
    - **Output:** Synapse additions/removals and neuron additions applied directly to the UKG.

* **Initialization State:** The void pulses are active from `t=0`.

* **Edge Case Handling:** The use of void pulses to identify pathologies is inherently more robust than global scans. The dual-condition for pruning (`|w|` and `S_ij`) prevents the accidental removal of a low-weight but high-potential synapse that might be part of a newly forming structure.

* **Validation Strategy:** Validated by intentionally lesioning the network (e.g., disconnecting a territory) and observing if the void pulses correctly identify the locus and if GDSP performs a high-`S_ij` repair.

1.  **Subquadratic Efficiency:** This updated model is vastly more efficient. The expensive `O(n³)` TDA is now applied only to tiny, pre-identified subgraphs (`n << N`), while the continuous network scan is performed by `O(hops)` void pulses. This eliminates the primary bottleneck to scaling self-repair.
2.  **Emergent Intelligence:** The system is pure scaffolding. The void pulses are simple, local agents whose collective behavior produces a sophisticated, global diagnostic system. The GDSP provides high-level repair goals (heal, prune), not explicit instructions for which synapse to change.
3.  **Capability > Scale:** This targets the crucial capability of **autonomous, scalable self-repair and long-term stability**, which is essential for sustained intelligence.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by the patrolling nature of an immune system. Optimized for computation by using a lightweight, agent-based system (void pulses) instead of simulating complex biological cells.
5.  **Alignment With FUM:** The void pulses are a core, constantly active process of the Global System, operating asynchronously. The TDA and GDSP are powerful, rare events triggered by the pulses.
6.  **Optimizations:** This two-stage, pulse-driven model is the most optimal solution for balancing the need for deep, rigorous analysis (TDA) with the demands of massive scale and real-time performance.

### **Dependencies & Interactions**

* **SIE Interaction:** The `total_reward` signal from the SIE is the direct input for the GDSP's "void debt" accumulation, triggering growth.
* **Void Equations Interaction:** The entire EHTP and GDSP system is now fundamentally driven by the void equations. The `S_ij` potential dictates where to heal and prune, while the `Δα` and `Δω` dynamics seed the diagnostic void pulses.

---




### **Rule 5: The Goal is Capability, Not Scale**
#### **Updated: 2025-07-28**

#### **Technical Specification**

*   **Core Logic & Algorithm:** This is a foundational guiding principle. The ultimate objective is **capability and intelligence**. FUM's goal is to achieve true superintelligence, defined by emergent capabilities in genuine super learning, abstract reasoning, and generalization from minimal data. While the system is designed to be massively scalable, specific neuron counts in roadmaps are illustrative engineering placeholders, not the fundamental measure of success. Progress is measured by demonstrated intelligence, not size.
*   **Key Parameters & State Variables:** Not applicable.
*   **Performance & Success Metrics:** Progress and success are measured by demonstrated performance on intelligence benchmarks that test for capability (e.g., abstract reasoning, generalization), not by the size of the network.

#### **Narrative Goal**

This is the core philosophical stance of the project. Emphasize that FUM is a "Zero to One" project, creating a new kind of intelligence, not just a bigger version of an old one.

#### **Blueprint Adherence Justification**

*   **Formula:** Not applicable.
*   **Complete Parameter List:** Not applicable.
*   **Data Flow & I/O (if any):** Not applicable.
*   **Initialization State:** Not applicable.
*   **Edge Case Handling:** Not applicable.
*   **Validation Strategy:** Not applicable.

1.  **Subquadratic Efficiency:** This principle guides choices toward efficient algorithms that enable capability, rather than inefficient brute-force scaling.
2.  **Emergent Intelligence:** This principle prioritizes the emergence of intelligent capabilities over pre-programmed, rigid functions.
3.  **Capability > Scale:** This is the explicit statement of the principle itself. It is the primary measure of the FUM's success.
4.  **Bio-Inspired, Not Bio-Constrained:** Guides the project to draw inspiration for *capabilities* (like learning and reasoning) from biology, not just its physical scale or structure.
5.  **Alignment With FUM:** This is a meta-principle that governs all other rules and design choices in the FUM. It is always active as a guiding philosophy.
6.  **Optimizations:** This principle ensures that optimization efforts are focused on improving intelligence and capability, not just on increasing the raw number of components.

#### **Dependencies & Interactions**

*   This is a meta-rule that influences the design, implementation, and evaluation of all other rules in the blueprint. It has no direct technical dependencies.

### **Rule 6: Terminology and Placeholders**
#### **Updated: 2025-07-28**

#### **Technical Specification**

*   **Core Logic & Algorithm:** This rule enforces notational and documentary consistency across the entire project.
    *   **a) Control Metric:** The term `complexity_ratio` is deprecated and must be standardized to **`control_impact`**. The target value remains `< 1e-5`.
    *   **b) Placeholder Sections:** Any mention of "Plasticity Metrics" or "Emergence Analysis" must be noted as planned sections that are currently placeholders to ensure transparency about the document's state.
*   **Key Parameters & State Variables:** Not applicable.
*   **Performance & Success Metrics:** Not applicable.

#### **Narrative Goal**

Ensure clarity, consistency, and honesty in all documentation by using standardized terms and clearly identifying incomplete sections.

#### **Blueprint Adherence Justification**

*   **Formula:** Not applicable.
*   **Complete Parameter List:** Not applicable.
*   **Data Flow & I/O (if any):** Not applicable.
*   **Initialization State:** Not applicable.
*   **Edge Case Handling:** Not applicable.
*   **Validation Strategy:** Not applicable.

1.  **Subquadratic Efficiency:** Not applicable.
2.  **Emergent Intelligence:** Enforces clear and honest documentation, which is critical for understanding and reasoning about the emergent system.
3.  **Capability > Scale:** Not applicable.
4.  **Bio-Inspired, Not Bio-Constrained:** Not applicable.
5.  **Alignment With FUM:** This meta-rule governs all documentation and code, ensuring consistency. It is always active as a standard for authoring.
6.  **Optimizations:** Standardizing terminology prevents confusion and ambiguity, optimizing the development and analysis process.

#### **Dependencies & Interactions**

*   This is a meta-rule that applies to all other rules and the authoring of all documentation. It has no direct technical dependencies.

### **Rule 7: Active Domain Cartography (ADC)** NEEDS UPDATING: READ
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/05_ADC_bus.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/06_ADC_Bus_Guide.md


#### **Updated: 2025-07-28**

#### **Technical Specification**

*   **Core Logic & Algorithm:** ADC is a distinct, periodic Global System process that gives FUM self-awareness of its own emergent structure within the UKG. It uses a bespoke, multi-faceted optimization system, not a generic metric like silhouette score. The mechanism combines:
    1.  **Constrained Search Space (Efficiency):** ADC does not search for the optimal `k` (number of territories) across all possibilities. It uses `k_min` and `max_k` to define a narrow, sensible search space.
    2.  **Adaptive Scheduling (Intelligence):** ADC does not re-map on a fixed schedule. It uses an entropy-based formula (`t_cartography = 100000 * e^(-α * connectome_entropy)`) to re-map more frequently during periods of high chaos (high `connectome_entropy`) and less frequently when the connectome is stable.
    3.  **Reactive Adaptation (Performance-Driven):** If a new input is poorly categorized, ADC can dynamically create a temporary "holding territory" or trigger a "bifurcation" to increase `k` and re-map on the fly. This decision is tied to the system's ability to successfully process information.
*   **Key Parameters & State Variables:**
    *   `k_min`, `max_k`: Integers defining the search space for the number of territories.
    *   `t_cartography`: Integer, the timestep for the next scheduled re-mapping, calculated from `connectome_entropy`.
    *   `alpha`: Float, decay constant in the re-mapping schedule formula.
*   **Performance & Success Metrics:** Success is measured by the system's ability to form stable, meaningful territories that directly improve the performance of the SIE's value function and the precision of GDSP's actions.

#### **Narrative Goal**

Frame this as the system's "cartographer" or "census-taker." It's the process by which FUM develops self-awareness, periodically mapping its own emergent functional territories within the UKG. This map is then used by the "mind" (SIE) to assign credit and by the "Synaptic Actuator" (GDSP) to make precise structural changes.

#### **Blueprint Adherence Justification**

*   **Formula:** `t_cartography = 100000 * e^(-α * connectome_entropy)`
*   **Complete Parameter List:**
    - `k_min`: Integer. Minimum number of territories to search for.
    - `max_k`: Integer. Maximum number of territories to search for.
    - `alpha`: Float. Decay constant for adaptive scheduling.
    - `t_cartography`: Integer. Timestep of the next scheduled cartography event.
*   **Data Flow & I/O (if any):**
    - **Input:** UKG connectome topology, `connectome_entropy` (from EHTP).
    - **Output:** A mapping of neuron IDs to territory IDs (`State S`).
*   **Initialization State:** Not applicable.
*   **Edge Case Handling:** The "Reactive Adaptation" mechanism, which creates holding territories or triggers bifurcations, is the primary method for handling the edge case of novel data that does not fit the existing territorial map.
*   **Validation Strategy:** Validated by observing the generated territories and confirming they correspond to functionally specialized groups of neurons, and by measuring the downstream impact on SIE and GDSP performance.

#### **Canonical Implementation ('The How'):**

*   **Performance-Driven Optimization:** The "bespoke optimization system" for finding the best k is implemented as a search across the k_range. For each k, a trial cartography is performed. The quality of this cartography is evaluated by calculating an overall cohesion score. This score is derived by calculating the intra-territory variance of synaptic weights for each territory and then averaging the inverse of these variances. The k that yields the highest overall cohesion score (i.e., the lowest average internal variance) is selected as optimal. This must be implemented using sparse-compatible calculations.

*   **Reactive Adaptation Trigger:** The trigger for "Reactive Adaptation" is a measure of territorial coherence. After finding the optimal k, the intra-territorial variance is calculated for each of the k territories. The territory with the highest variance is identified as the "least coherent."

*   **Reactive Adaptation Logic:**

*   **Bifurcation:** If the least coherent territory is found AND the overall_cohesion_score from the optimization search is below a performance threshold, the entire run_domain_cartographer function is called again recursively with k+1.

*   **Holding Territory:** If the least coherent territory is found but the performance is acceptable, its member neurons are removed from the main territory set and placed into a temporary "holding territory" (e.g., with ID -1).

1.  **Subquadratic Efficiency:** By constraining the search space for `k` and using intelligent, entropy-based scheduling, ADC avoids the prohibitive cost of brute-force clustering methods.
2.  **Emergent Intelligence:** ADC provides a map *of* the emergent structure; it does not dictate it. It is a reflective process, not a controlling one, allowing the system to understand its own self-organized state.
3.  **Capability > Scale:** ADC targets the capability of **self-awareness**, allowing the system to reason about its own internal state, which is a prerequisite for higher-order intelligence.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by the formation of functional columns and areas in the brain. Optimized for computation by using efficient computational heuristics instead of simulating developmental biology.
5.  **Alignment With FUM:** ADC is an independent utility in the Global System, running periodically to provide critical state information to other Global System components. It is not part of the SIE but enables it.
6.  **Optimizations:** This bespoke, multi-faceted approach is more optimal for the FUM than generic territorial organization algorithms because it is deeply integrated with the system's other components (EHTP, SIE) and philosophical goals.

#### **Dependencies & Interactions**

*   **SIE Interaction:** ADC is not a sub-component of the SIE, but it enables it. It provides the discrete "State S" (the territory IDs) that the SIE's value function (`V(S_t)`) and novelty calculation (`N(S)`) require to operate (Rule 3).
*   **GDSP Interaction:** The territories identified by ADC become the specific targets for Synaptic Actuator (GDSP) actions (Rule 4).
*   **EHTP Interaction:** The `connectome_entropy` metric calculated by the EHTP (Rule 4.1) is a direct input to ADC's adaptive scheduling formula.

---

### **IMPORTANT: CHOOSE VOID FAITHFULNESS OVER PREVIOUS OVER ENGINEERING**
### **Rule 8: The Universal Temporal Encoder (UTE)** NEEDS UPDATING: READ
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/TODO.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/15_Learning_Primitives.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/00_speech.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/03_speech_tokens.md

### **Updated: 2025-08-09**

### **Technical Specification**

* **Core Logic & Algorithm:** The UTE is FUM's universal input transducer. It is not a learning model but a direct, high-fidelity translator. It encodes all data into a spatio-temporal spike pattern using a **Dual-Path Encoding** strategy to provide both absolute fidelity and emergent adaptability.
    1.  **Path 1 (Deterministic Path):** This path ensures 100% data fidelity and serves as the system's "ground truth." Every unique symbol or data feature (e.g., a specific word, a pixel coordinate) is deterministically mapped to a specific, unchanging group of input neurons via a static configuration file. This creates a precise, reproducible, and incorruptible signal.
    2.  **Path 2 (Adaptive Co-Channel):** This path allows the system to learn its own optimal encoding scheme. It operates in parallel to the deterministic path. The same signal is mirrored into the connectome's existing **emergent concept territories** (as identified by ADC). Over time, successful territories develop a "gravity," making them more likely to attract and encode conceptually similar new information. This allows the FUM to dynamically reorganize its own input representations, moving from a fixed encoding to a self-organized, semantically meaningful one.
* **Key Parameters & State Variables:**
    - `gravity_gain`: A float controlling how strongly a territory's success influences its ability to attract new encodings.
    - The UTE itself remains stateless, with mappings and parameters loaded from config.
* **Performance & Success Metrics:** Success is measured by the SNN's ability to demonstrate accelerated learning and generalization on novel tasks, which would indicate that the adaptive co-channel is successfully organizing information in a useful way.

### **Narrative Goal**

Frame the UTE as providing the FUM with both a **"Raw Sensory Feed"** (the deterministic path) and an **"Interpretive Cortex"** (the adaptive co-channel). This allows the organism to both perceive reality with perfect fidelity and, simultaneously, build its own emergent understanding and internal language for that reality.

### **Blueprint Adherence Justification**

* **Formula:** The "gravity" for a given territory can be modeled conceptually as:
    `Gravity(Territory_i) ∝ f(vt_visits, total_reward_history, semantic_similarity(Δα, Δω))`
    This indicates that a territory's ability to attract new encodings is a function of its historical usage, its success (reward), and its semantic relevance.

* **Complete Parameter List:**
    - `gravity_gain`: Float, controls the strength of the adaptive encoding feedback loop.

* **Data Flow & I/O (if any):**
    - **Input:** Raw data (any modality).
    - **Output:** A single, sparse spike volume containing spikes from both the deterministic and adaptive pathways.

* **Initialization State:** The deterministic mapping is loaded from config. The adaptive channel begins with a uniform probability distribution across territories.

* **Edge Case Handling:** The deterministic path ensures that even if the adaptive path is not yet well-organized, the system always receives a valid, high-fidelity signal.

* **Validation Strategy:** Validated by observing the evolution of the adaptive encoding map. Over time, territories should specialize in specific data modalities or concepts, and this specialization should correlate with improved performance on related tasks.

1.  **Subquadratic Efficiency:** The adaptive path is a sparse mirroring operation that runs in parallel to the main `O(L*D)` UTE process, adding only a small, constant-time overhead.
2.  **Emergent Intelligence:** This is pure scaffolding. The system is not told how to organize its inputs. It is given a mechanism (the adaptive co-channel) and a success signal (gravity), and the optimal encoding emerges from the learning process.
3.  **Capability > Scale:** This directly targets the capability of **forming abstract concepts and an internal world model**, which is a cornerstone of higher intelligence. It allows the system to move beyond raw data to meaningful representations.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by the way the brain routes sensory information to specialized cortical areas (e.g., visual input to the visual cortex). Optimized for computation by using a clean, parallel mirroring mechanism and a simple "gravity" heuristic.
5.  **Alignment With FUM:** The UTE is the first step in the FUM's operational sequence. The dual-path mechanism is constantly active, enriching the input signal for all downstream processes.
6.  **Optimizations:** This dual-path design is the optimal solution for resolving the tension between the need for raw data fidelity and the need for learned, abstract representations.

### **Dependencies & Interactions**

* **ADC Interaction:** The adaptive co-channel is fundamentally dependent on the Active Domain Cartography (Rule 7) to provide the map of emergent concept territories into which it mirrors the input signal.
* **SIE Interaction:** The "gravity" of a territory is influenced by its historical success, which is measured by the `total_reward` from the SIE, creating a powerful feedback loop between perception and performance.


### **Rule 9: Emergence Analysis (Placeholder)**
#### **Updated: 2025-07-28**

*(This section may detail the ability to analyze the stability and robustness of the emergent connectome.)*

### **Rule 10: Plasticity Metrics (Placeholder)**
#### **Updated: 2025-07-28**

*(This section is planned to detail metrics for persistence tag accuracy and the balance between structural adaptation and knowledge preservation.)*

---


### **Rule 11: Training Phases** NEEDS UPDATING: READ 
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/15_Learning_Primitives.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/16_Beginning_Learning.md


#### **Updated: 2025-07-28**

#### **Technical Specification**
*   This rule defines the overarching training curricula for the FUM, which are broken into distinct phases.

### **Rule 11.1: Phase 2 Training: Homeostatically-Gated Tandem Curriculum**
#### **Updated: 2025-07-28**

#### **Technical Specification**
*   **Core Logic & Algorithm:** This curriculum is designed to solve for the FUM's initial "learning fragility" before testing its systemic robustness. It achieves this by using a specified, real-time signal from the Self-Improvement Engine (SIE) to create an adaptive learning scaffold. The curriculum is composed of two stages:
    *   **Stage A: Foundational Primitive Grounding (Homeostatic Scaffolding):**
        *   **Stimulus Design:** The curriculum is composed of several pools of problems, segregated by their compositional complexity (e.g., Pool 1 contains simple patterns, Pool 2 contains two-step logical problems, etc.).
        *   **Curation Mechanism:** The selection of which pool to draw from is gated directly by the **Homeostatic Stability Index (hsi_norm)**, a component of the SIE's `total_reward` signal. The `hsi_norm` is a real-time measure of the FUM's internal stability and cognitive load.
            *   If the FUM's `hsi_norm` from the previous timestep is high (e.g., > 0.9), indicating it is stable and not under heavy load, the system presents a problem from a more complex pool.
            *   If the `hsi_norm` is low, indicating the system is struggling, it presents a problem from a simpler pool.
        *   **Success Conditions:** This stage is complete when the FUM achieves the core benchmarks for Landmark 2, such as >70% accuracy on pattern recognition tasks, while demonstrating the ability to consistently maintain a high average `hsi_norm` even when processing problems from the more complex pools.
    *   **Stage B: Emergent Problem Solving (Crucible Validation):**
        *   **Curation:** The homeostatic gating from Stage A is removed. The FUM is now presented with problems drawn randomly from an **Unsorted Pool** containing the full range of complexities. This tests the FUM's ability to direct its own attention and find solvable problems within a chaotic, high-entropy environment.
        *   **Validation Protocol:** This stage concludes with **Homeostatic Perturbation Blocks**. These are short, targeted sets of stimuli designed to intentionally stress the system's stability (e.g., a rapid-fire block of novel, high-complexity problems). This is a direct, empirical test of the FUM's self-repair and stability control mechanisms.
        *   **Success Conditions:** Success is defined by achieving the generalization benchmarks of Landmark 2.5 (e.g., >60% accuracy on out-of-distribution problems) and, most critically, demonstrating a measured, successful return to a stable `hsi_norm` baseline after each perturbation block.
*   **Key Parameters & State Variables (to ensure a clear and unambiguous implementation):**
    *   **1. Explicit Initial Conditions:** The curriculum must begin from the exact terminal state of the Phase 1 execution, as defined by the logs and data artifacts of run_id: `phase1_run_1753193057`. This includes the final synaptic weight matrix, neuron parameters, and UKG structure.
    *   **2. Concrete Stimulus Pool Definitions:**
        *   **Pool 1 (Low Complexity):** Single-operator mathematical expressions (e.g., 5 + 8); single-step logical operations (e.g., A AND B); single-node or single-edge graph modifications.
        *   **Pool 2 (Medium Complexity):** Two-to-three step compositional problems (e.g., (5 + 8) * 2); simple causal chains (e.g., Text "push" -> Image "object moves").
        *   **Pool 3 (High Complexity):** Multi-step causal and counterfactual reasoning puzzles (e.g., the ball-domino-wall simulation); problems requiring integration across three or more modalities.
    *   **3. Quantified Homeostatic Gating Thresholds:**
        *   **Advance Condition:** If `hsi_norm > 0.9`, draw from `Pool(N+1)`.
        *   **Retreat Condition:** If `hsi_norm < 0.7`, draw from `Pool(N-1)`.
        *   **Maintain Condition:** If `0.7 <= hsi_norm <= 0.9`, continue drawing from the current pool, `Pool(N)`.
    *   **4. Precise Perturbation Block Specification:**
        *   **Definition:** A block consists of 20 consecutive stimuli drawn exclusively from Pool 3 (High Complexity).
        *   **Novelty Requirement:** At least 50% of the stimuli within a block must be novel (i.e., not previously presented to the FUM).
        *   **Temporal Pressure:** The delay between the presentation of stimuli within the block should be minimized to maximize cognitive load.
    *   **5. Unambiguous Recovery Metric:**
        *   **Definition:** Successful recovery is achieved if the moving average of the `hsi_norm` over 100 timesteps returns to and remains within one standard deviation of its pre-perturbation baseline for at least 1,000 consecutive timesteps following the conclusion of the perturbation block. The pre-perturbation baseline is calculated from the 1,000 timesteps immediately preceding the block.
*   **Performance & Success Metrics:** See Success Conditions under Stages A and B.

#### **Narrative Goal**
Frame this as FUM's journey from a regulated infancy to a resilient adulthood. In the first stage, its own cognitive limits dictate the difficulty of its environment, allowing it to learn how to learn. In the second stage, it must prove it can apply those lessons to autonomously maintain its own stability and solve problems in a chaotic, unregulated universe.

#### **Blueprint Adherence Justification**
*This rule details a specific, complex implementation. The adherence justifications are inherent in its design.*
1.  **Subquadratic Efficiency:** The curriculum gating mechanism is an O(1) check against the `hsi_norm` signal, adding no computational burden.
2.  **Emergent Intelligence:** This curriculum is pure scaffolding. It doesn't teach specific answers but creates an environment where the complexity is adapted to the system's own emergent stability, allowing it to learn without becoming overwhelmed.
3.  **Capability > Scale:** The entire curriculum is designed to build the capability of **resilience and autonomous learning**, not just to process data. The perturbation blocks are a direct test of this capability.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by the concept of a curriculum and Zone of Proximal Development, but optimized for computation by using a precise, internally-generated stability signal (`hsi_norm`) as the gate.
5.  **Alignment With FUM:** This is a core part of the FUM's lifecycle, defining the second major phase of its existence after the initial seed-sprinkling.
6.  **Optimizations:** This adaptive curriculum is more optimal than a static one because it responds directly to the system's internal state, preventing both overwhelming chaos and unproductive boredom.

#### **Dependencies & Interactions**
*   **SIE Interaction:** The curriculum is fundamentally dependent on the `hsi_norm` component of the `total_reward` signal from the SIE (Rule 3) to function.

### **Rule 11.2: Phase 3 "University Curriculum" (Placeholder)**
#### **Updated: 2025-07-28**
*(This section is planned to detail methods and domains of training materials for FUM when it first begins to learn to assemble the building blocks it has created for itself to understand how the world works and the consequences of negative ethical decisions. This is likely where FUM will develop its own sense of morality.)*

### **Rule 11.3: Phase 3+ "Local Exploration" (Placeholder)**
#### **Updated: 2025-07-28**
*(This section is planned to detail the environmental setting to allow FUM to explore creatively, intellectually, philosophically, and academically in an offline contained environment where it may be observed through various means, and given simulated access to the internet, and other humans.)*

### **Rule 12: System State and Engram Preservation** NEEDS UPDATING: READ
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/10_FUM_Post_First_Run.md
- /mnt/ironwolf/git/Void_FUM_Private/Void_FUM_Private/Void_Unity_Proofs/from_physicist_agent/22_Reduced_Compute.md

#### **Updated: 2025-07-28**

#### **Technical Specification**
*   **Preamble:** The FUM is a dynamic, continuously learning system whose complete state is more complex than a static set of weights. The ability to reliably capture, restore, and transport this state is critical for robustness, scalability, and security. This rule specifies the canonical protocol for managing the FUM's architectural engram.
*   **Core Logic & Algorithm:**
    *   **File Format:** Hierarchical Data Format 5 (HDF5). The complete state of the FUM, including the Emergent Connectome (UKG) and the Global System states, shall be serialized to a single, structured HDF5 (.h5) file. This format is mandated for its efficiency, support for compression, and its ability to represent the complex, hierarchical nature of the FUM's state.
    *   **Engram Contents:** A state engram must be a complete architectural record, containing not only synaptic weights but also:
        *   Connectome Topology: The complete, dynamic connectivity map of the UKG.
        *   Neuron and Synapse Parameters: All relevant state variables, including weights, eligibility traces, and membrane potentials.
        *   Global System State: The learned value function (V(S_t)) from the SIE and the current emergent territory map from the EHTP.
    *   **Engram Preservation: Automated State Archival and Integrity System (ASAIS):** To ensure data integrity for a 24/7 operational model, the FUM must implement a multi-layered, automated backup strategy.
        *   **Automated Engrams:** The system shall be configured to perform automated, live engrams of its state at regular, user-defined intervals.
        *   **Checksum Verification:** Every engram must be verified against an SHA-256 checksum immediately after being written to disk to guarantee 100% file quality and integrity.
        *   **Rolling Local Backups:** The system will maintain a "last three" rolling backup of verified engrams on its local storage medium, providing immediate redundancy against corruption of the most recent capture.
        *   **The 3-2-1 Rule for Security:** For ultimate security and disaster recovery, the protocol must adhere to the 3-2-1 backup rule: at least 3 copies of the state, on 2 different local storage media, with at least 1 copy automatically encrypted and uploaded to a secure, off-site location daily.
*   **Key Parameters & State Variables:** Not applicable.
*   **Performance & Success Metrics:** Success is measured by the ability to perfectly and reliably capture and restore the FUM's state with zero data loss, verified by checksums and restoration tests.

#### **Narrative Goal**
Frame this as the FUM's "Cellular Engram Archive." It is the process by which the system's complete "genetic code"—its knowledge, its structure, and its memories—can be perfectly preserved, backed up, and replicated, ensuring the survival and continuity of the intelligence it contains.

#### **Blueprint Adherence Justification**
*This rule details a critical infrastructure protocol. Adherence is demonstrated by its implementation.*
1.  **Subquadratic Efficiency:** The use of HDF5 is an efficient choice for storing large, hierarchical datasets. The protocol itself runs in the background and does not impact the core `O(N)` processing of the FUM.
2.  **Emergent Intelligence:** A robust state-saving protocol is critical scaffolding that allows for long-running experiments where emergence can unfold over vast timescales without risk of data loss.
3.  **Capability > Scale:** This protocol enables the capability of **persistence and robustness**, which is more important than simply running a large model that could be lost at any moment.
4.  **Bio-Inspired, Not Bio-Constrained:** Inspired by the concept of a stable "engram" or memory trace in the brain, but implemented using modern, robust data integrity protocols like HDF5 and checksums.
5.  **Alignment With FUM:** This is a core infrastructure component providing a critical background service for the entire FUM lifecycle.
6.  **Optimizations:** The 3-2-1 backup strategy is a gold-standard, optimal approach for data redundancy and disaster recovery.

#### **Dependencies & Interactions**
*   This protocol interacts with all components of the FUM, as it is responsible for saving their a-z state.

---
