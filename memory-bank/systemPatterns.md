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
