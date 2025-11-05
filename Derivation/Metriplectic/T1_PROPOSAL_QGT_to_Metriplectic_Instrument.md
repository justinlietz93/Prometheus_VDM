# T1 (Proto-model) — QGT → Metriplectic Instrument

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE

Short summary (TL;DR):  
Construct and validate an instrument that maps the Quantum Geometric Tensor (QGT) $Q_{\mu\nu}$ of a parametric state family $\lvert\psi(\theta)\rangle$ into metriplectic operators $(J,M)$ that satisfy skew-symmetry/PSD and degeneracy gates, with reproducible meters and artifacts.

Alignment:

- Canon anchors: [VDM-E-108](Derivation/EQUATIONS.md#vdm-e-108), [VDM-E-109](Derivation/EQUATIONS.md#vdm-e-109)
- Program: [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md)
- Policy/gates: [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md), [Derivation/code/common/io_paths.py](Derivation/code/common/io_paths.py:1)

Status: T1 (instrument proto-model). No new physics claims; only meters and construction validated by acceptance gates.

---

## 1. Scope and Goals

Given a differentiable state family $\theta\mapsto \lvert\psi(\theta)\rangle$ on a low-dimensional parameter manifold with QGT
$$
Q_{\mu\nu} \;=\; \langle \partial_\mu \psi \mid \partial_\nu \psi \rangle - \langle \partial_\mu \psi \mid \psi \rangle \, \langle \psi \mid \partial_\nu \psi \rangle
$$
and canonical split
$$
Q_{\mu\nu} \;=\; g_{\mu\nu} \;-\; \frac{i}{2}\,\Omega_{\mu\nu},
$$
this instrument constructs metriplectic operators $(J,M)$ on a reduced set of observables $F(\theta)$ such that:

- $J^\top=-J$ (skew-symmetry) derived from the Berry curvature $\Omega$,
- $M\succeq 0$ (positive semidefinite) derived from the quantum metric $g$,
- Degeneracy gates hold for chosen functionals $I,\Sigma$:
  - $\langle J\,\delta \Sigma,\,\delta \Sigma\rangle \approx 0$,
  - $\langle M\,\delta I,\,\delta I\rangle \approx 0$,
- Practical identities and QC meters mirror Metriplectic standards (two-grid, identity residuals), reusing canon meters and routing.

Outputs: PNG+CSV+JSON artifacts logged to canon paths; pass/fail by pre-registered gates.

---

## 2. Background & Rationale

Analogy: The QGT provides a Riemannian metric (real symmetric) and a symplectic form (imaginary antisymmetric). Metriplectic evolution requires exactly these ingredients: a skew-symmetric $J$ (Hamiltonian limb) and a symmetric PSD $M$ (metric limb). This instrument confirms that a constructive mapping $Q\mapsto(J,M)$ respects:

- Structure gates: $J^\top=-J$, $M\succeq 0$,
- Degeneracy gates (A4): $J\cdot \delta\Sigma=0$, $M\cdot \delta I=0$ at meter tolerance,
- QC meters for discrete composition when used as a limb in numerical flows (optional integration tests).

Canon references:

- QGT definitions: [VDM-E-108](Derivation/EQUATIONS.md#vdm-e-108), [VDM-E-109](Derivation/EQUATIONS.md#vdm-e-109)
- Metriplectic gates/usage context: [Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md](Derivation/Metriplectic/Metriplectic_JMJ_RD/RESULTS_Metriplectic_JMJ_RD_v1.md)

---

## 3. Instrument Construction

3.1 Inputs

- Parametric family $\lvert \psi(\theta)\rangle$ with $\theta\in\mathbb{R}^d$, $d\in\{1,2,3\}$.
- Orthonormalization fixed; phase gauge fixed (e.g., parallel-transport gauge) for stable $\Omega$ evaluation.
- Numerical derivatives $\partial_\mu \lvert\psi\rangle$ via complex-step or centered finite differences (documented tolerance).

3.2 Compute QGT

- Estimate $Q_{\mu\nu}$ on a grid in $\theta$ using inner products; separate $g_{\mu\nu}=\operatorname{Re} Q_{\mu\nu}$ and $\Omega_{\mu\nu} = -2\,\operatorname{Im} Q_{\mu\nu}$.

3.3 Map to (J,M)

- Define $M(\theta) = g(\theta)$ (symmetric, PSD by construction; numerically project negative eigenvalues below $\varepsilon_{\rm eig}$ to 0 and log them).
- Define $J(\theta)$ from $\Omega(\theta)$ as the linear operator induced by the 2-form: on the chosen basis, $J(\theta)$ is the matrix representation satisfying $J^\top=-J$ (enforce by $(J-J^\top)/2$ symmetrization and log residual norm).
- Choose observables/coordinates $q(\theta)$ so that the metriplectic evolution on $F(q)$ relates to tangent dynamics in $\theta$-space (documentation details captured in JSON).

3.4 Degeneracy choices

- Select $I=H$ (energy-like) and $\Sigma$ (entropy-like) as quadratic forms in $q$ with gradients spanning identity checks (details in run JSON). Tune coefficients (fixed set) such that degeneracy monitors test structure, not curve-fitting.

---

## 4. Meters and Acceptance Gates

Structural gates (per [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)):

- Skew-symmetry: $\|J+J^\top\|_\infty \le 1\times 10^{-12}$ (grid-refined); PASS/FAIL recorded.
- PSD check: all eigenvalues of $M$ $\ge -1\times 10^{-14}$; any negative eigenvalue is projected to 0 and logged; count of negatives must be 0 (strict PASS).
- Degeneracy monitors (grid-refined):
  - $g_1=\langle J\,\delta\Sigma,\,\delta\Sigma\rangle \le 1\times 10^{-10}$,
  - $g_2=\langle M\,\delta I,\,\delta I\rangle \le 1\times 10^{-10}$.

Consistency meters (report; informational at T1):

- Jacobi proxy for $J$: sample triplets $(f,g,h)$ from a basis and report median discrete Jacobi residual $\le 1\times10^{-8}$ (not a hard gate at T1).
- Condition numbers and stability of $Q$ estimation vs. derivative step (report curves; ensure robust window).

Artifacts (per tag):

- Figures: structure heatmaps (skew residuals), eigen-spectra of $M$, degeneracy histograms; optional Jacobi residual plot.
- CSV: per-grid structural metrics and degeneracy monitors.
- JSON: full provenance (commit, salted proposal hash, code_hashes), configuration, metrics, gates, verdicts.

Routing:

- Figures → Derivation/code/outputs/figures/metriplectic/qgt_to_metriplectic/  
- Logs → Derivation/code/outputs/logs/metriplectic/qgt_to_metriplectic/  
- IO helper: [Derivation/code/common/io_paths.py](Derivation/code/common/io_paths.py:1)

---

## 5. Methods

5.1 Parameter grid  
Define a hyper-rectangle in $\theta$ with $n_\mu$ points/axis (default $n_\mu\in\{9,11\}$). For each grid point:

- Evaluate $\lvert \psi\rangle$ and directional derivatives via complex-step (preferred) or centered finite difference (fallback).
- Assemble $Q$, extract $(g,\Omega)$, form $(M,J)$.

5.2 Numerical hygiene  

- Normalize $\lvert\psi\rangle$; enforce fixed global phase convention.  
- Complex-step step-size $h_c=10^{-20}$ (double precision safe); FD $h_f$ chosen by error model, report both when used.  
- Symmetrize/antisymmetrize once at the end of the construction to enforce exact algebraic properties to floating precision.

5.3 Degeneracy monitors  

- With fixed $I,\Sigma$ (documented in JSON), compute $g_1,g_2$ using gradients at the grid point and inner products induced by the chosen basis; log values and PASS/FAIL.

5.4 Optional composition test (informational)  

- Integrate a short-time metriplectic step with $(J,M)$ on a synthetic $F$ and confirm identity residuals and Lyapunov monotonicity (not a T1 gate; for T2 promotion planning).

---

## 6. Variables and Defaults

- Independent: grid points $\theta$, derivative method (complex-step, FD), seeds for noise-injected probes (if any).
- Dependent: $\|J+J^\top\|_\infty$, min-eig$(M)$, $g_1, g_2$, Jacobi residual median/IQR, condition numbers.
- Controls: step sizes, normalization tolerances, symmetrization toggles, projection thresholds.

Default configuration:

- $d=2$ parameter testbed; $11\times 11$ grid; complex-step on both axes; FD fallback off by default.

---

## 7. Acceptance Criteria

- Structure: PASS iff $\|J+J^\top\|_\infty \le 10^{-12}$ and min-eig$(M)\ge 0$ with zero negative eigenvalue count.  
- Degeneracy: PASS iff $g_1,g_2 \le 10^{-10}$ at all reported grid-refined checkpoints.  
- JSON must include gate verdicts, per-point metrics, CI/summary stats, and environment hashes.

Failure handling:

- Route artifacts to failed_runs/, emit contradiction JSON with metrics, diffs, and configuration snapshot; do not make claims.

---

## 8. Risks and Mitigations

- Gauge/phase instability: fix parallel-transport gauge; validate by small residuals in $\Omega$.  
- Numerical differentiation error: prefer complex-step; if FD required, perform step-size sweep and pick flat region.  
- PSD violations from noise: project tiny negative eigenvalues to 0; log counts; PASS requires 0.

---

## 9. Approvals & Provenance

Approvals required before artifact-emitting runs; see [Derivation/code/common/authorization/README.md](Derivation/code/common/authorization/README.md:1).  
All artifacts routed via io_paths; seeds and commit hash recorded.

---

## 10. Pre-registration JSON (template)

```json
{
  "proposal_title": "T1 - QGT to Metriplectic Instrument",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "Skew residual ||J+J^T||_inf <= 1e-12 across grid.", "direction": "no-change" },
    { "id": "H2", "statement": "M has no negative eigenvalues (count==0).", "direction": "no-change" },
    { "id": "H3", "statement": "Degeneracy monitors g1,g2 <= 1e-10.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["theta_grid","diff_method","seed"],
    "dependent": ["skew_res","min_eig_M","neg_eig_count","g1","g2","jacobi_median"],
    "controls": ["gauge","stepsize","symmetrize","project_eps"]
  },
  "pass_fail": [
    { "metric": "skew_res", "operator": "<=", "threshold": 1e-12, "unit": "-" },
    { "metric": "neg_eig_count", "operator": "==", "threshold": 0, "unit": "-" },
    { "metric": "g1", "operator": "<=", "threshold": 1e-10, "unit": "-" },
    { "metric": "g2", "operator": "<=", "threshold": 1e-10, "unit": "-" }
  ],
  "spec_refs": [
    "Derivation/EQUATIONS.md#vdm-e-108",
    "Derivation/EQUATIONS.md#vdm-e-109",
    "Derivation/Unification/T0_Unification_Program_Spec_v1.md"
  ],
  "registration_timestamp": "<ISO-8601>"
}
```

---

## 11. Specs & Schemas (skeleton)

Specs path (example):

- Derivation/code/physics/metriplectic/specs/qgt-to-metriplectic.v1.json

Schema path:

- Derivation/code/physics/metriplectic/schemas/qgt-to-metriplectic.v1.schema.json

Schema stub (minimum keys):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "qgt-to-metriplectic.v1.schema.json",
  "title": "QGT to Metriplectic - v1",
  "type": "object",
  "properties": {
    "theta_grid": { "type": "array", "items": { "type": "array", "items": { "type": "number" } }, "minItems": 2 },
    "diff_method": { "type": "string", "enum": ["complex_step","finite_difference"] },
    "stepsize": { "type": "number", "exclusiveMinimum": 0 },
    "gauge": { "type": "string", "enum": ["parallel_transport","fixed_phase"] },
    "symmetrize": { "type": "boolean" },
    "project_eps": { "type": "number", "minimum": 0, "default": 1e-14 }
  },
  "required": ["theta_grid","diff_method","gauge","symmetrize","project_eps"]
}
```

---

## 12. Deliverables

Per tag, emit:

- Figures: skew residual maps; $M$ eigenvalue spectra; degeneracy monitor histograms; optional Jacobi residuals.
- CSV: gridwise metrics (skew_res, min_eig_M, neg_eig_count, g1, g2).
- JSON: provenance, configuration, gate metrics, verdicts, hashes.

Paths:

- Figures → Derivation/code/outputs/figures/metriplectic/qgt_to_metriplectic/  
- Logs → Derivation/code/outputs/logs/metriplectic/qgt_to_metriplectic/

---

## 13. Escalation Path

- T2 (Instrument): freeze specs; add Jacobi gate and composition sanity tests; extend grids.  
- Bridge demos: apply $(J,M)$ in small metriplectic flows and compare meters with canonical metriplectic instruments for consistency (identity residuals, Lyapunov monotonicity).

---

## 14. References (canon anchors)

- [VDM-E-108](Derivation/EQUATIONS.md#vdm-e-108), [VDM-E-109](Derivation/EQUATIONS.md#vdm-e-109)  
- [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md)  
- [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md)
