# Progress (Updated: 2025-10-06)

## Done

- Implemented failed_runs routing across Q-invariant, Obj-A/B residuals, and Lyapunov; verified with a harness run that failing artifacts route to outputs/*/rd_conservation/failed_runs and logs/CSVs land under logs.

## Doing

- Tune pass/fail thresholds if needed and clean legacy sidecars under figures from prior runs.

## Next

- Add Obj-B explicit gate reporting to console summary and a CONTRADICTION_REPORT stub if any gate fails.
