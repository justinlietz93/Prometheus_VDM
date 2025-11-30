# 1. **T4 (Prereg)** – *Origin‑Void Test:* Is the CMB Cold Spot the VDM Level‑0 Void?

> **Created Date:** 2025‑11‑19
> **Commit:** `<git rev-parse HEAD>`
> **Salted provenance:** `{base_sha256}:{salt_hex}:{salted_sha256}` (see §5.1.1)
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** See `LICENSE` in repo
> **Short summary (TL;DR):** VDM posits a tachyonic genesis that leaves a **Level‑0 “Origin Void.”** This preregistered test asks whether the **CMB Cold Spot** directionally **coincides with** and **modulates** low‑ℓ structure as predicted by VDM, using a pseudo‑(C_\ell) E/B/N pipeline and low‑ℓ power‑tensor diagnostics.

***Provenance discipline.*** Salt and record the repo tree hash in `PRE-REGISTRATION.json`; tag a prereg (signed/annotated) *before* any artifact‑writing run. The proposal itself carries the same hashes in §5.1.1. 

---

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** — PI, proposer, implementer (Neuroca / Prometheus VDM)

---

## 3. Abstract

VDM’s axiom‑core predicts a hierarchical vacuum break (A8) with a **distinguished origin** left as a deep void; if correct, the CMB should exhibit **large‑angle directionality** pointing toward that origin and a **deficit imprint** consistent with a supervoid ISW template. This T4 prereg registers a concrete, falsifiable claim: the **CMB Cold Spot** encodes VDM’s **Level‑0 Origin Void**. Using Planck PR4 component‑separated maps (temperature, optional polarization), we test: (i) **low‑ℓ axis alignment** between the power‑tensor principal direction and the Cold‑Spot axis; (ii) **hemispherical power asymmetry** aligned with that same axis; and (iii) **template‑matched ISW correlation** with an Eridanus‑supervoid profile. Gates, nulls, and look‑elsewhere penalties are preregistered; decisions are machine‑auditable.

---

## 4. Background & Scientific Rationale

* **CMB anomalies exist and persist.** Planck confirms several large‑angle “anomalies” (e.g., hemispherical asymmetry, low‑ℓ alignments, Cold Spot), debated since WMAP. ([ResearchGate][1])
* **Cold Spot ↔ Eridanus supervoid (ISW)** remains contested but repeatedly studied; several analyses support a line‑of‑sight supervoid contribution. ([ADS][2])
* **VDM alignment.** Your canon places measurements under a **metriplectic** umbrella and enforces dimensionless programs; instruments (meters) precede phenomenon claims. We chain to the T2 E/B/N pseudo‑(C_\ell) pipeline and low‑ℓ diagnostics already outlined in your cosmology proposal index and validation map.   
* **Scope & boundaries.** This is a **phenomenon claim (T4)** on top of **T2 meters**; it does **not** alter GR nor Planck instrument models. It registers strict gates; failures auto‑emit contradiction reports.

*Why now?* The claim is uniquely **geometric and directional**—a clean win/loss telemetry for VDM’s “single origin” narrative with near‑term computability (PR4 maps + pseudo‑(C_\ell) tools). For standard context on anomaly status, we cite PDG 2024 CMB review. ([Particle Data Group][3])

---

## 5. Intellectual Merit and Procedure

**Importance.** A positive result turns large‑angle “glitches” into a coherent **origin geometry** consistent with VDM’s A8 hierarchy. A null result constrains VDM’s anisotropy claims.

**Approach.** Treat **numerical analysis as a meter**: show derivation → discretization → implementation, tie every claim to a **gate** with a **threshold** and **decision rule**; bind runs to **pre‑tagged provenance**. 

---

## 5.1 Experimental Setup and Diagnostics

**Data.** Planck PR4/NPIPE full‑sky (T) maps (SMICA, Commander); optional (E/B) for EBN cross‑checks. Standard PR4 masks and beams. (Paths captured in SPEC.)
**Meters (upstream, T2).** Pseudo‑(C_\ell) E/B/N estimator; power‑tensor (low‑ℓ) axis extractor; hemispherical asymmetry metrics. (These are already present/outlined in your proposal index.) 
**Parameters (defaults).** (N_{\rm side}\in{256,512}), (\ell_{\max}\in{64,128}), component (\in{\text{SMICA}, \text{Commander}}), mask (\in{\text{conservative}, \text{aggressive}}), smoothing (\theta_{\rm FWHM}\in{1^\circ,2^\circ}).
**Diagnostics (per run).**
D1. **Power‑tensor axis** (\hat{\mathbf{n}}*{\rm PT}) for (\ell\le 3,5); **alignment angle** (\alpha=\cos^{-1}(\hat{\mathbf{n}}*{\rm PT}!\cdot!\hat{\mathbf{n}}*{\rm CS})).
D2. **Hemispherical power asymmetry** (A) (dipole modulation amplitude) evaluated along (\hat{\mathbf{n}}*{\rm CS}) and on rotated nulls.
D3. **Cold‑Spot template match**: ISW supervoid matched‑filter SNR with void radius/depth prior ranges from literature; significance via MC/phase‑shuffle nulls. ([ADS][2])
D4. **EBN sanity**: pseudo‑(C_\ell^{EE,BB,NN}) in low‑ℓ bins consistent with reference bands (meter QC).

---

### 5.1.1 Pre‑Run Config Requirements (with JSON)

**Repository discipline** (approvals, prereg, schemas/specs) follows your canonical template. 

#### `Derivation/code/physics/cosmology/cmb/APPROVALS.json` (skeleton)

```json
{
  "preflight_name": "cmb_pr4_preflight",
  "description": "Approval manifest: preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "pre_registered": true,
  "proposal": "Derivation/Cosmology/CMB/T4_PROPOSAL_Origin_Void_ColdSpot_v1.md",
  "allowed_tags": ["cmb-origin-void-pr4-v1"],
  "schema_dir": "Derivation/code/physics/cosmology/cmb/schemas",
  "approvals": {
    "cmb-origin-void-pr4-v1": {
      "schema": "Derivation/code/physics/cosmology/cmb/schemas/cmb_origin_void.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "<auto>",
      "approval_key": "<auto>"
    }
  }
}
```

#### `Derivation/code/physics/cosmology/cmb/PRE-REGISTRATION.json` (minimum keys; salted)

```json
{
  "proposal_title": "T4 — Origin-Void Test: CMB Cold Spot = VDM Level-0",
  "tier_grade": "T4",
  "commit": "<git-sha>",
  "salted_provenance": {
    "base_sha256": "<tree-hash>",
    "salt_hex": "<16B-hex>",
    "salted_sha256": "<hash(base||salt)>"
  },
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Low-ℓ power-tensor axis aligns with Cold Spot axis within α≤20° after beam/mask corrections.", "direction": "decrease" },
    { "id": "H2", "statement": "Hemispherical power asymmetry A is maximized along the Cold Spot axis and exceeds prereg threshold under null-calibrated p≤0.01.", "direction": "increase" },
    { "id": "H3", "statement": "ISW supervoid template centered at the Cold Spot shows matched-filter SNR≥3 with LEE-corrected p≤0.05.", "direction": "increase" },
    { "id": "H4", "statement": "EBN meter QC holds (pseudo-C_ℓ^BB, pseudo-C_ℓ^NN consistent with null bands at low-ℓ).", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["Nside","lmax","component","mask","theta_fwhm_deg","seeds"],
    "dependent": ["alpha_deg","A","SNR_isw","p_axis","p_A","p_isw","qc_E","qc_B","qc_N"],
    "controls": ["n_mc","n_rot","beam_file","mask_file","bandpass","phase_shuffle"]
  },
  "pass_fail": [
    { "metric": "alpha_deg", "operator": "<=", "threshold": 20.0, "unit": "deg" },
    { "metric": "p_A", "operator": "<=", "threshold": 0.01, "unit": "" },
    { "metric": "SNR_isw", "operator": ">=", "threshold": 3.0, "unit": "" },
    { "metric": "p_isw", "operator": "<=", "threshold": 0.05, "unit": "" },
    { "metric": "qc_flags", "operator": "==", "threshold": "PASS", "unit": "" }
  ],
  "nulls": {
    "rotations": 2000,
    "phase_shuffles": 2000,
    "axis_uniform": true
  },
  "spec_refs": ["Derivation/code/physics/cosmology/cmb/specs/cmb_origin_void.pr4.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

#### `Derivation/code/physics/cosmology/cmb/schemas/cmb_origin_void.schema.json` (stub)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vdm://cosmology/cmb/cmb_origin_void.schema.json",
  "title": "CMB Origin-Void (Cold Spot) Spec Schema",
  "type": "object",
  "required": ["run_name", "version", "tag", "data", "parameters", "seeds"],
  "properties": {
    "run_name": { "type": "string" },
    "version":  { "type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$" },
    "tag":      { "type": "string", "enum": ["cmb-origin-void-pr4-v1"] },
    "data": {
      "type": "object",
      "required": ["map_T","mask","beam"],
      "properties": {
        "map_T": { "type": "string" },
        "mask":  { "type": "string" },
        "beam":  { "type": "string" }
      }
    },
    "parameters": {
      "type": "object",
      "required": ["Nside","lmax","theta_fwhm_deg","n_mc","n_rot"],
      "properties": {
        "Nside": { "type": "integer", "enum": [256,512] },
        "lmax":  { "type": "integer", "enum": [64,128] },
        "theta_fwhm_deg": { "type": "number" },
        "n_mc": { "type": "integer", "minimum": 1000 },
        "n_rot": { "type": "integer", "minimum": 1000 }
      }
    },
    "seeds": {
      "type": "array", "items": { "type": "integer", "minimum": 1 }, "minItems": 1
    }
  }
}
```

#### `Derivation/code/physics/cosmology/cmb/specs/cmb_origin_void.pr4.v1.json` (example SPEC)

```json
{
  "run_name": "cmb-origin-void-pr4",
  "version": "1.0.0",
  "tag": "cmb-origin-void-pr4-v1",
  "schema_ref": "Derivation/code/physics/cosmology/cmb/schemas/cmb_origin_void.schema.json",
  "data": {
    "map_T": "inputs/planck/pr4/SMICA/NPIPE_full_T_nside512.fits",
    "mask":  "inputs/planck/pr4/masks/NPIPE_common_mask_nside512.fits",
    "beam":  "inputs/planck/pr4/beams/SMICA_beam_transfer_lmax600.fits"
  },
  "parameters": {
    "Nside": 512,
    "lmax": 128,
    "theta_fwhm_deg": 1.0,
    "n_mc": 2000,
    "n_rot": 2000
  },
  "seeds": [1, 2, 3]
}
```

---

## 5.2 Experimental runplan

**Classification:** *Derived‑limit (phenomenon) built atop T2 meters.*
**Objective recap:** Decide whether **Cold Spot ≡ Level‑0 Origin Void** is supported by **axis alignment, hemispherical asymmetry, and ISW template correlation** under preregistered nulls.

**Action plan (risk‑reduction order):**

1. **Meter QC:** Run E/B/N pseudo‑(C_\ell) checks and verify low‑ℓ bands vs references (pass/fail recorded).
2. **Axis test (H1):** Compute power‑tensor principal direction for (\ell\le 3) and (\ell\le 5); record (\alpha) to CS axis; MC rotations for p‑value.
3. **Hemispherical asymmetry (H2):** Evaluate amplitude (A) along CS axis and on rotated nulls; compute (p_A).
4. **ISW template (H3):** Fit supervoid template centered on CS; matched‑filter SNR and (p_{\rm isw}) via phase‑shuffled nulls.
5. **Decision:** Apply prereg thresholds with look‑elsewhere correction; emit PASS/FAIL JSON and CONTRADICTION_REPORT on fail.

**Verification:** Canon coupling to symbols/equations/constants for unit discipline.   

---

## 6. Research question

**Question.** Given PR4 maps, masks, and beams, do low‑ℓ statistics **prefer the Cold Spot axis** and does an **ISW supervoid template** produce **significant correlation** at that location—consistent with a VDM **Level‑0 origin**?
**Independent variables.** (N_{\rm side}), (\ell_{\max}), component method, mask choice, smoothing, seeds.
**Dependent variables.** (\alpha_{\rm deg}), (A), (\mathrm{SNR}_{\rm ISW}), (p)-values.
**Estimation.** Power‑tensor via low‑ℓ covariance; hemispherical asymmetry via dipole modulation fit; matched‑filter for ISW; MC/phase‑shuffle nulls for p.
**Falsifiable thresholds.** As in PRE‑REGISTRATION (`α≤20°`, `p_A≤0.01`, `SNR_isw≥3 & p_isw≤0.05`). (Look‑elsewhere penalty applied across ℓ‑cuts and masks.)

---

## 7. Methods

**Meters as instruments.** Treat pseudo‑(C_\ell) and low‑ℓ axis extraction as calibrated **T2 meters**; report their QC first. Your canon already codifies the “instrument‑first, phenomenon‑later” discipline. 

**Dimensionless program.** Binning and smoothing defined in (\ell)‑space; angles in degrees. Constants (e.g., defaults for sampling) reference the single‑source **CONSTANTS & DEFAULTS** registry. 

---

## 8. Gate definitions (pass/fail)

> **Primary gate (axis alignment, preregistered)**
> Target direction fixed at Cold Spot center ((\ell=209^\circ, b=-57^\circ)) in Galactic coordinates (Planck convention). Test statistic is the absolute cosine of the angle between the power‑tensor principal axis (computed from (\ell=2,3) or preregistered (\ell)-set) and the target direction. Null is isotropy with scan‑strategy surrogate.
> **Acceptance:** (p_{\text{axis,LEE}} \le 0.01) from 100,000 rotation scrambles of the mask‑and‑beam weighted sky, with the single preregistered direction eliminating field‑wide LEE. Failure emits **CONTRADICTION_REPORT** with seeds, commit, and mask id. (See PROPOSAL template/RESULTS standards for gate discipline.)  

> **G1 (Axis alignment)** — **PASS** if median (\alpha \le 20^\circ) and null‑calibrated (p_{\rm axis}\le 0.05) (with LEE correction across (\ell\le3,5) and mask set). **FAIL** otherwise.
> **G2 (Asymmetry amplitude)** — **PASS** if (p_A \le 0.01) along CS axis after null rotations; **FAIL** otherwise.
> **G3 (ISW template)** — **PASS** if matched‑filter (\mathrm{SNR}*{\rm ISW}\ge 3) **and** (p*{\rm isw}\le 0.05) under phase‑shuffled nulls; **FAIL** otherwise.
> **G4 (Meter QC)** — **PASS** if low‑ℓ (C_\ell^{BB}) and noise (C_\ell^{NN}) sit within reference bands and E/B leakage tests pass; **FAIL** otherwise.

**Decision rule.** Overall PASS requires **all** G1–G4 PASS. Any FAIL auto‑emits a `*_CONTRADICTION_REPORT.json` and quarantines artifacts.

---

## 9. Risks & mitigations

* **Mask/beam systematics at low‑ℓ.** Use PR4 masks, beam transfer functions; rotate‑nulls and phase‑shuffles to absorb residuals. ([ResearchGate][1])
* **ISW template uncertainty.** Use radius/depth priors spanning literature ranges; report Bayes factors and SNR; include alternative profiles in appendix. ([ADS][2])
* **Selection bias (axis hunting).** Preregister all axis choices (CS, low‑ℓ PEV, random rotations); apply LEE corrections.

---

## 10. Expected artifacts (numbered, with JSON/CSV)

* **Figure 1.** *Low‑ℓ power‑tensor axis vs Cold Spot direction.* Caption reports (\alpha), (p_{\rm axis}), CI.
* **Figure 2.** *Hemispherical power asymmetry along CS axis.* Caption reports (A), (p_A), CI.
* **Figure 3.** *ISW matched‑filter SNR map around CS.* Caption reports (\mathrm{SNR}*{\rm ISW}), (p*{\rm isw}).
* **Tables A–C.** CSVs for axis statistics, asymmetry metrics, and matched‑filter outputs.
* **JSON receipts.** Gate outcomes, seeds, commit, salted_provenance, meter QC.

---

## 11. References / Works cited (selection)

* **Planck 2018 (Isotropy & statistics of the CMB):** anomaly overview and methods. ([ResearchGate][1])
* **Axis of Evil (Land & Magueijo 2005; revisited 2007):** low‑ℓ alignment debates. ([arXiv][4])
* **Cold Spot ↔ Eridanus supervoid:** evidence and mapping. ([ADS][2])
* **Recent anomaly reviews/notes:** hemispherical asymmetry re‑assessments; PDG 2024 CMB review. ([arXiv][5])

**VDM canon & program indices:** Symbols, Equations, Constants, Results/Proposals, Unification Spec.     

---

## 12. Appendix — JSON sections (complete, ready to drop)

All four JSON blocks above (APPROVALS, PRE‑REGISTRATION, SCHEMA, SPEC) are included verbatim for immediate use. The prereg salted hashes must be created and recorded **before** artifact‑writing runs as per your template. 

---

## TL;DR (operational)

* **What’s new (explicit injection):** “**Cold Spot = Origin Void**” is now a **preregistered**, falsifiable VDM hypothesis with **axis**, **asymmetry**, and **ISW** gates, look‑elsewhere accounted.
* **How to run:** Fill SPEC data paths → create salted provenance → push signed prereg tag → run the T2 EBN meter then the H1–H3 tests with nulls → publish JSON gates and figures.
* **Strict discipline:** PASS requires **all** G1–G4; any FAIL triggers an automatic contradiction report.

[1]: https://www.researchgate.net/publication/337947259_Planck_2018_results_VII_Isotropy_and_Statistics_of_the_CMB?utm_source=chatgpt.com "Planck 2018 results. VII. Isotropy and Statistics of the CMB"
[2]: https://ui.adsabs.harvard.edu/abs/2015MNRAS.450..288S/abstract?utm_source=chatgpt.com "Detection of a supervoid aligned with the cold spot ..."
[3]: https://pdg.lbl.gov/2025/reviews/rpp2024-rev-cosmic-microwave-background.pdf?utm_source=chatgpt.com "29. Cosmic Microwave Background"
[4]: https://arxiv.org/abs/astro-ph/0502237?utm_source=chatgpt.com "[astro-ph/0502237] The axis of evil"
[5]: https://arxiv.org/html/2411.15786v1?utm_source=chatgpt.com "A Reassessment of Hemispherical Power Asymmetry in ..."
