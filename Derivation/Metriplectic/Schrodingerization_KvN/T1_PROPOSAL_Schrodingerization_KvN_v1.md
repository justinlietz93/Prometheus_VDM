<!-- White Paper Proposal based on Templates/PROPOSAL_PAPER_TEMPLATE.md -->

# T1 (Proto-model) - Schrödingerization (Koopman–von Neumann) Lifting of Metriplectic J ⊕ M to a Unified Hamiltonian Instrument

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> Short summary (one sentence TL;DR):  
> Lift the dissipative metriplectic evolution to a purely Hamiltonian Koopman–von Neumann system $i\,\partial_t\lvert\psi\rangle=\hat H_{\mathrm{KvN}}\lvert\psi\rangle$ that projects back to $J\oplus M$ with canon gates and reproducible artifacts.

Practical Provenance pattern (see template):

- Pre-register salted hashes and tag before any artifact-writing run; store base_sha256, salt_hex, salted_sha256 in PRE-REGISTRATION.json; tag must be included in run logs.

---

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz — Principal Investigator, approval authority

---

## 3. Abstract

Proposed is a T1 (Proto-Model) instrument to unify the metriplectic $J\oplus M$ evolution into a single reversible Hamiltonian flow by “Schrödingerization” (Koopman–von Neumann lifting). The canonical metriplectic equation $\,\dot q=J(q)\,\delta \mathcal I/\delta q + M(q)\,\delta \Sigma/\delta q\,$ (degeneracies and gates in canon) is lifted to a wavefunctional dynamics
$$
i\,\partial_t \,\lvert \psi\rangle \;=\; \hat H_{\mathrm{KvN}}\,\lvert \psi\rangle,
$$
[VDM-E-110](Derivation/EQUATIONS.md#vdm-e-110). A projection map recovers the metriplectic semigroup while preserving identity residuals, degeneracy gates, and Lyapunov monotonicity at the discrete level. The instrument defines the construction, diagnostics, and acceptance gates, and produces PNG+CSV+JSON artifacts via the io helper. This proposal does not claim new physics (T2+), only an instrument for unification and analysis (T1→T2).

---

## 4. Background & Scientific Rationale

Canon anchors and prior work:

- Metriplectic evolution and degeneracies: [VDM-E-104](Derivation/EQUATIONS.md#vdm-e-104), [VDM-E-101](Derivation/EQUATIONS.md#vdm-e-101).
- KvN lifting equation (spec-level): [VDM-E-110](Derivation/EQUATIONS.md#vdm-e-110), text source [schrodingerization.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/schrodingerization.md).
- Metriplectic proposals/results that certify $J$ skew, $M$ PSD, Strang diagnostics, and Noether baselines (instrument lineage):  
  - [PROPOSAL_Metriplectic_SymplecticPlusDG.md](Derivation/Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md)  
  - [PROPOSAL_Metriplectic_JMJ_RD_v1.md](Derivation/Metriplectic/Strang_Defect_vs_dt_kg_RD/PROPOSAL_Metriplectic_JMJ_RD_v1.md)  
  - [RESULTS_Metriplectic_Structure_Checks.md](Derivation/Metriplectic/RESULTS_Metriplectic_Structure_Checks.md)  
  - [RESULTS_KG_Noether_Invariants_v1.md](Derivation/Metriplectic/RESULTS_KG_Noether_Invariants_v1.md)  
  - [RESULTS_KG_Jonly_Locality_and_Dispersion.md](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md)

Motivation and positioning:

- A single reversible generator eases analysis of invariants, projection errors, and stability bands while maintaining metriplectic acceptance gates.  
- KvN lifting provides a constructive test-bed for “M as necessary shadow of J” (projection viewpoint) without asserting a phenomenon claim (remains T1/T2 instrument domain).  
- The instrument strengthens prereg paths that need unified actions (e.g., cosmology pipeline notes) while staying within canon discipline.

Assumptions and limitations:

- Discrete-to-continuum consistency is checked numerically (identity residuals, reversibility, two-grid slopes) rather than proven abstractly here (that belongs in separate theory notes).  
- Projection operator design is specified for the experiment classes targeted (KG⊕RD baselines); generalization is future work.

---

## 5. Intellectual Merit and Procedure

- Importance: Unifies analysis by embedding $J\oplus M$ in a single Hamiltonian generator suitable for verification of degeneracy and Lyapunov behavior through projection diagnostics.  
- Broader impacts: Provides a standard instrument to contrast projection-induced dissipation against explicit $M$ steps, clarifying meter semantics for causality and entropy budgets.  
- Approach: Construct $\hat H_{\mathrm{KvN}}$ and a projection $\Pi$ such that
  $$
  \Pi\!\left(e^{-i\,\Delta t\,\hat H_{\mathrm{KvN}}}\lvert \psi\rangle\right)\;\approx\; \Phi^{J\oplus M}_{\Delta t}\big(\Pi\lvert\psi\rangle\big),
  $$
  and quantify approximation by canon gates (identity residuals, $\Delta L_h\le 0$, degeneracies).

---

## 5.1 Experimental Setup and Diagnostics

Known parameters (dimensionless normalization consistent with [UNITS_NORMALIZATION.md](Derivation/UNITS_NORMALIZATION.md)):

- Temporal step and horizon: $\Delta t$, $T$; grid sizes $N$, $\Delta x$.  
- Model knobs for baselines: $(c,m)$ for KG limb; RD coefficients $(D,r,u)$ for $M$-limb comparators.  
- KvN construction parameters: choice of basis/functions for $\lvert\psi\rangle$, truncation level $K$, projection operator family $\Pi_\alpha$ (hyperparameters $\alpha$).

Diagnostics and meters (counts indicate minimum per run):

- Identity residuals (1): $\lVert \Phi^{\mathrm{KvN}}_{\Delta t\to -\Delta t}-\mathrm{Id}\rVert_\infty \le 10^{-12}$ (reversibility check on lifted system).  
- Projection error (1): $\varepsilon_{\Pi} = \lVert \Pi\circ \Phi^{\mathrm{KvN}}_{\Delta t}-\Phi^{J\oplus M}_{\Delta t}\circ \Pi\rVert$ tracked vs $\Delta t$, $K$, $N$.  
- Degeneracy monitors (2): $\langle J\,\delta\Sigma,\delta\Sigma\rangle\approx 0$; $\langle M\,\delta I,\delta I\rangle\approx 0$ [VDM-E-101](Derivation/EQUATIONS.md#vdm-e-101).  
- Lyapunov monotonicity (1): discrete $\,\Delta L_h\le 0\,$ under projected metric limb [VDM-E-099](Derivation/EQUATIONS.md#vdm-e-099).  
- Two-grid order (1): slope $\ge 2.90$ on designated norms for Strang-like comparators when used (informational).

New tooling/scripts (paths to be committed prior to runs):

- KvN builder: Derivation/code/physics/metriplectic/kvn/builder.py  
- Projection utilities: Derivation/code/physics/metriplectic/kvn/projection.py  
- Runner: Derivation/code/physics/metriplectic/kvn/run_kvn_lift.py

Required parameters and defaults (example T1 set, unit-consistent):  

- $(N,\Delta x,\Delta t,T)=(256,1.0,5\times 10^{-3},50)$; seeds $=$ 10; $(c,m)=(1.0,0.5)$; $(D,r,u)=(1.0,0.2,0.25)$; $K=32$; $\alpha=\{ \text{orth proj},\text{DG-consistent} \}$.

### 5.1.1 Pre-Run Config Requirements

- APPROVALS and schema/spec plumbing must exist before any artifact-writing run; approval is required (see [authorization/README.md](Derivation/code/common/authorization/README.md)).

Required config and metadata:

- Approvals manifest: Derivation/code/physics/metriplectic/APPROVAL.json  
- Schemas dir: Derivation/code/physics/metriplectic/schemas/  
  - kvn-lift.v1.schema.json  
- Specs dir: Derivation/code/physics/metriplectic/specs/  
  - kvn-lift-run.v1.json

PRE-REGISTRATION.json (minimum keys, values to be filled at prereg):

```json
{
  "proposal_title": "T1 - KvN Schrödingerization of Metriplectic J+M",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "KvN lifting reproduces J⊕M step to first order with bounded projection error εΠ at fixed (Δt,K,N).", "direction": "no-change" },
    { "id": "H2", "statement": "Reversibility on lifted system achieves identity residual ≤ 1e-12 across seeds.", "direction": "decrease" }
  ],
  "variables": {
    "independent": ["Δt","K","N"],
    "dependent": ["εΠ","identity_residual","two_grid_slope"],
    "controls": ["c","m","D","r","u","seed"]
  },
  "pass_fail": [
    { "metric": "identity_residual", "operator": "<=", "threshold": 1e-12, "unit": "-" },
    { "metric": "two_grid_slope", "operator": ">=", "threshold": 2.90, "unit": "-" }
  ],
  "spec_refs": ["Derivation/code/physics/metriplectic/specs/kvn-lift-run.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

Specs (example):

```json
{
  "run_name": "kvn-lift-baseline",
  "version": "1.0.0",
  "tag": "kvn-lift.v1",
  "schema_ref": "Derivation/code/physics/metriplectic/schemas/kvn-lift.v1.schema.json",
  "parameters": { "N": 256, "dx": 1.0, "dt": 0.005, "T": 50, "c": 1.0, "m": 0.5, "D": 1.0, "r": 0.2, "u": 0.25, "K": 32, "proj_kind": "orth" },
  "seeds": [0,1,2,3,4,5,6,7,8,9]
}
```

Schemas (skeleton):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "kvn-lift.v1.schema.json",
  "title": "KvN Schrödingerization Lift - v1",
  "type": "object",
  "properties": {
    "N": { "type": "integer", "minimum": 8 },
    "dx": { "type": "number", "exclusiveMinimum": 0 },
    "dt": { "type": "number", "exclusiveMinimum": 0 },
    "T": { "type": "number", "exclusiveMinimum": 0 },
    "K": { "type": "integer", "minimum": 4 },
    "proj_kind": { "type": "string", "enum": ["orth","dg-consistent"] }
  },
  "required": ["N","dx","dt","T","K","proj_kind"]
}
```

---

## 5.2 Experimental runplan

Plan of use:

- Build $\hat H_{\mathrm{KvN}}$ for the chosen baseline (KG⊕RD references available in metriplectic canon), choose $\Pi_\alpha$, and execute a seed sweep across $(\Delta t,K,N)$.
- Record:
  - Identity residual (lifted reversibility), projection error metrics $\varepsilon_{\Pi}$, two-grid slope, and degeneracy monitors pulled through the projection.

Success criteria (pass gates):

- Identity residuals $\le 10^{-12}$ across seeds (lifted reversibility).  
- Two-grid slope $\ge 2.90$ (Strang-comparable informational check when applicable).  
- Degeneracy monitors consistent with [VDM-E-101](Derivation/EQUATIONS.md#vdm-e-101); projected $\Delta L_h \le 0$ per step [VDM-E-099](Derivation/EQUATIONS.md#vdm-e-099).  
- Projection error $\varepsilon_{\Pi}$ bounded and decreasing under refinement (profile documented).

Failure actions:

- Route artifacts to failed_runs/; emit contradiction report JSON with seed, commit/tag, and gate diffs; no narrative claims are made.

Artifacts and routing:

- Figures: Derivation/code/outputs/figures/metriplectic/kvn/  
- Logs (CSV, JSON): Derivation/code/outputs/logs/metriplectic/kvn/  
- All paths go through [io_paths.py](Derivation/code/common/io_paths.py) with deterministic seeds and commit hashes recorded.

Compute budget:

- Estimated runtime per run: O(minutes) on CPU for $(N=256,K=32,T=50)$; total budget scaling linearly with seeds and grid refinements.

---

## 6. Personnel

- Justin K. Lietz — design, approvals, and review; ensures adherence to authorization and artifact policies; signs prereg tags; reviews metrics vs [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md).

---

## 7. References

- Schrödingerization/KvN overview: [schrodingerization.md](PRIVATE/Axiom-8/Status/T8-A8_Insights/Collections/schrodingerization.md)  
- Canon equations: [EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-110), [EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-104), [EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-101), [EQUATIONS.md](Derivation/EQUATIONS.md#vdm-e-099)  
- Authorization policy: [authorization/README.md](Derivation/code/common/authorization/README.md)  
- Results standards: [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md)

---
