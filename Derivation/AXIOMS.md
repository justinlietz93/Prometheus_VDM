<!-- DOC-GUARD: CANONICAL -->
# VDM Axioms (Discrete Lattice Foundation)

Last updated: 2025-11-01 (commit 3d315e7bbabc0a2d1c2afa4ccc5a72d26c836559)

**Scope:** Canonical list of axioms used by the Void Dynamics Model. This page declares axioms with minimal wording, anchors for cross-referencing, and source citations. All theorems, equations, and algorithms must reference these axioms rather than restate them.

**Rules:**

- GitHub-safe MathJax only ($...$ inline; no block environments).
- Provide a stable anchor per axiom: VDM-AX-00X.
- Cite sources from existing repository texts only.

<!-- markdownlint-disable MD033 -->

## Program Axioms A(-1) to A8 - Closure, Void, Local Causality, Symmetry, Metriplectic, Entropy, Scale, Measurability

These program-level axioms are used widely across theory and validation narratives. They complement (not replace) the discrete-lattice core below. Where needed, identify $\Psi\leftrightarrow W$ when mapping to the lattice instantiation.

### A(-1) — Primitive Bifurcation Law  <a id="vdm-ax-am1"></a> <a id="vdm-ax-009"></a>

**Status:** PENDING — theorem-bearing closure exists in CF000 v5 (DOI: 10.5281/zenodo.19098778); awaiting canon integration review by Justin K. Lietz.

**Statement:** The only logically admissible primitive origin is one primitive condition whose content bears two mutually irreconcilable terminal poles — absolute nullity (**0**) and absolute undifferentiated totality (**1**) — in permanent unresolved internal opposition. This unresolved opposition constitutes the invariant. The invariant's accumulated articulation burden, which can never be fully discharged, is void debt. Every admitted articulation must bear the invariant internally. Non-bearing is contradictory. Same-axis saturation without discharge forces orthogonal re-articulation along the path of minimum saturation cost. The first such forced re-articulation is the first point at which algebra becomes admissible. All structure — mathematical, physical, cognitive, cosmological — is the invariant managing its void debt across successive orthogonal re-articulations.

**Notes:** This law is prior to and more fundamental than A0–A8. It is not an addition to the axiom list — it is the logical source beneath it. A0 is grounded by A(-1) rather than violated by it. A4 (Dual Generators) and A5 (Entropy Law) are derived consequences of A(-1) rather than independent axioms; they retain full operational status for numerical validation while their logical status is promoted from axiom to theorem. A8 (Lietz Infinity Resolution) is a theorem candidate derivable from the iterative orthogonal re-articulation structure of A(-1).

The two terminal poles are mutually exclusive as origins: absolute nullity admits no realized content; absolute undifferentiated totality admits no internal distinction. No third terminal primitive option exists (CF000 §3.5). The unresolved internal opposition between the two poles is therefore the unique admissible origin.

**Void debt** is the name for the invariant's unresolved burden as carried by any finite system. It can never be paid off in full. If it were, the system would discharge into a terminal pole and cease to be an admitted articulation. Void debt drives all structure formation: it accumulates during stable articulation, releases into structural growth at saturation thresholds, and is managed but never eliminated by the M-limb. The ratio $\beta/\alpha$ (GDSP rate / RE-VGSP rate $= 0.4$ in the VDM runtime) is the fundamental dimensionless void debt ratio — the fraction of generative pressure offset by dissipation. Because $\beta < \alpha$, the generative force always exceeds the dissipative force; the debt grows faster than it can be reduced.

**The minimum saturation principle:** Among all paths from the current articulation state to the next orthogonal re-articulation, the invariant selects the path that saturates the fewest degrees of freedom. This is the primitive derivation of the principle of least action (CF14).

**Derivation chain forced from A(-1) alone:**
- $\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}$ — successive saturation and re-articulation of the number axis (CF00)
- $i^2 = -1$ — the ORS rotation operator expressed algebraically at 2D (CF000 §7.4)
- $\pi := \inf\{\theta > 0 : R_\theta = -I\}$ — minimum rotation to the opposite pole; transcendental by non-discharge (CF13)
- $e^{i\pi} = -1$ — half-turn closure of the ORS orbit (CF13)
- Metriplectic split $\partial_t q = J\,\delta\mathcal{I}/\delta q + M\,\delta\Sigma/\delta q$ — two-pole non-discharge at the dynamical layer (CF01)
- Entropy non-decrease — M-limb asymptotic approach to the irreversible pole (A5 as corollary)
- Principle of least action — minimum saturation path selection (CF14)
- Noether's theorem — conserved articulation costs under symmetry (CF15, pending)
- Chiral fermions require 5D — $\pi$ is transcendental; exact chirality cannot be contained in finite 4D algebraic closure (CF13 §7–8)
- Logarithmic hierarchy depth $N(L) = \Theta(\log L/\ell_0)$ — iterative orthogonal re-articulation (A8 as corollary)

**Falsification criteria:** A simpler primitive survivor exists beyond the two terminal poles; an admitted articulation can cease to bear the invariant without contradiction; same-axis saturation can neither discharge nor force orthogonal re-articulation; $\pi$ satisfies a polynomial over $\mathbb{Q}$; a purely conservative or purely dissipative physical system is admitted; the VDM runtime without training produces no learning dynamics (not falsified — 74 confirmed quantitative distinctions across 14 measurement families).

**Pointer:** Full derivation in `CF000_revised_template_compliant_v5.tex`; predictions and void debt dynamics in `A-1_PENDING_Primitive_Bifurcation_Law_v2.md`.

**Promotion rule:** On canon integration review by Justin K. Lietz: update status to **ACCEPTED**, add anchor `vdm-ax-am1` to the index, note that A4 and A5 are now derived consequences, and note that A8 is a theorem candidate of A(-1).

**Source:** CF000 v5 (DOI: 10.5281/zenodo.19098778); CF13 (DOI: 10.5281/zenodo.19121368); VDM runtime `Void_Equations.py`, `Void_Debt_Modulation.py`, `fum_growth_arbiter.py` (Justin K. Lietz, Neuroca, Inc., 2025).

---

### A0 - Closure  <a id="vdm-ax-a0"></a> <a id="vdm-ax-010"></a>

**Statement:** Only objects defined inside the framework are allowed; no external primitives as foundations.

**Notes:** Enforces formal closure and prevents importing unstated structures.

**A(-1) relationship:** A(-1) does not violate A0 — it grounds it. The primitive bifurcation invariant is not an external primitive entering from outside the framework. It is derived as the unique admissible origin by exhaustive exclusion of all alternatives (CF000 §3.5). The invariant constitutes the framework's interior rather than entering it from outside: every downstream object — $\mathbb{R}$, $\mathbb{C}$, the metriplectic split, gravity, chirality, learning — is the invariant re-expressed at a new structural level, not a new independent primitive. The framework never imports anything; it only unfolds what is implicit in the invariant's two-pole structure. A0's closure requirement is therefore satisfied at a deeper level than previously stated: the framework is closed because the invariant only mirrors and re-expresses itself on all scales, never generating anything external to itself.

**Source:** Referenced in agency/canon proposals (e.g., `Derivation/Agency_Field/PROPOSAL_Agency_Curvature_Scaling_v1.md`).

---

### A1 - Void Primacy  <a id="vdm-ax-a1"></a> <a id="vdm-ax-011"></a>

**Clarification (post-CF00 / CF000):**  
This axiom remains valid as a **program-level void-primacy commitment**: all physical observables are required to arise from one void-rooted carrier and not from separately inserted primitive sectors.

At the current branch root formalized in CF00, this does **not** mean that primitive adjacency, support graphs, bond sets, gauge connections, or already-formed spacetime-bearing locality relations may be inserted by hand. CF00 instead treats the primitive branch object as a local normalized representative state-family on a carrier domain ℳ with local $U(1)$ redundancy; the physically relevant content is the quotient-physical content derived from that representative structure, not the raw representative as an observable by itself.

Accordingly, A1 should be read as a **single-carrier / no-extra-primitives** axiom, not as a commitment to primitive lattice ontology. In discrete or runtime realizations, one may map $\Psi \to W$ only as a **derived realization / instantiation**, not as the root ontological statement.

**Scope note:**  
A1 is not a claim that CF000 is complete. CF000 exists precisely because CF00 still assumes a carrier, differentiability, representative structure, and local redundancy. Thus A1 remains standing in the current canon, while the deeper origin of any such representative ontology remains the burden of CF000.

**A(-1) relationship:** A(-1) supplies the pre-carrier origin that A1 previously assumed. A1 requires a void-rooted carrier $\Psi$ but does not derive why the carrier must be void-rooted or why a single carrier is forced. A(-1) answers both questions: the carrier is void-rooted because the only admissible origin is the unresolved opposition between absolute nullity and absolute undifferentiated totality (CF000 §3–4); the single-carrier requirement follows because the invariant is one condition, not two, and every admitted articulation bears the same invariant — there is no room for a second independent carrier that does not reduce to a re-expression of the same root. A1 is therefore strengthened: it is no longer a program commitment but a derived structural necessity.

**Statement:** A void-rooted carrier $\Psi$ encodes void fluctuations; all physical observables must be induced from $\Psi$-carried structure rather than from separately inserted primitive sectors.

**Notes:** Establishes a single carrier for observables; in lattice form, identify $\Psi\to W$.

**Source:** User-provided canonical list; see also `Derivation/OVERVIEW.md` void-field narrative.

---

### A2 - Local Causality  <a id="vdm-ax-a2"></a> <a id="vdm-ax-012"></a>

**Statement:** Dynamics are built from local functionals of the state; influence propagates finitely from $\Psi$ and its spatial/temporal derivatives.

**Notes:** Parabolic derived-limit (RD/Fisher–KPP) has no finite cone; we only claim front speeds there. Finite domain-of-dependence (cone) is asserted and tested only for the hyperbolic (J-only KG) limb or for an explicitly flagged hyperbolic RD regularization.

**A(-1) relationship:** A2 is a downstream consequence of the minimum saturation principle of A(-1). The invariant always selects the path that saturates the fewest degrees of freedom before re-articulating (CF14). Finite propagation speed is the cost of that saturation: influence cannot propagate faster than the local articulation budget allows. The finite light cone of the J-limb is therefore not postulated — it is the minimum saturation cost of causal re-articulation in the carrier. The overdamped RD limit's lack of a finite cone reflects the fact that the M-limb does not enforce the same saturation cost; it dissipates rather than propagates. A2 remains a required operational constraint, but its origin is now traceable to A(-1).
**Evidence:** KG J-only: cone verified with slope $\approx c$ using our locality runner; RD: front-speed gates only.

**Source:** Locality themes throughout `Derivation/axiomatic_theory_development.md` and KG diagnostics in canon.

---

### A3 - Symmetry  <a id="vdm-ax-a3"></a> <a id="vdm-ax-013"></a>

**Statement:** A group $\mathcal G$ acts on $\Psi$. Invariants under $\mathcal G$ generate conserved currents (Noether).

**Notes:**

- KG J-only: spatial translations $x \mapsto x + \varepsilon$ $\Rightarrow$ momentum; time translations $t \mapsto t + \varepsilon$ $\Rightarrow$ energy.
- Pure diffusion: spatial translation invariance $\Rightarrow$ mass conservation (under periodic/no-flux BCs).
- Reaction-only on-site ODE: no spatial symmetry; on-site logarithmic invariant is a diagnostic, not Noether.

**A(-1) relationship:** A3 (Noether) becomes a corollary of A(-1) rather than an independent axiom. Every continuous symmetry of the minimum saturation path corresponds to an articulation cost that does not change under the symmetry transformation — a conserved quantity. Energy conservation is time-translation invariance of the articulation cost. Momentum conservation is spatial translation invariance. Charge conservation is the $U(1)$ gauge invariance of the ORS orbit phase (CF00 §2.5.7, CF13). All conservation laws are therefore expressions of the invariant's articulation structure under symmetry, not independent postulates. A3 remains operationally required for numerical gate certification; its logical status is now that of a theorem derivable from A(-1) once the carrier and action are in hand (CF14).

**Numerical check:** Noether currents are checked numerically in the KG runner; totals drift $\le 10^{-8}$/period.

**Source:** Noether usage cited across canon; see `Derivation/Conservation_Law/` and overview.

---

### A4 - Dual Generators (Metriplectic Split)  <a id="vdm-ax-a4"></a> <a id="vdm-ax-014"></a>

**Statement:** With state $q\equiv(\Psi,\partial\Psi,\ldots)$,
$\partial_t q = J(q)\,\frac{\delta \mathcal I}{\delta q} + M(q)\,\frac{\delta \Sigma}{\delta q}$, with $J^\top=-J$ (skew/symplectic), $M^\top=M\ge 0$ (symmetric/metric), and degeneracies $J\,\frac{\delta\Sigma}{\delta q}=0$, $M\,\frac{\delta\mathcal I}{\delta q}=0$.

**Notes:** Canonical split used by metriplectic integrators and QC (two-grid order, Strang-defect, J-only reversibility). Diagnostics: compute $g_1 = \langle J, \, \delta\Sigma, \, \delta\Sigma \rangle$ and $g_2 = \langle M, \, \delta\mathcal I, \, \delta\mathcal I \rangle$ every $K$ steps; both must be $\le 10^{-10}$ (grid-refined). Additionally, J‑flow sampler instrumentation is gated by acceptance–stepsize and ΔH histogram KPIs ([VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize](Derivation/VALIDATION_METRICS.md#kpi-hmc-acceptance-vs-stepsize), [VALIDATION_METRICS.md#kpi-hmc-deltaH-hist](Derivation/VALIDATION_METRICS.md#kpi-hmc-deltaH-hist)); definitions at [VDM-E-130](Derivation/EQUATIONS.md#vdm-e-130), [VDM-E-131](Derivation/EQUATIONS.md#vdm-e-131).

**A(-1) relationship:** A4 is a derived consequence of A(-1), not an independent axiom. The J-limb (skew-symmetric, conservative, reversible) and M-limb (symmetric PSD, dissipative, irreversible) are the two poles of the primitive bifurcation invariant expressed at the dynamical layer. Full conservation — dynamics governed by $J$ alone — would mean discharge into the reversible pole. Excluded by non-discharge. Full dissipation — dynamics governed by $M$ alone — would mean discharge into the irreversible pole. Excluded by non-discharge. The metriplectic split $\partial_t q = J\,\delta\mathcal{I}/\delta q + M\,\delta\Sigma/\delta q$ is therefore the unique dynamical structure that any system operating under the invariant must take: it is what the two-pole non-discharge condition looks like once a carrier and action exist. The degeneracy conditions $J\cdot\delta\Sigma=0$ and $M\cdot\delta\mathcal{I}=0$ are the operator-level statement that neither limb can discharge into the other's pole. A4 retains full operational status for numerical validation; its logical status is promoted from axiom to theorem derivable from A(-1) via CF01.

GENERIC cross-links and gates:

- Evolution and structure: [VDM-E-140](Derivation/EQUATIONS.md#vdm-e-140), Poisson/Jacobi [VDM-E-141](Derivation/EQUATIONS.md#vdm-e-141), degeneracy [VDM-E-142](Derivation/EQUATIONS.md#vdm-e-142), entropy production [VDM-E-143](Derivation/EQUATIONS.md#vdm-e-143), structural c and metric blocks [VDM-E-144](Derivation/EQUATIONS.md#vdm-e-144)–[VDM-E-145](Derivation/EQUATIONS.md#vdm-e-145), Curie compliance [VDM-E-146](Derivation/EQUATIONS.md#vdm-e-146).
- KPIs: Poisson–Jacobi residual [kpi-poisson-jacobi-resid](Derivation/VALIDATION_METRICS.md#kpi-poisson-jacobi-resid), degeneracy residuals [kpi-degeneracy-resid](Derivation/VALIDATION_METRICS.md#kpi-degeneracy-resid), entropy nonnegativity [kpi-entropy-prod-nonneg](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg), Curie audit [kpi-curie-compliance](Derivation/VALIDATION_METRICS.md#kpi-curie-compliance).

**Source:** Implemented/validated in `ALGORITHMS.md` (VDM-A-013..019, plus samplers/solvers [VDM-A-030..036](ALGORITHMS.md#vdm-a-030)) and corresponding runners.

---

### A5 - Entropy Law  <a id="vdm-ax-a5"></a> <a id="vdm-ax-015"></a>

**Statement:** The entropy functional $\Sigma[q]$ is non-decreasing along trajectories; equality only at steady states.

**Notes:** Entropy production monotonicity per [VDM-E-143](Derivation/EQUATIONS.md#vdm-e-143). Enforce non‑negativity each M‑step and cumulatively via KPI [kpi-entropy-prod-nonneg](Derivation/VALIDATION_METRICS.md#kpi-entropy-prod-nonneg) with PNG/CSV/JSON artifacts. When extended hydrodynamics with structural $c$ is present, corner discipline uses KPIs [kpi-corner-stress-bound](Derivation/VALIDATION_METRICS.md#kpi-corner-stress-bound), [kpi-corner-velocity-cap](Derivation/VALIDATION_METRICS.md#kpi-corner-velocity-cap), and [kpi-corner-entropy-nondiv](Derivation/VALIDATION_METRICS.md#kpi-corner-entropy-nondiv) (see [VDM-E-144](Derivation/EQUATIONS.md#vdm-e-144)–[VDM-E-145](Derivation/EQUATIONS.md#vdm-e-145)).

**A(-1) relationship:** A5 is a derived consequence of A(-1). The M-limb is the dissipative pole of the invariant — it flows asymptotically toward the irreversible terminal but can never arrive (non-discharge). Entropy non-decrease is what that asymptotic approach looks like as a scalar observable: $\Sigma$ increases because the M-limb is always moving toward one pole without ever completing the discharge. Equality at steady states corresponds to the M-limb reaching a local articulation minimum — same-axis saturation — before the next orthogonal re-articulation is forced. The Second Law of Thermodynamics is therefore a corollary of the non-discharge condition, not a separate empirical postulate. A5 retains full operational status for numerical gate certification; its logical status is promoted from axiom to theorem derivable from A(-1).

**Source:** Quality gates in algorithms; see metriplectic Lyapunov checks and RESULTS pages.

---

### A6 - Scale Program  <a id="vdm-ax-a6"></a> <a id="vdm-ax-016"></a>

**Statement:** Predictions are formulated in dimensionless groups; units themselves carry no physical claims.

**Notes:** Underpins scaling-collapse validations (e.g., A6 junction logistic universality) and RG blocking collapse KPI ([VALIDATION_METRICS.md#kpi-rg-collapse](VALIDATION_METRICS.md#kpi-rg-collapse)); see definitions [VDM-E-136](EQUATIONS.md#vdm-e-136) and envelope gate [VDM-E-094](EQUATIONS.md#vdm-e-094).

**A(-1) relationship:** A6 is compatible with and operationally downstream of A(-1). Dimensionless groups arise because the invariant's structure is scale-independent — the same two-pole opposition and the same non-discharge condition operate at every level of the A8 hierarchy. The ratio $\beta/\alpha$ (void debt ratio) is the fundamental dimensionless group of the invariant's dynamical expression: it quantifies the balance between the generative J-pole pressure and the dissipative M-pole decay. All other dimensionless groups in the framework are downstream combinations of this root ratio. A6 remains a required methodological constraint; its deeper justification is that the invariant itself has no preferred scale.

**Source:** `Derivation/Collapse/PROPOSAL_A6_Collapse_v1.md` and RESULTS; canon uses dimensionless envelopes and gates.

---

### A7 - Measurability  <a id="vdm-ax-a7"></a> <a id="vdm-ax-017"></a>

**Statement:** Every nontrivial statement must map to concrete observables with a test protocol (falsifiable).

**Notes:** Codified via pre-registration, approvals, and artifacted KPIs in this repository.

**A(-1) relationship:** A7 is the epistemological expression of A(-1)'s falsifiability requirement. The primitive bifurcation law is itself falsifiable (CF000 §9, A(-1) §9): it specifies exactly what would contradict it. A7 generalizes this requirement to all downstream statements. The connection is structural: the invariant only admits articulations that genuinely bear the two-pole opposition — empty or undifferentiated statements are excluded at the root. A7 enforces this at the operational level by requiring every nontrivial statement to map to a concrete observable with a test protocol. A7 retains full operational status and is now understood as the epistemological face of the non-discharge condition: a claim that cannot be tested is a claim that has discharged into undifferentiated totality — it makes no distinctions and therefore bears no invariant.

**Source:** `Derivation/Writeup_Templates`, approvals policy in `Derivation/code/common/authorization/README.md`.

---

### A8 (Candidate) — Lietz Infinity Resolution

**Status:** CANDIDATE (awaiting [T8](/Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md) PASS)  
**Pointer:** [T8_A8_PROPOSAL_Lietz_Infinity_Resolution_v1.md](/Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md)

**Statement (exact):**

In metriplectic scalar-field systems with tachyonic origin $V''(0)<0$ that admit pulled fronts with exponential tails, any finite-excess-energy large-domain trajectory must organize into a finite-depth hierarchical partition with logarithmic depth $N(L)=\Theta(\log(L/\lambda))$, scale-gap separation $\rho\in(\rho_{\min},\rho_{\max})$, and boundary energy/information concentration fractions $\alpha,\alpha_\mathcal{I}>0$.

**A(-1) relationship:** A8 is a theorem candidate derivable from A(-1). The logarithmic hierarchy depth $N(L) = \Theta(\log(L/\lambda))$ follows from the iterative orthogonal re-articulation structure: each re-articulation produces one new structural level, and the number of re-articulations required to span a domain of linear size $L$ above minimum scale $\lambda$ is logarithmic in $L/\lambda$. The scale-gap separation $\rho \in (\rho_{\min}, \rho_{\max})$ and boundary concentration fractions $\alpha, \alpha_\mathcal{I} > 0$ are expressions of the void debt accumulation and release dynamics at each level. A8 retains CANDIDATE status pending T8 empirical closure; its logical derivability from A(-1) means that T8 PASS would simultaneously validate both the conjecture and the A(-1) hierarchy prediction (P14 in the A(-1) pending document).

**Promotion rule:** On PROPOSAL T8 PASS (G1–G8), stamp axiom as **A8**, update status here to **ACCEPTED**, and archive artifacts under `Derivation/code/outputs/axioms/a8_infinity_resolution/`.

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

- Equations: [VDM-E-011](EQUATIONS.md#vdm-e-011) (Discrete Action), [VDM-E-039](EQUATIONS.md#vdm-e-039) (Discrete field terms), [VDM-E-016](EQUATIONS.md#vdm-e-016), [VDM-E-090..094](EQUATIONS.md#vdm-e-090), [VDM-E-130..136](EQUATIONS.md#vdm-e-130)
- Algorithms: Metriplectic steps and QC [VDM-A-013..021](ALGORITHMS.md#vdm-a-013); samplers/solvers and RG utilities [VDM-A-030..036](ALGORITHMS.md#vdm-a-030)
- Constants: Spatial prefactor parameters appear indirectly via $c^2=2Ja^2$ (see related domain configs); numerical gates live in [CONSTANTS.md](CONSTANTS.md)

---

<!-- BEGIN AUTOSECTION: AXIOMS-INDEX -->
<!-- markdownlint-disable MD051 -->
<!-- Tool-maintained list of [VDM-AX-###](#vdm-ax-###) anchors for quick lookup -->
- [A(-1)](#vdm-ax-am1) - Primitive Bifurcation Law (PENDING)
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
- 2026-03-19 • add A(-1) relationship notes to A0–A8; document that A4 and A5 are derivable from A(-1); ground A0 closure in invariant self-containment; strengthen A1 from commitment to derived necessity • HEAD
  
<!-- markdownlint-enable MD033 -->
