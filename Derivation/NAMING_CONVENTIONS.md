<!-- DOC-GUARD: CANONICAL -->
<!-- RULES for maintaining this file are here: /mnt/ironwolf/git/Prometheus_VDM/prompts/naming_conventions_maintenance.md -->
# VDM Naming & Notation Conventions (Auto-compiled)

Last updated: 2025-10-09 (commit 09f871a)

**Scope:** Single source of truth for mathematical and semantic naming conventions used in this repository.  
**Rules:** Extract from repository evidence only; link to canonical symbols/equations/units/constants. Do not redefine them here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing snippets.

---

## 1) Symbol Styling (typography choices)

| Category | Convention (MathJax) | Example from repo | Source (path:lines • commit) | Notes |
|---|---|---|---|---|
| Vectors | `\mathbf{}` | `$\mathbf{x}$` - spatial coordinate | derivation/SYMBOLS.md:9 • 1060de4 | Position vectors, velocity vectors |
| Multi-channel fields | `\boldsymbol{}` | `$\boldsymbol{\phi}(\mathbf{x},t)$` - $C$-channel field stack | derivation/SYMBOLS.md:10 • 1060de4 | Tensor/multi-component fields |
| Multi-channel fields (cont.) | `\boldsymbol{}` | `$\boldsymbol{\mu}(\mathbf{x},t)$` - memory-steering field | derivation/SYMBOLS.md:90 • 1060de4 | Slow bias fields |
| Multi-channel fields (cont.) | `\boldsymbol{}` | `$\boldsymbol{\gamma}(\mathbf{x},t)$` - gating mask | derivation/SYMBOLS.md:81 • 1060de4 | Channel/space control masks |
| Sets/spaces | `\mathcal{}` | `$\mathcal{W}$` - set of walkers | derivation/SYMBOLS.md:13 • 1060de4 | Sets, collections |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{B}_{\ell}$` - bus at level $\ell$ | derivation/SYMBOLS.md:76 • 1060de4 | Hierarchical structures |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{H}$` - bus hierarchy | derivation/SYMBOLS.md:77 • 1060de4 | Hierarchies |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{S}(t)$` - scoreboard state | derivation/SYMBOLS.md:79 • 1060de4 | State/status objects |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{A}$` - aggregator | derivation/SYMBOLS.md:78 • 1060de4 | Operators/aggregations |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{P}$` - plasticity policy | derivation/SYMBOLS.md:93 • 1060de4 | Policies |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{J}$` - objective | derivation/SYMBOLS.md:94 • 1060de4 | Objectives, functionals |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{C}$` - constraint set | derivation/SYMBOLS.md:84 • 1060de4 | Constraints |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{N}_r(\mathbf{x})$` - neighborhood | derivation/SYMBOLS.md:70 • 1060de4 | Neighborhoods |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{V}(\mathbf{x},t)$` - void baseline scalar | derivation/SYMBOLS.md:11 • 1060de4 | Reference fields |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{H}_i$` - discrete Hamiltonian | derivation/SYMBOLS.md:55 • 1060de4 | Energy densities |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{K}_i$` - kinetic energy | derivation/SYMBOLS.md:56 • 1060de4 | Energy components |
| Sets/spaces (cont.) | `\mathcal{}` | `$\mathcal{I}_i$` - interaction energy | derivation/SYMBOLS.md:57 • 1060de4 | Energy components |
| Field spaces | `\mathbb{R}^d`, `\mathbb{R}^C` | `$\mathbf{x}\in\mathbb{R}^d$` | derivation/SYMBOLS.md:9 • 1060de4 | Euclidean spaces |
| Field spaces (cont.) | `\mathbb{R}^d`, `\mathbb{R}^C` | `$\boldsymbol{\phi}(\mathbf{x},t)\in\mathbb{R}^{C}$` | derivation/SYMBOLS.md:10 • 1060de4 | Multi-channel target spaces |
| Field spaces (cont.) | `\mathbb{R}^d`, `\mathbb{R}^C` | `$\mathbf{g}(t)\in\mathbb{R}^{K}$` - GDSP score vector | derivation/SYMBOLS.md:80 • 1060de4 | Score vectors |
| Lattice spaces | `\mathbb{Z}_N` | `$\mathbb{Z}_N$` - cyclic graph | derivation/BC_IC_GEOMETRY.md:18 • c31d0c9 | Discrete periodic lattice |
| Operators (named) | `\mathrm{}` | `$\mathrm{nbr}(i)$` - neighbor set | derivation/SYMBOLS.md:22 • 1060de4 | Neighbor functions |
| Operators (named) (cont.) | `\mathrm{}` | `$\mathrm{KDE}_\sigma$` - kernel density estimate | derivation/SYMBOLS.md:155 • 1060de4 | Named operators |
| Operators (named) (cont.) | `\mathrm{}` | `$\mathrm{SIE}$` - Self Improvement Engine | derivation/SYMBOLS.md:100 • 1060de4 | System abbreviations (upright) |
| Operators (named) (cont.) | `\mathrm{}` | `$\mathrm{ADC}$` - Adaptive Domain Cartographer | derivation/SYMBOLS.md:101 • 1060de4 | System abbreviations (upright) |
| Operators (differential) | Standard | `$\nabla^2$` - Laplacian | derivation/SYMBOLS.md:10 • 1060de4 | Differential operators |
| Operators (differential) (cont.) | Standard | `$\nabla \cdot$` - discrete divergence | derivation/SYMBOLS.md:59 • 1060de4 | Divergence |
| Operators (differential) (cont.) | Standard | `$\Box$` - d'Alembertian | derivation/SYMBOLS.md:48 • 1060de4 | Wave operator |
| Operators (differential) (cont.) | Standard | `$\partial_t$`, `$\partial_n$` | derivation/EQUATIONS.md:14, BC_IC_GEOMETRY.md:50 • various | Partial derivatives |
| Dimensionless groups | `\mathrm{}` or plain | `$\mathrm{Re}$` - Reynolds number | derivation/SYMBOLS.md:145 • 1060de4 | Named dimensionless numbers (upright) |
| Dimensionless groups (cont.) | `\mathrm{}` or plain | `$\mathrm{Ma}$` - Mach number | derivation/SYMBOLS.md:146 • 1060de4 | Named dimensionless numbers (upright) |
| Dimensionless groups (cont.) | `\mathrm{}` or plain | `$\mathrm{Pe}$` - Péclet number | derivation/SYMBOLS.md:147 • 1060de4 | Named dimensionless numbers (upright) |
| Dimensionless groups (cont.) | `\mathrm{}` or plain | `$\mathrm{Da}$` - Damköhler number | derivation/SYMBOLS.md:136 • 1060de4 | Named dimensionless numbers (upright) |
| Functions | Italic (default) | `$V(\phi)$` - potential energy | derivation/SYMBOLS.md:41 • 1060de4 | Functions |
| Functions (cont.) | Italic (default) | `$F(W)$` - discrete dynamics | derivation/SYMBOLS.md:33 • 1060de4 | Functions |
| Functions (cont.) | Italic (default) | `$Q(W,t)$` - logarithmic first integral | derivation/SYMBOLS.md:28 • 1060de4 | Functions |
| Greek scalars | Italic (default) | `$\rho(\mathbf{x},t)$` - activity density | derivation/SYMBOLS.md:12 • 1060de4 | Scalar fields |
| Greek scalars (cont.) | Italic (default) | `$\alpha, \beta$` - on-site rates | derivation/SYMBOLS.md:26 • 1060de4 | Parameters |
| Greek scalars (cont.) | Italic (default) | `$\epsilon$` - time-scale ratio | derivation/SYMBOLS.md:92 • 1060de4 | Small parameters |
| Greek scalars (cont.) | Italic (default) | `$\tau$` - BGK relaxation time | derivation/SYMBOLS.md:142 • 1060de4 | Relaxation times |
| Greek scalars (cont.) | Italic (default) | `$\nu$` - kinematic viscosity | derivation/SYMBOLS.md:143 • 1060de4 | Physical parameters |
| Greek scalars (cont.) | Italic (default) | `$\lambda, \mu, \gamma$` - EFT parameters | derivation/SYMBOLS.md:43-44 • 1060de4 | Field theory parameters |
| Indices | Italic (default) | `$i, j$` - spatial site indices | derivation/SYMBOLS.md:21-22 • 1060de4 | Lattice site labels |
| Indices (cont.) | Italic (default) | `$c$` - channel index | derivation/SYMBOLS.md:10 • 1060de4 | Channel labels |
| Indices (cont.) | Italic (default) | `$k$` - objective index | derivation/SYMBOLS.md:80 • 1060de4 | Objective/metric labels |
| Indices (cont.) | Italic (default) | `$w$` - walker index | derivation/SYMBOLS.md:13 • 1060de4 | Walker labels |
| Indices (cont.) | Italic (default) | `$t, n$` - time indices | derivation/SYMBOLS.md:9, 21 • 1060de4 | Time labels |
| Indices (cont.) | Italic (default) | `$\ell$` - level index | derivation/SYMBOLS.md:76 • 1060de4 | Hierarchy level |
| Indices (cont.) | Italic (default) | `$d$` - dimension | derivation/SYMBOLS.md:9 • 1060de4 | Spatial dimension |

---

## 2) Reserved Names & Abbreviations

| Name | Expansion / Meaning | Where used | Source | Notes |
|---|---|---|---|---|
| SIE | Self Improvement Engine | Global controller for self-evaluation and tuning | derivation/SYMBOLS.md:100 • 1060de4 | Computes scores, updates budgets, refines policies, adjusts plasticity; see [$\mathrm{SIE}$](../derivation/SYMBOLS.md#L100) |
| ADC | Adaptive Domain Cartographer | Global controller for objective-domain mapping | derivation/SYMBOLS.md:101 • 1060de4 | Sets gating masks, selects targets, chooses neighborhoods; see [$\mathrm{ADC}$](../derivation/SYMBOLS.md#L101) |
| GDSP | Goal-Directed Structural Plasticity | Plasticity mechanism | derivation/SYMBOLS.md:80 • 1060de4 | Universal plasticity rate; see [$\mathbf{g}(t)$](../derivation/SYMBOLS.md#L80) GDSP score vector |
| RE-VGSP | Resonance-Enhanced Valence-Gated Synaptic Plasticity | Learning mechanism | derivation/CONSTANTS.md:10 • 0922758 | Universal learning rate; see [`ALPHA`](../derivation/CONSTANTS.md#const-alpha) |
| KPP | Kolmogorov-Petrovsky-Piskunov | Reaction-diffusion wave equation | derivation/EQUATIONS.md, derivation/SYMBOLS.md:135 • various | Fisher-KPP equation; normalized speed $c^*$ |
| RD | Reaction-Diffusion | System class | derivation/SYMBOLS.md:17-36 • 1060de4 | Discrete lattice to continuum mapping |
| EFT | Effective Field Theory | Theoretical framework | derivation/SYMBOLS.md:37-49 • 1060de4 | Tachyon, quartic $\phi^4$, masses |
| LBM | Lattice Boltzmann Method | Fluid simulation method | derivation/SYMBOLS.md:138-147 • 1060de4 | BGK collision, D2Q9 lattice |
| BGK | Bhatnagar-Gross-Krook | Collision operator in LBM | derivation/SYMBOLS.md:142 • 1060de4 | Relaxation time $\tau$ |
| KDE | Kernel Density Estimate | Smoothing method | derivation/SYMBOLS.md:155 • 1060de4 | Smooth sparse events with kernel $K_\sigma$ |
| BC | Boundary Condition | Domain boundary specification | derivation/BC_IC_GEOMETRY.md:24-95 • c31d0c9 | Periodic, Neumann, Dirichlet types |
| IC | Initial Condition | Initial state specification | derivation/BC_IC_GEOMETRY.md:96-145 • c31d0c9 | Front, bump, perturbation types |
| CFL | Courant-Friedrichs-Lewy | Stability condition | derivation/CONSTANTS.md:21 • 0922758 | Time step constraint; see [`cfl`](../derivation/CONSTANTS.md#const-cfl) |
| VDM | Void Dynamics Model | Physics theory name | derivation/SYMBOLS.md:1, EQUATIONS.md:1 • various | Overarching theory framework |
| DOF | Degrees of Freedom | System dimension | derivation/SYMBOLS.md:128 • 1060de4 | Edits per DOF per step (sparsity ratio) |

---

## 3) Indices & Ordering

| Role | Index letters | Ordering / Semantics | Source | Notes |
|---|---|---|---|---|
| Spatial sites (discrete) | $i, j$ | Lattice site index; $j \in \mathrm{nbr}(i)$ for neighbors | derivation/SYMBOLS.md:21-22 • 1060de4 | Discrete lattice indexing; $i$ for site, $j$ for neighbor |
| Spatial dimension | $d$ | Dimension of Euclidean space $\mathbb{R}^d$ | derivation/SYMBOLS.md:9 • 1060de4 | Usually 1D, 2D, or 3D |
| Channel/field component | $c$ | Channel index in multi-component field $\boldsymbol{\phi} \in \mathbb{R}^C$ | derivation/SYMBOLS.md:10 • 1060de4 | Labels field components; $\phi_c$ for channel $c$ |
| Time step (discrete) | $n$ | Discrete time index in $W_i^n$ | derivation/SYMBOLS.md:21 • 1060de4 | Superscript for discrete time |
| Continuous time | $t$ | Continuous time variable | derivation/SYMBOLS.md:9 • 1060de4 | Function argument $\phi(\mathbf{x},t)$ |
| Walker index | $w$ | Walker label in set $\mathcal{W}$ | derivation/SYMBOLS.md:13 • 1060de4 | Labels individual walkers; $\mathbf{x}_w$, $s_w$ |
| Objective/metric index | $k$ | Objective or metric label | derivation/SYMBOLS.md:80, 82 • 1060de4 | Budget $B_k$, score $\mathbf{g}_k$, heatmap $H_k$ |
| Bus hierarchy level | $\ell$ | Level in bus hierarchy | derivation/SYMBOLS.md:76 • 1060de4 | $\mathcal{B}_\ell$ at level $\ell$ |
| Neighbor set | $N(i)$ or $\mathrm{nbr}(i)$ | Set of neighbors of site $i$ | derivation/SYMBOLS.md:22, 32 • 1060de4 | Graph connectivity |
| Mode number | $m$ | Fourier mode index | derivation/CONSTANTS.md:25 • 0922758 | $m_{\max}$ for mode range |

---

## 4) Coordinate Systems & Orientation

No explicit coordinate system frames or handedness/orientation conventions are stated in the current repository. Spatial coordinates are denoted $\mathbf{x} \in \mathbb{R}^d$ without specifying a particular basis or orientation.

**Evidence:** derivation/SYMBOLS.md:9 • 1060de4 states `$\mathbf{x}\in\mathbb{R}^d$, $t$` as spatial coordinate and time, but does not define axes labels, handedness, or orientation.

---

## 5) Subscripts, Superscripts, Diacritics (semantics)

| Notation | Meaning (as used) | Example link | Source | Notes |
|---|---|---|---|---|
| $_c$ (subscript) | Channel index | `$\phi_c$` - field channel $c$ | derivation/SYMBOLS.md:10 • 1060de4 | Multi-channel field component |
| $_i$ (subscript) | Spatial site index | `$W_i(t)$` - node state at site $i$ | derivation/SYMBOLS.md:21 • 1060de4 | Discrete lattice site |
| $_w$ (subscript) | Walker index | `$\mathbf{x}_w(t)$` - walker position | derivation/SYMBOLS.md:65 • 1060de4 | Labels walkers |
| $_k$ (subscript) | Objective/metric index | `$B_k(t)$` - budget for objective $k$ | derivation/SYMBOLS.md:82 • 1060de4 | Objective labels |
| $_\ell$ (subscript) | Hierarchy level | `$\mathcal{B}_\ell$` - bus at level $\ell$ | derivation/SYMBOLS.md:76 • 1060de4 | Level in hierarchy |
| $_j$ (subscript) | Neighbor site index | `$W_j$` in sum over $j \in \mathrm{nbr}(i)$ | derivation/SYMBOLS.md:21-22 • 1060de4 | Neighbor lattice site |
| $_t$ (subscript) | Time derivative | `$\partial_t \phi$` - time derivative | derivation/SYMBOLS.md:10, EQUATIONS.md:14 • various | Partial derivative w.r.t. time |
| $_n$ (subscript) | Normal direction or discrete time | `$\partial_n u$` - normal derivative; $W_i^n$ - time step | BC_IC_GEOMETRY.md:50, SYMBOLS.md:21 • various | Context-dependent: boundary normal or time index |
| $^n$ (superscript) | Discrete time step | `$W_i^n$` - state at time step $n$ | derivation/SYMBOLS.md:21 • 1060de4 | Discrete time index |
| $^+$ (superscript) | Forward difference or positive edit | `$\Delta^+_{w,c}$` - sparse local patch edit | derivation/SYMBOLS.md:69 • 1060de4 | Plastic write operation |
| $^2$ (superscript) | Squared or second-order | `$\nabla^2$` - Laplacian; $c^2$ - speed squared | derivation/SYMBOLS.md:10, 47 • 1060de4 | Exponent or differential order |
| $^*$ (superscript) | Normalized or conjugate | `$c^*$` - normalized KPP speed | derivation/SYMBOLS.md:135 • 1060de4 | Dimensionless form |
| `\dot{}` (overdot) | Time derivative | `$\dot{W}_i$` - rate of change | derivation/SYMBOLS.md:21, 56 • 1060de4 | $\dot{W}_i = \frac{dW_i}{dt}$ |
| `\hat{}` (hat) | Estimator or dimensionless form | `$\hat{V}(\phi)$` - potential | derivation/EQUATIONS.md:187 • various | Fitted or dimensionless version |
| `\tilde{}` (tilde) | Rescaled or transformed variable | `$\tilde{t}, \tilde{x}$` - nondimensional coordinates | derivation/EQUATIONS.md:84, 87 • various | Dimensionless rescaling |
| `\prime` (prime) | Derivative or variant | `$V'(\phi)$` - derivative of potential | derivation/SYMBOLS.md:110 • 1060de4 | $V'(\phi) = \frac{dV}{d\phi}$ |
| `\text{subscript}` (text subscript) | Named subscript | `$\alpha_{\text{plast}}$` - plasticity scale | derivation/SYMBOLS.md:91 • 1060de4 | Multi-letter subscript names (upright) |
| `\mathrm{subscript}` (roman subscript) | Named subscript | `$m_{\text{eff}}, m_{\text{in}}, m_{\text{out}}$` | derivation/SYMBOLS.md:45-46 • 1060de4 | Named physical quantities (upright) |

---

## 6) Sign Conventions & Inequalities

| Convention | Statement (verbatim or minimal) | Appears in | Source |
|---|---|---|---|
| Laplacian sign | $\nabla^2 = \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2} + \cdots$ (positive semi-definite on lattice) | Diffusion term: $D\nabla^2\phi$ | derivation/SYMBOLS.md:10, EQUATIONS.md • various |
| d'Alembertian sign | $\Box = \partial_t^2 - c^2 \nabla^2$ | EFT wave operator | derivation/SYMBOLS.md:48 • 1060de4 |
| Tachyonic curvature | $\mu^2 > 0$ implies $V''(0) = -\mu^2 < 0$ (drives condensation) | Tachyon potential | derivation/SYMBOLS.md:42 • 1060de4 |
| Discrete Laplacian | $\sum_{j \in N(i)} (W_j - W_i)$ (standard site-centered form) | Discrete diffusion | derivation/SYMBOLS.md:21-22, axiomatic_theory_development.md:273 • various |
| CFL constraint | $\text{cfl} \le 0.5$ for stability | Time step: $\Delta t = \text{cfl} \cdot \frac{(\Delta x)^2}{2D}$ | derivation/CONSTANTS.md:21 • 0922758 |
| Sparsity constraint | $\kappa \ll 1$ (edits per DOF per step) | Keep system sparse | derivation/SYMBOLS.md:128 • 1060de4 |
| Time scale separation | $\epsilon \ll 1$ (slow/fast layer ratio) | Memory steering scale | derivation/SYMBOLS.md:92 • 1060de4 |
| Mach constraint (LBM) | $\mathrm{Ma} \ll 1$ for incompressible flow | LBM low-Mach regime | derivation/SYMBOLS.md:146 • 1060de4 |
| Void Mach constraint | $M_v < 1$ for stability | Void propagation speed | derivation/SYMBOLS.md:120 • 1060de4 |
| Plasticity limit | $\lVert \Delta^+ \rVert \le \alpha_{\text{plast}}$ | Write magnitude cap | derivation/SYMBOLS.md:91 • 1060de4 |
| Budget update | $B_k \leftarrow B_k - \text{cost}(\Delta^+)$ | Decrement on edit | derivation/SYMBOLS.md:82 • 1060de4 |
| Gate threshold | Pass if score $\ge \tau_k$ | Edit gating condition | derivation/SYMBOLS.md:83 • 1060de4 |

---

## 7) File/Anchor Naming Patterns (for cross-links)

| Artifact | Anchor/ID Pattern | Example | Source | Notes |
|---|---|---|---|---|
| Equations | `vdm-e-###` (header) | `VDM-E-001` - Agency/Consciousness Field Evolution | derivation/EQUATIONS.md:10 • 6885588 | Equation headers numbered sequentially |
| Equations (link) | `#vdm-e-###` | Link: `[VDM-E-012](../derivation/EQUATIONS.md#vdm-e-012)` | derivation/CANON_MAP.md:48 • 1060de4 | Link pattern for equations |
| Symbols | `sym-...` (not yet used) | Intended: `<a id="sym-phi_c"></a>` | derivation/CANON_MAP.md:56 • 1060de4 | Planned symbol anchors (not yet implemented) |
| Constants | `const-...` | `<a id="const-alpha"></a>` - `ALPHA` | derivation/CONSTANTS.md:10 • 0922758 | Constant anchors in CONSTANTS.md |
| Constants (link) | `#const-...` | Link: `[ALPHA](../derivation/CONSTANTS.md#const-alpha)` | derivation/CONSTANTS.md:10 • 0922758 | Link pattern for constants |
| Geometries | `geom-...` | `<a id="geom-1d-periodic-interval"></a>` | derivation/BC_IC_GEOMETRY.md:14 • c31d0c9 | Geometry anchors |
| Boundary Conditions | `bc-...` | `<a id="bc-periodic-1d-rd-dispersion"></a>` | derivation/BC_IC_GEOMETRY.md:26 • c31d0c9 | BC anchors |
| Initial Conditions | `ic-...` | `<a id="ic-..."></a>` (pattern used but no examples yet) | derivation/BC_IC_GEOMETRY.md • c31d0c9 | IC anchors (pattern established) |
| Data Products | `data-...` | `<a id="data-geom-index"></a>` | derivation/DATA_PRODUCTS.md:761 • various | Data product anchors |
| Algorithms | `vdm-a-###` (intended) | Not yet present | derivation/CANON_MAP.md:84 • 1060de4 | Planned algorithm IDs |
| Units/Normalization | `#...` (varied) | `<a id="kappa-l"></a>` - $\kappa L$ | derivation/UNITS_NORMALIZATION.md:203 • ec0833a | Varied anchor patterns |
| Metrics/KPIs | `kpi-...` (intended) | Not yet present | derivation/CANON_MAP.md • 1060de4 | Planned metric anchors |

---

### Linking rules (anchors only; no duplication)

* Symbols → `../derivation/SYMBOLS.md#sym-...` (pattern established but anchors not yet added)
* Equations → `../derivation/EQUATIONS.md#vdm-e-...` (headers like `VDM-E-001`)
* Units → `../derivation/UNITS_NORMALIZATION.md#...` (varied anchor patterns)
* Constants → `../derivation/CONSTANTS.md#const-...`
* Algorithms → `../derivation/ALGORITHMS.md#vdm-a-...` (pattern established but not yet used)
* Geometries → `../derivation/BC_IC_GEOMETRY.md#geom-...`
* Boundary Conditions → `../derivation/BC_IC_GEOMETRY.md#bc-...`
* Initial Conditions → `../derivation/BC_IC_GEOMETRY.md#ic-...`

**Note:** Symbol anchors (`sym-...`) are planned but not yet implemented in SYMBOLS.md. TODO: add symbol anchors to SYMBOLS.md to enable stable deep linking.

---

<!-- BEGIN AUTOSECTION: NAMING-INDEX -->
<!-- Tool-maintained list of anchors/slugs for quick lookup -->
<!-- END AUTOSECTION: NAMING-INDEX -->

## Change Log
- 2025-10-04 • conventions extracted from repository • 8e27c34
