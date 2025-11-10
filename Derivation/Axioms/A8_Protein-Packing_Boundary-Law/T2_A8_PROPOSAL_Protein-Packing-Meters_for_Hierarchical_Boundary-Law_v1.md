# T2_A8_PROPOSAL_Protein‑Packing‑Meters_for_Hierarchical_Boundary‑Law_v1.md

> **Created Date:** (fill on commit)
> **Provenance:** c2d71627c286029ae90267e4051411fa1fb3973e
> **SHA Hash:** → `HEAD_SHA_HERE`; salted provenance recorded per template (Section 5.1.1).
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** (Repository `LICENSE`)
> **Short summary (TL;DR):** Proposed is a **T2 instrument** that clones protein‑structure meters—(R_g(n)), (S(q)), (f_{\text{core}}), (\langle\phi\rangle)—as **A8 boundary‑law hierarchy meters**, with preregistered pass/fail gates and provenance. It calibrates against high‑resolution x‑ray monomer proteins and the coarse‑grained model ladder that progressively adds stereochemical constraints.

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** (Neuroca, Inc.) — PI, implementer, approver.

## 3. Abstract

Folded proteins present a tight, empirical sandbox linking **compactness**, **internal scale‑breaks**, and **void structure**. Key observables—internal radius‑of‑gyration (R_g(n)) with two exponents, structure factor (S(q)), core fraction (f_{\text{core}}!\approx!0.09), and core packing fraction (\langle\phi\rangle!\approx!0.55)—are reproducible across thousands of x‑ray monomer structures. Minimal coarse‑grained models succeed only when **backbone bend/dihedral constraints** and **realistic side‑chain geometry** are enforced. Proposed here is a **T2 instrument** that (i) re‑implements the rSASA‑based core detector and Voronoi/MC packing calculator, (ii) computes (R_g(n)) and (S(q)), and (iii) preregisters **A8‑style gates** so these metrics function as boundary‑law meters for hierarchical interfaces. The instrument is phenomenon‑agnostic at T2; it becomes a **gate** for later A8 claims at T4–T8.

## 4. Background & Scientific Rationale

**A8 context.** CF3 formalizes A8’s prediction that finite‑energy compact phases resolve via **hierarchical interfaces** with **area‑law energy**, **log‑depth (N(L))**, and **boundary information concentration**. This proposal supplies meters to operationalize those quantities in a biological exemplar.

**Protein system as meter bed.** Folded proteins are compact (R_g(N)!\sim!N^{1/3}) yet show **two‑regime scaling** internally: (R_g(n)!\sim!n^{\nu_1}) for small (n) with (\nu_1>1/3), and (R_g(n)!\sim!n^{\nu_2}) for large (n) with (\nu_2<1/3); the kink sits near (n^*!\sim!30) in realistic models. The dataset also stabilizes (f_{\text{core}}!\approx!0.09) and (\langle\phi\rangle!\approx!0.55) for core residues. Minimal models require backbone **bend/dihedral** constraints plus **multi‑bead side‑chains** to match all four metrics simultaneously. These are **boundary‑law‑like constraints** that generate a robust, hierarchical interior.

**Why a T2 instrument.** The Tier Ladder mandates **meter calibration before claims**. This instrument joins your STIV meters as a cross‑domain boundary‑law gate. Later A8 proposals must pass **both** STIV boundary meters and the protein‑packing meters before asserting area‑law/log‑depth claims.

## 5. Intellectual Merit and Procedure

**Importance.** Supplies **high‑signal, biological meters** for compactness, internal scale‑breaks, and void structure—exactly the regime A8 targets.
**Broader impacts.** Provides falsifiable gates for compact phases in **materials, active matter, and biomolecular** simulations.
**Approach.** Reproduce (R_g(n)), (S(q)), (f_{\text{core}}), (\langle\phi\rangle) pipelines against x‑ray baselines; certify pass/fail gates; publish machine‑actionable artifacts per template.

---

## 5.1 Experimental Setup and Diagnostics

**Meters (and methods).**

1. **(R_g(n))** — average subchain (R_g) over all windows of length (n) (as defined in the papers). Report two‑slope fit ((\nu_1,\nu_2)) and kink (n^*) with CIs.
2. **(S(q))** — backbone structure factor; overlay vs backbone diameter scale (\sigma_{bb}).
3. **Core fraction (f_{\text{core}})** — **rSASA thresholding** (Lee–Richards probe, rSASA (<10^{-3})) to tag core residues.
4. **Core packing (\langle\phi\rangle)** — **radical Voronoi** near the core surface + Monte‑Carlo volume estimation to compute local packing and (\langle\phi\rangle).

**Diagnostics (counts).** (R_g(n)) (1), two‑slope/kink fit (1), (S(q)) (1), rSASA core detector (1), Voronoi/MC packer (1), agreement scores (4).

**Known parameters / defaults.**

| Key           | Meaning                             | Default            |
| ------------- | ----------------------------------- | ------------------ |
| (\sigma_{bb}) | backbone bead spacing for scaling   | (3.8,\text{Å})     |
| probe         | rSASA probe diameter (Lee–Richards) | (0.73,\sigma_{bb}) |
| rSASA cut     | core threshold                      | (10^{-3})          |
| seeds         | random seeds                        | ({0..19})          |

(Probe and rSASA follow the referenced method; (\sigma_{bb}) is dimensional context for (S(q)) overlays.)

**Pass/Fail gates (calibration against x‑ray baseline).**

* **G‑Rg‑2Slope.** Detect two distinct exponents with CI‑separation and kink (n^*) in (20!-!40) (unitless (n)); report (\nu_1>1/3), (\nu_2<1/3); normalized MSE of (\langle R_g(n)\rangle) vs x‑ray baseline (\le 0.03).
* **G‑S(q).** Cross‑correlation with x‑ray ensemble average (\ge 0.95) over prereg (q)‑window; peak positions within prereg tolerances.
* **G‑CoreFrac.** (f_{\text{core}}=0.09\pm 0.01) under the prereg detector.
* **G‑PackFrac.** (\langle\phi\rangle) within ([0.55,0.59]) under the prereg Voronoi/MC method; instrument PASS if CI overlaps this band.

**Model ladder sanity (non‑gating, for context figures).** Reproduce the qualitative ladder: CRW/BADA fail core packing; FJSC/InSeq match (R_g(n)) and (S(q)); multi‑bead side‑chains (modMPSC) improve (\langle\phi\rangle) while maintaining (f_{\text{core}}). These are **reference overlays**, not PASS criteria.

### 5.1.1 Pre‑Run Config Requirements (machine‑readable)

Follow the repository’s approvals/prereg discipline exactly (paths may be adjusted to your tree).

```
Derivation/code/physics/protein_packing/APPROVALS.json
Derivation/code/physics/protein_packing/schemas/ProteinPackingMeters.schema.json
Derivation/code/physics/protein_packing/specs/ProteinPackingMeters.v1.json
Derivation/experiments/prereg/ProteinPackingMeters.v1.json
```

**APPROVALS.json (template)**

```json
{
  "preflight_name": "protein_packing_preflight",
  "description": "Approval manifest for protein-packing meters; preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight runs may execute under Derivation/code/tests. Artifact-writing runs require this proposal.",
  "pre_registered": true,
  "proposal": "Derivation/Proposals/T2_A8_PROPOSAL_Protein-Packing-Meters_v1.md",
  "allowed_tags": ["protein-packing-meters-v1"],
  "schema_dir": "Derivation/code/physics/protein_packing/schemas",
  "approvals": {
    "protein-packing-meters-v1": {
      "schema": "Derivation/code/physics/protein_packing/schemas/ProteinPackingMeters.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto",
      "approval_key": "auto"
    }
  }
}
```

**PRE‑REGISTRATION.json (minimum)**

```json
{
  "proposal_title": "T2 — Protein-Packing Meters for A8 Hierarchical Boundary Law",
  "tier_grade": "T2",
  "commit": "HEAD_SHA_HERE",
  "salted_provenance": "salted_sha256_here",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"Two-slope (ν1>1/3, ν2<1/3) structure in ⟨Rg(n)⟩ is detected with CI-separated exponents.","direction":"no-change"},
    {"id":"H2","statement":"S(q) overlay passes prereg cross-correlation band.","direction":"no-change"},
    {"id":"H3","statement":"Core fraction f_core matches 0.09±0.01 under prereg method.","direction":"no-change"},
    {"id":"H4","statement":"Core packing ⟨φ⟩ lies in [0.55,0.59] under prereg method.","direction":"no-change"}
  ],
  "variables": {
    "independent": ["protein_id","seed","q_window","n_window"],
    "dependent": ["ν1","ν2","n_star","MSE_Rg","xcorr_Sq","f_core","phi"],
    "controls": ["probe_diam","rSASA_cut","voronoi_boxN","mc_samples"]
  },
  "pass_fail": [
    {"metric":"MSE_Rg","operator":"<=","threshold":0.03,"unit":""},
    {"metric":"xcorr_Sq","operator":">=","threshold":0.95,"unit":""},
    {"metric":"|f_core-0.09|","operator":"<=","threshold":0.01,"unit":""},
    {"metric":"phi_band_violation","operator":"==","threshold":0,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/protein_packing/specs/ProteinPackingMeters.v1.json"],
  "registration_timestamp": "AUTO-UTC"
}
```

**Specs (runner)**

```json
{
  "run_name": "ProteinPackingMeters",
  "version": "1.0.0",
  "tag": "protein-packing-meters-v1",
  "schema_ref": "Derivation/code/physics/protein_packing/schemas/ProteinPackingMeters.schema.json",
  "parameters": {
    "probe_diam_over_sigma_bb": 0.73,
    "rSASA_cut": 1e-3,
    "voronoi_boxN": 500000,
    "mc_samples": 500000,
    "q_window": [0.5, 3.0],
    "n_window": [2, 512]
  },
  "seeds": [0,1,2,3,4,5,6,7,8,9]
}
```

**Schema (minimum)**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vdm://schemas/ProteinPackingMeters.schema.json",
  "title": "ProteinPackingMeters v1",
  "type": "object",
  "properties": {
    "probe_diam_over_sigma_bb": {"type":"number","minimum":0},
    "rSASA_cut": {"type":"number","minimum":0},
    "voronoi_boxN": {"type":"integer","minimum":10000},
    "mc_samples": {"type":"integer","minimum":10000},
    "q_window": {"type":"array","items":{"type":"number"},"minItems":2,"maxItems":2},
    "n_window": {"type":"array","items":{"type":"integer"},"minItems":2,"maxItems":2}
  },
  "required": ["probe_diam_over_sigma_bb","rSASA_cut","voronoi_boxN","mc_samples","q_window","n_window"]
}
```

(Conforms to your proposal template’s prereg/schemas discipline.)

## 5.2 Experimental runplan

**Scope banner:** *T2 instrument calibration only; no phenomenon claims.*

**Datasets.** Subset of single‑chain x‑ray structures as described in the referenced study (monomers; PISCES‑derived; chain‑quality filters). Use 100–300 proteins for calibration and reserve ≥200 for holdout QC plots.

**Independent variable grid.**

* (n)-windows: (n\in[2,512]) (log‑spaced); seeds: 10; (q)-window: ([0.5,3.0]\times 2\pi/\sigma_{bb}).
* rSASA probe (=0.73,\sigma_{bb}), cut (10^{-3}); Voronoi box (5\times10^5); MC samples (5\times10^5).

**Outputs & artifacts.** CSV/JSON for (R_g(n)), ((\nu_1,\nu_2,n^*)), (S(q)), (f_{\text{core}}), (\langle\phi\rangle); PDF plots; PASS/FAIL manifest. Publish under `Derivation/code/outputs/meters/protein_packing/{tag}/` and author RESULTS per repo standards.

**Success action.** Mark instrument **CERTIFIED**; register as an A8 meter/gate used by subsequent CFN/PROPOSALs.
**Failure action.** Quarantine with contradiction report; sweep probe size and rSASA cuts; check Voronoi box and MC convergence; re‑estimate two‑slope CI method.

---

## 6. Personnel

**Justin K. Lietz** — implement meters, prereg/specs/schemas; run calibration/holdout; publish RESULTS and PASS/FAIL; file promotion PR on PASS. (Organization mirrors your STIV meter role definitions.)

## 7. References

* **Proposal & Tier Standards** — VDM Whitepaper Template; Tier‑Graded Ladder v3.
* **A8 Lineage** — CF3_A8_Scaling_Hierarchical_Interfaces; T8_A8_PROPOSAL_Lietz_Infinity_Conjecture.
* **STIV Meters (for cross‑gating)** — T2_STIV Macrostate & Gradient‑Flow Meters.
* **Protein structural meters** — Logan et al., *Effect of stereochemical constraints on the structural properties of folded proteins* (v2, Sep‑2025) and v1 (Jan‑2025). (Metrics: (R_g(n)), (S(q)), (f_{\text{core}}!\approx!0.09), (\langle\phi\rangle!\approx!0.55); kink (n^*), minimal model ladder).

---

## Lineage mapping to your ladder (what you asked for)

* **HYPOTHESIS (new):** `H3_A8_Protein_Boundary_Meter.md` — “Compact hierarchical interfaces admit protein‑like boundary meters with stable scale‑break signatures (two‑slope (R_g(n)), (f_{\text{core}}), (\langle\phi\rangle), (S(q))).”
* **COMPLETE FORMALISM:** already anchored by `CF3_A8_Scaling_Hierarchical_Interfaces.md`.
* **CFN (1:1 Notebook):** `CFN3_A8_Scaling_Hierarchical_Interfaces.ipynb` — exact re‑derivation-to‑code of CF3; add a section that computes (N(L)), area‑law fits, and tubular‑energy/Info proxies for A8 (ties to STIV gates for later T‑tiers).
* **PROPOSAL (this):** `Derivation/Proposals/T2_A8_PROPOSAL_Protein-Packing-Meters_v1.md` — instrument certification so later A8 claims can use these meters as acceptance gates.

---

## Implementation classification, objective, and plan (VDM work order style)

**Classification:** Derived‑limit (Instrument)
**Objective (one‑liner):** Certify protein‑packing meters as A8 boundary‑law gates with prereg PASS/FAIL.
**Action plan (≤7):**

1. Implement rSASA core detector and Voronoi/MC packer per v2 methods.
2. Implement (R_g(n)) and two‑slope/kink fitter; add normalized MSE vs x‑ray baseline.
3. Implement (S(q)) overlay and cross‑correlation meter.
4. Author **APPROVALS/PREREG/SPEC/SCHEMA** (Section 5.1.1) and sign the prereg tag.
5. Calibrate thresholds on 100–300 monomer structures; reserve holdout for QC.
6. Publish RESULTS whitepaper + artifacts; register as A8 meter/gate.
7. Wire cross‑gating with STIV meters in the CI to guard later A8 claims.

**Verification**

* **Axiom gates:** A7 measurability (explicit meters & protocol); A6 scale windows; instrument locality.
* **Software gates:** ≤500 LOC/file, clean architecture, repo‑style artifacts, tests mirror source.
* **Derived checks:** Agreement with x‑ray baselines on four metrics; two‑slope detection stability.

**Assumptions/Risks**

* Dataset filters shift (\langle\phi\rangle) a few percent; **kill‑method:** lock detector/probe; run sensitivity sweeps.
* Two‑slope fit depends on (n)-window; **kill‑method:** prereg windows and bootstrap CIs.
