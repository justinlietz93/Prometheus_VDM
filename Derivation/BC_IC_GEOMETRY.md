<!-- DOC-GUARD: CANONICAL -->
<!-- RULES for maintaining this file are here: /mnt/ironwolf/git/Prometheus_VDM/prompts/bc_ic_geometry_maintenance.md -->
# VDM Boundary/Initial Conditions & Domain Geometries (Auto-compiled)

Last updated: 2025-10-09 (commit 09f871a)

**Scope:** Single source of truth for BC/IC and domain geometries used in this repository.  
**Rules:** Link to equations/constants/symbols by anchor; do not restate them here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only.

---

## 1) Domain Geometries

| Geometry ID | Dim $d$ | Domain $\Omega$ (MathJax) | Parameters (link) | Boundary sets | Source (path:lines • commit) | Notes |
|---|---:|---|---|---|---|---|
| <a id="geom-1d-periodic-interval"></a>**1d-periodic-interval** | 1 | $(0, L)$ with periodic identification | $L$<sup>[↗](CONSTANTS.md#const-L)</sup>, $N$<sup>[↗](CONSTANTS.md#const-N)</sup> | Periodic in $x$ | derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:110 • c31d0c9 | 1D interval discretized with $N$ sites, spacing $dx = L/N$; used for dispersion validation |
| <a id="geom-1d-neumann-interval"></a>**1d-neumann-interval** | 1 | $[-L/2, L/2]$ | $L$<sup>[↗](CONSTANTS.md#const-L)</sup>, $N$<sup>[↗](CONSTANTS.md#const-N)</sup> | $\partial\Omega$ (both ends) with Neumann | derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:148 • c31d0c9 | 1D interval with zero-gradient (Neumann) boundaries at both ends; used for front-speed validation |
| <a id="geom-2d-periodic-torus"></a>**2d-periodic-torus** | 2 | $(0,1)^2$ with periodic identification | $nx$<sup>[↗](CONSTANTS.md#const-nx)</sup>, $ny$<sup>[↗](CONSTANTS.md#const-ny)</sup> | Periodic in both $x$ and $y$ | derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:58 • c31d0c9 | 2D periodic torus (unit domain); Taylor-Green vortex benchmark |
| <a id="geom-2d-square-box"></a>**2d-square-box** | 2 | $[0, nx] \times [0, ny]$ | $nx$<sup>[↗](CONSTANTS.md#const-nx)</sup>, $ny$<sup>[↗](CONSTANTS.md#const-ny)</sup> | $\partial\Omega$ consists of 4 walls | derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:148-149 • c31d0c9 | 2D square cavity (lid-driven); no-slip walls (bounce-back) on bottom/left/right, velocity BC on top |
| <a id="geom-1d-periodic-ring"></a>**1d-periodic-ring** | 1 | $\mathbb{Z}_N$ (cyclic graph) | $N$ nodes | Periodic (ring topology) | derivation/code/physics/axioms/verify_discrete_EL.py:30 • c31d0c9 | Discrete 1D periodic lattice (ring); nearest-neighbor connectivity |
| <a id="geom-2d-periodic-torus-lattice"></a>**2d-periodic-torus-lattice** | 2 | $\mathbb{Z}_{N_y} \times \mathbb{Z}_{N_x}$ (2D torus graph) | $N_y \times N_x$ nodes | Periodic in both directions | derivation/code/physics/axioms/verify_discrete_EL.py:40 • c31d0c9 | Discrete 2D periodic lattice (torus); von Neumann 4-neighborhood |
| <a id="geom-walker-box-2d"></a>**walker-box-2d** | 2 | Box of size $(n_x, n_y)$ | $(n_x, n_y)$ | Periodic or Neumann | derivation/code/obs/walker_glow.py:22-23 • c31d0c9 | Regular 2D grid for walker observability; supports periodic or homogeneous Neumann BCs |

---

## 2) Boundary Conditions (by geometry and field/channel)

##### Periodic BC for 1D RD dispersion  <a id="bc-periodic-1d-rd-dispersion"></a>
**Context:** derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:34-37, 106, 125 • c31d0c9 • RD dispersion validation

**Field(s):** $\phi$ (linearized Fisher-KPP field $u$) • TODO: add anchor `sym-phi` in SYMBOLS.md:10 for $\boldsymbol{\phi}(\mathbf{x},t)$  
**Type:** Periodic  
**Definition (quote from source if formula exists):**
$$
u(0, t) = u(L, t), \quad \partial_x u|_{x=0} = \partial_x u|_{x=L}
$$

**Applies on:** All boundaries of [1d-periodic-interval](#geom-1d-periodic-interval)  
**Parameters:** None (topological identification)  
**Implemented at:** derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:34-37 (laplacian_periodic using `np.roll`)  
**Notes:** Enforced via periodic wrap in second-order difference stencil; conserves total mass $\sum_i u_i$ in diffusion-only regime

---

##### Neumann (zero-gradient) BC for 1D RD front speed  <a id="bc-neumann-1d-rd-front"></a>
**Context:** derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:28-36, 183 • c31d0c9 • RD front-speed validation

**Field(s):** $\phi$ (Fisher-KPP field $u$) • TODO: add anchor `sym-phi` in SYMBOLS.md:10 for $\boldsymbol{\phi}(\mathbf{x},t)$  
**Type:** Neumann (homogeneous / no-flux)  
**Definition (quote from source if formula exists):**
$$
\partial_n u|_{\partial\Omega} = 0
$$
(Ghost cells mirror interior: $u_{-1} = u_1$, $u_N = u_{N-2}$ for discrete stencil.)

**Applies on:** Both endpoints $x = -L/2$ and $x = L/2$ of [1d-neumann-interval](#geom-1d-neumann-interval)  
**Parameters:** None  
**Implemented at:** derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:28-36 (laplacian_neumann with ghost mirroring)  
**Notes:** Allows front to propagate without boundary reflection; conserves total mass when reaction term $f \equiv 0$

---

##### Periodic BC for 2D Taylor-Green vortex  <a id="bc-periodic-2d-taylor-green"></a>
**Context:** derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:58 • c31d0c9 • Fluids (LBM) Taylor-Green benchmark

**Field(s):** LBM populations $f_i$, macroscopic velocity $(u_x, u_y)$, density $\rho$  
**Type:** Periodic  
**Definition (quote from source if formula exists):**
$$
f_i(0, y, t) = f_i(n_x, y, t), \quad f_i(x, 0, t) = f_i(x, n_y, t)
$$
(and similarly for $(u_x, u_y, \rho)$ in both $x$ and $y$ directions)

**Applies on:** All boundaries of [2d-periodic-torus](#geom-2d-periodic-torus)  
**Parameters:** None (topological identification)  
**Implemented at:** derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:115-116 (LBMConfig.periodic_x=True, periodic_y=True), lbm2d.py:274-303 (streaming with periodic wrap)  
**Notes:** LBM streaming uses `np.roll` for periodic boundaries; viscous decay validation benchmark

---

##### Bounce-back no-slip walls for 2D lid cavity  <a id="bc-bounce-back-lid-cavity"></a>
**Context:** derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:379, fluids/lbm2d.py:175, 303-313 • c31d0c9 • Fluids (LBM) lid-driven cavity benchmark

**Field(s):** LBM populations $f_i$ at solid boundaries  
**Type:** Bounce-back (no-slip wall)  
**Definition (quote from source if formula exists):**
At solid boundaries (marked by `solid[y,x]=True`), the post-streaming populations are reflected:
$$
f_i^{\mathrm{post}}(\mathbf{x}_{\mathrm{solid}}, t) = f_{\bar{i}}^{\mathrm{pre}}(\mathbf{x}_{\mathrm{solid}}, t)
$$
where $\bar{i}$ is the opposite direction to $i$ (e.g., $\mathrm{OPP}[i]$ in D2Q9).

**Applies on:** Bottom, left, and right walls of [2d-square-box](#geom-2d-square-box)  
**Parameters:** None (half-way bounce-back on boundary nodes)  
**Implemented at:** derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:303-313 (bounce-back swap at solid cells after streaming)  
**Notes:** Enforces zero velocity at walls; no-slip condition in NS limit

---

##### Zou/He velocity BC for lid cavity top wall  <a id="bc-zou-he-lid-top"></a>
**Context:** derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:181-197, lid_cavity_benchmark.py:379 • c31d0c9 • Fluids (LBM) lid-driven cavity

**Field(s):** LBM populations at top boundary (moving lid)  
**Type:** Zou/He velocity boundary condition (Dirichlet-like for velocity)  
**Definition (quote from source if formula exists):**
At the top boundary ($y=0$, fluid side), reconstruct unknown incoming populations $f_4, f_7, f_8$ to impose $u_x = U_{\mathrm{lid}}$, $u_y = 0$:
$$
\begin{aligned}
\rho &= f_0 + f_1 + f_3 + 2(f_2 + f_5 + f_6) \\
f_4 &= f_2 \\
f_7 &= f_5 - \tfrac{1}{2}(f_1 - f_3) - \tfrac{1}{6} \rho U_{\mathrm{lid}} \\
f_8 &= f_6 + \tfrac{1}{2}(f_1 - f_3) + \tfrac{1}{6} \rho U_{\mathrm{lid}}
\end{aligned}
$$

**Applies on:** Top wall ($y=0$) of [2d-square-box](#geom-2d-square-box), excluding corner cells  
**Parameters:** $U_{\mathrm{lid}}$<sup>[↗](CONSTANTS.md#const-U_lid)</sup>  
**Implemented at:** derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:181-197 (set_lid_velocity method)  
**Notes:** Imposes tangential velocity on top boundary; drives the cavity flow

---

##### Periodic BC for walker glow observability (1D/2D)  <a id="bc-periodic-walker-glow"></a>
**Context:** derivation/code/obs/walker_glow.py:22, 76, 94 • c31d0c9 • Observability layer

**Field(s):** Glow intensity $M$, fluxes $F$  
**Type:** Periodic  
**Definition (quote from source if formula exists):**
Wraparound neighbors on a regular grid (1D or 2D); incoming flux from outside the domain is taken from the opposite boundary via periodic wrap.

**Applies on:** All boundaries of [walker-box-2d](#geom-walker-box-2d) (when `bc="periodic"`)  
**Parameters:** None  
**Implemented at:** derivation/code/obs/walker_glow.py:76-77, 94-98 (periodic wrap via `np.roll` for incoming flux accumulation)  
**Notes:** Read-only observability; does not alter dynamics

---

##### Neumann BC for walker glow observability (1D/2D)  <a id="bc-neumann-walker-glow"></a>
**Context:** derivation/code/obs/walker_glow.py:23, 79, 100 • c31d0c9 • Observability layer

**Field(s):** Glow intensity $M$, fluxes $F$  
**Type:** Neumann (homogeneous no-flux)  
**Definition (quote from source if formula exists):**
Boundary incoming from outside is zero (no flux across domain boundary).

**Applies on:** All boundaries of [walker-box-2d](#geom-walker-box-2d) (when `bc="neumann"`)  
**Parameters:** None  
**Implemented at:** derivation/code/obs/walker_glow.py:79-83, 100-110 (explicit handling of boundary terms, dropping wrap contributions)  
**Notes:** Read-only observability; does not alter dynamics

---

##### Periodic or Neumann BC for flux-form diffusion  <a id="bc-flux-diffusion"></a>
**Context:** derivation/code/physics/reaction_diffusion/flux_core.py:11-16, 58-118 • c31d0c9 • Conservative flux-form RD

**Field(s):** $\phi$ (general RD field) • TODO: add anchor `sym-phi` in SYMBOLS.md:10 for $\boldsymbol{\phi}(\mathbf{x},t)$  
**Type:** Periodic or Neumann (user-specified)  
**Definition (quote from source if formula exists):**
Conservative flux-form update with antisymmetric edge fluxes $F_{ij} = -F_{ji}$:
$$
\phi_i^{n+1} = \phi_i^{n} - \frac{\Delta t}{a} \sum_{j \in N(i)} F_{ij}
$$
With periodic BCs, fluxes wrap at boundaries; with Neumann BCs, boundary fluxes are set to zero.

**Applies on:** Boundaries of [1d-periodic-interval](#geom-1d-periodic-interval) or [1d-neumann-interval](#geom-1d-neumann-interval) (1D), or [2d-periodic-torus](#geom-2d-periodic-torus) or analogous Neumann 2D box (2D)  
**Parameters:** $D$<sup>[↗](CONSTANTS.md#const-D)</sup>, $a$ (lattice spacing), $\Delta t$  
**Implemented at:** derivation/code/physics/reaction_diffusion/flux_core.py:58-118 (flux_update_periodic, flux_update_neumann)  
**Notes:** Conserves total mass $\sum_i \phi_i$ to machine precision when $f \equiv 0$; Lemma F.1 validated

---

##### Axiom 5: Periodic or no-flux (Neumann) BCs for continuum integration by parts  <a id="bc-axiom5"></a>
**Context:** agent-onboarding/axiomatic_theory_development.md:42 • c31d0c9 • Axiomatic foundations

**Field(s):** General continuum field $\phi(\mathbf{x}, t)$  
**Type:** Periodic or no-flux (homogeneous Neumann)  
**Definition (quote from source if formula exists):**
When performing continuum integrations by parts, require one of:
- Periodic BCs, or
- No-flux (homogeneous Neumann) BCs: $\hat{n} \cdot \nabla \phi = 0$ on $\partial\Omega$

**Applies on:** Boundary $\partial\Omega$ of continuum domain $\Omega \subset \mathbb{R}^d$  
**Parameters:** None (axiomatically specified)  
**Implemented at:** Axiom 5 in agent-onboarding/axiomatic_theory_development.md:42  
**Notes:** Foundational constraint for continuum theory derivations; ensures surface terms vanish in integration by parts

---

##### Absorbing (Dirichlet) boundary for agency walkers  <a id="bc-absorbing-agency-walkers"></a>
**Context:** AGENCY_FIELD_V2.md:§Runtime Walkers • observability/gating runs (agency)   

**Field(s):** Walker positions (X); optional agency map (M) (read-only)     
**Type:** Absorbing / Dirichlet (out-of-domain removal)     
**Definition (quote from source if formula exists):**
Walkers that step outside (\Omega) are removed from the simulation at that step (no re-injection or wrap). If a scalar field (M) is logged, enforce $(M|_{\partial\Omega}=0)$ for visualization.  

**Applies on:** All boundaries of [walker-box-2d](#geom-walker-box-2d)  
**Parameters:** None    
**Implemented at:** - (spec; planned alongside agency walker runtime)   
**Notes:** Models “cliff” domains where leaving the workspace terminates control; reduces reachable option-space near walls, which measurably lowers $V_{\text{useful\_bits}}$ under identical noise.

---

##### Reflecting (specular) boundary for agency walkers  <a id="bc-reflecting-agency-walkers"></a>

**Context:** AGENCY_FIELD_V2.md:§Runtime Walkers • explorative runs (agency)    
**Field(s):** Walker positions (X); optional agency map (M) (read-only)     
**Type:** Reflecting / Neumann-like (specular reflection)   
**Definition (quote from source if formula exists):**   
On attempted step $(\Delta x)$ that exits $(\Omega)$, reflect the normal component at the boundary:     
$(\Delta x\_{\perp} \leftarrow -\Delta x\_{\perp})$\, $(\Delta x\_{\parallel})$ unchanged; then apply the reflected step.   

**Applies on:** All boundaries of [walker-box-2d](#geom-walker-box-2d)  
**Parameters:** None    
**Implemented at:** - (spec; planned alongside agency walker runtime)   
**Notes:** Preserves mass of walkers; appropriate when physical walls exist but agents can “bounce.” Typically raises reachable option-space vs. absorbing, shifting agency thresholds.     

---

## 3) Initial Conditions

##### Random noise IC for RD dispersion  <a id="ic-random-noise-rd-dispersion"></a>
**Context:** derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:106, 119 • c31d0c9

**Quantity:** Linearized Fisher-KPP field $u(\mathbf{x}, 0)$ • TODO: add anchor `sym-phi` in SYMBOLS.md:10 for $\boldsymbol{\phi}(\mathbf{x},t)$  
**Definition (quote from source if formula exists):**
$$
u(x, 0) = A_0 \cdot \eta(x)
$$
where $\eta(x) \sim \mathcal{N}(0, 1)$ is standard Gaussian noise, and $A_0$ is a small amplitude.

**Parameters:** $amp0 = 10^{-6}$<sup>[↗](CONSTANTS.md#const-amp0)</sup>, $seed = 42$<sup>[↗](CONSTANTS.md#const-seed)</sup>  
**Randomization/Seeds:** `seed=42` for `np.random.default_rng(seed).standard_normal(size=N)`  
**Applies to Geometry:** [1d-periodic-interval](#geom-1d-periodic-interval)  
**Notes:** Small amplitude ensures linearization $\partial_t u \approx D \partial_{xx} u + r u$ is valid; used to measure dispersion relation $\sigma(k)$

---

##### Smooth tanh step IC for RD front speed  <a id="ic-tanh-step-rd-front"></a>
**Context:** derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:157-170 • c31d0c9

**Quantity:** Fisher-KPP field $u(\mathbf{x}, 0)$ • TODO: add anchor `sym-phi` in SYMBOLS.md:10 for $\boldsymbol{\phi}(\mathbf{x},t)$  
**Definition (quote from source if formula exists):**
$$
u(x, 0) = \frac{1}{2} \left(1 - \tanh\left(\frac{x - x_0}{w}\right)\right), \quad u(x > x_0 + 6w, 0) = 0
$$
where $x_0$ is the initial front position and $w = 2.0$ is the interface width.

**Parameters:** $x_0 = -60$<sup>[↗](CONSTANTS.md#const-x0)</sup>, $w = 2.0$ (hardcoded), optional noise amplitude (default 0.0)  
**Randomization/Seeds:** If `noise_amp > 0`, add Gaussian noise with [`seed`](CONSTANTS.md#const-seed) to left side of interface only  
**Applies to Geometry:** [1d-neumann-interval](#geom-1d-neumann-interval)  
**Notes:** Left region $u \approx 1$ (populated), right region $u = 0$ (unpopulated); front propagates to the right at speed $c \approx 2\sqrt{Dr}$

---

##### Taylor-Green vortex IC for 2D LBM  <a id="ic-taylor-green-vortex"></a>
**Context:** derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:32-39 • c31d0c9

**Quantity:** LBM velocity field $(u_x, u_y)$  
**Definition (quote from source if formula exists):**
$$
\begin{aligned}
u_x(x, y, 0) &= U_0 \cos(k x) \sin(k y) \\
u_y(x, y, 0) &= -U_0 \sin(k x) \cos(k y)
\end{aligned}
$$
where $x, y \in 0, 1)$ are normalized coordinates, and populations $f_i$ are set to equilibrium.

**Parameters:** [$U_0 = 0.05$<sup>[↗](CONSTANTS.md#const-U0)</sup>, $k = 2\pi$<sup>[↗](CONSTANTS.md#const-k-tg)</sup>  
**Randomization/Seeds:** None (deterministic analytical IC)  
**Applies to Geometry:** [2d-periodic-torus](#geom-2d-periodic-torus)  
**Notes:** Analytical solution decays as $E(t) = E_0 \exp(-2 \nu k^2 t)$; used to validate viscosity recovery in LBM

---

##### Equilibrium IC for LBM (lid cavity and general)  <a id="ic-lbm-equilibrium"></a>
**Context:** derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:166-172 • c31d0c9

**Quantity:** LBM populations $f_i$ at $t=0$  
**Definition (quote from source if formula exists):**
Initialize to equilibrium with $\rho = 1$, $\mathbf{u} = \mathbf{0}$:
$$
f_i^{\mathrm{eq}} = w_i \rho \left(1 + \frac{3 \mathbf{c}_i \cdot \mathbf{u}}{c_s^2} + \frac{9 (\mathbf{c}_i \cdot \mathbf{u})^2}{2 c_s^4} - \frac{3 \mathbf{u}^2}{2 c_s^2}\right)
$$
where $w_i$ are D2Q9 weights, $\mathbf{c}_i$ are lattice velocities, and $c_s^2 = 1/3$.

**Parameters:** $\rho = 1$, $\mathbf{u} = (0, 0)$, D2Q9 weights and velocities from lbm2d.py:98-106  
**Randomization/Seeds:** None (deterministic)  
**Applies to Geometry:** [2d-square-box](#geom-2d-square-box) (lid cavity), [2d-periodic-torus](#geom-2d-periodic-torus) (Taylor-Green, overridden by analytical IC)  
**Notes:** Default initialization for LBM; _set_equilibrium() method in lbm2d.py:166-172

---

##### Near-void initial state for discrete lattice (axiom verification)  <a id="ic-near-void-axiom"></a>
**Context:** derivation/code/computational_toy_proofs/toy_QM.py:28 • c31d0c9

**Quantity:** Discrete node state $W(0)$ • TODO: add anchor `sym-Wi` in SYMBOLS.md:21 for $W_i(t)$  
**Definition (quote from source if formula exists):**
$$
W(0) = 0.1
$$
(near-void state for single-node logistic evolution test)

**Parameters:** $W_0 = 0.1$ (hardcoded)  
**Randomization/Seeds:** None (deterministic)  
**Applies to Geometry:** Single-node system (0D)  
**Notes:** Used for computational proof of logarithmic first integral $Q(W, t) = \ln(W/(r - u W)) - r t$

---

##### Uniform quiescent agency field  <a id="ic-agency-field-quiescent"></a>

**Context:** AGENCY_FIELD_V2.md:§Field Definition • cold-start runs     
**Quantity:** Agency map $(M(\mathbf{x},0))$ (capability/affordance density; read-only for probes)  
**Definition (quote from source if formula exists):**   
$(M(\mathbf{x},0) = 0)$ on $(\Omega)$\.

**Parameters:** None    
**Randomization/Seeds:** None (deterministic)   
**Applies to Geometry:** [walker-box-2d](#geom-walker-box-2d)   
**Notes:** Clean baseline for observing how walkers and constraints imprint structure; pairs with absorbing or reflecting BCs above.    

---

##### Seeded walker distribution (Poisson)  <a id="ic-agency-walkers-poisson"></a>

**Context:** AGENCY_FIELD_V2.md:§Runtime Walkers • default seeding      
**Quantity:** Walker set $({X\_k(0)}\_{k=1}^{N\_w})$     
**Definition (quote from source if formula exists):**   
Sample (N_w) initial positions i.i.d. uniform on $(\Omega)$ (Poisson disc optional).    

**Parameters:** (N_w) (see `walkers` in CONSTANTS.md)   
**Randomization/Seeds:** Use `seed`<sup>[↗](CONSTANTS.md#const-seed)</sup> to control RNG for reproducibility   
**Applies to Geometry:** [walker-box-2d](#geom-walker-box-2d)   
**Notes:** Matches your other ICs: deterministic when seeded; supports side-by-side BC comparisons for agency thresholds.   

---

## 4) Lattice/Stencil & Neighbor Topology

| ID | Stencil/Topology | Description (as named) | Parameters (link) | Source | Notes |
|---|---|---|---|---|---|
| <a id="lattice-nn-1d"></a>**nn-1d** | 1D nearest-neighbor (ring) | Neighbors $N(i) = \{i-1, i+1\}$ (periodic) | $N$ nodes, lattice spacing $a$ | derivation/code/physics/axioms/verify_discrete_EL.py:28-35 • c31d0c9 | Coordination $z = 2$ |
| <a id="lattice-nn-2d"></a>**nn-2d** | 2D von Neumann (torus) | Neighbors $N(i) = \{\text{north, south, east, west}\}$ (periodic) | $N_y \times N_x$ nodes, spacing $a$ | derivation/code/physics/axioms/verify_discrete_EL.py:38-47 • c31d0c9 | Coordination $z = 4$ |
| <a id="lattice-d2q9"></a>**D2Q9** | D2Q9 LBM lattice (2D) | 9 velocity directions: rest (1), cardinals (4), diagonals (4) | Velocities $\mathbf{c}_i$, weights $w_i$, $c_s^2 = 1/3$ | derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:98-106 • c31d0c9 | Standard LBM D2Q9 stencil; opposite directions via OPP array |
| <a id="lattice-generic-cartesian"></a>**cartesian-1d-2d** | Regular Cartesian grid (1D/2D) | Uniform spacing $a$, cell-centered values | Grid spacing $a$ (or $dx$) | derivation/code/physics/reaction_diffusion/flux_core.py:14-16 • c31d0c9 | Supports periodic or Neumann BCs; used in flux-conservative RD |
| <a id="lattice-moore-8"></a>**moore-8** | 2D Moore (8-neighbor) | Neighbors $(N(i)={\text{N,S,E,W,NE,NW,SE,SW}})$ | $(N\_y \times N\_x)$, spacing (a) | - (spec) | If agency walkers step diagonally as well as axially |

---

<!-- BEGIN AUTOSECTION: BCIC-INDEX -->
<!-- Tool-maintained list of [Geometry](#geom-...), [BC](#bc-...), and [IC](#ic-...) anchors -->

**Geometry Anchors:**
- [1d-periodic-interval](#geom-1d-periodic-interval)
- [1d-neumann-interval](#geom-1d-neumann-interval)
- [2d-periodic-torus](#geom-2d-periodic-torus)
- [2d-square-box](#geom-2d-square-box)
- [1d-periodic-ring](#geom-1d-periodic-ring)
- [2d-periodic-torus-lattice](#geom-2d-periodic-torus-lattice)
- [walker-box-2d](#geom-walker-box-2d)

**BC Anchors:**
- [bc-periodic-1d-rd-dispersion](#bc-periodic-1d-rd-dispersion)
- [bc-neumann-1d-rd-front](#bc-neumann-1d-rd-front)
- [bc-periodic-2d-taylor-green](#bc-periodic-2d-taylor-green)
- [bc-bounce-back-lid-cavity](#bc-bounce-back-lid-cavity)
- [bc-zou-he-lid-top](#bc-zou-he-lid-top)
- [bc-periodic-walker-glow](#bc-periodic-walker-glow)
- [bc-neumann-walker-glow](#bc-neumann-walker-glow)
- [bc-flux-diffusion](#bc-flux-diffusion)
- [bc-axiom5](#bc-axiom5)

**IC Anchors:**
- [ic-random-noise-rd-dispersion](#ic-random-noise-rd-dispersion)
- [ic-tanh-step-rd-front](#ic-tanh-step-rd-front)
- [ic-taylor-green-vortex](#ic-taylor-green-vortex)
- [ic-lbm-equilibrium](#ic-lbm-equilibrium)
- [ic-near-void-axiom](#ic-near-void-axiom)

**Lattice Anchors:**
- [nn-1d](#lattice-nn-1d)
- [nn-2d](#lattice-nn-2d)
- [D2Q9](#lattice-d2q9)
- [cartesian-1d-2d](#lattice-generic-cartesian)

<!-- END AUTOSECTION: BCIC-INDEX -->

## Change Log
- 2025-10-03 • Initial creation of BC_IC_GEOMETRY.md with all BC/IC/geometries • 24ddc4d

Short version: the **options-probe** itself is parametric (grid over $(E)$ and $(p\_{\text{slip}}$)), so it doesn’t belong in a BC/IC/geometry doc.

Where agency *does* touch this file is when walkers or any “agency field” actually live on a spatial lattice (same grid already used for `walker_glow`). In that case, adding a couple of BCs and ICs makes the canon complete and prevents future ambiguity about “edge-of-domain behavior.”
