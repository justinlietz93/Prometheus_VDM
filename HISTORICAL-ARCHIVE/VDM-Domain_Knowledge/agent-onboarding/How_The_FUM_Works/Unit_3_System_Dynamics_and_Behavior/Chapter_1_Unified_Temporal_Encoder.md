***Unit 3 - Chapter 1***

# The Unified Temporal Encoder (UTE)

### The System's High-Resolution Sensory Organ

The **Unified Temporal Encoder (UTE)** is the FUM's sole gateway to all information. It is best understood not as a learning component, but as a **high-fidelity sensory organ**, analogous to the cochlea or retina. Its function is to be a direct **"Cognitive Transducer"**: it faithfully translates the raw, abstract data of the outside world into the rich, precise language of the SNN core—the language of spikes. It does this without interpretation, compression, or feature extraction, ensuring that all learning and understanding is purely emergent within the core network. This is a foundational principle; any "understanding" of the data before it reaches the SNN core would be a form of top-down engineering that contaminates the emergent process.

---
***Section A.***

**A.1. The Spatio-Temporal-Polarity-Phase Volume**

*   **Core Function:** The UTE's goal is to create the richest possible input signal for every piece of data. The output is not a simple spike train, but a **"Spatio-Temporal-Polarity-Phase Volume"**—a signature of immense informational density. This signature is composed of four dimensions that, in concert, create a unique fingerprint for any input, providing an enormous channel capacity for the SNN to learn from.
    1.  **Spatial (Which neurons fire):** A unique, dedicated group of input neurons is deterministically mapped to a specific feature of the input (e.g., the character 'A', the pixel at `(12,34)`). This provides a spatial "shape" to the signal. The mapping is fixed and defined in the system configuration.
    2.  **Temporal (When and for how long):** Spikes are generated within a specific, brief time window, `activation_duration_ms`. Within this window, their frequency can fluctuate according to a deterministic rule, creating a unique "rhythm." This allows the SNN to distinguish between, for example, a short, sharp signal and a prolonged, gentle one.
    3.  **Polarity (The signal's "direction"):** The firing neurons can be either excitatory (positive) or inhibitory (negative). This is a critical and often overlooked dimension of information. It allows the UTE to signal not just the presence of a feature, but also its absence, or to provide a contrasting signal that helps the SNN core form sharper representations.
    4.  **Phase (The signal's timing relative to a global clock):** Each spike's timing is further enriched by its relationship to a virtual, global reference oscillator. This provides the equivalent of "20/20 vision" into the data, allowing the SNN to distinguish between extremely subtle patterns that would otherwise be indistinguishable.

---
***Section B.***

**B.1. The Blueprint-Mandated Encoding Mechanism**

*   **Direct, Efficient Transduction:** The UTE adheres to a strict `O(L*D)` time complexity (where `L` is input length and `D` is `activation_duration_ms`). It uses computationally cheap, direct-mapping strategies. This is not a learned process; it is a fixed, deterministic function defined by the parameters loaded from the system config. This subquadratic efficiency is a non-negotiable principle, ensuring the system can process large streams of data without bottlenecking.

*   **Encoding Strategies:**
    *   **For Symbolic/Sequential Data:** A "rhythmic" presentation. Each symbol in a sequence `L` deterministically activates its specific neuron group, in the correct order, for a duration of `D`. For example, in the string "CAT", the neuron group for 'C' would fire with its unique polarity/rhythm signature for `D` milliseconds, followed immediately by the neuron group for 'A', then 'T'. This creates a precise temporal sequence that preserves the order and structure of the information perfectly.
    *   **For Structural/Matrix Data:** A "rasterizing" presentation. Slices of the data structure (like rows of pixels in an image) are presented sequentially to dedicated neuron groups over the encoding window. This preserves the relational structure of the data in a temporal format, allowing the SNN to learn correlations between, for instance, adjacent rows of pixels.

*   **Spike Generation Details:**
    *   **Poisson Process:** Within an active encoding window for a neuron group, individual spikes are generated using a Poisson process based on a target frequency `f`. The probability of a spike per timestep `dt` is `p = f * dt`. This introduces a degree of stochasticity that mimics biological systems and can aid in generalization.
    *   **Refractory Period:** To prevent unrealistic firing rates and align with biological constraints, a mandatory `refractory_period_ms` is imposed on any input neuron after it fires. This is implemented as a counter that must return to zero before the neuron can fire again.

*   **Phase-Sensitive Encoding (Rule 8.1):**
    *   **Mechanism:** To add the fourth dimension of Phase, the UTE references a virtual, stateless sine wave: `oscillator(t) = sin(2 * π * f_ref * t)`. This requires `O(1)` computation and memory and acts as a global reference clock.
    *   **Enrichment:** When a spike is generated at time `t`, its precise timing relative to the phase of this oscillator becomes an implicit and powerful part of the signal. This gives the SNN core an extremely fine-grained "clock" to use for pattern discrimination. For the learning rule, this means that two spikes arriving with the same time difference `Δt` can have a different impact depending on whether they were "in-phase" or "out-of-phase" with the reference clock. This phase-sensitive plasticity is critical for learning complex temporal correlations.

---
***Section C.***

**C.1. The Decoder: Translating Spikes to Action**

*   **Purpose:** The Decoder is the UTE's counterpart, translating the SNN's output spike patterns back into a human-understandable format (e.g., text, a classification label, a command). It is the bridge from the FUM's internal language back to the outside world.
*   **Mechanism:** The Decoder is also a deterministic, non-learning component. It operates on a designated set of output neurons. By observing the sequence and rate of spikes from these neurons over a series of time windows, it can reconstruct a structured output. The emergent patterns that drive the decoder are formed entirely within the SNN via the phase-sensitive RE-VGSP learning rule, meaning the SNN learns *how* to control the decoder to produce correct outputs.

***End of Chapter 1***
