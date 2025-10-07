# Progress (Updated: 2025-10-07)

## Done

- Updated VALIDATION_METRICS: dark-photon KPIs marked planned; fixed implementation paths.
- Implemented runner guardrails in run_dp_noise_budget.py and run_dp_fisher_check.py with --allow-unapproved and policy stamping.
- Quarantined existing DP smoke artifacts; added README notices under logs/ and figures/.

## Doing

- Prepare approval registry hook to flip pre_registered once proposal is approved.

## Next

- Propagate guardrails pattern to other experimental runners (where applicable).
- Add unit tests for CLI guard behavior (exit=2 on unapproved).
