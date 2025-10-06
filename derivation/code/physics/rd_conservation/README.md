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
- `run_rd_conservation.py`: Runner for controls, Obj‑A/B baseline sweeps, and Lyapunov monitor; saves logs/figures using `common/io_paths.py`.

Acceptance gates:

- V1/V2 exactness (if a candidate S is provided) with (|ΔS|≤1e−12).
- V3 dt‑slope ≥ p+1−0.1 with R² ≥ 0.999.
- V4 controls: diffusion‑only mass (machine‑epsilon), reaction‑only Q‑invariant order‑4 with RK4.
- V5 out‑of‑sample: freeze any fitted H parameters and rerun on fresh seeds.

Run:

```bash
python derivation/code/physics/rd_conservation/run_rd_conservation.py --spec derivation/code/physics/rd_conservation/step_spec.example.json
```

Expected outputs (under `derivation/code/outputs`):

- Logs (`logs/rd_conservation`):
  - `controls_diffusion-<stamp>.json` (mass conservation)
  - `controls_reaction-<stamp>.json` (Q‑invariant slope)
  - `step_spec_snapshot-<stamp>.json` (spec + CFL check)
  - `sweep_exact-<stamp>.json` (Obj‑A samples, H=0 baseline)
  - `sweep_dt-<stamp>.json` (Obj‑B slope/R²)
  - `lyapunov_series-<stamp>.json` (Obj‑C ΔL per step)
- Figures (`figures/rd_conservation`):
  - `q_invariant_convergence-<stamp>.png` + `.json` sidecar (numeric caption)
  - `residual_vs_dt-<stamp>.png` + `.json` sidecar
  - `lyapunov_delta_per_step-<stamp>.png`
