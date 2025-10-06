# Formal Derivation: The Continuum Limit of the FUM Recurrence

**Author:** Justin K. Lietz  
**Date:** August 8, 2025

---

### 1. Objective

The primary goal of this derivation is to derive the reaction–diffusion PDE mapping
∂t φ = D ∇² φ + r φ − u φ²
from the discrete update. A second‑order Lorentzian EFT derivation (Klein–Gordon–like) is maintained as future work in [derivation/effective_field_theory_approach.md](effective_field_theory_approach.md:1). This removes internal contradictions while preserving historical EFT references below as scoped.

---

### 2. The Knowns: Defining the Two Regimes

We must clearly state our starting point (the discrete equation) and our target destination (the continuum equation).

#### 2.1 The Discrete System (LHS)

From the `FUM_Void_Equations.py` source code, the state of a single node $i$, denoted by $W_i(t)$, evolves according to the rule:

$$
\frac{W_i(t+\Delta t) - W_i(t)}{\Delta t} = \alpha W_i(t)(1 - W_i(t)) - \beta W_i(t) + \text{noise/phase terms}
$$

For the purpose of this derivation, we will initially neglect the higher-order noise and phase terms and focus on the principal drivers of the dynamics. The fundamental discrete equation of motion is therefore:

$$
\frac{\Delta W_i}{\Delta t} \approx \alpha W_i - \alpha W_i^2 - \beta W_i
$$

#### 2.2 The Continuum System (RHS)

From the foundational paper (Paper 1, Section 2.3), the theory proposes a Klein-Gordon Lagrangian for the continuum scalar field $\phi(x)$:

$$
\mathcal{L} = \frac{1}{2}(\partial_\mu \phi)(\partial^\mu \phi) - \frac{1}{2}m^2\phi^2
$$

*(Note: We use a general mass term $m$; the paper sets $m=1$.)*

The resulting Euler-Lagrange equation of motion is the Klein-Gordon equation:

$$
(\Box + m^2)\phi = 0 \quad \text{or} \quad \Box\phi + m^2\phi = 0
$$

Where $\Box \equiv \partial_\mu \partial^\mu = \frac{\partial^2}{\partial t^2} - \nabla^2$ is the d'Alembertian operator.

---

### 3. The Bridge: Formalizing the Field $\phi(x)$

To connect the discrete and continuum regimes, we must postulate a precise relationship between the discrete nodal states $W_i(t)$ and the continuous field $\phi(\vec{x}, t)$.

**Postulate 3.1: The Field as a Local Density**

The continuous scalar field $\phi(\vec{x}, t)$ at a spacetime point $x = (\vec{x}, t)$ is defined as the local spatial average density of the discrete states $W_i(t)$ in a small volume $V$ centered on the position $\vec{x}$.

In the discrete limit, this corresponds to averaging the state of a node $i$ and its immediate neighbors (its k-nearest neighbors, or KNN, from the simulation setup). Let the set of neighbors of node $i$ be $N(i)$.

$$
\phi(\vec{x}_i, t) \equiv \frac{1}{|N(i)|+1} \sum_{j \in \{i\} \cup N(i)} W_j(t)
$$

This definition provides the crucial link: it defines how the macroscopic, smoothly varying field $\phi$ emerges from the microscopic, discrete states $W$. With this, we can now begin to analyze the continuum limit of the discrete equation of motion.

---

### 4. Derivation of the Continuum Equation

To proceed, we will rewrite the discrete equation of motion in terms of the field $\phi$. This involves two key steps:
1. Approximating the discrete time difference with a time derivative.
2. Approximating the interaction with discrete neighbors with spatial derivatives.

#### 4.1 Temporal derivative and origin of second‑order dynamics (variational)

The left-hand side of the discrete equation is a first-order forward difference in time. In the limit $\Delta t \to 0$, this becomes the partial time derivative:
$$
\lim_{\Delta t \to 0} \frac{W_i(t+\Delta t) - W_i(t)}{\Delta t} = \frac{\partial W_i}{\partial t}.
$$

Crucially, the second-order time derivative in the continuum equation is not imposed ad hoc; it follows from varying the continuum Lagrangian density fixed by the lattice derivation of the kinetic and gradient terms (see [derivation/kinetic_term_derivation.md](derivation/kinetic_term_derivation.md:78-116)):
$$
\mathcal{L} \;=\; \frac{1}{2}(\partial_t \phi)^2 \;-\; J a^2\,(\nabla \phi)^2 \;-\; V(\phi).
$$
The Euler–Lagrange equation gives
$$
\partial_t^2 \phi \;-\; c^2 \nabla^2 \phi \;+\; V'(\phi) \;=\; 0,\qquad c^2 \equiv 2 J a^2,
$$
so the second-order dynamics arise from the action principle with a wave speed set by the lattice coupling. One may set $c=1$ by a units choice (e.g., choose $\tau=\sqrt{2J}\,a$) without tying $J$ to $a$ microscopically.

#### 4.2 Spatial Derivatives and the Laplacian

The core of the simulation involves interactions on a k-NN graph. To take a continuum limit, we approximate this graph as a regular d-dimensional lattice (e.g., a cubic lattice where d=3) where each node $i$ is at position $\vec{x}_i$ and is connected to its nearest neighbors.

The dynamics of $W_i$ depend on the states of its neighbors $W_j$. Let's assume the interaction term (the source of spatial derivatives) comes from a coupling between neighbors. A standard discrete Laplacian operator on a lattice is defined as:
$$
\nabla^2_{\text{discrete}} W_i = \sum_{j \in N(i)} (W_j - W_i)
$$
This term represents the difference between a node and its neighbors. Let's expand $W_j$ in a Taylor series around the point $\vec{x}_i$. For a neighbor $j$ at position $\vec{x}_i + \vec{\delta}_j$, where $\vec{\delta}_j$ is the displacement vector:
$$
W_j \approx W(\vec{x}_i + \vec{\delta}_j) \approx W(\vec{x}_i) + \vec{\delta}_j \cdot \nabla W(\vec{x}_i) + \frac{1}{2}(\vec{\delta}_j \cdot \nabla)^2 W(\vec{x}_i) + \dots
$$
Summing over all neighbors in a symmetric lattice (e.g., with neighbors at $+\vec{\delta}_j$ and $-\vec{\delta}_j$), the first-order gradient terms cancel out. The sum of the second-order terms yields a result proportional to the continuous Laplacian operator, $\nabla^2$.

$$
\sum_{j \in N(i)} (W_j - W_i) \approx C (\Delta x)^2 \nabla^2 W(\vec{x}_i)
$$
where $C$ is a constant dependent on the lattice structure.

#### 4.3 Assembling the Field Equation

We now substitute our field postulate, $W_i(t) \approx \phi(\vec{x}_i, t)$, into the right-hand side of the discrete equation. Let's assume the spatial coupling introduces the discrete Laplacian. The equation becomes:

$$
\frac{\partial \phi}{\partial t} \approx D \nabla^2 \phi + (\alpha - \beta)\phi - \alpha\phi^2
$$
Here, $D$ is the diffusion coefficient that emerges from the neighbor coupling strength and lattice constants. On a regular lattice with per‑site coupling,
$D = J a^2$ (or $D = (J/z)\,a^2$ if you average over $z$ neighbors). This is a **Reaction–Diffusion Equation**, renowned for generating complex patterns.

Using $V'(\phi)$ from the discrete law, $V'(\phi)=\alpha\phi^2-(\alpha-\beta)\phi$, the variational equation yields
$$
\partial_t^2 \phi \;-\; c^2 \nabla^2 \phi \;+\; \alpha\phi^2 \;-\; (\alpha - \beta)\phi \;=\; 0.
$$
In $c=1$ units this is
$$
\Box\phi \;+\; \alpha\phi^2 \;-\; (\alpha - \beta)\phi \;=\; 0.
$$

### 5. Analysis of the Result and Baseline EFT Choice

The derived continuum dynamics are nonlinear and exhibit a tachyonic instability about $\phi = 0$ stabilized by self‑interaction. For a well‑posed, bounded EFT we adopt the standard symmetric quartic as the default baseline:
$$
V_{\text{baseline}}(\phi)\;=\;-\frac{1}{2}\,\mu^2\,\phi^2\;+\;\frac{\lambda}{4}\,\phi^4,\qquad \mu^2>0,\ \lambda>0.
$$
- Linearizing about $\phi = 0$ gives $m_0^2 = -\mu^2 < 0$ (tachyonic).
- The true minima are at $\phi = \pm v$ with $v = \mu/\sqrt{\lambda}$.
- Fluctuations about either minimum have
$$
m_{\text{eff}}^2 \;=\; \left.\frac{d^2 V}{d\phi^2}\right|_{\phi=\pm v} \;=\; 2\,\mu^2.
$$

The earlier cubic–quadratic structure in our EOM (the $\alpha\,\phi^2 - (\alpha - \beta)\,\phi$ terms) is then treated as a small asymmetry (a “cubic tilt”) superposed on this bounded baseline; the precise mapping is made in Section 6.

---

### 6. Baseline Potential, Vacuum, and Mass (bounded)

#### 6.1 Bounded baseline and stationary points

We take as default
$$
V(\phi)\;=\;-\frac{1}{2}\,\mu^2\,\phi^2\;+\;\frac{\lambda}{4}\,\phi^4,\qquad \mu^2>0,\ \lambda>0.
$$
Stationary points satisfy
$$
\frac{dV}{d\phi}\;=\;-\mu^2\,\phi+\lambda\,\phi^3\;=\;0
\quad\Rightarrow\quad
\phi\in\{0,\pm v\},\ \ v\equiv \mu/\sqrt{\lambda}.
$$
Curvatures are
$$
\left.\frac{d^2V}{d\phi^2}\right|_{\phi=0}=-\mu^2<0,\qquad
\left.\frac{d^2V}{d\phi^2}\right|_{\phi=\pm v}=-\mu^2+3\lambda v^2=2\mu^2>0,
$$
so $\phi = 0$ is unstable (tachyon) and the true vacua are at $\pm v$. Small fluctuations about a chosen vacuum have
$$
m_{\text{eff}}=\sqrt{2}\,\mu.
$$

#### 6.2 Optional cubic tilt and mapping to $(\alpha, \beta)$

To prefer one vacuum and connect to the discrete‑to‑continuum coefficients, include a small cubic bias:
$$
V(\phi)\;=\;-\frac{1}{2}\,\mu^2\,\phi^2\;+\;\frac{\lambda}{4}\,\phi^4\;+\;\frac{\gamma}{3}\,\phi^3,\qquad |\gamma|\ll \mu^2\sqrt{\lambda}.
$$
For small fields the equation of motion reads
$$
\square\phi\;-\;\mu^2\,\phi\;+\;\gamma\,\phi^2\;+\;\lambda\,\phi^3\;\approx\;0.
$$
Comparing with our dimensionless continuum form
$$
\square\phi\;+\;\alpha\,\phi^2\;-\;(\alpha-\beta)\,\phi\;=\;0
$$
gives, to leading order about $\phi \approx 0$,
$$
\mu^2 \;\longleftrightarrow\; \alpha-\beta,\qquad
\gamma \;\longleftrightarrow\; \alpha.
$$
In this bounded EFT the symmetric‑limit VEV is $v = \mu/\sqrt{\lambda}$; a small $\gamma$ tilts the potential to select a unique vacuum near $+v$. To leading order the fluctuation mass remains $m_{\text{eff}}^2 \approx 2\mu^2 + \mathcal{O}(\gamma)$.

#### 6.3 Units and calibration

Using the physical map in [derivation/fum_voxtrium_mapping.md](derivation/fum_voxtrium_mapping.md:44-80), one has $\mu$ in GeV, $\lambda$ dimensionless, and
$$
m_{\text{eff}} = \sqrt{2}\,\mu
$$
in GeV once $\tau$ is fixed ($m^2 = \mu^2/\tau^2$ at the level of the dimensionful EOM). Choose $(\tau, \phi_0)$ to match a target $m_{\text{eff}}$ and quartic $\lambda$; see the worked example in that document.