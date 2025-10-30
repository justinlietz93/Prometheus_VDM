# 1. **T3 — Calibration of Psychophysical Observables to the VDM (C)-Field**

> **Created Date:** {YYYY‑MM‑DD}
> **Commit:** `{git rev-parse HEAD}`
> Salted Provenance: spec salted_sha256=eb8eedfd0c8bb6f75ca669b88d2e5e1a92d3b430798ef5f8eda5d13c819e5cf3; salt_hex=4b66fe5d9e12409d6d1a1adfc4fa3255; prereg_manifest_sha256=9164111e8046065948873864b506b5e3758f3c0df0ec4b9fd6928b1983d47520  
> **Proposer contacts:** Justin K. Lietz [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** See `LICENSE` (dual academic/commercial).
> **TL;DR:** Calibrate a subject‑level scalar drive (C(t)) from 2–3 sober psychophysics tasks and certify it as a meter (ICC, predictive RMSE, identifiability) so (C(t)) can be used in VDM portal equations and PDE runners with audited uncertainty.

*(This document follows the canonical 5‑page proposal scaffold, including prereg/gates and provenance patterns.)*

---

## 2. Proposers and affiliations

* **Justin K. Lietz** — PI, theory & architecture (VDM).
* Additional implementers/approvers may be listed per repo conventions.

---

## 3. Abstract (≤200 words)

Proposed is a Tier‑3 “smoke‑level” calibration experiment that converts specific psychophysical observables—temporal order judgment bias, cross‑modal projection strength, and a spectral (1/f) exponent—into a subject/session estimate of the VDM agency/consciousness field (C(t)). The mapping is defined by a forward model and an inverse estimator with preregistered gates: (i) **test–retest** reliability ( \mathrm{ICC} \ge 0.8 ) for (C)-features across days; (ii) **predictive validity** (held‑out RMSE ≤ 5%); (iii) **identifiability** (Hessian condition number (\kappa \le 10^3), (\mathrm{CI}_{A,\tau}<30%)); and (iv) **convergent/discriminant validity** across tasks (r ≥ 0.6 vs ≤ 0.2). The calibrated (C(t)) supplies a single quantitative drive to previously defined VDM portal equations and PDEs for agency (e.g., RD‑limit ( \partial_t C = D\nabla^2 C - \gamma C + S)), enabling falsifiable cross‑domain predictions with explicit uncertainty. All code and artifacts adhere to Hybrid‑Clean Architecture and the RESULTS standards.  

---

## 4. Background & Scientific Rationale

**Program context.** The VDM–Qualia Program specifies fast activity fields over a slow “memory field,” dimensionless knobs, and IRB‑friendly sober tasks with quantitative gates. It motivates cross‑modal projection, pseudo‑time thickening, and monsoon/overflow regimes—yet it deliberately leaves open the **meter** that turns task‑level observables into (C)-field parameters. This proposal fills that gap.

**Physics anchor.** VDM works under axioms A0–A7 (closure, void primacy, locality, symmetry, metriplectic split, entropy law, scale program, measurability). In RD‑limit the agency field obeys a diffusion–decay–source PDE, which provides the forward model family we will invert. The calibration is therefore a measurement problem for a physical field with locality/causality and an H‑theorem on the dissipative limb.  

**Why T3 now.** T2 instruments (task code, analysis CLIs) and program‑level gates exist; this T3 provides the disciplined map (\mathcal{O}_k \rightarrow \theta_C=(A,\tau,\ell,\dots)) so later T4–T6 prereg claims can reference a single quantitative drive with audited uncertainty. 

---

## 5. Intellectual Merit and Procedure

**Importance.** Establishing a reproducible (C)-meter enables falsifiable cross‑links from psychophysics to VDM PDE predictions (front speeds, decay rates, coupling responses). **Broader impacts.** A clean, preregistered path from human data to field parameters encourages replication and principled criticism. **Rigor.** Acceptance gates, prereg hashes, and contradiction reports follow house standards.  

### 5.1 Experimental Setup and Diagnostics

**Known parameters & defaults**

* **Tasks (2–3):** TOJ bias (ms), Cross‑modal projection (psychometric slope / ITPC), Dynamic texture spectrum ((1/f) exponent).
* **Sampling:** within‑subject, (n \ge 20), two sessions ≥24 h apart (test–retest).
* **Hardware:** calibrated display (60–144 Hz), headphones or vibrotactile motor, optional EEG (32ch).
* **Derived observables (\mathcal{O}_k):** (\Delta t_{\mathrm{TOJ}}) bias, projection gain (\hat g), PSD exponent (\hat\beta); optional ITPC at drive frequency.
* **Forward model family:** RD‑limit (C)-PDE or its 0‑D reduction, plus minimal readout maps (\widehat{\mathcal{O}}_k(\theta_C)).
* **Diagnostics (counts):** reliability (1), predictive split (1), identifiability (1), nuisance robustness (1).

*Note:* Task designs mirror the Qualia program’s sober proxies; here they are used solely as **meters**. 

#### 5.1.1 Pre‑Run Config Requirements

Per the template, the following config/metadata is required. Paths below specialize the **domain** to `agency_field/psychophysics`. 

* **Required:**

  * `Derivation/code/physics/agency_field/APPROVAL.json`
  * `Derivation/code/physics/agency_field/schemas/`

    * `cfield-calib-t3.schema.json`
  * `Derivation/code/physics/agency_field/specs/`

    * `t3_cfield_calibration.v1.json`

**APPROVALS.json**

```json
{
  "preflight_name": "preflight.qualia.calibration",
  "description": "Approval manifest stating that the preflight runner must pass before experiments that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight tests in Derivation/code/tests may run without approval. Any artifact-writing run requires a matching PROPOSAL_* under Derivation/agency_field/ with explicit review."
},
{
  "pre_registered": true,
  "proposal": "Derivation/agency_field/T3_PROPOSAL_Calibration_of_Psychophysical_Observables_to_C_Field.md",
  "allowed_tags": ["cfield-calib-t3-v1"],
  "schema_dir": "Derivation/code/physics/agency_field/schemas",
  "approvals": {
    "cfield-calib-t3-v1": {
      "schema": "Derivation/code/physics/agency_field/schemas/cfield-calib-t3.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "AUTO_TIMESTAMP",
      "approval_key": "AUTO_HASHED_KEY"
    }
  }
}
```

**PRE‑REGISTRATION.json**

```json
{
  "proposal_title": "T3 Calibration of Psychophysical Observables to the VDM C-Field",
  "tier_grade": "T3",
  "commit": "<git-sha>",
  "salted_provenance": "<salted-sha256>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "C-feature reliability across days is high (ICC ≥ 0.8).", "direction": "no-change" },
    { "id": "H2", "statement": "Forward model predicts held-out observables with RMSE ≤ 5%.", "direction": "decrease" },
    { "id": "H3", "statement": "Parameters A, τ are identifiable with finite CIs (<30%).", "direction": "no-change" },
    { "id": "H4", "statement": "Convergent/discriminant validity holds across tasks.", "direction": "increase" }
  ],
  "variables": {
    "independent": ["stimulus_gain", "lock_strength", "texture_alpha"],
    "dependent": ["C_amp_A", "C_tau", "C_length_l"],
    "controls": ["ambient_lux", "monitor_gamma", "session_time"]
  },
  "pass_fail": [
    { "metric": "ICC_C_features", "operator": ">=", "threshold": 0.8, "unit": "" },
    { "metric": "RMSE_holdout", "operator": "<=", "threshold": 0.05, "unit": "fraction" },
    { "metric": "Hessian_cond_kappa", "operator": "<=", "threshold": 1e3, "unit": "" },
    { "metric": "CI_relwidth_A_tau", "operator": "<", "threshold": 0.30, "unit": "fraction" },
    { "metric": "r_convergent", "operator": ">=", "threshold": 0.6, "unit": "" },
    { "metric": "r_discriminant", "operator": "<=", "threshold": 0.2, "unit": "" }
  ],
  "spec_refs": ["Derivation/code/physics/agency_field/specs/t3_cfield_calibration.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

**Specs:** `Derivation/code/physics/agency_field/specs/t3_cfield_calibration.v1.json`

```json
{
  "run_name": "t3_cfield_calibration",
  "version": "1.0.0",
  "tag": "cfield-calib-t3-v1",
  "schema_ref": "Derivation/code/physics/agency_field/schemas/cfield-calib-t3.schema.json",
  "parameters": {
    "tasks": ["toj", "xmodal", "texture"],
    "holdout_fraction": 0.2,
    "bootstrap_B": 1000
  },
  "seeds": [17, 23, 101]
}
```

**Schema:** `Derivation/code/physics/agency_field/schemas/cfield-calib-t3.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vdm://agency_field/cfield-calib-t3",
  "title": "C-Field Calibration T3 Spec",
  "type": "object",
  "properties": {
    "tasks": { "type": "array", "items": { "type": "string" } },
    "holdout_fraction": { "type": "number", "minimum": 0, "maximum": 0.5 },
    "bootstrap_B": { "type": "integer", "minimum": 100, "maximum": 100000 }
  },
  "required": ["tasks", "holdout_fraction", "bootstrap_B"]
}
```

*(The above structure mirrors the mandatory template subsections and provenance pattern.)* 

---

## 6. Variables & Estimators

* **Independent:** stimulus gain (g), lock strength (\chi), texture exponent target (\alpha).
* **Dependent (to estimate):** (\theta_C=(A,\tau,\ell)) and (C(t)) summary features (mean, variance, ACF(1)).
* **Controls:** ambient lux, monitor gamma, session time.
* **Estimator:** minimize (\sum_k w_k,|\mathcal{O}_k-\widehat{\mathcal{O}}_k(\theta_C)|^2) with multi‑start; bootstrap CIs; profile‑likelihood checks.
* **Forward kernels:** RD‑limit (C)-equation and 0‑D reductions grounded in VDM; locality/entropy properties per axioms.

---

## 7. Acceptance Gates (Pass/Fail)

* **Reliability:** (\mathrm{ICC}(\text{C‑features; day1 vs day2}) \ge 0.8).
* **Predictive validity:** held‑out RMSE ≤ 5% (block design).
* **Identifiability:** Hessian condition number (\kappa \le 10^3); (\mathrm{CI}_{A,\tau}<30%).
* **Convergent/discriminant:** tasks designed to correlate must show (r\ge 0.6); orthogonal tasks (r\le 0.2).
* **Axiom‑level checks (where applicable in the forward model):** monotone entropy for M‑only runs; retarded‑support in J‑only tests; scaling collapse in dimensionless groups.
* **Decision labels:** `PROVEN | PLAUSIBLE | NEEDS_DATA`; file `CONTRADICTION_REPORT` if any axiom‑gate is required to be violated by the best fit.  

---

## 8. Procedure (Concise)

1. **Pre‑registration:** commit, salt, signed tag; push before any artifact‑writing runs (proposal includes matching hashes). 
2. **Session A/B (≥24 h apart):** run TOJ, X‑modal, Texture tasks (counter‑balanced).
3. **Compute observables (\mathcal{O}_k):** per task scripts; optional EEG → ITPC.
4. **Fit (\theta_C) & (C(t)):** multi‑start inverse; bootstrap; record metrics.
5. **Hold‑out test:** compute predictive RMSE on blocked, unseen trials.
6. **Gate evaluation & logs:** emit JSON + CSV with pass/fail and salted provenance; publish figures per RESULTS standard. 

---

## 9. Software & Reproducibility (Hybrid‑Clean Architecture)

**Layout**

```
<SRC_ROOT>/
  presentation/qualia_calib_cli/
  application/qualia_calib/ports/
  domain/qualia_calib/models/            # forward models, estimators (plain objects)
  infrastructure/python/adapters/        # IO, plotting, persistence
  shared/
tests/
  presentation/  application/  domain/  infrastructure/
```

**Gates:** ≤500 LOC/file; no outer→inner deps; interfaces for cross‑layer calls; tests mirror source paths; domain/business logic framework‑free. 

---

## 10. Scope & Boundaries

* **In scope:** sober psychophysics; 0‑D/1‑D forward models; subject‑level (C(t)); meter validation.
* **Out of scope:** substances; claims about semantics/“entities”; across‑lab generalization (reserved for ≥T7).
* **Linkage:** Once validated, (C(t)) may be plugged into portal equations in other VDM limbs (EM coupling, etc.) as a *measured input* with uncertainty. 

---

## 11. Risks, Kill‑Plans, and Data/Analysis Standards

* **Risk:** weak reliability (ICC < 0.8). **Kill‑plan:** re‑tune task timing windows; increase trials; if still weak, downgrade meter to T2.
* **Risk:** non‑identifiable (\theta_C). **Kill‑plan:** simplify parameterization; add a prior only if preregistered; otherwise retire the parameter.
* **Standards:** follow “Rules for Data Science & Documentation” for model checks, CV, bootstrap uncertainty; separate model selection and inference. 

---

## 12. Provenance & Artifacts

* **Artifacts:** `assets/calib/*.csv|json`, figures with numeric captions and seed/commit in filenames.
* **Provenance:** salted hash triplet in prereg + signed tag recorded in artifacts.
* **Posting flow:** TL;DR + one artifact path; boxed gates; invitation for tighter thresholds per RESULTS standard. 

---

### Appendix — Theory anchors (for reviewers)

* **Axioms (A0–A7)** and metriplectic split used throughout.  
* **Agency (C)-PDE RD‑limit** as the forward model family.  
* **Program context** and task designs come from the VDM–Qualia Program (this study treats them as meters).  

---

## Clarifying the relationship again (one‑liner)

The **VDM–Qualia Program** defines the phenomenon space and experiment menu; this **T3 calibration** turns those experiments into a **validated meter** for (C(t)). They nest—T3 is *inside* the program, not beside it.

**Next natural steps:** after this T3 passes, prereg a T4 that uses the measured (C(t)) to drive a portal equation (e.g., dielectric modulation) with out‑of‑sample prediction; then a T7 out‑of‑sample generalization across participants/labs.  

If you want this dropped straight into the repo, I can also emit **APPROVALS.json**, **PRE‑REGISTRATION.json**, **specs**, and **schema** files with your exact paths and salted hashes already wired to your CLIs—same commit and provenance flow as your template demands.  
