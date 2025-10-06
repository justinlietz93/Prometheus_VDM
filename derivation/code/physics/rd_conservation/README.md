# RD Conservation Harness

Location: `derivation/code/physics/rd_conservation`

Outputs (via io helper):

- Logs: `derivation/code/outputs/logs/rd_conservation/...`
- Figures: `derivation/code/outputs/figures/rd_conservation/...`

This harness evaluates Obj‑A/B/C for the discrete RD update using the production Euler step (and optionally Strang with an exact reaction substep).

Key policies:

- Periodic BC for Obj‑A/B runs; Neumann only for front‑speed control.
- Disable clamps and `nan_to_num` in proof paths.
- Record CFL compliance and use the exact adjacency/stencil as the stepper.

Files:

- `step_spec.schema.json`: JSON schema for configuration.
- `step_spec.example.json`: Example config aligned with the “Go” setup.
- `run_rd_conservation.py`: Minimal runner wiring controls and dt‑sweep (RK4 reaction‑only) and saving logs/figures using `common/io_paths.py`.

Acceptance gates:

- V1/V2 exactness (if a candidate S is provided) with (|ΔS|≤1e−12).
- V3 dt‑slope ≥ p+1−0.1 with R² ≥ 0.999.
- V4 controls: diffusion‑only mass (machine‑epsilon), reaction‑only Q‑invariant order‑4 with RK4.
- V5 out‑of‑sample: freeze any fitted H parameters and rerun on fresh seeds.
