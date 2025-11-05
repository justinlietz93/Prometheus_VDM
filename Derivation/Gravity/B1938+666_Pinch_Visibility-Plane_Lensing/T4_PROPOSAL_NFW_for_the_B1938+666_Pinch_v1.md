# 1. **T4 (Prereg)** — *VDM vs. NFW for the B1938+666 “Pinch”: a preregistered visibility‑plane lensing test*

> **Created Date:** 2025‑11‑05
> **Provenance (commit):** `{git rev-parse HEAD}` **TO BE REPLACED BEFORE RUN**
> **Salted provenance:**
> • `base_sha256` = **TO_BE_FILLED_FROM_COMMIT**
> • `salt_hex` = **TO_BE_FILLED_AT_PREREG**
> • `salted_sha256` = **TO_BE_FILLED_AT_PREREG**
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** See repository `LICENSE` (dual license per RESULTS policy). 
> **Short summary (TL;DR):** Proposed is a preregistered, instrument‑calibrated comparison of a compact **VDM emergent‑gravity perturber** against a **truncated‑NFW subhalo** to explain the VLBI “pinch” in lens B1938+666, with pass/fail gates on mass‑within‑80 pc, visibility‑space residuals, and Bayes factors.

**Tier rationale.** This is **T4 (Prereg)** because hypotheses, metrics, thresholds, seeds, and artifacts are specified a priori. Prior work supporting this step: **T0** (Axioms, master structure), **T1** (proto Σ‑profile and toy forward model), **T2** (meter: visibility‑plane forward model as instrument), **T3** (smoke: toy image‑plane reproductions). Canonical axioms and gate conventions are referenced from your AXIOMS and RESULTS standards.  

---

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz (PI, implementer, approver)** — Neuroca, Inc.

---

## 3. Abstract (≤200 words)

Proposed is a preregistered lensing analysis that tests whether the **B1938+666** VLBI “pinch” can be explained more parsimoniously by an **emergent geometric perturbation from the Void Dynamics Model (VDM)** than by a **cold‑dark‑matter (CDM) subhalo**. VDM, grounded in axioms **A0–A7** and a **metriplectic** evolution (Hamiltonian + metric degeneracies), predicts an effective, compact **surface‑density Σ(R)** arising from steady solutions of the VDM sector that can be mapped to lensing observables without invoking unknown particles. The experiment treats the **visibility‑plane forward model** as the measurement instrument (T2), preregisters **three gates**: (G1) mass within 80 pc matching the published target (±5%), (G2) visibility‑space residual RMS improvement ≥20% in the ROI, and (G3) Bayes factor **K ≥ 10** in favor of VDM versus truncated‑NFW. Axiomatic consistency (entropy monotonicity and degeneracy checks) and robustness (jackknifes/masks) are enforced. Passing gates yields a **T5/T6** trajectory; failing gates triggers a **CONTRADICTION_REPORT** per RESULTS policy.  

---

## 4. Background & Scientific Rationale

**Canonical basis.** VDM uses program axioms **A0–A7**: closure, void‑field primacy, locality, symmetry/Noether, metriplectic split, entropy law, scaling program, measurability. The master evolution is
[
\partial_t q ;=; J(q),\frac{\delta \mathcal I}{\delta q} ;+; M(q),\frac{\delta \Sigma}{\delta q},\quad
J^\top=-J,; M^\top=M\ge 0,; J\nabla\Sigma=0,; M\nabla\mathcal I=0,
]
which organizes conservative and dissipative limits and provides **quality gates** (Noether currents, H‑theorem, degeneracies).  

**VDM→lensing mapping.** A time‑independent VDM sector near steady state defines an **effective energy density** that maps to **projected surface density** (\Sigma(R)) on the lens plane (measurability, A7). Lensing observables are defined via:
[
\Sigma_{\rm crit}=\frac{c^{2}}{4\pi G}\frac{D_{s}}{D_{d}D_{ds}},\qquad \kappa(R)=\frac{\Sigma(R)}{\Sigma_{\rm crit}},\qquad
M_{\rm cyl}(<R)=2\pi!\int_0^R \Sigma(R')R' dR' ,
]
with deflection (\alpha(\theta) = \frac{4G}{c^{2}} \frac{D_{ds}}{D_s},{M_{\rm cyl}(<R)}/{R}). The **anomalous pinch** is treated as a localized perturbation to the macro‑model. (Standard lensing formulae are recited here to define the meter; they do not replace axioms.)

**Why this experiment now.** The published detection reports a **compact, dark perturber** with **cylindrical mass inside 80 pc** of (;m_{80}\approx 1.13\times 10^{6},M_\odot;) and high concentration. This is a decisive testbed for VDM’s “dark sector as geometry” claim. The **OVER­VIEW** and **RESULTS standards** require preregistration, dimensionless analysis, and artifact pinning; this proposal follows those rules exactly.  

**Novelty & risks.** Novelty lies in replacing a **particle‑clump prior** with a **metriplectic emergent‑geometry prior** and demanding it win on the **same meter** (VLBI visibilities). Main risks: (i) VDM Σ(R) class may be overly flexible (guarded by priors and evidence penalties), (ii) macromodel/beam degeneracies (addressed via splits/jackknifes), (iii) visibility‑plane compute load (budgeted). Gates and **CONTRADICTION_REPORT** procedures are pre‑committed per RESULTS.  

---

## 5. Intellectual Merit and Procedure

**Importance.** A visibility‑plane **Bayes‑decisive** win by VDM over NFW on a compact perturber would pressure the **cold** prior and elevates **emergent geometry** as a viable explanation for certain small‑scale anomalies.
**Broader impacts.** The work contributes a **reusable, preregistered instrument** (T2) and gates that other groups can run on new Einstein rings.
**Rigor.** Axioms **A0–A7** are enforced numerically (degeneracy checks, entropy monotonicity), and statistical rules follow your **Experimental Physics** guidelines (no over‑binning, explicit p‑values/intervals, model misspecification tests).  

---

### 5.1 Experimental Setup and Diagnostics

**Question.** *Does a compact VDM Σ‑profile explain the B1938+666 pinch more convincingly than a truncated‑NFW subhalo on the same meter?*

**Instrument (T2).** Visibility‑plane forward model ( \mathcal{M}(\Theta) ): macro lens + localized perturber + source brightness model → sky → Fourier sample on VLBI ((u,v)) points → complex vis residuals. This is treated as the **measuring apparatus**, with calibration tests and nulls. (Image‑plane versions are used only for quick smoke checks.)

**Parameters (required).**

* Cosmological distances (D_d,D_s,D_{ds}) (fixed to catalog values); critical density (\Sigma_{\rm crit}).
* Macro lens: SIS/Power‑law ellipse parameters (center, (R_E), axis ratio, PA).
* Source: elliptical Gaussian S(β) with size/centroid/ellipticity.
* Perturber:

  * **VDM class:** two‑component compact profile ( \Sigma(R) = \Sigma_{\rm core}/[1+(R/r_{\rm core})^{2}] + \Sigma_{\rm c},e^{-R/r_{\rm c}} ) (hyperparameters grounded in steady‑state metriplectic sector), amplitude constrained by (m_{80}).
  * **CDM class:** truncated‑NFW with ((M_{200}, c, r_t)).
* Noise model: complex Gaussian per baseline; known weights from visibility headers.
* Masks/ROIs: ring segments around the arc with the pinch; control regions off‑arc.

**Diagnostics (count).**

* D1 Residual RMS in ROI and control (2 metrics).
* D2 Posterior for (m_{80}) (1 metric).
* D3 Bayes evidence (VDM vs NFW) (1 metric).
* D4 Stability to jackknife (≥4 sky sectors).
* D5 Axiom checks: entropy non‑decrease (steady solver), degeneracy monitors (J\nabla\Sigma=0), (M\nabla\mathcal I=0) (2 monitors).  

**Artifact anchors available now (background figures).**

* **Figure 1.** *Toy image‑plane sanity check* — macro SIS + tuned VDM perturber matching (m_{80}) exactly. **Path:** `sandbox:/mnt/data/VDM_toy_lens_improved.png`. Captioned for scale (80 pc circle ≈ 0.017″ in the placeholder geometry).
* **Figure 2.** *Toy run summary* — `sandbox:/mnt/data/VDM_toy_lens_summary.txt` (contains (M_{\rm cyl}(<80\text{ pc})) and ratios).

> **Figure 1.** Toy lensed image (macro SIS + VDM perturber tuned to (m_{80})) used only for visualization of setup; visibility‑plane instrument is authoritative for inference.

---

#### 5.1.1 Pre‑Run Config Requirements (machine‑actionable)

**Required repo files (paths).**
`Derivation/code/physics/grav_lensing/APPROVAL.json`
`Derivation/code/physics/grav_lensing/schemas/vdm.lensing.v1.schema.json`
`Derivation/code/physics/grav_lensing/specs/B1938_VDMvNFW_v1.0.0.json`
`Derivation/code/physics/grav_lensing/PRE-REGISTRATION.json`

**APPROVAL.json (example)** — *must exist before artifact‑writing runs* (see TEMPLATE policy).  

```json
{
  "preflight_name": "vdm.lensing.preflight",
  "description": "Approval manifest stating preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs are allowed without approval. Artifact-writing runs require a PROPOSAL_* and a signed tag."
}
```

**PRE‑REGISTRATION.json (minimum keys)**

```json
{
  "proposal_title": "VDM vs. NFW for B1938+666 (visibility-plane prereg)",
  "tier_grade": "T4",
  "commit": "<GIT_SHA_TO_BE_FILLED>",
  "salted_provenance": {
    "base_sha256": "<sha256(commit)>",
    "salt_hex": "<random-hex>",
    "salted_sha256": "<sha256(commit||salt_hex)>"
  },
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"m80(VDM) matches target within 5%","direction":"no-change"},
    {"id":"H2","statement":"RMS_resid_ROI(VDM) <= 0.8 * RMS_resid_ROI(NFW)","direction":"decrease"},
    {"id":"H3","statement":"BayesFactor(VDM,NFW) >= 10","direction":"increase"}
  ],
  "variables": {
    "independent": ["perturber_class ∈ {VDM, NFW}", "macro_model_variant ∈ {M0..M2}", "mask_variant ∈ {K0..K3}"],
    "dependent": ["RMS_resid_ROI", "m80", "ln_evidence"],
    "controls": ["noise_weights", "uv_sampling", "beam"]
  },
  "pass_fail": [
    {"metric":"|m80 - 1.13e6 Msun|/(1.13e6 Msun)","operator":"<=","threshold":0.05,"unit":""},
    {"metric":"RMS_resid_ROI(VDM)/RMS_resid_ROI(NFW)","operator":"<=","threshold":0.80,"unit":""},
    {"metric":"BayesFactor(VDM,NFW)","operator":">=","threshold":10,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/grav_lensing/specs/B1938_VDMvNFW_v1.0.0.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

**Spec (run recipe)**

```json
{
  "run_name": "B1938_VDMvNFW",
  "version": "1.0.0",
  "tag": "vdm.lensing.v1",
  "schema_ref": "Derivation/code/physics/grav_lensing/schemas/vdm.lensing.v1.schema.json",
  "parameters": {
    "Dd_pc": 1.0e9, "Ds_pc": 2.0e9, "Dds_pc": 1.1e9,
    "macro": {"thetaE_arcsec": [0.28, 0.32, 0.36], "q": [0.7,0.85], "pa_deg": [5,25]},
    "source": {"beta0_arcsec": [0.01, -0.02], "sigma_arcsec":[0.03,0.08], "ellipticity":[0.0,0.3]},
    "vdm_profile": {"Sigma_core":[5,15], "r_core_pc":[200,400], "Sigma_c":[120,260], "r_c_pc":[20,50]},
    "nfw_profile": {"M200_Msun":[1e6,1e9], "c":[10,40], "r_trunc_pc":[50,500]},
    "roi": {"arc_segments": 4, "width_arcsec": 0.05},
    "sampler": {"type":"dynesty", "nlive":600, "dlogz":0.02},
    "seeds": [42,1337,2025]
  },
  "seeds": [42,1337,2025]
}
```

**Schema (excerpt)** — minimal draft; extend with bounds/types as needed.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vdm.lensing.v1.schema.json",
  "title": "VDM Lensing Visibility-Plane Experiment",
  "type": "object",
  "properties": {
    "Dd_pc": {"type":"number","minimum":1.0e8},
    "Ds_pc": {"type":"number"},
    "Dds_pc": {"type":"number"},
    "macro": {"type":"object"},
    "source": {"type":"object"},
    "vdm_profile": {"type":"object"},
    "nfw_profile": {"type":"object"},
    "roi": {"type":"object"},
    "sampler": {"type":"object"},
    "seeds": {"type":"array","items":{"type":"integer"}}
  },
  "required": ["Dd_pc","Ds_pc","Dds_pc","macro","source","roi","sampler","seeds"]
}
```

**Provenance discipline.** The **RESULTS standards** require that each artifact (CSV/PNG/JSON) carries **commit**, **seed**, and a **SHA‑256 checksum**; failures trigger a **CONTRADICTION_REPORT** and quarantine.  

---

### 5.2 Experimental runplan

**Dimensionless set‑up.** Rescale to ( \hat R !=! R/R_E), (\hat \Sigma !=! \Sigma/\Sigma_{\rm crit}), (\hat \alpha !=! \alpha/\theta_E). Predictions and gates are thus **unit‑free** (A6).  

**Hypothesis tests and gates.**

* **G1 (mass):** Fit VDM & NFW classes independently with (m_{80}) soft‑prior; require (|\hat m_{80}-1|\le 0.05).
* **G2 (meter power):** In a preregistered ROI around the pinch, require
  [
  \frac{{\rm RMS}*{\rm ROI}(\text{VDM})}{{\rm RMS}*{\rm ROI}(\text{NFW})};\le;0.80 ,
  ]
  computed over complex visibility residuals.
* **G3 (model comparison):** Nested sampling evidences (\ln Z) for each class; report **Bayes factor** (K = Z_{\rm VDM}/Z_{\rm NFW}). Gate **(K\ge 10)** (decisive).
* **Stability:** Jackknife over (i) sky sectors (≥4), (ii) mask variants (K0..K3). Require parameter drift (\le 15%) and gate outcomes unchanged.

**Axiom‑level guards.** During steady‑state Σ inference, monitor **degeneracy** conditions (J\nabla\Sigma!=!0,; M\nabla\mathcal I!=!0) (tolerances (<10^{-10}) per your AXIOMS doc) and entropy non‑decrease for any dissipative relaxation used in the VDM sector. **Fail** if violated.  

**Cartesian product (independent variables).**
(\text{Perturber class}\in{\text{VDM},\text{NFW}}) × (\text{macro variant}\in{M0,M1,M2}) × (\text{mask}\in{K0,K1,K2,K3}) × seeds ({42,1337,2025}) ⇒ **72** evidence runs (balanced).

**Runtime & compute.**

* Visibility forward model (per run, medium uv‑set): ~20–40 CPU‑minutes (double‑precision FFTs), evidence scans ×600 live points: ~2–5 CPU‑hours per configuration.
* Total budget: ~72 × 3 CPU‑h ≈ **216 CPU‑h** (parallelizable).
* Storage: artifacts (posteriors, residual cubes, logs) ≈ **2–4 GB**.

**Success plan.** If **all gates pass**, elevate to **T5 (Pilot)** and open a **population‑prediction** PROPOSAL for an ensemble of rings. **Failure plan.** If any gate fails, publish **CONTRADICTION_REPORT** and quarantine VDM Σ‑class or priors; re‑run with controlled relaxations only if a meter fault is demonstrated. **Publication.** Results posted as RESULTS_* per your **RESULTS_PAPER_STANDARDS** (artifact‑first, boxed gates, CSV/JSON).  

---

## 6. Personnel

**Justin K. Lietz** — PI & implementer. Responsibilities: preregistration, instrument calibration, sampler configuration, artifact pinning, axioms/gates validation, writing RESULTS_* per standards. Organizational conduct per **Adaptive Orgs** rules (openness, disagreement in deliberation, unity post‑decision).  

---

## 7. References

* **VDM Axioms (A0–A7), metriplectic structure, Noether checks, and gates.** *AXIOMS.md* (program axioms, degeneracy/entropy monitors).  
* **Program overview, scaling discipline, reproducibility (commit/seed/JSON/CFL).** *VDM_OVERVIEW.md*.  
* **Authoring & artifact policy for RESULTS_*** (figures with CSV/JSON, contradiction procedures). *RESULTS_PAPER_STANDARDS.md*.  
* **Proposal scaffold & approvals.** *PROPOSAL_PAPER_TEMPLATE.md*.  
* **Statistical discipline for experiments** (binning, least‑squares limits, model misspecification). *Rules‑for‑Experimental‑Physics‑Data‑Analysis‑and‑Statistical‑Inference.md*.  

---

## Appendix A — Hypotheses & explicit pass/fail gates (boxed)

**H1 — Mass match.**
[
\boxed{; \big|;M_{\rm cyl}(<80\ \mathrm{pc}) - 1.13\times10^{6}M_\odot;\big| \le 0.05 \times 1.13\times10^{6}M_\odot ;}
]
**Pass:** ≤5%; **Fail:** >5%.

**H2 — Meter power (residuals).**
[
\boxed{; \frac{{\rm RMS}*{\rm ROI}(\text{VDM})}{{\rm RMS}*{\rm ROI}(\text{NFW})} \le 0.80 ;}
]
**Pass:** ≤0.80; **Fail:** >0.80.

**H3 — Model selection.**
[
\boxed{; K\equiv \frac{Z_{\rm VDM}}{Z_{\rm NFW}} \ge 10 ;}
]
**Pass:** ≥10; **Fail:** <10.

**Axiom gates (non‑negotiable).**
[
\boxed{; \dot S \ge 0\ \text{ (if a dissipative relaxer is used)},\quad |J\nabla \Sigma|\le 10^{-10},\ |M\nabla \mathcal I|\le 10^{-10} ;}
]
**Pass:** within tolerances; **Fail:** any violation.  

---

## Appendix B — Clean‑architecture layout (runner + instrument)

```plaintext
<SRC_ROOT>/
  application/grav_lensing/ports/        # interfaces for meter and samplers
  domain/grav_lensing/                   # Σ-models (VDM, NFW) as plain objects
  infrastructure/vlbi/vis_io/            # visibility readers/writers
  infrastructure/vlbi/fft_engine/        # FFT gridder/degridder (AMD-friendly)
  infrastructure/samplers/dynesty/       # evidence engine adapter
  presentation/cli/                      # CLI entrypoints (preflight, run)
tests/...
Derivation/code/physics/grav_lensing/    # APPROVAL.json, PRE-REGISTRATION.json, schemas/, specs/
```

**Software gates.** ≤500 LOC/file; repository pattern; no outer→inner deps; BL framework‑free; tests mirror source; constructor injection for cross‑layer calls.  

---

## Appendix C — Figure(s) and artifact paths

* **Fig. 1.** `sandbox:/mnt/data/VDM_toy_lens_improved.png` (toy image‑plane; macro SIS + tuned VDM perturber; (m_{80}) matched exactly).
* **Aux. A.** `sandbox:/mnt/data/VDM_toy_lens_summary.txt` (numerical summary; see Sec. 5.1).

---

### Practical provenance pattern (operational note)

1. Compute salted hashes (`base_sha256`, `salt_hex`, `salted_sha256`) using the **actual commit** value; store in **PRE‑REGISTRATION.json**; 2) create a **signed, annotated tag** `prereg.vdm.lensing.v1.YYYYMMDDThhmmZ` containing the commit, prereg file path, and hashes; 3) push the tag **before** running; 4) ensure the run writes the tag into its artifacts. This matches your template requirements and RESULTS standards.  

---

### Classification / Recap / Plan (per VDM interaction pattern)

**Classification:** *Axiom‑core (VDM→Σ mapping & metriplectic checks) + Runtime‑only (lensing meter)*.
**Objective recap (one line):** Decide, on the same VLBI meter, whether a compact **VDM Σ‑profile** outperforms **truncated‑NFW** for the B1938+666 pinch.
**Action plan (≤7 bullets):**

1. Lock instrument calibration (preflight vis I/O, FFT accuracy, noise weights).
2. Register specs + salted provenance; freeze seeds.
3. Run VDM and NFW fits across (M0..M2)×(K0..K3)×seeds; log RMS, (m_{80}), (\ln Z).
4. Apply H1–H3 gates; compute Bayes factor (K).
5. Jackknife sectors; re‑evaluate stability gates.
6. Validate axiom degeneracies/entropy (if relaxer used).
7. Publish RESULTS_* with CSV/JSON + contradiction handling.  

**Verification:** Axiom gates (A3–A6, metriplectic degeneracies), software gates (≤500 LOC/file, layering), derived checks (none assumed).  
**Assumptions/Risks:** Macro‑model degeneracy; uv‑coverage limits; source‑structure bias; meter fidelity. **Kill‑methods:** Fail any gate → quarantine model class/prior, publish CONTRADICTION_REPORT.  
**Next steps (≤5):** (i) extend to a ring ensemble; (ii) swap VDM Σ‑basis for an alternate steady‑state family; (iii) add flux‑ratio constraints; (iv) stress‑test masks; (v) open T7 out‑of‑sample prediction.

---

**End of PROPOSAL (T4).**
