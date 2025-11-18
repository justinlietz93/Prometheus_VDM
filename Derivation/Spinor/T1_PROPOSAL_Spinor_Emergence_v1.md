# T1 (Proto-model) - Spinor Emergence from the VDM J‑Limb (Dirac Sector from a Scalar Void Lattice)

> Created Date:  2025-11-18  
> Commit: {git rev-parse HEAD}  
> Salted provenance: {salted_hash}  
> Proposer contact(s):  (<justin@neuroca.ai>)  
> License: See [LICENSE](/LICENSE.md)  
> Short summary (one sentence TL;DR):  

## 2. List of proposers and associated institutions/companies
Justin K. Lietz (PI, theory & numerics), Neuroca (infrastructure).

## 3. Abstract
Proposed in this document is a constructive derivation of effective Dirac spinors from the conservative (J‑limb) of the Void Dynamics Model’s discrete action. The objective is to replace deprecated particle–triad analogies with a falsifiable spinor sector built from the lattice micro‑dynamics, using three complementary constructions: (i) **domain‑wall (Jackiw–Rebbi‑style) modes** of the tachyonic potential yielding chiral bound states and an effective low‑energy Dirac operator along interfaces; (ii) **staggered‑spinor (doubling‑controlled) field redefinitions** that map the second‑order lattice wave operator to a first‑order Dirac form at long wavelengths; and (iii) a **local Jordan–Wigner/Majorana pair factorization** on bipartite sublattices, establishing emergent Clifford algebra and spin‑statistics via band geometry. Success is declared only if algebraic and symmetry gates (below) pass with rigorous proofs and audit logs.

## 4. Background & Scientific Rationale
- Canonical discrete action and KG limit define the reversible J‑limb. The goal is to realize fermionic excitations as **emergent** defect/band‑geometry degrees of freedom without adding new primitives.  
- Motivation: closes the S5 gap by providing a sector where baryon‑like charges become Noether charges under J‑limb symmetries; violations are then confined to cosmogenesis regimes.  
- Prior meters (Noether, locality/dispersion) already pass on the J‑limb substrate; this proposal stays theory‑first (proofs + toy numerics for visualization only).

## 5. Intellectual Merit and Procedure
**(1)** Importance: establishes matter degrees of freedom inside VDM from first principles.  
**(2)** Broader impacts: unlocks phenomenology (baryogenesis analogues, stability) without extra axioms.  
**(3)** Approach: three constructive lines with shared acceptance gates.  
**(4)** Rigor: lemmas ≤3 lines where possible; proofs logged; independence from external postulates.

## 5.1 Experimental Setup and Diagnostics (theoretical meters)
- **C1 — Clifford algebra gate:** Construct local γ^μ on coarse cells with `{γ^μ, γ^ν}=2η^{μν}` to O(a^2).  
- **C2 — Dirac reduction gate:** Linearization of the discrete Euler–Lagrange equation around an interface produces a first‑order Dirac operator for the bound mode manifold up to controlled remainders; dispersion linear near k=0.  
- **C3 — Spin‑statistics/Berry gate:** Two‑state bundle over Brillouin torus exhibits spin‑½ monodromy; Berry curvature integrates to the required topological invariant; 2π rotation acquires a sign.  
- **C4 — Anomaly accounting:** Lattice doubling accounted; chiral charge nonconservation localized to defects; consistency with discrete Noether currents.
- **Deliverables:** proof PDFs + minimal visual numerics (mode profiles, band sketches); JSON proof registry.

### 5.1.1 Pre-Run Config Requirements (registries)
- **Approvals:** `Derivation/code/physics/spinor/APPROVAL.json` (requires approval before artifact‑writing).  
- **Schemas:** `Derivation/code/physics/spinor/schemas/spinor-proof.schema.json`  
- **Specs:** `Derivation/code/physics/spinor/specs/spinor-emergence.v1.json`

### PRE-REGISTRATION.json
```json
{
  "proposal_title": "Spinor Emergence from the VDM J-Limb",
  "tier_grade": "T1",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "There exists a local coarse-cell mapping producing a Clifford algebra {γ^μ,γ^ν}=2η^{μν} to O(a^2).", "direction": "no-change" },
    { "id": "H2", "statement": "Interface-bound modes obey an effective Dirac equation with linear dispersion near k=0.", "direction": "no-change" },
    { "id": "H3", "statement": "Berry curvature certifies spin-1/2 monodromy for the two-state bundle.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["lattice spacing a", "coupling J", "potential parameters (α,β,λ)", "interface width"],
    "dependent": ["algebra residual ε_C", "dispersion linearity R2", "Berry index I_B"],
    "controls": ["boundary conditions", "coarse-graining window", "proof discretization order"]
  },
  "pass_fail": [
    { "metric": "ε_C", "operator": "<=", "threshold": 1e-12, "unit": "" },
    { "metric": "R2", "operator": ">=", "threshold": 0.999, "unit": "" },
    { "metric": "I_B", "operator": "==", "threshold": 1, "unit": "integer" }
  ],
  "spec_refs": ["Derivation/code/physics/spinor/specs/spinor-emergence.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

## 5.2 Workplan (derivation steps)
1) Define interface background and linearize discrete action; isolate bound‑state manifold.  
2) Construct γ^μ via staggered field redefinition; prove Clifford relations to O(a^2).  
3) Compute Berry curvature for the two‑state band; certify spin‑½ monodromy.  
4) Prove current conservation and locate anomaly budget at defects.  
**Failure plan:** If any gate fails, issue CONTRADICTION_REPORT with lemma id, counterexample, and affected S5 claims.

## 6. Broader impacts
Enables matter sector, paves path to baryogenesis analogues and proton‑stability regimes inside VDM.

