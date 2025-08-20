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
- Define falsifiable acceptance thresholds for the fluids sector (LBM→NS) to certify reduction to Navier–Stokes.

Benchmarks (double precision)
1) Taylor–Green vortex (2‑D periodic)
- Fit viscous decay E(t) = E0 exp(−2 ν k² t).
- Thresholds:
  - Baseline grid (≥ 256²): |ν_fit − ν_th| / ν_th ≤ 5%.
  - Refinement (×2 linear res): error decreases consistent with scheme order.
- Artifact paths:
  - Figure: derivation/code/outputs/figures/fluid_dynamics/taylor_green_benchmark_<timestamp>.png
  - Log: derivation/code/outputs/logs/fluid_dynamics/taylor_green_benchmark_<timestamp>.json

2) Lid‑driven cavity (square, no‑slip walls, moving lid)
- Monitor divergence norm ‖∇·v‖₂ over time.
- Thresholds:
  - max_t ‖∇·v‖₂ ≤ 1e−6 (double).
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
- Taylor–Green:
  python Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py --nx 256 --ny 256 --tau 0.8 --steps 5000 --sample_every 50
- Lid cavity:
  python Prometheus_FUVDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py --nx 128 --ny 128 --tau 0.7 --U_lid 0.1 --steps 15000 --sample_every 200

Notes
- These thresholds certify the LBM→NS reduction operationally. They do not change the RD sector’s canonical status; both sectors live side‑by‑side with separate claims and tests.