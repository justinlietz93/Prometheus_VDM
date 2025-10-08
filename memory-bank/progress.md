# Progress (Updated: 2025-10-08)

## Done

- Trail chaining implemented with CLI flags (--trail-chain, --trail-topk, --trail-minval); approved runs completed with enriched DAG outputs
- Macro VAR Granger DAG with BH-FDR integrated; macro figures and logs saved; interpretable edges validated

## Doing

- Document new causality runner flags and macro DAG workflow in existing README; add example outputs and interpretation notes

## Next

- Sensitivity analysis: sweep trail_topk/minval and macro lags/alpha; compare edge stability and density
- Consider bounded cross-neuron coupling with small max_successors and time tolerance for candidate interactions
