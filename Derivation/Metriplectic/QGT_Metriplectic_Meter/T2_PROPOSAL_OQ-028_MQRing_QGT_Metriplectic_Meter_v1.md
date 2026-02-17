# 1. T2 (Instrument) - QGT→Metriplectic Meter on Mandelbrot Quantum Rings (OQ-028, MQRing-QGT-v1)

> **Created Date:** 2026-02-17  
> **Git Commit (rev-parse HEAD):** 91332f4cf89a52d239eaab6659b8df8d8b9f3202  
> **Base SHA256:** 1293dbc685c05d2556ddb42f551c2e48b7a5ed3faffdbceab7d0a375b8384063  
> **Salt (hex):** 90b0be843af3c9c58ff9f6d41357542c  
> **Salted SHA256:** 7ed60efbafa5703aac444728cf32c3e55f30b2830b738773ef42709cb4b8c9bd  
> **Proposer contact(s):** Justin K. Lietz (<justin@neuroca.ai>)  
> **License:** `LICENSE` (repository root)  
> **Short summary (one sentence TL;DR):** A validated computational instrument that computes the Quantum Geometric Tensor (QGT) and induced metriplectic bracket data $(J,M)$ on flux-threaded Mandelbrot quantum rings, with explicit numerical and invariance gates.

***Practical Provenance pattern (enforced)***

- Compute salted hashes with a random salt; store `base_sha256`, `salt_hex`, `salted_sha256` in `PRE-REGISTRATION.json`.
- Commit prereg and proposal, then create an annotated, signed tag whose message includes: commit SHA, prereg path, and the salted provenance items (or a single manifest hash).
- Push the tag before running. The run must record that tag in artifacts.
- The authorization / approval system must reject any artifact-writing run that does not match the approved prereg + tag.

***Avoid circularity***

- Hashing must exclude the line(s) containing the hash itself (implemented by blanking `1293dbc685c05d2556ddb42f551c2e48b7a5ed3faffdbceab7d0a375b8384063`, `90b0be843af3c9c58ff9f6d41357542c`, `7ed60efbafa5703aac444728cf32c3e55f30b2830b738773ef42709cb4b8c9bd` prior to hashing; see §5.1.1).

---

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Neuroca AI, LLC — PI / implementer / approver
- Independent reviewer (TBD) — external approver (required before artifact-writing runs)

---

## 3. Abstract

Proposed in this document is a Tier‑2 **instrument** that numerically evaluates the **Quantum Geometric Tensor (QGT)** and its induced **metriplectic bracket data** $(J,M)$ for a family of **flux-threaded Mandelbrot quantum ring** Hamiltonians. The meter is required to pass explicit **grid-convergence**, **flux periodicity**, **QGT gauge invariance**, **metric positive semi-definiteness**, and **Poisson/Jacobi** gates on both a circular-ring baseline and a fractal-border ring. The motivating external reference is a Scientific Reports study reporting flux-dependent spectra and persistent currents in Mandelbrot quantum rings, providing a concrete geometry where boundary hierarchy and flux response can be stress-tested. Passing this proposal produces a reusable computational meter that connects the CF1 “QGT→metriplectic” mapping to future, higher-tier VDM experiments.

---

## 4. Background & Scientific Rationale

### 4.1 Why this experiment is important

- VDM requires a disciplined separation between **meter validation** (T2) and **physics claims** (T3+). A QGT→$(J,M)$ implementation must be proven as a meter before it is used as evidence.
- Mandelbrot quantum rings provide a boundary-complex but controlled geometry, threaded by a clean control parameter: **dimensionless flux** $\varphi=\Phi/\Phi_0$.
- The observable class (flux response of eigenenergies; persistent current as a derived diagnostic) is low-ambiguity and supports clear QA thresholds.

### 4.2 What this proposal materially contributes (new in VDM)

- A new **T2 meter**: stable QGT evaluation plus induced bracket extraction $(J,M)$ on a 2-parameter manifold $(\varphi,\alpha)$.
- A reproducible **QA harness** with pass/fail gates that blocks higher-tier work if invariances or convergence fail.
- A concrete bridge between:
  - External derived-limit quantum Hamiltonians (testbeds), and
  - CF1’s internal mapping that produces metriplectic objects from QGT.

### 4.3 Related work and prerequisite tier ladder (must exist in-repo)

This proposal is graded **T2**; therefore prerequisite in-repo artifacts for **T0** and **T1** must be referenced (in sequence):

- **T0:** `Derivation/Unification/T0_Unification_Program_Spec_v1.md`
- **T1:** `Derivation/Metriplectic/Constructive_QGT_to_Metriplectic/T1_PROPOSAL_G-QGT-1_QGT-to-Metriplectic_Mapping_v1.md`
- **CF stack:** `Derivation/Complete-Formalisms/CF1_QGT_to_Metriplectic_Brackets.md`

External motivating reference (non-foundational):

- D. H. T. Tehrani, M. Solaimani, “Persistent currents and electronic properties of Mandelbrot quantum rings”, *Scientific Reports* **13**:5710 (2023). DOI: 10.1038/s41598-023-32905-w.

### 4.4 Criticisms, gaps, and kill-plans

- **Criticism:** QGT numerics are phase/gauge sensitive and can produce artifacts near eigenvalue crossings.  
  **Kill-plan:** Gate G2 (gauge invariance) + an explicit “crossing exclusion” rule; failure blocks all downstream use.
- **Criticism:** Fractal boundaries may demand high spatial resolution and destabilize eigen-solvers.  
  **Kill-plan:** Gate G0 (grid refinement) is mandatory; failure triggers either (a) increased $N$, (b) larger $L$, or (c) smoother $\alpha<1$ for derivative evaluation; if still failing, the meter is rejected.
- **Criticism:** In 2D parameter manifolds, Poisson consistency can be “too easy.”  
  **Kill-plan:** Gate G4 evaluates a numerical Jacobiator on nontrivial test functions and requires nondegeneracy of $\Omega_{\varphi\alpha}$.

---

## 5. Intellectual Merit and Procedure

**(1) Importance of the scientific questions addressed.**  
This proposal validates whether QGT→$(J,M)$ mapping is numerically stable and invariant in a boundary-complex quantum testbed.

**(2) Potential broader impacts.**  
A passing T2 meter is reusable across parameterized quantum test systems and provides a disciplined bridge from QGT geometry to metriplectic structures used throughout the VDM CF stack.

**(3) Clarity and reasonableness of the experimental approach.**  
The plan is explicit: define a Hamiltonian family on a ring domain, compute eigenpairs, compute QGT on $(\varphi,\alpha)$ with two independent phase conventions, and enforce pass/fail gates.

**(4) Planned rigor and discipline.**  
All gates are quantitative; all run specs and schemas are machine-readable; approval and preregistration are mandatory before artifact-writing runs.

---

## 5.1 Experimental Setup and Diagnostics

### 5.1.1 Pre-Run Config Requirements

**Mandatory before artifact-writing runs** (preflight tests are allowed without approval).

- Required config and metadata:
  - `Derivation/code/physics/quantum_fractals/mqring_qgt/APPROVALS.json`
  - `Derivation/code/physics/quantum_fractals/mqring_qgt/PRE-REGISTRATION.json`
  - `Derivation/code/physics/quantum_fractals/mqring_qgt/schemas/`
    - `mqring-qgt-v1.schema.json`
  - `Derivation/code/physics/quantum_fractals/mqring_qgt/specs/`
    - `mqring_qgt_meter.v1.json`

**Proposal provenance values (must match header):**

- `base_sha256`: `1293dbc685c05d2556ddb42f551c2e48b7a5ed3faffdbceab7d0a375b8384063`
- `salt_hex`: `90b0be843af3c9c58ff9f6d41357542c`
- `salted_sha256`: `7ed60efbafa5703aac444728cf32c3e55f30b2830b738773ef42709cb4b8c9bd`

### APPROVALS.json

```json
[
  {
    "preflight_name": "mqring_qgt_meter_preflight",
    "description": "Approval manifest stating that the preflight runner must pass before real runs that write artifacts.",
    "author": "Justin K. Lietz",
    "requires_approval": true,
    "pre_commit_hook": true,
    "notes": "Preflight runs (Derivation/code/tests) are allowed without approval. To run real experiments that write artifacts, a relevant PROPOSAL_* must exist at Derivation/Quantum_Fractals/Mandelbrot_QR_QGT/ with explicit review."
  },
  {
    "pre_registered": true,
    "proposal": "Derivation/Quantum_Fractals/Mandelbrot_QR_QGT/T2_PROPOSAL_OQ-028_MQRing_QGT_Metriplectic_Meter_v1.md",
    "allowed_tags": [
      "mqring-qgt-v1"
    ],
    "schema_dir": "Derivation/code/physics/quantum_fractals/mqring_qgt/schemas",
    "approvals": {
      "mqring-qgt-v1": {
        "schema": "Derivation/code/physics/quantum_fractals/mqring_qgt/schemas/mqring-qgt-v1.schema.json",
        "approved_by": "Justin K. Lietz",
        "approved_at": "2026-02-17",
        "approval_key": "a59f3f4b7d4c1389c48674eaace0c2b2"
      }
    }
  }
]
```

### PRE-REGISTRATION.json

```json
{
  "proposal_title": "T2 (Instrument) - QGT→Metriplectic Meter on Mandelbrot Quantum Rings (OQ-028, MQRing-QGT-v1)",
  "tier_grade": "T2",
  "commit": "91332f4cf89a52d239eaab6659b8df8d8b9f3202",
  "salted_provenance": "7ed60efbafa5703aac444728cf32c3e55f30b2830b738773ef42709cb4b8c9bd",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {
      "id": "H1",
      "statement": "The QGT computed for the ground state on (phi, alpha) is gauge-invariant within the specified tolerance across circular and fractal-border rings.",
      "direction": "no-change"
    }
  ],
  "variables": {
    "independent": ["phi", "alpha", "N"],
    "dependent": ["QGT_components", "gate_metrics"],
    "controls": ["m", "mandelbrot_iters", "v0", "L_over_R"]
  },
  "pass_fail": [
    { "metric": "E_refinement_relerr", "operator": "<=", "threshold": 1e-3, "unit": "dimensionless" },
    { "metric": "flux_periodicity_relerr", "operator": "<=", "threshold": 1e-3, "unit": "dimensionless" },
    { "metric": "QGT_gauge_residual", "operator": "<=", "threshold": 1e-4, "unit": "dimensionless" },
    { "metric": "g_min_eigenvalue", "operator": ">=", "threshold": -1e-10, "unit": "dimensionless" },
    { "metric": "jacobiator_max_abs", "operator": "<=", "threshold": 1e-6, "unit": "dimensionless" }
  ],
  "spec_refs": [
    "Derivation/code/physics/quantum_fractals/mqring_qgt/specs/mqring_qgt_meter.v1.json"
  ],
  "registration_timestamp": "2026-02-17T00:00:00Z",
  "base_sha256": "1293dbc685c05d2556ddb42f551c2e48b7a5ed3faffdbceab7d0a375b8384063",
  "salt_hex": "90b0be843af3c9c58ff9f6d41357542c",
  "salted_sha256": "7ed60efbafa5703aac444728cf32c3e55f30b2830b738773ef42709cb4b8c9bd"
}
```

### Specs

```json
{
  "run_name": "mqring_qgt_meter",
  "version": "v1",
  "tag": "mqring-qgt-v1",
  "schema_ref": "Derivation/code/physics/quantum_fractals/mqring_qgt/schemas/mqring-qgt-v1.schema.json",
  "parameters": {
    "grid": { "N_values": [201, 401], "L_over_R": 1.25 },
    "physics": { "v0": 1.0e3, "m_eff_over_m0": 0.067 },
    "geometry": { "m": 6, "mandelbrot_iters": 200, "alpha_values": [0.0, 1.0] },
    "sweep": {
      "phi_gate_set": [0.0, 0.25, 0.5, 0.75],
      "delta_phi": 0.01,
      "delta_alpha": 0.05,
      "K_eigs": 8
    },
    "qgt": { "phase_methods": ["parallel_transport", "anchor_phase"] }
  },
  "seeds": [0]
}
```

### Schemas

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "vdm.mqring-qgt-v1.schema",
  "title": "MQRing QGT meter artifacts schema (v1)",
  "type": "object",
  "properties": {
    "run_name": { "type": "string" },
    "tag": { "type": "string" },
    "params": { "type": "object" },
    "metrics": { "type": "object" },
    "passes": { "type": "object" },
    "artifacts": { "type": "object" }
  },
  "required": ["run_name", "tag", "params", "metrics", "passes", "artifacts"]
}
```

---

### 5.1.2 System definition (derived-limit testbed)

A single-particle 2D effective-mass Hamiltonian in the plane, threaded by Aharonov–Bohm flux:

$$
\hat H(\varphi,\alpha) ;=; \frac{1}{2m^*}\Big(\hat{\mathbf P} - \frac{e}{c}\hat{\mathbf A}(\varphi)\Big)^2 ;+; V(\mathbf r;\alpha),
$$

with $\mathbf r=(x,y)$ and a confining potential implemented by a barrier mask:
$$
V(\mathbf r;\alpha)=V_0 \,\chi_{\text{outside ring}}(\mathbf r;\alpha).
$$

**Dimensionless reporting (A6 compliance):**

- Length scale: $R$ (outer ring radius or equivalent).
- Energy scale: $E_\star=\hbar^2/(2m^*R^2)$.
- Flux: $\varphi=\Phi/\Phi_0$ with $\Phi_0=hc/e$.
- Barrier: $v_0 = V_0/E_\star$.

---

### 5.1.3 Geometry parameterization

Define $\lambda=(\varphi,\alpha)$ with:

- $\alpha\in[0,1]$ interpolating between a circular ring mask and a Mandelbrot-border ring mask.
- Mandelbrot order fixed at $m=6$ for T2, with membership defined by:
$$
z_{n+1} = z_n^{\,m} + c,\qquad z_0 = 0,\qquad c=x+iy,
$$
and membership if $|z_n|\le 2$ for $n\le N_{\text{iter}}$.

Outside-ring mask interpolation:
$$
\chi_{\text{outside ring}}(\mathbf r;\alpha) \;=\; (1-\alpha)\,\chi_{\text{outside,circle}}(\mathbf r)\;+\;\alpha\,\chi_{\text{outside,fractal}}(\mathbf r;m).
$$

---

### 5.1.4 Required parameters and defaults (keys + units)

Primary (dimensionless) parameters:

- `N` (grid points per dimension): default 401 (also 201 for refinement gate)
- `L_over_R` (box half-width over outer radius): default 1.25
- `v0 = V0 / E_*` (barrier height): default $10^3$
- `m` (Mandelbrot order): default 6
- `mandelbrot_iters`: default 200
- `phi_gate_set` (flux samples): default `[0.0, 0.25, 0.5, 0.75]`
- `delta_phi`: default `0.01`
- `alpha_values`: default `[0.0, 1.0]`
- `delta_alpha`: default `0.05`
- `K_eigs`: default 8

---

### 5.1.5 QGT and induced bracket definitions (used by diagnostics)

Let $|\psi_0(\lambda)\rangle$ be the ground-state eigenvector of $\hat H(\lambda)$ with $\lambda=(\varphi,\alpha)$.

Define the QGT:
$$
Q_{ij}(\lambda) \;=\;\langle \partial_i \psi_0 \,|\, (1-|\psi_0\rangle\langle\psi_0|)\,|\, \partial_j \psi_0\rangle,
$$
with indices $i,j\in\{\varphi,\alpha\}$.

Then:
$$
g_{ij} = \Re Q_{ij},\qquad \Omega_{ij} = -2\,\Im Q_{ij}.
$$

Candidate induced metriplectic data on parameter space:
$$
M(\lambda) \equiv g(\lambda),\qquad
J(\lambda) \equiv \Omega(\lambda)^{-1}\;\;\text{(defined only where $\Omega_{\varphi\alpha}\neq 0$)}.
$$

---

### 5.1.6 Diagnostics and pass/fail gates (explicit)

A run **passes** iff all gates pass on the gate set.

- **Gate G0 (grid refinement, eigen-solver convergence):**  
  For the circular ring ($\alpha=0$) at $\varphi=0.5$, require:
  $$
  \max_{0\le n< K}\frac{|E_n^{(401)}-E_n^{(201)}|}{1+|E_n^{(401)}|} \le 10^{-3}.
  $$

- **Gate G1 (flux periodicity sanity check):**  
  For circular ring ($\alpha=0$), require:
  $$
  \max_{\varphi\in\{0,0.25,0.5,0.75\}}\max_{0\le n<K}\frac{|E_n(\varphi+1,0)-E_n(\varphi,0)|}{1+|E_n(\varphi,0)|} \le 10^{-3}.
  $$

- **Gate G2 (QGT gauge invariance):**  
  Compute $Q(\lambda)$ by two phase-fixing methods (parallel transport vs anchor-phase) and require:
  $$
  \max_{\lambda\in\mathcal S_\lambda}\frac{\|Q^{(a)}(\lambda)-Q^{(b)}(\lambda)\|_F}{1+\|Q^{(a)}(\lambda)\|_F} \le 10^{-4},
  $$
  where $\mathcal S_\lambda=\{(\varphi,\alpha):\varphi\in[0,0.25,0.5,0.75],\alpha\in[0,1]\}$.

- **Gate G3 (metric PSD):**  
  Require $\lambda_{\min}(g(\lambda))\ge -10^{-10}$ for all $\lambda\in\mathcal S_\lambda$.

- **Gate G4 (Poisson/Jacobi check):**  
  On smooth test functions $f,g,h$ on parameter space,
  $$
  \{f,g\} = \nabla f^\top J \nabla g,\qquad
  \mathcal J = \{f,\{g,h\}\} + \{g,\{h,f\}\} + \{h,\{f,g\}\},
  $$
  require $\max_{\lambda\in\mathcal S_\lambda}|\mathcal J(\lambda)| \le 10^{-6}$ wherever $J$ is defined.

- **Nondegeneracy requirement (definition of $J$):**  
  Require $|\Omega_{\varphi\alpha}(\lambda)| \ge 10^{-8}$ on at least one $\lambda$ per geometry endpoint ($\alpha=0$ and $\alpha=1$). If violated, $J$ is declared undefined and the instrument fails.

---

### 5.1.7 New scripts/tools to be fabricated (paths)

Required new runner (or equivalent):

- `Derivation/code/physics/quantum_fractals/mqring_qgt/run_mqring_qgt_meter.py`

Required tests:

- `Derivation/code/tests/physics/quantum_fractals/mqring_qgt/test_qgt_gauge_invariance.py`
- `Derivation/code/tests/physics/quantum_fractals/mqring_qgt/test_poisson_jacobi.py`
- `Derivation/code/tests/physics/quantum_fractals/mqring_qgt/test_grid_convergence.py`

---

## 5.2 Experimental runplan

### 5.2.1 Resources employed to answer the question

- Compute eigenpairs $E_n,|\psi_n\rangle$ of $\hat H(\varphi,\alpha)$ for circular and fractal-border ring endpoints.
- Compute QGT on $(\varphi,\alpha)$ using symmetric finite differences and two phase-fixing methods.
- Derive $g$ and $\Omega$ and compute candidate $(M,J)$ where $\Omega_{\varphi\alpha}\neq 0$.
- Compute and store the gate metrics; declare pass/fail by the thresholds in §5.1.6 and the prereg in §5.1.1.

### 5.2.2 Exact Cartesian product of independent variables

Gate-critical runs are defined by the Cartesian product:

- `N ∈ {201, 401}`
- `alpha ∈ {0.0, 1.0}`
- `phi ∈ {0.0, 0.25, 0.5, 0.75}`

Plus required neighbor evaluations for finite differences:

- For each `(phi, alpha)` also evaluate `(phi±delta_phi, alpha)` and `(phi, alpha±delta_alpha)`.

### 5.2.3 Estimated runtime and compute budget (order-of-magnitude)

Runtime scales with sparse eigen-solves on an $N^2$ grid and $K=8$ eigenpairs. Budget is reported as:

- Per parameter point: one sparse eigensolve + QGT neighbor solves (constant-factor multiple).
- Total gate set: $2$ (N values) × $2$ (alpha) × $4$ (phi) × neighbor factor.

Exact wall-clock time is hardware-dependent; the gating plan is defined independently of timing.

### 5.2.4 Success and failure actions

- **Success (all gates pass):**
  - Produce a `RESULTS_T2_MQRing_QGT_Meter_v1.md` document with embedded figures, gate tables, and artifact links.
  - Un-quarantine the meter for reuse in higher-tier proposals (T3+), scoped to validated parameter ranges.

- **Failure (any gate fails):**
  - File a `CONTRADICTION_REPORT` describing the failing gate, parameter point(s), and suspected cause.
  - Quarantine the runner and artifacts; do not use outputs for any physics claim.
  - Only modifications that directly address the failure (e.g., resolution increase, phase-fixing fix) are allowed; rerun under a new tag version.

### 5.2.5 Publication/display plan

- Results will be published in a whitepaper-grade `RESULTS_*` document following `Derivation/Templates/RESULTS_PAPER_STANDARDS.md`, including:
  - Gate metrics table (pass/fail)
  - Spectrum plots (baseline)
  - QGT component tables
  - Provenance block (commit + hashes + tag)

---

## 6. Personnel

- **PI / implementer (Justin K. Lietz):** authors the proposal, implements the runner + tests, and ensures that artifact-writing runs are blocked until approval and preregistration requirements are satisfied.
- **Independent reviewer:** verifies that gates and preregistration are unambiguous and signs off in `APPROVALS.json` before non-preflight runs.

---

## 7. References

1. D. H. T. Tehrani, M. Solaimani, “Persistent currents and electronic properties of Mandelbrot quantum rings”, *Scientific Reports* **13**:5710 (2023). DOI: 10.1038/s41598-023-32905-w.  
2. `Derivation/Complete-Formalisms/CF1_QGT_to_Metriplectic_Brackets.md`  
3. `Derivation/Metriplectic/Constructive_QGT_to_Metriplectic/T1_PROPOSAL_G-QGT-1_QGT-to-Metriplectic_Mapping_v1.md`  
4. `Derivation/Unification/T0_Unification_Program_Spec_v1.md`