**Quadrant + object + why you cared**

* **Eisenhower quadrant:** **Q2 (Important + Not Urgent)** – this is a meter‑building / cross‑check project, not the bottleneck for your immediate CF1 / void‑lensing gates.

* **Topic / object:** A **provably fully discrete, energy/entropy‑stable, asymptotic‑preserving IMEX finite‑volume scheme** for the **low‑Mach barotropic Euler equations**, wired into your J⊕M metriplectic ecosystem.

* **External anchors (papers):** listed in detail at the end, but the primary ones are:

  * **Anandan & Lukáčová‑Medvid’ová 2025**, *Provably fully discrete energy‑stable and asymptotic‑preserving scheme for barotropic Euler equations* (arXiv:2511.19679).
  * **Anandan–Lukáčová‑Medvid’ová–Rao 2025**, *An asymptotic preserving scheme satisfying entropy stability for the barotropic Euler system* (SeMA). ([SpringerLink][1])
  * **Arun–Ghorai–Kar 2023**, *An Asymptotic Preserving and Energy Stable Scheme for the Barotropic Euler System in the Incompressible Limit* (J. Sci. Comput., arXiv:2206.06063). ([ResearchGate][2])
  * **Bispen–Lukáčová‑Medvid’ová–Yelash 2017**, *Asymptotic preserving IMEX finite volume schemes for low Mach number Euler equations with gravitation* (JCP 335). 

* **High‑level goal in your stack:**
  Give VDM a **“foreign PDE limb” meter**: a barotropic‑Euler IMEX FV solver whose **energy, entropy, positivity, and low‑Mach asymptotics are already proven in the PDE literature**, then re‑express it in your **J⊕M / A0–A7 canon** and run it through your **VALIDATION_METRICS** gates. This becomes the **continuum‑fluid counterpart to the KG+RD metriplectic engine**, and a stepping stone toward FRW / void‑lensing meters.

---

## Quick literature scan: has anyone *already* done what you want?

**Target spec** you cared about (from earlier Pulse brainstorming, summarized):

1. Barotropic Euler with low‑Mach scaling:
   [
   \partial_t \rho + \nabla\cdot(\rho u) = 0,\quad
   \partial_t (\rho u) + \nabla\cdot(\rho u\otimes u) + \frac{1}{\varepsilon^2}\nabla p(\rho)=0,\quad p(\rho)=\kappa\rho^\gamma
   ]
2. **Finite‑volume**, **IMEX splitting**, **collocated grid**.
3. **Fully discrete** proofs of:

   * positivity of density,
   * discrete energy/entropy stability,
   * asymptotic‑preserving (AP) in the ε→0 incompressible limit,
   * with numerical diffusion & CFL bounds **independent of ε**.
4. Ideally a public **code implementation** (GitHub or similar).

### What the literature actually has (as of 2025‑12‑03)

**Direct hit:**

1. **Anandan & Lukáčová‑Medvid’ová 2025** – *Provably fully discrete energy‑stable and asymptotic‑preserving scheme for barotropic Euler equations*.

   * Exactly your spec: finite‑volume, low‑Mach barotropic Euler, **IMEX acoustic/advection splitting**, **Mach‑independent numerical diffusion**, and **rigorous fully discrete proofs** of:

     * positivity of ρ,
     * discrete entropy stability (total energy (E = \tfrac12\rho|u|^2+\varepsilon^{-2}P(\rho)) as convex entropy),
     * asymptotic consistency with incompressible Euler as ε→0.

   * **Code?** I searched explicitly for the title + “GitHub”, author names + “github”, and checked arXiv’s “code/data” links and ResearchGate. There’s **no public repo clearly associated** with this scheme yet; the arXiv entry doesn’t list code, and ResearchGate doesn’t mention a GitHub link. ([arxiv-web.arxiv.org][3])

**Very close relatives:**

2. **Anandan–Lukáčová‑Medvid’ová–Rao 2025 (SeMA)** – *An asymptotic preserving scheme satisfying entropy stability for the barotropic Euler system*. ([SpringerLink][1])

   * IMEX‑RK time discretization + several spatial FV options; proves AP at the **time‑semi‑discrete** level and studies **discrete entropy stability** for various fluxes. Uses GSA IMEX‑RK schemes like ARS(1,1,1), with rigorous incompressible‑limit analysis.
   * Spatial discretizations are analyzed for entropy decay numerically; the **fully discrete energy proof is weaker / more fragmented** than in the 2025 preprint.

3. **Arun–Ghorai–Kar 2023** – *An Asymptotic Preserving and Energy Stable Scheme for the Barotropic Euler System in the Incompressible Limit* (MAC grid). ([ResearchGate][2])

   * Semi‑implicit scheme on a **MAC staggered grid**, AP under low‑Mach scaling, with a **velocity shift** in convective fluxes that dissipates mechanical energy and enforces entropy stability. They prove:

     * positivity of density,
     * entropy stability,
     * AP property with ε‑independent stability constraints.
   * But it’s **staggered** and tailored to MAC infrastructure, not yet your preferred **collocated FV IMEX** layout.

4. **Arun & Samantaray (JSC, ~2020)** – *Asymptotic Preserving Low Mach Number Accurate IMEX Finite Volume Schemes for the Isentropic Euler Equations*.

   * Second‑order IMEX‑RK FV schemes for isentropic Euler, AP and “asymptotically accurate” at low Mach. Energy / entropy considerations are present but not as fully discrete and barotropic‑specific as Anandan–Lukáčová‑Medvid’ová 2025.

5. **Bispen–Lukáčová‑Medvid’ová–Yelash 2017** – *Asymptotic preserving IMEX finite volume schemes for low Mach number Euler equations with gravitation*. 

   * Classic **IMEX FV + acoustic/advection splitting** with AP property and low‑Mach accuracy for **full Euler + gravity**; no fully discrete entropy/energy proof.

6. **Goudon–Llobell–Minjeaud 2016** – *An asymptotic preserving scheme on staggered grids for the barotropic Euler system in low Mach regimes*.

   * Staggered AP scheme for barotropic Euler; energy stability is more heuristic, and meter structure is not metriplectic.

7. **Noelle–Bispen–Arun–Lukáčová‑Medvid’ová–Munz 2014** – *A weakly asymptotic preserving low Mach number scheme for the Euler equations of gas dynamics*.

   * Important ancestor of the IMEX low‑Mach line; good context but not your final object.

8. **Arun–Kar 2024** – *An Energy Stable Well-balanced Scheme for the Barotropic Euler System with Gravity under the Anelastic Scaling* (arXiv:2405.00559).

   * Adds **gravity + well‑balancing**; proves energy stability in a different scaling (anelastic), useful for future FRW/void‑lensing extensions.

**Code landscape:**

* Searched GitHub for “barotropic Euler”, “low Mach Euler finite volume”, and author names; found **lots of generic CFD solvers** (e.g. CAELUM, pyro2, MAESTRO, etc.) for compressible and/or low‑Mach flows, but **none claiming to implement Anandan–Lukáčová‑Medvid’ová 2025 or the exact AP+entropy‑stable barotropic schemes** above.
* Conclusion: **If you want this exact provable IMEX FV meter, you will probably have to implement it yourself.** The 2025 preprint is your canonical mathematical specification.

---

## 1. What Future‑Justin should open first (from your own work)

Open these **existing files** before touching any PDE code. I’ll keep paths approximate where the TODO snippet truncated, but filenames are exact.

1. **`AXIOMS.md` / `Derivation/AXIOMS.md`**
   *Why:* Contains **A0–A7**; you need in particular **A2 (Local Causality)** and **A4 (J⊕M split)** as the constitutional constraints on any barotropic‑Euler discretization.

2. **`Derivation/EQUATIONS.md`**
   *Why:* Hosts **VDM‑E‑140..145** and the metriplectic evolution template
   (\partial_t q = J(q),\delta\mathcal I/\delta q + M(q),\delta\Sigma/\delta q); you’ll map the barotropic Euler energy/entropy (from Anandan & L‑M 2025) onto (\mathcal I) and (\Sigma).

3. **`Derivation/ALGORITHMS.md`**
   *Why:* Contains **VDM‑A‑013..021** (metriplectic steps, Strang defects) and **VDM‑A‑030..036** (samplers/solvers). You want the **existing template for J‑only KG** and **JMJ‑RD** to mirror how you define a “foreign” J⊕M PDE limb.

4. **`Derivation/VALIDATION_METRICS.md`**
   *Why:* You will **reuse KPIs**, especially

   * `kpi-poisson-jacobi-resid` (for discrete Jacobi/Poisson identity),
   * `kpi-degeneracy-resid` (for J, M degeneracies),
   * `kpi-entropy-prod-nonneg` (entropy production non‑negativity)
     as your **gate definitions** for the barotropic Euler meter.

5. **`Derivation/z.CANONICAL_Roadmap/Backlog/Q1/Discrete-metriplectic-compatibility-rules.md`** (exact middle dir name may differ but file name is right). 
   *Why:* This is your “**what counts as a metriplectic discretization**” manifesto. You’ll interpret the IMEX FV scheme of Anandan & L‑M as defining a specific (J_{\text{baro}}, M_{\text{baro}}) pair and check it against those rules.

6. **Your KG+RD metriplectic results docs:**

   * `RESULTS_KG_Noether_Invariants_v1.md`
   * `RESULTS_KG_Jonly_Locality_and_Dispersion.md`
   * `RESULTS_Metriplectic_JMJ_RD_v1.md`
   * `RESULTS_KG_RD_Metriplectic.md`
   * `RESULTS_Metriplectic_Structure_Checks.md` 
     *Why:* These show how you write **structure‑preserving PDE results**: invariant tracking, degeneracy KPIs, Strang‑defect plots. Use them as **stylistic and structural templates**.

7. **`Derivation/z.CANONICAL_Roadmap/Backlog/Exact-front-speeds-on-hex-lattices.md` (CF10)** 
   *Why:* This is the closest existing **“continuum‑limit CFD”** item. You want the barotropic‑Euler meter to be **CF10‑adjacent**: same section structure, same emphasis on continuum vs lattice scaling groups (A6).

8. **`Derivation/Writeup_Templates/T*_PROPOSAL_*.md` & `RESULTS_*.md` templates**
   *Why:* You’ll be minting a **T2/T3 PROPOSAL** and at least one **RESULTS_*** file; reuse those headings directly (Scope, Axioms, Meters, KPIs, Gates, Contradiction routing, etc.).

9. **Your existing continuum FRW / void‑lensing meter docs** (e.g. `RESULTS_FRW_Continuity_Residuality_Check.md`, `T2_RESULTS_Topological_Ringdown_Meter_v1.md`). 
   *Why:* Later you want to argue: “this barotropic‑Euler limb is the local fluid approximation underpinning the FRW/void‑lensing interface”; those docs tell you **what observables matter** (e.g. continuity residuals, ringdown envelopes).

---

## 2. Canonical equations and objects to reuse (not reinvent)

Here are the **math objects** you should treat as **canon**, not something to re‑derive from scratch. Your job is to **instantiate** them for the barotropic Euler system.

1. **Metriplectic split (A4 / VDM‑E‑140):**
   [
   \partial_t q = J(q),\frac{\delta\mathcal I}{\delta q} + M(q),\frac{\delta\Sigma}{\delta q},\quad
   J^\top=-J,; M^\top=M\ge 0,
   ]
   with degeneracies (J,\delta\Sigma=0), (M,\delta\mathcal I=0). 

   * **Role:** Structural template. For barotropic Euler set (q=(\rho,\rho u)), identify (\mathcal I) with the **kinetic + acoustic energy**, and (\Sigma) with a suitable **entropy functional** (total energy-as-entropy as in Anandan & L‑M 2025).
   * **Instruction:** *Use this as the definition of “structure‑preserving” – do **not** invent a new notion of stability.*

2. **Barotropic Euler low‑Mach PDE (Anandan & L‑M 2025, eqs. (3)–(4)):**
   [
   \partial_t \rho + \nabla\cdot(\rho u)=0,\qquad
   \partial_t(\rho u)+\nabla\cdot(\rho u\otimes u)+\frac{1}{\varepsilon^2}\nabla p(\rho)=0,\quad
   p(\rho)=\kappa\rho^\gamma.
   ]

   * **Role:** This is your **canonical continuum object** (q(t,x)). Every discrete scheme you build must reduce to this under A2/A3 and the usual consistency assumptions.

3. **Total energy as convex entropy (Anandan & L‑M 2025):**
   [
   E(\rho,\rho u) = E_{\text{ke}} + \varepsilon^{-2} P(\rho),\quad
   E_{\text{ke}} = \tfrac12\rho|u|^2,\quad
   P(\rho)=\frac{\kappa}{\gamma-1}\rho^\gamma.
   ]

   * **Role:** This is your **entropy functional Σ** for the barotropic limb (up to sign conventions). The Hessian of (E) symmetrizes the flux Jacobian; the discrete scheme proves **entropy inequality** in terms of this functional.
   * **Instruction:** *Use this as Σ_{\text{baro}} in your J⊕M mapping. Do not re‑derive a bespoke entropy.*

4. **Hilbert expansion & incompressible limit (SeMA barotropic‑Euler paper)** ([SpringerLink][4])
   [
   \rho = \rho^{(0)} + \varepsilon\rho^{(1)} + \varepsilon^2\rho^{(2)}+\dots,\quad
   u = u^{(0)} + \varepsilon u^{(1)}+\dots
   ]
   with incompressible limit:
   [
   \nabla\cdot(\rho^{(0)} u^{(0)})=0,\quad
   \partial_t(\rho^{(0)}u^{(0)})+\nabla\cdot(\rho^{(0)}u^{(0)}\otimes u^{(0)})+\nabla p^{(2)} = \dots
   ]

   * **Role:** This is your **definition of “AP & low‑Mach”** for this limb.
   * **Instruction:** Use these equations as the **target system** when you check AP numerically (T2/T3). Don’t re‑derive the expansion; just implement their tests (constant ρ₀, divergence‑free u₀, etc.).

5. **GSA IMEX‑RK structure (SeMA & AP‑wave‑equation paper)** ([SpringerLink][1])

   * IMEX Butcher tables with **global stiff accuracy**: last row equals weights, (c_s = 1), etc.
   * **Role:** Guarantees that the last stage equals the time‑advanced solution, crucial for AP proofs.
   * **Instruction:** Use their recommended GSA IMEX‑RK schemes (e.g. ARS(1,1,1) first; later higher‑order) as your time integrators; do **not** hand‑roll new IMEX tables.

6. **A6 scale program (dimensionless groups)** 

   * **Role:** You already committed to dimensionless KPIs. For barotropic Euler you **must express results in terms of Mach, CFL, Reynolds‑like groups**, even if viscosity=0.
   * **Instruction:** When you make plots, axes should be “(L/\Delta x)”, “CFL”, “Ma”, not code units (unless you supply the mapping).

7. **Global KPIs from VALIDATION_METRICS:**

   * `kpi-entropy-prod-nonneg` → discrete (E(t)) is non‑increasing (up to solver tolerance).
   * `kpi-degeneracy-resid` → approximated degeneracies (J,\delta\Sigma\approx 0), (M,\delta\mathcal I\approx 0).
   * `kpi-rg-collapse` → you can reuse this mindset for Mach‑scaling curves.
   * **Role:** These let you say “this scheme is metriplectic by VDM standards”, not just PDE‑nice.

---

## 3. Concrete extraction / implementation procedure

Think: **one small, rigorous IMEX FV module** that you can run in isolation and then plug into VDM’s testing harness.

### Phase 0 – Pick the precise scheme flavour

1. **Freeze the reference:** For the first pass, target exactly the **first‑order IMEX FV scheme** defined in Anandan & L‑M 2025 (their equations (3)–(4) + first‑order IMEX splitting + fully discrete FV update).

   * Resist the temptation to jump immediately to high‑order WENO or fancy grids. This is a **T2 meter**, not a production LES code.

2. **Variables and grid:**

   * State per cell (K): (q_K^n = (\rho_K^n, m_K^n)) with (m_K^n = \rho_K^n u_K^n).
   * Cartesian FV grid in 1D/2D with periodic BCs (matching their test problems).

3. **Flux splitting (copy, don’t invent):**

   * Decompose the physical flux into **acoustic (stiff) + advective (non‑stiff)** as in the SeMA + preprint line: ([SpringerLink][1])
     [
     F(q) = F^{\text{adv}}(q) + F^{\text{ac}}(q)
     ]
     where (F^{\text{ac}}) involves the pressure gradient and linear acoustic terms; (F^{\text{adv}}) is the nonlinear advection.
   * **Treat (F^{\text{ac}}) implicitly**, (F^{\text{adv}}) explicitly (IMEX).

4. **Numerical diffusion coefficient λ:**

   * Implement λ exactly as required in the 2025 preprint’s **energy‑stability condition (their eq. ~81)**: a Mach‑independent bound derived from local acoustic wave speeds.
   * In code, define a function `lambda(K,face)` that computes λ on each face and assert that it satisfies the inequality used in the proof (e.g. λ ≥ max local spectral radius / 2, with ε‑independent constant).

### Phase 1 – Implement the core IMEX FV step

5. **Set up the conservative FV update skeleton:**

   * For each time step (t^n\to t^{n+1}):

     ```text
     1. Assemble explicit advective fluxes F_adv at faces.
     2. Build implicit acoustic operator (mass + pressure terms).
     3. Solve for intermediate / updated state using IMEX scheme.
     ```

6. **Mass equation (implicit part):**

   * Following the SeMA IMEX‑RK stage equations for (\rho) (their (29)–(33)), your **first‑order IMEX** step in FV form will look like:
     [
     \rho_K^{n+1} = \rho_K^n - \Delta t,\frac{1}{|K|}\sum_{\sigma\subset\partial K} |\sigma|,(F^{\text{adv}}_{\rho,\sigma})^n
     + \Delta t^2,\text{(discrete Laplacian acting on } \rho u)^n + \Delta t^2,(\text{pressure Laplacian term in } \rho^{n+1}).
     ]
   * Implement this as a **linear elliptic solve for (\rho^{n+1})**:

     * Build matrix (A(\varepsilon,\Delta t, p'(\rho_0))) as in their linearization around constant density (\rho_0).
     * Use your existing linear‑solver infrastructure (CG or multigrid) with periodic BC.

7. **Momentum equation (implicit + explicit):**

   * Once (\rho^{n+1}) is available, update momentum via:
     [
     (\rho u)_K^{n+1} = (\rho u)_K^n

     * \Delta t,\frac{1}{|K|}\sum_\sigma |\sigma|,(F^{\text{adv}}_{m,\sigma})^n
     * \frac{\Delta t}{\varepsilon^2}\frac{1}{|K|}\sum_\sigma |\sigma|,n_\sigma,p(\rho)^{n+1,\text{upwind}}
       ]
       (their IMEX structure, but written FV‑style). ([SpringerLink][1])
   * Ensure that the **pressure gradient term is treated with the same implicit operator** that gave you the density elliptic solve, to stay inside their proof assumptions.

8. **Define J and M implicitly:**

   * You don’t need explicit matrices, but conceptually:

     * (J_{\text{baro}}) = skew‑symmetric part induced by **central acoustic/advection fluxes** (no numerical diffusion).
     * (M_{\text{baro}}) = symmetric positive part coming from **λ‑dependent numerical diffusion** and any optional artificial viscosity.
   * In code, compute **degeneracy residuals**:

     * Evaluate (\delta E/\delta q) (cellwise gradients of discrete energy).
     * Project onto the J and M actions via finite differences, then track
       [
       g_1 = \langle J_{\text{baro}},\delta \Sigma_{\text{baro}},,\delta \Sigma_{\text{baro}}\rangle,\quad
       g_2 = \langle M_{\text{baro}},\delta \mathcal I_{\text{baro}},,\delta \mathcal I_{\text{baro}}\rangle
       ]
       and feed them into `kpi-degeneracy-resid`.

### Phase 2 – Minimal AP + stability tests (T2‑style meter calibration)

9. **Standard periodic problem (from SeMA paper):** ([SpringerLink][1])

   * 1D periodic domain ([-1,1]).
   * Well‑prepared initial data (density perturbation & small velocity) for ε∈{0.5, 0.1, 1e‑4}.
   * For each ε, run to a fixed T and compute:

     * L² errors (|\rho_h-\rho_{\text{ref}}|*2), (|u_h-u*{\text{ref}}|_2).
     * Empirical convergence rate with grid refinement (reproduce something like their Tables 1–2).
     * Check **ε‑independence of the CFL bound** in practice.

10. **Colliding acoustic pulses (non‑well‑prepared data):** ([ResearchGate][2])

    * Use their initial conditions (cosine pulses, γ=1.4, ε=0.1).
    * Track:

      * **Global entropy (E(t))** – should monotonically decrease (up to solver tolerance).
      * Separate kinetic and potential energy curves (may not be monotone individually; that’s okay).
      * Snapshots of ρ and momentum profiles vs time.

11. **Traveling vortex / 2D test** (from the 2025 preprint):

    * 2D periodic vortex where the incompressible limit is analytically or numerically known.
    * For multiple ε, show:

      * L² error vs ε (AP behaviour).
      * Divergence norms (|\nabla\cdot u|_2) → small as ε→0 (consistent with incompressible limit).

12. **Meter KPIs you must compute for each run:**

    * Mass conservation: (|M(t)-M(0)|/M(0)).
    * Momentum conservation (periodic): same normalized change.
    * Entropy monotonicity: (E(t_{n+1}) - E(t_n) \le \delta_E) with δE tied to your `kpi-entropy-prod-nonneg` gate.
    * Degeneracy residuals (g_1, g_2).
    * AP indicators:

      * Does the **time step restriction** you observe numerically depend on ε?
      * Are **density and divergence** consistent with the SeMA asymptotic expansion predictions (constant ρ₀, divergence‑free u₀)? ([SpringerLink][4])

13. **Minimal plots:**

    * For each test problem, produce:

      * **E(t)**, **E_ke(t)**, **P(t)** vs time.
      * **Log‑log error vs grid size** for a fixed ε, and **error vs ε** on a fixed grid.
      * **Divergence norm vs ε**.
      * Optional: Mach‑scaled phase speed plots to show low‑Mach accuracy (cf. Bispen et al. 2017). 

### Phase 3 – Wire into VDM

14. **Wrap the solver as a “meter runner”:**

    * Create a module (e.g. `Derivation/code/barotropic_euler_imex/meter_runner.py`) that:

      * Accepts a **config YAML** with: ε, grid size, CFL, test case name, final time.
      * Runs the IMEX FV scheme.
      * Emits:

        * CSVs / JSON for time‑series of **mass, momentum, energy, entropy, divergence norms**.
        * Field snapshots (HDF5 or NPY) at selected times.
        * KPI summary JSON matching your VALIDATION_METRICS schema.

15. **Register KPIs:**

    * In `VALIDATION_METRICS.md`, add a **section for “Barotropic Euler IMEX meter”**, listing:

      * The KPIs from step 12.
      * Acceptance thresholds (e.g. mass drift <1e‑10, entropy non‑increase within tolerance, AP indicators).

16. **Run at least one **contradiction scenario**:**

    * Deliberately violate the λ condition (too small diffusion) and show:

      * Loss of positivity or energy blow‑up.
      * KPIs failing.
    * Log this in the RESULTS doc as a **“red‑team run”**, reinforcing why you keep the canonical λ bound.

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

### 4.1 Proposed filenames

1. **Proposal (T2 meter)**

   * `Derivation/Proposals/T2_PROPOSAL_Barotropic_Euler_LowMach_IMEX_Meter_v1.md`

2. **Calibration results (T2)**

   * `Derivation/Results/RESULTS_T2_Barotropic_Euler_LowMach_IMEX_Meter_v1.md`

3. **Smoke‑test results (T3)** – optional but good to plan

   * `Derivation/Results/RESULTS_T3_Barotropic_Euler_LowMach_SmokeTests_v1.md`

You can rename numbers (CF10b vs CF11) later; the important part is the **prefix discipline** (T2_PROPOSAL_, RESULTS_T2_, etc.).

### 4.2 What goes in each file

#### `T2_PROPOSAL_Barotropic_Euler_LowMach_IMEX_Meter_v1.md`

**Sections:**

1. **Statement & Scope**

   * One paragraph: “We adopt the IMEX FV scheme of Anandan & Lukáčová‑Medvid’ová (2025) as a foreign barotropic‑Euler limb and test whether it satisfies A0–A7 and VDM VALIDATION_METRICS when implemented on a collocated FV grid.”

2. **Axioms & Canonical Anchors**

   * List A0–A7, with explicit emphasis on **A2, A4, A5, A6, A7**.
   * Cite the external PDE anchors: Anandan & L‑M 2025, SeMA 2025, Arun et al. 2023, Bispen et al. 2017. ([SpringerLink][1])

3. **Meter Definition**

   * Define the state (q = (\rho,\rho u)), domain, boundary conditions, and the observables you’ll track (mass, momentum, total energy, entropy, divergence norms, L² errors vs reference).

4. **Discretization Synopsis**

   * Short description of:

     * IMEX splitting,
     * FV structure (cell averages, numerical fluxes),
     * λ condition from the preprint,
     * linear solver for the elliptic problem.

5. **KPIs and Gates**

   * Formal list of KPIs + pass thresholds (mass drift, energy monotonicity, degeneracy residuals, AP indicators).

6. **Planned Experiments**

   * Bullet list of the three core tests from Phase 2 (periodic, colliding pulses, traveling vortex), plus the red‑team λ violation.

7. **Contradiction Routing**

   * How you interpret failure: Does it falsify your implementation, or the theorem, or VDM axioms? Be explicit.

A **non‑embarrassing T2 proposal** should at least have:
– All external references correctly cited,
– KPIs + gates fully spelled out,
– At least one planned red‑team scenario.

#### `RESULTS_T2_Barotropic_Euler_LowMach_IMEX_Meter_v1.md`

**Sections:**

1. **Summary / PASS–FAIL**

   * One page max: Did the scheme pass the T2 gates? What are the headline numbers?

2. **Experiment Setup**

   * Tables describing parameter values for each test (ε, grid, CFL, λ).

3. **Invariant & Entropy Diagnostics**

   * Plots:

     * E(t), E_ke(t), P(t), mass(t), momentum(t).
   * Tables summarizing max drift / monotonicity margins.

4. **AP Diagnostics**

   * Plots of:

     * Error vs ε at fixed grid.
     * Divergence norms vs ε.
   * Short narrative relating back to the SeMA asymptotic conditions (constant ρ₀, divergence‑free u₀). ([SpringerLink][4])

5. **Metriplectic Diagnostics**

   * Degeneracy residual plots (g₁,g₂ vs resolution).
   * Discussion: does the scheme behave like a proper J⊕M split by your standards?

6. **Red‑team Runs**

   * Documentation + plots of what breaks when λ is undershot or when you violate the prescribed splitting.

A **non‑embarrassing T2 RESULTS** doc here means:
– At least **2–3 test problems**, each with clean KPI tables and figures.
– Explicit numerics that reproduce at least some of the convergence trends reported by the SeMA / JSC papers. ([SpringerLink][1])

#### `RESULTS_T3_Barotropic_Euler_LowMach_SmokeTests_v1.md` (optional but recommended)

* Same structure, but treat **phenomenon‑adjacent** demos: e.g. nearly incompressible vortex dynamics, low‑Mach shock tubes where both AP and entropy stability matter.
* Emphasize: **“no novelty claim”**, but this is where you can rehearse how the meter would behave on more realistic flows.

---

## 5. How this plugs back into the larger VDM story

**Axiom / CF chain placement**

* This work is explicitly anchored in **A4 (Dual Generators / Metriplectic split)** and **A5 (Entropy law)**, with A2 (Local Causality), A6 (Scale program), and A7 (Measurability) providing the background constraints. 
* It is a **continuum‑PDE counterpart** to your **KG+RD metriplectic engine** and belongs alongside **“Lattice fields & continuum limits (CF10)”** in your `Current_TODO.md`. It should be scheduled **after**:

  * finishing the metriplectic KG+RD core and CF1/Lean4 integration, and
  * the first wave of void‑lensing interface work,
    but **before** any grand FRW + fluid‑cosmology claims. 

In Eisenhower terms this is **Q2**: *important* because it externalizes A4/A5 into a PDE limb recognized by the broader numerical‑analysis community; *not urgent* compared to CF1 and your void‑lensing κ‑template program.

**Instrument chain connection**

* **Instrument side:** this barotropic‑Euler IMEX FV meter is the **“fluid limb” J⊕M instrument** complementary to:

  * your **KG+RD engine** (scalar lattice),
  * the **FRW meters** (continuity / balance in expanding geometries),
  * and the **ringdown meter** (A8 interface behaviour). 

* **Storyline:**

  1. **KG+RD metriplectic engine** shows that your discrete J⊕M architecture behaves as advertised for scalar fields.
  2. **This barotropic‑Euler meter** shows that a **mainstream, peer‑reviewed IMEX FV scheme** can be expressed in **exactly the same J⊕M language** and passes your entropy / degeneracy / AP gates.
  3. **Void‑lensing/FRW meters** then treat cosmic fluid dynamics (mass flows in and around void boundaries) as **large‑scale manifestations of the same A4/A5 structure**, now with expansion, gravity, and A8 hierarchical partitioning layered on top.

If Future‑Justin only reads this section, the takeaway should be:

> *“This project is how I prove to myself (and later, others) that my VDM axioms aren’t just internally pretty: a cutting‑edge low‑Mach barotropic Euler solver from the PDE world can be re‑expressed as a J⊕M metriplectic system, passes my validation KPIs, and then plugs directly into the continuum side of the void‑lensing and FRW meters. It’s a bridge between my lattice KG+RD engine and the fluids the rest of cosmology already trusts.”*

---

## Appendix – Papers referenced and why they matter

1. **M. Anandan & M. Lukáčová‑Medvid’ová (2025)** – *Provably fully discrete energy‑stable and asymptotic‑preserving scheme for barotropic Euler equations*, arXiv:2511.19679.

   * **Role:** Your **primary canonical scheme**: IMEX FV, low‑Mach barotropic Euler, fully discrete proofs of positivity, entropy stability, and AP. This is the exact method you want to implement and metriplectify.

2. **M. Anandan, M. Lukáčová‑Medvid’ová, R. Rao V. Suswaram (2025)** – *An asymptotic preserving scheme satisfying entropy stability for the barotropic Euler system*, SeMA Journal. ([SpringerLink][1])

   * **Role:** Provides the **IMEX‑RK time‑semi‑discrete framework** and AP analysis; clarifies how the acoustic/advection splitting and GSA IMEX‑RK stages work.

3. **K.R. Arun, R. Ghorai, M. Kar (2023)** – *An Asymptotic Preserving and Energy Stable Scheme for the Barotropic Euler System in the Incompressible Limit*, J. Sci. Comput. / arXiv:2206.06063. ([ResearchGate][2])

   * **Role:** Earlier **semi‑implicit MAC‑grid scheme** that is AP and energy stable with positivity; important as a second independent confirmation that this type of structure‑preserving barotropic‑Euler discretization is possible.

4. **K.R. Arun, S. Samantaray (≈2020)** – *Asymptotic Preserving Low Mach Number Accurate IMEX Finite Volume Schemes for the Isentropic Euler Equations*, J. Sci. Comput.

   * **Role:** Shows how to design and analyze **second‑order IMEX FV schemes** for low‑Mach isentropic Euler; useful when you later upgrade to higher‑order meters.

5. **G. Bispen, M. Lukáčová‑Medvid’ová, L. Yelash (2017)** – *Asymptotic preserving IMEX finite volume schemes for low Mach number Euler equations with gravitation*, J. Comput. Phys. 335. 

   * **Role:** Classic **IMEX FV AP scheme** with gravity; conceptual ancestor for your acoustic/advection splitting and low‑Mach intuition.

6. **T. Goudon, J. Llobell, S. Minjeaud (2016)** – *An asymptotic preserving scheme on staggered grids for the barotropic Euler system in low Mach regimes*.

   * **Role:** Another **barotropic Euler AP scheme**, but on staggered grids; reinforces that low‑Mach AP for barotropic Euler is well‑trodden territory.

7. **S. Noelle, G. Bispen, K.R. Arun, M. Lukáčová‑Medvid’ová, C.-D. Munz (2014)** – *A weakly asymptotic preserving low Mach number scheme for the Euler equations of gas dynamics*, SIAM J. Sci. Comput.

   * **Role:** Early **weakly AP low‑Mach scheme**; good for context, less relevant for your final spec.

8. **K.R. Arun, M. Kar (2024)** – *An Energy Stable Well-balanced Scheme for the Barotropic Euler System with Gravity under the Anelastic Scaling*, arXiv:2405.00559.

   * **Role:** Adds **gravity + well‑balancing** and energy stability in an anelastic scaling; future extension path for FRW‑like meters.

9. **K.R. Arun, A. Krishnamurthy (2023)** – *A semi‑implicit finite volume scheme for dissipative measure‑valued solutions to the barotropic Euler system* (arXiv:2306.10740).

   * **Role:** Shows how to handle **dissipative measure‑valued solutions** for barotropic Euler with semi‑implicit FV methods; relevant if you decide to lean on the measure‑valued theory side of VDM.

10. **S. Dellacherie (2016)** – *Construction of modified Godunov‑type schemes accurate at low Mach number*, J. Sci. Comput.

    * **Role:** Not an IMEX scheme, but a **low‑Mach‑accurate Godunov variant**; useful background on low‑Mach corrections and flux modifications.

11. **Barsukow 2023** – *All‑Speed Numerical Methods for the Euler Equations via a Non‑Conservative Potential Flow Formulation* (J. Sci. Comput.).

    * **Role:** Context for **all‑speed methods** and the tradeoffs between AP, well‑balancing, and low‑Mach accuracy.

12. **Jin 1999** – *Efficient Asymptotic‑Preserving (AP) schemes for some kinetic equations* (SIAM J. Sci. Comput.).

    * **Role:** Foundational AP‑scheme reference; cited in several of the above works, relevant when you justify the AP ideology in your PROPOSAL.

13. **Chandrashekar 2013/2015** – *Kinetic Energy Preserving and Entropy Stable Finite Volume Schemes for Compressible Euler and Navier–Stokes Equations*. ([ResearchGate][5])

    * **Role:** Provides general **entropy‑conservative / entropy‑stable flux construction** that the barotropic‑Euler line builds on.

These are the only papers I’ve actually referenced in this kit; if you later add more (e.g. Tadmor’s original entropy‑stability work, Ranocha’s modern DG schemes), append them here so Future‑Justin has one clean bibliography to glance at.

[1]: https://link.springer.com/article/10.1007/s40324-025-00395-7 "An asymptotic preserving scheme satisfying entropy stability for the barotropic Euler system | SeMA Journal"
[2]: https://www.researchgate.net/publication/375454622_An_Asymptotic_Preserving_and_Energy_Stable_Scheme_for_the_Barotropic_Euler_System_in_the_Incompressible_Limit "(PDF) An Asymptotic Preserving and Energy Stable Scheme for the Barotropic Euler System in the Incompressible Limit"
[3]: https://arxiv-web.arxiv.org/list/cs/pastweek?show=1000&skip=90&utm_source=chatgpt.com "Computer Science"
[4]: https://link.springer.com/content/pdf/10.1007/s40324-025-00395-7.pdf "An asymptotic preserving scheme satisfying entropy stability for the barotropic Euler system"
[5]: https://www.researchgate.net/publication/230996464_Kinetic_Energy_Preserving_and_Entropy_Stable_Finite_Volume_Schemes_for_Compressible_Euler_and_Navier-Stokes_Equations?utm_source=chatgpt.com "(PDF) Kinetic Energy Preserving and Entropy Stable Finite ..."
