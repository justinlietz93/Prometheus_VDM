<!-- DOC-GUARD: CANONICAL -->
# VDM Axioms (Discrete Lattice Foundation)

Last updated: 2025-10-09 (commit 09f871a)

**Scope:** Canonical list of axioms used by the Void Dynamics Model. This page declares axioms with minimal wording, anchors for cross-referencing, and source citations. All theorems, equations, and algorithms must reference these axioms rather than restate them.

**Rules:**

- GitHub-safe MathJax only ($...$ inline; no block environments).
- Provide a stable anchor per axiom: VDM-AX-00X.
- Cite sources from existing repository texts only.

<!-- markdownlint-disable MD033 -->

## Program Axioms (A0–A7) - Closure, Void, Local Causality, Symmetry, Metriplectic, Entropy, Scale, Measurability

These program-level axioms are used widely across theory and validation narratives. They complement (not replace) the discrete-lattice core below. Where needed, identify $\Psi\leftrightarrow W$ when mapping to the lattice instantiation.

### A0 - Closure  <a id="vdm-ax-a0"></a> <a id="vdm-ax-010"></a>

**Statement:** Only objects defined inside the framework are allowed; no external primitives as foundations.

**Notes:** Enforces formal closure and prevents importing unstated structures.

**Source:** Referenced in agency/canon proposals (e.g., `Derivation/Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md`).

---

### A1 - Void Primacy  <a id="vdm-ax-a1"></a> <a id="vdm-ax-011"></a>

**Statement:** A field $\Psi(x,t)$ encodes void fluctuations; all physical observables are functionals of $\Psi$ (and its derivatives).

**Notes:** Establishes a single carrier for observables; in lattice form, identify $\Psi\to W$.

**Source:** User-provided canonical list; see also `Derivation/OVERVIEW.md` void-field narrative.

---

### A2 - Local Causality  <a id="vdm-ax-a2"></a> <a id="vdm-ax-012"></a>

**Statement:** Dynamics are built from local functionals of the state; influence propagates finitely from $\Psi$ and its spatial/temporal derivatives.

**Notes:** Parabolic derived-limit (RD/Fisher–KPP) has no finite cone; we only claim front speeds there. Finite domain-of-dependence (cone) is asserted and tested only for the hyperbolic (J-only KG) limb or for an explicitly flagged hyperbolic RD regularization.

**Evidence:** KG J-only: cone verified with slope $\approx c$ using our locality runner; RD: front-speed gates only.

**Source:** Locality themes throughout `Derivation/axiomatic_theory_development.md` and KG diagnostics in canon.

---

### A3 - Symmetry  <a id="vdm-ax-a3"></a> <a id="vdm-ax-013"></a>

**Statement:** A group $\mathcal G$ acts on $\Psi$. Invariants under $\mathcal G$ generate conserved currents (Noether).

**Notes:**

- KG J-only: spatial translations $x \mapsto x + \varepsilon$ $\Rightarrow$ momentum; time translations $t \mapsto t + \varepsilon$ $\Rightarrow$ energy.
- Pure diffusion: spatial translation invariance $\Rightarrow$ mass conservation (under periodic/no-flux BCs).
- Reaction-only on-site ODE: no spatial symmetry; on-site logarithmic invariant is a diagnostic, not Noether.

**Numerical check:** Noether currents are checked numerically in the KG runner; totals drift $\le 10^{-8}$/period.

**Source:** Noether usage cited across canon; see `Derivation/Conservation_Law/` and overview.

---

### A4 - Dual Generators (Metriplectic Split)  <a id="vdm-ax-a4"></a> <a id="vdm-ax-014"></a>

**Statement:** With state $q\equiv(\Psi,\partial\Psi,\ldots)$,
$\partial_t q = J(q)\,\frac{\delta \mathcal I}{\delta q} + M(q)\,\frac{\delta \Sigma}{\delta q}$, with $J^\top=-J$ (skew/symplectic), $M^\top=M\ge 0$ (symmetric/metric), and degeneracies $J\,\frac{\delta\Sigma}{\delta q}=0$, $M\,\frac{\delta\mathcal I}{\delta q}=0$.

**Notes:** Canonical split used by metriplectic integrators and QC (two-grid order, Strang-defect, J-only reversibility). Diagnostics: compute $g_1 = \langle J, \, \delta\Sigma, \, \delta\Sigma \rangle$ and $g_2 = \langle M, \, \delta\mathcal I, \, \delta\mathcal I \rangle$ every $K$ steps; both must be $\le 10^{-10}$ (grid-refined).

**Source:** Implemented/validated in `ALGORITHMS.md` (VDM-A-013..019) and corresponding runners.

---

### A5 - Entropy Law  <a id="vdm-ax-a5"></a> <a id="vdm-ax-015"></a>

**Statement:** The entropy functional $\Sigma[q]$ is non-decreasing along trajectories; equality only at steady states.

**Notes:** H-theorem spirit; used in Lyapunov/entropy monitors and QC gates.

**Source:** Quality gates in algorithms; see metriplectic Lyapunov checks and RESULTS pages.

---

### A6 - Scale Program  <a id="vdm-ax-a6"></a> <a id="vdm-ax-016"></a>

**Statement:** Predictions are formulated in dimensionless groups; units themselves carry no physical claims.

**Notes:** Underpins scaling-collapse validations (e.g., A6 junction logistic universality).

**Source:** `Derivation/Collapse/PROPOSAL_A6_Collapse_v1.md` and RESULTS; canon uses dimensionless envelopes and gates.

---

### A7 - Measurability  <a id="vdm-ax-a7"></a> <a id="vdm-ax-017"></a>

**Statement:** Every nontrivial statement must map to concrete observables with a test protocol (falsifiable).

**Notes:** Codified via pre-registration, approvals, and artifacted KPIs in this repository.

**Source:** `Derivation/Writeup_Templates`, approvals policy in `Derivation/code/common/authorization/README.md`.

---

# A8 (Candidate) — Lietz Infinity Resolution

**Status:** CANDIDATE (awaiting T8 PASS)  
**Pointer:** Derivation/Proposals/PROPOSAL_T8_A8_Lietz_Infinity_Resolution_v1.md

**Statement (exact):**

In metriplectic scalar-field systems with tachyonic origin $V''(0)<0$ that admit pulled fronts with exponential tails, any finite-excess-energy large-domain trajectory must organize into a finite-depth hierarchical partition with logarithmic depth $N(L)=\Theta(\log(L/\lambda))$, scale-gap separation $\rho\in(\rho_{\min},\rho_{\max})$, and boundary energy/information concentration fractions $\alpha,\alpha_\mathcal{I}>0$.

**Promotion rule:** On PROPOSAL T8 PASS (G1–G8), copy this statement verbatim into `Canon/AXIOMS.md` as **A8**, update status here to **ACCEPTED**, and archive artifacts under `Derivation/code/outputs/axioms/a8_infinity_resolution/`.

---

## Immediate Corollaries (Used Throughout)

> These are not new axioms; they are direct deductions repeatedly referenced by canon files.

### VDM-AX-C01 - Discrete Euler–Lagrange Equations  <a id="vdm-ax-c01"></a>

From VDM-AX-004:
$$\frac{W_i^{n+1}-2W_i^n+W_i^{n-1}}{\Delta t^2} = J \sum_{j\in N(i)} (W_j^n - W_i^n) - V'(W_i^n).$$

**Source:** Derivation/axiomatic_theory_development.md ("Derivation 1.2.1: Discrete Euler-Lagrange Equations").

---

### VDM-AX-C02 - Continuum Limit and Exact Spatial Prefactor  <a id="vdm-ax-c02"></a>

On the cubic lattice, the continuum action derived from VDM-AX-004 yields
$$S = \int dt\, d^d x\, \Big[ \tfrac{1}{2}(\partial_t\phi)^2 - \tfrac{c^2}{2}|\nabla\phi|^2 - V(\phi) \Big], \quad c^2 = 2 J a^2.$$

**Source:** Derivation/axiomatic_theory_development.md ("Derivation 1.3.1: Exact Spatial Kinetic Prefactor" and "Derivation 2.1.1/2.1.2").

---

### VDM-AX-C03 - RD Limit (Overdamped Regime)  <a id="vdm-ax-c03"></a>

In the overdamped limit of the corollary equations: $\partial_t \phi = D\nabla^2\phi + f(\phi)$ with $D = c^2/\gamma$ and $f(\phi) = -V'(\phi)/\gamma$.

**Source:** Derivation/axiomatic_theory_development.md ("Derivation 2.1.2: Continuum Field Equation").

---

## Cross-References

- Equations: [VDM-E-011](EQUATIONS.md#vdm-e-011) (Discrete Action), [VDM-E-039](EQUATIONS.md#vdm-e-039) (Discrete field terms), [VDM-E-016](EQUATIONS.md#vdm-e-016), [VDM-E-090..094](EQUATIONS.md#vdm-e-090)
- Algorithms: Metriplectic steps and QC [VDM-A-013..021](ALGORITHMS.md#vdm-a-013)
- Constants: Spatial prefactor parameters appear indirectly via $c^2=2Ja^2$ (see related domain configs); numerical gates live in [CONSTANTS.md](CONSTANTS.md)

---

<!-- BEGIN AUTOSECTION: AXIOMS-INDEX -->
<!-- markdownlint-disable MD051 -->
<!-- Tool-maintained list of [VDM-AX-###](#vdm-ax-###) anchors for quick lookup -->
- [A0](#vdm-ax-a0) - Closure
- [A1](#vdm-ax-a1) - Void Primacy
- [A2](#vdm-ax-a2) - Local Causality
- [A3](#vdm-ax-a3) - Symmetry
- [A4](#vdm-ax-a4) - Dual Generators (Metriplectic Split)
- [A5](#vdm-ax-a5) - Entropy Law
- [A6](#vdm-ax-a6) - Scale Program
- [A7](#vdm-ax-a7) - Measurability
- [VDM-AX-001](#vdm-ax-001) - Field Variable (Discrete Scalar)
- [VDM-AX-002](#vdm-ax-002) - Lattice Structure (Regular Cubic)
- [VDM-AX-003](#vdm-ax-003) - Locality Principle (Nearest-Neighbor, One-Step Memory)
- [VDM-AX-004](#vdm-ax-004) - Discrete Action Principle (Stationary Action)
- [VDM-AX-C01](#vdm-ax-c01) - Discrete Euler–Lagrange Equations
- [VDM-AX-C02](#vdm-ax-c02) - Continuum Limit and Exact Spatial Prefactor
- [VDM-AX-C03](#vdm-ax-c03) - RD Limit (Overdamped Regime)
<!-- END AUTOSECTION: AXIOMS-INDEX -->
<!-- markdownlint-enable MD051 -->

## Change Log

- 2025-10-08 • refine A2/A3/A4 notes: diffusion vs cone and KG evidence; explicit symmetry groups and Noether drift bound; metriplectic degeneracy diagnostics • HEAD
- 2025-10-08 • add program axioms A0–A7 with stable anchors and cross-refs; preserve discrete core • HEAD
- 2025-10-08 • initialize axioms (AX-001..004 + corollaries C01..C03) from existing axiomatic_theory_development.md • HEAD

<!-- markdownlint-enable MD033 -->

