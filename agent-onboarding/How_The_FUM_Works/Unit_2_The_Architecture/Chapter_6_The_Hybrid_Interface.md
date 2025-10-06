***Unit 2 - Chapter 6***

# The Hybrid Interface

### Tensor-Based Computation and Hybrid Interface

While SNNs excel at temporal processing, certain operations like analyzing connectome properties, calculating complex SIE rewards, managing large state vectors (like the **Eligibility Trace (`e_ij`)** or the value function `V_states`), or performing clustering are often more efficiently handled using optimized tensor libraries. FUM adopts a hybrid approach, leveraging the strengths of both SNN simulation and tensor computation.

---
***Section A.***

**A.1. Frameworks & Hardware Roles (Development Context)**

*   **PyTorch:** Utilizes PyTorch for tensor manipulation.
*   **AMD Radeon 7900 XTX (24GB VRAM):** Primarily runs the custom ROCm HIP kernel (`neuron_kernel.hip`) for high-frequency, parallel **ELIF** updates and spike generation. Also handles the final **RE-VGSP** weight updates (`w += ...`). Stores `V`, `spikes`, `spike_history`, `w`. Considerations are being made about converting the entire custom FUM math library via AMD's "Composable Kernel" framework located on their Github repository.
*   **AMD Instinct MI100 (32GB VRAM):** Primarily runs PyTorch tensor operations for tasks like the `Plasticity Impulse (PI)` calculation for **RE-VGSP**, **Eligibility Trace** (`e_ij`) updates, SIE component calculations (novelty, habituation, **HSI**, TD error), value function (`V_states`) updates, and k-means clustering. Stores `e_ij`, `V_states`, `recent_inputs`, `habituation_counter`, etc.
*   **CPU (AMD Threadripper PRO 5955WX):** Manages overall orchestration, data loading, potentially graph partitioning (METIS), parameter server logic (if scaling beyond node memory), and decoding outputs.

---
***Section B.***

**B.1. Interface: Data Flow & Synchronization**

*   **Frequency:** Interaction occurs primarily after each 50-timestep simulation window. Global operations like clustering or scaling occur less frequently (e.g., every 1000 timesteps).
*   **Data Flow (SNN -> Tensor):**
    1.  `spike_history` (uint8, ~6KB for 1k neurons) recorded on 7900 XTX by the **ELIF** kernel.
    2.  After 50 timesteps, transfer `spike_history` to MI100 (`spike_history_mi100 = spike_history.to('cuda:0')`).
    3.  MI100 computes `Plasticity Impulse (PI)`, updates the **Eligibility Trace** (`e_ij`), calculates `rates`, computes SIE components (`novelty`, `habituation`, `HSI`, `TD_error`), updates `V_states`.
*   **Data Flow (Tensor -> SNN):**
    1.  `total_reward` (float16 scalar) is calculated on the MI100.
    2.  The **Eligibility Trace (`e_ij`)** (sparse float16, ~10KB) has been updated on the MI100.
    3.  Transfer `total_reward` and the updated **Eligibility Trace (`e_ij`)** to the 7900 XTX (`total_reward.to('cuda:1')`, `e_ij.to('cuda:1')`).
    4.  The 7900 XTX applies the final weight update to `w` using `total_reward` and the transferred `e_ij` as part of the canonical **RE-VGSP** rule.
*   **Synchronization:** Use `torch.cuda.synchronize()` or CUDA events to ensure data transfers are complete before dependent computations begin. Buffering mechanisms (e.g., `rate_buffer` on MI100, appending `rates.to('cuda:0')` every 50 steps) handle aggregation for less frequent operations like k-means (processed when buffer full, e.g., 1000 steps). Timing mismatches are managed by the fixed interaction frequency (every 50 timesteps).

***End of Chapter 6***
