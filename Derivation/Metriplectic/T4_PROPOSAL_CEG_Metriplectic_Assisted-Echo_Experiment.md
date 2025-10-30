# 1. T4 — Counterfactual Echo Gain (CEG): A Metriplectic Assisted‑Echo Experiment in VDM

> **Created Date:**  October 30, 2025
> **Commit**: 80ee5476e4f887fed3c34534a99daa878f55382f  
> **Salted Provenance: spec salted_sha256=b96103661cc6f5b9be1a751581c32e86dcc2fd1613f19d4e6d7168046eb25225; salt_hex=2402d87739d5173cc9b86ee572e68b0b; prereg_manifest_sha256=08f4b3b7829bdd67cdc54d17a706952b046c33b7d560fc71dcb31780f9772c93  
> **Proposer contact(s):**  (<justin@neuroca.ai>)  
> **License:** (See LICENSE at repository root)  
> **Short summary (one sentence TL;DR):**  Test whether a metriplectic, model‑aware assisted‑echo improves echo fidelity under strict Noether/H‑theorem gates and energy‑matching.

**Tier Grade:** T4 (Preregistered claim) — prior support exists at T2 (instrument calibration) and T3 (smoke tests) in the VDM canon (Noether/H‑theorem meters; Strang‑composition QC; scaling‑collapse), with pinned artifacts and logs.

**Date:** 2025‑10‑28

---

## 2. List of proposers and associated institutions/companies

**Justin K. Lietz** — Prometheus VDM (independent research program)

---

## 3. Abstract

VDM (Void Dynamics Model) separates dynamics into a conservative limb (J) and a dissipative limb (M) (metriplectic split). The proposed experiment defines and tests **Counterfactual Echo Gain (CEG)**—the improvement in echo fidelity when a system uses its **internal model** of (J) and (M) to assist the time‑reversal phase, relative to an energy‑matched, model‑blind baseline. The preregistered observable is

$$
\mathrm{CEG} \equiv \frac{E_{\text{baseline}}-E_{\text{assisted}}}{E_{\text{baseline}}} \in [0,1]
$$

with explicit physics gates: **J‑Noether drift** bounded, **M‑monotonicity** (H‑theorem) respected, and **energy‑matching** enforced. Passing requires $\mathrm{median}_{\text{seeds}}(\mathrm{CEG}) \ge 0.05$ without gate violations, across a preregistered grid of step sizes and split compositions. This elevates echoes from calibration demos to a falsifiable claim about **model‑aware self‑correction** under metriplectic dynamics. (Prepared per the white‑paper template and RESULTS standards for artifacts and gates.)  

---

## 4. Background & Scientific Rationale

**Metriplectic core.** VDM enforces two coupled generators on state $q$:

$$
\dot q = J(q)\,\frac{\delta \mathcal{I}}{\delta q} + M(q)\,\frac{\delta \Sigma}{\delta q},\quad J^\top=-J,\; M^\top = M\succeq 0
$$
with degeneracies $J,\,\delta\Sigma/\delta q=0$ and $M,\,\delta\mathcal{I}/\delta q=0$. The $J$ limb preserves invariants (e.g., discrete Hamiltonian), while $M$ increases an entropy/Lyapunov functional $\Sigma$ (discrete H‑theorem). VDM’s existing canon documents meters for these properties and composition‑error scaling under Strang splitting.

**Governing equations used later.** The validated KG/RD branches and conservation‑law diagnostics provide the measurement substrate for the echo tests; e.g., the discrete action and Lagrangian/Euler–Lagrange structure (for $J$), and gradient‑flow RD updates (for $M$). These appear in the EQUATIONS registry used as the computational “instrument manual.”

**Maturity ladder (T0–T9) in brief.** Tiers track evidence maturity and scope: T0 (Concept) articulates ideas and falsifiers; T1 (Proto‑model) implements the first working toy; T2 (Instrument) certifies meters/instruments; T3 (Smoke) demonstrates phenomena with certified instruments; T4–T6 (Preregistered → Pilot → Main) make formal, preregistered claims with increasing sample and scope; T7–T8 (Out‑of‑sample → Robustness) validate forecasts and parameter sweeps; T9 (Reproduction) is external verification. This document is a T4 preregistration, building on existing T2/T3 artifacts (Noether/H‑theorem meters, Strang QC, scaling collapse) and specifying explicit pass/fail gates and machine‑readable configs. Successful passage promotes follow‑on work to T5 (Pilot) and T7/T8 checks.

**Why this experiment now.** Prior VDM work certified the **meters** (T2): J‑only reversibility and Noether drift, M‑only monotonicity, and Strang‑defect slopes; T3 smoke tests showed scaling collapses and routing discipline. The present T4 proposal upgrades echoes from instrument checks to a **phenomenon test**: whether **internal J/M knowledge** can be operationally exploited to improve a reversible‑attempt under dissipation, **without breaking the gates**.

**Novelty & targets.** The novelty is not the echo sequence itself, but the **gate‑bounded, metriplectic assisted‑echo** and its preregistered metric (CEG). Target findings: (i) statistically robust $(\mathrm{CEG}>0)$ under energy‑matched controls; (ii) zero violations of J‑Noether bounds and M‑monotonicity; (iii) sensitivity map (where assistance pays off most).

**Criticisms & responses.**
*Critique:* “Assistance could cheat by injecting energy.” *Response:* energy‑matching gate.
*Critique:* “Improvement may stem from numerics, not physics.” *Response:* instruments are already QC’d (Noether/H‑theorem/Strang), and ablations will scramble the internal model while keeping numerics identical.
*Critique:* “Self‑awareness is metaphysical.” *Response:* the claim here is purely **physical**: model‑aware correction under metriplectic gates.

*Provenance & maturity ladder are documented in template/RESULTS standards used here.*  

---

## 5. Intellectual Merit and Procedure

**Importance.** Establishes a falsifiable competency—**model‑aware self‑correction**—measured under strict conservation/entropy gates.
**Impact.** If validated, metriplectic assisted‑echoes become a general tool for probing agency‑like competencies in field models (far beyond this specific setup).
**Approach & rigor.** Treat the **numerical scheme as the measuring instrument**; pair every claim to a metric and gate; preregister parameters, seeds, and pass/fail thresholds; publish artifacts per RESULTS standards.

### 5.1 Experimental Setup and Diagnostics

**State and splits.** Domain $\Omega\subset\mathbb{R}^d$ (1D/2D) with field $W$ (KG for $J$; RD/gradient‑flow for $M$). Discrete action and updates from EQUATIONS registry; canonical constants from CONSTANTS registry.  

**Integrator.** Strang JMJ (or MJM as control): symplectic step for $J$; discrete‑gradient step for $M$. Diagnostics on each limb are enabled during both forward and reverse phases.

**Primary observable.** Echo error $E \equiv \|q_{\text{final}}-q_0\|_{\mathcal{H}}$ in a declared discrete energy norm $\|\cdot\|_{\mathcal{H}}$ (per VDM discrete Hamiltonian density). CEG as above.

**Gates (physics constraints).**

* **G1 (Noether‑J):** $\max_t \frac{|\Delta \mathcal{I}|}{\mathcal{I}_0} \le 10^{-8}$ (fp64; multi‑seed median).
* **G2 (H‑M):** $\Delta \Sigma \ge -10^{-12}$ per step (tolerance for fp rounding); non‑increasing cumulative $\Sigma$ in M‑only segments.
* **G3 (Energy‑match):** assistance work budget equals baseline work budget within $10^{-4}$ relative.
* **G4 (Composition QC):** Strang defect slope $\beta \in [2.8,3.2]$ on $\Delta t$ log–log fit before running assisted tests.

**Independent variables (preregistered grid).**

* Grid: $N\in\{256,512,1024\}$, $\Delta x=L/N$.
* Time step: $\Delta t\in\{0.5,1,2\}\times \Delta t_\text{CFL}$ (within stable envelope per branch).
* Split order: JMJ vs MJM.
* Assistance strength: $\lambda\in\{0.0,0.1,0.2,0.3\}$ (0.0 = baseline).
* Seeds: $n_{\text{seeds}}\ge 12$ (preregistered list).

**Diagnostics (counts).**

* Noether drift monitor (1), H‑theorem monitor (1), composition‑slope fitter (1), CEG aggregator (1), gate‑ledger (1), light‑cone/dispersion probes (optional, KG J‑health) (2). Artifacts (CSV/JSON/PNG) paired per RESULTS standards.

**New tools/scripts to fabricate.**

* `experiments/metriplectic/assisted_echo.py` (SMAE micro‑sequence during rewind; energy‑budget clamp).
* `metrics/echo_fidelity.py` (norms; CEG computation).
* `gates/echo_gates.py` (G1–G4 JSON pass/fail; contradiction reports on fail).
* `schemas/echo_artifacts.schema.json` (artifact typing).

**Compute environment (declared).** x86_64 Linux, Python 3.11+, NumPy/SciPy/FFT libs; optional ROCm‑accelerated FFT/BLAS on **AMD** GPUs; commit+seed logged for every run; IEEE‑754 fp64.

#### 5.1.1 Pre-Run Config Requirements

* Required config and metadata:
  * Derivation/code/physics/metriplectic/APPROVAL.json
  * Derivation/code/physics/metriplectic/schemas/
    * echo_spec-v1.schema.json
  * Derivation/code/physics/metriplectic/specs/
    * assisted_echo.v1.json

##### APPROVAL.json (excerpt — minimal fields)

```json
[
  {
    "preflight_name": "preflight",
    "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
    "author": "Justin K. Lietz",
    "requires_approval": true,
    "pre_commit_hook": true,
    "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must be created at Derivation/Metriplectic/ and approved."
  },
  {
    "pre_registered": true,
    "proposal": "Derivation/Metriplectic/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md",
    "allowed_tags": [
      "echo_spec-v1"
    ],
    "schema_dir": "Derivation/code/physics/metriplectic/schemas",
    "approvals": {
      "echo_spec-v1": {
        "schema": "Derivation/code/physics/metriplectic/schemas/echo_spec-v1.schema.json",
        "approved_by": "Justin K. Lietz",
        "approved_at": "<auto-generated>",
        "approval_key": "<hashed-key>"
      }
    }
  }
]
```

##### PRE-REGISTRATION.json (minimum required keys)

```json
{
  "proposal_title": "CEG Assisted-Echo",
  "tier_grade": "T4",
  "commit": "80ee5476e4f887fed3c34534a99daa878f55382f",
  "salted_provenance": {
    "schema": "vdm.provenance.salted_hash.v1",
    "generated_utc": "2025-10-30T16:49:47.201492Z",
    "salt_bytes": 16,
    "single_salt": true,
    "salt_hex": "aff7a0cb80e8d430873bc504be978525",
    "items": [
      {
        "path": "Derivation/code/physics/metriplectic/specs/assisted_echo.v1.json",
        "size": 274,
        "base_sha256": "40917004b65550b10dd89dcaeef43df9191ddb2d2f08656bb9c1e37a7372116d",
        "salt_hex": "aff7a0cb80e8d430873bc504be978525",
        "salted_sha256": "7cb47d741d087a65fc5f9eeb73c599904702ba199c101b81ae1954658fc51029"
      }
    ]
  },
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Median CEG >= 0.05 under gates G1–G4.", "direction": "increase" }
  ],
  "variables": {
    "independent": ["N", "dt", "split", "lambda"],
    "dependent": ["CEG"],
    "controls": ["energy_match", "seed"]
  },
  "pass_fail": [
    { "metric": "CEG_median", "operator": ">=", "threshold": 0.05, "unit": "dimensionless" }
  ],
  "spec_refs": ["Derivation/code/physics/metriplectic/specs/assisted_echo.v1.json"],
  "registration_timestamp": "2025-10-30T16:49:47.201492Z"
}
```

##### Specs (assisted_echo.v1.json — minimum keys)

```json
{
  "tag": "assisted-echo-t4-prereg",
  "grid": { "N": 256, "dx": 1.0 },
  "params": { "c": 1.0, "m": 0.5, "D": 1.0, "m_lap_operator": "spectral" },
  "dt": 0.02,
  "steps": 200,
  "seeds": [1,2,3,4,5,6,7,8,9,10,11,12],
  "lambdas": [0.0, 0.1, 0.2, 0.3],
  "budget": 1e-3
}
```

##### Schemas (echo_spec-v1.schema.json — minimum JSON Schema)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:metriplectic:echo_spec-v1",
  "title": "assisted_echo spec schema",
  "type": "object",
  "metadata": { "tag": "echo_spec-v1" },
  "properties": {},
  "required": []
}
```

### 5.2 Experimental runplan

**RP‑1 Baseline calibration (meters).**
Run J‑only reversibility, M‑only monotonicity, and Strang defect slope across the grid; must pass G1–G2–G4 before any assisted runs. (Artifacts posted with same‑basename CSV/JSON and figure captions that include slope/$R^2$ and seed/commit.)

**RP‑2 Assisted‑echo implementation.**
Insert a micro‑sequence during the reverse M‑segment using the internal $M$ estimator, with assistance parameter $\lambda$ and **energy‑match clamp**. Log assistance work, ensure G3.

**RP‑3 Preregistered evaluation.**
For each grid point and seed: forward JMJ → perturb (“walker” pulse) → reverse. Record $E_{\text{baseline}}$ at $\lambda=0$ and $E_{\text{assisted}}$ for $\lambda>0$. Compute CEG and gate statuses.

**RP‑4 Ablations & controls.**
Model‑blind assistance (scramble $M$ map), J‑scramble, M‑scramble, and MJM ordering as controls; same energy budget, same seeds.

**RP‑5 Publication pipeline.**
Prepare **RESULTS_CEG_AssistedEcho.md** with TL;DR, gates, tables, figures with numeric captions, and reproducibility manifests (commit/seed). Emit contradiction reports if any gate fails.

**Runtime scope (non‑temporal specification).**
Total run budget is specified as **(#grid points) × (#seeds) × (# $\lambda$ levels) × (#forward+reverse steps)** with all artifacts retained; RESULTS standards require per‑figure paired CSV/JSON and gate JSON for each run.

**Plan of action (success).**
If $\mathrm{median}_{\text{seeds}}(\mathrm{CEG}) \ge 0.05$ and all gates pass across ≥80% of grid points, promote to T5 (Pilot) with a ridge map of CEG vs ($\lambda$, M‑strength).

**Plan of action (failure).**
If any gate fails, emit **CONTRADICTION_REPORT** (gate, threshold, seed, commit, artifact) and quarantine. If gates pass but $\mathrm{CEG} \le 0$, publish null result; run ablations to bound sensitivity and update assistance design.

**White‑paper conformance.** This document follows the proposal template requirements on structure, equations, gates, provenance; the subsequent RESULTS note will follow the RESULTS standards for figures, numeric captions, and evidence discipline.  

---

## 6. Personnel

**Justin K. Lietz (PI):** designs experiment; implements `assisted_echo.py`, metrics, gates, and artifact schemas; runs preregistered sweeps; authors RESULTS note; maintains provenance (commit/seed/logging) and compliance with artifact/figure pairing.

---

## 7. References

1. **White Paper Proposal Template**, for section structure, narrative discipline, and provenance requirements.
2. **RESULTS Paper Standards**, for figure/CSV pairing, numeric captions, gate JSONs, and contradiction‑reporting norms.
3. **VDM EQUATIONS Registry**, for discrete action/Lagrangian, Euler–Lagrange, and RD/KG update forms used as instruments.
4. **VDM Overview (Canon & Maturity)**, for T2/T3 meters and maturity ladder context (Noether/H‑theorem checks; metriplectic structure gates).
5. **VDM CONSTANTS**, for canonical default parameters used in preregistration (e.g., $D, r, N, L, \text{CFL}$).
6. **Rules for Technical & Scientific Principles**, for treating numerical schemes as instruments and enforcing IEEE‑754 discipline and engineering rigor.

---

## Appendix (informative, minimal)

**Instrument equations referenced in §5.1** (drawn from the EQUATIONS registry):

* Discrete Lagrangian / Euler–Lagrange for the (J) limb (KG branch):
  $$
  \frac{W_i^{n+1}-2W_i^{n}+W_i^{n-1}}{(\Delta t)^2}
  -\kappa \sum_{\mu=1}^d \big(W_{i+\mu}^{n}+W_{i-\mu}^{n}-2W_i^{n}\big)
  + V'(W_i^{n}) = 0,\quad
  \mathcal{L} = \tfrac12 (\partial_t \phi)^2 - \tfrac{\kappa a^2}{2} (\nabla \phi)^2 - V(\phi)
  $$
  (Continuum limit and notation as in the registry.)

**Primary reproducibility note.** All runs will log commit, seed, full parameters, and SHA‑256 checksums for CSV/JSON/PNG artifacts, consistent with VDM’s reproducibility policy.

---

**Compliance statement.** This proposal conforms **exactly** to the mandated sections, length discipline, provenance lines, MathJax equations, explicit **pass/fail gates**, and artifact standards specified by the template and RESULTS policy.  

**Scope reminder.** The claim is **operational and physical** (assisted echoes improve fidelity under metriplectic gates); no metaphysical claims are made.
