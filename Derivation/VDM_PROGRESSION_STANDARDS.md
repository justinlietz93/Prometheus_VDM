<!-- DOC-GUARD: CANONICAL -->
# VDM Progression Standards (Theory Constitution)

Last updated: 2025-10-15

**Scope:** Canonical rules for progression of theoretical claims from concept to physical law within the Void Dynamics Model. This document parallels [AXIOMS.md](AXIOMS.md) but defines progression rules rather than theory content.

**Rules:**

- GitHub-safe MathJax only ($...$ inline; no block environments).
- All progression decisions reference these standards.
- Status tags and tier definitions must align with these rules.

---

## I. Status Tags (Concept → Physical Law)

Four status tags govern all theoretical claims in VDM. Each claim in the theory must carry exactly one tag.

### [DISPROVEN]  <a id="status-disproven"></a>

**Definition:** A claim that has been explicitly falsified by computational or logical evidence.

**Requirements:**
- Evidence showing the claim fails to meet its gate criteria
- Or logical proof of inconsistency with established axioms
- Must be documented in negative controls section

**Promotion path:** None (terminal state)

**Examples:**
- "RD/Fisher–KPP has a causal cone with speed $2\sqrt{D r}$" (exponential tails visible for any $t>0$)
- "Site-wise conservation of $Q$ under diffusion" (lattice $\Delta Q\ne 0$ beyond tolerance)

**Source:** `CANON_PROGRESS.md` §D "Negative controls"

---

### [PLAUSIBLE]  <a id="status-plausible"></a>

**Definition:** A claim with theoretical motivation and preliminary evidence, but lacking complete validation infrastructure.

**Requirements:**
- Theoretical derivation from axioms OR compelling analogy to validated systems
- Preliminary numerical checks OR structural arguments
- Defined acceptance gates (quantitative pass/fail criteria)
- Proposal document (in `Derivation/<Domain>/PROPOSAL_*.md`)

**Promotion path:** → [PLAUSIBLE→PROVEN] → [PROVEN]

**Examples:**
- Telegraph-RD hyperbolic regularization (hyperbolic flux restores cone)
- Memory/Agency field $C(x,t)$ step response ($C_{ss}\approx (\gamma/\delta)R_0$, $\tau\approx 1/\delta$)
- Dark Photons decoherence portals (Fisher consistency and noise budget)

**Source:** `CANON_PROGRESS.md` §B "Domain claims"

---

### [PLAUSIBLE→PROVEN]  <a id="status-plausible-to-proven"></a>

**Definition:** Intermediate state during active validation; used when transitioning evidence is being assembled.

**Requirements:**
- All [PLAUSIBLE] requirements met
- Validation runner implemented
- Partial evidence artifacts (some figures/CSV/JSON)
- Gate criteria formalized in `VALIDATION_METRICS.md`

**Promotion path:** → [PROVEN]

**Time limit:** Should not persist >1 sprint without progression

**Source:** `CANON_PROGRESS.md` line 81 "Promotion rules"

---

### [PROVEN]  <a id="status-proven"></a>

**Definition:** A claim that has passed all acceptance gates with pinned computational artifacts.

**Requirements (ALL must be satisfied):**
- Runner script name (e.g., `run_rd_front_speed.py`)
- Output CSV/JSON data in `Derivation/code/outputs/logs/`
- Visualization figure in `Derivation/code/outputs/figures/`
- Gate criteria met with explicit numbers (e.g., "Gate met: $v\approx 0.998$; $R^2\approx 0.99985$")
- RESULTS document in `Derivation/<Domain>/RESULTS_*.md`
- Entries in `CANON_PROGRESS.md` with all evidence paths

**Promotion path:** None (terminal state, canonical physics)

**Examples:**
- J-only (KG) locality cone: $v_{\text{front}}$ within 2% of $c$
- RD Fisher–KPP front speed: rel-err $\le 5\%$, $R^2 \ge 0.999$
- Noether energy/momentum conservation: drift $\le 10^{-12}$

**Source:** `CANON_PROGRESS.md` lines 4, 19-26, 80-81

---

## II. Tier Structure (Evidence Strength)

Claims are organized into tiers reflecting their evidentiary status and role in the theory.

### Tier A — Proven Canonical Physics  <a id="tier-a"></a>

**Definition:** Quantitative claims backed by artifact-pinned validations.

**Requirements:**
- Status: [PROVEN]
- All gate criteria passed with documented margins
- Reproducible via committed runners
- Multiple validations across parameter regimes (preferred)

**Canonical domains:**
- Reaction–Diffusion core: Fisher–KPP front speed and linear dispersion
- Discrete conservation laws: Q-invariant convergence; Noether invariants
- Fluids (baseline): LBM viscosity recovery on D2Q9

**Promotion from Tier B:** Requires formal RESULTS document and CANON_PROGRESS entry

**Source:** `VDM_OVERVIEW.md` lines 19-22

---

### Tier B — Active KPI-Gated Physics  <a id="tier-b"></a>

**Definition:** Claims accepted as active research (not speculative), with defined KPI gates.

**Requirements:**
- Status: [PLAUSIBLE] or [PLAUSIBLE→PROVEN]
- Quantitative gates defined in `VALIDATION_METRICS.md`
- Proposal document approved
- Active validation infrastructure

**Active domains:**
- EFT/KG branch: tachyonic tube spectra and condensation
- Metriplectic structure: J/M degeneracy checks, H-theorem
- Agency field: relaxation $\tau\approx 1/\gamma$ and coordination-response
- Topology scaling-collapse; Cosmology FRW residual QC
- Dark-photon toy experiments

**Promotion to Tier A:** All KPI gates passed + RESULTS document + artifact archive

**Source:** `VDM_OVERVIEW.md` lines 23-27

---

### Tier C — Engineering & Policy Substrate  <a id="tier-c"></a>

**Definition:** Infrastructure enabling scientific validation; no physics claims.

**Requirements:**
- Documented in canonical registries
- Versioned schemas and specifications
- CI/CD enforcement where applicable

**Components:**
- Approvals/quarantine system
- I/O paths routing
- JSON Schemas/Data Products
- RESULTS standards
- Canon registries: EQUATIONS, SYMBOLS, ALGORITHMS, VALIDATION_METRICS, etc.

**Promotion path:** None (permanent infrastructure role)

**Source:** `VDM_OVERVIEW.md` lines 28-30

---

### Tier D — Exploratory & Bridges  <a id="tier-d"></a>

**Definition:** Speculative research threads; clearly labeled, promoted only after KPI validation.

**Requirements:**
- Status: [PLAUSIBLE] at most
- Explicitly marked as exploratory
- No claims in canonical documentation until promoted
- May reference Tier A/B work but cannot be cited as evidence

**Domains:**
- Gravity_Regression and Quantum_Gravity bridges
- Quantum/Quantum_Witness threads
- Thermodynamic_Routing (early stages)
- Causality audit
- Memory_Steering (early stages)
- Converging External Research

**Promotion to Tier B:** Requires approved proposal + defined KPIs

**Promotion to Tier A:** Must first pass through Tier B validation

**Source:** `VDM_OVERVIEW.md` lines 31-33, 37-42

---

## III. Progression Gates (Concept → Physical Law)

### Stage 1: Concept Formation

**Entry criteria:**
- Theoretical motivation from axioms OR analogy to validated physics
- Preliminary sketch of mathematical structure
- Identification of potential observables

**Exit criteria:**
- Written concept document in `Derivation/<Domain>/`
- Initial parameter estimates
- Sketch of validation approach

**Tier assignment:** Tier D (Exploratory)

**Status tag:** [PLAUSIBLE] (not yet)

---

### Stage 2: Proposal Development

**Entry criteria:**
- Complete Stage 1
- Mathematical formulation detailed
- Acceptance gates defined

**Exit criteria:**
- Approved PROPOSAL document (`Derivation/<Domain>/PROPOSAL_*.md`)
- KPIs registered in `VALIDATION_METRICS.md`
- Validation runner specification written

**Tier assignment:** Tier D → Tier B (upon approval)

**Status tag:** [PLAUSIBLE]

**Gate template:**
```markdown
**Acceptance criteria:**
- Gate 1: <metric> <comparison> <threshold> (e.g., rel-err ≤ 5%)
- Gate 2: <metric> <comparison> <threshold> (e.g., R² ≥ 0.999)
- Gate 3: <observable> exhibits <behavior> (e.g., exponential decay)
```

---

### Stage 3: Active Validation

**Entry criteria:**
- Complete Stage 2
- Runner implemented
- Initial data collection underway

**Exit criteria:**
- All runners producing outputs
- Figures generated
- CSV/JSON data archived
- Preliminary gate checks passing

**Tier assignment:** Tier B (Active)

**Status tag:** [PLAUSIBLE→PROVEN] (during validation)

**Quality checks:**
- Numerical stability verified (convergence tests)
- Boundary condition sensitivity assessed
- Parameter regime mapping documented
- Error analysis completed

---

### Stage 4: Canonical Acceptance

**Entry criteria:**
- Complete Stage 3
- All acceptance gates passed with documented margins
- Artifacts pinned in repository

**Exit criteria:**
- RESULTS document completed (`Derivation/<Domain>/RESULTS_*.md`)
- Entry in `CANON_PROGRESS.md` with status [PROVEN]
- Runner committed to `Derivation/code/`
- Outputs archived in `Derivation/code/outputs/`

**Tier assignment:** Tier B → Tier A (upon completion)

**Status tag:** [PROVEN]

**Required documentation:**
```markdown
## [Domain/Claim Name] <a id="anchor"></a>
**Status:** PROVEN • **Priority:** <P1/P2/P3>

**Gate met:** <metric1>≈<value1>, <metric2>≈<value2>, ...

**Artifacts:**
- Runner: `path/to/runner.py`
- Figure: `path/to/figure.png`
- Data: `path/to/data.csv`, `path/to/data.json`
- RESULTS: `Derivation/<Domain>/RESULTS_*.md`
```

---

## IV. Falsification and Correction

### Falsification Process

**Triggering conditions:**
- Gate criteria failed in validation
- Logical inconsistency discovered
- Computational evidence contradicts claim
- Experimental observation (future) refutes prediction

**Required actions:**
1. Document failure mode in `Derivation/CORRECTIONS.md`
2. Update status tag to [DISPROVEN]
3. Move to negative controls in `CANON_PROGRESS.md`
4. Issue correction notice if claim was previously [PROVEN]
5. Update all citing documents

**Source:** `VDM_OVERVIEW.md` line 3 (corrections reference)

---

### Correction Without Falsification

**Conditions:**
- Parameter refinement within tolerance
- Gate threshold adjustment (stricter only)
- Mathematical notation improvement
- Clarification of scope

**Required actions:**
1. Document change in `Derivation/CORRECTIONS.md`
2. Update affected canonical documents
3. Maintain status tag (if still passing gates)
4. Version-tag if material change

**Note:** Loosening gates requires re-validation cycle

---

## V. Enforcement and CI

### Allowed Status Tags

**Enforcement:** CI linter checks all markdown files in `Derivation/` for status tags.

**Allowed tags only:**
```bash
\[(DISPROVEN|PLAUSIBLE→PROVEN|PLAUSIBLE|PROVEN)\]
```

**Action on violation:** Build fails; PR blocked

**Source:** `CANON_PROGRESS.md` lines 85-91

---

### Cross-Reference Requirements

**Canon documents must link, not duplicate:**
- Equations → `EQUATIONS.md#vdm-e-###`
- Symbols → `SYMBOLS.md#sym-###`
- Constants → `CONSTANTS.md#const-###`
- Algorithms → `ALGORITHMS.md#vdm-a-###`
- KPIs → `VALIDATION_METRICS.md#kpi-###`
- Units → `UNITS_NORMALIZATION.md#...`
- Data products → `DATA_PRODUCTS.md#data-###`

**Enforcement:** Hygiene checker (`tools/md_hygiene_check.py`)

**Source:** `README.md` lines 19-32, `prompts/roadmap_maintenance.md`

---

### Artifact Pinning Requirements

**For [PROVEN] status:**
- All artifacts committed to repository
- Paths relative to repository root
- Commit SHA recorded in RESULTS document
- No external dependencies for reproducibility

**For [PLAUSIBLE]:**
- Proposal document committed
- Runner specification (may be incomplete)

**Source:** `CANON_PROGRESS.md` rule line 4

---

## VI. Theory Constitution Principles

### Minimality

**Principle:** Make smallest possible claim that is testable.

**Implementation:**
- Avoid overgeneralization from single validation
- State parameter regime explicitly
- Flag regime boundaries where behavior changes

**Example:** RD front speed claim limited to Fisher–KPP form; does not extend to bistable fronts without separate validation

---

### Falsifiability

**Principle:** Every nontrivial claim must have defined failure conditions.

**Implementation:**
- Quantitative gates with thresholds (not "approximately" or "similar to")
- Explicit error tolerances
- Documented parameter ranges

**Connection:** Axiom A7 (Measurability)

**Source:** `AXIOMS.md` lines 99-105

---

### Reproducibility

**Principle:** All [PROVEN] claims must be independently reproducible.

**Implementation:**
- Committed runners with dependency specifications
- Seed control for stochastic processes
- Commit logging for artifact provenance
- Data archival with schemas

**Quality metric:** Third-party validation (future goal)

---

### Transparency

**Principle:** Failure modes and limitations documented as prominently as successes.

**Implementation:**
- Negative controls section in `CANON_PROGRESS.md`
- Error analysis in RESULTS documents
- Parameter regime boundaries stated
- Numerical stability limitations noted

**Example:** "Site-wise conservation of $Q$ under diffusion" explicitly listed as [DISPROVEN]

---

## VII. Special Regimes and Transitions

### Hyperbolic vs. Parabolic

**Critical distinction:** Finite propagation speed (hyperbolic) vs. instantaneous tails (parabolic)

**Progression rules:**
- Causal cone claims: [PROVEN] only for J-only (KG) regime or explicitly flagged hyperbolic regularizations
- RD regime: Use "front speed" language, never "cone"
- Telegraph-RD: Must show cone recovery and RD limit as $\tau\to 0$

**Gate criteria:**
- Hyperbolic: Finite domain-of-dependence with speed $\le c$
- Parabolic: Front speed matching analytical prediction

**Source:** `CANON_PROGRESS.md` lines 13, 34, 44-45; `AXIOMS.md` A2

---

### Discrete to Continuum

**Progression path:** Discrete axioms → Continuum limit → Physical interpretation

**Requirements:**
- Discrete action specified (VDM-AX-004)
- Euler–Lagrange equations derived (VDM-AX-C01)
- Continuum limit taken (VDM-AX-C02)
- Prefactors exact, not fitted

**Gate criteria:**
- Lattice spacing convergence: Power-law scaling with known exponent
- Continuum equation recovery: Coefficient rel-err $\le 5\%$

**Source:** `AXIOMS.md` lines 113-137

---

### Noether Conservation

**Progression requirements:**
- Symmetry group specified (VDM-AX-A3)
- Conserved current derived via Noether theorem
- Numerical drift monitored

**Gate criteria:**
- Per-step drift $\le 10^{-12}$ or $10\,\epsilon\sqrt{N}$ (whichever larger)
- Reversibility check $\le 10^{-10}$ (if applicable)

**Source:** `CANON_PROGRESS.md` line 21; `AXIOMS.md` lines 52-65

---

### Metriplectic Structure

**Progression requirements:**
- J (symplectic) and M (metric) operators specified
- Degeneracies $J\,\delta\Sigma=0$ and $M\,\delta\mathcal{I}=0$ verified

**Gate criteria:**
- $\langle J\,\delta\Sigma,\,\delta\Sigma \rangle \le 10^{-10}\,N$
- $\langle M\,\delta\mathcal{I},\,\delta\mathcal{I} \rangle \le 10^{-10}\,N$

**Source:** `CANON_PROGRESS.md` line 26; `AXIOMS.md` lines 68-76

---

## VIII. Administrative

### Document Maintenance

**Update frequency:** On promotion events or correction discoveries

**Update procedure:**
1. Edit relevant section
2. Update "Last updated" timestamp
3. Add change log entry
4. Commit with descriptive message

**Reviewers:** Theory lead (required)

---

### Change Log

- 2025-10-15 • Initialize VDM_PROGRESSION_STANDARDS.md from CANON_PROGRESS.md tier standards • HEAD

---

## Cross-References

- Canonical progress tracking: [CANON_PROGRESS.md](CANON_PROGRESS.md)
- Axiom definitions: [AXIOMS.md](AXIOMS.md)
- Validation metrics: [VALIDATION_METRICS.md](VALIDATION_METRICS.md)
- Data products: [DATA_PRODUCTS.md](DATA_PRODUCTS.md)
- Roadmap: [ROADMAP.md](ROADMAP.md)
- Overview: [VDM_OVERVIEW.md](VDM_OVERVIEW.md)

---

<!-- BEGIN AUTOSECTION: STANDARDS-INDEX -->
<!-- Tool-maintained list of anchors for quick lookup -->

**Status Tags:**
- [DISPROVEN](#status-disproven) — Falsified claim
- [PLAUSIBLE](#status-plausible) — Preliminary evidence
- [PLAUSIBLE→PROVEN](#status-plausible-to-proven) — Active validation
- [PROVEN](#status-proven) — Canonical physics

**Tiers:**
- [Tier A](#tier-a) — Proven Canonical Physics
- [Tier B](#tier-b) — Active KPI-Gated Physics
- [Tier C](#tier-c) — Engineering & Policy Substrate
- [Tier D](#tier-d) — Exploratory & Bridges

<!-- END AUTOSECTION: STANDARDS-INDEX -->
