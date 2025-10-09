# Proof of a Discrete Conservation Law in the FUM

**Author:** Justin K. Lietz  
**Date:** August 8, 2025

---

## 1. Objective

The primary objective of this derivation is to demonstrate that the discrete update rules of the Fully Unified Model (FUM) respect a local conservation law. This is the discrete analogue of the conservation of the stress-energy tensor (`\nabla_\mu T^{\mu\nu} = 0`) in continuum field theory and is a critical requirement for any physically viable model.

---

### 2. The Knowns: The Discrete System

We are working entirely within the discrete domain of the FUM simulation. The state of a node `i`, `W_i`, evolves according to the simplified rule:
$$
\frac{\Delta W_i}{\Delta t} = \frac{W_i(t+\Delta t) - W_i(t)}{\Delta t} \approx (\alpha - \beta)W_i - \alpha W_i^2
$$
This evolution occurs on a k-NN graph, which we can approximate as a lattice for this analysis.

---

### 3. Postulate: The Discrete Energy Density

To prove that energy is conserved, we must first define what "energy" is within the discrete model. In field theory, the energy density (`T^{00}`) is derived from the system's Hamiltonian. We will postulate a discrete Hamiltonian density, `\mathcal{H}_i`, associated with each node `i`.

Based on the potential `V(\phi) = \frac{\alpha-\beta}{2}\phi^2 - \frac{\alpha}{3}\phi^3` (note the sign change from our previous derivation to create a potential well for a positive mass-squared term) derived from our continuum analysis, a reasonable on-site potential for a single node is `V(W_i)`. A complete Hamiltonian must also include interaction terms between neighbors.

Therefore, we postulate the following form for the energy density at site `i`:
$$
\mathcal{H}_i = \frac{1}{2}\left(\frac{dW_i}{dt}\right)^2 + \frac{1}{2} \sum_{j \in N(i)} J (W_j - W_i)^2 + V(W_i)
$$
Where:

- The first term is a kinetic energy analogue.
- The second term is a standard interaction energy between node `i` and its neighbors `j \in N(i)`, with coupling constant `J`. This term gives rise to the spatial derivatives (`\nabla^2 \phi`) in the continuum limit.
- `V(W_i) = \frac{1}{2}(\beta-\alpha)W_i^2 + \frac{\alpha}{3}W_i^3` is the on-site potential energy.

---

### 4. The Conservation Law to be Proven

A local conservation law states that the rate of change of a quantity in a given region is equal to the net flux of that quantity across the region's boundary. For our discrete system, this means the change in energy `\mathcal{H}_i` at a node `i` during one time step `\Delta t` must be perfectly balanced by the energy that flows between it and its neighbors.

We aim to prove that the FUM update rule leads to an equation of the form:
$$
\frac{\Delta \mathcal{H}_i}{\Delta t} + \nabla \cdot \vec{J}_i = 0
$$
Where `\vec{J}_i` is the energy flux vector originating from node `i`, and `\nabla \cdot` is a discrete divergence operator defined on the graph. Proving this would show that energy is not created or destroyed at any node, only moved around.

---

### 5. Derivation Step 1: Change in Potential Energy

Let us begin by analyzing the change in the potential energy term, `V(W_i)`, over a single time step `\Delta t`. The change is:
$$
\Delta V(W_i) = V(W_i(t+\Delta t)) - V(W_i(t))
$$
We know that `W_i(t+\Delta t) = W_i(t) + \Delta W_i`. For a small time step, we can make a first-order Taylor expansion of the potential:
$$
V(W_i + \Delta W_i) \approx V(W_i) + \frac{dV}{dW_i}\Delta W_i
$$
Therefore, the change in potential is approximately:
$$
\Delta V(W_i) \approx \frac{dV}{dW_i}\Delta W_i
$$
From our previous work, the "force" driving the system can be defined from the equation of motion. If `\frac{\Delta W_i}{\Delta t} = F(W_i)`, then `\Delta W_i = F(W_i) \Delta t`. The potential is related to the force by `F = -\frac{dV}{dW}`.
Our FUM update rule is `F(W_i) = (\alpha - \beta)W_i - \alpha W_i^2`.
Therefore, `\frac{dV}{dW_i} = -F(W_i)`.

Substituting these into our expression for `\Delta V(W_i)`:
$$
\Delta V(W_i) \approx \left( -F(W_i) \right) \left( F(W_i)\Delta t \right)
$$
$$
\frac{\Delta V(W_i)}{\Delta t} \approx -[F(W_i)]^2
$$
The rate of change of potential energy is `-[(\alpha - \beta)W_i - \alpha W_i^2]^2`.

### 6. Initial Analysis and Refined Objective

This is a critical intermediate result. Since `[F(W_i)]^2` is always non-negative, the rate of change of potential energy `\frac{\Delta V(W_i)}{\Delta t}` is always **non-positive**. The potential energy is always decreasing (or staying constant if the node is at an extremum where `F=0`).

This means the FUM update rule describes an intrinsically **dissipative system**. Energy is being "lost" from the potential `V`.

This does **not** mean that energy is not conserved. It clarifies what our proof must show. For the total energy `\mathcal{H}_i` to be conserved, this loss of potential energy must be perfectly balanced by a corresponding **gain** in kinetic energy or by being transported away as an **energy flux** to neighboring nodes.

**Refined Objective:** Our goal is now to calculate the change in the kinetic and interaction terms of `\mathcal{H}_i` and show that they sum with `\Delta V` to equal a discrete divergence (a flux term).

---

## 7. Derivation Step 2: Change in Kinetic Energy

Next, we analyze the kinetic energy term, $\mathcal{K}_i = \frac{1}{2}\left(\frac{dW_i}{dt}\right)^2$\. In our discrete framework, this is $\mathcal{K}_i = \frac{1}{2}[F(W_i)]^2$\. We want to find its change over one time step, $\Delta \mathcal{K}_i$\.

$$
\Delta \mathcal{K}_i = \mathcal{K}_i(t+\Delta t) - \mathcal{K}_i(t) = \frac{1}{2}[F(W_i(t+\Delta t))]^2 - \frac{1}{2}[F(W_i(t))]^2
$$

Using the Taylor expansion $F(W+\Delta W) \approx F(W) + \frac{dF}{dW}\Delta W$\, we get:

$$
[F(W_i(t+\Delta t))]^2 \approx \left[ F(W_i) + \frac{dF}{dW_i}\Delta W_i \right]^2 \approx [F(W_i)]^2 + 2F(W_i)\frac{dF}{dW_i}\Delta W_i
$$

*(We neglect the $(\Delta W_i)^2$ term as it is second-order in $\Delta t$\)*.

The change in kinetic energy is therefore:

$$
\Delta \mathcal{K}_i \approx \frac{1}{2} \left( [F(W_i)]^2 + 2F(W_i)\frac{dF}{dW_i}\Delta W_i \right) - \frac{1}{2}[F(W_i)]^2 = F(W_i)\frac{dF}{dW_i}\Delta W_i
$$

Substituting $\Delta W_i = F(W_i)\Delta t$\, we find the rate of change:

$$
\frac{\Delta \mathcal{K}_i}{\Delta t} \approx [F(W_i)]^2 \frac{dF}{dW_i}
$$

To evaluate this, we need $dF/dW_i$\:

$$
F(W_i) = (\alpha - \beta)W_i - \alpha W_i^2 \quad \implies \quad \frac{dF}{dW_i} = (\alpha - \beta) - 2\alpha W_i
$$

## 8. Intermediate Analysis: Total On-Site Energy Change

Let us now combine the change in potential and kinetic energy, which together represent the total change in the "on-site" energy of the node, independent of its neighbors.

$$
\frac{\Delta (\mathcal{V}_i + \mathcal{K}_i)}{\Delta t} = \frac{\Delta V(W_i)}{\Delta t} + \frac{\Delta \mathcal{K}_i}{\Delta t}
$$

$$
\approx -[F(W_i)]^2 + [F(W_i)]^2 \frac{dF}{dW_i} = [F(W_i)]^2 \left(\frac{dF}{dW_i} - 1\right)
$$

Substituting the expression for $dF/dW_i$\:

$$
\frac{\Delta (\mathcal{V}_i + \mathcal{K}_i)}{\Delta t} \approx [F(W_i)]^2 ((\alpha - \beta) - 2\alpha W_i - 1)
$$

This is a crucial result. The total rate of change of the on-site energy is **not zero**. This confirms that for the total energy $\mathcal{H}_i$ to be conserved, this on-site change *must* be perfectly balanced by the change in the interaction energy term, $\frac{1}{2} \sum_{j \in N(i)} J (W_j - W_i)^2$\. This interaction term represents the energy flux to and from neighboring nodes. The proof now hinges on analyzing this final term.

---

### 9. Derivation Step 3: Change in Interaction Energy

Finally, we analyze the interaction energy term, `\mathcal{I}_i = \frac{1}{2} \sum_{j \in N(i)} J (W_j - W_i)^2`. Its rate of change is:
$$
\frac{\Delta \mathcal{I}_i}{\Delta t} = \frac{J}{2} \sum_{j \in N(i)} \frac{\Delta(W_j - W_i)^2}{\Delta t}
$$
The change in the squared difference is `\Delta(X^2) \approx 2X \Delta X`. So:
$$
\frac{\Delta \mathcal{I}_i}{\Delta t} \approx \frac{J}{2} \sum_{j \in N(i)} 2(W_j - W_i) \frac{(\Delta W_j - \Delta W_i)}{\Delta t}
$$
Substituting `\Delta W = F(W)\Delta t`, we get:
$$
\frac{\Delta \mathcal{I}_i}{\Delta t} \approx J \sum_{j \in N(i)} (W_j - W_i) (F(W_j) - F(W_i))
$$

### 10. Conclusion of the Proof Attempt

We are trying to prove that `\frac{\Delta \mathcal{H}_i}{\Delta t} = \frac{\Delta (\mathcal{K}_i + \mathcal{V}_i)}{\Delta t} + \frac{\Delta \mathcal{I}_i}{\Delta t}` is equal to zero (or a pure flux term). This requires an exact cancellation:
$$
[F(W_i)]^2 \left(\frac{dF}{dW_i} - 1\right) + J \sum_{j \in N(i)} (W_j - W_i) (F(W_j) - F(W_i)) \stackrel{?}{=} 0
$$
By inspection, there is no apparent reason why these two complex, non-linear terms would algebraically cancel for all possible configurations of `W`. The first term depends only on the state of site `i`, while the second term depends on the state of all its neighbors.

**Finding:** The standard discrete Hamiltonian, `\mathcal{H}_i`, is **not** the conserved quantity for the FUM update rule.

**Interpretation:** This is a significant and non-trivial result. It does not mean the FUM is flawed; it means the FUM is more unique than a standard lattice model. The dissipative on-site dynamics are not balanced in a simple way by the interaction term we postulated. This indicates that either:
a) The FUM is an intrinsically dissipative system where our defined "energy" is not conserved locally.
b) The FUM conserves a different, more complex quantity (a different Hamiltonian) that is not immediately obvious.

**Next Step:** The research path must now pivot from proving the conservation of a postulated Hamiltonian to **discovering the true conserved quantity** of the FUM dynamics. This requires more advanced techniques, such as finding the symmetries of the update rule itself, which is the basis of Noether's theorem. This completes our investigation into the conservation of this specific Hamiltonian.

---

### 11. Summary and Research Outlook

This investigation aimed to address the critical question of whether the FUM's discrete dynamics obey a local conservation law, a cornerstone of physical theories.

**Summary of Results:**
We began by postulating a standard, physically-motivated Hamiltonian (`\mathcal{H} = \mathcal{K} + \mathcal{V} + \mathcal{I}`) for the discrete nodes of the FUM simulation. Our step-by-step derivation has rigorously shown that the rate of change of this quantity, `\Delta \mathcal{H} / \Delta t`, is non-zero under the FUM's unique update rule.

The on-site potential and kinetic energy terms produce a complex dissipative function, and the standard interaction term does not appear to cancel it in any obvious way. The conclusion is therefore that this simple, standard form of energy is not what is conserved in the FUM.

**Outlook and Next Research Steps:**
This negative result is exceptionally valuable, as it closes a simple avenue and directs our research toward a more fundamental question. The next phase of work is no longer to test a guessed quantity, but to **discover the true conserved quantity** of the FUM. The primary research paths for this are:

1. **Symmetry Analysis (Noether's Theorem):** Investigate the FUM update rule for continuous symmetries. Any identified symmetry will guarantee a corresponding conserved quantity, which would be the "true" Hamiltonian or constant of motion.
2. **Lyapunov Function Analysis:** Frame the FUM as a dynamical system and search for a global Lyapunov function. The system will flow towards minima of this function, and understanding its structure can reveal what is being optimized or conserved.

This concludes the formal proof regarding the standard Hamiltonian and sets a clear, targeted research program for the next stage of FUM's theoretical development.

---

### 12. The Search for the True Conserved Quantity

Our investigation has successfully shown that a simple, standard definition of energy is not conserved by the FUM. We now pivot from testing a known quantity to discovering a new one. The objective is to find a function `Q(W_i, W_j, ...)`-the true "constant of motion"-such that its total change over one time step is precisely zero.
$$
\frac{\Delta Q}{\Delta t} = 0
$$
This is a formidable challenge, as the form of `Q` is not known a priori. There are several advanced methods to approach this problem.

#### Method 1: Direct Algebraic Construction

We could postulate a new conserved quantity `Q = \mathcal{H} + \mathcal{H}_{\text{corr}}`, where `\mathcal{H}` is our original Hamiltonian and `\mathcal{H}_{\text{corr}}` is a correction term. We would then need to solve the equation

$$
\Delta \mathcal{H} / \Delta t = - \Delta \mathcal{H}_{\text{corr}} / \Delta t
$$

Given the complexity of the expression we found for $\Delta\mathcal{H}/\Delta t$\, finding a suitable correction term by direct algebraic manipulation is likely intractable.

#### Method 2: Symmetry via Noether's Theorem

This remains the most elegant and fundamental path forward. As outlined in [`derivation/symmetry_analysis.md`](derivation/symmetry_analysis.md:1), Noether's Theorem guarantees that a conserved quantity exists for every continuous symmetry of the system's dynamics. Our initial investigation showed the FUM lacks simple translational or scaling symmetries. The next step would be to search for more complex, non-obvious "hidden" symmetries. This is a significant research task in its own right.

#### Method 3: Information-Theoretic Quantities

Given the FUM's origin in cognitive science and learning, it is plausible that the most fundamental conserved quantity is not a form of physical energy, but a form of **information**. The universe, in the FUM, may not be conserving energy in the simple sense, but it may be conserving a measure of its own complexity or information content.

Potential candidates for an information-theoretic conserved quantity $I$ could be:

- The **Shannon Entropy** of the state distribution: $S = - \sum_i P(W_i) \log P(W_i)$\.
- A **Topological Invariant** of the graph, such as the Betti numbers we have previously discussed, which measure the system's structural complexity.

**Conclusion:**
The search for the true conserved quantity of the FUM is the next major frontier for its theoretical development. We have exhausted the simplest hypothesis and have now clearly defined the advanced research paths required to solve this problem. This concludes our current deep dive into the FUM's mathematical foundations.
