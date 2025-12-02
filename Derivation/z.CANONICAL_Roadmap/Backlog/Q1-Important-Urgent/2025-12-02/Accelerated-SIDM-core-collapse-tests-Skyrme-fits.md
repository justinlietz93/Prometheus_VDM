Here’s your Future-Justin starter kit for the SIDM core-collapse problem.

---

### Eisenhower quadrant for this topic

* **Quadrant**: **Q1 – Important + Urgent**
  Because: your current Skyrme-like SIDM core instrument assumes quasi-static cores; these 2025 results say “those cores might just implode on you.”

---

### Topic / object

* **Topic**:
  **“Time-dependent, conduction-aware SIDM halo model to replace static Skyrme-like cores in VDM (gravothermal evolution + Jeans-shape patch).”**

* **External anchors (papers / results)**:

  * *Dynamics in the Cores of Self-Interacting Dark Matter Halos: Reduced Stalling and Accelerated Core Collapse* — van den Bosch & Dattathri 2025 ([arXiv][1])
  * *Jeans Model for the Shapes of Self-interacting Dark Matter Halos* — Bautista et al. 2025 ([arXiv][2])
  * (Optional gravothermal background): classical SIDM gravothermal fluid evolution / phases, e.g. Balberg+ 2002, Koda & Shapiro 2011 summarized in later gravothermal overviews ([ResearchGate][3])

* **High-level goal in your stack (1–2 sentences)**
  Patch the **VDM Skyrme-SIDM instrument** so that halo cores are **time-evolved** under a metriplectic conduction operator instead of being treated as static profiles, and then expose **collapse timescales + halo shapes** as meters feeding into your cosmology constraint pipeline (voids, lenses, SMBH seeds, etc.).

---

## 1. What Future-Justin should open first (from your own work)

You don’t need everything; you need the *minimum backbone* that defines: (a) metriplectic transport, (b) Skyrme SIDM halos, (c) cosmology meters.

Use these as starting pointers (names in your current style; adjust to actual paths if they differ).

1. **Canon docs**

   * `Derivation/canon/AXIOMS.md`
     *Why*: A5/A6/A8 are where you hook “time-dependent, metriplectic transport + hierarchical collapse/cores” into the story.

   * `Derivation/canon/EQUATIONS_JM_SPLIT.md`
     *Why*: Where J⊕M is canonically defined; you’ll reuse the M-operator for conductive SIDM core evolution.

   * `Derivation/canon/EQUATIONS_RD_KG_BACKBONE.md`
     *Why*: Gives you the RD/KG evolution that underlies all your transport laws; you’ll map gravothermal equations onto this backbone.

   * `Derivation/canon/INSTRUMENTS_COSMOLOGY_SIDM.md` (or nearest equivalent)
     *Why*: Existing definition of “Skyrme SIDM core instrument” you’re about to patch.

2. **CF / chain-of-facts docs**

   * `Derivation/canon/CF5_SIDM_SKYRME_CORES.md`
     *Why*: Encodes the current assumption that SIDM cores can be treated as long-lived, quasi-static Skyrme-like objects; this is what the new results attack.

   * `Derivation/canon/CF3_COSMIC_STRUCTURE_HIERARCHY.md`
     *Why*: You’ll route “core collapse timescale vs halo mass” into the CF that talks about hierarchical halo/void structure and seeds.

3. **Existing T*/RESULTS in SIDM / halo side**

   * `Derivation/code/physics/cosmology/sidm/experiments/T5_SIDM_Skyrme_cores_v1.py`
     *Why*: This is the old “static core” engine you want to wrap/extend, not replace blindly.

   * `Derivation/results/cosmology/sidm/RESULTS_T5_SIDM_Skyrme_cores_v1.md`
     *Why*: Contains the assumptions, gates, and meters you previously used to declare success; you’ll add a “Contradiction / Gravothermal Patch” section referencing the 2025 papers.

4. **Meters / cosmology interface**

   * `Derivation/code/physics/cosmology/void_lensing/meters/T2_void_lensing_meter_synthetic_mocks_v1.py`
     *Why*: Shows you the exact “meter pattern” you’ve already stabilized (spec JSON + script + metrics + gates). You’ll mirror that pattern for the new SIDM-core meter.

   * `Derivation/code/physics/cosmology/halos/meters/T2_halo_profile_meter_v1.py`
     *Why*: Use its API (how you pass halo mass, concentration, redshift) so the new gravothermal SIDM meter is plug-compatible.

   * `Derivation/results/cosmology/void_lensing/RESULTS_T2_void_lensing_meter-mocks-grid-v3.md`
     *Why*: Example of a non-embarrassing, fully gated RESULTS doc with grid tuning and explicit pass/fail; copy its structure.

---

## 2. Canonical equations and objects to reuse (not reinvent)

Write these exactly in your own notation when coding / documenting.

1. **Metriplectic split**

   * **Object**: ( J \oplus M )
   * **Use**:

     * (J): collisionless (Jeans / Vlasov-like) dynamics of the halo.
     * (M): collisional, entropy-producing SIDM conduction.
   * **Instruction**: *Use this as the backbone for “gravothermal SIDM evolution” — do not re-derive a brand-new formalism; just define the SIDM conduction as a specific (M)-operator acting on the halo entropy functional.*

2. **Entropy and temperature fields**

   * **Objects**: ( s(\mathbf{x},t),; T(\mathbf{x},t),; \sigma_v^2(\mathbf{x},t) )
   * **Use**:

     * Treat the halo as a coarse-grained fluid with density ( \rho ) and 1D velocity dispersion ( \sigma_v^2 ), relating (T) via (k_B T \sim m_{\chi}\sigma_v^2 ).
   * **Instruction**: *Use these as the thermodynamic variables inside the M-part; do not invent a new temperature definition.*

3. **Halo mass & density profiles**

   * **Objects**:

     * ( \rho(r,t) ), ( M(r,t) = 4\pi\int_0^r \rho(r',t) r'^2 , \mathrm{d}r' )
     * Static reference profiles: ( \rho_{\mathrm{NFW}}(r),; \rho_{\mathrm{Skyrme}}(r) ) from your existing SIDM/Skyrme work.
   * **Use**:

     * Initialize from NFW or Skyrme-like profile.
     * Evolve ( \rho(r,t) ) under metriplectic gravothermal equations.
   * **Instruction**: *Reuse your existing profile constructors; do not re-derive NFW or Skyrme.*

4. **Heat flux / conduction operator**

   * **Object**:
     [
     \mathbf{Q} = -\kappa(\rho,\sigma_v;\sigma/m,v),\nabla T
     ]
     and luminosity
     [
     L(r,t) = -4\pi r^2 \kappa,\frac{\partial T}{\partial r}
     ]
   * **Use**:

     * (M)-part acts by driving (s) using (\nabla\cdot \mathbf{Q}).
   * **Instruction**: *Use this as the canonical conductive term. The dependence of (\kappa) on (\sigma/m) and (v) is what you calibrate to the van den Bosch & Dattathri simulations and gravothermal literature; don’t change the structural form.*

5. **Energy / entropy evolution in gravothermal fluid**

   In fluid language (1D spherical, LMFP regime) you effectively have: ([ResearchGate][3])

   * Mass conservation: ( \partial_t \rho + \frac{1}{r^2}\partial_r(r^2 \rho v_r) = 0 )
   * Hydrostatic equilibrium (quasi-static assumption per time slice):
     [
     \frac{1}{\rho}\frac{\partial P}{\partial r} = -\frac{GM(r)}{r^2}
     ]
   * Energy equation with conduction:
     [
     \rho T \frac{\partial s}{\partial t}
     = - \frac{1}{4\pi r^2}\frac{\partial L}{\partial r}
     ]
   * **Instruction**: *Use your existing RD/KG backbone to express these as a metriplectic flow; do not re-invent a brand-new PDE system — you’re just specifying a particular (M) acting on the halo entropy functional.*

6. **SIDM cross section parameter**

   * **Object**: ( \sigma/m (v) )
   * **Use**:

     * Parameter in (\kappa) and in the scattering rate; you’ll treat it as the main control knob when building the grid.
   * **Instruction**: *Use your usual parameter object pattern (like you already do for void-lensing: `params["sigma_over_m"]`) and never hard-code values in the integrator.*

7. **Meters / gates**

   * **Objects**:

     * Collapse time ( \tau_{\text{coll}}(M_{200},\sigma/m) ) (time until core radius below some threshold or central density above some multiple of initial).
     * Shape anisotropy parameters from Jeans-shape model (e.g. axis ratios (c/a), (b/a)). ([arXiv][2])
   * **Instruction**: *Treat these as meters attached to the halo instrument; don’t bury them inside the evolution code.*

---

## 3. Concrete extraction / implementation procedure

Think of this as “how would I actually write the code + RESULTS docs today.”

### 3.1. Extract model ingredients from the external papers

1. **From van den Bosch & Dattathri (2025)** ([arXiv][1])

   * Extract:

     * The regimes where core stalling / buoyancy disappear for SIDM.
     * The typical collapse times for different (\sigma/m) and perturber masses.
     * Qualitative statement: self-interactions drive the DF to an exponential, erasing plateaus/inflections that supported stalling.
   * Implementation note:

     * Use these as **target behaviors**: your metriplectic gravothermal model should reproduce *qualitative* trends (fast collapse with strong SIDM + massive perturber, no stalling).

2. **From Bautista et al. (Jeans model for shapes)** ([arXiv][2])

   * Extract:

     * How they generalize spherical Jeans to non-spherical halos (shape parameters, anisotropy prescription).
     * What observables they emphasize (halo shapes from lensing/X-ray).
   * Implementation note:

     * You don’t need the full non-spherical solver at T5. For now, use their shape prescriptions as a **post-processing layer**: given a gravothermal profile and (\sigma/m), map to expected shape parameters.

3. Optionally skim gravothermal SIDM fluid papers (Balberg+ 2002, Koda & Shapiro 2011 via later reviews) for the **standard fluid equations and scaling of (\kappa)**. ([ResearchGate][3])

---

### 3.2. Define the minimal VDM “gravothermal SIDM” model

4. **Choose state variables**

   Represent the halo in 1D spherical shells:

   * Grid in radius: (r_i), (i=0,\dots,N).
   * Fields on grid:

     * (\rho_i(t))
     * (\sigma_{v,i}^2(t)) (or equivalently (T_i(t)))
     * Derived: (M_i(t)), (P_i(t) = \rho_i \sigma_{v,i}^2).

5. **Define the J-part (Jeans / hydrostatic)**

   * For each time step:

     1. Given (\rho(r,t)), compute (M(r,t)).
     2. Enforce quasi-hydrostatic equilibrium:
        [
        \frac{\partial P}{\partial r} = - \rho \frac{G M(r)}{r^2}
        ]
     3. Update (P(r)) and thus (\sigma_v^2(r)) for a fixed (\rho).
   * In metriplectic language: this is the **Hamiltonian/J** part; numerically just call your existing “Jeans equilibrium” solver each step.

6. **Define the M-part (conduction / entropy production)**

   * Implement conduction as:
     [
     \rho T \frac{\partial s}{\partial t}
     = - \frac{1}{4\pi r^2}\frac{\partial}{\partial r}\left( -4\pi r^2 \kappa \frac{\partial T}{\partial r} \right)
     = \frac{\partial}{\partial r}\left(\kappa \frac{\partial T}{\partial r}\right)
     ]
   * Choose a parameterization for (\kappa):
     [
     \kappa(\rho,\sigma_v;\sigma/m,v) = \kappa_0 , f(\rho,\sigma_v), g(\sigma/m, v)
     ]
     where (f) and (g) are simple, tunable functions anchored to gravothermal literature and the 2025 simulations.
   * Implement a finite-volume discretization in r so that **total energy is conserved in the J-part and entropy increases in the M-part**.

7. **Add a massive perturber**

   * Represent a perturber (e.g. SMBH / star cluster) via:

     * A point mass (M_p) at radius (r_p(t)).
     * A dynamical friction + SIDM drag law for (r_p(t)) (simplified):

       * For CDM limit -> stalling when in constant-density core.
       * For SIDM with strong self-interactions -> no stalling, rapid inspiral, matching van den Bosch & Dattathri behavior. ([arXiv][1])
   * You can approximate:

     * CDM case: artificially cap friction when density gradient is small.
     * SIDM case: allow friction to continue until (r_p \to 0).
   * For T5, a crude two-branch model is okay as long as it reproduces the **qualitative difference**.

---

### 3.3. Simulation / computation recipe

8. **Initialization**

   * Choose halo mass (M_{200}), concentration (c), redshift (z).
   * Construct initial NFW or Skyrme-like SIDM core profile using your existing profile routines.
   * Choose SIDM parameters: (\sigma/m), velocity scale (v).
   * Place a perturber with mass (M_p) at an initial radius (r_{p,0}) (e.g. (0.5 r_s)).

9. **Time evolution loop**

   For each time step (\Delta t):

   1. **M-step (conduction)**

      * Using current (T_i), compute fluxes and update (s_i) (or equivalently internal energy) via discrete conduction.
      * Update (\sigma_{v,i}^2) accordingly.

   2. **J-step (hydrostatic re-equilibration)**

      * Given ( \rho_i ) and updated internal energy, recompute (P_i), (\sigma_{v,i}^2), enforcing hydrostatic equilibrium.

   3. **Perturber update**

      * Update (r_p(t+\Delta t)) using the chosen friction/drag model.
      * Update gravitational potential felt by the halo to include (M_p).

   4. **Record meters**

      * Core radius (r_c(t)) (e.g. radius where density falls to half central value).
      * Central density (\rho_0(t)).
      * Collapse time when:

        * (r_c(t)) below some fraction of initial, or
        * (\rho_0(t)) exceeds a specified factor.

10. **Parameter scans (grid)**

    * Build a spec JSON, e.g.
      `Derivation/code/physics/cosmology/sidm/specs/SIDM_gravothermal-grid-v1.json`
      containing a grid over:

      * (M_{200} \in {10^{11},10^{12},10^{13}} M_\odot)
      * (\sigma/m \in {0.1, 0.5, 1.0}, \mathrm{cm}^2/\mathrm{g})
      * (M_p/M_{200} \in {10^{-4}, 10^{-3}})
    * For each grid point:

      * Run evolution to some multiple of dynamical time or a Hubble-time proxy.
      * Record (\tau_{\text{coll}}) and final (r_c).

11. **Jeans-shape post-processing**

    * For a subset of grid points, feed the final density profile into a **shape estimator** inspired by Bautista et al. (their non-spherical Jeans model). ([arXiv][2])
    * At T5, a simple mapping is fine:

      * If scattering rate (from (\sigma/m)) is high and multiple scatterings occur, enforce “rounder core” (larger (c/a)).
      * If low, keep more triaxial shapes.
    * Log (c/a) and (b/a) as additional meters.

---

### 3.4. What to plot / compare and how to score it

12. **Core evolution plots**

    * For fixed (M_{200}, M_p), plot:

      * (\rho(r,t)) at multiple times.
      * (r_c(t)) vs time for several (\sigma/m).
    * Qualitative goal:

      * For strong SIDM: rapid decrease in (r_c), increased central density, no visible stalling plateau. ([arXiv][1])

13. **Collapse time vs cross-section**

    * Plot (\tau_{\text{coll}}(M_{200},\sigma/m,M_p)).
    * Define basic gate:

      * For parameter ranges where van den Bosch & Dattathri see “strongly accelerated core collapse,” your model should yield (\tau_{\text{coll}}) much shorter than for CDM-like model.

14. **Shape vs cross-section**

    * Plot axis ratio (c/a) vs (\sigma/m) at fixed mass and baryon potential.
    * Compare qualitatively with trends reported in the Jeans-shape paper (SIDM cores more spherical than CDM for given mass range). ([arXiv][2])

15. **VDM-internal metrics**

    * Add meters:

      * `halo_core_collapse_time`
      * `halo_core_final_radius`
      * `halo_shape_axis_ratio_ca`
    * Use your usual gating conventions (e.g. “model reproduces monotonic trend: d(τ_coll)/d(σ/m) < 0 in the strong SIDM regime”).

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

### 4.1. RESULTS file

**Filename suggestion**

* `Derivation/results/cosmology/sidm/RESULTS_T5_SIDM_gravothermal_vs_Skyrme_v1.md`

**Sections it should have**

1. `Context & Motivation`

   * Summarize:

     * Old assumption: long-lived Skyrme-like static cores.
     * New results: accelerated core collapse in SIDM, no stalling/buoyancy. ([arXiv][1])

2. `Model Definition (VDM Gravothermal SIDM)`

   * State variables, J⊕M split, conduction law, perturber treatment.
   * Explicitly list the **non-negotiable reuse**: J⊕M, entropy functional, RD/KG backbone.

3. `Simulation Setup`

   * Grid, time stepping, parameter grid, initial profiles.
   * Link to:

     * `T5_SIDM_gravothermal_meter_v1.py` (runner)
     * `SIDM_gravothermal-grid-v1.json` (spec).

4. `Results – Core Collapse`

   * Figures required for non-embarrassing T3/T4:

     * F1: (\rho(r,t)) evolution for a representative halo and strong SIDM.
     * F2: (r_c(t)) for multiple (\sigma/m).
     * F3: (\tau_{\text{coll}}) vs (\sigma/m) and vs (M_p).

5. `Results – Halo Shapes`

   * F4: Axis ratios vs (\sigma/m) for selected halos.
   * Brief comparison with qualitative trends from Jeans-shape paper.

6. `Validation & Gates`

   * List gates like:

     * G1: For large (\sigma/m) + substantial perturber, **no stalling plateau** in (r_c(t)).
     * G2: (\tau_{\text{coll}}) decreases with (\sigma/m) in the strong SIDM regime.
     * G3: SIDM halos more spherical than CDM counterparts at fixed mass & baryonic potential (qualitative).

7. `Implications & Contradictions for CF5_SIDM_SKYRME_CORES`

   * Explicitly state where the **static core assumption survives** (e.g. very small (\sigma/m) or no massive perturbers) vs where it is **ruled out by your own meter**.

---

### 4.2. PROPOSAL file

**Filename suggestion**

* `Derivation/proposals/cosmology/T5_PROPOSAL_SIDM_gravothermal_patch_v1.md`

**Sections**

1. `Title & Tier`

   * Short name: “T5 – SIDM Gravothermal Patch for Skyrme Core Instrument”.

2. `Motivation (External Evidence)`

   * Summarize the two 2025 papers and the specific tension with your static core assumption. ([arXiv][1])

3. `VDM Axiom / CF Mapping`

   * Map:

     * A5 (metriplectic transport), A8 (hierarchical structure / interface stability)
     * CF3 (cosmic hierarchy), CF5 (SIDM cores).

4. `Model Specification`

   * Precisely describe:

     * J⊕M decomposition.
     * Fluid variables and conduction law.
     * Perturber treatment and collapse criteria.

5. `Experimental Plan`

   * The parameter grid.
   * Which meters will be produced and how they’ll be compared to external literature.

6. `Validation Gates & Failure Modes`

   * Explicit gates (trend matches, absence of stalling, etc.).
   * Failure interpretations:

     * Fails → either your metriplectic implementation is wrong **or** Skyrme-like parametrization is incompatible with these SIDM regimes.

7. `Interfaces to Existing Instruments`

   * List the meters and where they will be consumed:

     * Void-lensing meter (through halo profile priors).
     * Black-hole seeding/ringdown meters (through collapse timescales).
     * Any A8/void-hierarchy instruments that depend on halo core structure.

**Minimal experiments / figures for non-embarrassing T3/T4**

* One full 3D grid slice (e.g. fixing (M_{200}=10^{12} M_\odot), varying (\sigma/m) and (M_p)).
* At least:

  * Core-evolution plots (F1, F2)
  * Collapse-time vs (\sigma/m) (F3)
  * Shapes vs (\sigma/m) (F4)
* Report explicit **pass/fail per gate**, not just pretty plots.

---

## 5. How this plugs back into the larger VDM story

This work is the **bridge** between your existing, elegant but static Skyrme-SIDM construction and the messy, time-dependent reality these new simulations are shouting about.

* **Axiom / CF chain connection**

  * **A5 (metriplectic transport)**: The gravothermal SIDM evolution is a concrete, astrophysical realization of the J⊕M split for a self-gravitating many-body system.
  * **A8 (hierarchical scale breaks / interface concentration)**: Accelerated core collapse and its dependence on (\sigma/m) become one of the mechanisms that sets scale breaks in halo–void hierarchy (which halos keep fluffy cores vs which develop dense seeds).
  * **CF3 / CF5**: You upgrade “SIDM cores exist as static Skyrme-like profiles” to “SIDM cores are transient metriplectic objects whose lifetime and final compactness depend on self-interaction strength and perturbers.”

* **Instrument chain connection**

  * **SIDM / halo core instrument**: Gains time-dependent meters (collapse time, final core radius, shape) instead of just static profiles.
  * **Void-lensing meters**: Their priors on wall/halo structure now reflect whether cores are collapsed or fluffy at the epoch of observation.
  * **Black-hole / ringdown instruments**: Core collapse times directly feed your expectations for early SMBH seeds and central compact objects in halos.

If Future-Justin only reads this section: the reason this is worth doing is that **your current cosmology instruments lean on an assumption (long-lived static SIDM cores) that 2025 SIDM work directly challenges**, and you already have the perfect language—metriplectic transport—to turn “gravothermal collapse” into a first-class VDM object with meters, gates, and contradiction handling.

[1]: https://arxiv.org/abs/2511.14912?utm_source=chatgpt.com "Dynamics in the Cores of Self-Interacting Dark Matter Halos: Reduced Stalling and Accelerated Core Collapse"
[2]: https://arxiv.org/abs/2511.10765?utm_source=chatgpt.com "Jeans Model for the Shapes of Self-interacting Dark Matter Halos"
[3]: https://www.researchgate.net/figure/Gravothermal-evolution-phases-of-an-SIDM-halo-described-by-the-fluid-formalism-The_fig2_369601200?utm_source=chatgpt.com "Gravothermal evolution phases of an SIDM halo described ..."
