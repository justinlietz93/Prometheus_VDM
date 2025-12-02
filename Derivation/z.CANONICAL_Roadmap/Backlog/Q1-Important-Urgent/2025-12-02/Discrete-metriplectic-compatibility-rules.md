Eisenhower quadrant for this: **Q1 — Important + Urgent**
If the metriplectic core / integrator is even slightly wrong, every higher-level VDM result can be questioned. This is foundational.

**Topic / object:**
Structure-preserving GENERIC / metriplectic integrators (with auxiliary variables) for the VDM KG+RD core and toy ODEs.

**External anchors:**

* Peletier & Seri – geometric GENERIC on manifolds (degenerate Poisson + co-metric + unimodularity).
* Andrews & Farrell – conservative + dissipative discretizations of GENERIC systems with auxiliary variables (AV) and time-FEM.

**High-level goal in your stack (one-liner):**
Give the VDM metriplectic engine a **provably structure-preserving discrete kernel** (H conserved, S monotone, causal) so all void/cosmology/SIE meters sit on solid thermodynamic ground.

---

## 1. What Future-Justin should open first (from your own work)

Open these in roughly this order.

1. `Current_TODO.md` (the “Unifying Existing Work” doc you just dropped)
   Reason: Confirms this is aligned with item **1. Finish metriplectic KG+RD core** and the new ACSP exemplar (1b). 

2. `AXIOMS.md`
   Reason: To recall the precise **J⊕M axioms** (degeneracy, non-interaction of H and S, causality/finite speed constraints).

3. `SYMBOLS.md`
   Reason: Get the canonical names of `J`, `M`, `H[Φ]`, `S[Φ]`, lattice fields `Φ_i`, momenta `Π_i`, and any discrete operators `∇_d`, `Δ_d` so you don’t invent new notations in the integrator paper.

4. `EQUATIONS.md` (esp. VDM-E-107,-108,-109,-106) 
   Reason: These are already flagged in your TODO as the core VDM equations – especially the KG+RD engine and J/M brackets the numerics must respect.

5. `RESULTS_Metriplectic_Structure_Checks.md`
   Reason: This is your existing “does this implementation actually satisfy degeneracy / H & S constraints?” sanity check. The new work will extend and harden these tests.

6. `RESULTS_Metriplectic_JMJ_RD_v1.md` and `RESULTS_KG_RD_Metriplectic.md`
   Reason: They encode the current KG+RD metriplectic engine behavior, Strang splitting behavior, and any drift you’ve already observed.

7. `CF4_Telegraph_Fisher_Causality.md`
   Reason: This is your causal transport spec. Any new integrator must not break the finite-speed cone or telegraph-like behavior when lifted to PDEs.

8. Code: your current metriplectic engine + integrators
   Paths will be approximate, but open whatever you currently use in the KG+RD tests:

   * `Derivation/code/core/metriplectic_engine/*.py`
   * `Derivation/code/physics/common/integrators/*.py`
   * `Derivation/code/physics/lattice/kg_rd/*.py`
     Reason: You’ll graft the AV / structure-preserving scheme into these rather than starting from scratch.

9. ACSP / Lindblad exemplar scaffold (from item 1b in TODO) 

   * Any `CF*` or `T*_PROPOSAL_*` you’ve started for **ACSP → Lindblad SU(2) metriplectic exemplar**.
     Reason: SU(2) / Bloch-ball is a clean finite-dimensional testbed for J⊕M + AV integrator before PDEs.

---

## 2. Canonical equations and objects to reuse (not reinvent)

Use these as fixed anchors. Don’t re-derive them; just reference and implement.

1. **Metriplectic split (J⊕M)**

   * Objects: `J(Ψ)`, `M(Ψ)`, energy `H[Ψ]`, entropy `S[Ψ]`.
   * Brackets:

     * Poisson: `{F,G}_J = ⟨∇F, J ∇G⟩`
     * Metric: `(F,G)_M = ⟨∇F, M ∇G⟩`
   * Evolution:
     [
     \dot Ψ = J(Ψ),∇H[Ψ] + M(Ψ),∇S[Ψ]
     ]
     Use this as the **canonical continuum form**. Role: defines what “correct” means; integrator must approximate this while preserving:
   * `J = -Jᵀ` (skew)
   * `M = Mᵀ ≥ 0` (psd)
   * `M ∇H = 0` (H in null of M)
   * `J ∇S = 0` (S a Casimir of J)

2. **Discrete J_d and M_d on the lattice**

   * Objects: `J_d(Φ)`, `M_d(Φ)` acting on the stacked state `(Φ_i, Π_i, …)`.
   * Constraints to reuse:

     * `J_d = -J_dᵀ` exactly.
     * `M_d = M_dᵀ` and numerically psd (eigenvalues ≥ 0 to tolerance).
     * `J_d ∇_d S_d = 0`, `M_d ∇_d H_d = 0` up to machine precision.
       Role: These are **not negotiable**; all AV/integrator tricks must respect these algebraic facts.

3. **Lattice KG energy H_d[Φ,Π]**

   * Standard discrete Klein–Gordon Hamiltonian:
     [
     H_d = \sum_i \left(\frac{1}{2} Π_i^2 + \frac{1}{2} (\nabla_d Φ)_i^2 + V(Φ_i)\right),Δx^d
     ]
     Role: This is your **canonical energy functional** for the scalar void field. Do not invent a new one; just ensure the discrete integrator conserves this (or the AV-modified version of it) to the specified tolerance.

4. **Lattice entropy S_d[Φ]**

   * Whatever you currently use in the metriplectic KG+RD docs (e.g. local convex `s(Φ_i)` + possibly gradient terms).
     Role: Provides the **entropy gradient** that the metric part aligns with. For this project, treat its exact functional form as fixed; your task is to make `dS_d/dt ≥ 0` at the discrete level.

5. **Reaction–diffusion metric operator (RD part)**

   * Symbolically:
     [
     (∂_t Φ)_M = (M_d ∇_d S_d)_Φ ≈ D Δ_d μ[Φ] + …
     ]
     where `μ` is a chemical potential derived from `S_d`.
     Role: Use the existing form as the **metric piece**; don’t re-invent RD physics. You’re only changing time discretization / AV handling.

6. **Telegraph / causality constraints (CF4)**

   * Key relation: effective propagation speed `c = √(D/τ)` and finite-speed theorem for fronts.
     Role: Use this to define **causal stability gates**: no integrator is acceptable if it breaks the telegraph cone or lets information outrun `c` on the lattice.

7. **SU(2) / Bloch-ball metriplectic form (from ACSP exemplar)**

   * State: Bloch vector `r ∈ ℝ³`, |r| ≤ 1.
   * Hamiltonian part: `\dot r_H = Ω × r`.
   * Metric part: double-bracket / GKSL-equivalent dissipator `\dot r_M = -Γ (r - r_* ) + …`.
     Role: This is your **finite-dimensional testbed** for the AV integrator: if you can’t keep purity / entropy behavior correct here, don’t trust PDEs.

---

## 3. Concrete extraction / implementation procedure

Think of this in two layers: (A) toy ODE metriplectic integrator with AV, then (B) lift to KG+RD lattice.

### A. Build and test an AV-enhanced GENERIC integrator on a toy system

**Target toy:** Damped Hamiltonian pendulum or SU(2)/Bloch-ball.

1. **Define state and functionals**

   1. Choose a simple metriplectic toy:

      * Option 1: pendulum `(q,p)` with

        * `H(q,p)` = standard pendulum energy
        * `S(q,p)` = quadratic or log entropy chosen so that the dissipative part reproduces linear friction.
      * Option 2: Bloch ball `r` with

        * `H(r)` = Zeeman energy
        * `S(r)` = von Neumann / quadratic entropy on Bloch vector.
   2. Implement `H(x)`, `S(x)`, gradients `∇H`, `∇S`.

2. **Define continuous J and M for the toy**

   1. Implement `J` as a fixed matrix:

      * Pendulum: `J = [[0,1],[-1,0]]`.
      * Bloch: generator of cross product (3×3 skew matrix).
   2. Implement `M(x)` as a symmetric psd matrix with the correct nullspace:

      * Ensure `M ∇H = 0` (e.g., project out ∇H direction).
      * For Bloch, align `M` so it contracts toward fixed point `r_*` while preserving constraints.

3. **Introduce auxiliary variables (AV)**

   1. Add scalar AVs `E` and `Ξ` to track:

      * `E` ~ discrete energy constraint (target H).
      * `Ξ` ~ entropy production or dissipative potential.
   2. Extend the system:

      * State becomes `z = (x, E, Ξ)`.
      * Construct an extended Hamiltonian `Ĥ(z)` and entropy `Ŝ(z)` such that:

        * Dynamics of `x` reduce to original J⊕M flow when `E = H(x)` and `Ξ` follows the designed law.
        * The AVs enforce exact energy conservation at the discrete level (as in time-FEM / AV schemes).

4. **Design the time integrator (single step)**

   1. Choose a base scheme: midpoint or Crank–Nicolson-like for structure preservation.
   2. Write the implicit step:
      [
      z^{n+1} = z^n + Δt , \Big( J̃(z^{n+½}) ∇Ĥ(z^{n+½}) + M̃(z^{n+½}) ∇Ŝ(z^{n+½}) \Big)
      ]
      with `z^{n+½} = (z^n + z^{n+1})/2`.
   3. Enforce discrete constraints:

      * Add algebraic equations:

        * `H(x^{n+1}) = E^{n+1}`
        * `Ŝ(z^{n+1}) - Ŝ(z^n) = Δt * σ^{n+½}`, with `σ ≥ 0` entropy production.
      * Solve the coupled nonlinear system for `z^{n+1}` each step (small dimension, can use Newton).

5. **Implement metrics for checking structure preservation**

   * Over a long integration (e.g., 10⁴ steps):

     1. Track:

        * `ΔH_rel = |H(x^n) - H(x^0)| / |H(x^0)|`
        * `ΔS_step = S(x^{n+1}) - S(x^n)`
     2. Gates:

        * `max_n ΔH_rel ≤ 1e-8`
        * `ΔS_step ≥ -1e-10` for all steps (allow tiny numerical noise only).
   * Plot:

     * `H(x^n)` vs `t` (flat line).
     * `S(x^n)` vs `t` (monotone non-decreasing).
     * Phase portrait of x vs reference solution.

6. **Compare against naive integrators**

   1. Run the same toy with:

      * Explicit RK4
      * Strang splitting without AV
   2. Show:

      * Energy drifts over long time.
      * Entropy may oscillate / slightly decrease.
   3. Quantify:

      * Present log-error vs step size `Δt` curves for `H` and S-monotonicity violations.

### B. Lift to the lattice KG+RD metriplectic engine

7. **Define the discrete state and operators**

   1. State: `X = (Φ_i, Π_i)` on a 1D or 2D periodic lattice.
   2. Use your **existing** discrete operators:

      * `∇_d`, `Δ_d`, etc. from the KG+RD code.
   3. Use **existing** `H_d[X]` and `S_d[X]` as in `RESULTS_KG_RD_Metriplectic.md`.

8. **Build J_d and M_d explicitly**

   1. Implement `J_d` as the canonical discrete KG Poisson operator:

      * Blocks mapping `(Φ,Π)` → `(Π, ΔΦ, …)` with the usual skew pattern.
   2. Implement `M_d` such that:

      * It matches your RD metric term.
      * It satisfies:

        * `M_d = M_dᵀ`
        * `M_d ∇_d H_d = 0`
   3. Add sanity checks:

      * Symmetry and skew-symmetry to machine precision.
      * Numerical check that `∥J_d ∇_d S_d∥` and `∥M_d ∇_d H_d∥` are ≈ 0.

9. **Extend the AV integrator to high-dimensional X**

   1. Generalize the toy AV scheme:

      * AVs could be:

        * `E` (total energy)
        * Possibly `E_local` per block if you want stronger local conservation tests, but start global.
   2. Implicit step:
      [
      X^{n+1} = X^n + Δt \big(J_d ∇_d H_d(X^{n+½}) + M_d ∇_d S_d(X^{n+½})\big)
      ]
      with `X^{n+½}` midpoint as before and AV-enforced constraints:

      * `H_d(X^{n+1}) = E^{n+1}`
      * `S_d(X^{n+1}) ≥ S_d(X^n)` (or encoded via AV in Ŝ).
   3. Use iterative solver (Newton–Krylov or similar) with:

      * Small `Δt` to keep cost manageable.
      * Stop when both the dynamic equation and constraints are satisfied to tolerance.

10. **Design benchmark problems**

Use **two types of tests**:

**(a) Equilibrium / relaxation tests**

* Start from a slightly perturbed equilibrium configuration.
* Expect:

  * H_d constant in time.
  * S_d monotone → asymptote.
* Metrics:

  * `max_n ΔH_rel ≤ 1e-8` over long run.
  * No negative `ΔS` beyond tiny noise.

**(b) Front / pulse propagation (causality tests)**

* Initialize a localized perturbation (e.g. Gaussian bump).
* Run:

  * Pure KG (J only) to verify light-cone / dispersion (already partially done).
  * KG+RD (J⊕M) with AV integrator.
* Measure:

  * Front speed `v_front` vs analytic prediction from CF4 (`c = √(D/τ)`).
* Gates:

  * `|v_front - c| / c ≤ 0.05` (≤5% error).
  * No visible superluminal “ghost” ahead of the cone.

11. **Compare against the current Strang / naive schemes**

12. Re-run the same lattice tests with:

    * Your current Strang split integrator.
    * Any explicit/semi-implicit schemes you already use.

13. Compare:

    * Energy drift vs time.
    * Entropy monotonicity.
    * Front speed & cone violations.

14. Summarize in tables:

    * Rows: scheme type.
    * Columns: `Δt`, `T_final`, `max ΔH_rel`, fraction of steps with `ΔS < 0`, `v_front` error.

15. **Generate the plots and tables you’ll need for RESULTS docs**

At minimum:

* Toy ODE:

  * H(t) flat line vs integrator.
  * S(t) monotone vs noisy behavior of naive schemes.
  * Phase portrait overlay vs analytical trajectory.

* Lattice KG+RD:

  * H_d(t) for each scheme.
  * S_d(t) for each scheme (zoom in to show monotonicity vs violations).
  * Front position vs time compared to analytic `ct`.
  * (Optional) Fourier spectra vs reference to show no artificial damping of Hamiltonian modes.

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

Here’s a concrete file scaffolding set that fits your existing naming.

### 4.1 RESULTS: toy metriplectic AV integrator

**Filename:**
`Derivation/results/metriplectic/RESULTS_Metriplectic_AV_Integrator_Toy_v1.md`

**Suggested sections:**

1. Context & Canonical Link

   * How this ties to AXIOMS/EQUATIONS and why naive integrators are not enough.

2. Model Definition

   * Toy system (pendulum or SU(2) Bloch ball).
   * H, S, J, M definitions with references to EQUATIONS and ACSP exemplar where relevant.

3. AV-Extended Dynamics

   * Definition of extended state `z = (x, AVs)`.
   * Discrete step equations, constraints.

4. Numerical Experiments

   * Setup: time step, total time, tolerance, solvers.
   * Comparison integrators (RK4, Strang, etc.).

5. Metrics & Gates

   * Exact definitions of `ΔH_rel`, `ΔS_step`, thresholds used for pass/fail.

6. Results

   * Tables and plots, clearly labeled.
   * “Pass/Fail” status for each integrator vs your gates.

7. Failure Modes & Red Flags

   * When does the AV scheme fail?
   * What pathologies show up in naive schemes?

8. Next Steps

   * How this generalizes to lattice KG+RD and ACSP SU(2) exemplar.

**Minimum for non-embarrassing T3:**

* At least one toy system.
* At least one figure each for H(t) and S(t).
* At least one clear table comparing with naive integrators.
* Explicit gates and pass/fail statements.

---

### 4.2 RESULTS: lattice KG+RD structure-preserving integrator

**Filename:**
`Derivation/results/metriplectic/RESULTS_KG_RD_Structured_Integrator_v1.md`

**Suggested sections:**

1. Context & Role in VDM

   * This is *the* integrator used by the VDM KG+RD core (backend for void/cosmology).

2. Lattice Metriplectic Setup

   * Brief description of lattice, H_d, S_d, J_d, M_d with pointers to EQUATIONS.md and prior RESULTS docs.

3. AV-Enhanced Scheme for KG+RD

   * Exact step equations.
   * Constraint enforcement, solver details.

4. Test Problems

   * Equilibrium relaxation.
   * Front propagation / telegraph cone tests.

5. Metrics & Validation Gates

   * Energy conservation thresholds.
   * Entropy monotonicity.
   * Front speed / causality bounds.

6. Results

   * Plots and tables for each test.
   * Comparison with existing Strang and explicit schemes.

7. Discussion

   * Where the AV scheme wins.
   * Trade-offs (e.g. implicit cost vs long-time reliability).

8. Implications for VDM Instruments

   * Explicit notes that **void-lensing**, **ringdown**, and **A8 tachyonic runs** using this kernel inherit its guarantees.

**Minimum for non-embarrassing T3/T4:**

* At least two benchmarks with clean plots.
* Direct comparison against at least one old integrator.
* Clear statement that gates are passed (or where they fail and why).

---

### 4.3 PROPOSAL: metriplectic AV integrator as a standard engine

**Filename:**
`Derivation/proposals/T2_PROPOSAL_Metriplectic_AV_Structure_Preserving_Integrator_v1.md`

**Suggested sections:**

1. Motivation & Scope

   * Why VDM needs a structure-preserving metriplectic integrator as a shared engine.

2. Canonical Objects

   * Summary of H, S, J, M, and AVs.
   * References to AXIOMS/SYMBOLS/EQUATIONS.

3. Algorithm Spec

   * Pseudocode for a single step.
   * Expected preconditions (e.g. available gradients, J/M construction).

4. Validation Plan

   * Which RESULTS docs will be produced (the two above).
   * Which gates must be passed to “graduate” the integrator.

5. Integration Plan

   * Which modules in the codebase will adopt this as the default.
   * Migration strategy from old schemes.

6. Risk & Red-Team Notes

   * Where this can still go wrong (e.g. solver convergence, stiffness, high dimensionality).
   * How to detect and report those failures.

**Minimum for non-embarrassing T2/T3:**

* Clear, implementation-ready spec.
* Direct links to dependent CF/RESULTS docs.
* Explicit graduation criteria (what “done” means).

---

## 5. How this plugs back into the larger VDM story

This project is the **numerical backbone** of your whole J⊕M universe.

* **Axiom / CF chain connection:**

  * Directly tied to **CF1_QGT_to_Metriplectic_Brackets** (it ensures the J⊕M structure derived from QGT is not numerically mangled) and **CF4_Telegraph_Fisher_Causality** (it preserves finite-speed transport on the lattice). 
  * It also underpins the “Finish metriplectic KG+RD core” item at the top of your unified TODO, which is the front-door to A8, spinor emergence, gauge emergence, and everything else.

* **Instrument chain connection:**

  * The **KG+RD metriplectic engine** is the backend physics kernel for:

    * **Void-lensing meters** (you evolve void fields + interfaces).
    * **Ringdown meters** (tachyonic interfaces behaving like horizons).
    * **SIE/agency fields** once you use the same metriplectic machinery for cognitive dynamics.
  * If this engine leaks energy, violates entropy monotonicity, or breaks the telegraph cone, every downstream meter (void boundaries, ringdown spectra, A8 hierarchy tests) can be dismissed as a numerical artifact.

Short version for Future-Justin’s brain:

> This task is about **making the J⊕M core trustworthy**. Once the AV-based metriplectic integrator is in place and certified, you can point to a single RESULTS chain and say:
> *“All my void, cosmology, and agency simulations sit on a discrete engine that provably respects my own axioms for energy, entropy, and causality.”*

From there, every new meter (void-lensing, black-hole ringdown, A8 hierarchy probes) becomes a physics question instead of a “maybe your integrator is borked” question, which is exactly the kind of sharp edge you want when people start poking at VDM.
