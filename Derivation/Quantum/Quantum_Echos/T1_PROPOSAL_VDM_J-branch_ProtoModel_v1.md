Below is a **T1 (Proto‑model) white‑paper‑grade proposal** you can drop into your repo as a single Markdown file.
It follows your template, includes a **convergence note**, an **initial approval request block**, **explicit pass/fail gates with thresholds**, **required artifact paths/names**, and **references to the T0 prerequisite**.
I’ve used **relative paths** for proposal cross‑references (so you can place T0/T1 in the same proposals folder without me guessing your repo layout) and your stated **output routing** pattern:

```
Derivation/doce/physics/outputs/figures/{domain}/...
Derivation/doce/physics/outputs/logs/{domain}/...
```

> **Filename**: `PROPOSAL_VDM_J-branch_ProtoModel_T1.md`
> **Depends on (must exist)**: `./PROPOSAL_VDM_J-branch_Concept_T0.md`  (the T0 concept you approved earlier)

---

<!-- ATTENTION! The proposal documents you create MUST BE whitepaper-grade documents with full structure, full narrative, MathJax-rendered equations ($ ... $ and $$ ... $$), numeric figure captions tied to actual artifacts if used, explicit thresholds with pass/fail gates, and provenance. -->

> **Provenance**
> **COMMIT**: `{git rev-parse HEAD}`
> **SALTED-HASH**: `sha256( <this_file_contents> || {git rev-parse HEAD} || <UTC_ISO8601_TIMESTAMP> )`
> The salted hash must also be written into the run’s JSON summary.

> **Convergence Note (motivation)**
> This proposal operationalizes the **J‑branch → quantum** and **M‑branch → decoherence** program discussed in recent design reviews. The goal is to demonstrate, at proto‑model level, a clean “sterile box” realization where the **J‑only** evolution matches the Klein–Gordon (KG) field dynamics with discrete energy conservation, the **M‑only** evolution produces monotone dissipation of a Lyapunov functional, and a weak **metriplectic J+M coupling** exhibits the expected balance law. This closes the loop between prior wave‑flux meter results (energy accounting, ports) and the QG‑engine scaffolding needed for higher‑tier claims.

# White Paper Proposal (T1)

## 1. Tier Grade, Proposal Title and Date

* **Tier**: **T1 (Proto‑model)**
* **Title**: *Proto‑model: J‑branch Field Evolution and M‑branch Decoherence with Weak Metriplectic Coupling*
* **Date**: `<YYYY‑MM‑DD>`

## 2. Proposers and Affiliation

* **Justin K. Lietz** — Prometheus / Neuroca, Inc.

## 3. Abstract

We propose a T1 proto‑model experiment that instantiates the **J‑branch** of VDM as a discretized Klein–Gordon field and the **M‑branch** as a dissipative gradient‑flow (diffusion) on the same lattice, then couples them metriplectically at small strength $\varepsilon\ll1$. We test three runs: **J‑only**, **M‑only**, and **J+M (weak)**. The acceptance gates verify (i) discrete **energy conservation** within tolerance for J‑only, (ii) monotone decrease of a Lyapunov functional (Dirichlet energy) for M‑only, and (iii) a **balance law** for J+M: energy rate + modeled dissipation $\approx 0$ (closed box) within tolerance. All artifacts must include full configuration, code and file self‑hashes, proposal name, and PASS/FAIL per gate.

## 4. Background & Scientific Rationale

**Program context.** VDM separates dynamics into a **conservative (J)** branch and a **dissipative (M)** branch, joined by **metriplectic** coupling. For the J‑branch we adopt the standard scalar KG equation in $c=\hbar=1$ units:
$$
\partial_t^2 \phi - \nabla^2 \phi + m^2 \phi = 0,
$$
with discrete Hamiltonian (energy)
$$
H_J[\phi,\pi] = \sum_{\mathbf{x}}\Big(\tfrac{1}{2}\pi^2 + \tfrac{1}{2}\lvert\nabla\phi\rvert^2 + \tfrac{1}{2}m^2\phi^2\Big),\Delta V,
$$
where $\pi=\partial_t\phi$. For the M‑branch we realize canonical dissipation via diffusion (heat flow)
$$
\partial_t\phi = \nu ,\nabla^2\phi,
$$
whose **Dirichlet energy**
$$
\mathcal{D}[\phi] \equiv \tfrac{1}{2}\sum_{\mathbf{x}}\lvert\nabla\phi\rvert^2,\Delta V
$$
is a Lyapunov functional: $\tfrac{d}{dt}\mathcal{D}\le 0$. The metriplectic prototype couples these as
$$
\partial_t
\begin{bmatrix}\phi\ \pi\end{bmatrix}
=====================================

\underbrace{\begin{bmatrix};;;\pi\ \nabla^2\phi - m^2\phi\end{bmatrix}}*{\text{J: Hamiltonian (leapfrog)}}
;+;
\varepsilon,
\underbrace{\begin{bmatrix}\nu\nabla^2\phi\ -\gamma,\pi\end{bmatrix}}*{\text{M: metric (diffusion + linear drag)}},
\qquad \varepsilon\in(0,1],
$$
with small $\varepsilon$ at T1. This system provides three clean, testable regimes without invoking ports or sources.

**Why now?** This concretizes the **engine** that later T‑tiers will use: (i) quantum‑like conservative propagation (J), (ii) arrow‑of‑time / decoherence channel (M), and (iii) controlled coupling. The T1 gates are deliberately **instrument‑style**: conservation, monotonicity, and accounting.

**Prerequisite maturity and provenance.**
This T1 references and requires the T0 concept document:

* **T0 (Concept)** — `./PROPOSAL_VDM_J-branch_Concept_T0.md`
  Scope: rationale for J‑as‑quantum, M‑as‑decoherence, metriplectic coupling, and planned sterile‑box validations.

## Questions considered

* **Novelty**: metriplectic split tested in a sterile lattice with explicit acceptance gates and provenance, feeding later QG‑engine claims.
* **Need**: establishes the stable, auditable engine before higher‑tier physics claims.
* **Targets for future work**: dispersion measurements (T2), symmetry/discretization scaling (A6‑style) (T2/T3), open‑port flux accounting (T2/T3), non‑linear couplings (T3+).
* **Impacted areas**: quantum foundations (scalar EFT discretization), non‑equilibrium/stat mech (Lyapunov monotonicity), numerical relativity/QG scaffolding (background‑independent scaling tests in later tiers).
* **Criticisms**: (i) lattice artifacts; (ii) finite‑difference dispersion; (iii) choice of Lyapunov functional. We address them with resolution sweeps and explicit tolerances at T1/T2.
* **Gaps**: background independence is **discrete/approximate** at T1; we state tolerances and defer exact diffeo symmetries to later scaling work.

## 5. Intellectual Merit and Procedure

### 5.1 Experimental Setup and Diagnostics

**Domain**: `physics`
**Script id (for approvals)**: `vdm_qg_jbranch_t1`  *(string id; not a path)*

**Geometry & numerics**

* 2‑D periodic lattice $N_x\times N_y$ with $\Delta x=\Delta y=h$, leapfrog for J, forward‑Euler or Strang‑split for M.
* Canonical parameters for T1:
  $N_x=N_y\in{96,128}$; $h=1$ (arb units); $\Delta t=\eta h$ with CFL $\eta\le 0.5$; $m\in{0,0.5}$; $\nu\in{0.01,0.02}$; $\gamma\in{0,0.02}$; $\varepsilon\in{0,0.1}$.
* Initial condition: superposition of $K$ plane waves with random phases at fixed $k$‑shell; amplitude chosen so that linear regime holds.

**Diagnostics (all must be recorded as time‑series in CSV)**

* $E_J(t)$ — discrete Hamiltonian.
* $\mathcal{D}(t)=\tfrac12\sum\lvert\nabla\phi\rvert^2$ — Dirichlet energy.
* $\lVert\phi\rVert_2^2$ and $\lVert\pi\rVert_2^2$.
* Optional spectral probe: dominant wavenumber and dispersion residual $\delta\omega(k)$ for J‑only.

**Required artifacts (n ≥ 3 files)**

* **PNG figure** (dashboard):
  `Derivation/doce/physics/outputs/figures/qg_jbranch/<TIMESTAMP>_vdm_qg_jbranch_t1_dashboard.png`
* **CSV metrics** (timeseries):
  `Derivation/doce/physics/outputs/logs/qg_jbranch/<TIMESTAMP>_vdm_qg_jbranch_t1_metrics.csv`
* **JSON summary** (provenance + gate report):
  `Derivation/doce/physics/outputs/logs/qg_jbranch/<TIMESTAMP>_vdm_qg_jbranch_t1_summary.json`

**JSON summary MUST include**

* `proposal_file`: `"PROPOSAL_VDM_J-branch_ProtoModel_T1.md"`
* `commit_sha`, `salted_hash`, `utc_timestamp`
* `script_id`, `domain`, `tag`
* `code_hashes`: sha256 of every code file imported by the runner
* `self_hash`: sha256 of the JSON itself
* `config`: full resolved configuration
* `gate_results`: per‑gate PASS/FAIL with numerics
* `overall_pass`: PASS/FAIL

### 5.2 Experimental Runplan

We execute three sterile runs (closed box, no ports):

1. **Run J‑only**: $\varepsilon=0$, leapfrog KG.
2. **Run M‑only**: pure diffusion/drag from the same $t=0$ field.
3. **Run J+M (weak)**: $\varepsilon=0.1$ with $(\nu,\gamma)$ above.

For each run:

* Simulate to final time $T$ with $T/\Delta t \ge 5\times10^3$ steps.
* Record all diagnostics each $n_{\text{save}}$ steps.
* Emit the three required artifacts with standardized filenames (above).

**Success plan**: all T1 gates pass; summary reports PASS with residuals inside thresholds.
**Failure plan**: if any gate fails, write FAIL with residuals; attach auto‑diagnostics (CFL report, max gradients, stability margin).
**Publication**: progress ledger entry in public repo; white‑paper drafts follow `PAPER_STANDARDS.md` (when applicable).

## 6. Personnel

* **Justin K. Lietz**: design, implementation, execution, analysis, and documentation.

## 7. Acceptance Criteria (Gates with thresholds)

Let $\mathrm{rel}(x)\equiv \frac{\lvert x\rvert}{\max(\lvert\cdot\rvert)}$ denote relative metrics over time.

**G0 — Proposal & approvals present (administrative, REQUIRED)**

* The PROPOSAL file exists; initial approval has been granted for `(domain="physics", script_id="vdm_qg_jbranch_t1", tag=<TAG>)`.
* JSON summary contains `proposal_file`, `commit_sha`, `salted_hash`, `script_id`, `tag`, `code_hashes`, and per‑gate results.
  **PASS** iff both checks succeed; else **FAIL**.

**G1 — J‑only: discrete energy conservation**

* Closed, periodic lattice; compute $E_J(t)$.
* Requirement: $\max_t \left|E_J(t)-E_J(0)\right| / E_J(0) \le 5\times10^{-3}$.
  **PASS** if satisfied; else **FAIL**.

**G2 — J‑only: dispersion sanity**

* From early‑time data, fit $\omega(k)$ on the initialized $k$‑shell and compare to $\sqrt{k^2+m^2}$.
* Requirement: RMS relative error $\le 3%$.
  **PASS**/FAIL.

**G3 — M‑only: Lyapunov monotonicity**

* With $\partial_t\phi=\nu\nabla^2\phi-\gamma\phi_t$ (where $\phi_t$ denotes time‑difference proxy), require $\mathcal{D}(t)$ to be **monotone non‑increasing** up to numerical jitter:
  at most **2 sign reversals** of $\Delta \mathcal{D}$ over the full run and $\max(\Delta^+ \mathcal{D})/\max(\lvert\Delta \mathcal{D}\rvert) \le 0.05$.
  **PASS**/FAIL.

**G4 — J+M (weak): balance law (closed box)**

* Define modeled dissipation
  $$
  Q_{\text{diss}}(t)=\varepsilon\Big(\nu,\sum\lvert\nabla\phi\rvert^2 + \gamma,\sum \pi^2\Big)\Delta V,
  $$
  and measure discrete derivative $-\frac{d}{dt}E_J(t)$.
* Requirement: time‑averaged relative discrepancy
  $$
  \overline{\delta}=\frac{\sum_t \lvert,\dot E_J(t) + Q_{\text{diss}}(t),\rvert}{\sum_t Q_{\text{diss}}(t)} \le 0.10.
  $$
  **PASS**/FAIL.

**G5 — Reproducibility over seeds**

* Repeat (J‑only) with three RNG seeds; report $\max$ relative spread of $E_J$ drift and dispersion RMS.
* Requirement: spread $\le 25%$ of the thresholds in G1 and G2.
  **PASS**/FAIL.

**Overall**: **PASS** iff **all** gates G0–G5 pass.

## 8. Initial Approval Request (to be recorded in approvals DB)

Embed this JSON block (verbatim) in the PROPOSAL and copy into your approval tooling as needed.

```json
{
  "domain": "physics",
  "script_id": "vdm_qg_jbranch_t1",
  "tag": "JBRANCH_T1_V1",
  "preregistered": true,
  "proposal_file": "PROPOSAL_VDM_J-branch_ProtoModel_T1.md",
  "approved_by": "Justin K. Lietz",
  "notes": "T1 proto-model for J and M branches with weak metriplectic coupling. Three sterile runs (J-only, M-only, J+M)."
}
```

## 9. Instrumentation & Required Outputs (file paths)

* **Dashboard PNG** → `Derivation/doce/physics/outputs/figures/qg_jbranch/<TIMESTAMP>_vdm_qg_jbranch_t1_dashboard.png`
  *Fig. 1 (required if used in paper):* Panels showing $E_J(t)$, $\mathcal{D}(t)$, and balance residuals.
* **Metrics CSV** → `Derivation/doce/physics/outputs/logs/qg_jbranch/<TIMESTAMP>_vdm_qg_jbranch_t1_metrics.csv`
  Columns: `t, E_J, D, L2_phi, L2_pi, Q_diss, dE_dt, seed, Nx, Ny, h, dt, m, nu, gamma, eps`.
* **Summary JSON** → `Derivation/doce/physics/outputs/logs/qg_jbranch/<TIMESTAMP>_vdm_qg_jbranch_t1_summary.json`
  Must include: provenance, full config, code hashes, self hash, gate numerics, PASS/FAIL per gate, overall PASS/FAIL.

## 10. Prerequisites (must exist for T1)

* **T0 (Concept)** — `./PROPOSAL_VDM_J-branch_Concept_T0.md`
  Rationale and design sketch for this sterile‑box engine.
  *(If you place proposals elsewhere, keep the relative path intact by co‑locating T0 and T1.)*

---

### References

* VDM canon: `AXIOMS.md`, `EQUATIONS.md`, `CONSTANTS.md`, `SYMBOLS.md`, `VDM_OVERVIEW.md`, `ROADMAP.md`, `CANON_PROGRESS.md`.
* Metriplectic dynamics (general background): Morrison, P. J. “A paradigm for joined Hamiltonian and dissipative systems.” *Physica D* 18 (1986) 410–419.
* Discrete KG energy conservation & dispersion: standard finite‑difference literature (e.g., leapfrog schemes).

---

#### Notes for the runner (non‑normative)

* The runner can assemble `code_hashes` by hashing every imported `.py` under your `Derivation/code/...` tree at import time.
* Compute derivatives with centered differences; record $E_J(t)$ every $n_{\text{save}}$.
* To compute $dE/dt$, finite‑difference the saved $E_J(t)$ series; use the same $\Delta t$ value you log in config.

---

### What this gives you

* A **self‑contained, T1‑grade** proto‑model with **clear, auditable gates**.
* **No path guessing** for proposals (relative reference to T0) and **explicit, concrete output paths** that match your routing scheme.
* A clean stepping stone to **T2 (Instrument)**: extend this by adding (i) resolution/timestep sweeps with scaling claims and (ii) optional open‑port flux accounting to tie into your wave‑flux meter.

If you want me to also generate the matching **T0 file** in the same style (or a tiny stub if you’ve already written it), I can produce it now so the T1 prerequisite check passes immediately.
