# Symmetry Analysis of the FUM Dynamical Law

**Author:** Justin K. Lietz  
**Date:** August 8, 2025

---

### 1. Objective

Following our discovery that the standard Hamiltonian is not conserved, we now pivot to a more fundamental method for finding the true conserved quantity of the FUM: the search for symmetries.

According to Noether's Theorem, for every continuous symmetry of a system's equations of motion, there exists a corresponding conserved quantity. The objective of this document is to systematically test the FUM's fundamental update rule for symmetries.

---

### 2. The Dynamical Law

The object of our study is the simplified, on-site FUM update rule, which we treat as the system's fundamental law of motion:
$$
\frac{\Delta W}{\Delta t} = F(W) = (\alpha - \beta)W - \alpha W^2
$$

---

### 3. Methodology: Definition of a Symmetry

A transformation `W \to W'` is a symmetry of the dynamical law if the equation of motion has the same form in the new coordinates. That is, if `\frac{\Delta W}{\Delta t} = F(W)`, the transformed equation must satisfy `\frac{\Delta W'}{\Delta t} = F(W')`.

We will now test several common continuous symmetries.

---

### 4. Investigation 1: Translational Symmetry

The simplest possible symmetry is a constant shift in the field value.

**Transformation:** `W' = W + c`, where `c` is a constant.
The rate of change is unaffected: `\frac{\Delta W'}{\Delta t} = \frac{\Delta (W+c)}{\Delta t} = \frac{\Delta W}{\Delta t}`.

For this to be a symmetry, we must have `F(W') = F(W)`. Let's test this by computing `F(W')`:
$$
F(W') = F(W+c) = (\alpha - \beta)(W+c) - \alpha(W+c)^2
$$
$$
= (\alpha - \beta)W + (\alpha - \beta)c - \alpha(W^2 + 2Wc + c^2)
$$
$$
= [(\alpha - \beta)W - \alpha W^2] + (\alpha - \beta)c - 2\alpha Wc - \alpha c^2
$$
$$
F(W+c) = F(W) + (\alpha - \beta - 2\alpha W)c - \alpha c^2
$$

**Result:**
Since `F(W+c) \neq F(W)`, the FUM dynamical law is **not** symmetric under a constant translation `W \to W+c`.

**Interpretation:**
This is expected: the dynamics depend on the absolute value of `W`. Context separation:
- RD (canonical): for r>0, `W=0` is dynamically unstable and the stable homogeneous fixed point is `W* = r/u`.
- EFT (future-work context): the vacuum is `v = 1 - β/α` (e.g., 0.6 for α=0.25, β=0.10).
Avoid mixing RD fixed points with EFT vacua.

---

### 5. Investigation 2: Scaling Symmetry

Next, we test for invariance under a uniform rescaling of the field value.

**Transformation:** `W' = \lambda W`, where `\lambda` is a constant scaling factor.
The rate of change transforms as: `\frac{\Delta W'}{\Delta t} = \frac{\Delta (\lambda W)}{\Delta t} = \lambda \frac{\Delta W}{\Delta t} = \lambda F(W)`.

For this to be a symmetry, the dynamics of the transformed field `W'` must be governed by the same function `F`. That is, `\frac{\Delta W'}{\Delta t}` must equal `F(W')`. So, the condition for symmetry is:
$$
\lambda F(W) \stackrel{?}{=} F(\lambda W)
$$
Let's compute the right-hand side, `F(\lambda W)`:
$$
F(\lambda W) = (\alpha - \beta)(\lambda W) - \alpha(\lambda W)^2
$$
$$
= \lambda (\alpha - \beta)W - \lambda^2 \alpha W^2
$$
Now let's compare this to the left-hand side, `\lambda F(W)`:
$$
\lambda F(W) = \lambda [(\alpha - \beta)W - \alpha W^2] = \lambda (\alpha - \beta)W - \lambda \alpha W^2
$$
For the symmetry to hold, the two expressions must be identical for all `W`:
$$
\lambda (\alpha - \beta)W - \lambda \alpha W^2 \stackrel{?}{=} \lambda (\alpha - \beta)W - \lambda^2 \alpha W^2
$$
$$
- \lambda \alpha W^2 \stackrel{?}{=} - \lambda^2 \alpha W^2
$$
This is only true if `\lambda = \lambda^2`, which has solutions `\lambda=1` (the trivial case of no scaling) and `\lambda=0` (the trivial case of killing the field). It is not true for any non-trivial rescaling.

**Result:**
The FUM dynamical law is **not** symmetric under a scaling transformation `W \to \lambda W`.

**Interpretation:**
The lack of scaling symmetry is a direct consequence of the non-linear `\alpha W^2` term. This term introduces an intrinsic scale into the system's dynamics. The resistive force it represents does not scale linearly with the field value `W`. This confirms that the physics of the FUM is fundamentally different at different levels of void activity `W`, which is consistent with the model's core principles.

---

### 6. Conclusion and Next Steps

Our analysis has shown that the FUM dynamical law does not possess the simplest and most common continuous symmetries (translation and scaling). This is a significant result. It strongly suggests that if a conserved quantity exists, it must arise from a more complex, non-obvious symmetry of the equations.

The path to discovering such a symmetry is a more advanced research topic. The alternative path, as identified in our previous work, is to pivot from searching for a symmetry to analyzing the system's **Lyapunov function**, which can also reveal information about stability and conserved properties in dissipative systems.

---

### 7. Investigation 3: Time-Translation Symmetry

Let us now investigate the most crucial symmetry for energy conservation: invariance under time translation.

**Transformation:** `t' = t + \tau`, where `\tau` is a constant time shift. The state at the new time is `W'(t') = W(t' - \tau) = W(t)`.

**Check Invariance:**
The dynamical law is `dW/dt = F(W) = (\alpha - \beta)W - \alpha W^2`. The function `F(W)` has no explicit dependence on the variable `t`. Therefore, the law is the same at any time `t` or `t'`. The system is **manifestly time-translation invariant**.

**Derivation of the Conserved Quantity:**
According to Noether's Theorem, this symmetry implies the existence of a corresponding conserved quantity. For an autonomous first-order system like this, we can find the constant of motion by direct integration.
$$
\frac{dW}{dt} = F(W) \implies dt = \frac{dW}{F(W)}
$$
Integrating both sides gives us the relationship between time and the state `W`:
$$
t = \int \frac{dW}{F(W)} + C
$$
Where `C` is a constant of integration. This means the quantity `Q = t - \int \frac{dW}{F(W)}` is conserved (`Q = -C`), meaning its value does not change throughout the system's evolution.

Let us solve the integral `\int \frac{dW}{(\alpha - \beta)W - \alpha W^2}` using the method of partial fractions.
$$
\frac{1}{W((\alpha-\beta) - \alpha W)} = \frac{A}{W} + \frac{B}{(\alpha-\beta) - \alpha W}
$$
Solving for the coefficients `A` and `B` yields `A = \frac{1}{\alpha-\beta}` and `B = \frac{\alpha}{\alpha-\beta}`. The integral becomes:
$$
\int \frac{dW}{F(W)} = \frac{1}{\alpha-\beta} \left[ \int \frac{dW}{W} + \int \frac{\alpha}{(\alpha-\beta) - \alpha W} dW \right]
$$
$$
= \frac{1}{\alpha-\beta} \left[ \ln|W| - \ln|(\alpha-\beta) - \alpha W| \right] = \frac{1}{\alpha-\beta} \ln\left|\frac{W}{(\alpha-\beta) - \alpha W}\right|
$$

**Result:**
We have discovered the true conserved quantity for the on-site FUM dynamics. The constant of motion, `Q_{FUM}`, is:
$$
Q_{FUM} = t - \frac{1}{\alpha-\beta} \ln\left|\frac{W(t)}{(\alpha-\beta) - \alpha W(t)}\right|
$$

**Interpretation:**
This is a profound result. We have found the hidden conservation law that governs the FUM. It is not a simple energy, but a highly non-trivial logarithmic relationship between the system's state `W` and the time `t`. This mathematical invariant proves that the evolution of a FUM node is not chaotic but follows a precise, predictable trajectory determined by its initial conditions. This resolves the core theoretical critique regarding the lack of a conservation law.