***Unit 2 - Chapter 4***

# Stability Controls

### Input Scaling Factor

A complex adaptive system, particularly one designed to learn, must walk a fine line between sensitivity and stability. It must be open enough to new information from the environment to change and adapt, yet robust enough to prevent that same information from overwhelming its internal dynamics and causing catastrophic failure. This chapter explores one of the simplest and most essential mechanisms the FUM uses to maintain this delicate balance: the control and scaling of raw input stimulus. The membrane of a cell is a selective barrier, protecting the delicate machinery within from the chaotic environment outside. In a similar way, a neural network requires a buffer to shield its learning mechanisms from the raw, untamed nature of external data. Without such a buffer, the system can be shocked into a state of hyperactivity where learning becomes impossible.

---
***Section A.***

**A.1. Concept and Rationale**

*   **Problem:** A primary challenge in any spiking neural network is managing the influx of external stimuli. If external input currents are too strong, they can overwhelm the network, leading to widespread, synchronized firing that is both biologically unrealistic and computationally useless. This state of hyperactivity can prevent any meaningful learning or pattern discrimination from occurring.
*   **Solution:** To mitigate this, FUM employs a simple but critical stability mechanism: a global **Input Scaling Factor**.

---
***Section B.***

**B.1. Implementation**

*   **Mechanism:** Before any external stimulus was applied to the network's designated input neurons, the raw current values were multiplied by this scaling factor. In early demonstration models, this was controlled by a single parameter, `STIMULUS_SCALING_FACTOR`, which was typically set to a default value of `0.1`.
*   **Function:** This mechanism ensures that input from the environment provides a gentle nudge to the system's dynamics rather than a convulsive shock. It is a foundational component for maintaining network stability, particularly during the initial phases of self-organization when synaptic weights are still being adapted. By preventing hyperactivity, it allows the more nuanced dynamics of Resonance-Enhanced Valence-Gated Synaptic Plasticity (RE-VGSP) to operate effectively.

***End of Chapter 4***
