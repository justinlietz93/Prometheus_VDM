Here’s your “Future-Justin Starter Kit” for this exact thing you were just thinking about.

---

### Meta for this task

* **Eisenhower Quadrant:** **Q2 – Important + Not Urgent (schedule soon)**
* **Topic / object:**
  **“ACT DR6 T→P leakage template + void-lensing ‘shoulder’ null test in the VDM void-lensing meter stack.”**
* **External anchors (papers / results):**

  * *“The Atacama Cosmology Telescope DR6 power spectra likelihoods and ΛCDM parameters”* (JCAP 11 (2025) 062) – DR6 T→P leakage model and correction strategy.
  * ACT DR6 map release + documentation for polarization maps and transfer functions.
* **High-level goal in your stack (one-liner):**
  Give the **void-lensing interface meter** a **CMB polarization systematics firewall**, by quantifying how much of the “shoulder” signal could be mimicked by ACT DR6 T→P leakage and ruling that out (or in) with your own meters.

---

## 1. What Future-Justin should open first (from your own work)

Open these in roughly this order:

1. **Roadmap / prioritization**

   * `Derivation/z.CANONICAL_Roadmap/Backlog/Q1/Current_TODO.md`
     *Why:* Confirms that “Void-lensing interface program” and “CMB polarization birefringence gate” are already on the core ladder; this task is basically the **ACT leakage sub-gate** for those.

2. **Void-lensing meter code + specs (already used for mocks grid)**

   * `Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_meter_synthetic_mocks_v1.py`
   * `Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-grid-v3.json`
     *Why:* This is your working T2 meter skeleton with H1–H3, AUROC, shoulder metrics, etc. You’ll clone this for an **ACT-DR6-specific leakage null** experiment.

3. **Void-lensing / interface CF doc(s)**

   * Whatever you’ve named the CF for void interfaces, e.g.

     * `Derivation/CF/CFx_Void_Lensing_Interface_Meter.md` (or similar)
       *Why:* Contains the **definitions of void interface, shoulder profile, and meter hypotheses H1–H3**; the leakage gate must reuse these definitions, not invent new ones.

4. **Causality / finite-speed transport canon (for “no unphysical leakage”)**

   * `Derivation/CF/CF4_Telegraph_Fisher_Causality.md`
     *Why:* Gives you the **telegraph / Fisher causal cone** and language to argue about what kinds of map-level leakage distortions are physically admissible vs pure instrument artifacts.

5. **FRW & CMB cosmology instruments**

   * `Derivation/code/physics/cosmology/FRW/...` (meters + results)
   * `Derivation/CF/CF3_A8_Scaling_Hierarchical_Interfaces.md` (A8 → void hierarchy)
     *Why:* You’ll want to phrase void-wall shoulders as **A8-style hierarchical interfaces in the CMB lensing field**, and distinguish that from **pure map leakage**.

6. **CMB polarization / birefringence gate stub**

   * Whatever you started for this, e.g.:

     * `Derivation/cosmology/CMB/T2_PROPOSAL_CMB_Pol_Birefringence_Gate_v1.md`
       *Why:* This ACT leakage null is a **sub-meter** of the broader CMB pol gate; reuse its notation for Q/U, E/B, α(n̂) if present.

If any of the specific CF/T* files don’t exist yet, create them using these names rather than inventing new styles; consistency is the point.

---

## 2. Canonical equations and objects to reuse (not reinvent)

Use these as **imported canon**, not re-derived in this task:

1. **Metriplectic KG+RD engine**

   * Symbols: `Φ(x, t)`, `J`, `M`, `H[Φ]`, `S[Φ]` and the evolution
     [
     \dot{Φ} = J ,\frac{δH}{δΦ} + M ,\frac{δS}{δΦ}
     ]
   * **Role:** Background: void field dynamics, causality, and interface sharpening. **Use this as the story for what the void really is. Do not fiddle with J/M here.**

2. **Void-lensing meter definitions**

   * `γ_t(r)` = tangential shear profile around void centers.
   * “Shoulder” metric `S_sh` = e.g. contrast of shear between inner shell and outer shell, plus slope asymmetry.
   * Hypotheses H1–H3:

     * H1: presence of non-Gaussian, interface-like shoulder vs smooth underdensity.
     * H2: hierarchy (large vs small voids) shows scale-broken profiles.
     * H3: robustness across mocks / catalogues.
   * **Role:** These are your **existing H1–H3**; the leakage gate should **ask whether leakage alone can pass the same H’s**.

3. **CMB polarization objects**

   * Stokes fields: `T(n̂)`, `Q(n̂)`, `U(n̂)`; spin-2 decomposition to `E(n̂)`, `B(n̂)`.
   * Birefringence angle: `α(n̂)` with
     [
     (Q \pm iU)'(n̂) = e^{\pm 2 i α(n̂)} (Q \pm iU)(n̂)
     ]
   * **Role:** You will reuse the **Q/U → E/B machinery** and the **α(n̂)** language from the CMB pol gate so that “leakage vs true birefringence vs void-shear” are all expressed in the same basis.

4. **ACT DR6 leakage operator (conceptual)**

   * Treat as a **linear transfer operator**:
     [
     (Q_\text{leak}, U_\text{leak}) = \mathcal{L} , T
     ]
     where (\mathcal{L}) is ℓ-dependent and array-band dependent (from DR6).
   * **Role:** In code, this is a combination of **harmonic-space kernels or pre-supplied templates** from ACT. You don’t re-derive it; you just implement it as provided (or as close as the public products allow).

5. **Causal-cone / telegraph equation (CF4)**

   * Telegraph-like form:
     [
     τ , \ddot{ψ} + \dot{ψ} = D \nabla^2 ψ
     ]
     with `c = sqrt(D/τ)` and **finite propagation speed**.
   * **Role:** Use this as the **conceptual constraint** when you argue about whether a “shoulder-like” pattern can arise from physical propagation vs map-level leakage—i.e., leakage distortions don’t obey your causal metriplectic cone, but true lensing-interface signals do.

6. **A8 scaling / hierarchical interfaces**

   * Interface hierarchy depth: `K(L) ~ Θ(log L)` from CF3.
   * **Role:** Use this to interpret “large vs small voids” and their shoulders as manifestations of A8; this helps phrase the final RESULTS doc in terms of **“A8 survives the leakage null”** instead of just “signal still there.”

---

## 3. Concrete extraction / implementation procedure

Think of this as building **one new T2 experiment script + spec** and **two new data pipelines**:

* Pipeline A: ACT DR6 maps **as-is** (baseline).
* Pipeline B: ACT DR6 maps **with T→P leakage template subtracted**.
* Pipeline C: **leakage-only synthetic** (no true polarization) as a **hard null**.

---

### Step 0 – Clone the existing meter skeleton

1. Copy your current mocks experiment:

   * From:
     `Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_meter_synthetic_mocks_v1.py`
   * To (new file):
     `Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_ACTDR6_leakage_null_v1.py`
2. Copy the spec:

   * From:
     `Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-grid-v3.json`
   * To:
     `Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_ACTDR6_leakage-null-v1.json`
3. Strip the synthetic-mocks grid stuff and replace the data source entries with fields for:

   * `act_dr6_temperature_map` (per band or coadd)
   * `act_dr6_Q_map`, `act_dr6_U_map`
   * `act_dr6_leakage_kernel` or references to pre-computed leakage templates
   * `void_catalog` (the void centers you’ll stack around)

---

### Step 1 – Implement the leakage operator 𝓛 on ACT DR6 maps

4. In a new module, e.g.
   `Derivation/code/physics/cosmology/cmb/systematics/act_dr6_leakage_operators.py`, implement:

   ```python
   def apply_T_to_P_leakage_kernel(T_map, leakage_kernel):
       """
       T_map: HEALPix or flat-sky temperature map
       leakage_kernel: structure encoding ℓ-dependent or pixel-space kernel
       returns: Q_leak_map, U_leak_map
       """
       # 1. Transform T_map to harmonic or Fourier space
       # 2. Apply leakage_kernel (band-dependent)
       # 3. Transform back, split into Q_leak, U_leak as given by DR6 model
   ```

5. If ACT provides map-level leakage templates directly (e.g. `leak_Q`, `leak_U` per band), treat them as the result of 𝓛 and **skip the kernel construction**; your function just loads those.

6. Add a helper:

   ```python
   def subtract_leakage(Q_map, U_map, Q_leak, U_leak):
       return Q_map - Q_leak, U_map - U_leak
   ```

---

### Step 2 – Build the three pipelines (A/B/C)

7. In `T2_void_lensing_ACTDR6_leakage_null_v1.py`, define three meter configurations sharing the same void catalog and stacking machinery:

   * **Pipeline A – Baseline ACT DR6:**

     * Input maps: `(T, Q, U)` from DR6.
     * No subtraction.
     * Output metrics: `S_sh^A`, AUROC, interface counts, H1–H3 decision.

   * **Pipeline B – Leakage-subtracted:**

     * Compute `(Q_leak, U_leak) = 𝓛[T]` (per band or coadd).
     * Form `(Q_clean, U_clean) = (Q, U) - (Q_leak, U_leak)`.
     * Run the **exact same void-stacking / shear-estimation code** as baseline.
     * Output metrics: `S_sh^B`, AUROC, etc.

   * **Pipeline C – Leakage-only null:**

     * Use `(Q_only, U_only) = (Q_leak, U_leak)` with **no true polarization**.
     * Run the same stack.
     * Output metrics: `S_sh^C`, AUROC, etc., expected to **fail H1–H3** if the shoulder is truly cosmological.

8. Ensure the spec JSON exposes a simple switch, e.g.:

   ```json
   "pipelines": [
     {"name": "ACT_DR6_baseline", "mode": "baseline"},
     {"name": "ACT_DR6_leakage_subtracted", "mode": "leakage_subtracted"},
     {"name": "ACT_DR6_leakage_only", "mode": "leakage_only"}
   ]
   ```

   and your experiment script branches on `mode` with common code for stacking and metrics.

---

### Step 3 – Reuse the void-lensing meter (no new statistics if possible)

9. Import your existing meter functions from the mocks code:

   ```python
   from Derivation.code.physics.cosmology.void_lensing.meters import (
       compute_shear_profile,
       compute_shoulder_metrics,
       evaluate_H1_H3,
   )
   ```

10. For each pipeline, do:

* Convert `(Q, U)` (or `(Q_clean, U_clean)`, `(Q_leak, U_leak)`) into shear estimates in annuli around voids.
* Compute:

  * `γ_t(r)` profiles (stacked over all voids or in bins of void radius).
  * Shoulder metric `S_sh` and slope asymmetry.
  * Any existing H1–H3 gate scores (e.g. AUROC vs randomized catalogs).

11. Save a compact summary per pipeline:

```json
{
  "pipeline": "ACT_DR6_leakage_subtracted",
  "S_sh": ...,
  "S_sh_err": ...,
  "AUROC": ...,
  "H1_pass": true,
  "H2_pass": true,
  "H3_pass": false,
  "notes": "..."
}
```

into something like:
`Derivation/results/cosmology/void_lensing/T2_void_lensing_ACTDR6_leakage_null_v1.json`.

---

### Step 4 – Define the comparison metrics and gates

12. Introduce **relative suppression factors**:

* Leakage impact on shoulder amplitude:
  [
  R_\text{sh} = \frac{S_\text{sh}^B}{S_\text{sh}^A}
  ]
* Leakage-only shoulder fraction:
  [
  f_\text{leak} = \frac{S_\text{sh}^C}{S_\text{sh}^A}
  ]

13. Suggested gate thresholds (tune later but write them down):

* **Gate G1 (non-leakage dominated):**
  `f_leak < 0.1` (leakage-only explains <10% of baseline shoulder amplitude).

* **Gate G2 (robust under subtraction):**
  `R_sh > 0.7` and H1–H3 still pass for pipeline B.

* **Gate G3 (shape stability):**
  L2 norm difference between normalized profiles
  [
  ||\hat{γ}_t^A(r) - \hat{γ}_t^B(r)||*2 < ε*\text{shape}
  ]
  with e.g. `ε_shape ≈ 0.2`.

14. Compute these gate metrics in the experiment and dump them to JSON so the RESULTS doc just **reads them off**.

---

### Step 5 – Plots / figures to generate

15. For the T2 RESULTS doc, plan to auto-generate:

16. **Figure 1:** `γ_t(r)` profiles for A/B/C on the same axes, with error bars.

    * Show especially the region where the shoulder lives.

17. **Figure 2:** Histogram or violin plot of `S_sh` across bootstrap resamples for A/B/C.

18. **Figure 3:** `R_sh` and `f_leak` with error bars vs void radius bins (showing hierarchy).

19. **Figure 4 (optional):** Map-space visual of one patch: `(Q, U)`, `(Q_clean, U_clean)`, and `(Q_leak, U_leak)` for intuition.

20. Save plots under e.g.:
    `Derivation/results/cosmology/void_lensing/figures/ACTDR6_leakage_null_*_v1.png`.

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

Here’s a minimal but non-embarrassing scaffold set.

### 4.1 RESULTS file

**Filename:**

* `Derivation/results/cosmology/void_lensing/RESULTS_T2_Void_Lensing_ACTDR6_Leakage_Null_v1.md`

**Sections:**

1. **Context & Goal**

   * One-paragraph reminder: you already have a T2 void-lensing meter; this doc asks whether ACT DR6 T→P leakage could fake the observed shoulder.

2. **Data & Pipelines**

   * Brief description of:

     * ACT DR6 maps used (bands, mask, resolution).
     * Void catalog used.
     * Pipelines A/B/C as defined above.

3. **Meter Definitions (Imported)**

   * Short summary of:

     * `γ_t(r)`, `S_sh`.
     * H1–H3 (referencing the main void-lensing CF doc).
     * New gate metrics `R_sh`, `f_leak`, and profile-shape distance.

4. **Results**

   * Subsections:

     * **4.1. Shoulder amplitudes & gates**

       * Table with `S_sh^A`, `S_sh^B`, `S_sh^C`, `R_sh`, `f_leak`, gate pass/fail.
     * **4.2. Profile shapes**

       * Discussion of Figure 1 & 3; are shoulders preserved after subtraction?
     * **4.3. Null pipeline behavior**

       * Show that leakage-only fails H1–H3 (this is key).

5. **Null Tests & Systematics Discussion**

   * Explicit bullet list:

     * Mask randomization.
     * Catalog randomization.
     * Band dependence (if you can do per-band).
     * Residual leakage estimate vs ACT’s quoted 0.3%.

6. **Gate Decision & Impact on VDM**

   * Final bullet:

     * “G1, G2, G3 passed/failed,” and what that implies for:

       * The T2 void-lensing meter’s validity.
       * The planned T4 void-lensing + A8 proposal.

7. **Next Steps**

   * Link to the PROPOSAL doc below and to the CMB birefringence gate.

**Minimal requirement for “non-embarrassing T2/T3”:**

* At least 1 ACT DR6 configuration fully run.
* All three pipelines A/B/C with quantitative metrics.
* At least Figures 1 and 2.
* Clear pass/fail statement for G1–G3.

---

### 4.2 PROPOSAL file

**Filename:**

* `Derivation/proposals/cosmology/T3_PROPOSAL_CMB_Pol_Leakage_Gate_for_Void_Lensing_v1.md`

**Sections:**

1. **Summary**

   * 3–5 sentences: define the leakage gate as a **standardized, reusable meter** applicable to ACT, SPT, Simons Obs, etc.

2. **Background & Canon Anchors**

   * Cite:

     * CF3 (A8 interfaces).
     * Void-lensing meter CF.
     * CF4 causality.
     * CMB birefringence gate stub.

3. **Meter Definition**

   * Formal definitions of:

     * Pipelines A/B/C.
     * `S_sh`, `R_sh`, `f_leak`, shape distance.
     * H-style hypotheses for leakage gate, e.g.:

       * L1: leakage-only cannot pass H1–H3.
       * L2: shoulder survives leakage subtraction.
       * L3: leakage contribution < X% across scales.

4. **Experimental Plan**

   * Stage 1: Implement and run on ACT DR6.
   * Stage 2: Apply to at least one other experiment or simulation.
   * Stage 3: Integrate into CMB birefringence gate as a prerequisite.

5. **Success Criteria & Tiering**

   * Define **T3 success**: mock + real data with clear gates and figures (what the RESULTS doc just did).
   * Define **T4 upgrade path**: cross-experiment confirmation, inclusion in a paper.

6. **Risks & Contradiction Modes**

   * Enumerate failure modes:

     * Leakage-only passes H1–H3.
     * Subtraction kills the shoulder.
     * Strong band dependence that doesn’t match VDM predictions.
   * Say explicitly: these would trigger a **contradiction report** and force a re-examination of the void-lensing meter.

---

## 5. How this plugs back into the larger VDM story

This task is the **bridge between your A8 void interface predictions and the messy reality of CMB instruments**. On the axiom/CF side, it touches **CF3 (A8 hierarchical interfaces)** and **CF4 (telegraph/Fisher causality)**: A8 says void walls should have structured, scale-broken interfaces, and CF4 says those structures propagate under strict causal rules. On the instrument side, it sits directly in the **void-lensing meter chain** and the **CMB polarization birefringence gate**, acting as a **systematics firewall**: if the shoulder signal survives a rigorous ACT DR6 leakage null (pipelines A/B/C, gates G1–G3), then your void-interface story graduates from “pretty numerics” to “survived the most obvious CMB map-level booby trap.” That, in turn, makes every downstream thing—A8→FRW, dark sector stress-energy, horizon structure—much more believable, because the first place the universe could have said “nope, this is just leakage” has been explicitly checked and logged.
