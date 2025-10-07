# BENCHMARKS_FLUIDS

> Author: Justin K. Lietz  
> Date: August 9, 2025
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.<br> 
> Commercial use requires written permission from Justin K. Lietz.
> 
> See LICENSE file for full terms.

Purpose
- Define falsifiable acceptance thresholds for the fluids sector (LBM→NS) to certify reduction to Navier-Stokes.

Benchmarks (double precision)
1) Taylor-Green vortex (2‑D periodic)
- Fit viscous decay E(t) = E0 exp(-2 ν k² t).
- Thresholds:
  - Baseline grid (≥ 256²): |ν_fit - ν_th| / ν_th ≤ 5%.
  - Refinement (×2 linear res): error decreases consistent with scheme order.
- Artifact paths:
  - Figure: derivation/code/outputs/figures/fluid_dynamics/taylor_green_benchmark_<timestamp>.png
  - Log: derivation/code/outputs/logs/fluid_dynamics/taylor_green_benchmark_<timestamp>.json

2) Lid‑driven cavity (square, no‑slip walls, moving lid)
- Monitor divergence norm ‖∇·v‖₂ over time.
- Thresholds:
  - max_t ‖∇·v‖₂ ≤ 1e-6 (double).
  - Centerline profiles converge with grid (qualitative check; optional quantitative against literature).
- Artifact paths:
  - Figure: derivation/code/outputs/figures/fluid_dynamics/lid_cavity_benchmark_<timestamp>.png
  - Log: derivation/code/outputs/logs/fluid_dynamics/lid_cavity_benchmark_<timestamp>.json

Logging schema
- JSON payload must include:
  - theory (string)
  - params (object): grid, τ, ν_th (if applicable), steps, sample_every
  - metrics (object): key numbers, elapsed_sec, passed (boolean)
  - outputs (object): figure path
  - timestamp (UTC ISO‑8601)

Pass gate
- A benchmark “passes” when all thresholds above are met and metrics.passed is true.

How to run (PowerShell)
- Always activate venv:
  & .\venv\Scripts\Activate.ps1
- Taylor-Green:
  python Prometheus_VDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py --nx 256 --ny 256 --tau 0.8 --steps 5000 --sample_every 50
- Lid cavity:
  python Prometheus_VDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py --nx 128 --ny 128 --tau 0.7 --U_lid 0.1 --steps 15000 --sample_every 200

Notes
- These thresholds certify the LBM→NS reduction operationally. They do not change the RD sector’s canonical status; both sectors live side‑by‑side with separate claims and tests.
## Void-walker announcers (read-only observability)

Purpose
- Provide a passive, causal measurement layer that rides the existing flow and announces localized signals without injecting forces or altering the solver.
- Outputs robust summaries (counts, quantiles) and optional event markers; suitable for diagnostics and policy previews.

Design
- Sensors: walkers advected by measured velocity u(x,y); sense div, swirl (|ω|), and a near-wall shear proxy.
- Bus: in-memory petition bus collecting events (kind, value, x, y, t).
- Reducer: computes robust per-kind quantiles and counts; used for printing and JSON logging.
- Policy (optional): AdvisoryPolicy suggests bounded nudges to numerical parameters (τ, u_clamp, U_lid). Default mode is observe-only; advise/act requires explicit flags and never injects body forces.

CLI (lid cavity)
- Flags (all optional, OFF by default):
  - --walker_announce: enable announcers (Bus/Reducer).
  - --walkers N: number of walkers to seed (top-lid line).
  - --walker_seed S: PRNG seed.
  - --announce_max K: top events to render if overlaying markers.
  - --walker_overlay: plot path tracks (void-walker-inspired) and, if announcers on, value-sized event markers.
  - --walker_mode {off,observe,advise,act} (default observe)
  - --policy_div_target (default 1e-6), --policy_swirl_target (default 5e-3)
- Examples:
  - Observe-only metrics:
    - python [lid_cavity_benchmark.py](Prometheus_VDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:316) --nx 128 --ny 128 --steps 15000 --warmup 2000 --walker_announce --walkers 210
  - Overlay markers + tracks:
    - python [lid_cavity_benchmark.py](Prometheus_VDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:316) --nx 128 --ny 128 --steps 15000 --warmup 2000 --walker_announce --walkers 210 --walker_overlay --announce_max 256
  - Advisory preview (prints suggestions; does not apply when --auto is set to avoid controller conflict):
    - python [lid_cavity_benchmark.py](Prometheus_VDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:316) --walker_announce --walkers 210 --walker_mode advise

JSON additions
- metrics.void_announcers:
  - announce_counts: per-kind counts (e.g., {"div":..., "swirl":..., "shear":...})
  - announce_stats: per-kind quantiles (e.g., div_p50, div_p90, div_max, etc.)
- metrics.void_walkers:
  - coverage/loop metrics from the cheap void-walker-inspired traversal (when --walkers > 0).

Non-interference test (falsifiable)
- Ensure read-only walker usage does not alter flow fields.
- Test file: [test_walkers_noninterference.py](Prometheus_VDM/derivation/code/tests/fluid_dynamics/test_walkers_noninterference.py:1)
- Run (PowerShell):
  - & .\venv\Scripts\Activate.ps1; pytest -q .\Prometheus_VDM\derivation\code\tests\fluid_dynamics\test_walkers_noninterference.py
- Acceptance: max |Δu| = 0 and |Δv| = 0 at end of matched runs (with/without walkers).

Notes
- Announcers are for observability and diagnostics. Any act mode applies bounded numerical parameter updates only (τ, u_clamp, U_lid). No forcing is added to the PDE step, preserving physics integrity.