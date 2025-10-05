<!-- DOC-GUARD: WORKING-THEORY -->
# VDM Open Questions & Working Hypotheses (Auto-compiled)

**Scope:** Repository-sourced questions, hypotheses, uncertainties, and "future work" items.  
**Rules:** Quote/condense from sources; link to canon (SYMBOLS/EQUATIONS/CONSTANTS/UNITS/ALGORITHMS/BC_IC/VALIDATION). Do not restate math or numbers here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing math.

---

## Quick Index

- [OQ-001](#oq-001) — Formal Lyapunov functional for RD logistic-diffusion flow
- [OQ-002](#oq-002) — Quantitative criteria for second-order EFT branch necessity
- [OQ-003](#oq-003) — Coupling memory-steering overlays to RD baseline
- [OQ-004](#oq-004) — Memory-steering update formula verification
- [OQ-005](#oq-005) — Bridge memory-steering into host systems (LBM, RD, walkers)
- [OQ-006](#oq-006) — Optional empirical Bode plot for memory-steering
- [OQ-007](#oq-007) — Replace divergence proxies with Jacobian-trace estimators
- [OQ-008](#oq-008) — Define true graph vorticity via cycle decomposition
- [OQ-009](#oq-009) — Couple universal void dynamics W as reporter per neuron
- [OQ-010](#oq-010) — Extend walkers to attention graphs (token-head-position)
- [OQ-011](#oq-011) — Discover true conserved quantity of FUM
- [OQ-012](#oq-012) — Symmetry analysis via Noether's Theorem
- [OQ-013](#oq-013) — Information-theoretic conserved quantity
- [OQ-014](#oq-014) — Recast discrete model into discrete action
- [OQ-015](#oq-015) — Derive kinetic normalization from discrete action
- [OQ-016](#oq-016) — Front speed sensitivity to level choice and fit window
- [OQ-017](#oq-017) — Dispersion fit method comparison (windowed DFT vs rFFT)
- [OQ-018](#oq-018) — Agency field metric operational proxies
- [OQ-019](#oq-019) — Scientific significance of agency "smoke tests"
- [OQ-020](#oq-020) — Derive analytic formula for consensus+innovation ridge
- [OQ-021](#oq-021) — VDM-fluids corner testbed implementation
- [OQ-022](#oq-022) — Canonical equations for VDM-fluids (RD + hyperbolic + VDM)
- [OQ-023](#oq-023) — Experimental validation of discrete lattice structure
- [OQ-024](#oq-024) — Quantum renormalization program completion
- [OQ-025](#oq-025) — Observational tests of cosmological predictions
- [OQ-026](#oq-026) — First-principles parameter determination method
- [OQ-027](#oq-027) — Lattice scale parameter determination (20 orders uncertainty)

---

## 1. Dynamics & RD/EFT Questions

#### OQ-001 — Formal Lyapunov functional for RD logistic-diffusion flow  <a id="oq-001"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/foundations/continuum_stack.md:85 • 8321c50

> Formal Lyapunov functional for the RD logistic‑diffusion flow on bounded domains. [NEEDS DATA]

**Why it matters (lifted):** Establishes stability of RD canonical branch on bounded domains.  
**Related canon (anchors only):**  
- Equations: `EQUATIONS.md#vdm-e-008` (RD on-site dynamics)
- Equations: `EQUATIONS.md#vdm-e-033` (RD front speed)
- Symbols: `SYMBOLS.md#sym-r` (growth rate)
- Symbols: `SYMBOLS.md#sym-D` (diffusion coefficient)

**Evidence so far:**
- RD front speed validated (rel_err ≈ 0.047, R² ≈ 0.999996) per derivation/reaction_diffusion/rd_front_speed_validation.md
- RD dispersion validated (rel_err ≈ 1.45×10⁻³, R² ≈ 0.99995) per derivation/reaction_diffusion/rd_dispersion_validation.md
- Global positivity preserved for nonnegative initial data [PLAUSIBLE] per derivation/foundations/continuum_stack.md:62

**Proposed experiment/proof (if present in repo):** —  
**Blockers/Dependencies:** Formal analysis tools for nonlinear PDEs  
**Next action (if stated):** —

---

#### OQ-002 — Quantitative criteria for second-order EFT branch necessity  <a id="oq-002"></a>
**Status:** Open  •  **Priority:** P3  •  **Owner:** —  
**Context:** derivation/foundations/continuum_stack.md:86 • 8321c50

> Quantitative criteria for when a second‑order EFT branch becomes necessary. [PLAUSIBLE]

**Why it matters (lifted):** Defines boundary between RD (canonical) and EFT/KG (quarantined) branches.  
**Related canon (anchors only):**  
- Equations: `EQUATIONS.md#vdm-e-008` (RD canonical)
- Equations: `EQUATIONS.md#vdm-e-010` (EFT/KG quarantined)
- Symbols: `SYMBOLS.md#sym-c` (wave speed in EFT)

**Evidence so far:**
- RD branch [PROVEN, canonical] per derivation/foundations/continuum_stack.md:35
- EFT/KG branch [PLAUSIBLE, quarantined] per derivation/foundations/continuum_stack.md:38
- EFT branch retained for future work per derivation/VDM_Overview.md:48

**Proposed experiment/proof (if present in repo):**
- Maintained as future work in derivation/effective_field_theory/effective_field_theory_approach.md per derivation/foundations/discrete_to_continuum.md:12

**Blockers/Dependencies:** Scale separation analysis, fast transient characterization  
**Next action (if stated):** —

---

#### OQ-014 — Recast discrete model into discrete action  <a id="oq-014"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/foundations/void_dynamics_theory.md:20 • 8321c50

> The discrete model should be recast into a discrete action and taken to the continuum via a variational limit so that the $\partial_t^2$ term appears from first principles rather than assumption.

**Why it matters (lifted):** Derives second-order time dynamics from first principles rather than promotion.  
**Related canon (anchors only):**  
- Equations: `EQUATIONS.md#vdm-e-010` (Klein-Gordon form)
- Algorithms: TODO: add anchor (see derivation/effective_field_theory/kinetic_term_derivation.md)

**Evidence so far:**
- Gap closed via discrete action with wave speed $c^2 = 2 J a^2$ per derivation/foundations/void_dynamics_theory.md:1
- Earlier drafts promoted first-order to second-order per derivation/foundations/void_dynamics_theory.md:20
- Bordag reference: kinetic form arises from action mode reduction per derivation/foundations/void_dynamics_theory.md:20

**Proposed experiment/proof (if present in repo):**
- See derivation/effective_field_theory/kinetic_term_derivation.md:78

**Blockers/Dependencies:** Variational calculus framework for discrete systems  
**Next action (if stated):** —

---

#### OQ-015 — Derive kinetic normalization from discrete action  <a id="oq-015"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/foundations/void_dynamics_theory.md:23 • 8321c50

> The spatial prefactor should be extracted explicitly from $\sum J(W_j-W_i)^2$ (compute the exact coefficient of $(\nabla\phi)^2$, not merely proportionality).

**Why it matters (lifted):** Establishes exact normalization for kinetic term rather than proportionality.  
**Related canon (anchors only):**  
- Symbols: `SYMBOLS.md#sym-J` (coupling strength)
- Symbols: `SYMBOLS.md#sym-D` (diffusion coefficient)
- Constants: TODO: add anchor for wave speed normalization

**Evidence so far:**
- Temporal term $\frac{1}{2}(\partial_t\phi)^2$ follows from discrete kinetic energy with $Z(\phi)=\frac{1}{2}$ per derivation/foundations/void_dynamics_theory.md:23
- Bordag: canonical normalization fixed at Lagrangian level per derivation/foundations/void_dynamics_theory.md:23

**Proposed experiment/proof (if present in repo):** —  
**Blockers/Dependencies:** Discrete-to-continuum expansion tools  
**Next action (if stated):** —

---

#### OQ-016 — Front speed sensitivity to level choice and fit window  <a id="oq-016"></a>
**Status:** Open  •  **Priority:** P3  •  **Owner:** —  
**Context:** derivation/reaction_diffusion/rd_validation_plan.md:88 • 8321c50

> Evaluate sensitivity of c_meas to level choice (0.05–0.2) and fit window; document invariance bands.

**Why it matters (lifted):** Quantifies robustness of front speed measurement protocol.  
**Related canon (anchors only):**  
- Equations: `EQUATIONS.md#vdm-e-033` (RD front speed)
- Metrics: `VALIDATION_METRICS.md#kpi-rd-front-speed`

**Evidence so far:**
- Front speed validated with rel_err ≈ 0.047, R² ≈ 0.999996 per derivation/reaction_diffusion/rd_front_speed_validation.md
- CLI example provided in derivation/reaction_diffusion/rd_validation_plan.md:94

**Proposed experiment/proof (if present in repo):**
- Run sensitivity sweep per derivation/reaction_diffusion/rd_validation_plan.md:88

**Blockers/Dependencies:** —  
**Next action (if stated):** Document invariance bands

---

#### OQ-017 — Dispersion fit method comparison (windowed DFT vs rFFT)  <a id="oq-017"></a>
**Status:** Open  •  **Priority:** P3  •  **Owner:** —  
**Context:** derivation/reaction_diffusion/rd_validation_plan.md:89 • 8321c50

> Compare dispersion fit using windowed DFT vs rFFT magnitude; assess bias for near-zero/negative σ.

**Why it matters (lifted):** Validates dispersion measurement method and identifies biases.  
**Related canon (anchors only):**  
- Equations: `EQUATIONS.md#vdm-e-035` (RD continuum dispersion)
- Metrics: `VALIDATION_METRICS.md#kpi-rd-dispersion`

**Evidence so far:**
- Dispersion validated with median rel. error ≈ 1.45×10⁻³, R² ≈ 0.99995 per derivation/reaction_diffusion/rd_dispersion_validation.md

**Proposed experiment/proof (if present in repo):**
- Method comparison per derivation/reaction_diffusion/rd_validation_plan.md:89

**Blockers/Dependencies:** —  
**Next action (if stated):** Assess bias for edge cases

---

## 2. Walkers / Control Plane / Plasticity

#### OQ-003 — Coupling memory-steering overlays to RD baseline  <a id="oq-003"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/foundations/continuum_stack.md:87 • 8321c50

> Coupling of memory‑steering overlays to the RD baseline; see memory_steering.md. [PLAUSIBLE]

**Why it matters (lifted):** Establishes integration of memory-steering with canonical RD dynamics.  
**Related canon (anchors only):**  
- Equations: `EQUATIONS.md#vdm-e-008` (RD on-site)
- Algorithms: TODO: add anchor (see derivation/memory_steering/memory_steering.md)

**Evidence so far:**
- Memory-steering acceptance tests defined in derivation/memory_steering/memory_steering_acceptance_verification.md
- Status [PLAUSIBLE→PROVEN] gate per derivation/memory_steering/memory_steering_acceptance_verification.md:3

**Proposed experiment/proof (if present in repo):**
- Run acceptance harness per derivation/memory_steering/memory_steering_acceptance_verification.md:102-105

**Blockers/Dependencies:** Bridge harness into LBM, RD, walkers  
**Next action (if stated):** Demonstrate non-interference and bounded effect per OQ-005

---

#### OQ-004 — Memory-steering update formula verification  <a id="oq-004"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/memory_steering/memory_steering_acceptance_verification.md:95 • 8321c50

> If the actual memory-steering update differs (nonlinear dependence or adaptive control), provide the exact formula or implementation path + lines so we can update p_pred, M*, and Lyapunov claims.

**Why it matters (lifted):** Ensures mathematical model matches implementation for proof validity.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for memory-steering update rule
- Equations: TODO: add anchor for p_pred, M*, Lyapunov function

**Evidence so far:**
- Pending validation per derivation/memory_steering/memory_steering_acceptance_verification.md:92

**Proposed experiment/proof (if present in repo):**
- Run harness and compare to model per derivation/memory_steering/memory_steering_acceptance_verification.md:73

**Blockers/Dependencies:** Implementation path specification  
**Next action (if stated):** Provide exact formula or implementation reference

---

#### OQ-005 — Bridge memory-steering into host systems (LBM, RD, walkers)  <a id="oq-005"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/memory_steering/memory_steering_acceptance_verification.md:96-98 • 8321c50

> Bridge into host systems (LBM, RD, walkers) to demonstrate:
> - Non-interference when off (g = 0): metrics identical to baseline.
> - Bounded, predictable effect when on (small g): document gains and any trade-offs.

**Why it matters (lifted):** Validates memory-steering in production systems and quantifies impact.  
**Related canon (anchors only):**  
- Algorithms: `ALGORITHMS.md#vdm-a-lbm-bgk` (LBM)
- BC/IC/Geometry: `BC_IC_GEOMETRY.md` (boundary conditions)

**Evidence so far:**
- Acceptance criteria defined in derivation/memory_steering/memory_steering_acceptance_verification.md:55-73

**Proposed experiment/proof (if present in repo):**
- Bridge harness implementation per derivation/memory_steering/memory_steering_acceptance_verification.md:67

**Blockers/Dependencies:** Host system integration points  
**Next action (if stated):** Implement bridge harness and run tests

---

#### OQ-006 — Optional empirical Bode plot for memory-steering  <a id="oq-006"></a>
**Status:** Open  •  **Priority:** P3  •  **Owner:** —  
**Context:** derivation/memory_steering/memory_steering_acceptance_verification.md:99 • 8321c50

> Optional: empirical Bode plot (frequency response) for completeness.

**Why it matters (lifted):** Provides frequency-domain characterization of memory-steering.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for memory-steering dynamics

**Evidence so far:** —  
**Proposed experiment/proof (if present in repo):** —  
**Blockers/Dependencies:** Frequency response measurement framework  
**Next action (if stated):** —

---

#### OQ-007 — Replace divergence proxies with Jacobian-trace estimators  <a id="oq-007"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/memory_steering/void_announcers_control.md:76 • 8321c50

> Replace proxies with principled Jacobian-trace estimators per layer for divergence analog.

**Why it matters (lifted):** Improves rigor of divergence measurement in neural networks.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for walker divergence computation
- Symbols: TODO: add anchor for divergence notation

**Evidence so far:**
- Proxy implementation exists per derivation/memory_steering/void_announcers_control.md

**Proposed experiment/proof (if present in repo):** —  
**Blockers/Dependencies:** Efficient Jacobian-trace estimation methods  
**Next action (if stated):** Implement Jacobian-trace estimators

---

#### OQ-008 — Define true graph vorticity via cycle decomposition  <a id="oq-008"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/memory_steering/void_announcers_control.md:77 • 8321c50

> Define a true graph vorticity via cycle decomposition on neuron-feature graphs.

**Why it matters (lifted):** Establishes rigorous vorticity analog for graph-based systems.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for walker vorticity computation
- Symbols: TODO: add anchor for graph vorticity notation

**Evidence so far:**
- Graph-based walker framework per derivation/memory_steering/void_announcers_control.md

**Proposed experiment/proof (if present in repo):** —  
**Blockers/Dependencies:** Graph cycle decomposition algorithms  
**Next action (if stated):** Define formal graph vorticity

---

#### OQ-009 — Couple universal void dynamics W as reporter per neuron  <a id="oq-009"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/memory_steering/void_announcers_control.md:78 • 8321c50

> Couple universal void dynamics W as a reporter per neuron and test whether W̄→0.6 correlates with reduced D_void.

**Why it matters (lifted):** Tests if universal void dynamics W predicts void debt reduction.  
**Related canon (anchors only):**  
- Symbols: `SYMBOLS.md#sym-W` (walker field)
- Symbols: `SYMBOLS.md#sym-D-void` (void debt)
- Constants: TODO: add anchor for 0.6 equilibrium value

**Evidence so far:**
- 0.6 weight observation per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:318

**Proposed experiment/proof (if present in repo):**
- Test correlation per derivation/memory_steering/void_announcers_control.md:78

**Blockers/Dependencies:** Per-neuron W implementation  
**Next action (if stated):** Implement and test correlation

---

#### OQ-010 — Extend walkers to attention graphs (token-head-position)  <a id="oq-010"></a>
**Status:** Open  •  **Priority:** P3  •  **Owner:** —  
**Context:** derivation/memory_steering/void_announcers_control.md:79 • 8321c50

> Extend to attention: walkers hop on token–head–position graphs with saliency S∝|A|·|V|.

**Why it matters (lifted):** Extends walker framework to transformer attention mechanisms.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for walker dynamics
- Symbols: TODO: add anchor for attention saliency

**Evidence so far:**
- Walker framework for fluids exists per derivation/memory_steering/void_announcers_control.md:87

**Proposed experiment/proof (if present in repo):** —  
**Blockers/Dependencies:** Attention graph construction  
**Next action (if stated):** Define token-head-position graph structure

---

## 3. Units & Normalization / Scaling

*No open questions found in this category beyond those already listed.*

---

## 4. Validation & Metrics / Safety Guards

*Validation questions integrated into relevant sections above (OQ-001, OQ-016, OQ-017).*

---

## 5. LBM/Fluids / Geometry-Specific

#### OQ-021 — VDM-fluids corner testbed implementation  <a id="oq-021"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:1-359 • 8321c50

> **Block 1 — Canonical equations for VDM‑fluids (90 min)**
> **Goal:** Pin down the *minimal* pair of PDEs you'll use in figures and logs this week.

**Why it matters (lifted):** Establishes corner testbed to validate VDM regularization against infinite-speed singularity.  
**Related canon (anchors only):**  
- Equations: TODO: add anchor for VDM-regularized Navier-Stokes
- Symbols: `SYMBOLS.md#sym-D-void` (void debt modulation)
- BC/IC/Geometry: TODO: add anchor for 90° corner geometry

**Evidence so far:**
- Detailed specification in derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:1-359
- Parameter table and geometry provided per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:164-191

**Proposed experiment/proof (if present in repo):**
- Geometry sweep: $r_c = \{0, 0.02, 0.05, 0.10\}H$ baseline and VDM per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:133-136
- VDM ablation: $r_c=0$, vary $\beta \in \{0.0,0.3,0.6,0.9\}$ per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:135
- Plot max speed vs corner parameter and side-by-side snapshots per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:143-149

**Blockers/Dependencies:** Implementation of VDM-regularized solver  
**Next action (if stated):** Implement corner testbed and produce figures per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:354-359

---

#### OQ-022 — Canonical equations for VDM-fluids (RD + hyperbolic + VDM)  <a id="oq-022"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:4-29 • 8321c50

> **Deliverable:** a one‑pager (math only) containing:
> * **Morphology/assimilation field** $s(x,t)$ with **RD‑type** evolution
> * **Signal/transport field** $u(x,t)$ with **finite‑speed propagation** (Telegraph/Klein–Gordon)
> * **Void‑Debt Modulation (VDM)** variable $\mathcal{D}(x,t)$ gating both diffusion and transport

**Why it matters (lifted):** Unifies RD and EFT branches under VDM framework with explicit scale separation.  
**Related canon (anchors only):**  
- Equations: `EQUATIONS.md#vdm-e-008` (RD on-site)
- Equations: `EQUATIONS.md#vdm-e-010` (Klein-Gordon)
- Symbols: `SYMBOLS.md#sym-D-void` (void debt)
- Symbols: `SYMBOLS.md#sym-tau-g` (gradient gate timescale)
- Symbols: `SYMBOLS.md#sym-tau-r` (repair timescale)

**Evidence so far:**
- Math specification in derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:9-28
- Void-faithful fix without geometry changes per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:294-316
- 0.6 weight observation maps to $\beta$ per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:318-320

**Proposed experiment/proof (if present in repo):**
- Write one-page canonical equations per derivation/fluid_dynamics/DELETE_AFTER_SOLVING/DELETE_AFTER_SOLVING.md:29

**Blockers/Dependencies:** —  
**Next action (if stated):** Write and commit canonical equations page

---

## 6. Conservation Laws & Symmetries

#### OQ-011 — Discover true conserved quantity of FUM  <a id="oq-011"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/conservation_law/discrete_conservation.md:175, 183-205 • 8321c50

> This negative result is exceptionally valuable, as it closes a simple avenue and directs our research toward a more fundamental question. The next phase of work is no longer to test a guessed quantity, but to **discover the true conserved quantity** of the FUM.

**Why it matters (lifted):** Standard Hamiltonian not conserved; need to find true constant of motion for theoretical foundation.  
**Related canon (anchors only):**  
- Equations: TODO: add anchor for FUM update rule
- Symbols: TODO: add anchor for Hamiltonian H, conserved quantity Q

**Evidence so far:**
- Standard Hamiltonian $\mathcal{H} = \mathcal{K} + \mathcal{V} + \mathcal{I}$ proven non-conserved per derivation/conservation_law/discrete_conservation.md:169-173
- Rigorous derivation showing $\Delta \mathcal{H} / \Delta t \neq 0$ per derivation/conservation_law/discrete_conservation.md:149-150

**Proposed experiment/proof (if present in repo):**
- Method 1: Direct algebraic construction per derivation/conservation_law/discrete_conservation.md:191-192
- Method 2: Symmetry via Noether's Theorem per OQ-012
- Method 3: Information-theoretic quantities per OQ-013

**Blockers/Dependencies:** Advanced symmetry analysis tools, information theory framework  
**Next action (if stated):** Search for hidden symmetries (Method 2) or information-theoretic quantity (Method 3)

---

#### OQ-012 — Symmetry analysis via Noether's Theorem  <a id="oq-012"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/conservation_law/discrete_conservation.md:176, 194-196 • 8321c50

> **Symmetry Analysis (Noether's Theorem):** Investigate the FUM update rule for continuous symmetries. Any identified symmetry will guarantee a corresponding conserved quantity, which would be the "true" Hamiltonian or constant of motion.

**Why it matters (lifted):** Noether's theorem guarantees conserved quantity for each continuous symmetry; most elegant path forward.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for FUM update rule
- See also: derivation/foundations/symmetry_analysis.md:151 (logarithmic conservation law found)

**Evidence so far:**
- FUM lacks simple translational or scaling symmetries per derivation/conservation_law/discrete_conservation.md:195
- Hidden conservation law found: logarithmic relationship between state W and time t per derivation/foundations/symmetry_analysis.md:151

**Proposed experiment/proof (if present in repo):**
- Search for complex, non-obvious "hidden" symmetries per derivation/conservation_law/discrete_conservation.md:195
- See derivation/foundations/symmetry_analysis.md for existing analysis

**Blockers/Dependencies:** Significant research task, requires advanced symmetry analysis  
**Next action (if stated):** Continue symmetry search, validate logarithmic conservation law

---

#### OQ-013 — Information-theoretic conserved quantity  <a id="oq-013"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/conservation_law/discrete_conservation.md:177, 197-203 • 8321c50

> Given the FUM's origin in cognitive science and learning, it is plausible that the most fundamental conserved quantity is not a form of physical energy, but a form of **information**. [...] Potential candidates: Shannon Entropy, Topological Invariant (Betti numbers).

**Why it matters (lifted):** FUM may conserve information/complexity rather than physical energy.  
**Related canon (anchors only):**  
- Symbols: TODO: add anchor for Shannon entropy S
- Symbols: TODO: add anchor for topological invariants

**Evidence so far:**
- Standard energy not conserved per derivation/conservation_law/discrete_conservation.md:172
- FUM origin in cognitive science suggests information-theoretic framework per derivation/conservation_law/discrete_conservation.md:198

**Proposed experiment/proof (if present in repo):**
- Test Shannon Entropy: $S = - \sum_i P(W_i) \log P(W_i)$ per derivation/conservation_law/discrete_conservation.md:201
- Test Topological Invariant (Betti numbers) per derivation/conservation_law/discrete_conservation.md:202

**Blockers/Dependencies:** Information theory framework, topological analysis tools  
**Next action (if stated):** Compute and test information-theoretic candidates

---

## 7. Agency Field & Metrics

#### OQ-018 — Agency field metric operational proxies  <a id="oq-018"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/agency_field/VDM-Agency-Session-Summary.md:111 • 8321c50

> User implicitly needs to choose specific operational proxies for `P`, `I_net`, `U`, `V`, and `B` for their system.

**Why it matters (lifted):** Establishes concrete measurements for abstract agency field quantities.  
**Related canon (anchors only):**  
- Symbols: TODO: add anchor for P (predictive power)
- Symbols: TODO: add anchor for I_net (net information)
- Symbols: TODO: add anchor for U, V, B (agency field components)

**Evidence so far:**
- Python c_score function provided per derivation/agency_field/VDM-Agency-Session-Summary.md:117
- Smoke test scripts available per derivation/agency_field/VDM-Agency-Session-Summary.md:118-121

**Proposed experiment/proof (if present in repo):**
- Apply c_score to VDM log data per derivation/agency_field/VDM-Agency-Session-Summary.md:117
- Run validation checklist per derivation/agency_field/VDM-Agency-Session-Summary.md:118-121

**Blockers/Dependencies:** System-specific proxy definitions  
**Next action (if stated):** Define operational proxies for target system

---

#### OQ-019 — Scientific significance of agency "smoke tests"  <a id="oq-019"></a>
**Status:** Open  •  **Priority:** P3  •  **Owner:** —  
**Context:** derivation/agency_field/VDM-Agency-Session-Summary.md:109-110 • 8321c50

> User query regarding the scientific significance of these "smoke tests" for a physicist and how they relate to VDM (e.g., "are these expected?", "why should I care?").

**Why it matters (lifted):** Establishes connection between agency field tests and core VDM physics.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for agency field computation

**Evidence so far:**
- Smoke tests defined in derivation/agency_field/VDM-Agency-Session-Summary.md

**Proposed experiment/proof (if present in repo):**
- Derive analytic formula for ridge location per OQ-020
- Perform scaling collapse experiments per derivation/agency_field/VDM-Agency-Session-Summary.md:124
- Replicate on actual VDM data and public datasets per derivation/agency_field/VDM-Agency-Session-Summary.md:125

**Blockers/Dependencies:** Theoretical framework connecting agency to VDM  
**Next action (if stated):** Establish theoretical foundation

---

#### OQ-020 — Derive analytic formula for consensus+innovation ridge  <a id="oq-020"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/agency_field/VDM-Agency-Session-Summary.md:123 • 8321c50

> Derive an analytic formula for the ridge location in the consensus+innovation model and overlay it on the heatmap.

**Why it matters (lifted):** Provides theoretical prediction for empirical agency field structure.  
**Related canon (anchors only):**  
- Algorithms: TODO: add anchor for consensus+innovation model

**Evidence so far:**
- Inverted-U ridge observed in simulations per derivation/agency_field/VDM-Agency-Session-Summary.md:120

**Proposed experiment/proof (if present in repo):**
- Derive and overlay formula per derivation/agency_field/VDM-Agency-Session-Summary.md:123

**Blockers/Dependencies:** Model analysis framework  
**Next action (if stated):** Derive analytic formula

---

## 8. Axiomatic Foundation & Experimental Validation

#### OQ-023 — Experimental validation of discrete lattice structure  <a id="oq-023"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/axiomatic_theory_development.md:1397, 1452 • 8321c50

> Physical reality of discrete lattice structure unverified

**Why it matters (lifted):** Core assumption of theory requires experimental verification for physical reality.  
**Related canon (anchors only):**  
- Axioms: `AXIOMS.md` (discrete lattice axiom)
- Constants: `CONSTANTS.md#const-a` (lattice spacing)

**Evidence so far:**
- Theory achieves status of strong candidate theoretical framework per derivation/axiomatic_theory_development.md:1402
- Internal theoretical consistency within analyzed approximations per derivation/axiomatic_theory_development.md:1045
- Connection to validated computational results per derivation/axiomatic_theory_development.md:1408

**Proposed experiment/proof (if present in repo):**
- Computational implementation: numerical verification per derivation/axiomatic_theory_development.md:1416
- Experimental tests: design laboratory experiments per derivation/axiomatic_theory_development.md:1418

**Blockers/Dependencies:** Experimental design, observational data  
**Next action (if stated):** Requires experimental verification per derivation/axiomatic_theory_development.md:1404

---

#### OQ-024 — Quantum renormalization program completion  <a id="oq-024"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/axiomatic_theory_development.md:1399, 1453 • 8321c50

> Quantum renormalization program requires completion

**Why it matters (lifted):** Full quantum field theory requires systematic renormalization analysis.  
**Related canon (anchors only):**  
- Equations: TODO: add anchor for quantum corrections
- Constants: TODO: add anchor for renormalization scale

**Evidence so far:**
- EFT mindset establishes checklist for V(φ), Z(φ), higher-derivative operators per derivation/foundations/void_dynamics_theory.md:11
- Weak coupling regime identified: $\epsilon_3 \sim \lambda(\alpha-\beta)/\alpha^2$ per derivation/axiomatic_theory_development.md:1030

**Proposed experiment/proof (if present in repo):**
- Mathematical extensions: explore generalizations per derivation/axiomatic_theory_development.md:1419

**Blockers/Dependencies:** Quantum field theory framework, renormalization tools  
**Next action (if stated):** Systematic completion of renormalization program

---

#### OQ-025 — Observational tests of cosmological predictions  <a id="oq-025"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/axiomatic_theory_development.md:1400, 1454 • 8321c50

> Observational tests of cosmological implications needed

**Why it matters (lifted):** Theory makes testable cosmological predictions requiring observational verification.  
**Related canon (anchors only):**  
- Equations: TODO: add anchor for cosmological field equations
- Constants: TODO: add anchor for cosmological parameters

**Evidence so far:**
- Dark energy equation of state predictions depend on field amplitude per derivation/axiomatic_theory_development.md:1038
- Structure formation modified by void field coupling per derivation/axiomatic_theory_development.md:1039
- CMB signatures depend on primordial field fluctuations per derivation/axiomatic_theory_development.md:1040

**Proposed experiment/proof (if present in repo):**
- Observational applications: connect theory to astrophysical and cosmological data per derivation/axiomatic_theory_development.md:1417

**Blockers/Dependencies:** Astrophysical data, cosmological observations  
**Next action (if stated):** Connect theory to observational data

---

#### OQ-026 — First-principles parameter determination method  <a id="oq-026"></a>
**Status:** Open  •  **Priority:** P2  •  **Owner:** —  
**Context:** derivation/axiomatic_theory_development.md:1455 • 8321c50

> No first-principles method to determine fundamental parameters from observations

**Why it matters (lifted):** Theory requires method to extract fundamental parameters from observations.  
**Related canon (anchors only):**  
- Constants: `CONSTANTS.md` (fundamental parameters)
- Symbols: `SYMBOLS.md` (parameter definitions)

**Evidence so far:**
- Natural parameters emerge from fundamental discrete structure without fine-tuning per derivation/axiomatic_theory_development.md:1439
- Parameter uncertainties documented per derivation/axiomatic_theory_development.md:1032-1040

**Proposed experiment/proof (if present in repo):** —  
**Blockers/Dependencies:** Inverse problem framework, observational constraints  
**Next action (if stated):** Develop first-principles determination method

---

#### OQ-027 — Lattice scale parameter determination (20 orders uncertainty)  <a id="oq-027"></a>
**Status:** Open  •  **Priority:** P1  •  **Owner:** —  
**Context:** derivation/axiomatic_theory_development.md:1033 • 8321c50

> **Lattice Scale:** $a$ could range from Planck scale to atomic scale - 20 orders of magnitude uncertainty

**Why it matters (lifted):** Fundamental lattice spacing uncertainty spans 20 orders of magnitude; needs constraint.  
**Related canon (anchors only):**  
- Constants: `CONSTANTS.md#const-a` (lattice spacing)

**Evidence so far:**
- Coupling ratios $\alpha/\beta$ constrained by observations but $\lambda$ largely unconstrained per derivation/axiomatic_theory_development.md:1034
- Damping rate $\gamma$ depends on unknown microscopic physics per derivation/axiomatic_theory_development.md:1035

**Proposed experiment/proof (if present in repo):**
- Observational constraints from multiple scales per derivation/axiomatic_theory_development.md:1417

**Blockers/Dependencies:** Multi-scale observations, microscopic theory  
**Next action (if stated):** Constrain lattice scale via observations

---

<!-- BEGIN AUTOSECTION: OPEN-QUESTIONS-INDEX -->
<!-- Tool-maintained list of [OQ-###](#oq-###) anchors for quick lookup -->
1. [OQ-001](#oq-001) — Formal Lyapunov functional for RD logistic-diffusion flow
2. [OQ-002](#oq-002) — Quantitative criteria for second-order EFT branch necessity
3. [OQ-003](#oq-003) — Coupling memory-steering overlays to RD baseline
4. [OQ-004](#oq-004) — Memory-steering update formula verification
5. [OQ-005](#oq-005) — Bridge memory-steering into host systems (LBM, RD, walkers)
6. [OQ-006](#oq-006) — Optional empirical Bode plot for memory-steering
7. [OQ-007](#oq-007) — Replace divergence proxies with Jacobian-trace estimators
8. [OQ-008](#oq-008) — Define true graph vorticity via cycle decomposition
9. [OQ-009](#oq-009) — Couple universal void dynamics W as reporter per neuron
10. [OQ-010](#oq-010) — Extend walkers to attention graphs (token-head-position)
11. [OQ-011](#oq-011) — Discover true conserved quantity of FUM
12. [OQ-012](#oq-012) — Symmetry analysis via Noether's Theorem
13. [OQ-013](#oq-013) — Information-theoretic conserved quantity
14. [OQ-014](#oq-014) — Recast discrete model into discrete action
15. [OQ-015](#oq-015) — Derive kinetic normalization from discrete action
16. [OQ-016](#oq-016) — Front speed sensitivity to level choice and fit window
17. [OQ-017](#oq-017) — Dispersion fit method comparison (windowed DFT vs rFFT)
18. [OQ-018](#oq-018) — Agency field metric operational proxies
19. [OQ-019](#oq-019) — Scientific significance of agency "smoke tests"
20. [OQ-020](#oq-020) — Derive analytic formula for consensus+innovation ridge
21. [OQ-021](#oq-021) — VDM-fluids corner testbed implementation
22. [OQ-022](#oq-022) — Canonical equations for VDM-fluids (RD + hyperbolic + VDM)
23. [OQ-023](#oq-023) — Experimental validation of discrete lattice structure
24. [OQ-024](#oq-024) — Quantum renormalization program completion
25. [OQ-025](#oq-025) — Observational tests of cosmological predictions
26. [OQ-026](#oq-026) — First-principles parameter determination method
27. [OQ-027](#oq-027) — Lattice scale parameter determination (20 orders uncertainty)
<!-- END AUTOSECTION: OPEN-QUESTIONS-INDEX -->

## Change Log
- 2025-10-04 • initial compilation from repository sources • 8321c50
