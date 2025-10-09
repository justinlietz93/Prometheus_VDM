# Derivation - Index and Hygiene

Last updated: 2025-10-09 (commit 09f871a)

## Canonical registries (single source of truth)

- EQUATIONS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/EQUATIONS.md`
- SYMBOLS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/SYMBOLS.md`
- CONSTANTS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/CONSTANTS.md`
- UNITS_NORMALIZATION - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/UNITS_NORMALIZATION.md`
- BC_IC_GEOMETRY - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/BC_IC_GEOMETRY.md`
- ALGORITHMS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/ALGORITHMS.md`
- VALIDATION_METRICS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/VALIDATION_METRICS.md`
- DATA_PRODUCTS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/DATA_PRODUCTS.md`
- SCHEMAS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/SCHEMAS.md`
- CANON_MAP - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/CANON_MAP.md`
- ROADMAP - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/ROADMAP.md`
- OPEN_QUESTIONS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/OPEN_QUESTIONS.md`
- NAMING_CONVENTIONS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/NAMING_CONVENTIONS.md`
- AXIOMS - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/AXIOMS.md`
- OVERVIEW - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/OVERVIEW.md`

Note: These are “latest-only” registries; CORRECTIONS.md remains chronological.

## Working domain folders (what they’re for)

- Agency_Field - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Agency_Field`
  - Agency field definitions, proxies, and acceptance tests; connects control-plane metrics to physics claims.
- Causality - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Causality`
  - Event DAG auditing, Granger/VAR macros, and acyclicity checks for causal structure in runtime logs.
- code - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/code`
  - Experiment runners, common helpers (io_paths, approvals), outputs/{logs,figures} routing.
- Collapse - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Collapse`
  - Scaling-collapse narratives, A6 universality checks, envelopes and KPI definitions.
- Conservation_Law - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Conservation_Law`
  - Discrete conservation derivations, invariants, and structure checks (Noether-style diagnostics).
- Converging_External_Research - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Converging_External_Research`
  - External results that converge with VDM hypotheses; literature crosswalks and evidence mapping.
- Cosmology - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Cosmology`
  - Cosmological implications and observational tests tied to VDM parameters.
- Dark_Photons - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Dark_Photons`
  - Noise budgets, Fisher checks, and approval-gated DP experiments.
- Draft-Papers - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Draft-Papers`
  - Manuscripts and in-progress writeups prior to RESULTS/PROPOSAL promotion.
- Effective_Field_Theory - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Effective_Field_Theory`
  - EFT/KG branch math, kinetic normalization from discrete action, and KPI-gated analyses.
- Fluid_Dynamics - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Fluid_Dynamics`
  - LBM notes/benchmarks and VDM-fluids corner testbed plans.
- Foundations - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Foundations`
  - Discrete→continuum stack, symmetry analysis, and axiomatic theory development.
- Gravity_Regression - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Gravity_Regression`
  - Empirical gravity modeling/fits and related validation plans.
- Information - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Information`
  - Information-theoretic constructs and metrics (e.g., entropy, divergence surrogates).
- Legacy_Claims - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Legacy_Claims`
  - Archived or superseded claims retained for provenance.
- Memory_Steering - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Memory_Steering`
  - Theory and acceptance harnesses for graded-index memory overlays and routing.
- Metriplectic - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Metriplectic`
  - J/M split, degeneracy structure checks, and metriplectic integrators with QC gates.
- Notebooks - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Notebooks`
  - Interactive exploration (kept non-canonical) linked to scripts and RESULTS where applicable.
- Quantum - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Quantum`
  - Quantum mechanics threads relevant to VDM, including measurement and decoherence links.
- Quantum_Gravity - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Quantum_Gravity`
  - Bridges and consistency checks between QFT and GR under VDM assumptions.
- Quantum_Witness - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Quantum_Witness`
  - Macrorealism/contextuality-style tests and proxies tailored to VDM systems.
- Reaction_Diffusion - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Reaction_Diffusion`
  - Canonical RD branch: front-speed/dispersion validation plans, scripts, and RESULTS.
- References - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/References`
  - Source materials, citations, and curated bibliographies.
- Speculations - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Speculations`
  - Clearly labeled non-canonical ideas for exploration.
- Supporting_Work - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Supporting_Work`
  - Auxiliary analyses and utilities that support canonical runs and plots.
- Tachyon_Condensation - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Tachyon_Condensation`
  - Finite-tube mode solves and condensation scans; KPI-gated RESULTS and schemas.
- Thermodynamic_Routing - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Thermodynamic_Routing`
  - Thermodynamic arguments for signal routing/control.
- Topology - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Topology`
  - Topological constructs and planned graph/loop experiments.
- Writeup_Templates - `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Writeup_Templates`
  - Canonical PROPOSAL and RESULTS templates governing papers and artifacts.

## Critically important file paths and rules

Critically important registries:

- `/mnt/ironwolf/git/Prometheus_VDM/derivation/AGENCY_FIELD.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/ALGORITHMS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/BC_IC_GEOMETRY.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/CONSTANTS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/CANON_MAP.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/DATA_PRODUCTS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/EQUATIONS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/VALIDATION_METRICS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/UNITS_NORMALIZATION.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/SYMBOLS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/SCHEMAS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/ROADMAP.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/OPEN_QUESTIONS.md`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/NAMING_CONVENTIONS.md`

## Experiment code and configs

- `/mnt/ironwolf/git/Prometheus_VDM/derivation/code/physics/{domain/topic folder}`

## Result artifacts

- `/mnt/ironwolf/git/Prometheus_VDM/derivation/code/outputs/logs/{domain/topic folder}`
- `/mnt/ironwolf/git/Prometheus_VDM/derivation/code/outputs/figures/{domain/topic folder}`

## You must use the io helper for outputs

- `/mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/io_paths.py`

## ALL new experiments MUST have a proposal file created first, follow this template

- `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Writeup_Templates/PROPOSAL_PAPER_TEMPLATE.md`

Put the proposal file in the correct domain folder:

- `/mnt/ironwolf/git/Prometheus_VDM/derivation/{domain/topic folder}`

## ALL completed experiments MUST have a results write-up, follow these standards

- `/mnt/ironwolf/git/Prometheus_VDM/Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md`

Put the results file in the correct domain folder next to the proposal:

- `/mnt/ironwolf/git/Prometheus_VDM/derivation/{domain/topic folder}`

## ALL experiment runs MUST produce a MINIMUM of 1 figure, 1 CSV log, and 1 JSON log as artifacts. Use the io helper to manage paths and naming

- `/mnt/ironwolf/git/Prometheus_VDM/derivation/code/common/io_paths.py`

## ALL new experiments MUST be approved by Justin K. Lietz before running, read this for context

- `/mnt/ironwolf/git/Prometheus_VDM/Derivation/code/ARCHITECTURE.md`
- `/mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/authorization/README.md`

## ALWAYS update the canonical files in the Derivation/ folder root when new discoveries are made, or when experiments are completed and results are confirmed

This should be done AFTER creating a RESULTS_ file in the designated `Derivation/{domain}` folder.

