# Progress (Updated: 2025-10-06)

## Done

- Implemented small-Δt JMJ sweep with dg_tol=1e-12, logging Newton iterations/residuals and emitting paired CSV/JSON/PNG.
- Added commutator/defect diagnostic comparing JMJ vs MJM with slope fit and artifacts.
- Implemented V5 robustness grid across (r,u,D,N) tuples with pass-rate calculation and CSV.
- Enhanced RESULTS with Theory primer and expanded standards for comprehensive documentation.
- Improved |ΔS| panel x-axis (log bins) and annotations; re-ran artifacts.

## Doing

- Tune parameters (N, Δt, seeds) to reach JMJ slope ≥ 2.9 consistently; iterate on small-Δt sweep.
- Update RESULTS with new artifacts and a short defect explanation plot once gates pass.

## Next

- Increase N or shrink Δt to 0.0025, 0.00125; consider seeds=12 for medians.
- Add dt_sweep_small and dg_tol to step_spec JSON; optionally add v5_grid.
- Re-run harness; update RESULTS with new figures and robustness table.
- Draft the small proposal to couple J⊕M to a conservative two-field (KG) using the provided template.
