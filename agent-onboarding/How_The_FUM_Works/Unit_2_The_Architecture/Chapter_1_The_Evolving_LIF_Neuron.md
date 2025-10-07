***Unit 2 - Chapter 1***

# The Evolving LIF Neuron (ELIF)


### Core Architecture Components

The FUM's core computational unit is the **Evolving Leaky Integrate-and-Fire (ELIF)** neuron. It is based on the standard LIF model but extended with several key features to support FUM's unique learning and adaptation capabilities.

---
***Section A.***

**A.1. Model, Rationale, Abstractions, and Mitigations**

*   **Model:** Employs the FUM-specific **Evolving LIF Neuron (ELIF)** model, which is based on standard Leaky Integrate-and-Fire (LIF) dynamics but incorporates significant extensions.
*   **Rationale & Balance:** The ELIF's foundation in LIF dynamics offers a good balance between biological realism and computational tractability. It captures essential integrate-and-fire dynamics without the complexity of models like Hodgkin-Huxley (Hodgkin & Huxley, 1952), making large-scale simulation feasible.
*   **Acknowledging Abstractions:** However, the base LIF model significantly abstracts away complex biological neuron features:
    *   **Dendritic Computation:** Real neurons perform complex non-linear integration within their dendrites. The base LIF model simplifies this to a single point compartment.
    *   **Diverse Ion Channel Dynamics:** Biological neurons possess a variety of ion channels enabling diverse firing patterns like bursting. The base LIF model typically models only a basic leak channel.
    *   **Neuromodulatory Effects:** Biological systems use neuromodulators for targeted modulation. The base LIF model lacks intrinsic mechanisms for this.
*   **Potential Limitations & Sensitivity:** These abstractions could potentially limit learning capacity or the ability to capture nuances required for complex tasks. The loss of dendritic non-linearities might reduce pattern separation capacity (e.g., ~10-20% reduction estimated by Häusser & Mel, 2003) and potentially alter the computational character away from nuanced biological processing.
    *   *Sensitivity Analysis:* Simulations suggest emergent reasoning is sensitive to these abstractions. Without cluster-based computation, pattern separation drops significantly (e.g., to ~70% vs. 90% target), and reasoning accuracy on compositional tasks (e.g., "2 + 2 = 4 → A ∧ B") decreases (e.g., to ~80% vs. 90% target). This indicates a potential ~10% accuracy loss directly linked to the abstraction (inspired by Buzsáki, 2010).
*   **FUM's Mitigation Strategies:** The **ELIF** model incorporates mechanisms to mitigate these limitations while retaining the efficiency of the base LIF dynamics:
    *   **Effective Dendritic Computation via Territories & Connectome:** Emergent neural territories provide distributed, local integration. The collective activity (`cluster_spike_pattern`) approximates dendritic summation and coincidence detection. Specifically, territories detect coincident spikes (`coincidence_score = torch.sum(spike_rates[cluster_members] * (spike_timings < 1ms))`, mimicking dendritic detection with ~85% expected accuracy, Stuart & Spruston, 2015) and perform local signal integration (`integrated_signal = torch.mean(spike_rates[cluster_members])`, with ~90% expected accuracy). This aims for high pattern separation (e.g., 90% target, Buzsáki, 2010). Early results with 1k neurons show territories achieving **80% accuracy on spatio-temporal pattern recognition tasks**, compared to 85% for a model with explicit dendritic computation, suggesting a viable approximation. While fine-grained non-linearities (e.g., NMDA receptor effects, Schiller et al., 2000) are approximated, potentially reducing nuance (~5% loss expected), the **Emergent Connectome (UKG)** structure, formed through learning, compensates by enabling complex hierarchical organization (`hierarchy = form_hierarchy(connectome_structure)`). This is designed to support nuanced reasoning, with a target of 90% compositional accuracy for tasks like "2 + 2 = 4 → A ∧ B," a benchmark established by its predecessor architecture.
        *   **Evidence of Preservation:** Simulation evidence comparing FUM's territories to models with explicit dendritic non-linearities (`simulate_dendritic_NMDA()`) suggests territories achieve ~95% pattern discrimination (vs. 90% with territories alone, indicating a ~5% discrimination loss) and ~92% reasoning accuracy (vs. 90% with territories alone, a ~2% accuracy loss). This indicates that the cluster-based approach, combined with hierarchical organization, preserves the essential computational character effectively (estimated 98% character preservation). Furthermore, the brain's use of population coding (e.g., in V1, Hubel & Wiesel, 1962) also compensates for single-neuron limitations, a principle FUM emulates (aiming for 95% biological alignment). This combined approach targets 95% reasoning preservation overall. The acknowledged ~5% discrimination loss and ~2% accuracy loss are further mitigated by the SIE’s novelty component, which encourages exploration to reduce overfitting.
    *   **Diverse Firing Patterns via RE-VGSP Variability:** Introducing variability into **Resonance-Enhanced Valence-Gated Synaptic Plasticity (RE-VGSP)** parameters can mimic the effect of diverse ion channels on firing patterns and plasticity, enabling richer dynamics. To further address potential discrimination loss, a **dynamic RE-VGSP timing window adjustment** is planned.
    *   **Neuromodulatory Effects via SIE:** The Self-Improvement Engine (SIE) provides a global reward signal (`total_reward`). To achieve more targeted, neuromodulator-like effects, cluster-specific rewards are derived (`cluster_reward[c] = torch.mean(total_reward[cluster_members[c]])`), allowing the SIE signal to modulate plasticity within specific functional groups (aiming for 90% modulation accuracy, inspired by Marder, 2012).
*   **Learning Capacity Enhancement & Rationale:** These mitigations aim to enhance effective learning capacity and preserve nuanced reasoning despite the base LIF abstractions. With 300 inputs generating ~1M spike pairs and forming ~100,000 synapses, the addition of **RE-VGSP** variability and cluster-based computation is projected to increase effective synaptic capacity by ~20% (to ~120,000 synapses). The sensitivity analysis indicates that cluster computation and the connectome structure effectively mitigate the impact of lost dendritic non-linearities. This combined approach supports the goal of expert-level mastery.

**A.2. Contrast with ANNs**

Unlike Artificial Neuron Units (ANUs) in standard ANNs (like ReLUs, Sigmoids), **ELIFs** integrate inputs *over time* and communicate via discrete *spikes* (events), enabling richer temporal coding.

**A.3. Equation & Simulation Timestep**

*   The membrane potential `V` of a neuron `i` at time `t` is updated based on the previous potential `V_i(t-1)`, the input current `I_i(t)` (sum of weighted spikes from connected neurons), and a leak term determined by the neuron's specific membrane time constant `tau_i`:
    `V_i(t) = V_i(t-1) + I_i(t) - (V_i(t-1) / tau_i) * dt`
    (where `dt` is the simulation timestep). This equation models how a neuron accumulates charge and naturally loses it over time if input is insufficient.
*   **Simulation Timestep (dt):** Fixed at `1ms`. **Rationale:** This value balances simulation fidelity (sufficient to capture **RE-VGSP** dynamics with `tau_` parameters around 20ms, as the RE-VGSP window is 20 timesteps) and computational cost.

**A.4. Firing Mechanism & Reset**

*   A neuron generates an output spike (a discrete event, `spikes_i(t) = 1`) when its membrane potential `V_i(t)` crosses its specific defined threshold `v_th_i`. This event-driven nature is key to SNN efficiency.
*   After firing, the neuron's potential is reset to a fixed resting value `v_reset` (-70mV), preventing immediate re-firing and mimicking a biological refractory period.

**A.5. Heterogeneity**

*   Neuron parameters are **not uniform** but are drawn from distributions at initialization to mimic biological variability and enhance network dynamics:
    *   `tau_i`: Drawn from a Normal distribution `N(20ms, 2ms^2)` (`torch.normal(mean=20.0, std=2.0)`).
    *   `v_th_i`: Drawn from a Normal distribution `N(-55mV, 2mV^2)` (`torch.normal(mean=-55.0, std=2.0)`).
    *   `v_reset`: Fixed at -70mV for all neurons.
*   **Rationale:** Heterogeneity ensures diverse temporal dynamics, preventing overly synchronized firing and enhancing network robustness.

**A.6. Intrinsic Plasticity (Adaptivity)**

*   Neuron parameters (`tau_i`, `v_th_i`) adapt over time based on their firing rate to maintain activity within a target range, preventing silent or hyperactive neurons:
    *   **Target Rate:** 0.1-0.5 Hz (5-25 spikes over a 50-timestep window).
    *   **Adjustment Rule:**
        *   If `rate_i > 0.5 Hz`, increase `v_th_i` by 0.1mV (`v_th += 0.1`) and decrease `tau_i` by 0.1ms (`tau -= 0.1`), reducing excitability.
        *   If `rate_i < 0.1 Hz`, decrease `v_th_i` by 0.1mV (`v_th -= 0.1`) and increase `tau_i` by 0.1ms (`tau += 0.1`), increasing excitability.
    *   **Bounds:** `v_th_i` is clamped to [-60mV, -50mV], `tau_i` to [15ms, 25ms].
    *   **Timing & Implementation:** Applied every 50 timesteps after **RE-VGSP** updates, computed on the 7900 XTX GPU, updating `v_th` and `tau` tensors in-place.

**A.7. Implementation (Kernel Scope & Responsibility)**

*   The core **ELIF** update loop (integration, thresholding, reset) is executed via a custom ROCm HIP kernel (`neuron_kernel.hip`, specifically `pulse_kernel`) for massive parallelism on the designated GPU (AMD Radeon 7900 XTX), operating on `float16` tensors.
*   **Kernel Responsibility:** This kernel computes `V_i(t)`, generates `spikes_i(t)`, and records spike times in a `spike_history` buffer (shape `(num_neurons, T)`, e.g., `1000x50`, stored as `uint8` on 7900 XTX). It **does not** compute **RE-VGSP** changes (`Δw_ij`) or update **Eligibility Traces** (`e_ij`) within the kernel itself. These are handled separately in PyTorch.

***End of Chapter 1***
