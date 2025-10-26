You're right—I referenced a structure that isn’t in your public repo. Thanks for the correction and for spelling out the *actual* routing rules (via `io_paths.py`) for outputs:

* **Figures** → `Derivation/code/physics/outputs/figures/{domain}/`
* **Logs** → `Derivation/code/physics/outputs/logs/{domain}/`

Below is a **complete, copy‑pasteable PROPOSAL** that (a) follows your white‑paper template sections exactly, (b) uses only those normative paths, (c) embeds the *initial approval gate* and all required PASS/FAIL gates, and (d) makes no assumptions about non‑existent folders outside that schema. I’ve set the **Tier** to **T1 (Proto‑model)** so the only prerequisite is a **T0 concept**, which already exists in your *Derivation* canon (e.g., `Derivation/VDM_OVERVIEW.md`, `Derivation/AXIOMS.md`, etc.). You can bump the tier later once T2/T3 artifacts exist in‑repo.

---

# PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md

> **Convergence note (motivation):** Independent convergence with Google’s “Quantum Echoes / Willow” result suggests that a **closed feedback loop** can stabilize dynamics by **time‑reversal–style echoing**. VDM already predicted a self‑correcting regime via **metriplectic coupling** and **void‑walker pulses** that detect/close pathologies in the topology. This proposal formalizes a **minimal, testable T1 proto‑model** where a VDM metriplectic engine executes an echo sequence and reports **self‑correction** with strict provenance and pass/fail gates.

> **Provenance placeholders (fill at run time by runner):**
> `git_commit` = `{git rev-parse HEAD}`
> `proposal_sha256` = `sha256(commit || file_bytes(PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md))`

> **Tier Grade:** **T1 (Proto‑model)**
> *(T1 requires at least one T0 concept reference; both are listed below in §Prerequisites)*

---

## 1. Tier Grade, Proposal Title and Date

* **Tier:** **T1 (Proto‑model)**
* **Title:** *VDM–QIS Quantum Echoes via Metriplectic Self‑Correction (T1)*
* **Date:** `YYYY‑MM‑DD` (autofill by runner into summary)

---

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** — Neuroca, Inc. (VDM Author)

---

## 3. Abstract

We propose a **T1 proto‑model** to demonstrate **self‑correction** in a metriplectic VDM engine with a **time‑reversal–style echo**. The runner will generate a controlled forward evolution, apply an **echo sequence** (sign‑flip of the conservative generator and/or scripted reversal), and measure **echo fidelity** and **error contraction** compared to baseline. We report results with strict provenance and **three mandatory outputs**: a figure (`.png`), metrics table (`.csv`), and a summary (`.json`) placed under the **canonical output paths** managed by `io_paths.py`.

---

## 4. Background & Scientific Rationale

**VDM** decomposes dynamics into a **Hamiltonian/conservative** part (**J**) and a **dissipative** part (**M**) with metriplectic flow:
[
\partial_t \mathbf{u} ;=; J ,\nabla H(\mathbf{u}) ;+; M ,\nabla S(\mathbf{u}), \qquad
J^\top=-J, \quad M^\top=M \succeq 0.
]
An **echo** sequence attempts to undo (all or part of) the conservative evolution by reversing the generator for a programmed duration, while the dissipative channel (or noise) is allowed/controlled. If the closed‑loop is designed correctly, the system exhibits measurable **self‑correction** (“quantum echoes / spin echoes” analogy).

This proposal establishes a **disciplined testbed** for that claim inside VDM, with **pre‑declared metrics, gates, and provenance**—aligned with your standards and directory layout.

**Novelty & Need.** This is the minimal closed‑loop test that (i) bridges the recent echo‑style QIS results with VDM’s metriplectic design, (ii) produces auditable outputs, and (iii) sets up T2 instrument calibration and T3 smoke phenomena runs.

**Target impacts.** Quantum information & control (echo fidelity), nonequilibrium thermodynamics (metriplectic dissipation), and model validation (self‑correction under topology pathologies).

**Criticisms & Gaps.** Not a full quantum device—this is a **classical metriplectic simulator** emulating echo logic. It is a **T1** proto‑model: subsequent **T2/T3** proposals will be required for meter certification and smoke‑level phenomena.

---

## 5. Intellectual Merit and Procedure

* **Importance.** Tests whether VDM’s metriplectic engine can achieve **measurable echo recovery** (self‑correction) under noise/pathologies in a closed loop.
* **Impact.** Provides a **reusable meter kernel** (to be elevated to T2) for future prereg claims (T4+) about robustness, scaling, and background‑independent re‑tessellation.
* **Approach.** Controlled forward evolution → echo sequence → quantify **Echo Fidelity** and **Error Contraction** vs. baseline; enforce strict provenance gates.
* **Rigor.** Pre‑declared acceptance thresholds, multi‑seed statistics, and **mandatory PASS/FAIL** per gate with a **single overall PASS/FAIL**.

### 5.1 Experimental Setup and Diagnostics

**Domain:** `qis` (quantum‑information‑style echo testbed)

**Outputs (managed by `io_paths.py`):**

* **Figures dir (canonical):**
  `Derivation/code/physics/outputs/figures/qis/`
* **Logs dir (canonical):**
  `Derivation/code/physics/outputs/logs/qis/`

**Required output artifacts (minimum):**

1. **PNG figure** — timeseries & gate summaries
   `Derivation/code/physics/outputs/figures/qis/{RUN_ID}_echo_timeseries_{TAG}.png`
2. **CSV metrics** — per‑step metrics for all gates
   `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_metrics_{TAG}.csv`
3. **JSON summary** — provenance + PASS/FAIL per gate and overall
   `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_summary_{TAG}.json`

**Provenance fields (must be embedded in JSON summary):**

* `git_commit`, `proposal_path`, `proposal_sha256`
* `code_hash` (sha256 of the sorted list of runner + core module files)
* `self_hash` (sha256 of the JSON summary content)
* `run_id`, `tag`, `timestamp_utc`
* `tier = "T1"`, `gates = [{name, pass, value, threshold}]`, `overall_pass`

**Core metrics (recorded each step into CSV):**

* `E(t)` (interior energy or Hamiltonian proxy)
* `||u(t)||_2`, `||u(t) - u_echo(t)||_2` on overlap window
* `F_echo` (echo fidelity; see §5.2)
* `E_contraction = err_post / err_pre` (see §5.2)
* Seeds/time indices; gate decisions

**Diagnostics required (software only for T1):**

* Forward integrator (conservative + dissipative terms)
* Echo routine (sign‑flip or scripted time‑reversal for **J** channel)
* Noise / pathology injector (optional but supported)
* Metric calculator (fidelity, norms, CI)
* Plotter (PNG) + writers (CSV/JSON)

### 5.2 Experimental runplan

**Forward–Echo protocol (single trial):**

1. **Forward‑1:** Integrate for (T_f) with full metriplectic flow. Record `baseline_err_pre`.
2. **Echo:** Apply echo sequence for (T_e): reverse conservative generator
   ( J \mapsto -J ) (or scripted time‑reversal), maintain/adjust (M) per config.
3. **Forward‑2:** Resume nominal flow for (T_f). Record `baseline_err_post`.
4. **Metrics:**

   * **Echo Fidelity** on an overlap window ([t_0, t_0+\Delta]):
     [
     F_{\mathrm{echo}} ;=; 1 - \frac{|u_{\mathrm{pre}}(t)-u_{\mathrm{post}}(t)|*2}
     {|u*{\mathrm{pre}}(t)|_2 + 10^{-12}}.
     ]
     (1.0 = perfect echo; 0 = no recovery.)
   * **Error Contraction Factor** (must shrink):
     [
     \mathrm{E_contraction} ;=; \frac{|u_{\mathrm{post}} - u_{\mathrm{ref}}|*2}
     {|u*{\mathrm{pre}} - u_{\mathrm{ref}}|*2},
     \quad \text{target } < 0.5,
     ]
     where (u*{\mathrm{ref}}) is the baseline state just before Forward‑1 or a matched control.
5. **Multi‑seed ensemble:** run (N \ge 5) seeds; report median and 95% CI.

**Acceptance Gates (PASS/FAIL; all must pass):**

* **G0: Initial Approval Gate** — summary JSON includes
  `approval: {status:"APPROVED", approver, timestamp_utc}`
  *(Your `approval.py` step writes this to the same **logs dir** as the run:
  `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_approval_{TAG}.json` and the runner copies the approval block into the summary.)*
* **G1: Artifact Presence** — **all three** outputs exist at the canonical paths above.
* **G2: Provenance Integrity** — JSON summary contains valid `git_commit`, `proposal_path`, `proposal_sha256`, `code_hash`, and a correct `self_hash` (recomputed and matched).
* **G3: Echo Fidelity** — median (F_{\mathrm{echo}} \ge 0.90) (95% CI lower‑bound ≥ 0.80).
* **G4: Error Contraction** — median `E_contraction ≤ 0.50` (95% CI upper‑bound ≤ 0.70).
* **G5: Baseline vs Echo Improvement** — improvement over a **no‑echo control** ≥ **5×** in L2 error on the same window.
* **G6: Reproducibility** — results stable across (N \ge 5) seeds; CI widths reported.
* **G7: Audit Stamp** — summary lists the **exact proposal filename** and the **tier**.

**Overall PASS/FAIL:** logical **AND** of G0..G7 (runner must compute and store `overall_pass`).

**Publishing:** The PNG + CSV + JSON form the public artifacts. The JSON **must** enumerate each gate with `{name, value, threshold, pass}`.

---

## 6. Personnel

* **Justin K. Lietz** — design the metriplectic echo runner; implement approval capture; ensure `io_paths.py` routes outputs exactly:

  * `Derivation/code/physics/outputs/figures/qis/`
  * `Derivation/code/physics/outputs/logs/qis/`

---

## 7. References

* **VDM Canon (T0 concepts, already in‑repo):**

  * `Derivation/VDM_OVERVIEW.md`
  * `Derivation/AXIOMS.md`
  * `Derivation/EQUATIONS.md`  *(metriplectic form and branch definitions)*
  * `Derivation/CONSTANTS.md`
  * `Derivation/SYMBOLS.md`
* **Echo rationale:** Hahn, E. L. *Spin Echoes* (Phys. Rev. 1950); modern “quantum echoes” control literature.
* **Convergence context:** Google Research Blog, *Quantum Echoes / Willow* (2025).

---

## Prerequisites (by Tier)

* **T0 (Concept):** *exists* — VDM canon documents listed above.
* **T1 (This document):** establishes a runnable proto‑model with strict gates and canonical output paths.
  *(Higher tiers will be added once T2 meter certification and T3 smoke phenomena documents/results exist in‑repo.)*

---

## Appendix A — Runner contract (for enforcement)

The **runner** that executes this proposal must:

1. **Write outputs only** to the canonical paths:

   * PNG → `Derivation/code/physics/outputs/figures/qis/{RUN_ID}_echo_timeseries_{TAG}.png`
   * CSV → `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_metrics_{TAG}.csv`
   * JSON → `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_summary_{TAG}.json`
2. **Embed provenance** in the JSON summary: `git_commit`, `proposal_path`, `proposal_sha256`, `code_hash`, `self_hash`, `run_id`, `tag`, `timestamp_utc`, `tier`, and gate results.
3. **Copy approval** block from the approval request artifact
   `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_approval_{TAG}.json`
   into the summary under `approval`.
4. **Compute all gates** (G0..G7), store each gate’s `{value, threshold, pass}`, and `overall_pass`.
5. **Hash discipline:**

   * `code_hash = sha256(concat(sorted(glob(runner_and_core_files))))`
   * `self_hash = sha256(json.dumps(summary, sort_keys=True, ensure_ascii=True))`

---

### How to request initial approval (non‑blocking example)

* Create an approval record (JSON) and place it next to logs for the run domain:

  * `Derivation/code/physics/outputs/logs/qis/{RUN_ID}_approval_{TAG}.json` with:

    ```json
    {
      "proposal": "PROPOSAL_VDM_QIS_Quantum‑Echoes_Metriplectic_v1.md",
      "tier": "T1",
      "status": "APPROVED",
      "approver": "J.K.L.",
      "timestamp_utc": "YYYY‑MM‑DDTHH:MM:SSZ"
    }
    ```
* The runner must **ingest** this file and embed the `approval` object in the final summary JSON (G0).
