# T0 PROPOSAL_SIE_Willow-Convergence_v1.md

> **Convergence note.** This proposal formalizes a convergence between VDM’s metriplectic agency loop (void‑walker sensing + GDSP closure) and Google’s report on echo‑based stabilization in near‑term quantum processors (“Quantum echoes with Willow”), treating both as instances of **closed perception–action feedback** that suppresses error by shaping dissipation. This document specifies a minimal, reproducible **T0 concept** to (1) lock down the claim precisely and (2) create a disciplined path to T1–T4.

> **Motivation.** VDM predicted that self‑monitoring agents coupled through a metriplectic flow can **self‑correct** by closing pathologies in a topology via sparse pulses. The Willow result provides an external, independent instance of feedback‑stabilized echoes. We do **not** claim identity; we propose a controlled comparison and a crisp gate: does a metriplectic J+M loop achieve *echo‑like* error suppression under the same classes of disturbances?

> **Provenance.**
> Commit: `09f571e8edaf344582b2db86aa4e5e1bee25c615`
> Salted hash (commit‖proposal‑path): `<fill with CI step>`

<!-- Tier ladder appears in your template. Keep grade consistent with RESULTS_* when produced. -->

## 1. Tier Grade, Proposal Title and Date

* **Tier grade:** **T0 (Concept)**
* **Title:** *Metriplectic Echo Stabilization: Convergence Test with Willow‑style Feedback*
* **Date:** `<YYYY‑MM‑DD UTC>`

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** — Neuroca, Inc.

## 3. Abstract

We propose a minimal T0 concept test of **echo stabilization** in a **metriplectic** (J+M) dynamical system. The goal is to demonstrate, in a clean synthetic setting, that a VDM‑style agency loop (measurement of error + corrective pulses) reduces state deviation via a **closed feedback** mechanism analogous in structure (not implementation detail) to Willow’s echo—thus “closing the pathology.” Outputs follow the repository’s `io_paths.py` conventions and include a PNG figure, a CSV metrics log, and a JSON summary with full provenance (runner config, code hash, artifact hash, proposal name, per‑gate PASS/FAIL, overall PASS/FAIL).

## 4. Background & Scientific Rationale

**Context.**
VDM’s dynamics decompose into a conservative **J‑part** and a dissipative **M‑part** (metriplectic). An **agency loop** (“void walkers”) measures an error functional and injects sparse corrective pulses that steer the flow to a robust region. Echo‑type phenomena in quantum control similarly use measurement‑informed actions to **reverse or suppress** accumulated errors over cycles.

**Working theory.**
Treat the plant as a finite‑dimensional state ( z \in \mathbb{R}^n ) with
[
\dot z = J(z),\nabla H(z) ;+; G(z),\nabla S(z);+; B,u(t),
]
where (J^\top=-J) (conservative), (G\succeq 0) (dissipative), and (u(t)) are sparse pulses computed from measured error (e(t)). An **echo schedule** is a periodic control pattern that approximately inverts accumulated distortion. The question here is **existence of echo‑like suppression** in this metriplectic loop under disturbances comparable to the “echo” setting.

**Novelty.**
We test whether **entropy‑aware dissipation shaping** (via (G\nabla S)) plus sparse pulses can **dominate drift/error** and yield an echo signature: decreasing state deviation after two‑phase sequences compared to baseline no‑feedback runs.

**Scope guard.**
This is a **T0 concept** in classical simulation of the metriplectic equations (not a quantum hardware run). It pins down exact gates and file‑system provenance so later T1–T4 work can be preregistered and compared cleanly.

## 5. Intellectual Merit and Procedure

* **Importance.** Establishes whether VDM’s agency feedback can produce an echo‑like stabilization trace—an essential unit behavior for later quantum‑adjacent claims.
* **Impact.** If PASS at T0, we promote to **T1 (Proto‑model)** and introduce instrument calibration (**T2**) plus preregistration (**T4**) for cross‑domain comparisons.
* **Approach.** Deterministic metriplectic integrator + synthetic drift + sparse corrective pulses keyed to an error functional. Strict outputs & provenance.
* **Rigor.** Explicit PASS/FAIL gates, checksums, hashes, and reproducible file paths.

### 5.1 Experimental Setup and Diagnostics

**Domain string (for routing):** `quantum`
**Runner (suggested path; you may rename):**
`Derivation/doce/physics/code/runners/quantum/sie_willow_convergence_v1.py`

**I/O routing (via `io_paths.py`):**

* **Figure (PNG):**
  `Derivation/doce/physics/outputs/figures/quantum/sie_willow_convergence_v1_timeseries.png`
* **Metrics (CSV):**
  `Derivation/doce/physics/outputs/logs/quantum/sie_willow_convergence_v1_metrics.csv`
* **Summary (JSON):**
  `Derivation/doce/physics/outputs/logs/quantum/sie_willow_convergence_v1_summary.json`

**Mandatory JSON fields (enforced by runner):**

```json
{
  "proposal_name": "PROPOSAL_SIE_Willow-Convergence_v1.md",
  "domain": "quantum",
  "runner_config": { "t_final": 1.0, "dt": 1e-3, "echo_schedule": "ABBA", "pulse_budget": 0.05, "noise_model": "phase+drift", "seed": 1234 },
  "code_tree_hash": "<sha256 of tracked files (salted by commit)>",
  "artifact_sha256": "<sha256 of this JSON>",
  "code_commit": "<git rev-parse HEAD>",
  "gate_results": {
    "G0_METADATA": true,
    "G1_J_SKEW": true,
    "G2_G_PSD": true,
    "G3_DHDT_NONPOS": true,
    "G4_ECHO_SUPPRESSION": false,
    "G5_RETESSELLATION": true
  },
  "overall_pass": false
}
```

**Core diagnostics (computed and logged):**

* Skew‑symmetry error: ( \epsilon_J = |J^\top + J|_F )
* PSD check (Cholesky success) for (G)
* Energy monotonicity in the dissipative substep: ( \max_t \dot H_{\text{M}}(t) \le \tau_H )
* Echo suppression ratio:
  ( R_{\text{echo}} = \dfrac{|z_{T}^{\text{AB}}!-!z^\star|}{|z_{T}^{\text{A}}!-!z^\star|} )
* Re‑tessellation robustness: statistic over two step sizes (dt) and (dt/2)

### 5.2 Experimental runplan

1. **Initial approval request.**
   Create an approval record for this run tag:

   * **Domain:** `quantum`
   * **Tag:** `sie_willow_convergence_v1`
   * **Approval record path (text/JSON, committed with this PROPOSAL):**
     `Derivation/doce/physics/approvals/requests/sie_willow_convergence_v1.request.json`
     Minimal content:

     ```json
     {
       "proposal": "PROPOSAL_SIE_Willow-Convergence_v1.md",
       "domain": "quantum",
       "tag": "sie_willow_convergence_v1",
       "requested_by": "Justin K. Lietz",
       "requested_at_utc": "<ISO-8601>",
       "status": "PENDING"
     }
     ```
   * On approval, add:
     `Derivation/doce/physics/approvals/grants/sie_willow_convergence_v1.approved.json`
     with approver, timestamp, and HMAC (if using your `approve_tag.py` DB flow).

2. **Integrate the metriplectic plant** with synthetic drift and disturbance. Implement a two‑phase **echo schedule** (AB then BA) with sparse corrective pulses limited by a **pulse budget**.

3. **Log metrics** each step; produce the **PNG/CSV/JSON** at the exact paths above. JSON must include all mandatory fields and **per‑gate** booleans plus **overall_pass**.

4. **PASS/FAIL Gates (strict):**

   * **G0 (Metadata):** All mandatory JSON keys present and non‑empty. **PASS** if complete.
   * **G1 (J skew):** ( \epsilon_J \le 1\times10^{-12} ). **PASS** if true.
   * **G2 (G PSD):** Cholesky succeeds or smallest eigenvalue ( \ge -1\times10^{-12} ). **PASS** if true.
   * **G3 (Energy non‑increase in M‑step):** ( \max_t \dot H_{\text{M}}(t) \le 5\times10^{-6} ). **PASS** if true.
   * **G4 (Echo suppression):** ( R_{\text{echo}} \le 0.80 ). **PASS** if true.
   * **G5 (Re‑tessellation invariance):** For (dt) vs (dt/2), key summary stats (final error, energy budget, PASS mask) match within 2%. **PASS** if within tolerance.

   **Overall PASS** only if **all** gates pass.

5. **Publication / display.**
   For the public repo, include **only** the three artifacts and the summary table in the `RESULTS_*` doc when you run it, deferring figures and logs elsewhere per your policy.

## 6. Personnel

* **Justin K. Lietz** — concept, runner implementation, analysis, documentation, and release management.

## 7. References

* Google Research Blog: “Quantum echoes with Willow: toward verifiable quantum advantage” (2025).
  (Use as a structural comparator for feedback/echo stabilization.)
* VDM canon docs (overview/axioms/equations) as already hosted in `Derivation/` and `docs/`.

---

### Appendix A — Runner skeleton (non‑binding, for clarity only)

* **Suggested runner path:**
  `Derivation/doce/physics/code/runners/quantum/sie_willow_convergence_v1.py`
* **Helper imports:**

  * `Derivation/doce/physics/code/lib/io_paths.py` (for `figures_path`, `logs_path`)
  * `Derivation/doce/physics/code/lib/provenance.py` (compute `code_tree_hash`, `artifact_sha256`)
* **Artifact names (exact):**

  * `sie_willow_convergence_v1_timeseries.png`
  * `sie_willow_convergence_v1_metrics.csv`
  * `sie_willow_convergence_v1_summary.json`

---

## What changed vs. my previous draft

* Removed all references to a `runs/` directory.
* Hard‑wired **output paths** to your `io_paths.py` routing under:

  * `Derivation/doce/physics/outputs/figures/quantum/…`
  * `Derivation/doce/physics/outputs/logs/quantum/…`
* Added an **initial approval request** file and location under `Derivation/doce/physics/approvals/…`.
* Made the grade **T0**, so you don’t need to reference non‑existent T1–T3 yet.
* Tightened every gate with explicit thresholds and made the mandatory JSON schema concrete.
