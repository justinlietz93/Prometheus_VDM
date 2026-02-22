# Logging Crosswalk (v7 sparse-only)

## Physics primitives
- Node field: `phi_curr`, `phi_prev`
- Bond field: `psi_curr`, `psi_prev`
- Structure/state: `adj`, `debt`, `r_causal`

## Tick scalar outputs
- Energetics/regime: `H`, `dH_dt`, `S`, `dS_dt`, `fisher_speed`, `boundary_flux`
- Activity: `phi_dot_rms`, `phi_dot_var`, `phi_mean`, `phi_var`
- Structure:
  - `active_edges` is canonical and defined only as `psi > ETA_BOND_FLOOR`
  - `psi_mean`, `psi_rms`
- Traversal/gating: `vt_visits`, `vt_entropy`, `a_mean`, `omega_mean`, `valence_01`

## Persistence
- Event stream and scalar stream are append-only JSONL in smoke run.
- H5 engram checkpoint/resume remains functional.
