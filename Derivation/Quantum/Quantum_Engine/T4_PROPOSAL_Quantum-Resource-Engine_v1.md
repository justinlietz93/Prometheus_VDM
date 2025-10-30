# **T4 — Quantum‑Resource Engine: A Metriplectic Ledger to Test “Beyond‑Carnot” Efficiencies**

> **Created:** 2025‑10‑30
> **Commit:** *to be stamped by CI on publish*
> **Salted provenance:** *sha256(commit ∥ doc‑id) to be stamped by CI*
> **Proposer contacts:** [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** Dual (open academic use; commercial by written permission)
> **TL;DR:** Proposed is a preregistered, metriplectic (Hamiltonian+metric) test‑bed that treats **correlations/coherence as thermodynamic resources**. The meter must show apparent efficiencies above the **classical** Carnot number when athermal resources are supplied, while **passing a generalized second‑law audit** that includes those resources. The document follows VDM axioms (A0–A7), gates, and artifact discipline. 

---

## 2. Proposers and affiliations

**Justin K. Lietz** — Principal investigator, implementation, approvals (PI).
Affiliation: VDM Project (Neuroca/Prometheus).

---

## 3. Abstract (≤200 words)

Classical Carnot efficiency assumes **thermal baths with no pre‑existing correlations**. At the nanoscale, **coherence, squeezing, and system–bath correlations** act as ordered resources that can be **converted to work**. The proposal registers a falsifiable test using VDM’s **metriplectic split** (skew‑symplectic (J) + metric (M), with entropy functional (\Sigma)) to (i) demonstrate **apparent** (\eta_{\text{heat}}>\eta_C) when athermal resources are supplied, and (ii) **verify a generalized second‑law inequality** that charges those resources in the ledger—no perpetual motion. The meter is built against VDM axioms (A0–A7), with explicit gates for symmetry/Noether, entropy monotonicity, causality/locality, and efficiency accounting. Results will be posted as CSV/JSON+figures with seeds and commit. 

---

## 4. Background & Scientific Rationale

**Program axioms.** VDM models dynamics with a single carrier field and metriplectic evolution
[
\partial_t q = J(q),\frac{\delta \mathcal I}{\delta q} + M(q),\frac{\delta \Sigma}{\delta q},\quad J^\top=-J,\ M^\top=M\ge 0,
]
with degeneracies (J\delta\Sigma=0), (M\delta\mathcal I=0) and a non‑decreasing entropy functional (\Sigma). These encode reversible structure vs. dissipative drift and the **H‑theorem** at the discrete/instrument level. 

**Why Carnot is the wrong yardstick here.** The textbook bound (\eta_C=1-T_C/T_H) presumes input energy is **heat only** from **uncorrelated** thermal reservoirs. When **athermal order** (coherence/squeezing/correlations) piggybacks on the baths, that order is additional **work‑like** fuel. A correct ledger must separate heat from ordered energy (ergotropy/information), restoring the second law under a generalized inequality rather than the bare Carnot number. The proposed meter operationalizes exactly this accounting within the VDM framework and posts pass/fail artifacts per RESULTS standards.

**VDM provenance used as scaffolding.** We rely on the canonical axioms, notation, and procedural math; prior validated instruments (e.g., RD dispersion & Fisher–KPP front speed) are referenced for gating practice and artifact discipline, not as foundations for quantum claims.  The doc conforms to proposal/authorship policy and pass/fail gates. 

---

## 5. Intellectual Merit and Procedure

**Importance.** Nanoscale engines sit at the junction of thermodynamics and information. A clean, preregistered demonstration that **apparent** >Carnot efficiencies arise exactly when **athermal resources are present**, together with a **law‑compliant audit**, is decision‑grade evidence for the field’s generalized accounting narrative.

**Broader impacts.** The meter clarifies resource bookkeeping for micro‑engines and provides a reusable, axioms‑aligned harness for future “thermo‑of‑information” tests. It advances **measurability** (A7) with dimensionless groups (A6) and metriplectic gates (A4–A5). 

**Approach.** Build a **two‑oscillator working medium** coupled to hot/cold baths (metric leg), plus an **ancilla channel** that injects a tunable athermal resource (coherence/correlation; Hamiltonian leg). Track heat (Q_H,Q_C), work (W), and resource flow (E_{\text{ath}}) via mutual‑information/ergotropy proxies to test:

* **(i)** (\eta_{\text{heat}}:=W/Q_H) can exceed (\eta_C) when (E_{\text{ath}}>0);
* **(ii)** **generalized second law holds:** (W \le \Delta \mathcal F_{\text{sys}} + \text{(priced athermal terms)}).

All metrics, seeds, and figures are preregistered; software gates enforce Clean Architecture and repository discipline.

**Discipline.** Proof‑first framing, explicit lemmas and gates, and mechanical pass/fail reporting follow the project’s rules for rigorous math, logic, and objective decision‑making.   

---

## 5.1 Experimental Setup and Diagnostics

**State & symbols (VDM canon).** We use the canonical notation sheet for fields, fluxes, and ledger variables; Noether energy/flux diagnostics anchor the J‑leg.  

**System under test (SUT).**

* Working medium: two coupled harmonic modes (WM‑A, WM‑B).
* Baths: Hot ((T_H)) to WM‑A; Cold ((T_C)) to WM‑B (metric (M) coupling).
* Ancilla channel: supplies athermal order with knob (\chi) (e.g., squeezing (r) or initial WM–bath mutual information (I)) via Hamiltonian (J) injection.
* Integrator: metriplectic split with degeneracy checks (g_1, g_2 \le 10^{-10}) (refined). 

**Diagnostics (meters).**

* Heat/work ledger: ((Q_H,Q_C,W)) from energy budget with Poynting‑like flux for (J)-leg, entropy production for (M)-leg. 
* Resource ledger: (E_{\text{ath}}(\chi)) via (a) ergotropy proxy; and/or (b) priced information (k_BT_{\rm ref},\Delta I) for correlation exchange.
* Efficiencies:
  [
  \eta_{\text{heat}}=\frac{W}{Q_H},\qquad
  \eta_{\text{gen}}=\frac{W}{Q_H+E_{\text{ath}}},
  \quad \eta_C = 1-\frac{T_C}{T_H}.
  ]
* Axioms gates: symmetry residuals (Noether drifts), entropy monotonicity for (M), locality checks for J‑only cone. 

**Defaults and ranges.** Thermal parameters and seeds adopt the project’s single‑source constants where applicable (e.g., seeds, CFL‑style constraints for stability in PDE legs). 

**Software gates (Clean Architecture).** ≤500 LOC/file; layered directories; repository interfaces; tests mirror source; business logic framework‑free; constructor injection for cross‑layer calls; code/artifacts under `<SRC_ROOT>/` and `tests/`.

### 5.1.1 Pre‑Run Config Requirements

**APPROVALS.json (sketch):**

```json
{
  "preflight_name": "vdm_qre_preflight",
  "description": "Approval manifest: preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Only RESULTS_* after a matching PROPOSAL_* exists and is approved.",
  "pre_registered": true,
  "proposal": "Derivation/quantum/T4_PROPOSAL_QRE_Metriplectic_Ledger.md",
  "allowed_tags": ["qre-v1.0"],
  "schema_dir": "Derivation/code/physics/quantum/schemas",
  "approvals": {
    "qre-v1.0": {
      "schema": "Derivation/code/physics/quantum/schemas/qre.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto-ts",
      "approval_key": "auto-hash"
    }
  }
}
```

**PRE‑REGISTRATION.json (minimum):**

```json
{
  "proposal_title": "Quantum-Resource Engine: Metriplectic Ledger",
  "tier_grade": "T4",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id": "H1", "statement": "With E_ath>0, median η_heat/η_C ≥ 1.05", "direction": "increase"},
    {"id": "H2", "statement": "η_gen ≤ 1 with 95% CI", "direction": "no-change"}
  ],
  "variables": {
    "independent": ["T_H/T_C", "χ (r or I)", "coupling ratios"],
    "dependent": ["η_heat/η_C", "η_gen", "entropy production", "Noether drift"],
    "controls": ["domain size", "precision", "time step", "seeds"]
  },
  "pass_fail": [
    {"metric":"Axiom-EntropyDrift","operator":"<=","threshold":0,"unit":""},
    {"metric":"Noether-Drift-per-period","operator":"<=","threshold":1e-8,"unit":""},
    {"metric":"Median(η_heat/η_C) at χ≥χ*","operator":">=","threshold":1.05,"unit":""},
    {"metric":"CI95(η_gen)-1","operator":"<=","threshold":0,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/quantum/qre.v1.json"],
  "registration_timestamp": "auto-ISO8601"
}
```

**Specs and schema** follow the canonical structure in the template; full versions will be checked into the repo with the approved tag before RESULTS runs.

---

## 5.2 Experimental Runplan

1. **Instrument calibration (χ=0):** Run the engine with thermal baths only; require (\eta_{\text{heat}}\le \eta_C) within **2%** across (N\ge 16) seeds; entropy monotone on (M)‑only; Noether drifts (\le 10^{-8}) per period on (J)‑only. (Gate **G‑1 Baseline**). 
2. **Resource sweep (χ>0):** Enable athermal input via (a) squeezing parameter (r) **or** (b) initial mutual information (I). Sweep (\chi) over ≥6 levels; estimate median (\eta_{\text{heat}}/\eta_C) with bootstrap CI (5k). (Gate **G‑2 Apparent boost** ≥ **1.05** with CI not crossing 1).
3. **Generalized‑law audit:** Compute (\eta_{\text{gen}}=W/(Q_H+E_{\text{ath}})) with two independent estimators for (E_{\text{ath}}). Require median (\eta_{\text{gen}}\le 1) and per‑run residuals centered at 0 with no positive drift (p>0.1). (Gate **G‑3 Law compliance**).
4. **Null demolitions:** Repeat step 2 with the same numerics but (\chi!\to!0); the boost must vanish within error (A/B control).
5. **Locality & scaling:** For J‑leg pulses, confirm finite domain‑of‑dependence and report collapse in the chosen dimensionless groups. (Gate **G‑4 Locality/scale**). 
6. **Artifact posting:** For each figure, publish CSV/JSON (same basename), seed list, and commit in caption; post pass/fail JSON and CONTRADICTION_REPORT on any gate failure.

> **Note on runtime:** wall‑clock is **measured and logged** (systemspecs); it is **not** a scientific gate. Hardware is AMD/ROCm by default; no CUDA/NVIDIA is assumed.

---

## 6. Research Question (falsifiable)

**Question.** *When athermal order is supplied as a priced resource, do VDM’s meters report (\eta_{\text{heat}}>\eta_C) while (\eta_{\text{gen}}\le 1) and all axiom‑level gates pass?*

**Independent variables.** (\Pi_1=T_C/T_H \in [0.1,0.8]); (\Pi_2=\chi) (squeezing (r\in[0,1]) or mutual‑information (I\in[0,1]) bits); coupling ratios (\in{0.2,0.5,0.8}); seeds (\ge 16).

**Dependent variables.** (\eta_{\text{heat}}/\eta_C), (\eta_{\text{gen}}), entropy production, Noether drift. Estimation via multi‑seed bootstrap, discrete energy/flux ledgers, and information‑proxy pricing. **Thresholds** as in G‑1..G‑3 above.

**Dimensionless program (A6).** (\Pi_1=T_C/T_H,\ \Pi_2=E_{\text{ath}}/Q_H,\ \Pi_3)=coupling ratio,\ \Pi_4)=cycle Péclet. Predict (\partial(\eta_{\text{heat}}/\eta_C)/\partial\Pi_2>0), monotone in (\Pi_2). 

---

## 7. Variables & Controls

| Class       | Name                                   | Definition                  | Control / Range                            |
| ----------- | -------------------------------------- | --------------------------- | ------------------------------------------ |
| Independent | (\Pi_1)                                | (T_C/T_H)                   | ([0.1,0.8])                                |
| Independent | (\Pi_2)                                | athermal strength (\chi)    | (r\in[0,1]) or (I\in[0,1])                 |
| Independent | Coupling                               | bath & inter‑mode ratios    | ({0.2,0.5,0.8})                            |
| Dependent   | (\eta_{\text{heat}},\eta_{\text{gen}}) | efficiencies                | computed per run                           |
| Dependent   | Entropy prod.                          | (M)-leg (\Delta\Sigma\ge 0) | per step monotone                          |
| Dependent   | Noether drift                          | energy/momentum drift       | (\le 10^{-8}) per period                   |
| Control     | Time step / grid                       | integrator stability        | CFL‑like safety (\le 0.2) where applicable |
| Control     | Seeds                                  | RNG                         | (\ge 16); default 42 for baselines         |

Uncertainty is reported via bootstrap CI and two‑resolution checks; specification/tests adhere to the project’s data science rules for valid inference and documentation. 

---

## 8. Equipment / Hardware

* **Compute**: AMD/ROCm stack; BLAS/LAPACK per environment file.
* **Reproducibility**: `systemspecs` snapshot; seeds/commit logged; fp64 primary; tolerances recorded.
* **Integrity**: layered repo; tests mirror source; interfaces isolate outer/inner deps; ≤500 LOC/file.

---

## 9. Methods / Procedure (narrative)

1. **Equations & discretization.** Implement a metriplectic split consistent with A4: J‑leg reversible Hamiltonian for the coupled oscillators + ancilla; M‑leg Lindblad/collision‑style dissipator for thermalization, constructed to ensure (\Delta\Sigma\ge 0) (H‑theorem) and (J,\delta\Sigma=0), (M,\delta\mathcal I=0). Degeneracy guards (g_1,g_2) are logged each (K) steps. 
2. **ICs/BCs & parameters.** Initialize WM modes at specified energies; baths at (T_H,T_C); set (\chi) per spec.
3. **Solvers.** Strang‑like operator splitting; J‑only reversibility test; M‑only entropy monotonicity check; two‑resolution consistency.
4. **Post‑processing.** Energy budget → ((Q_H,Q_C,W)); resource pricing → (E_{\text{ath}}) via dual estimators; compute (\eta) metrics, bootstrap CI; plot per‑figure CSV/JSON with seed+commit in captions.
5. **Security/ethics.** No external data; compute cost/carbon logged; licenses respected.

All mathematical claims are presented with tiny lemmas and explicit gates; proof‑analysis and counterexample hygiene adhere to the project’s rigorous math and logic rules and to the compendium of scientific/technical principles (sampling, filters, numerical stability) used in diagnostics.   

---

## 10. Entire Formal Derivation Writeup (sketch of key invariants)

* **Axiom‑level lemma (degeneracy):** For the implemented split, ( \langle J,\delta\Sigma, \delta\Sigma\rangle=0) and (\langle M,\delta\mathcal I, \delta\mathcal I\rangle=0) at machine precision on grid‑refined runs; measured via (g_1,g_2\le 10^{-10}). **Gate:** PASS/FAIL is mechanical. 
* **Entropy lemma (M‑only):** Discrete gradient update yields ( \mathcal L^{n+1}-\mathcal L^n = -\Delta t\lVert(\phi^{n+1}-\phi^n)/\Delta t\rVert_2^2\le 0) in RD‑like tests, validating our dissipative monitor (background QC instrument). 
* **Noether lemma (J‑only):** Energy/flux conservation from translation symmetries yield drifts (\le10^{-8})/period (validated in KG branch, used here as QC diagnostic). 

---

## 11. Results / Data (planned artifact format)

* **Fig. 1 (Calibration):** (\eta_{\text{heat}}/\eta_C) vs. modes for (\chi=0). Caption lists median±CI; **Gate G‑1**.
* **Fig. 2 (Resource sweep):** (\eta_{\text{heat}}/\eta_C) vs. (\chi) showing monotone rise; **Gate G‑2** (≥1.05 with CI).
* **Fig. 3 (Generalized audit):** (\eta_{\text{gen}}) distribution; CI ≤ 1; residuals centered with no positive drift; **Gate G‑3**.
* **Fig. 4 (Axiom checks):** Noether and entropy monitors; degeneracy residuals (g_1,g_2).
  Each figure has matching CSV/JSON basename, seeds, commit in caption. CONTRADICTION_REPORT is emitted automatically on any gate failure.

---

## 12. Discussion / Analysis (planned)

Interpret whether **apparent** >Carnot arises **only** when (E_{\text{ath}}>0) and disappears when priced—aligning with the generalized‑law story; examine sensitivity to bath models (Lindblad vs. collision); analyze numerical artifacts (aliasing, step bias) using the project’s data rules; defend thresholds or tighten them post‑hoc with registered rationale. 

---

## 13. Conclusions

If G‑1..G‑3 pass, the instrument demonstrates that **efficiency limits depend on the resource ledger**: when athermal order is present, the textbook Carnot denominator is the wrong accounting; with pricing included, the generalized second law is unbroken. This supports VDM’s metriplectic separation of **order (J)** and **dissipation (M)** as a faithful computational probe of nanoscale thermodynamics. 

---

## 14. Tier Grade & Provenance Ladder

**This document is T4 (Prereg).** It relies on:

* **T0–T1**: Program axioms A0–A7 and metriplectic formalism. 
* **T2 instruments (validated)**: RD dispersion & Fisher–KPP front speed (artifacted validations referenced in canon). 
* **T3 smoke (internal)**: Split‑leg QC runners (Noether/entropy monitors) used as diagnostics here. 

---

## 15. Risks, Assumptions, Kill‑Plans

* **Resource mis‑accounting** (omitting prep/erase cost). *Kill‑plan:* include prep/erase cycle; require (\eta_{\text{gen}}\le 1) per run.
* **Bath modeling artifacts** (non‑Markovian spoofing). *Kill‑plan:* replicate with alternate bath kernel; require gate stability.
* **Numerical back‑action** (timestep bias injects spurious work). *Kill‑plan:* two‑resolution agreement; J‑only reversibility checks with Noether drifts ≤(10^{-8}).

Methodological discipline and decision‑making follow the project’s objective rules (bets, preregistration, CI‑driven artifacting), and formal logic constraints govern specification and inference.  

---

## 16. Clean‑Architecture Compliance (software gates)

Hierarchical directories; no outer→inner deps; interfaces for cross‑layer calls; business logic framework‑free; domain models plain; repository pattern enforced; tests mirror source; ≤500 LOC/file; imports follow allowed edges; Apps/Domain import no frameworks. **Pass/fail is mechanical** in CI.

---

## 17. References (project canon anchors used)

* **VDM Axioms (A0–A7)** and metriplectic split (master equation; entropy law; scale program; measurability). 
* **VDM Canonical Equations & Procedural Math** (Noether currents, energy flux, RD/KG QC instruments). 
* **VDM Constants & Defaults** (seeds, CFL‑style constraints for PDE QC). 
* **VDM Notation Reference Sheet** (symbols, fluxes, ledger variables). 
* **Rules for Rigorous Mathematical Inquiry & Presentation** (proof/gate discipline). 
* **Rules for Objective Decision‑Making & Truth‑Seeking** (preregistration, pass/fail, bets). 
* **Compendium of Technical & Scientific Principles** (sampling, filters, numerical stability). 
* **Rules distilled from Formal Logic, Set Theory, and Discrete Mathematics** (syntax/semantics for specs & proofs). 
* **Rules for Data Science & Documentation** (valid inference after selection; bootstrap; artifacting). 
* **Rules for Causal Systems…** (system individuation; intervention conditions; locality). 
* **White Paper Proposal Template** (this document’s structure/gates).

---

### Posting note (operational habit)

Open with a TL;DR and one artifact path; include at least one boxed gate; end by inviting threshold tightening with reruns posted. This proposal adheres to the RESULTS/PROPOSAL authoring policy.

---

**Classification:** *Axiom‑core → Derived‑limit.*
**Objective recap:** **Show** that when athermal order is supplied and accounted, the meter reports (\eta_{\text{heat}}>\eta_C) but **(\eta_{\text{gen}}\le1)** and all axiom gates pass.
**Next steps:** land PRE‑REGISTRATION.json; check in schema/specs; run G‑1 baseline; A/B resource sweep; post artifacts + pass/fail JSON; open CONTRADICTION_REPORT if any gate fails.
