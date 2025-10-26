<!-- PROPOSAL FILE: proposals/PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md -->

> Provenance (commit & salted hash)
> - git commit (repo state at authoring): {git rev-parse HEAD}
> - salted content hash (sha256): {sha256(commit || file_contents || SALT)}

> Initial Approval Request (required by repo policy)
> - request_id: APR-{YYYYMMDD}-{HHMMSS}-{short_commit}
> - requestor: Justin K. Lietz
> - branch: {feature/qdynamics-willow-convergence}
> - proposal_file: proposals/PROPOSAL_VDM_QEcho-Convergence_Willow_v1.md
> - required_artifacts (min 3): PNG, CSV, JSON
> - approval_tag (to be set by /tools/approve_tag.py): PENDING → APPROVED
> - run_gate: no runner may start until approval_tag == APPROVED

# Convergence Note (motivation-first)

This preregistration documents a **convergence** between VDM’s metriplectic
engine (reversible `J` + dissipative `M`) with closed-loop “void‑walker” pulses
and modern **echo/self-correction** quantum workflows. Both architectures exhibit
**feedback-stabilized dynamics** that suppress accumulated error while preserving a
conserved core (reversible) flow. The proposal registers that convergence and
tests it with instrument-grade gates.

---

## 1. Tier Grade, Proposal Title and Date

- **Tier Grade:** **T4 (Prereg)**
- **Title:** Convergence of VDM Metriplectic Echo Dynamics with Feedback‑Stabilized Quantum Echo Workflows
- **Date:** {YYYY‑MM‑DD}

## 2. List of proposers and associated institutions/companies

- **Justin K. Lietz** — Neuroca, Inc. (VDM Program)

## 3. Abstract (≤200 words)

We preregister a **numerical experiment** that couples VDM’s metriplectic flow to an
echo‑style, feedback‑stabilized control loop and evaluates whether the closed‑loop
dynamics achieve (i) **monotone fidelity recovery** per echo cycle, (ii) **bounded drift**
in the conservative invariant, and (iii) **reproducible gain** across seeds and noise
realizations. The reversible core is modeled by the VDM `J`‑branch, while the
`M`‑branch implements controlled dissipation mimicking error‑scrubbing. We define four
instrument‑grade **gates** with explicit thresholds and require **mandatory artifacts**:
PNG/CSV/JSON plus logs, with **runner config**, **code hash**, **self‑hash**, **proposal
name**, per‑gate PASS/FAIL, and an overall PASS/FAIL. Passing this preregistration
establishes a disciplined bridge from VDM’s metriplectic control to echo‑stabilized
workflows and prepares a T5 pilot with hardware surrogates.

## 4. Background & Scientific Rationale

**VDM metriplectic core.** We use the standard metriplectic form
$$
\dot{z} \;=\; J(z)\,\nabla H(z)\;+\;M(z)\,\nabla S(z),
$$
with $J^\top=-J$ (reversible/Poisson) and $M^\top=M\succeq 0$ (dissipative),
$H$ energy-like, $S$ entropy-like. The **echo** protocol is encoded as a
stroboscopic map that alternates (reversible step) → (dissipative scrub) →
(reverse of reversible step), forming one “echo cycle”.
We test whether the **feedback loop** produces self‑correction while preserving
conservative structure within tolerances.

**Why now.** VDM already achieved self‑correction in classical runs via
“void‑walker” pulses that locate pathologies and **GDSP** closure. This proposal
formalizes that mechanism as an echo‑stabilized metriplectic loop and subjects it
to instrument‑grade gates (drift, monotonic recovery, reproducibility).

**Novelty & risk.** Novelty lies not in the mathematics (metriplectic/echo are
standard) but in the **operational convergence** and the **meter‑grade gates**,
which make the claim falsifiable. Risks: over‑regularization (loss of signal),
or false recovery by smoothing. We guard with pre/post spectral checks and
two‑grid order tests.

*(This document conforms to your White Paper Proposal Template and results‑posting
discipline, including artifact provenance and PASS/FAIL accounting.)* :contentReference[oaicite:2]{index=2} :contentReference[oaicite:3]{index=3}

## 5. Intellectual Merit and Procedure

**Importance.** A disciplined, closed‑loop metriplectic echo establishes a reusable
**control primitive** for VDM (later: portal to hardware).  
**Impact.** If gates pass across seeds/noise, VDM’s echo control becomes a certified
instrument (T2→T4) for subsequent T5/T6 claims.  
**Clarity/rigor.** We predefine equations, discretization, diagnostics, and **gates**,
and we publish all artifacts with hashes and PASS/FAIL JSON.

### 5.1 Experimental Setup and Diagnostics

**State & flow.** Discretize $z\in\mathbb{R}^d$ on a cubic lattice (periodic),
Strang‑split the flow into $J$ and $M$ steps. Echo cycle length: $T_e$.

**Core equations (discrete):**
- Reversible (symplectic) step: $z^{n+\frac12} = \Phi_J^{\Delta t}(z^n)$ (symplectic integrator).
- Dissipative step (gradient flow): $z^{n+1} = z^{n+\frac12} - \Delta t\, M(z^{n+\frac12})\,\nabla S(z^{n+\frac12})$.
- Echo map: $\mathcal{E} = \Phi_J^{\Delta t}\circ \Phi_M^{\Delta t}\circ \Phi_J^{-\Delta t}$.

**Diagnostics (all recorded to CSV & JSON):**
- **Fidelity gain per cycle:** $\Delta F_k := F_{k}-F_{k-1}$, with
  $F_k = \frac{\langle z_k, z_0\rangle}{\|z_k\|\,\|z_0\|}$.
- **Conservative drift:** $\Delta H_k := H(z_k)-H(z_0)$.
- **Dissipative monotonicity:** $S(z_{k+1})-S(z_k)\ge 0$.
- **Two‑grid order test:** slope $\ge 2.0$ for an observable (e.g. RMSE to reference).
- **Reproducibility across seeds:** variability of $F_K$.

**Noise & perturbations.** Add bounded perturbations $\eta\sim\mathcal{N}(0,\sigma^2)$ at
each cycle, and a structured detuning $\delta$; sweep $\sigma\in\{0,\,\sigma_0,\,2\sigma_0\}$,
$\delta\in\{0,\,\delta_0\}$.

**Artifact & log paths (must exist post‑run):**
- **Image:** `artifacts/{date}/RESULTS_VDM_QEcho-Convergence_Willow_v1.png`
- **CSV:**   `artifacts/{date}/RESULTS_VDM_QEcho-Convergence_Willow_v1.csv`
- **JSON:**  `artifacts/{date}/RESULTS_VDM_QEcho-Convergence_Willow_v1.json`
- **Logs:**  `logs/{date}/RUNNER.log`, `logs/{date}/ENV.md`, `logs/{date}/CONTRA_REPORT.md`

*(“{date}” = YYYYMMDD_HHMMSS_seedNN)*

### 5.2 Experimental runplan

**Plan.** For each seed and noise level, run $K$ echo cycles (e.g., $K=256$),
record $(F_k,\Delta H_k,S_k)$, compute gates, emit artifacts with hashes.

**Runtime.** CPU; ~{N} minutes per seed × {S} seeds × {levels} noise settings.

**Success path.** All gates pass; publish artifacts & JSON; promote to T5 pilot.  
**Failure path.** Post **CONTRA_REPORT.md** with the failing gate, measured values,
and a minimal counterexample seed; file a remediation issue.

**Publication / display.** PNG shows $F_k$ trajectories and drift bounds with CI.
CSV holds per‑cycle metrics; JSON holds full provenance and PASS/FAIL accounting.
(Policy mirrors your RESULTS template.) :contentReference[oaicite:4]{index=4}

---

## Gates (explicit thresholds; all must pass)

- **Gate G1 — Monotone fidelity recovery.**  
  Metric: $\Delta F_k\ge 0$ for $k=1..K$, with at least **+0.05** net gain:  
  $F_K - F_0 \ge 0.05$. **Pass if TRUE** (allow ≤1 violation of $\Delta F_k<0$ with magnitude < 1e‑3).

- **Gate G2 — Conservative drift bound (Noether‑like).**  
  $|\Delta H_k| \le 5\times10^{-4}$ for all $k$ (per‑cycle bound, dimensionless units). **Pass if TRUE**.

- **Gate G3 — Dissipative monotonicity.**  
  $S_{k+1}-S_k \ge -1\times10^{-6}$ (tolerance for FP jitter) for all $k$. **Pass if TRUE**.

- **Gate G4 — Reproducibility across seeds.**  
  $\mathrm{RMAD}(F_K)\le 0.10$ across $N\ge 8$ seeds (relative median absolute deviation). **Pass if TRUE**.

*(Any failed gate triggers `logs/{date}/CONTRA_REPORT.md` with minimal repro.)*

---

## Mandatory outputs & JSON schema (repo‑enforced)

Every run **must** emit PNG/CSV/JSON with the same basename and include the following
JSON keys (self‑describing provenance & gate accounting):

```json
{
  "proposal_name": "PROPOSAL_VDM_QEcho-Convergence_Willow_v1",
  "runner_commit": "{git rev-parse HEAD}",
  "runner_config": { "dt": 0.005, "K": 256, "sigma": 0.01, "delta": 0.0, "grid": [128,128,128], "scheme": "Strang+symplectic" },
  "code_hash": "sha256(source_tree@commit || SALT)",
  "artifact_hash": "sha256(this_json_contents || SALT)",
  "artifacts": {
    "png":  "artifacts/{date}/RESULTS_VDM_QEcho-Convergence_Willow_v1.png",
    "csv":  "artifacts/{date}/RESULTS_VDM_QEcho-Convergence_Willow_v1.csv",
    "json": "artifacts/{date}/RESULTS_VDM_QEcho-Convergence_Willow_v1.json"
  },
  "gates": [
    { "name": "G1_Monotone_Fidelity", "threshold": "F_K - F_0 >= 0.05; ≤1 dip <1e-3", "measured": 0.072, "pass": true },
    { "name": "G2_H_Drift",          "threshold": "|ΔH_k| <= 5e-4 ∀k",               "measured_max": 2.1e-4, "pass": true },
    { "name": "G3_S_Monotonicity",   "threshold": "ΔS_k >= -1e-6 ∀k",                 "min_measured": -3e-7,  "pass": true },
    { "name": "G4_Seeds_RMAD",       "threshold": "RMAD(F_K) <= 0.10 over N>=8",      "measured": 0.06,       "pass": true }
  ],
  "overall_pass": true
}
