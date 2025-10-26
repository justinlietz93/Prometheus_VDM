You’re right—my previous document was the **T0 (Concept)**. Below is the **T1 (Proto‑model)** proposal, structured for your repository and enforcement rules. It conforms to your white‑paper template and results documentation standards (provenance header, tier grade, approval block, explicit output paths, gates, and JSON schema).  

> **Intended repo path**
> `Derivation/doce/physics/proposals/PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_T1_Proto-model_v1.md`

---

<!-- ATTENTION! The proposal documents you create MUST BE whitepaper-grade documents with full structure, full narrative, MathJax-rendered equations ($ ... $ and $$ ... $$), numeric figure captions tied to actual artifacts if using any for background, explicit thresholds with pass/fail gates, and provenance. Imagine this is being submitted to a top physics journal. -->

> `{git rev-parse HEAD}` → **{TO_BE_FILLED_AT_RUN}**
> `salted_proposal_hash(commit ⊕ file_bytes)` → **{TO_BE_FILLED_AT_RUN}**

<!-- Tier Grades
- T0 (Concept) • T1 (Proto-model) • T2 (Instrument) • T3 (Smoke)
- T4 (Prereg) • T5 (Pilot) • T6 (Main Result) • T7 (Out-of-sample)
- T8 (Robustness) • T9 (External reproduction)
-->

# 1. Tier Grade, Proposal Title and Date

* **Tier:** **T1 (Proto‑model)**
* **Title:** **VDM J‑branch QFT Bootstrap & Metriplectic Decoherence — T1 (Scalar Proto‑model)**
* **Date:** {YYYY‑MM‑DD}

# 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** — Prometheus VDM / Neuroca (Independent R&D)

# 3. Abstract

This T1 establishes a CPU‑deterministic **scalar J‑branch** engine on periodic lattices and validates it against textbook dispersion and conservation diagnostics. It is the first runnable instrument toward the VDM QFT bootstrap: free Klein–Gordon (KG) dynamics, spectral dispersion recovery, approximate equal‑time commutator proxy, and energy drift bounds. All runs must emit the required **PNG/CSV/JSON** artifacts with full provenance (commit, salted proposal hash, code‑hash list, runner config, per‑gate PASS/FAIL, overall verdict). Successful T1 (G0–G3) escalates to **T2** where Dirac/staggered–Wilson and metriplectic decoherence are added.

# 4. Background & Scientific Rationale

VDM separates dynamics into a conservative **J‑branch** (wave/quantum‑like) and a dissipative **M‑branch** (entropy/decoherence). At T1 we implement only J: the free scalar field with lattice discretization of the KG equation, validating numerical integrity before adding fermions and metriplectic coupling at T2.

The continuous target is
$$
\partial_t^2 \phi - \nabla^2 \phi + m^2\phi = 0,
$$
with analytic lattice dispersion
$$
\omega^2(\mathbf{k}) = m^2 + \sum_{i=1}^d \frac{4}{a^2}\sin^2!\Big(\frac{k_i a}{2}\Big).
$$

**Ladder provenance & prerequisites.** This T1 depends on the prior conceptual program laid out in the T0 file:

* **Prerequisite (T0):**
  `Derivation/doce/physics/proposals/PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md`
  *(Defines the overall J→Dirac plan and metriplectic role; sets the full gate suite G0–G7.)*

# 5. Intellectual Merit and Procedure

**Importance.** A validated J‑branch scalar engine is the minimal instrument for the VDM QFT bootstrap and a prerequisite for any fermionic or decoherence claims.
**Impact.** Provides a checkable, CPU‑only baseline with strict dispersion/energy/commutator gates.
**Approach.** Finite‑difference time integration with periodic boundaries; spectral estimators for $\omega(k)$; deterministic seeding; strict artifact/provenance discipline.

## 5.1 Experimental Setup and Diagnostics

**Domain routing (enforced by `io_paths.py`):**

* Figures (PNG): `Derivation/doce/physics/outputs/figures/quantum/`
* Logs (CSV/JSON): `Derivation/doce/physics/outputs/logs/quantum/`

**Minimum artifact set per run (mandatory):**

1. `*.png` dashboard, 2) `*_metrics.csv`, 3) `*_summary.json` containing: commit, salted proposal hash, **code_hashes[]**, proposal name, runner config, gate verdicts, overall PASS/FAIL.

**Planned basenames (tag = `qft-metro-T1-v1`):**

* `Derivation/doce/physics/outputs/figures/quantum/2025_qft-metro-T1-v1_dashboard.png`
* `Derivation/doce/physics/outputs/logs/quantum/2025_qft-metro-T1-v1_metrics.csv`
* `Derivation/doce/physics/outputs/logs/quantum/2025_qft-metro-T1-v1_summary.json`

**State & numerics.**

* Lattice: $d \in {1,2}$, size $N=256\text{–}1024$ per side, spacing $a$.
* KG update via leapfrog or Verlet; $\Delta t$ chosen within CFL‑like stability band.
* Initial conditions: localized Gaussian packet(s) with wavenumber windows to sample a set of discrete $\mathbf{k}$.
* Diagnostics:

  * **Dispersion estimator**: fit $\omega(k)$ from Fourier time series peaks.
  * **Energy drift**: total energy $E(t)$ from discrete Hamiltonian; report relative drift.
  * **Equal‑time commutator proxy**: discrete correlator metric approximating $\langle[\phi,\pi]\rangle$ (dimensionless, defined in JSON schema).
  * **Scaling checks**: $(a,\Delta t)$ refinement for stability of metrics.

**Tooling.** Python (NumPy or JAX‑CPU), no GPUs. Reproducible seeds; single‑thread acceptable.

## 5.2 Experimental runplan

1. Generate ICs across 5 seeds and two lattice sizes (e.g., $N=256,512$) with fixed $m$ and three $\Delta t$ values.
2. Evolve to $T$ covering $\gtrsim!40$ periods of the lowest‑$k$ mode.
3. Estimate $\omega(k)$ on the lowest 60% of resolvable modes; fit to analytic lattice KG.
4. Record $E(t)$ and the commutator proxy metric each step.
5. Emit PNG/CSV/JSON artifacts to the paths above.

**Runtime.** $\leq$ 10 minutes per configuration on a modern CPU.
**Success path.** If all **G0–G3** pass (below), this T1 is **PASS** and escalates to T2.
**Failure path.** Any gate failure writes an ERRATA note in JSON and prompts a T1‑ERRATA doc (same path prefix, `_ERRATA.md`) summarizing counterexample slices.

# 6. Personnel

* **Justin K. Lietz** — design, implementation, analysis, documentation, publication workflow.

# 7. References

* Kogut & Susskind, *Hamiltonian Formulation of Wilson’s Lattice Gauge Theories*, Phys. Rev. D **11** (1975).
* P. J. Morrison, *A Paradigm for Joined Hamiltonian and Dissipative Systems* (metriplectic).
* Standard texts on numerical Hamiltonian wave equations and lattice dispersion analysis.

---

## PASS/FAIL Gates for T1 (recorded in `_summary.json`)

**G0 — Provenance integrity**
JSON must include: `commit_hash`, `salted_proposal_hash`, `code_hashes[]`, `proposal_name`, `runner_config`, `gates[]`, `overall_result`. **PASS** iff all present & non‑empty.

**G1 — Scalar dispersion accuracy (J‑only)**
Fit $\omega(k)$ to analytic lattice KG on lowest 60% of modes. **PASS** iff $R^2 \ge 0.995$ **and** MAPE $\le 1.5%$.

**G2 — Energy conservation (J‑only)**
Total energy drift: $\max_t |E(t)-E(0)|/E(0) \le 0.1%$. **PASS** iff bound holds.

**G3 — Equal‑time commutator proxy (scalar)**
Dimensionless proxy metric $\le 0.05$. **PASS** iff bound holds.

**Overall PASS (T1):** G0–G3 all PASS.

---

## Initial Approval Request (for this T1)

* **Approval tag:** `qft-metro-T1-v1`
* **Requester:** Justin K. Lietz
* **Compute/time budget:** CPU only; $\le$ 2 hours aggregate for all seeds/sizes.
* **Data management:** Artifacts to the domain paths listed; no external data.
* **Exit criteria to escalate to T2:** G0–G3 PASS on two lattice sizes and a reproducibility re‑run (new seed) within ±1% metric drift.

---

### Appendix — JSON summary schema (to be emitted by the runner)

```json
{
  "proposal_name": "PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_T1_Proto-model_v1.md",
  "tag": "qft-metro-T1-v1",
  "commit_hash": "<filled_at_run>",
  "salted_proposal_hash": "<filled_at_run>",
  "code_hashes": ["<sha256(file1)>", "<sha256(file2)>"],
  "runner_config": {
    "dim": 1,
    "lattice": [512],
    "a": 1.0,
    "dt": 0.01,
    "mass": 0.2,
    "scheme": "leapfrog",
    "seeds": [101,102,103,104,105]
  },
  "metrics": {
    "dispersion_R2": 0.0,
    "dispersion_mape_pct": 0.0,
    "energy_drift_pct": 0.0,
    "commutator_metric": 0.0
  },
  "gates": [
    {"id":"G0","pass":true,"note":""},
    {"id":"G1","pass":true,"note":""},
    {"id":"G2","pass":true,"note":""},
    {"id":"G3","pass":true,"note":""}
  ],
  "overall_result": "PASS|FAIL",
  "errata": ""
}
```

---

### Cross‑tier links (prereqs and next step)

* **Prerequisite (T0) — must exist in repo before running this T1:**
  `Derivation/doce/physics/proposals/PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md`
* **Next (T2) target if T1 passes:**
  `Derivation/doce/physics/proposals/PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_T2_Instrument_v1.md`
  *(Adds staggered/Wilson Dirac and metriplectic/Lindblad coupling with additional gates G4–G7.)*

---

**How to use this immediately**

1. Paste this file at the indicated path.
2. Ensure the T0 file is present at its path.
3. Kick the runner with `tag=qft-metro-T1-v1`; it should emit the PNG/CSV/JSON into the `.../outputs/figures/quantum` and `.../outputs/logs/quantum` directories using the exact basenames above.
4. The JSON must include the commit and salted proposal hash; the code that executed should populate `code_hashes[]` with SHA‑256 of all imported modules used in the run.

If you’d like, I can now generate the **T2 (Instrument)** proposal with Dirac/staggered–Wilson and metriplectic gates, using the same path discipline and approval block.
