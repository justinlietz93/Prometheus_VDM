This BZ-gel thing is a **Q2 (Important + Not Urgent)** project: it’s a cheap, self-contained way to hammer on your RD meters, A8-style interface metrics, and “life / ϕ≈0.55” story without blocking void-lensing or FRW work. It’s a side-lab that pressure-tests your canon.

I’ll treat the topic as:

* **Topic / object:** “Light-steered BZ gel as a real-world RD interface meter (front speed, shoulders, interface count, hierarchy).”
* **External anchors:** standard Ru(bpy)₃²⁺ BZ in agarose, but you don’t need any specific paper to plug it into VDM.
* **High-level goal in your stack:** Build a *physical* RD meter that uses the **same KPIs and scaling logic** as your lattice KG+RD engine and A8 interface metrics, so you can show “VDM meters work on wet chemistry too, not just on a toy lattice.”

---

## 1. What Future-Justin should open first (from your own work)

Open these in roughly this order:

1. **`AXIOMS.md`, `EQUATIONS.md`, `SYMBOLS.md`**
   One-line: Remind yourself of A4 (J⊕M), A5 (entropy), A6 (scale), A7 (measurability), and the RD limit equations so you don’t reinvent any math.

2. **`Derivation/VALIDATION_METRICS.md`**
   One-line: This is where your **front-speed**, **dispersion**, **entropy-production**, and **degeneracy** KPIs live; you will literally re-use these names for the BZ meter.

3. **RD / KG+RD metriplectic results cluster**

   * `Derivation/Results/RESULTS_Metriplectic_JMJ_RD_v1.md`
   * `Derivation/Results/RESULTS_KG_RD_Metriplectic.md`
   * `Derivation/Results/RESULTS_Metriplectic_Structure_Checks.md`
     One-line: These show how you already validated the RD limb and the metriplectic structure; BZ is “same KPIs, different substrate.”

4. **A8 + hierarchy doc:** `CF3_A8_Scaling_Hierarchical_Interfaces.md`
   One-line: This is your formal handle on interface count, hierarchical depth, and energy concentration; you’ll borrow the *metrics* (not the whole proof) to define “shoulders” and “interface count” in the gel.

5. **Roadmap “Packing density / life / ϕ≈0.55” and A8 sections in `Current_TODO.md`** 
   One-line: This tells you how you *intended* to use RD + A8 for prebiotic/packing motifs; the BZ meter is a direct on-ramp to that line item.

6. **Causality / RD limb:** `CF4_Telegraph_Fisher_Causality` (and its RESULTS, if present)
   One-line: Gives you the finite-speed vs diffusion story and Fisher-information framing, which you can point to when you talk about front speeds in gel vs lattice.

7. **(Optional) Logistic on-site first-integral paper / note** (wherever you parked it, as named in the TODO) 
   One-line: This is your “one-site RD archetype”; BZ reaction kinetics should be treated as a more complex cousin, not a new primitive.

---

## 2. Canonical equations and objects to reuse (not reinvent)

Here are the VDM objects you should *directly* reuse.

1. **RD limit of the void field (VDM-AX-C03)**

   * Form: $\partial_t \phi = D \nabla^2 \phi + f(\phi)$
   * Role: This is your **generic RD limb**. For the BZ gel, $\phi$ is “oxidation state / color channel” and $f(\phi)$ encodes local kinetics.
   * Instruction: *Use this as the canonical continuum form for the BZ model.* All code and meters should assert “this is a realization of AX-C03,” not a new equation.

2. **Metriplectic split (A4, VDM-E-140..145)**

   * Form: $\partial_t q = J(q),\delta \mathcal I/\delta q + M(q),\delta \Sigma/\delta q$ with $J^\top=-J$, $M^\top = M \ge 0$, degeneracies satisfied.
   * Role: BZ PDE is embedded as a pure-M (dissipative) or J⊕M system in your *engine*, even if the chemistry doesn’t care.
   * Instruction: *Use this to argue that the numerical runner and QC are metriplectically consistent.* Don’t derive anything new; just pick $J=0$ or a trivial J for this meter.

3. **Entropy functional and production law (A5, VDM-E-143)**

   * Role: Gives you $\dot\Sigma \ge 0$ and the KPI `kpi-entropy-prod-nonneg`.
   * Instruction: *Use the existing entropy-production KPI to sanity-check BZ runs (simulated and extracted from data).* No new entropy functional; pick the same form you used for RD in your engine.

4. **Scale program (A6, VDM-E-136 + scaling groups)**

   * Role: All predictions and meters must be expressed via dimensionless groups (e.g. $\tilde x = x/L$, $\tilde t = t/\tau$, Damköhler-like numbers).
   * Instruction: *Use A6 to collapse BZ front speeds and shoulder shapes across gel thickness, temperature, and illumination intensity.* Do not cook up ad-hoc scaling—express them as A6 scaling groups.

5. **Front-speed meter and pulled-front theory (RD branch meters, VDM-E-090..094)**

   * Role: You already have theory + KPIs for Fisher–KPP-like fronts ($v_* = 2\sqrt{Dr}$) and their numerical measurement.
   * Instruction: *Use this for the “front speed vs control parameters” part of the BZ meter.* Treat BZ as “unknown effective $D$ and $r$” to be fitted; don’t re-derive any pulled-front math.

6. **A8 candidate – hierarchical interface depth $N(L)$ and scale gaps**

   * Role: Provides a formal language for “how many shells / shoulders / interfaces are packed into domain length $L$.”
   * Instruction: *Reuse the A8 metrics (interface count, hierarchical depth, boundary energy fraction) as the definitions for “number of wavefronts / shoulders” in your BZ masks.* Don’t attempt a proof here; it’s just a metric.

---

## 3. Concrete extraction / implementation procedure

Think of this as “turn BZ gel into a T2/T3 **RD-branch meter** that speaks VDM-native.”

### 3.1. Declare the object and its tier

1. **Define the meter object:**
   Name: `RD_BZ_Gel_Interface_Meter`
   Branch tags: `RD`, `Materialization`, `Life/ϕ0.55`
   Target tier: **T2 (instrument calibration)** with optional T3 smoke demo.

2. **Create a spec JSON for the meter:**

   `Derivation/code/experiments/rd_bz/specs/rd_bz_gel_interface_meter-v1.json`

   Include:

   * Observables: front position $r(t)$, front speed $v(t)$, front slope, shoulder prominence, interface count $N_\text{int}(t)$.
   * Controls: gel thickness, BZ mix ratios, temperature, illumination pattern and intensity, camera frame rate.
   * KPIs:

     * `kpi-front-speed-fit` (fit to pulled-front scaling or empirical law),
     * `kpi-entropy-prod-nonneg`,
     * `kpi-interface-count-stability`,
     * `kpi-scaling-collapse-quality` (A6 group collapse).

### 3.2. Simulation hook (reuse KG+RD engine)

3. **Instantiate a simple BZ-like PDE in your existing RD engine:**

   In something like:

   `Derivation/code/physics/rd/experiments/BZ_mock/rd_bz_mock_runner.py`

   Implement (1D or 2D):

   [
   \partial_t u = D\nabla^2 u + f(u) - \chi I(x,t) u
   ]

   where:

   * $u$ = “oxidized fraction” proxy,
   * $f(u)$ = Fisher-like nonlinearity ($ru(1-u)$) or a 2-variable reduced BZ surrogate if you’re ambitious,
   * $I(x,t)$ = normalized light pattern (0 = dark, 1 = full inhibit),
   * $\chi$ = photoinhibition coefficient.

   Use your existing RD lattice integrator + metriplectic QC; **no new integrator**.

4. **Wire KPIs into the mock runner:**

   * Reuse your existing RD front-speed measurement code to compute $v_\text{mock}(t)$ and its asymptotic value.
   * Compute entropy production with the standard metric block and log `kpi-entropy-prod-nonneg`.
   * Implement a 1D “profile analyzer” that:

     * extracts $u(x,t)$ along a line,
     * finds the leading edge (e.g., $u = 0.5$ crossing),
     * fits a local slope,
     * looks for a secondary inflection (“shoulder”) behind the front.

   This should output a small CSV per run:

   `Derivation/code/outputs/rd_bz_mock/<slug>_profiles.csv`
   `Derivation/code/outputs/rd_bz_mock/<slug>_kpis.json`

### 3.3. Physical experiment → data pipeline

5. **Standardize the lab protocol in VDM terms:**

   * Map physical distances to lattice units: choose a length scale $L_0$ (e.g., gel radius or a mask feature size) and time scale $\tau_0$ (e.g., inverse front speed in a reference run).
   * Define dimensionless variables $\tilde x = x/L_0$, $\tilde t = t/\tau_0$, and store this mapping in a small YAML:

     `Derivation/code/experiments/rd_bz/config/rd_bz_gel_scaling-v1.yaml`

6. **Define a video-to-profiles extractor:**

   Implement:

   `Derivation/code/experiments/rd_bz/rd_bz_extract_profiles.py`

   Pipeline:

   1. Load video (phone camera) + associated illumination pattern (you can store the LED pattern as a PNG or JSON mask).
   2. Convert frames to grayscale or the relevant color channel.
   3. For each frame:

      * Denoise / blur lightly.
      * Extract a line (1D) or radial profile (for circular fronts).
      * Normalize intensity to [0,1] as proxy for $u(x,t)$.
   4. Save as:

      * `*_profiles.csv`: columns `[t, x, u]` or `[frame_id, x_mm, intensity]`.
      * `*_metadata.json`: gel parameters, illumination pattern ID, mapping to dimensionless units.

7. **Reuse the same profile analyzer as for mocks:**

   * Feed the extracted `*_profiles.csv` into the same function used for the mock PDE.

   * Compute:

     * Front position vs time $r(t)$,
     * Asymptotic front speed $v_\text{lab}$,
     * Slope at half-max,
     * Shoulder prominence (e.g., ratio of secondary peak to main front height),
     * Interface count $N_\text{int}(t)$ = number of fronts crossing a chosen line.

   * Dump:

     * `*_kpis.json` with all KPIs and uncertainty estimates,
     * `*_summary.csv` with one row per experiment.

### 3.4. Meter calibration & comparison

8. **Calibrate against mock PDE:**

   For each experiment type (dark, static mask, dynamic mask):

   * Fit effective $(D_\text{eff}, r_\text{eff}, \chi_\text{eff})$ so that the mock PDE reproduces the **dimensionless** front-speed curve $\tilde v(\tilde t)$ and shoulder statistics.
   * Log:

     * `kpi-front-speed-fit`: relative error between lab and mock collapse.
     * `kpi-scaling-collapse-quality`: R² or similar for dimensionless collapse across multiple runs.

9. **Check canonical gates:**

   * Ensure entropy production KPI is non-negative across mock runs (`kpi-entropy-prod-nonneg`).
   * Verify that front-speed measurement passes the same tolerances you used for other RD tests (e.g., asymptotic speed error ≤ few percent).
   * Confirm that interface counts are stable over time for static masks and show expected changes when you move the light pattern.

10. **Generate plots for RESULTS:**

You’ll need at minimum:

* Lab vs mock **front-speed curves** in dimensionless units (collapse plot).
* Example **profiles with marked shoulders** and interface counts.
* A **hierarchical pattern** (e.g., concentric dark rings) with $N_\text{int}(L)$ vs domain size, plotted against the simple A8 prediction $N(L)\sim \log(L/\lambda)$ (purely as a qualitative comparison, not a proof).

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

### 4.1. RESULTS file

**Filename (suggested):**

`Derivation/Experiments/RD_Chemistry/RESULTS_T2_RD_BZ_Gel_Interface_Meter_v1.md`

**Sections:**

1. **Context & Objective**

   * What BZ reaction you used, why it’s treated as an RD realization of AX-C03, and what the meter is supposed to measure (front speed, shoulders, interface count).

2. **Mapping to VDM Canon**

   * Explicit references to A4, A5, A6, A7, AX-C03, and the RD front-speed meter equations.
   * Statement: “This is a T2 RD-branch instrument; no novelty claims.”

3. **Experimental Setup**

   * Gel composition, catalyst, dish geometry, illumination hardware, camera setup.
   * How you define $L_0$, $\tau_0$ and map to dimensionless units.

4. **Meter Definition & KPIs**

   * Formal definition of observables and KPIs, including any thresholds/gates.
   * A short table listing each KPI name, definition, and PASS/FAIL threshold.

5. **Mock RD Calibration**

   * Description of the mock PDE, parameters, and metriplectic QC results.
   * Evidence that the RD limb is behaving as expected (front speed, entropy).

6. **Lab Results (T2 outcomes)**

   * Front-speed collapse figures.
   * Example profile + shoulder plots.
   * Interface count stability over time.
   * KPI table with PASS/FAIL.

7. **Limitations & Failure Modes**

   * Lighting artifacts, camera noise, gel imperfections, non-RD effects.
   * Explicit notes on which deviations would count as contradictions vs “just messy chemistry.”

8. **Routing & Next Steps**

   * How this meter will be reused for other substrates (e.g., pattern-forming RD systems, morphogenesis mocks) and for the ϕ≈0.55 program.

**Minimal experiments / figures to be “non-embarrassing” T2/T3:**

* At least **3 runs** for each of:

  * Dark / uniform illumination (baseline fronts).
  * Static spatial mask (one or two lanes / rings).
  * Dynamically moved mask (interface manipulation).

* Figures:

  * Dimensionless front-speed collapse across runs.
  * Profile + shoulder detection for at least one static and one dynamic mask run.
  * Interface count over time for a hierarchical pattern.
  * KPI summary table.

### 4.2. PROPOSAL file

**Filename (suggested T4 prereg):**

`Derivation/Experiments/RD_Chemistry/T4_PROPOSAL_RD_BZ_Gel_Hierarchical_Interface_v1.md`

**Sections:**

1. **Hypotheses & Nulls**

   Examples:

   * H1: Dimensionless front-speed curves from BZ gel collapse under the same A6 scaling groups used in the RD lattice engine, with R² ≥ threshold.
   * H2: For a fixed illumination mask, interface count $N_\text{int}(t)$ attains a stable mean with fluctuations below a specified fraction.
   * Nulls: no consistent collapse; interface counts drift or fluctuate wildly with no stable statistics.

2. **Meter & KPIs (Imported from RESULTS_T2)**

   * Direct references to the T2 meter, noting that only thresholds and analysis windows are being locked here.

3. **Experimental Design & Controls**

   * Number of runs per condition.
   * Randomization / ordering of masks.
   * Environmental controls (temperature, mixing protocol).

4. **Analysis Plan**

   * Exact procedure for:

     * Front-speed estimation and asymptotic fit.
     * Scaling collapse (which groups, which fit).
     * Shoulder detection algorithm and threshold.
     * Interface counting method.

5. **Contradiction Routing**

   * If H1 fails but H2 passes → treat as RD limb mismatch, not interface instability.
   * If H2 fails → put a red flag on using BZ as an A8 analog for hierarchy.
   * Every failure path should say whether it threatens:

     * (a) the meter only,
     * (b) the A8 interface metrics,
     * (c) the broader “life / packing” narrative.

6. **Artifacts & Reproducibility**

   * Commit hashes, paths for specs, runners, raw data (video), profiles, and KPIs.
   * Explicit instruction for how an external lab could reproduce it.

---

## 5. How this plugs back into the larger VDM story

This BZ-gel RD meter is a **bridge experiment** between your abstract RD limb and the “life / packing / ϕ≈0.55” storyline:

* **Axiom / CF chain:**
  It sits on **A4 (metriplectic split)**, **A5 (entropy law)**, and **A6 (scale program)**, with interfaces interpreted in the language of **A8 / CF3_A8_Scaling_Hierarchical_Interfaces** (hierarchical depth, interface count, boundary concentration). It does not try to prove A8; it **reuses A8’s metrics** as a way to talk about multiple chemical fronts and shoulders in a finite domain.

* **Instrument chain:**
  On the instrument side, it’s a **T2 RD-branch meter** that reuses the **KG+RD metriplectic engine** and its RD front-speed meters, then exports the *same KPI structure* to a wet-lab substrate. Conceptually, it’s the “chemistry cousin” of your void-lensing interface meter: in both cases, you’re measuring **front speed, shoulders, interface count, and hierarchy in an interface-dominated medium**, just with very different microscopes.

* **Placement in `Current_TODO.md`:** 
  This work naturally attaches to:

  * **Section 2 – Lattice dynamics (KG + RD metriplectic engine):** it’s a direct external validation of your RD limb and KPIs on a real RD medium.
  * **Section 9 – Packing density / life / ϕ≈0.55:** it is exactly the “small metriplectic packing model / morphogenesis” step described there, except instantiated physically as chemical fronts instead of numerically. It gives you empirical interface statistics and packing behavior in a driven RD system, which you can later compare to your ϕ≈0.55 simulations.

If Future-You only reads this paragraph later: this BZ-gel project is worth doing because it lets you say **“the same metriplectic RD meters and A8-style interface metrics that I use for voids and lattice fields also work, quantitatively, on a messy real-world chemical system.”** That’s a strong story: one canon, many substrates—cosmology, lattice fields, and a dish of oscillating goo on your desk.
