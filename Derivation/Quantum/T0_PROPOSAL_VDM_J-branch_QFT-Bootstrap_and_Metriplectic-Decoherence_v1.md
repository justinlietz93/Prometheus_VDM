# **PROPOSAL — VDM J‑branch QFT Bootstrap & Metriplectic Decoherence (v1)**

**Convergence note.** This proposal supersedes *PROPOSAL_VDM_Particle-triad_Analogy_v1.md*. The triad analogy is retired as a research driver. The new objective is principled: (i) bootstrap the **J‑branch** as a lattice QFT engine (free scalar → Dirac), (ii) introduce **M‑branch** only as metriplectic/Lindblad‑like decoherence, and (iii) define quantitative gates for scale‑up toward quantum‑gravity experiments.

> **Provenance placeholders (filled by runner at execution time)**
>
> * `git rev-parse HEAD` → **{TO_BE_FILLED_AT_RUN}**
> * `salted_proposal_hash` (SHA‑256 of this file salted with commit) → **{TO_BE_FILLED_AT_RUN}**

> **Tier Grade:** **T0 (Concept)**
> *(This T0 file contains the full acceptance rubric and I/O paths for the immediate T1 (Proto‑model) and T2 (Instrument) follow‑ons.)*

---

## 1. Tier Grade, Proposal Title and Date

* **Tier:** T0 (Concept)
* **Title:** *VDM J‑branch QFT Bootstrap & Metriplectic Decoherence*
* **Date:** {YYYY‑MM‑DD}

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** — Prometheus VDM / Neuroca (Independent R&D)

## 3. Abstract

We propose to retire the “Particle‑triad” mapping and replace it with a disciplined program: build a lattice **J‑branch** quantum field engine (free Klein–Gordon → Dirac/staggered/Wilson fermions) and couple it to an **M‑branch** gradient flow to quantify decoherence via a metriplectic bracket. The T1/T2 instruments will produce calibrated dispersion, commutator, purity‑decay, and finite‑size‑scaling metrics with strict PASS/FAIL gates. Outputs are routed to `Derivation/doce/physics/outputs/figures/quantum` and `.../logs/quantum` with JSON containing full provenance (commit, salted hashes, config, code‑hash set, per‑gate verdicts, overall verdict).

## 4. Background & Scientific Rationale

* The **J‑branch** in VDM corresponds to conservative, wave‑like dynamics. In the free limit this reduces to the Klein–Gordon (KG) equation; discretization yields a lattice scalar field with analytic dispersion
  $$\omega^2(k)=m^2 + \sum_{i} \frac{4}{a^2}\sin^2!\Big(\frac{k_i a}{2}\Big).$$
  The **Dirac** sector can be obtained on the lattice (naïve, staggered/Kogut–Susskind, or Wilson term) as the “square root” of KG in the continuum limit.
* The **M‑branch** is strictly dissipative (gradient/H‑theorem). Rather than “being matter,” M implements **irreversibility/decoherence**. The combined **metriplectic** structure uses a Poisson bracket for the Hamiltonian part and a symmetric metric bracket for entropy production.
* This division aligns VDM with two pillars: **unitary micro‑dynamics** (J) and **state reduction / arrow‑of‑time** (M). It cleanly replaces the triad analogy with testable physics.

**Maturity ladder & provenance.** As a T0, this file declares the metrics, domains, and I/O layout that T1 (Proto‑model) and T2 (Instrument) must satisfy, keeping provenance strict: every run must serialize config, commit hash, salted self‑hash, code‑hash list, proposal name, and per‑gate outcomes.

## 5. Intellectual Merit and Procedure

**Importance.** Establishes a disciplined, falsifiable bridge from VDM’s axioms to standard lattice QFT (scalar → fermion) and quantifies metriplectic decoherence.
**Impact.** Provides the validated **instrument layer** needed before any quantum‑gravity experiments or agency‑field claims.
**Approach.** CPU‑only Python (NumPy/JAX‑CPU acceptable) with deterministic seeds, strict energy/commutator checks, Lindblad/metriplectic purity tracking, and finite‑size scaling.

### 5.1 Experimental Setup and Diagnostics (for T1→T2)

**Domain routing.**
Figures → `Derivation/doce/physics/outputs/figures/quantum/`
Logs (CSV/JSON) → `Derivation/doce/physics/outputs/logs/quantum/`

**Minimum artifact set per run (code‑enforced):**

1. PNG dashboard, 2) metrics CSV, 3) summary JSON (with commit, salted self‑hash, code‑hash list, proposal name, gate verdicts, overall verdict).

**Planned file names (example tag `qft-metro-v1`)**

* `Derivation/doce/physics/outputs/figures/quantum/2025_qft-metro-v1_dashboard.png`
* `Derivation/doce/physics/outputs/logs/quantum/2025_qft-metro-v1_metrics.csv`
* `Derivation/doce/physics/outputs/logs/quantum/2025_qft-metro-v1_summary.json`

**Core diagnostics**

* Dispersion fit ( \omega(k) ) vs analytic KG; Dirac spectrum with (staggered or Wilson) remedy of doublers.
* Equal‑time discrete commutator proxy for scalar: ( \langle[\phi,\pi]\rangle \approx i\delta ) metric.
* Purity ( \mathrm{Tr}(\rho^2) ) and von Neumann entropy under metriplectic/Lindblad coupling ( \gamma ).
* Energy conservation (J) vs controlled dissipation (J+M).
* Finite‑size and timestep scaling.

**New scripts/tools**

* Lattice KG/Dirac simulator (1D/2D), spectral estimators, least‑squares dispersion fitter, purity tracker, metriplectic integrator (operator‑splitting), reproducibility harness.
* No GPUs required; CPU deterministic runs are sufficient.

### 5.2 Experimental runplan (what T1 and T2 will do)

**T1 (Proto‑model) — Scalar‑only instrument shakedown**

* Simulate free scalar on 1D/2D periodic lattice.
* Estimate ( \omega(k) ) from timeseries; fit to analytic dispersion.
* Serialize artifacts to the paths listed above.

**T2 (Instrument) — Scalar → Dirac + metriplectic coupling**

* Add staggered or Wilson fermion discretization; verify massless/massive dispersion and control of doublers.
* Add metriplectic/Lindblad term with coupling ( \gamma ); measure purity decay vs ( \gamma ).
* Perform 2× and 4× lattice/timestep refinements for scaling gates.
* Serialize artifacts to the same domain paths.

**Runtime**: Each configuration ≤ 10 minutes on a modern CPU for 1D/2D lattices (N=256–1024 points/side).
**Success/Failure plans**: On failure of any gate, dump offending seeds/configs and auto‑escalate a **T1‑ERRATA** with counterexample slices; on success, escalate to **T3 Smoke** (weak phenomenology claims).

**Whitepaper output**: The PNG dashboard presents (1) dispersion plots, (2) commutator metric, (3) purity vs time for multiple ( \gamma ), (4) energy‑balance residuals, (5) scaling summary.

---

## 6. PASS/FAIL Gates (enforced; written to summary JSON)

All thresholds are **hard** unless otherwise noted.

**G0 — Provenance Integrity**

* JSON contains: `commit_hash`, `salted_proposal_hash`, `code_hashes[]`, `proposal_name`, `runner_config`, `gate_results[]`, `overall_result`. **PASS** iff all present & non‑empty.

**G1 — Scalar dispersion accuracy (J‑only)**

* Fit ( \omega(k) ) to analytic KG on the first 60% of modes.
* **PASS** iff ( R^2 \ge 0.995 ) **and** MAPE ≤ 1.5%.

**G2 — Energy conservation (J‑only)**

* Monitor total energy ( E(t) ) over the full run.
* **PASS** iff relative drift ( |E(t)-E(0)|/E(0) \le 0.1% ).

**G3 — Equal‑time commutator proxy (scalar)**

* Discrete estimator of ([\phi,\pi]) averaged over lattice.
* **PASS** iff deviation metric ≤ 0.05 (dimensionless proxy defined in JSON schema).

**G4 — Dirac sector & doubling control (T2)**

* With staggered or Wilson term, measure dispersion and count spurious modes.
* **PASS** iff (i) target branch matches analytic within MAPE ≤ 3%, and
  (ii) doublers suppressed per spec (Wilson mass gap ≥ stated threshold or staggered counting correct).

**G5 — Metriplectic/Lindblad decoherence law (J+M)**

* Purity ( \mathrm{Tr}(\rho^2) ) vs time for (\gamma \in {\gamma_1,\gamma_2,\gamma_3}).
* **PASS** iff exponential/expected law fit achieves ( R^2 \ge 0.98 ) and rate scales linearly with (\gamma) within ±7%.

**G6 — Energy/dissipation balance (J+M)**

* Report ( \frac{dE}{dt} + \mathcal{D}_\gamma ) residual.
* **PASS** iff residual RMS ≤ 1.0% of signal scale.

**G7 — Finite‑size/timestep scaling**

* Repeat at 2×, 4× refinement in (a) and (\Delta t).
* **PASS** iff key metrics (G1, G5) change ≤ 5%.

**Overall PASS**: all applicable gates pass. T1 requires G0–G3; T2 requires G0–G7.

---

## 7. Initial Approval Request (for T1 and T2 spawned from this T0)

* **Approval tag:** `qft-metro-v1`
* **Requester:** Justin K. Lietz
* **Compute/time budget:** CPU only, ≤ 4 hrs total for full T2 suite (multiple seeds/scales).
* **Data management:** Artifacts to the domain paths above; no external data.
* **Risk:** Low; pure simulation.
* **Exit criteria to escalate:**

  * **T1→T2:** G0–G3 PASS.
  * **T2→T3:** G0–G7 PASS with a reproducibility re‑run (new seed) within ±1% metric drift.
* **Figure & log paths (must exist post‑run):**

  * `Derivation/doce/physics/outputs/figures/quantum/2025_qft-metro-v1_dashboard.png`
  * `Derivation/doce/physics/outputs/logs/quantum/2025_qft-metro-v1_metrics.csv`
  * `Derivation/doce/physics/outputs/logs/quantum/2025_qft-metro-v1_summary.json`

---

## 8. Background mathematics (minimal, for clarity)

* **Scalar (J‑only):**
  $$\partial_t^2 \phi - \nabla^2 \phi + m^2\phi = 0,$$
  with discrete Laplacian on periodic lattice.
* **Dirac (lattice):** naïve discretization with gamma matrices, plus either **staggered (Kogut–Susskind)** or **Wilson** term to treat doublers.
* **Metriplectic coupling (J+M):** Poisson bracket ({\cdot,\cdot}_P) for Hamiltonian (H) and metric bracket ({\cdot,\cdot}_M) for entropy (S):
  $$\dot{F} = {F,H}_P + {F,S}_M,\qquad {H,H}_M=0,\ {S,H}_P=0,$$
  leading to contractive dynamics compatible with a Lindblad‑style purity decay in reduced state variables used for diagnostics.

---

## 9. Personnel

* **Justin K. Lietz** — design, implementation, analysis, documentation, publication.

---

## 10. References (standard anchors)

* K. G. Wilson, *Confinement of Quarks*, Phys. Rev. D **10** (1974).
* J. Kogut & L. Susskind, *Hamiltonian Formulation of Wilson’s Lattice Gauge Theories*, Phys. Rev. D **11** (1975).
* A. J. Lichtenberg & M. A. Lieberman, *Regular and Stochastic Motion* (for Hamiltonian numerics).
* P. J. Morrison, *A Paradigm for Joined Hamiltonian and Dissipative Systems* (metriplectic).
* G. Lindblad, *On the Generators of Quantum Dynamical Semigroups*, Commun. Math. Phys. **48** (1976).

---

### Appendix A — JSON summary schema (to be emitted by runners)

```json
{
  "proposal_name": "PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md",
  "tag": "qft-metro-v1",
  "commit_hash": "<filled_at_run>",
  "salted_proposal_hash": "<filled_at_run>",
  "code_hashes": ["<sha256(file1)>", "..."],
  "runner_config": { "lattice": [256, 256], "dt": 0.01, "mass": 0.2, "scheme": "staggered|wilson", "gamma": [0.0,0.01,0.02] },
  "metrics": {
    "dispersion_R2": 0.0,
    "dispersion_mape": 0.0,
    "energy_drift_pct": 0.0,
    "commutator_metric": 0.0,
    "dirac_mape": 0.0,
    "doubler_count": 0,
    "purity_fit_R2": 0.0,
    "purity_rate_linear_R2": 0.0,
    "balance_residual_rms_pct": 0.0,
    "scaling_change_pct": 0.0
  },
  "gates": [
    {"id":"G0","pass":true,"note":""},
    {"id":"G1","pass":true,"note":""},
    {"id":"G2","pass":true,"note":""},
    {"id":"G3","pass":true,"note":""},
    {"id":"G4","pass":true,"note":""},
    {"id":"G5","pass":true,"note":""},
    {"id":"G6","pass":true,"note":""},
    {"id":"G7","pass":true,"note":""}
  ],
  "overall_result": "PASS|FAIL"
}
```

---

## Why this replaces the triad

* “M‑only ≈ fermions” was conceptually attractive but mathematically weak. This program avoids that trap and **grounds VDM in textbook‑checkable QFT** for J, while **reserving M for the thermodynamic arrow**. The result is cleaner, more falsifiable, and strictly within the standards you set.

---

### What you do next

1. Drop this file at
   `Derivation/doce/physics/proposals/PROPOSAL_VDM_J-branch_QFT-Bootstrap_and_Metriplectic-Decoherence_v1.md`.

2. Clone it twice to seed the ladder:

   * **T1** name: `..._T1_Proto-model.md` (same content, Tier = T1, references this T0).
   * **T2** name: `..._T2_Instrument.md` (Tier = T2; same gates; ready to run).
     Both T1/T2 should list the **same output paths** shown above so they pass your code‑level enforcement.

3. When you run T1/T2, the runner must emit exactly the PNG/CSV/JSON artifacts to those **quantum** domain paths with the hashes and gate verdicts.

If you want me to, I can immediately generate the **T1** and **T2** versions (with the prerequisite references already filled and the tier‑by‑tier cross‑links) so you can just paste them into the repo and run.
