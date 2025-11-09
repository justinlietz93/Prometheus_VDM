# CFx: Complete Formalism — {Complete Formalism Title}

Date: {YYYY-MM-DD}  
Status: Template — replace placeholders and remove this line  
Gap Module: {S# from T0_Unification_Program_Spec_v1.md}  
Proposer: {Your Name}  
License: See LICENSE

---

## Executive Summary

Purpose: State the physical objective and scope in 3–5 sentences. Identify which VDM axioms are exercised and what is being proven or constructed at the formal level. This written CF document owns the derivation; notebooks must be exact code recreations, not new derivations.

Contributions (bulleted, each traceable to an anchor or algorithm):

- Formal definitions, identities, or theorems established here and linked into canon.
- Constructive algorithms (subject-only links to VDM-A-### anchors).
- Validation gates (subject-only links to Validation Metrics canon).
- Worked example specification (inputs/expected diagnostics; no plots, no code).

Do NOT duplicate registry numbers, constants, or equations that belong to canon; link by anchor only.

---

## Canon Registries and Policies (anchors only; no duplication)

- Equations registry: [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md)
- Algorithms registry: [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md)
- Validation metrics: [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)
- Symbols and units: [SYMBOLS.md](../SYMBOLS.md), [UNITS_NORMALIZATION.md](../UNITS_NORMALIZATION.md)
- I/O helper (runners only): [io_paths.py](../code/common/io_paths.py)
- Results standards: [RESULTS_PAPER_STANDARDS.md](../Writeup_Templates/RESULTS_PAPER_STANDARDS.md)
- Proposal template (for upstream experiments): [PROPOSAL_PAPER_TEMPLATE.md](../Writeup_Templates/PROPOSAL_PAPER_TEMPLATE.md)

Policy:

- Subject-only link labels: visible text must be titles/anchors (no raw paths displayed).
- Canon discipline: this file narrates and references; it does not reproduce equations, numeric constants, or registry IDs from the canonical registries.
- All measurable statements must map to unit-consistent observables and to gates defined in Validation Metrics.

---

## Read Me First (Template Rules)

- 1:1 mapping: This written CF must mirror the intended notebook CFx exactly (same numbering, same subsections). The notebook is a code recreation of this document; it adds executable meters and commentary after each code cell but does not introduce new derivations.
- Use anchors, not copies: Every equation or criterion that is canonical is linked by anchor (e.g., VDM-E-140) using the Equations registry; do not restate math or thresholds in this document.
- Units: State units and normalization choices by linking to the units registry; carry units textually where needed for clarity, but do not restate canonical normalization tables.
- Gates: Pair each claim or construct with the applicable gate(s) from Validation Metrics (by anchor), and specify what observable(s) the gate acts on (names, units).
- Scope control: Advanced topics beyond formal necessities live in the “Advanced Topics” section as pointers only.

---

### Lattice–Exactness & UQ Pack (Optional Template Insert)

Use this insert when the CF benefits from lattice-QCD-grade sampling exactness and uncertainty quantification. Integrate via anchor-only references; do not restate formulas or thresholds.

- Sampling exactness and integrators (HMC/RHMC)
  - Equations: link ΔH energy error, reversibility/area-preservation identities in [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md)
  - Algorithms: leapfrog / Sexton–Weingarten split, RHMC in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md)
  - Validation: acceptance vs stepsize curve, ΔH histogram, reversibility residuals in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)

- Autocorrelation and error bars
  - Equations: integrated autocorrelation time τ_int definitions in [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md)
  - Algorithms: windowed τ_int estimators; binning with B ≥ 2 τ_int; blocked jackknife/bootstrap in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md)
  - Validation: bin-stability of mean/variance; resample CIs in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)

- Correlated fits with SVD regularization
  - Equations: correlated χ² with full covariance in [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md)
  - Algorithms: SVD truncation of near-null modes in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md)
  - Validation: χ²_dof and parameter stability vs cutoff in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)

- RG blocking and scaling collapse
  - Algorithms: block-spin/field transforms with rescaling in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md)
  - Validation: scaling collapse across s ∈ {2,4} with envelope metric in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)

- Large-sparse solvers and preconditioning
  - Algorithms: CG/BiCGStab, even–odd (red–black) preconditioning, multi-shift in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md)
  - Validation: convergence per RHS, residual norms, and iteration budgets in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)

Provenance example (optional external reference):

- [Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf](../References/Lattice-Field-Theory_&_Discrete-Action-Principles/Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf)

---

## 1. Foundations and Setting

Describe the mathematical/physical setting (e.g., manifold, field space, state vectors) and name the objects that will be constructed.

### 1.1 Definitions

List named objects with short descriptions, each mapped to canonical symbols or to new symbols proposed here.

Required:

- Symbol inventory (referencing [SYMBOLS.md](../SYMBOLS.md) where existing).
- Dimension and units for each primary variable (reference [UNITS_NORMALIZATION.md](../UNITS_NORMALIZATION.md)).

### 1.2 Structural Forms and Identities

State the structural objects (e.g., forms, brackets, metrics) and identities used in the remainder.

- Link identities to Equations canon anchors (subject-only labels).
- If identities are derived here, provide the derivation steps, but place the equation itself as a reference to a new anchor you register in Equations canon via a separate PR (do not inline the final formula here).

### 1.3 Equilibrium/Constraint Manifolds (if applicable)

Describe any constraint submanifolds or equilibrium sets, the pullbacks/restrictions, and the conditions that define them.

- State which gates will later verify these conditions in code (unit names and anchor links only).

---

## 2. Generators and Evolution Law

Define the generators and the evolution law in the minimal terms necessary for downstream code recreation.

### 2.1 Generator Definitions

- Name each generator (e.g., energy-like I, entropy-like Σ, Hamiltonian H, free energy F) and map it to canon anchors when applicable.
- Provide the measurable observables these act upon (with units).

### 2.2 Evolution Structure (Anchor-only)

Reference the evolution law by anchor(s) in the Equations canon; e.g.:

- GENERIC/metriplectic form: link to the appropriate VDM-E-### anchor in [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md)
- Degeneracy conditions: link to the corresponding VDM-E-### anchor
- Entropy production/Lyapunov monotonicity (anchor link)

Do not restate the equations here.

### 2.3 Noether and Invariants (if applicable)

Reference the invariants and their verification gates (anchor-only), and specify unit-consistent observables.

---

## 3. Domain Identities and Thermodynamic/Geometric Relations

Provide domain-specific relations (thermodynamics, geometry, etc.) and how they constrain or inform the construction.

### 3.1 Primary Relations (Anchor-only)

List the relations with anchor links to the Equations registry and any involved Algorithms.

### 3.2 Derived Relations (Proof Sketches)

Provide succinct derivation sketches (text) with assumptions/limitations explicitly listed. Equations themselves are referenced by anchors; do not inline canonical formulas.

### 3.3 Measurement/Observable Map

Map each theoretical quantity to its measurable counterpart (names, units, how computed in code). State which gates test each mapping (Validation Metrics anchors).

---

## 4. Mapping and Decomposition (if applicable)

Describe constructive mappings (e.g., to metriplectic/GENERIC) and decomposition steps.

### 4.1 Structure Checks

List structure properties to verify (e.g., antisymmetry, PSD), and link each to gates in Validation Metrics.

### 4.2 Degeneracy Conditions

Name the degeneracy conditions and link to anchors; specify which observables are expected to be zero (or within tolerance) under projector enforcement.

### 4.3 Mapping Residuals

Define how residuals will be computed and summarized (e.g., R², min/median/max norms) in the paired notebook; do not include code.

---

## 5. Constructive Algorithm

Provide a stepwise, implementation-agnostic algorithm (pseudocode-style prose). Reference Algorithms canon anchors for any reusable components.

Checklist:

- Inputs (with units and normalization references).
- Steps (each linked to any relevant Equations/Algorithms anchors).
- Outputs: named observables/logs to be emitted by the notebook; specify expected dimensionality/shape and units where relevant.

Template Note — Lattice–Exactness & UQ implementation hints (remove if not used):

- If sampling-based: specify HMC/RHMC trajectory length, integrator step size ladder ε, splitting scheme; define recorded diagnostics: ΔH per trajectory, acceptance α, reversibility residual, and Jacobian determinant proxy.
- If correlated data fitting: state whether full covariance is used and SVD cutoff selection rule; plan a cutoff sweep for stability plots.
- If chains: specify τ_int estimator(s), bin size B and a rule B ≥ 2 τ_int; define blocked jackknife/bootstrap parameters.
- If scale-program: specify blocking factors s, rescaling rules, and collapse envelope metric to be reported.
- If sparse solvers: name preconditioner, stopping criteria, and multishift usage; log per-iteration residuals and totals.
- Route artifacts via [io_paths.py](../code/common/io_paths.py) and ensure IEEE‑754 doubles and deterministic seeds are used; record commit hash and seeds in JSON logs.

---

## 6. Worked Example (Specification)

Define a minimal worked example (parameters, units, initial conditions). This section is a specification only; implementation and figures live in the paired notebook and in runner-produced artifacts.

Provide:

- Parameter table (names, units, values/ranges).
- Expected qualitative behavior and which gates test it (anchors only).
- Data products/figures to be generated by runners (paths via io_paths, not inline here).

---

## 7. Advanced Topics (Pointers Only)

List advanced extensions or variations and link to references or other CF documents. Provide subject-only link labels; do not restate derivations here.

---

## 8. Integration with VDM Unification

Explain how this CF connects to the broader program (e.g., gap modules, T0/T1 instruments, or other CFs). Use subject-only links to relevant documents (e.g., Unification spec, other CF files).

---

## 9. Validation and Consistency

State the precise gates that apply and what constitutes acceptance, with anchors to Validation Metrics.

### 9.1 Mathematical Consistency

List the structure/identity checks and their associated anchors; name the observables and tolerances (tolerances by reference only; do not restate numeric thresholds).

### 9.2 Physical Consistency

List physically meaningful checks (e.g., monotonicity, conservation) and their anchors; specify observables/units.

### 9.3 Numerical Validation (Notebook Pairing)

State the grid/parameter sweeps or sampling required in the notebook and what summary statistics will be reported; refer to runner pipelines for figure/CSV/JSON artifacts.

### 9.4 Lattice–Exactness & UQ Gates (Optional)

- Sampling exactness (HMC/RHMC):
  - Acceptance vs stepsize ε follows predicted scaling band (anchor in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md))
  - ΔH histogram symmetric with expected mean/variance scaling (anchors in [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md), [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md))
  - Reversibility residual and volume preservation within tolerances (anchors in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md))

- Autocorrelation and error bars:
  - τ_int estimates agree within estimator spread; bin-stability achieved at B ≥ 2 τ_int (anchors in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md), [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md))

- Correlated fits (SVD):
  - χ²_dof and parameters stable across a range of SVD cutoffs; report chosen cutoff rationale (anchors in [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md), [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md))

- RG blocking/scaling:
  - Scaling collapse across s with envelope metric below threshold (anchors in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md), [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md))

- Sparse-solver performance:
  - Convergence within iteration budget; residual norms below threshold; preconditioning benefit quantified (anchors in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md), [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md))

---

## 10. References

Cite external literature only when necessary; prefer links to internal canon. Use subject-only labels for internal links.

---

## Appendix A: Symbol Definitions

If new symbols are introduced, define them here and open a PR to add them to [SYMBOLS.md](../SYMBOLS.md). Do not duplicate existing definitions here.

---

## Appendix B: Notebook Pairing & Traceability

- Paired notebook: [CFx — {Notebook Title}](../Notebooks/{Domain}/CFx_{Notebook_Title}.ipynb)
- 1:1 mapping promise: Every numbered subsection in this CF has a corresponding notebook segment with executable meters and commentary, maintaining identical numbering.
- Traceability map (example; update for your CF):

| CF Section | Notebook Cell/Tag | Meters/Gates (anchors) | Observables/Units |
|------------|--------------------|-------------------------|-------------------|
| 1.1        | tag: cf-1-1        | [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md) | {name, unit} |
| 2.2        | tag: cf-2-2        | [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md), [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md) | {name, unit} |
| 4.3        | tag: cf-4-3        | [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md) | {name, unit} |

Notes:

- Subject-only link labels throughout.
- No file I/O occurs in notebooks; all artifacts (PNG/CSV/JSON) are emitted by approved runners via [io_paths.py](../code/common/io_paths.py).
- After any canonical update, record provenance in CHRONICLES (date, commit, anchors touched).

---

## Appendix C: Lattice–Exactness & UQ Pack Checklist (Optional)

Anchors inserted (by section):

- [ ] Section 2: ΔH diagnostics, reversibility/volume-preservation, and evolution structure anchors linked in [00_EQUATIONS.md](../z.CANONICAL_Equations/00_EQUATIONS.md)
- [ ] Section 5: HMC/RHMC or solver algorithm anchors linked in [00_ALGORITHMS.md](../z.CANONICAL_Algorithms/00_ALGORITHMS.md)
- [ ] Section 6: Sampling/batching parameters and binning rules mapped to gates in [00_VALIDATION_METRICS.md](../z.CANONICAL_Validation_Metrics/00_VALIDATION_METRICS.md)
- [ ] Section 9: Gate definitions for acceptance, τ_int/binning, correlated χ² stability, scaling collapse, and solver convergence (anchors only)

Observables and units declared:

- [ ] ΔH [energy units per [UNITS_NORMALIZATION.md](../UNITS_NORMALIZATION.md)]
- [ ] Acceptance α [%]
- [ ] τ_int [steps], bin size B [steps]
- [ ] Covariance eigenvalues (dimensionless), SVD cutoff index k
- [ ] Blocking factor s and collapse envelope E_max [unitless]
- [ ] Solver residual ||r||₂ [same units as RHS], iteration counts

Provenance:

- [ ] External reference used: [Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf](../References/Lattice-Field-Theory_&_Discrete-Action-Principles/Lattice Methods for Quantum Chromodynamics -- Thomas A Degrand; Carleton Detar.pdf) (optional; prefer internal canon)
- [ ] Added CHRONICLES entry after merge

---

## Assumptions and Limitations

List all assumptions used in derivations and any limitations on applicability (domains, boundary conditions, scales). When possible, pair each limitation with a gate or a proposed robustness check.

---

## Acceptance Checklist (remove after completion)

- [ ] All sections completed and numbered 1:1 with the planned notebook.
- [ ] Every equation/threshold references canon by anchor; no duplication.
- [ ] Units and symbol usage align with [SYMBOLS.md](../SYMBOLS.md) and [UNITS_NORMALIZATION.md](../UNITS_NORMALIZATION.md).
- [ ] Validation gates are listed with anchors and mapped to observables.
- [ ] Worked example specified (parameters/units) without code or plots.
- [ ] Notebook pairing and traceability table filled with tags and anchors.
- [ ] Subject-only link labels verified (no raw paths visible).
- [ ] Provenance prepared for CHRONICLES after merge.
