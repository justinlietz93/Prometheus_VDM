> **Topic:** Angle-dependent minimal speeds of Fisher–KPP fronts on a hexagonal lattice, used as an analytic benchmark and calibration target for the VDM discrete reaction–diffusion front-speed module.
> **Anchor:** Nov 28 arXiv paper on Fisher–KPP traveling/pulsating fronts on a hexagonal lattice with minimal speed (c^*(\alpha)) as a function of propagation angle.
> **Goal:** Build a T2/T3 “hex-front meter” that compares VDM’s RD kernel front speeds to the rigorous (c^*(\alpha)), then extract angle-aware correction factors you can plug into the runtime.

---

## 1. What Future-Justin should open first (from your own work)

You don’t want to hunt; you want a path. Start with these:

1. **Canon / CF docs**

   * `Derivation/canon/AXIOMS.md`
     → To re-anchor which axiom(s) govern reaction–diffusion and front propagation (A2/A4/A8 candidates).
   * `Derivation/canon/EQUATIONS_RD.md` (or whatever you named the RD kernel doc)
     → This is where the continuum RD form and discrete Laplacian symbols live; that’s what you’re matching to Fisher–KPP.
   * `Derivation/canon/CF3_reaction_diffusion.md`
     → Conceptual chain for RD fields: symbols, regimes (KPP, bistable, etc.), and existing validation gates.
   * `Derivation/canon/CF4_front_speeds.md`
     → Your existing definition of front speed meters and how they’re supposed to be used as instruments.

2. **Existing RD / front-speed meters**

   * `Derivation/code/physics/reaction_diffusion/meters/T2_RD_front_speed_meter_1D_v1.py`
     → Template for how meters measure speeds (thresholds, regression window, output schema).
   * `Derivation/code/physics/reaction_diffusion/meters/T2_RD_front_speed_meter_2D_v1.py` (if present)
     → Reference for higher-dim RD meters and how you handle directions / profiles now.
   * `Derivation/code/physics/reaction_diffusion/experiments/`
     → Existing T2/T3 experiments that already measure front speeds in Cartesian grids.

3. **VDM runtime RD engine**

   * `Derivation/code/runtime/kg_rd_engine/rd_kernel_base.py`
     → Where the generic RD stepper lives (fields, operators, time integration).
   * `Derivation/code/runtime/kg_rd_engine/lattices/hex_lattice.py` (or your nearest analogue)
     → Where hexagonal connectivity and the discrete Laplacian are defined; this is the exact object being calibrated.

4. **Meters & results structure**

   * `Derivation/results/T2_RD_front_speeds/RESULTS_T2_RD_front_speed_meter_v1.md`
     → Pattern for what a non-embarrassing T2 front-speed RESULTS doc looks like.
   * `Derivation/results/VALIDATION_METRICS.md`
     → To pick numeric gates (e.g., “front speed error < 5% across angles”).

If some of these files don’t exist yet, treat the paths as *targets* with the correct style and create them in this project when you implement.

---

## 2. Canonical equations and objects to reuse (not reinvent)

Use these as primitives; don’t re-derive anything that’s already in canon.

1. **RD evolution operator (KG+RD engine)**

   * Canonical form (your notation may differ slightly):
     [
     \partial_t \phi = D ,\Delta \phi + f(\phi)
     ]
     For Fisher–KPP, (f(\phi) = r,\phi(1 - \phi/K)).
     **Role:** Base evolution law; Fisher–KPP is just a specific choice of (f) within CF3. Use the existing RD evolution operator; just plug in KPP nonlinearity.

2. **Discrete hexagonal Laplacian (\Delta_{\text{hex}})**

   * Symbol: (\Delta_{\text{hex}}\phi) or (L_{\text{hex}} \phi), whichever you already use for the hex lattice operator.
   * **Role:** Encodes adjacency on hex lattice. Use exactly the same operator used in the runtime hex lattice; this is what the paper’s model mimics in discrete form.

3. **J⊕M split (metriplectic decomposition)**

   * (\dot{z} = J \nabla H + M \nabla S), with RD sitting in the (M \nabla S) (dissipative) part.
   * **Role:** Conceptual. For this calibration, you mostly stay in the M-sector, but keep the J⊕M decomposition as the framing of “this is an M-only test”.

4. **Front-speed meter functional**

   * Something like:
     [
     v_{\text{front}}(\alpha) = \frac{d}{dt}, x_{\text{iso}}(\alpha,t)
     ]
     where (x_{\text{iso}}) is the position of a fixed isocontour (\phi(x,t) = \phi^*) along direction (\hat{e}(\alpha)).
   * **Role:** Use your existing meter interface (meter spec JSON + log format) to measure speed; do not invent a new ad-hoc measurement scheme.

5. **Angle parametrization (\alpha) and direction vector (\hat{e}(\alpha))**

   * (\hat{e}(\alpha) = (\cos\alpha, \sin\alpha)) in embedding space, with mapping to hex lattice coordinates you already use.
   * **Role:** Single source of truth for “direction” in both simulation (how you place planar fronts) and analysis (how you project positions).

6. **Entropy/energy diagnostics**

   * Any existing entropy functional (S[\phi]) or energy-like diagnostic for RD you use in SIE/CF3.
   * **Role:** Quick sanity check that simulations remain in the KPP-like regime (no blow-up, no weird oscillations), so results are valid for comparison.

---

## 3. Concrete extraction / implementation procedure

Think of this as the exact algorithm you’d follow to wire the paper into VDM as a T2 calibration instrument.

### 3.1. Implement analytic (c^*(\alpha)) from the paper

1. **Create a new module for the analytic benchmark:**

   * File:
     `Derivation/code/physics/reaction_diffusion/benchmarks/hex_fisher_kpp_cstar_v1.py`
2. **In that file, implement:**

   * A parameter container:

     ```python
     @dataclass
     class HexFisherParams:
         D: float  # diffusion coefficient
         r: float  # growth rate
         K: float  # carrying capacity (often =1)
         lattice_spacing: float  # a
     ```

   * A function `c_star_analytic(alpha: float, params: HexFisherParams) -> float`
     using the closed-form / semi-analytic expression from the paper (or a 1D minimization over a dispersion relation if the paper phrases it that way).
3. **Add a sweep helper:**

   ```python
   def c_star_polar_grid(params: HexFisherParams, n_angles: int = 72) -> tuple[np.ndarray, np.ndarray]:
       alphas = np.linspace(0.0, 2.0 * np.pi, n_angles, endpoint=False)
       speeds = np.array([c_star_analytic(a, params) for a in alphas])
       return alphas, speeds
   ```

4. **Unit test the helper:**

   * Check periodicity: `c_star(α)` equals `c_star(α + 2π/periodicity)` within numerical tolerance.
   * Check known special directions from the paper (e.g., along principal lattice axes) against values stated or plotted there.

### 3.2. Build a hex-RD simulation that matches the paper’s model

5. **Create a T2 experiment script:**

   * File:
     `Derivation/code/physics/reaction_diffusion/experiments/T2_hex_fisher_frontspeed_calibration_v1.py`

6. **Create a spec JSON:**

   * File:
     `Derivation/code/physics/reaction_diffusion/specs/hex_fisher_frontspeed-calibration-v1.json`
   * Include:

     * RD parameters: (D, r, K).
     * Lattice type: `"hex"`.
     * Grid size: e.g., `Nx = Ny = 512` (tunable).
     * Time step and total steps.
     * List of angles (\alpha_i) to test (e.g., 12–24 angles over ([0, \pi/3]) exploiting symmetry).
     * Front-speed meter configuration (isocontour level, warmup time, regression window).

7. **Inside the experiment runner:**

   * Initialize the RD field (\phi(x,y,0)) as a planar front aligned with angle (\alpha):
     For each angle:

     ```python
     # continuous embedding coords (x, y) for each hex cell
     # project onto direction e_hat(alpha)
     s = x * np.cos(alpha) + y * np.sin(alpha)
     phi0 = np.where(s < 0.0, params.K, 0.0)  # step front
     ```

   * Hook into your RD stepper:

     ```python
     from ...kg_rd_engine import rd_stepper
     from ...kg_rd_engine.lattices import hex_lattice

     state = rd_stepper.init_state(phi0, params, lattice="hex")
     ```

   * Evolve for (T_{\text{total}}) with regular meter sampling.

### 3.3. Measure empirical front speeds with the existing meter interface

8. **Reuse front-speed meter:**

   * Import your existing front-speed meter:

     ```python
     from ...meters.front_speed_meter import FrontSpeedMeter
     ```

   * Initialize with:

     * isocontour level `phi*` (e.g., `K/2`),
     * angle (\alpha),
     * warmup steps to ignore transient behavior,
     * regression window (final N samples).

9. **During simulation:**

   * At each sample time:

     * Compute position of the isocontour along (\hat{e}(\alpha)) using your existing meter logic (no new math).
     * Append `(t, position)` to a log.
   * After the run:

     * Run linear regression of position vs. time over the final window to get empirical (v_{\text{sim}}(\alpha)).
     * Record uncertainty (R², standard error) and reject runs that don’t meet your gate.

10. **Emit logs:**

    * For each angle, save:

      * `alpha`
      * `v_sim`
      * `R2`
      * `v_analytic = c_star_analytic(alpha, params)`
      * `rel_error = (v_sim - v_analytic) / v_analytic`
    * Store in a CSV under:
      `Derivation/results/T2_hex_fisher_front_speeds/data/hex_fisher_front_speeds-v1.csv`

### 3.4. Fit correction factors and define a runtime-usable object

11. **Define a correction representation:**

    * Aim for something like:
      [
      v_{\text{sim}}(\alpha) \approx c^*(\alpha), (1 + \delta(\alpha))
      ]
      where (\delta(\alpha)) is smooth and small.
    * Represent (\delta(\alpha)) as:

      * a low-order Fourier series over the fundamental symmetry interval, or
      * a simple lookup table on a fixed angle grid with interpolation.

12. **Fit the correction:**

    * In a small analysis script:

      * Load the CSV.
      * Restrict to angles with R² above a chosen threshold.
      * Fit (\delta(\alpha)) with your chosen representation.
    * Save fit parameters to a JSON:

      * `Derivation/results/T2_hex_fisher_front_speeds/hex_fisher_frontspeed_correction-v1.json`

13. **Add a runtime helper:**

    * File:
      `Derivation/code/runtime/kg_rd_engine/frontspeed/hex_correction_v1.py`
    * Expose:

      ```python
      def corrected_front_speed(alpha: float,
                                params: HexFisherParams,
                                use_correction: bool = True) -> float:
          c_analytic = c_star_analytic(alpha, params)
          if not use_correction:
              return c_analytic
          delta = delta_alpha(alpha)  # from fitted object
          return c_analytic * (1.0 + delta)
      ```

14. **Wire into any place that predicts front speeds:**

    * Wherever the runtime currently assumes isotropic front speed (or no explicit angle dependence), add an optional path:

      * If lattice == `"hex"` and RD regime == `"KPP_like"`, call `corrected_front_speed`.
      * Otherwise fall back to existing logic.

### 3.5. Plots and metrics to generate

15. **Produce plots (for RESULTS):**

    * (c^*(\alpha)) vs (\alpha) (analytic).
    * (v_{\text{sim}}(\alpha)) vs (\alpha) (empirical).
    * Relative error vs (\alpha).
    * Optional: polar plot with radius = speed, angle = (\alpha) to visualize anisotropy.

16. **Define numeric gates:**

    * Example T2 gate:

      * For all tested angles, with R² ≥ 0.98:

        * (|v_{\text{sim}} - c^*| / c^* \leq 0.05) (≤ 5%)
          and mean absolute relative error ≤ 3%.

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

### 4.1. RESULTS file

**Filename:**

* `Derivation/results/T2_hex_fisher_front_speeds/RESULTS_T2_hex_fisher_frontspeed_calibration_v1.md`

**Sections to include:**

1. **Context & Canon Link**

   * Short description of Fisher–KPP, hex lattice, and why this is a T2 calibration.
   * Explicit references to AXIOMS (A2/A4/A8 candidate), CF3, CF4.

2. **Model & Parameters**

   * RD equation used.
   * Parameter table (D, r, K, lattice spacing, grid size, dt, T, etc.).
   * Mapping from VDM RD notation to Fisher–KPP notation.

3. **Experiment Design**

   * Lattice type, boundary conditions.
   * Angle set ({\alpha_i}) and symmetry arguments (why you only need e.g. [0, π/3]).
   * Front initialization and meter configuration.

4. **Meters & Metrics**

   * Formal meter definition (how (v_{\text{sim}}(\alpha)) is computed).
   * Gate thresholds (R², error tolerances).

5. **Results**

   * Tables:

     * Per-angle: (\alpha), (c^*(\alpha)), (v_{\text{sim}}(\alpha)), relative error, R².
   * Figures:

     * Analytic vs simulated speed vs angle.
     * Error vs angle.
     * Optional polar anisotropy visualization.

6. **Contradictions / Deviations**

   * Any angles where error > gate.
   * Hypotheses: time step too large, grid not big enough, boundary contamination, etc.

7. **Calibration Object**

   * Description of the correction function / lookup.
   * Pointer to `hex_fisher_frontspeed_correction-v1.json`.

8. **Integration Notes**

   * Short list of runtime sites where this correction is used.
   * TODO list for promoting this from T2 → T3 (e.g., use in SIE or void-interface tests).

**Non-embarrassing bar for T2:**

* At least one clean plot of analytic vs simulated speeds.
* Clear evidence that your simulation matches the paper across a nontrivial range of angles.
* A concrete correction object extracted and saved.

### 4.2. PROPOSAL file

**Filename:**

* `Derivation/results/T2_PROPOSAL_hex_fisher_frontspeed_meter_v1.md`

**Sections:**

1. **Motivation**

   * Why hex-lattice anisotropy matters for VDM (discrete cognition fields, void interfaces, etc.).
   * Why Fisher–KPP is a good canonical testbed.

2. **Canonical Anchors**

   * AXIOMS: A2 (transport), A4 (hierarchy), A8 (interface structure, if you choose to bind it here).
   * CFs: CF3 (RD), CF4 (front speeds).

3. **Hypotheses**

   * H1: VDM’s hex RD kernel reproduces the rigorous (c^*(\alpha)) within ≤5% across all tested angles.
   * H2: Residual anisotropy can be captured by a smooth correction function (\delta(\alpha)) with magnitude ≤ 5%.
   * H3: The calibrated correction improves downstream interface predictions in higher-level instruments (to be tested later).

4. **Experimental Design**

   * Summary of simulation setup (with references to code/spec files).
   * List of angle sets and run counts.

5. **Validation Gates**

   * Explicit numeric gates for calling the T2 instrument “certified”.

6. **Promotion Path**

   * How this becomes:

     * a T3 validation for the RD engine, and
     * a dependency for T4/T5 cosmic void interface meters.

A T2 PROPOSAL is “non-embarrassing” if anyone reading it knows exactly:

* what you’ll run,
* what counts as success/failure,
* and where the objects live in the repo.

---

## 5. How this plugs back into the larger VDM story

This hex-front project ties directly into your canon and instruments:

* **Axiom / CF chain:**

  * It operationalizes the “RD transport is causal and structured” story in **A2** and feeds into your interface-centric thinking under **A8 (Lietz Infinity Resolution)** by showing that even simple RD on a discrete hex lattice carries nontrivial geometric structure in its propagation speeds.
  * It grounds **CF3 (reaction–diffusion fields)** and **CF4 (front-speed meters)** in a rigorously solved case: instead of hand-waving about front speeds, you bind them to a mathematically sharp (c^*(\alpha)).

* **Instrument chain:**

  * At the **instrument level**, this is a T2 calibration meter for the **RD engine** that feeds upward:

    * Into any **void-interface / void-lensing meters**, where interface motion and anisotropy matter.
    * Into the **KG+RD engine** that SIE and ADC rely on when they interpret spatial propagation as “cognitive transport.”
  * Once trusted, this correction becomes an internal “standard candle” for discrete front propagation on hex lattices, much like a calibration source in cosmology: anytime a later meter relies on RD front speeds on hex grids, it can inherit this calibration rather than inventing its own.

If Future-Justin only reads this section, the punchline is:

> *This work turns a rigorous hex-lattice Fisher–KPP result into a T2 calibration instrument for your RD engine, giving you angle-aware front-speed corrections that tighten every higher-level meter relying on discrete interfaces—especially anything touching void boundaries and lattice-based cognition.*

From there, you can immediately decide whether today’s job is “wire up the analytic (c^*(\alpha)) module” or “run the full T2 calibration and write the RESULTS file,” without re-reasoning the whole motivation.
