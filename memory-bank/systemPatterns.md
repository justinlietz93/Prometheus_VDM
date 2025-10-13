# System Patterns

## Architectural Patterns

- Pattern 1: Description

## Design Patterns

- Pattern 1: Description

## Common Idioms

- Idiom 1: Description

## Pre-registration execution guard for scientific runners

All scientific runners must default-deny execution unless a proposal is approved. Provide a CLI escape hatch --allow-unapproved for engineering-only smokes. When unapproved, stamp JSON logs with policy { pre_registered:false, engineering_only:true, quarantined:true } and route artifacts via failed/quarantine paths so they are excluded from RESULTS/KPIs. Add lightweight README notices in output domains explaining quarantine.

### Examples

- derivation/code/physics/dark_photons/run_dp_noise_budget.py: guard flag and policy block
- derivation/code/physics/dark_photons/run_dp_fisher_check.py: guard flag and policy block
- derivation/VALIDATION_METRICS.md: Status fields marked planned (pre-registered)


## Causality audit ingestion via neuron head expansion + bounded chaining

When runtime logs include per-tick arrays of top-k neuron indices (e.g., evt_*_head), construct per-neuron per-tick events with IDs like kind:neuron:tick. Chain edges across ticks for the same neuron (last-seen map) to ensure a sparse, acyclic baseline graph. Disable unbounded time-inference by default to avoid dense graphs. Optionally allow bounded cross-neuron successors with a small max_successors and time tolerance. Use iterative Kahn’s algorithm for acyclicity checks to avoid recursion limits on large graphs.

### Examples

- Derivation/code/physics/causality/run_causality_dag_audit.py head expansion path
- Derivation/code/common/causality/event_dag.py with is_acyclic via Kahn’s algorithm


## Structure-check runner pattern for algebraic invariants

Provide a tiny, policy-aware runner that samples random vectors to test operator properties (e.g., J skew-symmetry via median |<v,Jv>| and M positive semidefiniteness via counts of negative <u,Mu>). Route outputs through io_paths with quarantine on unapproved runs; pair a short RESULTS doc that defines gates and artifact paths.

### Examples

- Derivation/code/physics/metriplectic/metriplectic_structure_checks.py
- Derivation/Metriplectic/RESULTS_Metriplectic_Structure_Checks.md


## Experiment artifact and prereg discipline enforcement

All experiments must (1) be approved before running (default-deny; --allow-unapproved routes to quarantine), (2) use common.io_paths for all artifacts, (3) produce at minimum: 1 PNG figure + 1 CSV log + 1 JSON summary, (4) never emit a RESULTS document until metrics are finalized and approved, and (5) include a compliance block in the JSON with approvals, probe-limit, frozen-map, and artifact_minimum receipts.

### Examples

- Derivation/code/physics/thermo_routing/passive_thermo_routing/run_ftmc_v1.py writes 2 figures, a CSV metrics file via log_path_by_tag(..., type='csv'), and a JSON summary; approvals enforced via common.authorization.approval.check_tag_approval; RESULTS output disabled.
