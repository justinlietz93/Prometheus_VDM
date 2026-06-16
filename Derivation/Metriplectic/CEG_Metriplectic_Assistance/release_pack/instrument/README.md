# Instrument Source Map

The CEG metriplectic instrument code lives in the main repo under `Derivation/code/`.
Below is the dependency tree — every file the instrument touches.

## Core Runner

- `physics/metriplectic/assisted_echo.py` — Entry point. Contains `EchoSpec` dataclass and `run_assisted_echo(spec)`.

## Physics Modules (J-limb + M-limb)

- `physics/metriplectic/kg_ops.py` — Spectral Laplacian, gradient, KG energy, Störmer-Verlet stepper.
- `physics/metriplectic/j_step.py` — Pure J-limb: exact spectral advection (FFT phase shift).
- `physics/metriplectic/compose.py` — Strang composition + DG M-step wrapper.
- `physics/metriplectic/kg_noether.py` — Noether invariant checks (discrete energy/momentum).
- `physics/rd_conservation/run_rd_conservation.py` — DG Newton solver for reaction-diffusion (M-limb backend).
- `physics/reaction_diffusion/reaction_exact.py` — Exact logistic reaction step.

## Gate System

- `physics/metriplectic/echo_gates.py` — Gate functions: G1 (Noether), G2 (H-theorem), G3 (energy match), G4 (Strang defect).
- `physics/metriplectic/echo_metrics.py` — H-norm error, CEG formula.
- `physics/metriplectic/metriplectic_structure_checks.py` — J skew-symmetry, M PSD algebraic checks.

## Infrastructure

- `common/io_paths.py` — Timestamped artifact routing, quarantine policy.
- `common/authorization/approval.py` — Run approval system (use `--allow-unapproved` for external runs).
- `common/plotting/assisted_echo_plots.py` — Publication figure pack generator.

## Specs (Experiment Configurations)

- `physics/metriplectic/specs/assisted_echo.v1c.json` — Canonical: N=256, dt=0.02
- `physics/metriplectic/specs/assisted_echo.v1c_N512_dt0p04.json`
- `physics/metriplectic/specs/assisted_echo.v1c_N1024_dt0p04.json`
- `physics/metriplectic/specs/assisted_echo.v1c_walker.json` — With walker perturbation
- (+ several budget/grid variants)

## Schemas (Validation)

- `physics/metriplectic/schemas/echo_spec-v1c.schema.json`
- `physics/metriplectic/schemas/echo_artifacts-v1.schema.json`
- `physics/metriplectic/schemas/assisted-echo-t4-prereg-v1c.schema.json`

## Tests

- `tests/metriplectic/test_assisted_echo_preflight.py`
- `tests/metriplectic/test_instrumented_ceg.py`
