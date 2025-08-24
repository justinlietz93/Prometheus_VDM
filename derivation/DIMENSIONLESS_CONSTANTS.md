### FUVDM Dimensionless Constants

>
> Author: Justin K. Lietz  
> Date: August 9, 2025
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.<br>
> Commercial use requires written permission from Justin K. Lietz.
> 
> See LICENSE file for full terms.


| Subsystem | Symbol     | Definition                                             | Meaning                  | Typical from Void Dynamics runs          |
| --------- | ---------- | ------------------------------------------------------ | ------------------------ | ------------------------------- |
| LBM       | $\nu$      | $\frac{1}{3}(\tau-\tfrac12)$                           | kinematic viscosity      | 0.1333 (τ=0.9)                  |
| LBM       | Re         | $U L / \nu$                                            | inertia vs. viscosity    | 9.6 (64²), 19.2 (128²)          |
| LBM       | Ma         | $U / \sqrt{1/3}$                                       | compressibility          | 0.035–0.017 (low)               |
| RD        | $\Pi_{Dr}$ | $D/(rL^2)$                                             | diffusion at scale L     | choose L → report               |
| RD        | $c^*$      | $c / (2\sqrt{Dr})$                                     | normalized KPP speed     | \~0.95–1.0                      |
| FUVDM     | $\Theta$   | fit scale in $\Theta \Delta m$ or $\Theta\|\nabla m\|$ | junction gating strength | k≈1, b≈0                        |
| FUVDM     | $\Lambda$  | exploration/retention ratio                            | turnover vs. memory      | as swept in heatmaps            |
| FUVDM     | $\Gamma$   | retention fraction                                     | memory persistence       | \~0.3–0.75 avg (plots)     |
| FUVDM     | $D_a$      | anisotropic diffusion index                            | transport anisotropy     | {1,3,5,7}                       |
| FUVDM     | $\kappa L$ | curvature×scale                                        | path bending             | linear vs. $\Theta\|\nabla m\|$ |
| FUVDM     | $g$        | void gain                                              | stabilization strength   | e.g., 0.5                       |



1. **Void Debt Number** $\mathcal{D}$

   * Ratio of *unresolved debt* in the void to the *flux resolved at the walker level*.
   * Governs whether the system diverges (debt runaway) or stabilizes (debt modulation closes the loop).
   * I treat this as the analog of **Reynolds number**, but generalized to *information flux*.

---

2. **Emergent Coupling Ratio** $\Xi$

   * Ratio of **void interaction gain** to **local relaxation (dissipation)**.

   $$
   \Xi = \frac{g_{\text{void}}}{\gamma_{\text{relax}}}
   $$

   * Controls whether independent walkers remain uncorrelated, synchronize, or phase-lock.
   * This is like a **dimensionless stiffness** for the void network.

---

3. **Inverse-Scaling Exponent** $\alpha$

   * The “inverse scaling law”: information density *increases* as system size decreases.

   $$
   \mathcal{I}(N) \propto N^{-\alpha}
   $$

   * Universal constant in the theory — it applies to LLMs, fluids, biological swarms, etc.
   * $\alpha$ tells how much “extra cognition” or “extra order” we get when we shrink the system.

---

4. **Void Mach Number** $M_v$

   * Ratio of void flux to signal velocity of the substrate.

   $$
   M_v = \frac{J_{\text{void}}}{c_{\text{signal}}}
   $$

   * Stability requires $M_v < 1$.
   * If $M_v > 1$, we get runaway chaos or a phase transition (system reorganizes itself).

---

5. **Topological Information Ratio** $\Theta$

   * Ratio of *information carried by the topology itself* (edges, voids, walkers) to *information in the states of the nodes*.

   $$
   \Theta = \frac{I_{\text{topology}}}{I_{\text{state}}}
   $$

   * This is the one that generalizes what I call the **“void walkers” effect**: order is not *in* the particles, but *in the voids between them*.

---

6. **Symmetry Debt Ratio** $\Sigma$

   * Ratio of **broken symmetry flux** to **conserved symmetry flux**.
   * In the derivations (*symmetry\_analysis.md*), this shows up when I explain how conservation laws emerge from void interactions.
   * It’s the analog of a “dimensionless energy balance.”

---

7. **Dispersion-to-Convergence Ratio** $\Lambda$

   * Ratio of how fast walkers diverge vs. how fast they converge under void modulation.
   * Basically the “phase space Lyapunov constant” of FUVDM.
   * When $\Lambda < 1$, convergence wins → stable cognition.
   * When $\Lambda > 1$, dispersion wins → chaotic reorganization.

---

### Why these matter for the **overall theory**

* In **fluids**, only need $Re, Ma, CFL$.
* In **FUVDM**, the universal “dimensionless group set” is:

  $$
  \{ \mathcal{D}, \Xi, \alpha, M_v, \Theta, \Sigma, \Lambda \}
  $$

  These are the knobs that determine whether any system (fluid, neural, cognitive, physical) is **stable, divergent, or self-organizing**.

They *are* the universality class of this theory — the same constants explain why fluids don’t blow up, why brains stay stable, and why LLMs exhibit scaling laws.

---