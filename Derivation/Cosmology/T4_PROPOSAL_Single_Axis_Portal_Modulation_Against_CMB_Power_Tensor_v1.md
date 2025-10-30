# 1. **T4 (Preregistered)** — Testing a Single‑Axis VDM Portal Modulation Against CMB Low‑ℓ Power‑Tensor Anomalies

> **Created Date:** 2025‑10‑30  
> **Commit:** 80ee5476e4f887fed3c34534a99daa878f55382f  
> **Salted hash:** *to be generated from the commit at post*  
> **Proposer contact(s):** ([justin@neuroca.ai](mailto:justin@neuroca.ai))  
> **License:** See LICENSE in repository  
> **TL;DR:** Proposed is a preregistered, fully specified test of whether a **single, VDM‑predicted anisotropy axis** with small amplitude explains the **persistent low‑ℓ CMB power‑tensor anomalies** across WMAP and Planck; pass/fail gates hinge on axis stability, likelihood improvement, and cross‑release reproducibility.  

---

## 2. **List of proposers and associated institutions/companies**

**Justin K. Lietz** — PI, Neuroca AI / VDM Project (architecture, preregistration, gates)
Additional implementers/approvers to be appended upon internal sign‑off.

---

## 3. **Abstract** (≤200 words)

Persistent **low‑multipole alignments and power‑entropy deficits** appear in full‑sky CMB temperature maps from **WMAP** and **Planck**, even after uniform masking, inpainting, and mission‑specific simulations. The **power‑tensor** method isolates eigen‑axes per multipole and reveals **collective alignment** and **entropy deficits** inconsistent with the isotropic null at ≳2σ, with statistically robust contributions from ℓ≈13, 17, 30 and others. This proposal preregisters a **Void Dynamics Model (VDM)** mechanism—**small portal modulation** of electromagnetic response by a slow scalar background—predicting a **single preferred axis** and **rank‑1 deformations** of the multipole power tensors. The test fits a two‑parameter model (axis, amplitude) jointly across **2≤ℓ≤61**, evaluates **likelihood gains** over null, and checks **axis stability** across releases and pipelines. Data are sourced from **WMAP (LAMBDA)** and **Planck SMICA + FFP simulations (PLA)**, following Patel, Aluri & Ralston (2025) preprocessing (Nside=512, 1° smoothing, unified mask, ISAP inpainting). Success would elevate VDM from conceptual plausibility to a falsifiable account of a long‑standing cosmological anomaly. Failure triggers a contradiction report and parameter‑space kill‑plan.  

---

## 4. **Background & Scientific Rationale**

**Observed anomaly (meter‑side):** Using the **power tensor** (A_{ij}(\ell)) built from (a_{\ell m}), Patel et al. compute the **power entropy** (S(\ell)=-\sum_{\alpha=1}^3 \lambda_\alpha\ln\lambda_\alpha) and the **alignment tensor** over ranges of ℓ; across WMAP and Planck releases, **entropy deficits** and **axis alignments** recur, with collective deviations at ≳2σ even after multiple‑testing‑aware statistics and Kuiper tests. Their **log‑likelihood‑style global statistic** over (2\le\ell\le61) shows the ensemble is **not as random** as the cosmological principle predicts; ℓ = 13, 17, 30 stand out across all releases. Figures and methods (Nside=512, 1° smoothing; unified Kp8∪Planck mask with (f_{\rm sky}\approx0.929); ISAP inpainting; Planck FFP simulations) are explicit.  

**VDM hypothesis (theory‑side):** VDM posits a slow background field influencing matter/fields via **weak portal modulation**. In minimal form, the effective permittivity is
[
\varepsilon_{\rm eff}(\mathbf{x},t)=\varepsilon_0\bigl(1+\alpha,C(\mathbf{x},t)\bigr),\quad |\alpha|\ll1,
]
with (C) a slow scalar order parameter; this induces **mild, coherent anisotropy** over super‑horizon angular scales at last scattering and **rank‑1** distortions of the per‑ℓ power tensors, yielding a **common principal eigenvector** across low ℓ and **systematic entropy deficits** proportional to (\alpha^2). This portal is codified as VDM‑E‑008; the slow field dynamics arise as either an overdamped RD branch (VDM‑E‑015/E‑028) or EFT/Klein‑Gordon branch (VDM‑E‑014/E‑031), both consistent with Axioms A0–A7 (locality, symmetry, metriplectic structure).  

**Scope/novelty discipline:** No novelty is claimed for the **meter** (power‑tensor statistics) or for the **anomaly reportage**; novelty lies in a **falsifiable VDM prior** (single axis + weak amplitude) and stringent preregistered **cross‑release gates**. Methods follow standard data‑analysis rules (masking, simulations, specification tests) and preregistration norms.  

**Classification:** **Derived‑limit** — cosmological observable modeled as a small‑coupling VDM portal perturbing standard isotropic Gaussian CMB statistics (Axiom‑core preserved).  

---

## 5. **Intellectual Merit and Procedure**

**Importance:** Low‑ℓ anomalies have persisted across missions and pipelines; a single‑axis account (if true) would constrain **large‑scale physics** beyond vanilla ΛCDM without invoking ad hoc free functions per multipole.  

**Broader impacts:** A pass would establish a **reproducible, parameter‑sparse** anisotropy phenomenology tied to an axiomatized theory (VDM), improving model comparison, simulation targets, and cross‑domain inference discipline. A fail cleanly constrains VDM’s portal coupling.

**Approach clarity:** Treat the **power‑tensor** machinery as the **measuring instrument**. Fit a **two‑parameter** VDM anisotropy (axis (\hat f), amplitude (\epsilon)) to per‑ℓ power tensors (A_{ij}(\ell)) simultaneously for (2\leq \ell \leq 61). Compare to null via preregistered likelihood gates and axis‑stability gates, with simulation‑calibrated p‑values.  

**Rigor/discipline:** Explicit preregistration, out‑of‑sample checks across releases, and **kill‑conditions**. Statistical practice follows specification‑test and calibration rules; inferential claims are probability‑based, not dichotomous.

---

### 5.1 **Experimental Setup and Diagnostics**

**Model under test (VDM prior):** For each ℓ,
[
A_{ij}^{\text{model}}(\ell)=\frac{C_\ell}{3}\Bigl[\delta_{ij}+\epsilon,g_\ell,\bigl(3,\hat f_i\hat f_j-\delta_{ij}\bigr)\Bigr],\qquad |\epsilon|\ll1,
]
where (C_\ell) is the standard isotropic power (mission‑specific), (\hat f) is a **single global axis**, and (g_\ell) is a (preregistered) scaling: **Branch A** (g_\ell=1) (coherent, super‑horizon portal), **Branch B** (g_\ell\propto [\ell(\ell+1)]^{-1}) (screened EFT). Both arise as small‑anisotropy projections of VDM E‑008 combined with either RD or EFT branches (E‑015, E‑014/E‑031). Fitting targets the **eigenvalue triplets** and **principal eigenvectors** of (A_{ij}(\ell)) across ℓ.  

**Primary diagnostics (per ℓ and collectively):**

* **Power entropy** (S(\ell)) and its null p‑value; global statistic (\bar S\equiv -\sum_\ell \log\bigl[1-F(S(\ell))\bigr]).  
* **AT entropy** (S_X) and **AT‑PEV** (\tilde f) for stability of the **collective axis**.  
* **Axis dispersion**: pairwise angular separations between fitted (\hat f) (this model) and data‑driven AT‑PEVs across releases.
* **Likelihood gain**: (\Delta \log \mathcal{L}) of VDM model vs null from per‑ℓ tensor eigen‑spectra.

**Dimensionless analysis:** The only free, dimensionless control is (\epsilon); all comparisons are **scale‑free** after normalizing by (C_\ell). Predictions are monotone in (|\epsilon|) for entropy deficits and alignment concentration (Axiom A6).  

**Preprocessing diagnostics:** Reproduce the meter behavior (entropy curves, anomalous ℓ list, Kuiper tests) under Patel et al.’s unified mask ((f_{\rm sky}\approx0.929)), **Nside=512**, **1° Gaussian** beam, and **ISAP** inpainting before any model fitting; this is the **T2 instrument** gate. See their **Fig. 1 (p. 3)** for the mask and (f_{\rm sky}).  

---

> **Context note (methods and data):** The configuration below targets the low‑ℓ CMB alignment experiment using the power‑tensor (PT) framework and its power‑entropy (PE), alignment‑tensor entropy (AE), pairwise alignment statistic (x=1-\cos\alpha), Kuiper tests, and the log‑likelihood–style global statistic (\bar x=-\sum_\ell \log[1-F(x_\ell)]) over (2\le \ell\le61). The ℓ‑range, PT/PE/AE definitions, unified mask practice, and simulation discipline follow Patel, Aluri & Ralston (2025).  
> **Authoring/gates discipline:** Artifacts emitted by the runner must satisfy whitepaper‑grade gates and provenance practices exactly as specified in RESULTS standards.  

---

## 5.1.1 Pre‑Run Config Requirements

**Required config and metadata (domain = `cosmology_cmb_lowL_alignments`):**

* `Derivation/code/physics/cosmology_cmb_lowL_alignments/APPROVALS.json`
* `Derivation/code/physics/cosmology_cmb_lowL_alignments/schemas/`

  * `cmb-pt.schema.json`
* `Derivation/code/physics/cosmology_cmb_lowL_alignments/specs/`

  * `pt_pe_ae_fullscan.0.1.0.json`

> **Filename note:** The canonical filename for the approval manifest is `APPROVALS.json` (plural). If legacy tooling expects `APPROVAL.json`, create a repo alias/symlink to the pluralized file.

### `APPROVALS.json`

**Shape:** JSON array with two objects, in order: an approval *manifest* and an approval *registry* (which binds PROPOSAL prereg and schema/tag approvals).

```json
[
  {
    "preflight_name": "cmb_lowL_preflight",
    "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
    "author": "Justin K. Lietz",
    "requires_approval": true,
    "pre_commit_hook": true,
    "domain": "cosmology_cmb_lowL_alignments",
    "notes": "Preflight runs under Derivation/code/tests are allowed without approval. Any run that writes artifacts requires a PROPOSAL_* in Derivation/cosmology_cmb_lowL_alignments and explicit review."
  },
  {
    "pre_registered": true,
    "proposal": "Derivation/cosmology_cmb_lowL_alignments/T4_PROPOSAL_CMB_LowL_Alignment_Isotropy_Gate.md",
    "allowed_tags": [
      "cmb-pt-2025.10"
    ],
    "schema_dir": "Derivation/code/physics/cosmology_cmb_lowL_alignments/schemas",
    "approvals": {
      "cmb-pt-2025.10": {
        "schema": "Derivation/code/physics/cosmology_cmb_lowL_alignments/schemas/cmb-pt.schema.json",
        "approved_by": "Justin K. Lietz",
        "approved_at": "<auto ISO-8601 timestamp>",
        "approval_key": "<auto sha256(proposal|commit|salt)>"
      }
    }
  }
]
```

### `PRE-REGISTRATION.json`

**Path:** `Derivation/code/physics/cosmology_cmb_lowL_alignments/PRE-REGISTRATION.json`
**Minimum keys plus domain‑specific content (placeholders only where automation fills provenance):**

```json
{
  "proposal_title": "CMB Low-ℓ Power-Tensor Alignment & Entropy Gates (2 ≤ ℓ ≤ 61)",
  "tier_grade": "T4",
  "commit": "<git-sha>",
  "salted_provenance": "sha256(<git-sha>|<salt>)",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Global log-like statistic on PE across 2≤ℓ≤61 exceeds the 95th percentile of the isotropic null on Planck2018 SMICA.", "direction": "increase" },
    { "id": "H2", "statement": "Alignment-entropy SX across 2≤ℓ≤61 is below the 5th percentile of the isotropic null on Planck2018 SMICA.", "direction": "decrease" },
    { "id": "H3", "statement": "Pairwise PT-PEV alignments among ℓ∈{1,2,3} depart from Uniform[0,1] (x=1−cosα) by a Kuiper test at p≤0.05 in WMAP9 ILC and Planck2018 SMICA.", "direction": "decrease" }
  ],
  "variables": {
    "independent": ["dataset_release", "lmin", "lmax", "n_sims", "mask_fsky"],
    "dependent": ["pval_global_PE", "pval_SX", "pval_Kuiper_alignments"],
    "controls": ["nside", "beam_fwhm_deg", "smoothing_kernel", "inpaint_method", "seed"]
  },
  "pass_fail": [
    { "metric": "pval_global_PE_Planck2018_SMICA", "operator": "<=", "threshold": 0.05, "unit": "probability" },
    { "metric": "pval_Kuiper_x_l123", "operator": "<=", "threshold": 0.05, "unit": "probability" },
    { "metric": "pval_SX_Planck2018_SMICA_[2,61]", "operator": "<=", "threshold": 0.05, "unit": "probability" }
  ],
  "spec_refs": [
    "Derivation/code/physics/cosmology_cmb_lowL_alignments/specs/pt_pe_ae_fullscan.0.1.0.json"
  ],
  "registration_timestamp": "<ISO-8601>"
}
```

### Specs

**Path:**
`Derivation/code/physics/cosmology_cmb_lowL_alignments/specs/pt_pe_ae_fullscan.0.1.0.json`

**Content (domain‑specific parameters included and validated against `cmb-pt.schema.json`):**

```json
{
  "run_name": "pt_pe_ae_fullscan",
  "version": "0.1.0",
  "tag": "cmb-pt-2025.10",
  "schema_ref": "Derivation/code/physics/cosmology_cmb_lowL_alignments/schemas/cmb-pt.schema.json",
  "parameters": {
    "datasets": [
      { "id": "WMAP9_ILC", "source": "LAMBDA" },
      { "id": "Planck2018_SMICA", "source": "PLA" }
    ],
    "lmin": 2,
    "lmax": 61,
    "n_sims": 2000,
    "nside": 512,
    "beam_fwhm_deg": 1.0,
    "smoothing_kernel": "gaussian",
    "mask": {
      "name": "WMAP9_Kp8_x_Planck2018_common_inpaint",
      "path": "Derivation/data/cmb_masks/wmap9_kp8_x_planck2018_common_inpaint_n512.fits",
      "f_sky": 0.929
    },
    "inpaint": {
      "enabled": true,
      "method": "ISAP",
      "config": {}
    },
    "stats": {
      "compute": ["PE", "AT_entropy", "pairwise_x", "Kuiper_x", "global_loglike_PE"],
      "pairwise_ells": [1, 2, 3]
    },
    "artifact_dir": "Derivation/artifacts/cosmology_cmb_lowL_alignments/pt_pe_ae_fullscan/0.1.0",
    "data_sources": {
      "LAMBDA": "https://lambda.gsfc.nasa.gov/product/wmap/current/",
      "PLA": "https://www.cosmos.esa.int/web/planck/pla"
    }
  },
  "seeds": [17, 23, 42, 86, 101]
}
```

> **Why these values?** The ℓ‑range, unified masking/inpainting flow, and reliance on ILC/SMICA products mirror the analysis choices validated across WMAP and Planck releases; the statistics computed (PE, AE, pairwise (x), Kuiper (V), and (\bar x)) are exactly those needed to test isotropy and alignment robustness as in the reference analysis.  

### Schemas

**Path:**
`Derivation/code/physics/cosmology_cmb_lowL_alignments/schemas/cmb-pt.schema.json`

**Minimum JSON Schema (draft 2020‑12) with domain‑specific validation for `parameters`:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://vdm.local/schemas/cmb-pt.schema.json",
  "title": "CMB Power-Tensor Alignment Experiment Parameters",
  "type": "object",
  "properties": {
    "datasets": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "enum": ["WMAP1_ILC", "WMAP3_ILC", "WMAP5_ILC", "WMAP7_ILC", "WMAP9_ILC", "Planck2013_PR1_ILC", "Planck2015_SMICA", "Planck2018_SMICA"] },
          "source": { "type": "string", "enum": ["LAMBDA", "PLA"] }
        },
        "required": ["id", "source"],
        "additionalProperties": false
      }
    },
    "lmin": { "type": "integer", "minimum": 2 },
    "lmax": { "type": "integer", "minimum": 3 },
    "n_sims": { "type": "integer", "minimum": 500 },
    "nside": { "type": "integer", "enum": [256, 512, 1024, 2048] },
    "beam_fwhm_deg": { "type": "number", "exclusiveMinimum": 0 },
    "smoothing_kernel": { "type": "string", "enum": ["gaussian"] },
    "mask": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "path": { "type": "string" },
        "f_sky": { "type": "number", "minimum": 0.0, "maximum": 1.0 }
      },
      "required": ["name", "path", "f_sky"],
      "additionalProperties": false
    },
    "inpaint": {
      "type": "object",
      "properties": {
        "enabled": { "type": "boolean" },
        "method": { "type": "string", "enum": ["ISAP"] },
        "config": { "type": "object" }
      },
      "required": ["enabled", "method"],
      "additionalProperties": false
    },
    "stats": {
      "type": "object",
      "properties": {
        "compute": {
          "type": "array",
          "items": { "type": "string", "enum": ["PE", "AT_entropy", "pairwise_x", "Kuiper_x", "global_loglike_PE"] },
          "minItems": 1
        },
        "pairwise_ells": {
          "type": "array",
          "items": { "type": "integer", "minimum": 1, "maximum": 10 },
          "minItems": 2
        }
      },
      "required": ["compute"],
      "additionalProperties": false
    },
    "artifact_dir": { "type": "string" },
    "data_sources": {
      "type": "object",
      "properties": {
        "LAMBDA": { "type": "string" },
        "PLA": { "type": "string" }
      },
      "required": ["LAMBDA", "PLA"],
      "additionalProperties": true
    }
  },
  "required": ["datasets", "lmin", "lmax", "n_sims", "nside", "beam_fwhm_deg", "smoothing_kernel", "mask", "inpaint", "stats", "artifact_dir", "data_sources"],
  "allOf": [
    { "if": { "properties": { "lmin": { "const": 2 } } }, "then": { "properties": { "lmax": { "minimum": 3 } } } }
  ],
  "additionalProperties": false
}
```

---

### Implementation notes (for the runner and reviewers)

* **Data sourcing:** The spec encodes authoritative sources for WMAP ILC (LAMBDA) and Planck SMICA (PLA) products; these are the exact releases used in the reference analysis. The runner must verify accessibility and checksums before simulation.  
* **Gates wiring:** Bind pass/fail evaluation to the three preregistered metrics in `PRE-REGISTRATION.json`. Emit a machine‑readable `passfail.json` alongside figures and CSV/JSON logs per RESULTS standards. 
* **Provenance:** Surface `commit`, salted hash, seeds, and resolved paths in every artifact filename or companion JSON to satisfy proposal/RESULTS provenance discipline.  

---

Conventions and structure follow the canonical template.  

---

## 6. **Research Questions, Hypotheses, and Preregistered Gates**

**RQ1 (Instrument validity):** Do the reproduced **(S(\ell))** curves and anomalous‑ℓ counts match the mission‑release‑specific simulations at Patel et al.’s levels?
**Gate G‑T2.1:** Recreate ℓ‑wise **95% CL** envelopes and mark **p≤0.05** anomalies for Planck PR3; Kuiper test p‑value ≤0.05 for the **x=1-\cos\alpha** distribution under the null. **PASS** if counts and global (\bar S) fall within ±1 simulated σ of reported values; **FAIL** otherwise.  

**RQ2 (Axis stability):** Is there a **single axis** (\hat f) explaining per‑ℓ PEVs jointly across releases?
**Gate G‑Axis.1:** Fitted (\hat f) from Planck PR3 vs WMAP‑9 **angular separation** ≤ **20°** (median‑over‑ℓ AT‑PEV comparison). **PASS/FAIL.**  

**RQ3 (Entropy deficit):** Does a nonzero (\epsilon) significantly improve the **global entropy likelihood**?
**Gate G‑LLH.1:** (\Delta\log\mathcal{L}(\epsilon,\hat f)-\Delta\log\mathcal{L}(0,\cdot)\ge 6) (≈2.4σ for 2 dof) on PR3; **bootstrap** over FFP sims for p‑value. **PASS/FAIL.**  

**RQ4 (Pipeline invariance):** Are (\hat f,\epsilon) stable across releases/pipelines?
**Gate G‑Robust.1:** Relative change (|\epsilon_{\rm PR3}-\epsilon_{\rm PR2}|/\bar\epsilon \le 0.3) **and** axis shifts ≤ **25°** when swapping masks (Kp8‑only vs unified) and changing smoothing (0.5°–1.5°). **PASS/FAIL.**  

**RQ5 (Branch selection):** Which (g_\ell) (A or B) best explains the data?
**Gate G‑Model.1:** Prefer **Branch A** if AIC difference ≥ 4; else prefer **Branch B**; else **indeterminate**.

**Kill‑plan:** Any **FAIL** on G‑T2.1 or simultaneous **FAIL** on G‑Axis.1 and G‑LLH.1 triggers **CONTRADICTION_REPORT.md** with residual diagnostics; VDM portal amplitude set to bound (|\epsilon|) (95% CI) and the branch rejected.

---

## 7. **Variables and Controls**

**Independent variables:** Mission/release (WMAP 1–9, Planck PR1/PR2/PR3), mask (Kp8, unified), smoothing (0.5°, 1.0°, 1.5°), ℓ‑range (2–61), FFP seed sets.

**Dependent variables:** (S(\ell)), (\bar S), AT entropy (S_X), AT‑PEV (\tilde f), fitted (\hat f,\epsilon), (\Delta\log\mathcal{L}).

**Controls:** Nside=512; ISAP inpainting; mission‑specific beams; Planck FFP noise/beam realizations; HEALPix conventions. (All per Patel et al.; see **pages 2–4** for definitions, simulation handling, and mask/inpainting details.)  

---

## 8. **Equipment / Hardware**

**Compute environment:** Modular monolith repo; **AMD** CPU/GPU stack (e.g., Ryzen/EPYC + ROCm HIP); Python/NumPy + healpy; no NVIDIA/CUDA dependency. Clean‑Architecture layering (presentation/application/domain/infrastructure) with ≤500 LOC/file, repository pattern, tests mirroring source.  

---

## 9. **Data Sources & Acquisition (exact sourcing)**

**Primary maps (temperature, full‑sky cleaned):**

* **WMAP WILC** (1, 3, 5, 7, 9‑year) from **NASA LAMBDA** (public).
* **Planck SMICA** **2015 (PR2)** and **2018 (PR3)** maps from **Planck Legacy Archive (PLA)** (public).
* **Planck 2013 (PR1)** derived ILC (as in Patel et al.) where official SMICA sims superseded; see their Appendix notes.

**Simulations & beams:**

* **Planck FFP SMICA simulations** for PR2/PR3 (PLA).
* WMAP frequency‑level simulations combined using published **ILC weights** per release for WILC mocks (as in Patel et al.).
* Mission beam windows per release, **downgraded to Nside=512**, **FWHM=1°** for uniformity.

**Mask & inpainting:**

* **Unified mask** = WMAP‑9 Kp8 ∪ Planck‑2018 common inpainting; **(f_{\rm sky}\approx0.929)**; **ISAP** inpainting applied consistently (see **Fig. 1, p. 3** and accompanying text).  

*Note:* All of the above choices and their **uniform application across releases** follow Patel, Aluri & Ralston (2025) to remove pipeline‑induced degrees of freedom.  

---

## 10. **Analysis Plan (estimation, uncertainty, and model comparison)**

1. **Instrument replication (T2):** Compute (S(\ell)) and anomaly flags with mission‑matched simulations; compute (\bar S) (their eq. 10‑style log‑sum) and Kuiper statistic on (x=1-\cos\alpha).  
2. **VDM fit:** Minimize negative log‑likelihood over ({\hat f,\epsilon}) using the eigenvalue spectra of (A_{ij}(\ell)) across ℓ (covariances from simulations), separately for **Branch A** and **B** (g_\ell).
3. **Uncertainty:** Bootstrap over **FFP** (Planck) and WMAP mock catalogs; report **bias‑corrected** CIs for (\epsilon), angular CIs for (\hat f).
4. **Model comparison:** (\Delta\log\mathcal{L}), AIC, **out‑of‑release** validation (fit on PR3, check on WMAP‑9 and PR2).
5. **Robustness sweeps:** Masks, smoothing, ℓ‑truncations (e.g., 2–45), and noise inflation to assess sensitivity.

Statistical controls and specification‑test discipline follow the **Rules for Data Science & Documentation** and **Objective Decision‑Making** (calibration, p‑values as continuous evidence, no double‑use of data for selection + inference).

---

## 11. **Gates to PROVEN / PLAUSIBLE / NEEDS_DATA**

* **PROVEN** (for the VDM single‑axis account) requires **PASS** on **G‑T2.1**, **G‑Axis.1**, **G‑LLH.1**, and **G‑Robust.1**, with branch preference by **G‑Model.1**.
* **PLAUSIBLE** if the axis is stable (G‑Axis.1 PASS) but (\Delta\log\mathcal{L}) gains are marginal (4–6) or robustness only partly passes.
* **NEEDS_DATA** if instrument replication passes but cross‑release stability is inconclusive.

---

## 12. **Risks, Assumptions, and Kill‑Methods**

**Assumptions:** Weak‑anisotropy regime ((|\epsilon|\ll1)); correct mission beams/noise; inpainting does not preferentially imprint axes; VDM portal acts as rank‑1 deformation at last scattering.

**Key risks & mitigations:**

* **Mask/inpainting bias:** Swap masks, inpainting kernels; verify with FFP.
* **Chance overfitting:** Cross‑release validation; **Branch A/B** comparison.
* **Systematic axes (ecliptic, dipole):** Post‑hoc angular comparisons reported as **exploratory** only; preregistered tests ignore them.

**Kill‑methods:** If **G‑T2.1** fails, stop: the meter is untrusted. If **both** **G‑Axis.1** and **G‑LLH.1** fail, file **CONTRADICTION_REPORT.md** and bound (|\epsilon|) at 95% CI (VDM portal rejected in this channel).

---

## 13. **Reproducibility & Artifacts**

* **CLI stubs:**

  * `vdm-cmb meter --release PR3 --mask unified --nside 512 --smooth 1.0deg`
  * `vdm-cmb fit --branch A --ells 2:61 --seeds 1000`
* **Outputs:** JSON for per‑ℓ (S(\ell)), PEVs, AT entropy, fitted (\hat f,\epsilon), CIs; figure PNGs with CSV under same basename; logs include seeds and commit.

Clean‑Architecture and repository structure per VDM’s Hybrid‑Clean guidelines (≤500 LOC/file; tests mirror source; dependency inversion).  

---

## 14. **Scope Boundaries**

* **In scope:** Temperature (T) maps only (as in the cited study); low‑ℓ (2\leq\ell\leq61); small‑anisotropy VDM prior.
* **Out of scope:** E‑mode extension (future T5); parameterized ΛCDM changes; non‑VDM anisotropy models; claims about ultimate cosmological **cause** (this is a phenomenological test).  

---

## 15. **References & Provenance**

* **Proposal template and authoring rules** (this document follows them): PROPOSAL_PAPER_TEMPLATE.md.  
* **CMB anomaly meter and data handling:** Patel, Aluri & Ralston (2025), *MNRAS 539:542–556*, esp. **eqs. (2), (5)–(10)**, **Fig. 1 p. 3** (mask (f_{\rm sky}\approx0.929)), and simulation/inpainting procedures.  
* **VDM canonical equations and axioms** (portal modulation E‑008; RD/EFT branches E‑014/E‑015/E‑031; scale program A6): VDM Canonical Equations & Procedural Math.  
* **VDM constants/symbols** (notation, mapping): VDM Constants & Defaults; VDM Notation Reference.  
* **Statistical practice & preregistration discipline:** Rules for Data Science & Documentation; Rules for Objective Decision‑Making and Truth‑Seeking.

---

## **Where to source the data (actionable list)**

1. **WMAP WILC maps (1, 3, 5, 7, 9‑year)** and masks/ILC weights — **NASA LAMBDA** archive (public). Use mission documentation to combine frequency‑level mocks with published weights per release (as in Patel et al.).  
2. **Planck SMICA maps (2015 PR2, 2018 PR3)** and **FFP SMICA simulations** — **Planck Legacy Archive (PLA)** (public). Use official FFP simulations corresponding to each release.  
3. **Unified temperature mask** = **WMAP‑9 Kp8** ∪ **Planck‑2018 common inpainting mask**, downgraded or upgraded to **Nside=512**, giving **(f_{\rm sky}\approx0.929)**; see **Fig. 1 p. 3** for the combined mask example and (f_{\rm sky}). Apply **ISAP** for inpainting in masked regions.  

---

### Closing note

This is a **single‑axis** theory test, not a fishing expedition. If a coherent (\hat f) and small but nonzero (\epsilon) survive preregistered gates across **independent mission pipelines**, VDM earns the right to a deeper cosmological seat at the table; if not, the constraint tightens and the theory learns. Next natural extensions include E‑mode polarization (same gates), which sharpens or scuttles the axis.
