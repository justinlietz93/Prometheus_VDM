# **T2 — Discrete‑Scale Invariance Ringdown Meter (DSI‑RDM)**

**Tier Grade:** T2 (Instrument)
**Short title:** Fractal‑proxy diagnostics in black‑hole ringdown
**Created:** 2025‑11‑15 • **Commit:** *(pin at run time)* • **Salted provenance:** *(pin at run time)*
**Proposer:** Justin K. Lietz (PI, implementer, approver) • <[justin@neuroca.ai](mailto:justin@neuroca.ai)>
**License:** See LICENSE in repo
**TL;DR:** Proposed is a meter that mass‑normalizes ringdown data and tests for **discrete‑scale invariance** via log‑time spectral combs, wavelet‑ridge ratios, and cross‑event **scaling collapse**, with rigorous pass/fail gates and nulls. If the interior organizes in a self‑similar way (the A8 “Infinity‑Resolution” conjecture), these DSI footprints should be present after Kerr‑mode subtraction.

---

## 1) **Abstract** ($\le 200$ words)

The DSI‑RDM is a **T2 instrument** for detecting *fractal‑like self‑similarity* in gravitational‑wave **ringdown** time series. It normalizes time by a reference frequency (e.g., the dominant QNM), removes the smooth Kerr quasinormal model (QNM) fit, whitens residuals, and looks for **log‑periodic** structure expected from **discrete‑scale invariance** (DSI): equally spaced peaks in **log‑time** or **log‑frequency**, stable across events after mass scaling. The meter reports three primary diagnostics with pass/fail gates: (G1) **log‑time comb** coherence; (G2) **scaling collapse** across events; (G3) **null false‑positive** control on simulated Kerr+noise. This design obeys the canon: *dimensionless programs, metriplectic discipline, reproducible artifacts, and explicit gates*. It does **not** assert a new black‑hole interior; it only measures whether external data carry DSI/scale‑collapse fingerprints, which the **A8 Infinity‑Resolution** conjecture predicts for hierarchical organization.

---

## 2) **Background & Scientific Rationale**

* **Canon anchors.** The equations registry defines the hyperbolic (KG/J‑limb) and overdamped (RD/M‑limb) branches and requires **dimensionless normalization**; meters are judged by gates, not rhetoric. We will adopt that discipline here.
* **Why DSI for “fractal interior”?** A self‑similar (Mandelbulb‑like) interior implies **discrete** rather than continuous scale symmetry. That leaves **log‑periodic** imprints when waves scatter or “ring” through a hierarchical structure—observable as **equally spaced features in log‑time or log‑frequency** after removing the smooth Kerr QNMs.
* **Precedent for scaling collapse.** The *A6* result codifies a concrete “collapse” gate—curves from different parameter settings lie on one master curve after dimensionless re‑scaling. We adopt the same *instrumental* idea for ringdown across different source masses/spins.
* **Program fit.** This is a **T2 meter** in the Unification Spec: it makes **no** gravity claim; it only tests structure with numeric thresholds, matching the spec’s ethos of meters→phenomena.

---

## 3) **Intellectual Merit & Procedure (review rubric mapping)**

(1) **Importance:** If DSI passes robust gates on real events, that’s a *new, scale‑free structure* in ringdown residuals—high‑signal leverage for any interior model.
(2) **Broader impacts:** Same meter applies to *X‑ray/QPO* time series or lab analogs (log‑periodic cascades), encouraging cross‑domain tests.
(3) **Approach clarity:** Fully specified normalization, fits, transforms, nulls, and gates below; artifacts are CSV/JSON/PNG with commit+seed.
(4) **Rigor:** Windows, FFT/Wavelet caveats, and alias/Gibbs handling conform to the *Technical & Scientific Principles*; statistics use bootstrap/CV per the *Data Science Rules*.

---

## 4) **Experimental Setup and Diagnostics**

**Inputs (per event):** strain $h(t)$ or ringdown segment $t \in [t_0, t_1]$, detector PSD estimate, posterior mass/spin for mass scaling, chosen QNM basis $\{\omega_n, \tau_n\}$ for subtraction.
**Normalization:** define dimensionless time $ \theta = \omega_0 t $ with $ \omega_0 $ the best‑fit dominant QNM frequency; amplitude normalized by initial envelope. (Dimensionless programs are canon—drop units early and cleanly.)
**Pipeline (meter as measurement device):**

1. **Windowing & whitening.** Band‑limit and taper to control leakage; whiten residuals by PSD. (Windowing reduces Gibbs; oversample $\ge 7\text{–}10$ pts/cycle for reliable spectra.)
2. **QNM fit & subtraction.** Fit $ h_{\text{QNM}}(\theta) = \sum_k A_k e^{-\alpha_k \theta}\cos(\beta_k \theta + \phi_k) $. Residual $ r(\theta) = h(\theta) - h_{\text{QNM}}(\theta) $.
3. **Log‑time transform.** Let $ \tau = \ln(\theta/\theta_0) $. Compute periodogram $ P(\Omega) $ of $ r(\tau) $ (Lomb–Scargle acceptable for irregular $ \tau $).
4. **DSI comb test.** Search for $ \ge 3 $ peaks with ~constant spacing $ \Delta\Omega $ and stable phases across events after mass scaling.
5. **Wavelet ridge ratios.** Complex Morlet in $ \tau $: test for equal **log‑spacing of ridges**; compute ratio variance.
6. **Scaling collapse.** Aggregate normalized envelopes $ \mathcal{E}(\theta) $ across events; compute envelope of deviations vs. a template curve, as in A6.

**Primary metrics & gates (pass/fail):**

* **G1 (Log‑comb coherence):** mean pairwise peak‑position coherence $ C \ge 0.60 $ across events; FDR‑controlled p‑value ($< 0.01$). *(Decisive metric)*
* **G2 (Collapse envelope):** max envelope of collapsed curves $ \text{env}_{\max} \le 0.05 $ (A6 used 0.02 for its domain; here 0.05 acknowledges detector noise).
* **G3 (Null control):** on Kerr+colored‑noise simulations matched to each event’s SNR/PSD, **false‑positive rate $ \le 5\% $** for G1; empirical coverage reported with bootstrap.
* **G4 (Instrument sanity):** numerical cones/dispersion meter (KG J‑only) must meet M1 gates ($ R^2 \ge 0.999 $ on dispersion; light‑cone $ v \le c(1+0.02) $) before DSI runs are posted, per Spec.

**Secondary diagnostics (reported, not gated):** multifractal spectrum width $ \Delta \alpha $ via WTMM; stability vs. window choices (per the filter/alias rules).

### 4.1 Operational acceptance gates (DSI residuals)

* D1 — Peak detection: log‑time spectrum shows a single fundamental $ \omega_{\ln} $ with SNR $ \ge 5 $ and FDR $ q \le 0.05 $. Artifacts: spectrum PNG with annotated peak; detection JSON.
* D2 — $ t_0 $ robustness: peak location varies by $ \le 5\% $ across $ \pm 1\sigma $ jitter in $ t_0 $. Artifacts: sweep table CSV with peak frequency vs. jitter; summary JSON.
* D3 — Window robustness: peak location varies by $ \le 5\% $ across $ \pm 25\% $ changes in the analysis end time. Artifacts: sweep table CSV; summary JSON.
* D4 — Nulls: no spurious peak when the same pipeline runs on Kerr‑only injections (matched to the observed fit) and on shuffled residuals; measured power remains within the $ 95\% $ null band. Artifacts: null‑suite CSV/JSON; overlaid plots.
* D5 — Cross‑detector consistency: $ \omega_{\ln} $ estimates agree across H1, L1 (and V1 if present) within the joint $ 95\% $ CI. Artifacts: per‑detector estimates CSV with CIs; consistency summary JSON.

---

## 5) **Variables**

* **Independent:** event id; reference mode $ \omega_0 $; ringdown window $[t_0,t_1]$; whitening method; window function; QNM basis size $K$.
* **Dependent:** comb spacing $ \Delta \Omega $; comb coherence $ C $; collapse $ \text{env}_{\max} $; false‑positive rate $ \hat{p}_{\mathrm{FP}} $; $ \Delta \alpha $.
* **Controls:** taper type, PSD estimator, sampling cadence; all recorded in JSON; seed logged. Canon defaults (e.g., reference frequency constants) are drawn from the **Constants & Defaults** registry where applicable and *never* duplicated.

---

## 6) **Equipment / Hardware**

Data‑analysis only (CPU/GPU optional). AMD stack is assumed; double precision; deterministic seeds; wall‑clock and environment logged per Spec.

---

## 7) **Methods / Procedure (reproducible pipeline)**

* **Exact equations**: This meter is an analysis instrument; the physics kernels it references (KG J‑limb, RD M‑limb) remain as in canon, used only for *sanity meters* and not altered here.
* **IC/BC:** N/A for data; simulated nulls use canonical hyperbolic kernels for instrument checks.
* **Post‑processing:** FFT/Lomb–Scargle/wavelet routines with windowing; bootstrap uncertainty for metrics; CONTRADICTION_REPORT JSON on any gate failure, as in the standards.

---

## 8) **Pre‑Run Config Requirements** *(per template; minimal viable skeletons)*

**`Derivation/code/physics/black_holes/APPROVALS.json`**

```json
{
  "preflight_name": "dsi_ringdown_preflight",
  "description": "Approval manifest for DSI-RDM meter; preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Only PROPOSAL-tagged runs write artifacts."
}
```

**`PRE-REGISTRATION.json`**

```json
{
  "proposal_title": "T2 — Discrete-Scale Invariance Ringdown Meter",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"Ringdown residuals exhibit DSI log-comb post mass-scaling.","direction":"increase"},
    {"id":"H2","statement":"Mass-normalized envelopes collapse within env_max<=0.05.","direction":"decrease"}
  ],
  "variables": {
    "independent": ["omega0","window","whitener","K_QNM"],
    "dependent": ["comb_coherence","deltaOmega","env_max","p_fp"],
    "controls": ["taper","psd_method","seed"]
  },
  "pass_fail": [
    {"metric":"comb_coherence","operator">=","threshold":0.60,"unit":""},
    {"metric":"env_max","operator":"<=","threshold":0.05,"unit":""},
    {"metric":"p_fp","operator":"<=","threshold":0.05,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/black_holes/dsi_ringdown_meter.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

**`dsi_ringdown_meter.v1.json` (Spec)**

```json
{
  "run_name": "DSI-RDM",
  "version": "1.0.0",
  "tag": "dsi-rdm-v1",
  "schema_ref": "Derivation/code/physics/black_holes/schemas/dsi_rdm.schema.json",
  "parameters": {
    "omega0_ref":"qnm220",
    "window":[0.0,8.0],
    "whitener":"median-psd",
    "taper":"planck",
    "K_QNM":3,
    "seeds":[1,2,3]
  }
}
```

**`schemas/dsi_rdm.schema.json`** *(JSON Schema draft 2020‑12; minimal, extend as needed)*

```json
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "$id":"vdm:black_holes:dsi_rdm:1",
  "title":"DSI-RDM spec schema",
  "type":"object",
  "properties":{
    "omega0_ref":{"type":"string","enum":["qnm220","qnm330"]},
    "window":{"type":"array","items":{"type":"number"},"minItems":2,"maxItems":2},
    "whitener":{"type":"string"},
    "taper":{"type":"string"},
    "K_QNM":{"type":"integer","minimum":1}
  },
  "required":["omega0_ref","window","whitener","taper","K_QNM"]
}
```

---

## 9) **Results & Artifacts (expected for this meter)**

* **PNG:** log‑comb spectrum with peaks annotated; collapse plot with numeric caption reporting $ \text{env}_{\max} $.
* **CSV:** per‑event peak lists, ridge coordinates, envelope deviations.
* **JSON:** gate summary `{G1:true/false, G2:true/false, G3:true/false}`, seeds, commit, timings, environment. (Same basename discipline as the RESULTS standard.)

---

## 10) **Risk Notes & Kill‑Plans**

* **Spectral leakage / aliasing:** Mitigate with tapers, conservative bandwidths, oversampling; verify stability under alternative windows. If comb significance falls below gate after window sweep → **kill** H1 for that dataset.
* **QNM mis‑fit:** Use multiple (K) and cross‑validation; if residual power tracks fit errors rather than log‑periodic structure, **fail G1** and emit CONTRADICTION_REPORT.
* **Selection bias:** Pre‑register event list and mass‑scaling rule; bootstrap across events; if collapse is dominated by a single loud event, **quarantine** result and require replication.

---

## 11) **Clean‑Architecture Notes (execution comfort)**

Place code in a **modular monolith**: `presentation/black_holes/dsi_rdm/`, `application/.../ports/`, `domain/.../`, `infrastructure/gwosc/.../adapters/`. Enforce $ \le 500 $ LOC per file, repository pattern for I/O, and no outer→inner deps, mirroring the discipline elsewhere. *(You’ve already standardized this across instruments.)*

---

## **How this addresses the motivating question**

* A Mandelbulb‑like interior is a *geometric metaphor* for the **A8 Infinity‑Resolution** idea: *folding structure indefinitely without divergence*. This meter doesn’t assert that geometry; it **tests** for the **necessary consequence**—**discrete‑scale invariance**—in the only window we truly have: the **ringdown**. If G1–G3 pass across mass‑scaled events, you’ve got empirical smoke pointing straight at hierarchical organization in the interior (or its boundary dynamics). If they fail under strong null controls, the fractal‑interior hypothesis is culled at the instrument level—clean science either way.

---

## **Interaction Pattern (concise)**

**Classification:** *T2 Instrument (runtime‑only meter)*
**Objective recap:** Detect DSI/scale‑collapse in mass‑normalized ringdown residuals.
**Action plan:**

1. Implement meter per spec; wire approvals/PREREG.
2. Validate cones/dispersion sanity meter (M1 gates).
3. Run null suite (Kerr+noise) to set FP rate.
4. Process curated event set; compute G1–G3.
5. Emit RESULTS with PNG/CSV/JSON and PASS/FAIL; post CONTRADICTION_REPORT on any failure.
   **Verification:** Axiom/Noether meters (J‑limb) OK; Lyapunov checks (M‑limb) unaffected; collapse gate adopts A6 discipline.
   **Assumptions/Risks:** QNM basis adequate; whitening stable; mass posteriors narrow enough for collapse—kill plans above.  
   **Next steps:**
