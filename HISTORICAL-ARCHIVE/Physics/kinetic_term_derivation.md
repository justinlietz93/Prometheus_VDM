# Derivation of the FUM Kinetic Term

**Author:** Justin K. Lietz  
**Date:** August 8, 2025

---

### 1. Objective

As outlined in our Effective Field Theory (EFT) roadmap, we must rigorously derive the coefficients of the general Lagrangian from the underlying discrete FUM simulation. Our previous work derived the leading-order potential term, `V(\phi)`. The next most dominant term is the kinetic term, `\mathcal{L}_K = Z(\phi)(\partial_\mu \phi)^2`.

The objective of this proof is to formally derive the coefficient `Z(\phi)` and demonstrate that it is a constant (`Z(\phi) = 1/2`), as required for a standard Klein-Gordon field. We will analyze the temporal `(\partial_t \phi)^2` and spatial `(\nabla \phi)^2` components separately.

---

### 2. The Temporal Kinetic Term

The temporal part of the kinetic term, which relates to the change of the field in time, arises from the "kinetic energy" term in our postulated discrete Hamiltonian.

In `derivation/discrete_conservation.md`, we defined the kinetic energy at a node `i` as:
$$
\mathcal{K}_i = \frac{1}{2}\left(\frac{dW_i}{dt}\right)^2
$$
Here, `\frac{dW_i}{dt}` is the discrete difference `\frac{W_i(t+\Delta t) - W_i(t)}{\Delta t}`.

To find the contribution to the continuum Lagrangian density, we take the continuum limit (`W_i \to \phi(x)` and `\frac{dW_i}{dt} \to \frac{\partial \phi}{\partial t}`):
$$
\mathcal{L}_{\text{Kinetic, Temporal}} = \lim_{\text{continuum}} \mathcal{K}_i = \frac{1}{2}\left(\frac{\partial \phi}{\partial t}\right)^2
$$
This is a direct and encouraging result. It shows that the coefficient for the `(\partial_t \phi)^2` part of the kinetic term is indeed a constant, `1/2`.

---

### 3. The Spatial Kinetic Term

The spatial part of the kinetic term arises from the **interaction energy** between neighboring nodes, which we defined in the discrete Hamiltonian as:
$$
\mathcal{I}_i = \frac{1}{2} \sum_{j \in N(i)} J (W_j - W_i)^2
$$
This term penalizes differences in the state of adjacent nodes. Intuitively, a smooth field where neighbors have similar states has low energy, while a rapidly changing field has high energy. This "gradient energy" is the source of the spatial kinetic term `(\nabla \phi)^2`.

**Next Step:**

Our task is now to take the continuum limit of this interaction term. We will do this by performing a Taylor series expansion on `W_j` around the position of node `i`, summing over all neighbors, and showing that the leading-order result is proportional to `(\nabla \phi)^2`.

#### 3.1 The Continuum Limit of the Interaction Term

To perform the derivation, we will approximate the k-NN graph as a regular, 3-dimensional cubic lattice with lattice spacing `a`. A node `i` is at position `\vec{x}`, and its nearest neighbors `j` are at positions `\vec{x} \pm a\hat{k}` where `\hat{k}` is a unit vector in the `x, y,` or `z` direction.

We expand the state `W_j` of a neighbor in a Taylor series around the position `\vec{x}`:
$$
W_j = W(\vec{x} + a\hat{k}) \approx W(\vec{x}) + a (\hat{k} \cdot \nabla)W(\vec{x}) + \frac{a^2}{2}(\hat{k} \cdot \nabla)^2 W(\vec{x})
$$
The difference `(W_j - W_i)` is then:
$$
(W_j - W_i) \approx a \frac{\partial W}{\partial k} + \frac{a^2}{2} \frac{\partial^2 W}{\partial k^2}
$$
Squaring this and keeping only the lowest order term in `a` (which is `a^2`), we get:
$$
(W_j - W_i)^2 \approx a^2 \left( \frac{\partial W}{\partial k} \right)^2
$$
Now, we sum this over all neighbors. For a cubic lattice, there are 6 neighbors (pairs in the `\pm x`, `\pm y`, `\pm z` directions). The sum is:
$$
\sum_{j \in N(i)} (W_j - W_i)^2 \approx \sum_{k \in \{x,y,z\}} \left[ a^2\left(\frac{\partial W}{\partial k}\right)^2 + a^2\left(\frac{\partial W}{\partial (-k)}\right)^2 \right] = 2a^2 \sum_{k \in \{x,y,z\}} \left(\frac{\partial W}{\partial k}\right)^2
$$
This sum is simply the squared norm of the gradient vector:
$$
\sum_{j \in N(i)} (W_j - W_i)^2 \approx 2a^2 (\nabla W)^2
$$
Substituting this back into the interaction energy expression and taking the continuum limit `W \to \phi`:
$$
\mathcal{I} \approx \frac{1}{2} J (2a^2 (\nabla \phi)^2) = J a^2 (\nabla \phi)^2
$$
This is the Lagrangian density for the spatial part of the kinetic term.

---

### 3.2 Variational derivation from a discrete action (self‑contained)

We now derive the second‑order dynamics directly from a discrete action, which subsumes both the temporal and spatial kinetic terms and fixes the normalization without assumptions.

- Spatial lattice: cubic, spacing `a`, spatial dimension `d` (use `d=3` in practice)  
- Time step: `Δt`; sites indexed by `i`, times by `n` with `t_n = n Δt`  
- Site field: `W_i^n ≡ W(𝐱_i, t_n)`; neighbor directions `μ ∈ {1,…,d}` with unit vectors `ê_μ`

Discrete Lagrangian (per time step):
$$
L^n \;=\; a^d \sum_i\Bigg[
\frac{1}{2}\Big(\frac{W_i^{\,n+1}-W_i^{\,n}}{\Delta t}\Big)^2
\;-\; \frac{\kappa}{2}\sum_{\mu=1}^d\big(W_{i+\mu}^{\,n}-W_i^{\,n}\big)^2
\;-\; V\!\big(W_i^{\,n}\big)
\Bigg].
$$

Discrete Euler-Lagrange (central in time):
$$
\frac{W_i^{\,n+1}-2W_i^{\,n}+W_i^{\,n-1}}{(\Delta t)^2}
\;-\;\kappa\,\sum_{\mu=1}^d \big(W_{i+\mu}^{\,n}+W_{i-\mu}^{\,n}-2W_i^{\,n}\big)
\;+\;V'\!\big(W_i^{\,n}\big)=0.
$$

Continuum limit (`W_i^n \approx \phi(\mathbf{x}_i,t_n)`, `Δt→0`, `a→0`), using
`W_{i+\mu}+W_{i-\mu}-2W_i = a^2 ∂_\mu^2 \phi + O(a^4)`:
$$
\partial_t^2\phi \;-\; \kappa a^2 \nabla^2\phi \;+\; V'(\phi)=0,
$$
which follows from the continuum Lagrangian density
$$
\mathcal{L} \;=\; \frac{1}{2}(\partial_t\phi)^2 \;-\; \frac{\kappa a^2}{2}(\nabla\phi)^2 \;-\; V(\phi).
$$

Edge‑counting conventions:
- Per‑edge coupling `κ` (each undirected edge counted once) gives `c^2 = κ a^2`.
- Per‑site coupling with both `±μ` neighbors, `\frac{1}{2}\sum_{j\in N(i)} J (W_j-W_i)^2`, corresponds to `κ = 2J`, hence `c^2 = 2 J a^2`.

This variational derivation replaces any need to “promote to second order” by hand and makes the normalization and propagation speed explicit.
### 4. Assembling the Full Kinetic Term and Conclusion

We can now assemble the full kinetic Lagrangian density, `\mathcal{L}_K = \mathcal{L}_{\text{Kinetic, Temporal}} - \mathcal{L}_{\text{Kinetic, Spatial}}`. The minus sign is required for the signature of the Minkowski metric (`+---`).

$$
\mathcal{L}_K = \frac{1}{2}\left(\frac{\partial \phi}{\partial t}\right)^2 - J a^2 (\nabla \phi)^2
$$
Equivalently, compare to the standard relativistic form `\frac{1}{2}(\partial_\mu \phi)^2 = \frac{1}{2}\left( (\frac{\partial \phi}{\partial t})^2 - (\nabla \phi)^2 \right)` by defining the propagation speed
$$
c^2 \equiv 2\,J\,a^2,
$$
so the Euler-Lagrange equation carries `\partial_t^2\phi - c^2 \nabla^2 \phi + V'(\phi)=0`. One may set `c=1` by a benign rescaling of units (choose `\Delta t` and `a`, or equivalently `\tau` and `a` in the physical map); there is no need to hard‑wire a relation between `J` and `a`.

Note on edge‑counting conventions: if instead you count undirected edges once via a per‑edge coupling `\kappa`, the spatial term is `( \kappa / 2 ) \sum_\mu (W_{i+\mu}-W_i)^2` and the continuum prefactor is `\kappa a^2`; identifying `\kappa = 2J` gives `c^2=\kappa a^2 = 2 J a^2`.
**Conclusion:** We have successfully derived the full kinetic term from the discrete Hamiltonian. The derivation confirms that the kinetic term coefficient, `Z(\phi)`, is a constant and not a function of the field `\phi`. This is a successful and crucial step in formalizing the FUM.

**Note.** There is no microscopic constraint tying `J` to `a`. The continuum limit yields
`𝓛_K = ½(∂_t φ)^2 - J a^2 (∇φ)^2` and the wave speed `c^2 = 2 J a^2` (or `c^2 = κ a^2` with `κ = 2J`). One may set `c = 1` by a benign rescaling of time/length units (choose `Δt` and `a`, or equivalently `τ` and `a` in the physical map); this is a units choice, not a constraint.