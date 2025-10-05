# Physics scripts (derivation/code/physics/<domain>/)

Purpose
- Domain-scoped simulation and benchmark scripts. These are the source of truth for producing physics figures and logs under derivation/code/outputs/.

Directory layout
- Each research domain gets its own subfolder:
  - reaction_diffusion/ — canonical RD scripts (e.g., Fisher–KPP dispersion/front-speed)
  - fluid_dynamics/ — LBM→NS (Taylor–Green, lid-driven cavity), plus solver under fluid_dynamics/fluids/
  - tachyonic_condensation/ — EFT tube modes, etc.
- Example (fluid_dynamics):
  - Core solver: [fluids/lbm2d.py](Prometheus_VDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1)
  - Benchmarks:
    - [taylor_green_benchmark.py](Prometheus_VDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py:1)
    - [lid_cavity_benchmark.py](Prometheus_VDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:1)

Output routing
- Figures → derivation/code/outputs/figures/<domain>/
- Logs    → derivation/code/outputs/logs/<domain>/
- Filenames: <script_name>_YYYYMMDDThhmmssZ.ext (UTC timestamp)
- Override paths via CLI flags --outdir, --figure, --log when provided by the script.

Conventions
- Location: derivation/code/physics/<domain>/*.py
- Scripts must:
  - Accept reproducible CLI (with seeds where applicable).
  - Emit JSON logs with theory, params, metrics, outputs.figure, timestamp.
  - Emit a PNG figure (unless explicitly headless by design).
  - Record a pass/fail gate in metrics when applicable.
- Heavy numerics go here; unit tests belong under derivation/code/tests/<domain>/.

Examples

Reaction–Diffusion
- Dispersion experiment: [rd_dispersion_experiment.py](Prometheus_VDM/derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:1)
- Front speed: analogous front-speed scripts; outputs under reaction_diffusion/.

Fluid Dynamics (LBM→NS)
- Solver:
  - [fluids/lbm2d.py](Prometheus_VDM/derivation/code/physics/fluid_dynamics/fluids/lbm2d.py:1)
- Taylor–Green benchmark:
  - Runs TG vortex and fits log E(t) to recover ν.
  - Uses lattice scaling K² = k²(1/nx² + 1/ny²).
  - Outputs → figures/logs under fluid_dynamics/.
- Lid-driven cavity benchmark:
  - Runs no-slip box with moving lid; monitors ‖∇·v‖₂.
  - Outputs → figures/logs under fluid_dynamics/.

How to run (PowerShell)
- Activate venv:
  - & .\venv\Scripts\Activate.ps1
- Example (Taylor–Green):
  - python Prometheus_VDM/derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py --nx 256 --ny 256 --tau 0.8 --U0 0.05 --k 6.283185307179586 --steps 5000 --sample_every 50
- Example (Lid cavity):
  - python Prometheus_VDM/derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py --nx 128 --ny 128 --tau 0.7 --U_lid 0.1 --steps 15000 --sample_every 200

Design notes
- Keep solver code (fluids/, etc.) importable and benchmark-agnostic.
- Keep per-script acceptance gates aligned with BENCHMARKS_*.md.
- Prefer minimal external deps (numpy, matplotlib) for portability.

Cross-reference
- Benchmarks criteria: [BENCHMARKS_FLUIDS.md](Prometheus_VDM/derivation/BENCHMARKS_FLUIDS.md:1)
- Fluids derivation: [fluids_limit.md](Prometheus_VDM/derivation/fluids_limit.md:1)
- Tests overview: [tests/README.md](Prometheus_VDM/derivation/code/tests/README.md:1)