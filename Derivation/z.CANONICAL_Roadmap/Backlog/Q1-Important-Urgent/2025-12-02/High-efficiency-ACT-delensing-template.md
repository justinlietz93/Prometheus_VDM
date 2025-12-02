Alright, Future-Justin, here’s your starter kit for:

* **Eisenhower Quadrant:** **Q1 — Important + Urgent**
* **Topic:** High-fidelity ACT+unWISE+Planck CIB CMB-lensing template as a *pre-filter / calibrator* for the **void-lensing interface meter** in the A8 program.
* **External anchor:** arXiv:2511.21949 — high-correlation lensing-mode template combining **ACT DR6**, **unWISE galaxies**, and **Planck CIB**, used to build a gradient-order lensing B-mode template with record delensing efficiency.
* **High-level VDM goal:** Use this template to *sharpen void-wall shoulders* and *tighten A8 gates* in your void-lensing program, while staying fully inside the metriplectic / A8 / FRW meter stack.

---

## 1. What Future-Justin should open first (from your own work)

Open these in roughly this order.

1. **`AXIOMS.md`**

   * Reason: Remind yourself of **A2 (Local Causality)**, **A6 (Scale Program)**, **A7 (Measurability)**, and candidate **A8** language; these anchor what counts as a valid “meter + gate” for this new template.

2. **`EQUATIONS.md`** (pay attention to J⊕M, RD/KG, and scaling groups)

   * Reason: You’ll reuse the metriplectic evolution and scaling-group definitions for mapping void-lensing observables into A6-compliant dimensionless combinations.

3. **`VALIDATION_METRICS.md`**

   * Reason: You’ll plug new KPIs into existing gate machinery (entropy production, degeneracy checks, RG collapse, etc.) and define **new void-lensing-specific KPIs** for “shoulder clarity” and “noise suppression”.

4. **`Derivation/z.CANONICAL_Roadmap/Backlog/Q1/Discrete-metriplectic-compatibility-rules.md`**

   * Reason: Keeps you honest that any extra filtering you do with external κ-templates doesn’t secretly break the metriplectic bookkeeping in the sims.

5. **`Derivation/Proposals/CF3_A8_Scaling_Hierarchical_Interfaces.md`**

   * Reason: This is the math backbone for A8: depth $N(L)$, scale gaps $\rho$, boundary fractions $\alpha,\alpha_\mathcal I$; you’re literally trying to see these in the **void lensing shoulders**.

6. **Void-lensing meter experiment runner**

   * **`Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_meter_synthetic_mocks_v1.py`**
   * Reason: This is the existing **T2 instrument** you’re augmenting. You’ll patch in “use_external_kappa_template” here, not write a new runner from scratch.

7. **Void-lensing meter spec**

   * **`Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-grid-v3.json`**
   * Reason: This grid spec already encodes the H1–H3 hypotheses and parameter sweeps. You’ll add new switches/fields for template usage and output KPIs.

8. **FRW / cosmology results**

   * **`RESULTS_FRW_Continuity_Residual_Quality_Check.md`**
   * Reason: Provides the FRW background meters against which your void-interface predictions live; important when you interpret void profiles as **A8+FRW** rather than some arbitrary profile fit.

9. **Ringdown / interface meter**

   * **`T2_RESULTS_Topological_Ringdown_Meter_v1.md`**
   * Reason: Another T2 meter that already demonstrates how you structure **topological interface instruments**; mirror that style for this “void-wall shoulder” refinement.

10. **Current TODO / roadmap block you pasted (“Unifying Existing Work” )**

    * Reason: You need to remember that “Void-lensing interface program” is explicitly marked **highest priority** and how it talks to A8 and FRW.

If you open just those 10, you’ll be fully rehydrated.

---

## 2. Canonical equations and objects to reuse (not reinvent)

Use these as **imports**, not as re-derivations.

1. **Metriplectic evolution (A4)**

   * **Object:**
     [
     \partial_t q = J(q),\frac{\delta \mathcal I}{\delta q} + M(q),\frac{\delta \Sigma}{\delta q}
     ]
     with $J^\top=-J$, $M^\top=M\ge 0$, and $J,\delta\Sigma=0$, $M,\delta\mathcal I=0$.
   * **Role:** Underlies your KG+RD lattice engine; when you simulate mock voids or synthetic fields, **reuse this exact evolution and degeneracy diagnostics** for any “ground-truth” field that you lens.
   * **Instruction:** Use this for **all mock universe fields feeding the lensing pipeline**, do not re-derive.

2. **RD / Fisher-KPP limit (VDM-AX-C03)**

   * **Object:**
     [
     \partial_t \phi = D\nabla^2\phi + f(\phi)
     ]
   * **Role:** Toy for tachyonic fronts and interface growth; when you create void-mock morphologies, reuse this as the “shape generator” before projection.
   * **Instruction:** Use this for **simple void-mock interface generation**, do not re-derive.

3. **A6 scale program**

   * **Object:** Dimensionless variables and envelopes, e.g. $R/R_v$, $z/z_0$, and profile rescalings specified in `EQUATIONS.md` (scaling groups and collapse metrics).
   * **Role:** Your void profiles and lensing shoulders **must be expressed in scale-free form** for A8-gate comparisons across surveys and mocks.
   * **Instruction:** Use this for **radial binning and profile normalization**, do not re-derive scaling logic.

4. **A8 (candidate) hierarchical depth**

   * **Object:**

     * $N(L)=\Theta(\log(L/\lambda))$
     * scale gaps $\rho\in(\rho_{\min},\rho_{\max})$
     * boundary fractions $\alpha, \alpha_\mathcal I > 0$
   * **Role:** Turn void-lensing profiles into A8 metrics: “How many shoulders / inflection layers can we resolve as a function of scale?”.
   * **Instruction:** Use this to **define the shoulder-counting and gradient-sign-change KPIs**, do not re-derive any new hierarchy law.

5. **Lensing observables (standard cosmology layer in your meters)**

   * **Objects (symbol conventions you’d use):**

     * Convergence: $\kappa(\hat n)$
     * Tangential shear profile: $\gamma_t(R/R_v)$
     * Excess surface density or equivalent stacked quantity: $\Delta\Sigma(R/R_v)$
   * **Role:** These are the meters you already use in the void-lensing pipeline; the new template **only changes how you estimate / filter $\kappa$**, not the definitions.
   * **Instruction:** Use these as **fixed observables for all new experiments**, do not re-define what $\gamma_t$ or $\kappa$ mean.

6. **FRW background meters**

   * **Objects:** $H(a)$, $\rho(a)$, $p(a)$, and EOS fits you already use in FRW RESULTS docs.
   * **Role:** The void-lensing signal is interpreted on top of FRW; keep FRW as the **background meter** and interpret A8-induced structure as a perturbation.
   * **Instruction:** Use this for **background cosmology in mocks and data interpretation**, do not re-derive FRW.

7. **Meter KPI infrastructure from VALIDATION_METRICS**

   * **Objects:** KPI definitions and gates (e.g. error tolerances, R² thresholds, entropy nonnegativity).
   * **Role:** You’ll add new KPIs for:

     * “shoulder contrast”,
     * “slope asymmetry”,
     * “template vs recon residual noise”.
   * **Instruction:** Use existing KPI template & gate mechanism; **extend it**, don’t invent a new KPI framework.

---

## 3. Concrete extraction / implementation procedure

Goal: **Integrate the high-fidelity κ-template as an optional background field** in the void-lensing meter, then quantify how it sharpens A8-relevant features.

Let’s treat this like you’re writing code **today**.

---

### Step 0 — Define the concrete objects

1. **External κ-template file(s)**

   * Store under something like:
     `Derivation/data/external/cmb_lensing/ACT_DR6_unWISE_PlanckCIB_kappa_template_nsideXXXX_v1.fits`
   * Assume: HEALPix format, `kappa` map, with known $N_\text{side}$ and mask.

2. **Internal interface: a “κ-provider” abstraction**

   * New module:
     `Derivation/code/physics/cosmology/void_lensing/lib/kappa_provider.py`
   * Expose something like:

     ```python
     class KappaProvider:
         def __init__(self, mode: str, config: dict):
             # mode in {"none", "recon", "external_template"}
         def kappa_at(self, ra: float, dec: float) -> float:
             ...
     ```
   * So the meter runner just asks for `kappa_at(...)` and doesn’t care if it’s noisy recon or high-fidelity template.

---

### Step 1 — Extend the mocks-grid spec

Edit:
`Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-grid-v3.json`

Add fields like:

```json
{
  "kappa_source": ["none", "recon", "external_template"],
  "external_kappa_template": {
    "path": "Derivation/data/external/cmb_lensing/ACT_DR6_unWISE_PlanckCIB_kappa_template_nsideXXXX_v1.fits",
    "nside": 2048,
    "mask_path": "Derivation/data/external/cmb_lensing/ACT_DR6_unWISE_PlanckCIB_mask_nsideXXXX_v1.fits"
  },
  "profile_bins": {
    "r_over_Rv_min": 0.2,
    "r_over_Rv_max": 3.0,
    "nbins": 25
  },
  "a8_metrics": {
    "enable_hierarchy_depth": true,
    "enable_slope_asymmetry": true,
    "enable_shoulder_contrast": true
  }
}
```

This keeps it aligned with your meter-grid pattern.

---

### Step 2 — Patch the T2 meter runner

File:
`Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_meter_synthetic_mocks_v1.py`

Algorithm (skeleton):

1. **Load spec JSON.**
2. **Construct `KappaProvider`** based on `spec["kappa_source"]`.
3. For each grid point (mock config) and for each void catalog entry:

   * Read void center $(\text{RA}_v, \text{Dec}_v, z_v, R_v)$.
   * Build radial bins in $R/R_v$ as per `profile_bins`.
   * For each galaxy / pixel in an annulus:

     * Query `kappa = kappa_provider.kappa_at(ra, dec)` if needed (for CMB-lensing–type contamination modeling or cross-checks).
     * Use your existing shear / convergence estimators to build:

       * $\gamma_t(R/R_v)$,
       * $\Delta\Sigma(R/R_v)$,
       * any E/B-mode splits you already use.
4. **Stack** profiles across voids for each configuration.

Your only real “surgery” is adding the κ-provider and optionally using κ in how you define the **background** or how you weight / clean profiles.

---

### Step 3 — Define the A8-facing metrics on the stacked profiles

Given a stacked, dimensionless profile $\gamma_t(R/R_v)$ (or $\Delta\Sigma$):

1. **Shoulder contrast metric** $C_\text{shoulder}$

   * Detect region(s) where derivative changes sign or strongly changes magnitude near the wall (e.g. $R/R_v \sim 1$).
   * Compute something like:
     [
     C_\text{shoulder} = \frac{\max_{R\in \mathcal W} \gamma_t(R) - \min_{R\in \mathcal I} \gamma_t(R)}{\sigma_\text{noise}}
     ]
     where $\mathcal W$ is a small window around the wall and $\mathcal I$ an interior window; $\sigma_\text{noise}$ from bootstrap / mocks.

2. **Slope asymmetry metric** $A_\text{slope}$

   * Compare inner vs outer log-slopes:
     [
     A_\text{slope} = \left|\frac{d\log\gamma_t}{d\log(R/R_v)}\Big|*\text{inner} - \frac{d\log\gamma_t}{d\log(R/R_v)}\Big|*\text{outer}\right|
     ]
   * This is a direct proxy for asymmetric boundaries predicted by A8 interfaces.

3. **Hierarchy depth proxy** $N_\text{eff}$

   * Count distinct shoulders / inflection points in the profile, constrained by significance threshold (e.g. $\ge 2\sigma$).
   * Map this to effective depth $N_\text{eff}(L)$ vs void scale $L\sim R_v$.

Implement these in a library module, e.g.:
`Derivation/code/physics/cosmology/void_lensing/lib/a8_profile_metrics.py`

---

### Step 4 — Run three core comparison modes

Using the same mocks-grid (same void catalogs, same randoms), run:

1. **Mode A (baseline):** `kappa_source = "none"`

   * Just your current void-lensing meter; use as the existing T2 baseline.

2. **Mode B (noisy recon, if available):** `kappa_source = "recon"`

   * If you’re already using a standard Planck or ACT reconstruction, keep this as “status-quo CMB-lensing contamination model”.

3. **Mode C (external template):** `kappa_source = "external_template"`

   * Feed in the ACT+unWISE+Planck CIB template.

For each mode, compute:

* Profile: $\gamma_t(R/R_v)$ and $\Delta\Sigma(R/R_v)$.
* Metrics: $C_\text{shoulder}$, $A_\text{slope}$, $N_\text{eff}$ with uncertainties.

---

### Step 5 — Reduce raw outputs to final objects

For each grid point and mode:

1. Save **raw stacked profiles** to HDF5 or CSV:

   * `Derivation/code/outputs/void_lensing/profiles/<tag>_mode{A,B,C}_profiles.csv`
2. Save **metrics** (per grid point) to JSON:

   * `.../<tag>_mode{A,B,C}_a8_metrics.json`
3. Compute **relative improvement** of template vs baseline:

   * $\Delta C_\text{shoulder}/C_\text{shoulder,baseline}$
   * $\Delta N_\text{eff}$ significance
   * Possibly a small Bayes factor or Δχ² comparing fits of an A8-like multi-shoulder model vs a simple one-scale void.

---

### Step 6 — Plots and comparisons to make

At minimum:

1. **Profile overlay plot**

   * For a representative grid point (and then a small panel of them):

     * Plot $\gamma_t(R/R_v)$ for modes A/B/C.
     * Highlight wall region and any detected shoulders.
   * Export PNG to:

     * `Derivation/code/outputs/void_lensing/figures/PROFILE_VoidLensing_kappaTemplate_vsBaseline_v1.png`

2. **Metric comparison plot**

   * Scatter or bar plot of $C_\text{shoulder}$ and $N_\text{eff}$ across grid points for modes A, B, C.
   * Show error bars; highlight where template mode increases significance beyond your T4/T5 gate.

3. **A8 scaling check**

   * Plot $N_\text{eff}$ vs $\log(L/\lambda)$ or vs $\log(R_v)$ to see if A8’s $\Theta(\log L)$ behavior emerges more clearly in the template-cleaned mode.

These are what you’ll reference in RESULTS and PROPOSAL docs.

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

Here’s a concrete file scaffold.

### 4.1 RESULTS file

**Filename (T2/T3-level):**
`Derivation/RESULTS/RESULTS_T2_Void_Lensing_KappaTemplate_Calibration_v1.md`

**Suggested sections:**

1. **Context & Scope**

   * What the external κ-template is and how it is used.
   * Scope banner: “Meter calibration; no novelty claim about cosmology yet.”

2. **Instruments & Data**

   * Brief description of:

     * Void-lensing meter (tag, script, spec).
     * External κ-template (ACT+unWISE+Planck CIB, correlation coefficients as quoted from the paper).
     * Mocks / catalogs used.

3. **Methods**

   * KappaProvider abstraction.
   * Modes A/B/C (none, recon, external template).
   * Definition of $C_\text{shoulder}$, $A_\text{slope}$, $N_\text{eff}$.

4. **Results (Calibration)**

   * Table of metrics per grid point.
   * Key figures:

     * Profile overlays.
     * Metric comparison plots.

5. **Gates & QC**

   * Explicitly state:

     * Which VALIDATION_METRICS gates are checked and passed.
     * Any failures / odd regimes (e.g., low S/N small voids).

6. **Contradictions & Limitations**

   * Cases where template doesn’t help or hurts.
   * Any tensions with expected A8 scaling.

7. **Next Steps**

   * Path to T3/T4: apply same procedure on real DES-Y6 / other void catalogs.

**Non-embarrassing standard:**

* At least **2–3 grid points** thoroughly shown, not just one cherry-picked example.
* At least **one figure showing clear metric improvement** from template mode, or an honest statement that no significant improvement is seen.

---

### 4.2 PROPOSAL file (T4-level)

**Filename:**
`Derivation/Proposals/T4_PROPOSAL_Void_Lensing_KappaTemplate_A8_Gates_v1.md`

**Suggested sections:**

1. **Statement & Motivation**

   * One paragraph summarizing:

     * A8 prediction (hierarchical void interfaces).
     * Why CMB-lensing systematics / reconstruction noise can mimic or wash out shoulders.
     * How the new κ-template acts as a **calibration anchor**.

2. **Target Axioms / CF Chain**

   * Explicit references:

     * A2, A6, A7, candidate A8.
     * CF3_A8_Scaling_Hierarchical_Interfaces.
     * T2 void-lensing meter.

3. **Hypotheses & Nulls**

   * Example:

     * H1: With template-based calibration, the detected shoulder contrast $C_\text{shoulder}$ for large voids exceeds baseline by ≥Xσ.
     * H2: The inferred hierarchy depth vs scale is more consistent with $N(L)=\Theta(\log L)$ under template calibration than under baseline.
     * H0: Any differences are consistent with noise and systematics.

4. **Data & Meters**

   * Which surveys / catalogs (e.g., DES-Y6 voids, mock catalogs).
   * Which κ template file version.
   * Void-lensing meter tag and configuration.

5. **Analysis Plan**

   * Pre-registered:

     * Binning strategy.
     * Metric definitions.
     * Windows for wall/interface regions.
   * How you will propagate uncertainties (bootstrap, jackknife, mocks).

6. **Gates & Decision Criteria**

   * Define specific thresholds:

     * Minimal S/N for $C_\text{shoulder}$.
     * Minimal number of independent void bins.
     * Goodness-of-fit to A8 scaling vs a naive single-scale model.

7. **Contradiction Routing**

   * Where contradictions go:

     * If shoulders vanish after template calibration → flags on A8 cosmic-void realization.
     * If shoulders strengthen → log stronger support for A8 in void sector.

**Non-embarrassing T4 standard:**

* Fully specified hypotheses and thresholds.
* All meters and data sources clearly identified with **paths and tags**.
* At least one mock-based dryness-check already summarized from the T2 RESULTS (so PROPOSAL is not purely speculative).

---

## 5. How this plugs back into the larger VDM story

This work sits right on top of your **“Void-lensing interface program (highest priority)”** in the roadmap, and links multiple chains:

* **Axiom / CF chain**

  * **A2 (Local Causality):** The template reduces reconstruction noise that would smear local void-wall signatures. Cleaner profiles let you test whether void interfaces behave like finite-speed, locally causal fronts or are artifacts of noise.
  * **A6 (Scale Program):** The entire analysis is framed in dimensionless $R/R_v$ and scaling groups, letting you look for **A8’s logarithmic depth law** across different void sizes and redshifts.
  * **A7 (Measurability):** This is pure instrumentation: converting a theoretical A8 claim into concrete, testable profile metrics and KPIs.
  * **Candidate A8 + CF3_A8_Scaling_Hierarchical_Interfaces:** The endgame is literally to see whether void lensing profiles exhibit the finite-depth, logarithmically scaling hierarchy of interfaces predicted by your tachyonic interface formalism.

* **Instrument chain**

  * Builds directly on your **T2 void-lensing meter** (already grid-tuned with mocks).
  * Talks to **FRW meters** when you interpret the profiles as perturbations around FRW.
  * Interacts conceptually with the **CMB polarization birefringence gate** (roadmap item 6): both are ways to clean and probe subtle interface physics in CMB-related observables.
  * Fits into the larger **A8 → cosmology chain**, alongside:

    * FRW continuity checks,
    * ringdown meter,
    * Skyrme SIDM and dark sector probes.

Within the sequence you pasted, this project lives primarily under:

* **4. Void-lensing interface program (highest priority)**
  with strong ties to:
* **4. Materialization: tachyonic condensation & hierarchy (A8)**
* **6. CMB polarization birefringence gate**
* and contributes toward the **T8 A8 out-of-sample** vision in the cosmology limb.

If Future-You only remembers this:

> *“This κ-template integration is how I turn A8 from a pretty interface-theorem into a calibrated, scale-aware void-lensing instrument that either finds real hierarchical shoulders in the universe or proves they’re an artifact of noise. It’s the bridge between my A8 math and actual void-wall measurements, sitting at the heart of the void-lensing interface program.”*

That’s the “why” in one breath.
