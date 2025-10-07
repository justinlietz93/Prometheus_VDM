# METRICS

## Dynamics (RD model)
- Growth rate around φ=0:  σ(k) = r - D k².
- Front speed (pulled front): c = 2√(D r).
- Fixed-point stability: f'(φ*) < 0, with f(φ)=rφ-uφ²-λφ³.

## SIE/TDA System metrics
- Update latency vs nodes N: fit τ(N) = A N^b; report b and 95% CI.
- Coherence (text): normalized semantic similarity vs reference set.
- Novelty: distribution shift score vs training distribution.
- Structural lift (TDA): Δ predictive metric with vs without TDA layer.

## Reproducibility
- 5-seed variance for each key metric; require std/mean < threshold T.
- Commit hash + config snapshot stored alongside JSON logs.

## File paths
- Benchmarks: bench/logs/*.json
- Plots: bench/plots/*.png