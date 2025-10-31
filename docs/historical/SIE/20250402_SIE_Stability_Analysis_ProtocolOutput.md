# SIE Stability Analysis Framework (Preliminary)

*Justin Lietz - 4/2/2025*

## 1. FUM Problem Context

The Self-Improvement Engine (SIE) is central to FUM's learning, integrating multiple reward components (`TD_error`, `novelty`, `habituation`, `self_benefit`) and applying a non-linear modulation to Spike-Timing-Dependent Plasticity (STDP). This modulation is defined by the factor

```math
\text{mod\_factor} = 2 \sigma(R_{\mathrm{total}}) - 1 , where R_{\mathrm{total}}
```

 represents the combined reward signal (referred to as `total_reward` in code) and $\sigma$ denotes the sigmoid function. The resulting STDP update is proportional to 
 
 ```math
 \Delta w_{ij} \propto \eta \cdot (1 + \text{mod\_factor}) \cdot R_{\mathrm{total}} \cdot e_{ij} 
 ```
 
 This complexity, detailed in `How_It_Works/2_Core_Architecture_Components/2C_Self_Improvement_Engine.md`, necessitates a formal analysis to guarantee stable learning dynamics, prevent reward hacking, and ensure convergence towards desired outcomes. Uncontrolled interactions between components or the non-linear modulation could lead to oscillations, unbounded weight growth, or optimization of spurious internal metrics instead of external task performance.

## 2. Justification for Novelty & Prior Art Analysis

Standard Reinforcement Learning (RL) stability analyses often assume simpler reward structures and linear learning rules. FUM's SIE requires a novel approach due to:
- **Multi-Objective Nature:** Balancing potentially conflicting internal drives (novelty vs. stability) with external task rewards.
- **Non-Linear Modulation:** The sigmoid mapping ($\sigma$) and quadratic reward influence on STDP deviate significantly from standard linear RL updates.
- **Coupled Dynamics:** The feedback loop where rewards influence plasticity, which changes network activity, which in turn affects future rewards and internal states (like novelty or self-benefit).
- **Emergent State Space:** The reliance on cluster IDs as states for TD learning adds another layer of dynamic complexity.

Techniques from non-linear control theory (Lyapunov stability), multi-objective optimization, and potentially dynamical systems analysis are needed to rigorously analyze this specific system.

## 3. Mathematical Formalism (In Progress)

The mathematical framework involves:

1.  **System Modeling:** Representing the coupled SIE-STDP dynamics as a system of non-linear difference equations. The core STDP update rule, refined to include linear weight decay ($\lambda$) and non-linear modulation based on the total reward ($R_{\mathrm{total}}$), is approximated as:
    ```math
    \Delta W = \left[ \eta \cdot (1 + \text{mod\_factor}) \cdot R_{\mathrm{total}} \cdot E \right] \cdot \Delta t - \lambda W \cdot \Delta t
    ```
    * Where:
        * $W$: Synaptic weight matrix.
        * $\Delta W$: Change in the weight matrix per time step $\Delta t$.
        * $\eta$: Base learning rate (`eta`).
        * $R_{\mathrm{total}}$: The combined SIE reward signal (referred to as `total_reward` in code).
        * $\sigma(\cdot)$: The sigmoid function.
        * $\text{mod\_factor} = 2 \sigma(R_{\mathrm{total}}) - 1$: The non-linear reward modulation factor.
        * $E$: Matrix of eligibility traces ($e_{ij}$).
        * $\lambda$: Positive weight decay coefficient.
        * $\Delta t$: Time step duration (often assumed $\Delta t=1$ or absorbed into $\eta$ and $\lambda$ for difference equation analysis).

    Synaptic scaling is modeled separately as a periodic multiplicative normalization of incoming weights.

2.  **Lyapunov Stability Analysis (Preliminary & Refined):**
    * **Candidate Function (Weights Only):** Analyzing stability using the Lyapunov function $L(W)$:
        ```math
        L(W) = \frac{1}{2} \|W\|_F^2 = \frac{1}{2} \sum_{i,j} w_{ij}^2
        ```
    * **Change Analysis:** The change $\Delta L$ per update step is approximately $\Delta L \approx \langle W, \Delta W \rangle_F$. Substituting the $\Delta W$ equation (assuming $\Delta t=1$ or absorbed, and defining the effective learning rate $\eta_{\mathrm{eff}} = \eta \cdot (1 + \text{mod\_factor})$) yields:
        ```math
        \Delta L \approx \langle W, \eta_{\mathrm{eff}} \cdot R_{\mathrm{total}} \cdot E - \lambda W \rangle_F
        ```
        ```math
        \Delta L \approx \eta_{\mathrm{eff}} \cdot R_{\mathrm{total}} \cdot \langle W, E \rangle_F - \lambda \|W\|_F^2
        ```
    * **Stability Condition:** For bounded weights ($\Delta L \le 0$), we require the decay term to dominate the learning term:
        ```math
        \lambda \|W\|_F^2 \ge \eta_{\mathrm{eff}} \cdot R_{\mathrm{total}} \cdot \langle W, E \rangle_F
        ```
    * **Refined Interpretation (Bounding Terms):** By applying the bounds $\eta_{\mathrm{eff}} \le 2\eta$, $|R_{\mathrm{total}}| \le R_{\mathrm{max}}$, and $|\langle W, E \rangle_F| \le \|W\|_F \|E\|_F$, we can derive an approximate condition for stability:
        ```math
        \|W\|_F \ge \frac{2\eta R_{\mathrm{max}}}{\lambda} \|E\|_F
        ```
        This suggests the system tends towards an equilibrium where the weight norm $\|W\|_F$ is proportional to the error norm $\|E\|_F$ and the ratio $(\eta R_{\mathrm{max}} / \lambda)$. This aligns with simulation results showing that increasing $\lambda$ reduces the final weight norm. It provides a theoretical basis for how weight decay counteracts unbounded growth. *This analysis is still preliminary and requires further refinement, particularly regarding the $V(\text{state})$ dynamics and the assumptions on bounds.*
    * **Coupled Analysis Attempt (W & V):** Using $L(W, V) = \frac{1}{2} \|W\|_F^2 + \frac{c}{2} \|V\|^2$, the change $\Delta L$ becomes approximately:
        ```math
        \Delta L \approx \left[ \eta_{\mathrm{eff}} \cdot R_{\mathrm{total}} \cdot \langle W, E \rangle_F - \lambda \|W\|_F^2 \right] + c \alpha \sum_k V_k (r_k + \gamma V_{k+1} - V_k)
        ```
        Rigorously bounding this expression to find stability conditions for all parameters is mathematically complex due to coupled non-linearities and stochasticity. Advanced techniques (e.g., stochastic approximation theory) or simplifying assumptions are likely required for formal proofs. *Further theoretical work is needed.*

3.  **Convergence Analysis (Planned):** Identifying fixed points ($\Delta W = 0$, $\Delta V = 0$) of the refined system and analyzing their stability. Deriving bounds on reward variance.

4.  **Multi-Objective Analysis (Planned):** Using Pareto optimality concepts to analyze trade-offs between SIE components.

5.  **Gaming Analysis (Planned):** Identifying parameter regimes prone to reward hacking.

*(Note: Formal derivation of stability conditions and convergence proofs is pending further theoretical work in Phase 2 of the plan).*

## 4. Assumptions & Intended Domain

- Assumes the simplified simulator captures the core dynamics relevant to stability.
- Assumes the mathematical tools (Lyapunov theory, control theory) are applicable to this specific non-linear, multi-objective system.
- Intended domain is the FUM SIE operating within the context of the spiking neural network.

## 5. Autonomous Derivation / Analysis Log

1.  **Reviewed SIE Documentation:** Analyzed `2C_Self_Improvement_Engine.md`.
2.  **Developed Refined Plan:** Outlined phases for modeling, implementation, validation, documentation.
3.  **Implemented Simulator:** Created `simulate_sie_stability.py`.
4.  **Added Features:** Incorporated damping, weight decay, data logging, parameter arguments.
5.  **Ran Baseline Simulation:** Executed the simulator to generate initial data.
6.  **Developed Analysis Script:** Created `analyze_sie_stability_data.py`.
7.  **Performed Preliminary Analysis:** Ran the analysis script on the baseline data.
8.  **Refined Theory:** Added weight decay to model, performed preliminary Lyapunov analysis for $L(W)$, attempted coupled analysis for $L(W,V)$.
9.  **Enhanced Simulator:** Added LIF neuron dynamics and E/I balance.
10. **Ran Parameter Sweeps ($\lambda$, $\eta$):** Tested `lambda_decay` ($\lambda$) and `eta` ($\eta$) with the LIF+E/I simulator. Found high sensitivity to $\lambda$.
11. **Enhanced Simulator:** Added timing-based eligibility trace. Ran simulation. Found weights still collapsed with default $\lambda$.
12. **Enhanced Simulator:** Added synaptic scaling mechanism.
13. **Ran Validation Simulation:** Tested simulator with LIF+E/I+Trace+Scaling.
14. **Analyzed Results:** Confirmed synaptic scaling stabilizes weight norm at non-zero value with default $\lambda$.
15. **Updated Documentation:** Incorporating latest findings below (this update).

## 6. Hierarchical Empirical Validation Results & Analysis (Preliminary)

### 6.1 Experimental Setup

- **Simulator:** `simulate_sie_stability.py` (Version with LIF, E/I balance, timing-trace, synaptic scaling).
- **Parameters:** `NUM_NEURONS=100`, `NUM_CLUSTERS=10`, `SIMULATION_STEPS=10000`, `ETA` ($\eta$)=`0.01`, `GAMMA` ($\gamma$)=`0.9`, `ALPHA` ($\alpha$)=`0.1`, `TARGET_VAR=0.05`, `W_TD=0.5`, `W_NOVELTY=0.2`, `W_HABITUATION=0.1`, `W_SELF_BENEFIT=0.2`, `W_EXTERNAL=0.8`, `LAMBDA` ($\lambda$)=`0.001`.
- **Scenario:** Simplified LIF network activity with E/I balance, random state transitions, periodic external reward (+1.0 every 100 steps), periodic synaptic scaling.

### 6.2 Unit Test Results (Simulator Functionality)

- Simulator runs to completion with all enhancements.
- Data logging (`.npz`) and plotting (`.png`) functions correctly.
- Analysis script loads and processes data.

### 6.3 System Test Results (LIF + E/I + Trace + Scaling)

Based on the analysis of the latest `sie_stability_data_eta0.01_lambda0.001.npz` (run with synaptic scaling):
- **Reward Signal ($R_{\mathrm{total}}$):** Appears stable (Mean=0.0303, StdDev=0.0889).
- **Modulation Factor ($\text{mod\_factor}$):** Appears stable (Mean=0.0148, StdDev=0.0417).
- **Weight Norm ($\|W\|_F$):** Appears stable and bounded at a non-zero value (Start=14.4706, End=14.1981). Synaptic scaling effectively prevented the weight collapse seen previously with $\lambda=0.001$ in the absence of scaling.
- **V(state) ($V(\text{state})$):** Average value function appears to converge (Final 1000 steps StdDev=0.0042).
- **Component Interaction:** Weak positive correlation between Novelty and Self-Benefit (0.0426).

**Analysis:**
- **Synaptic Scaling Effect:** Adding synaptic scaling provides crucial homeostasis, allowing weights to stabilize at a non-zero level even with moderate weight decay ($\lambda=0.001$). This suggests a combination of regularization ($\lambda$) and homeostatic mechanisms (scaling) isfor stability, aligning with FUM design principles.
- **Previous Sweep Context:** The earlier sweeps (LIF+E/I+Trace, *without* scaling) highlighted the system's sensitivity to $\lambda$, with weights collapsing even for small decay values. The addition of scaling fundamentally changes this dynamic, enabling stable non-zero weights.

### 6.4 Performance Results

- Simulation Time (10k steps, 100 neurons, LIF+E/I+Trace+Scaling): ~3.5 seconds.
- Analysis Time: < 1 second.

*(Note: This validation used a simplified simulation environment. Further testing with more realistic dynamics, eligibility traces, and parameter ranges is needed).*

## 7. FUM Integration Assessment (Planned)

- **Component Additions:** Requires integrating the derived stability conditions and potentially adaptive parameter tuning mechanisms (for $\lambda$, scaling targets, etc.) into the core FUM SIE module (`_FUM_Training/src/model/sie.py`) and plasticity modules.
- **Resource Impact:** Stability analysis itself is primarily theoretical. Integration might involve adding parameter checks or adaptive adjustments with minimal computational overhead during runtime. Synaptic scaling adds computational cost (matrix operations).
- **Scaling Considerations:** Stability conditions derived from the model should ideally hold regardless of network size, but empirical validation at scale is necessary. The interaction of scaling and decay needs careful tuning at scale.

## 8. Limitations Regarding Formal Verification

The current work is based on simulation and empirical analysis. Formal mathematical proofs of stability and convergence incorporating all mechanisms (LIF, E/I, decay, scaling, non-linear modulation, TD learning) have not yet been completed and present significant theoretical challenges.

## 9. Limitations & Future Work

- **Simplified Simulation:** Still uses simplified eligibility traces, lacks sparsity constraints, realistic input/task structures, and detailed inhibitory plasticity rules.
- **Limited Parameter Space:** Only default parameters tested with the full simulator including scaling. Extensive parameter sweeps (varying $\lambda$, $\eta$, scaling targets, SIE weights) with the *current* simulator are needed.
- **Lack of Formal Proofs:** Rigorous mathematical derivation of stability conditions for the full system is pending.
- **Cluster Dynamics:** Does not yet model cluster-specific rewards or the dynamic clustering process.

**Future Work:**
1.  **Perform Parameter Sweeps:** Systematically vary $\lambda$, $\eta$, scaling targets, SIE weights ($w_i$), etc., with the current enhanced simulator (LIF+E/I+Trace+Scaling) to map stability boundaries.
2.  **Enhance Simulator:** Implement more realistic eligibility traces (full timing-based STDP) and sparsity constraints.
3.  **Refine Theory:** Revisit Lyapunov analysis (Phase 2) attempting to incorporate scaling and derive conditions, potentially using approximations or focusing on expected value analysis.
4.  **Test Specific Scenarios:** Simulate conditions designed to induce instability or reward hacking.

## 10. References

1.  FUM SIE Documentation: `How_It_Works/2_Core_Architecture_Components/2C_Self_Improvement_Engine.md`
2.  FUM STDP Documentation: `How_It_Works/2_Core_Architecture_Components/2B_Neural_Plasticity.md`
3.  SIE Stability Simulator: `design/Novelty/mathematical_frameworks/SIE_Analysis/Implementation/simulate_sie_stability.py`
4.  SIE Stability Analysis: `design/Novelty/mathematical_frameworks/SIE_Analysis/Implementation/analyze_sie_stability_data.py`
5.  Simulation Data: `design/Novelty/mathematical_frameworks/SIE_Analysis/Validation_Results/sie_stability_data_eta*_lambda*.npz` (Parameter sweep data files)
6.  Simulation Plot: `design/Novelty/mathematical_frameworks/SIE_Analysis/Validation_Results/sie_stability_sim*.png` (Plots from runs)
7.  Parameter Sweep Analysis: Output from `analyze_sie_stability_data.py --sweep` (when run from the Implementation directory).