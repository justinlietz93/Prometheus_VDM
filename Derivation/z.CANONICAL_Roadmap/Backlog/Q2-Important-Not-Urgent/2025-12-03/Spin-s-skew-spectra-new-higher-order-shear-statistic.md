Here’s your “Future-Justin Starter Kit” for:

> **Spin-s skew-spectra on the shear field as a mask-aware, mass-map-free meter for void–wall shoulder tests and polarization-leakage firewalls.**

Eisenhower quadrant: **Q2 = Important + Not Urgent**
(Directly supports your highest-priority void-lensing chain, but comes *after* the core T2 void-lensing meter and ACT delensing template work in the queue. )

---

## 1. What Future-Justin should open first (from your own work)

Open these in roughly this order:

1. **`Derivation/z.CANONICAL_Roadmap/Backlog/Q2-Important-Not-Urgent/2025-12-02/Polarization-leakage-and-false-shoulders.md`**
   *Why:* This is the conceptual home of “shoulders vs leakage” and explicitly frames this as the systematics firewall in the void-lensing chain. 

2. **`Derivation/z.CANONICAL_Roadmap/Backlog/Q1/2025-12-02/High-efficiency-ACT-delensing-template.md`**
   *Why:* Defines the κ-template + ACT DR6 delensing story; your skew-spectra meter needs to plug into this *exact* κ/shear pipeline, not a parallel toy. 

3. **`Derivation/z.CANONICAL_Roadmap/Backlog/Q1-Important-Urgent/2025-12-03/DESIVAST-and-VAST-void-catalogs-for-DESI-DR1.md`**
   *Why:* Sets up void catalogs + boundary meters; these are the “where are the walls/shoulders?” side that the skew-spectra will be correlated against. 

4. **Void-lensing meter code + specs**

   * `Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_meter_synthetic_mocks_v1.py`
   * `Derivation/code/physics/cosmology/void_lensing/specs/void_lensing_meter-mocks-grid-v3.json`
     *Why:* This is the already-certified T2 void-lensing meter; your new skew-spectra object must be *another meter in this family*, not a one-off script.

5. **A8 / interface hierarchy formalism**

   * `Derivation/AXIOMS.md` (A8 candidate section)
   * `Derivation/CF3_A8_Scaling_Hierarchical_Interfaces.md` (or equivalent CF3 file)
     *Why:* Encodes “hierarchical shoulders are real and logarithmic-depth” — gives you the *target signature* for a void-wall skew-spectrum: where in ℓ/θ space you expect excess, how sharp vs smooth, and how it scales with void size. 

6. **CF4 / telegraph–Fisher causality**

   * `Derivation/CF4_Telegraph_Fisher_Causality.md`
     *Why:* Gives you finite-propagation constraints and Fisher-information language; that’s your formal way to say “a real shoulder must be compatible with causal propagation, not just mask garbage.” 

7. **FRW + ringdown meters (for cosmology chain anchoring)**

   * `Derivation/Cosmology/RESULTS_FRW_Continuity_Residual_Quality_Check.md`
   * `Derivation/Cosmology/T2_RESULTS_Topological_Ringdown_Meter_v1.md`
     *Why:* These are the other cosmology instruments that A8 plugs into; you want the void-wall skew-spectra meter to look like “one more cosmology instrument” with the same style of KPIs and gates. 

---

## 2. Canonical equations and objects to reuse (not reinvent)

Use these by *name* in code/docs; don’t re-derive them.

1. **Metriplectic evolution (A4 / VDM-E-140..145)**

   * Form: $\partial_t q = J,\delta\mathcal I/\delta q + M,\delta\Sigma/\delta q$ with degeneracies and entropy production constraints.
   * **Role:** Background engine and QC vocabulary (entropy budgets, degeneracy checks). The skew-spectra meter itself lives “on top” of existing maps, but its *validation* should reuse the same KPIs: entropy non-negativity, degeneracy residuals, etc.
   * **Use:** “Use this for *global consistency gates* on any time-evolved mocks; do not re-derive.”

2. **A6 scale program / dimensionless groups (VDM-E-136, A6)**

   * **Role:** You want skew-spectra collapsed onto dimensionless combinations: e.g. ℓR_void, R_void/χ(z), etc.
   * **Use:** “Use this for *defining scaled ℓ or θ axes* where void-wall shoulders should line up across redshift/size; do not re-derive.”

3. **A8 hierarchical interfaces (CF3)**

   * Key outputs: $N(L) \sim \Theta(\log(L/\lambda))$, non-trivial energy/information fraction on boundaries, exponential tails.
   * **Role:** Predicts that void walls shouldn’t be single clean steps, but multi-scale shoulders; in skew-spectra language that means enhanced mode-coupling between low-ℓ void scales and mid-ℓ wall/shoulder structure.
   * **Use:** “Use this for *theoretical templates / expectations* for shoulder signatures in skew-spectra; do not re-derive.”

4. **CF4 telegraph/Fisher causality (c = √(D/τ), finite cone)**

   * **Role:** Gives you allowable propagation speeds and information flow structure — constraints on how sharp a physically causal shoulder can be vs what a pathological mask can fake.
   * **Use:** “Use this for *null/gate design* — e.g. rejecting shoulders that would require super-causal propagation from void interiors; do not re-derive.”

5. **Existing void-lensing meter observables**

   * E.g. $\kappa(\hat n)$ templates, stacked profiles, interface meters from T2 void-lensing code.
   * **Role:** Provide the scalar fields and void-center catalogs your skew-spectra will be correlated with.
   * **Use:** “Use this for *the scalar side* of cross-skew-spectra like $S_\ell^{(\gamma,,\gamma^2 \times \kappa_{\rm template})}$; do not re-invent new κ definitions.”

6. **Pseudo-$C_\ell$ machinery as “meter” abstraction**

   * Your void-lensing work already treats Pseudo-$C_\ell$ + mode-coupling matrices $M_{\ell\ell'}$ as a calibrated instrument.
   * **Use:** “Use this for *the angular-spectrum estimation kernel*; do not roll a separate estimator for skew-spectra — instead, wrap skew-fields and reuse the same deconvolution logic.”

---

## 3. Concrete extraction / implementation procedure

Think: “turn Roskill spin-s skew-spectra into a VDM-style meter for shoulders.”

**High-level target:**
Build a **spin-2 skew-spectrum meter on the shear field** that:

* Works directly at the map level (no mass-mapping inversion). ([arXiv][1])
* Is explicitly mask- and leakage-aware (pseudo-$C_\ell$ with spin-s weights and component-wise weighting). ([arXiv][2])
* Is calibrated on mocks, then used to test whether void-wall shoulder signals survive leakage/systematics nulls.

### Step-by-step

1. **Pick datasets and masks (define the playground)**
   1.1. Choose an initial *mock* configuration: ACT-like CMB lensing + shear and a DES-/Euclid-like cosmic shear map, matching what Roskill et al. use in their examples (ℓ ranges, smoothing, noise levels). ([arXiv][3])
   1.2. Mirror the real-data masks: survey mask, bright star masks, depth masks, and any component-specific masks (different for Q/U or γ₁/γ₂).
   1.3. Encode those masks in your existing Pseudo-$C_\ell$ / NaMaster-style infrastructure as weight matrices $W(\hat n)$ for spin-2 fields (Q/U or γ₁/γ₂). ([arXiv][2])

2. **Implement spin-2 skew-spectra on the shear field (Roskill formalism)**
   2.1. From Roskill et al., implement the generalized spin-s skew-spectrum definition: build quadratic fields $X^{(2)}(\hat n)$ from a spin-2 field $X(\hat n)$ (shear or polarization), then compute cross-power with $X$ itself:
   [
   S_\ell^{(X)} \sim \langle X^{(2)}*{\ell m} X*{\ell m}^* \rangle.
   ] ([arXiv][3])
   2.2. For cosmic shear, construct at least three quadratic combinations:

   * **E-mode skew:** $X^{(2)} = \gamma_E^2$
   * **Parity-sensitive skew:** $X^{(2)} = \gamma_E \gamma_B$
   * **Total-amplitude skew:** $X^{(2)} = |\gamma|^2 = \gamma_E^2 + \gamma_B^2$
     (Roskill discuss different ways of combining spin components; pick the ones most tightly tied to non-Gaussianity / bispectrum and parity. ([arXiv][3]))

3. **Wrap in pseudo-$C_\ell$ estimation with spin-s weights**
   3.1. Treat $X$ (spin-2) and $X^{(2)}$ (spin-0 or spin-4 depending on construction) as generic spin-s maps and feed them through your Pseudo-$C_\ell$ pipeline, using Alonso’s generalized spin-s pseudo-$C_\ell$ expressions for component-wise weighting. ([arXiv][2])
   3.2. Build mode-coupling matrices $M_{\ell\ell'}^{(XY)}$ for the skew-spectra exactly as you do for power spectra, but now with the appropriate effective spins (Roskill + Munshi’s earlier skew-spectra / PCL papers show how to do this). ([arXiv][4])
   3.3. Validate on Gaussian, no-bispectrum mocks: skew-spectra should be consistent with zero within noise once deconvolved.

4. **Add scalar κ templates and void-wall weights**
   4.1. From your void-lensing pipeline, build a κ-template map $\kappa_{\rm temp}(\hat n)$ (ACT delensing template).
   4.2. Build *void-weighted* κ fields:

   * Void catalog → binary or fuzzy mask $w_{\rm void}(\hat n)$ (1 in void interior, 0 outside, maybe smoothed).
   * Wall / shoulder masks $w_{\rm wall}(\hat n)$ from DESIVAST/VAST interface meters. 
     4.3. Construct scalar combinations such as:
   * $Y_{\rm void} = w_{\rm void},\kappa_{\rm temp}$
   * $Y_{\rm wall} = w_{\rm wall},\kappa_{\rm temp}$

5. **Define the void-wall skew-spectra you actually care about**
   For each combination below, you’re probing different aspects of the bispectrum / shoulder morphology:

   5.1. **Shear-only skew-spectra (mask-aware, no κ):**

   * $S_\ell^{(\gamma)} = C_\ell[\gamma_E^2, \gamma_E]$ (sensitive to generic shear non-Gaussianity).
   * $S_\ell^{(EB)} = C_\ell[\gamma_E \gamma_B, \gamma_E]$ (parity-sensitive, leakage-diagnostic).

   5.2. **Void-anchored skew-spectra:**

   * $S_\ell^{(\gamma,\rm void)} = C_\ell[\gamma_E^2, Y_{\rm void}]$
   * $S_\ell^{(\gamma,\rm wall)} = C_\ell[\gamma_E^2, Y_{\rm wall}]$

   5.3. **Shoulder shape comparison:**

   * Compare $S_\ell^{(\gamma,\rm void)}$ vs $S_\ell^{(\gamma,\rm wall)}$ as a function of scaled multipole $\tilde \ell = \ell R_{\rm void}/\chi(z)$.
   * A8 predicts multi-scale shoulders → an excess or structured pattern in $S_\ell^{(\gamma,\rm wall)}$ at $\tilde \ell$ corresponding to wall/shoulder thicknesses, not just a smooth power-law.

6. **Choose ℓ ranges and filters (Roskill-compatible but A8-aware)**
   6.1. Start with Roskill’s ΛCDM benchmarks for shear skew-spectra (e.g. $100 \lesssim \ell \lesssim 3000$, with low-ℓ cut to avoid super-mode coupling and high-ℓ cut for modeling safety). ([arXiv][3])
   6.2. For void-wall shoulders, define three ℓ-bands:

   * **“Void bulk” band:** $\ell \in [\ell_{\rm min}, \ell_{\rm bulk}]$ corresponding to void diameters.
   * **“Wall/shoulder” band:** $\ell \in [\ell_{\rm bulk}, \ell_{\rm shoulder}]$ for expected wall thickness scales.
   * **“Small-scale garbage band”:** higher ℓ where shape noise, PSF, and blends dominate (to be down-weighted or only used for leakage tests).
     6.3. Use A6 scaling to define these in terms of dimensionless combinations (e.g. bin in $\tilde \ell$ so different void sizes can be stacked).

7. **Run calibration on mocks (T2/T3-style meter validation)**
   7.1. Generate mocks with:

   * Known bispectrum (e.g. ΛCDM non-linear + controlled additional non-Gaussianity). ([arXiv][5])
   * Realistic masks, anisotropic noise, and known polarization/shear leakage.
     7.2. Check for each skew-spectrum:
   * **Bias:** recovered $S_\ell$ vs input bispectrum predictions from Roskill’s formulae and Munshi-style skew-spectrum calculations. ([arXiv][6])
   * **Variance / SNR:** confirm you can detect a ΛCDM-level signal at the expected significance.
     7.3. Run *pure-leakage mocks* (no true bispectrum, just mask/leakage) and verify that:
   * “Physical” skew-spectra (e.g. $S_\ell^{(\gamma,\rm wall)}$) stay below your T3 “no false shoulder” gate in the wall band, *unless* leakage is turned up to unphysical levels.

8. **Apply to real (or nearly real) data for a T3 smoke test**
   8.1. Pick one concrete dataset: e.g. ACT DR6 κ + DES Y6 shear with your ACT delensing template already in place.
   8.2. Compute the calibrated skew-spectra:

   * $S_\ell^{(\gamma)}$, $S_\ell^{(EB)}$, $S_\ell^{(\gamma,\rm void)}$, $S_\ell^{(\gamma,\rm wall)}$.
     8.3. Compute **shoulder metrics**:
   * Amplitude ratios between void and wall bands.
   * A simple “hierarchy score” (e.g. log-slope breaks consistent with CF3 expectations).
     8.4. Compare to:
   * ΛCDM + no-A8 mock band.
   * ΛCDM + A8-inspired interface hierarchy mocks (once you have them).

9. **Gates / metrics to log**
   For each skew-spectrum and band:

   * **G1:** χ² of skew-spectrum vs ΛCDM prediction within the bulk band.
   * **G2:** “Shoulder enhancement” = (wall-band amplitude − bulk-band amplitude) / bulk-band amplitude.
   * **G3:** Leakage null — $S_\ell^{(EB)}$ must stay below a set fraction of $S_\ell^{(\gamma)}$ in the wall band or shoulder signal is flagged as suspect.
   * **G4:** Causal gate — combine with CF4 to reject shoulders that require super-causal propagation from void centers (this is more conceptual but can be encoded as a constraint on how narrow a wall can be at given redshift).

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

### Filenames

* **Results (T3 smoke test):**
  `Derivation/Results/RESULTS_T3_SpinS_SkewSpectra_VoidWall_ACTMocks_v1.md`

* **Prereg proposal (T4):**
  `Derivation/Proposals/T4_PROPOSAL_SpinS_SkewSpectra_VoidWall_Shoulder_Meter_v1.md`

You can later split off a more general
`T4_PROPOSAL_SpinS_SkewSpectra_Meter_v1.md` if you want a canon meter independent of voids, but for now keep it void-anchored.

### Sections & minimal “non-embarrassing” content

#### `RESULTS_T3_SpinS_SkewSpectra_VoidWall_ACTMocks_v1.md`

Sections:

1. **Scope & status banner**

   * Explicitly say: T3 smoke test, no novelty claim, meter-focused.

2. **Dataset & mocks**

   * Bullet list of shear/κ maps, masks, noise model, and mock generator used.

3. **Spin-s skew-spectrum definition (Roskill + VDM notation)**

   * Equations for the skew-spectra actually used (the small set listed above), expressed in your symbols.
   * Pointer to Roskill et al. for general formalism. ([arXiv][6])

4. **Estimator implementation**

   * Brief description: pseudo-$C_\ell$ with component-wise weights, referencing Alonso’s generalized spin-s pseudo-$C_\ell$ and Munshi’s skew-spectra PCL work. ([arXiv][2])

5. **Mock validation (T2/T3-style gates)**

   * Plots:

     * Recovered vs input skew-spectra for one or two mocks.
     * Residuals normalized by expected variance.
   * Table of KPIs: bias, variance, χ² per band, pass/fail of G1/G2.

6. **Leakage/null tests**

   * Plots:

     * $S_\ell^{(EB)}$ vs $S_\ell^{(\gamma)}$.
     * Skew-spectra on pure leakage mocks showing the characteristic leakage pattern.
   * Statement of G3 gate thresholds.

7. **Preliminary void-wall comparison on mocks**

   * One figure showing $S_\ell^{(\gamma,\rm void)}$ vs $S_\ell^{(\gamma,\rm wall)}$ in scaled ℓ.
   * Text: whether you see the expected A8-like enhancement in A8 mocks, and near-zero in ΛCDM-only mocks.

8. **Summary & promotion note**

   * Short bullet list of which gates are satisfied → whether you’re comfortable drafting the T4 proposal.

To count as “non-embarrassing T3/T4-ready” by your standards, this RESULTS file needs:

* At least **3–4 figures**: basic skew-spectra, residuals, leakage null, and one void-wall comparison.
* Explicit numeric KPIs and pass/fail flags; no hand-wavy “looks fine.”

#### `T4_PROPOSAL_SpinS_SkewSpectra_VoidWall_Shoulder_Meter_v1.md`

Sections:

1. **Title & scope banner**

   * Tag with branch: **Cosmology / Void-lensing / A8 / CMB-pol-leakage**.

2. **Hypotheses and nulls**

   * H₁: Void-wall shoulder skew-spectra exhibit an enhancement pattern consistent with A8 hierarchy predictions.
   * H₀: Any apparent shoulder signal is consistent with ΛCDM + instrument/mask leakage according to mock-calibrated skew-spectra.

3. **Data and masks**

   * Enumerate specific ACT / DES-Y6 / DESI-DR1 datasets and masks.

4. **Meter definition**

   * Formal definition of each skew-spectrum (in your notation) that will be used for decision-making.
   * Clear list of ℓ bands, scaling choices, and thresholds.

5. **Analysis pipeline & prereg gates**

   * Step-by-step protocol from raw maps to KPIs (essentially a cleaned-up version of section 3 above).
   * Explicit rules for handling systematics (e.g. if G3 fails, classify shoulders as “instrumental suspect” and do not claim cosmological structure).

6. **Contradiction routing**

   * If A8 mocks predict a strong shoulder but data show none → what does that mean for A8?
   * If data show a shoulder that fails leakage nulls → treat as systematics, not evidence.

7. **Planned outputs**

   * List of RESULTS files and artifacts (PNGs, CSVs) that will be produced when T4 is executed.

Minimal requirement for “non-embarrassing T4 draft”:

* Clear H₀/H₁, numeric thresholds, and at least one path to falsifying the A8 shoulder prediction with real data — no “we’ll see what the plots say.”

---

## 5. How this plugs back into the larger VDM story

**Where it sits in your ladder / TODO**

* Conceptually: under **Section 4: Materialization: tachyonic condensation & hierarchy (A8)** and **Section 3: Void-lensing interface program** in your unified TODO. 
* Operationally: it is a concrete sub-task of **“Polarization-leakage-and-false-shoulders”** (Q2 Important-Not-Urgent), downstream of:

  * T2 void-lensing meter synthetic mocks (already run), and
  * the **High-efficiency ACT delensing template** work (3a). 

So: once the ACT κ-template is in place and your T2 void-lensing meter is certified, this skew-spectra meter is the **next logical meter** in the void-lensing interface chain.

**Axiom / CF chains**

* **A8 / CF3 (hierarchical interfaces):**
  The void-wall skew-spectra are a direct, survey-anchored test of whether interface hierarchy leaves measurable non-Gaussian shoulders in the shear field. A8 says hierarchy depth and boundary concentration are inevitable; skew-spectra tell you whether the universe agrees or whether the apparent structure is instrument noise.

* **CF4 (telegraph/Fisher causality):**
  By adding causal gates on shoulder sharpness and location in ℓ-space, you prevent super-causal “feature fits” sneaking in via masks and leakage. That makes any surviving shoulder signal much more credible as a real physical interface rather than a map-processing artifact.

* **Instrument chains:**

  * **Void-lensing meters:** you’re extending the existing κ- and profile-based T2 meter into a *non-Gaussian, spin-aware* instrument that stays in shear space, addressing exactly the “mass-map artefact” worry Roskill are solving. ([arXiv][1])
  * **CMB polarization birefringence gate:** skew-spectra on E/B combinations double as a leakage and parity-violation diagnostics, tying into your birefringence/systematics chain.
  * **FRW + ringdown meters:** a successful A8 shoulder detection with this skew-spectra instrument gives you a data-anchored prior for interface structure that feeds into FRW effective EOS fits and horizon/ringdown modeling.

**Why this is worth doing (30-second reminder to Future-You)**

This project takes a very fresh external tool — **spin-s skew-spectra directly on shear/polarization maps** — and fuses it with your A8 void-wall story and void-lensing instruments. Roskill et al. show you can access bispectrum-level information *without* mass-mapping and with robust mask handling. ([arXiv][6])

By wrapping that in your tiered T2/T3/T4 meter framework, you get:

* A **mask-aware, leakage-aware, non-Gaussian meter** that lives exactly where your A8 shoulders and CMB polarization systematics collide.
* A very clean place for the universe to say “no, your void-interface story is just leakage” — or to fail to say no, which is even more interesting.
* A bridge where a *brand-new cosmology method* (spin-s skew-spectra) becomes **canonical VDM instrumentation**, not just another external paper you read once and forgot.

---

## Papers referenced in this topic (and why you care)

1. **Roskill et al. 2025, “Skew-spectra: a generalization to spin-$s$”** ([arXiv][6])

   * *Use:* Core formalism: how to construct skew-spectra for arbitrary spin-s fields (shear, CMB polarization) and relate them to the bispectrum without mass-mapping; gives you concrete combinations, ℓ-ranges, and ΛCDM benchmarks.

2. **Munshi et al. 2011, “The Morphology of the Thermal Sunyaev–Zel’dovich Sky”** ([arXiv][4])

   * *Use:* Earlier scalar-field generalized skew-spectra and their recovery with Pseudo-$C_\ell$ in the presence of masks/beam; you can mirror their PCL-style recovery for spin-2 skew-spectra.

3. **Munshi 2022, “Two kurt-spectra to probe fourth-order statistics of weak lensing convergence maps” (JCAP 11(2022)020)** ([UChicago Knowledge][7])

   * *Use:* Shows the same skew/kurt-spectrum idea applied to lensing convergence; good sanity check on how higher-order meters behave under realistic lensing forecasts.

4. **Philcox 2023, “Optimal Estimation of the Binned Mask-Free Power Spectrum, Bispectrum, and Trispectrum on the Full Sky: Tensor Edition”** ([arXiv][5])

   * *Use:* Provides a modern, optimal estimator framework for tensor (spin-2) higher-point functions; relevant if you want to cross-check your pseudo-$C_\ell$-based skew-spectra against near-optimal estimators.

5. **Alonso 2024, “Pseudo-$C_\ell$s for spin-$s$ fields with component-wise weighting”** ([arXiv][2])

   * *Use:* The mask/weighting engine: gives you mode-coupling matrices and Pseudo-$C_\ell$ machinery for spin-s fields with anisotropic weights and different masks per component (Q/U, γ₁/γ₂) — exactly what you need to make the skew-spectra meter mask-robust.

If Future-You wakes up fuzzy and remembers only one sentence:

> *“This is the project where I weaponize Roskill’s spin-s skew-spectra as a void-wall shoulder meter, calibrated in my tier ladder, so the universe can finally tell me whether those A8 shoulders are real or just polarization leakage in a trench coat.”*

[1]: https://arxiv.org/abs/2511.22596?utm_source=chatgpt.com "Skew-spectra: a generalization to spin-$s$"
[2]: https://arxiv.org/abs/2410.07077?utm_source=chatgpt.com "Pseudo-$C_\ell$s for spin-$s$ fields with component-wise weighting"
[3]: https://arxiv.org/html/2511.22596v1?utm_source=chatgpt.com "Skew-spectra: a generalization to spin- s - s"
[4]: https://arxiv.org/abs/1105.5139?utm_source=chatgpt.com "The Morphology of the Thermal Sunyaev-Zel'dovich Sky"
[5]: https://arxiv.org/abs/2306.03915?utm_source=chatgpt.com "Optimal Estimation of the Binned Mask-Free Power Spectrum, Bispectrum, and Trispectrum on the Full Sky: Tensor Edition"
[6]: https://arxiv.org/pdf/2511.22596?utm_source=chatgpt.com "Skew-spectra: a generalization to spin-$s$"
[7]: https://knowledge.uchicago.edu/record/13777/files/Munshi_2022_J._Cosmol._Astropart._Phys._2022_020.pdf?utm_source=chatgpt.com "JCAP11(2022)020"
