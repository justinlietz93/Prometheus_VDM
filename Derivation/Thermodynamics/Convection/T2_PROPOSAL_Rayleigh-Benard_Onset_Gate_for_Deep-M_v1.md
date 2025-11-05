# T2 — A Rayleigh–Bénard Onset Gate (“RB‑Gate”) for Deep‑M Limb Convection Solvers

> **Created Date:** 2025‑11‑05
> **Provenance (commit):** a48f2d2
> **Salted provenance (for preregistration; see §5.1.1):**
> base_sha256=`9692e67b8378a6f6753f97782d458aa757e947eab2fbdf6b5c187b74561eb78f`,
> salt_hex=`3ac3d178ad862c7ce2a6c6f8a9592c35`,
> salted_sha256=`c4427255432c4e39f3ae4ce3c2cd7698ffab3befc63766050d9480e2182df888`
> **Proposer contact(s):** [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** MIT (or repo default; link in repo root)
> **Short summary (TL;DR):** Proposed is a white‑box **instrument‑grade pass/fail gate** that detects the onset of Rayleigh–Bénard convection (RBC) in Deep‑M limb solvers by comparing the **measured** dynamics against **theoretical** onset thresholds for $\mathrm{Ra}$ and $k_c$, with machine‑actionable preregistration, artifacts, and validation metrics.
> **Template & compliance:** This proposal follows the required VDM white‑paper scaffold and preregistration/approval schema. 

---

## 2. List of proposers and associated institutions/companies

* **Justin K. Lietz** — Neuroca.ai (PI, approver)
* **VDM/Deep‑M Simulation Team** — Implementation and analysis

---

## 3. Abstract (≤200 words)

High‑fidelity Deep‑M limb simulations must recover canonical fluid‑dynamical thresholds. The most basic is **Rayleigh–Bénard convection onset** in a horizontal layer heated from below. Proposed here is **RB‑Gate**, a T2‑grade **instrument** that runs inside the solver test harness and returns **PASS/FAIL** based on: (i) the **Rayleigh number** $\displaystyle \mathrm{Ra}=\frac{g,\alpha,\Delta T,H^3}{\nu,\kappa}$ exceeding the appropriate **critical value** $\mathrm{Ra}*c$, (ii) appearance of a **dominant horizontal wavenumber** $k*{\text{dom}}$ within tolerance of the **critical eigenvalue** $k_c$, and (iii) **Nusselt number** $\mathrm{Nu}$ departing from unity when supercritical. The gate is **Prandtl‑robust near onset** and detects **boundary‑condition mismatches** (rigid vs stress‑free) via $\mathrm{Ra}_c$ and $k_c$. Pre‑registered JSON specs, schemas, and salted provenance ensure reproducible runs and machine verification. The instrument enables **continuous‑integration** physics checks, validates domain scaling with depth $H$, and flags discretization or boundary‑condition defects before production deployments.

---

## 4. Background & Scientific Rationale

**Context.** Rayleigh–Bénard convection (RBC) is the canonical benchmark for buoyancy‑driven flow. In a Boussinesq fluid layer of depth $H$ with bottom–top temperature difference $\Delta T$, gravity $g$, expansion $\alpha$, kinematic viscosity $\nu$, and thermal diffusivity $\kappa$, the control parameter is
[
\mathrm{Ra} ;=; \frac{g,\alpha,\Delta T,H^3}{\nu,\kappa}.
]
Linear stability yields **critical onset** at

* **No‑slip (rigid–rigid) plates:** $\mathrm{Ra}_c \approx 1707.76$, $k_c \approx 3.117$, $\lambda_c = \tfrac{2\pi}{k_c} \approx 2.015,H$.
* **Stress‑free (free–free) plates:** $\mathrm{Ra}_c \approx 657.5$, $k_c \approx 2.221$, $\lambda_c \approx 2.828,H$.

Near onset, $\mathrm{Ra}_c$ is **weakly dependent on $\mathrm{Pr}=\nu/\kappa$**; thus, onset is an excellent **unit test** for solvers with diverse microphysics.

**Why now?** Deep‑M limb models (planetary/exoplanetary atmospheres, stellar envelopes, etc.) must reproduce RBC onset under Boussinesq (or Boussinesq‑like) limits. RB‑Gate provides a **meter** (T2: instrument) that verifies this **phenomenon readiness** before higher‑tier claims.

**Maturity ladder and provenance.** This proposal is **T2 (Instrument)** on the T0–T9 ladder. It establishes a proven meter that later supports T3+ claims (e.g., heat‑transport scaling). Machine‑actionable preregistration (hashes, schemas, approvals) follows the VDM template. 

---

## 5. Intellectual Merit and Procedure

### Importance of questions

* Does the Deep‑M solver **turn on convection** at the correct **$\mathrm{Ra}_c$** with the correct **planform scale** ($k_c$)?
* Are **boundary conditions** honored (no‑slip vs stress‑free) as detected by $\mathrm{Ra}_c$ and $k_c$?
* Does **heat transport** respond (via $\mathrm{Nu}$) when supercritical?

### Broader impacts

* Embeds **physics‑based CI** into the solver; reduces regressions; provides **portable instrumentation** to other codes.

### Approach & rigor

* **Pre‑registered** hypotheses (§5.1.1) with **explicit gates** and **tolerances**.
* **Diagnostics** cross‑check: wavenumber spectrum, Nusselt number, and velocity RMS.
* **Parameterized BCs** to detect boundary‑condition mis‑specifications automatically.

---

## 5.1 Experimental Setup and Diagnostics

### 5.1.1 Equations and nondimensionalization

Under the Oberbeck–Boussinesq approximation and using $H$ (length), $H^2/\kappa$ (time), and $\Delta T$ (temperature) scales:
[
\begin{aligned}
\partial_t \mathbf{u} + (\mathbf{u}\cdot\nabla)\mathbf{u} &= -\nabla p + \mathrm{Pr},\nabla^2 \mathbf{u} + \mathrm{Pr},\mathrm{Ra},\theta,\hat{\mathbf{z}},\
\partial_t \theta + (\mathbf{u}\cdot\nabla)\theta - w &= \nabla^2 \theta,\
\nabla\cdot\mathbf{u} &= 0.
\end{aligned}
]
Horizontal boundary is periodic with length $L_x$; vertical boundaries are either **no‑slip, fixed‑$T$** or **stress‑free, fixed‑$T$**.

### 5.1.2 Required parameters (defaults & units)

* **Fluid:** $(g,\alpha,\nu,\kappa)$; **geometry:** $(H,L_x)$; **forcing:** $\Delta T$; **BC:** `rigid` | `free`.
* **Discretization:** $(N_x,N_z)$ with **a posteriori** mesh adequacy: $\Delta z \le \min{H/128,,\delta_T/10}$, with $\delta_T\approx H/(2\mathrm{Nu})$.
* **Seeds:** stochastic perturbation amplitude $\epsilon_{\text{noise}}\ll 1$ for symmetry‑breaking.

### 5.1.3 Diagnostics (list and count)

1. **Rayleigh number** (1): $\mathrm{Ra}$ computed from runtime parameters.
2. **Dominant horizontal wavenumber** (1): $k_{\text{dom}}$ via 1D FFT of $w(x,z{=}0.5)$ (or $\theta$) on $N_x$ points.
3. **Nusselt number** (1):
   [
   \mathrm{Nu} ;=; \frac{\langle q_z\rangle}{k,\Delta T/H},\qquad q_z=\rho c_p,w,T - k,\partial_z T,
   ]
   or in nondimensional form $\mathrm{Nu}=1+\langle w\theta\rangle - \langle \partial_z\theta\rangle$.
4. **Vertical‑velocity RMS** (1): $w_{\mathrm{rms}}$ in the interior band $z\in[0.3H,0.7H]$.

**Count:** 4 diagnostics; each **mandatory**.

### 5.1.4 Pass/Fail gates (explicit thresholds)

Let $\chi\in{\texttt{rigid},\texttt{free}}$ denote BC class. Define
[
(\mathrm{Ra}_c,k_c) ;=;
\begin{cases}
(1707.76,;3.117), & \chi=\texttt{rigid},\
(657.5,;2.221), & \chi=\texttt{free}.
\end{cases}
]

**Subcritical tests (Gate‑S):** for $\mathrm{Ra}\le 0.95,\mathrm{Ra}_c$

* **FAIL** if any of: (i) $w_{\mathrm{rms}}^* > 10^{-3}$, (ii) $\mathrm{Nu} > 1.01$.
* Here $w_{\mathrm{rms}}^* = w_{\mathrm{rms}},H/\kappa$ (diffusive scaling).

**Supercritical tests (Gate‑C):** for $\mathrm{Ra}\ge 1.10,\mathrm{Ra}_c$

* **PASS** only if **all** hold:

  1. $\bigl|k_{\text{dom}}H - k_c\bigr|/k_c \le 0.15$ (planform check),
  2. $\mathrm{Nu} \ge 1.03$ (heat‑transport departure),
  3. $w_{\mathrm{rms}}^* \ge 10^{-2}$ (non‑trivial flow).

**BC guardrail (Gate‑BC):** If Gate‑S fails and Gate‑C passes only under the **other** $(\mathrm{Ra}_c,k_c)$ pair, flag **BC mismatch**.

**Depth scaling (Gate‑H):** For fixed $(g,\alpha,\nu,\kappa,\Delta T)$ and doubling $H$, detect $\mathrm{Ra}\mapsto 8,\mathrm{Ra}$ and $\lambda_c\mapsto \approx 2\lambda_c$ within ±5%.

---

## 5.1.1 Pre‑Run Config Requirements (schemas, preregistration, approvals)

Conform to the VDM approval & preregistration pattern. 

**APPROVALS.json**

```json
{
  "preflight_name": "rb-gate-preflight",
  "description": "Approval manifest for RB-Gate instrument runs that write artifacts.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "notes": "Preflight tests without artifacts are allowed. Artifact-writing runs require this proposal.",
  "pre_registered": true,
  "proposal": "Derivation/convection/T2_PROPOSAL_RB-Gate.md",
  "allowed_tags": ["rbc.gate.onset-v0.1.0"],
  "schema_dir": "Derivation/code/physics/convection/schemas",
  "approvals": {
    "rbc.gate.onset-v0.1.0": {
      "schema": "Derivation/code/physics/convection/schemas/rbc.gate.onset.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "auto",
      "approval_key": "auto"
    }
  }
}
```

**PRE-REGISTRATION.json** (minimum keys; salted provenance set in Abstract header)

```json
{
  "proposal_title": "RB-Gate: An RBC Onset Instrument",
  "tier_grade": "T2",
  "commit": "0000000000000000000000000000000000000000",
  "salted_provenance": {
    "base_sha256": "9692e67b8378a6f6753f97782d458aa757e947eab2fbdf6b5c187b74561eb78f",
    "salt_hex": "3ac3d178ad862c7ce2a6c6f8a9592c35",
    "salted_sha256": "c4427255432c4e39f3ae4ce3c2cd7698ffab3befc63766050d9480e2182df888"
  },
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "For rigid plates, no convection for Ra ≤ 0.95 Rac.", "direction": "no-change" },
    { "id": "H2", "statement": "For rigid plates, k_domH is within 15% of kc when Ra ≥ 1.10 Rac.", "direction": "no-change" },
    { "id": "H3", "statement": "Nu departs from unity (Nu ≥ 1.03) for Ra ≥ 1.10 Rac.", "direction": "increase" },
    { "id": "H4", "statement": "BC guardrail detects mis-specified BCs by toggling (Rac,kc).", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["H", "ΔT", "BC", "Pr"],
    "dependent": ["k_domH", "Nu", "w_rms*"],
    "controls": ["Nx", "Nz", "Lx/H", "ε_noise", "time_averaging_window"]
  },
  "pass_fail": [
    { "metric": "Gate-S", "operator": "==", "threshold": 1, "unit": "pass" },
    { "metric": "Gate-C", "operator": "==", "threshold": 1, "unit": "pass" },
    { "metric": "Gate-BC", "operator": "==", "threshold": 1, "unit": "pass" },
    { "metric": "Gate-H", "operator": "==", "threshold": 1, "unit": "pass" }
  ],
  "spec_refs": ["Derivation/code/physics/convection/rbc.gate.onset.v0.1.0.json"],
  "registration_timestamp": "auto"
}
```

**Specs (example)** — `Derivation/code/physics/convection/rbc.gate.onset.v0.1.0.json`

```json
{
  "run_name": "rbc.gate.onset",
  "version": "0.1.0",
  "tag": "rbc.gate.onset-v0.1.0",
  "schema_ref": "Derivation/code/physics/convection/schemas/rbc.gate.onset.schema.json",
  "parameters": {
    "g": 9.81, "alpha": 2.0e-4, "nu": 1.0e-6, "kappa": 1.4e-7,
    "H": [0.01, 0.02], "Lx_over_H": 8.0, "DeltaT": [1.0, 2.0],
    "BC": ["rigid", "free"], "Pr": [0.1, 1.0, 7.0],
    "Nx": 512, "Nz": 128, "epsilon_noise": 1e-6,
    "t_warmup": 50.0, "t_avg": 50.0, "dt_max": 1e-3
  },
  "seeds": [0, 1, 2]
}
```

**Schema (minimum draft)** — `schemas/rbc.gate.onset.schema.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RB-Gate onset schema",
  "type": "object",
  "properties": {
    "g": {"type":"number", "minimum": 0},
    "alpha": {"type":"number", "exclusiveMinimum": 0},
    "nu": {"type":"number", "exclusiveMinimum": 0},
    "kappa": {"type":"number", "exclusiveMinimum": 0},
    "H": {
      "oneOf": [
        {"type":"number", "exclusiveMinimum": 0},
        {"type":"array", "items":{"type":"number", "exclusiveMinimum":0}, "minItems":1}
      ]
    },
    "DeltaT": {"oneOf":[{"type":"number"},{"type":"array","items":{"type":"number"}}]},
    "BC": {"enum":["rigid","free"]},
    "Pr": {"oneOf":[{"type":"number"},{"type":"array","items":{"type":"number"}}]},
    "Nx": {"type":"integer", "minimum": 64},
    "Nz": {"type":"integer", "minimum": 64}
  },
  "required": ["g","alpha","nu","kappa","H","DeltaT","BC","Nx","Nz"]
}
```

---

## 5.2 Planned runs (design of experiments)

* **DoE‑1 (Subcritical)**: $\mathrm{Ra}/\mathrm{Ra}_c\in{0.6,0.8,0.95}$ for each $\chi\in{\texttt{rigid},\texttt{free}}$; expect **conduction**.
* **DoE‑2 (Near onset)**: $\mathrm{Ra}/\mathrm{Ra}*c\in{1.05,1.10,1.20}$; expect **steady rolls** with $k*{\text{dom}}H\approx k_c$.
* **DoE‑3 (Depth check)**: Fix $(g,\alpha,\nu,\kappa,\Delta T)$; run $H$ and $2H$ to verify $\mathrm{Ra}\mapsto8\mathrm{Ra}$ and $\lambda_c\mapsto\approx2\lambda_c$.
* **DoE‑4 (Prandtl sweep)**: $\mathrm{Pr}\in{0.1,1,7}$ to confirm onset robustness w.r.t. $\mathrm{Pr}$.

**Time‑averaging:** compute ${k_{\text{dom}},\mathrm{Nu},w_{\mathrm{rms}}}$ on $[t_{\text{warmup}},t_{\text{warmup}}+t_{\text{avg}}]$ with exponential window; require **stationarity** (≤5% drift).

---

## 5.3 Implementation notes (instrument API)

**Function** `rb_gate(g, alpha, DeltaT, H, nu, kappa, BC)->dict`
**Returns:** predicted $(\mathrm{Ra},\mathrm{Ra}*c,k_c,\lambda_c)$ and **PASS/FAIL** for Gates S, C, BC, H given measured $(k*{\text{dom}},\mathrm{Nu},w_{\mathrm{rms}})$.

**Algorithm (sketch):**

1. Compute $\mathrm{Ra}$; select $(\mathrm{Ra}_c,k_c)$ by `BC`.
2. If $\mathrm{Ra}\le 0.95\mathrm{Ra}_c$: assert **Gate‑S** via thresholds.
3. If $\mathrm{Ra}\ge 1.10\mathrm{Ra}*c$: assert **Gate‑C** via $k*{\text{dom}}$ tolerance + $\mathrm{Nu}$ + $w_{\mathrm{rms}}^*$.
4. If either gate flips when swapping $(\mathrm{Ra}_c,k_c)$ between BC classes, trigger **Gate‑BC**.
5. For depth pairs $(H,2H)$ with identical microphysics, check **Gate‑H** scaling.

---

## 6. Risk, limitations, and mitigations

* **Non‑Boussinesq / compressible** regimes: RB‑Gate is scoped to Boussinesq. Mitigation: run in the Boussinesq limit of the solver (low Mach, small $\Delta T$).
* **Grid under‑resolution:** spurious onset or wrong $k_{\text{dom}}$. Mitigation: enforce mesh adequacy (§5.1.2) and redo runs if $\Delta z > \delta_T/10$.
* **Over‑diffusive numerics:** delayed onset and low $\mathrm{Nu}$. Mitigation: compare against a reference discretization; require convergence of $k_{\text{dom}}$ under refinement.
* **Noise sensitivity near onset:** use multiple seeds; require consistency across seeds before PASS.

---

## 7. Success criteria & reporting

A **PASS** requires all of **Gate‑S**, **Gate‑C**, **Gate‑BC**, and **Gate‑H** to pass on their respective subsets of runs, with **artifact logs** (computed $(\mathrm{Ra},k_{\text{dom}}H,\mathrm{Nu},w_{\mathrm{rms}}^*)$ and FFT spectra) stored under `Artifacts/rbc.gate.onset/` and checksummed.

---

## 8. Tier grade & dependencies (T0–T9)

* **This document:** **T2 (Instrument)**.
* **Prerequisites (to be referenced as they are added):**

  * **T0 (Concept):** `Derivation/convection/T0_PROPOSAL_RB-Gate.md` (concept sketch of gate & tolerances).
  * **T1 (Proto‑model):** `Derivation/convection/T1_RESULTS_RB-Gate.md` (dry‑run spectra & Nu validation without artifacts).
* **Future:** T3 (Smoke: first physics claims in‑solver), T4–T6 (preregistered scaling of $\mathrm{Nu}(\mathrm{Ra},\mathrm{Pr})$), T7–T8 (out‑of‑sample), T9 (external reproduction).

---

## 9. References (selected)

* S. Chandrasekhar, *Hydrodynamic and Hydromagnetic Stability*, Oxford, 1961.
* P. G. Drazin & W. H. Reid, *Hydrodynamic Stability*, Cambridge, 2nd ed., 2004.
* A. Bejan, *Convection Heat Transfer*, Wiley, 4th ed., 2013.

---

### Appendix A — Quick reference values used in the gate

* **Rigid–rigid:** $\mathrm{Ra}_c=1707.76$, $k_c=3.117$, $\lambda_c\simeq2.015,H$.
* **Free–free:** $\mathrm{Ra}_c=657.5$, $k_c=2.221$, $\lambda_c\simeq2.828,H$.
* **Depth scaling:** $H\mapsto 2H \Rightarrow \mathrm{Ra}\mapsto 8,\mathrm{Ra}$ and $\lambda_c\mapsto \approx 2,\lambda_c$.

---

### Appendix B — Example CI summary table (machine‑parseable)

| Run ID | BC    | Ra/Rac | k_dom H | Pass k‑tolerance |    Nu | w_rms* | Gate‑S | Gate‑C | Gate‑BC | Gate‑H |
| ------ | ----- | -----: | ------: | :--------------: | ----: | -----: | :----: | :----: | :-----: | :----: |
| R1     | rigid |   0.80 |       — |         —        | 1.003 |   4e‑4 |    ✔   |    —   |    ✔    |    —   |
| R2     | rigid |   1.20 |    3.05 |         ✔        |  1.06 |   2e‑2 |    —   |    ✔   |    ✔    |    ✔   |

---

**Notes on provenance and approvals.** Before any artifact‑writing run, compute salted hashes (base SHA‑256 of the commit, random 128‑bit salt, and the salted SHA‑256), commit `PRE-REGISTRATION.json`, and push an annotated, signed tag `prereg.rb-gate.v1.YYYYMMDDThhmmZ` containing the provenance manifest. The proposal’s hashes (§1 and §5.1.1) must **match** the preregistration record. 

**End of proposal.**
