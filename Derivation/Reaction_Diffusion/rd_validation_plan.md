# RD validation plan (Fisher-KPP, 1D)

Purpose

- Establish reproducible numeric checks for the RD canonical model:

$$
u_t = D u_xx + r u (1 - u)
$$

with front speed 

$$
c_th = 2√(D r)
$$

and linear dispersion 

$$
σ(k) = r - D k²
$$

Scope

- Tests covered:
  1) Front-speed validation (pulled front, Fisher-KPP)
  2) Linear dispersion validation (periodic, linearized evolution)

Canonical scripts

- [rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py:1)
- [rd_front_speed_sweep.py](code/physics/rd_front_speed_sweep.py:1)
- [rd_dispersion_experiment.py](code/physics/rd_dispersion_experiment.py:1)
- Status log: [CORRECTIONS.md](CORRECTIONS.md:1)

Output locations

- Figures → derivation/code/outputs/figures/
- Logs → derivation/code/outputs/logs/
- Filenames: {script}_{UTC timestamp}.{png,json}
- Overridable via CLI: --outdir, --figure, --log

Front-speed test

- PDE: 

$$
∂t u = D ∂xx u + r u (1 - u)
$$

- Observable: front position $x_f(t)$ at level u = level (default 0.1); gradient-peak x_g(t) for cross-check.
- Method:
  - Neumann BCs; smooth step IC with far-field gating (u=0 ahead of the interface), optional left-gated noise.
  - Track $x_f$ only while a true crossing exists; robust fit of $x_f(t)$ on a late-time fraction window.
- Defaults: N=1024, L=200, D=1.0, r=0.25, T=80, cfl=0.2, seed=42, x0=-60, level=0.1, fit 0.6-0.9.
- Theory: 

$$
c_th = 2√(D r)
$$

- Acceptance:
  - $rel\_err = |c\_meas - c\_th| / |c\_th| ≤ 0.05$
  - $R² ≥ 0.98$
  - Cross-check: $|c\_meas\_grad - c\_th| / |c\_th| ≲ 0.05$ when available.
- CLI (PowerShell):
  - & .\venv\Scripts\Activate.ps1
  - python code/physics/rd_front_speed_experiment.py --N 1024 --L 200 --D 1.0 --r 0.25 --T 80 --cfl 0.2 --seed 42 --x0 -60 --level 0.1 --fit_start 0.6 --fit_end 0.9
- Sweep:
  - python code/physics/rd_front_speed_sweep.py

Dispersion test

- Linearized PDE: 

$$
u_t = D u_xx + r u
$$

(periodic BCs)

- Observable: per-mode growth rate $σ_meas(m)$ via linear fit of $log|Û_m(t)|$.
- Theory:
  - Discrete:
  
$$
σ_d(m) = r - (4 D / dx²) sin²(π m / N)
$$

- Continuum reference:
  
$$
σ_c(k) = r - D k², k = 2π m / L
$$

- Method:
  - Start from small random noise (amp0 ≪ 1), explicit Euler with diffusion CFL.
  - Record snapshots; fit on a fraction window away from startup transients.
- Defaults: N=1024, L=200, D=1.0, r=0.25, T=10, cfl=0.2, seed=42, amp0=1e-6, record=80, m_max=64, fit 0.1-0.4.
- Acceptance (array-level):
  - median relative error over good modes $(R²\_mode ≥ 0.95)$: $med\_rel\_err ≤ 0.10$
  - $R²\_array(measured vs σ\_d) ≥ 0.98$
- CLI (PowerShell):
  - & .\venv\Scripts\Activate.ps1
  - python code/physics/rd_dispersion_experiment.py --N 1024 --L 200 --D 1.0 --r 0.25 --T 10 --cfl 0.2 --seed 42 --amp0 1e-6 --record 80 --m_max 64 --fit_start 0.1 --fit_end 0.4

Reproducibility checklist

- Set seed and record it in logs (scripts do this by default).
- Confirm output JSON/PNG saved under derivation/code/outputs/{logs,figures}/.
- Verify acceptance metrics in JSON:
  - Front speed: metrics.passed = true
  - Dispersion: metrics.passed = true
- Keep generated artifacts under version control when passing.

Notes on stability and limits

- Explicit Euler step obeys $dt ≤ cfl · dx²/(2D)$\; scripts compute safe dt.
- Increase N and/or T to ensure clean linear regime and avoid boundary contamination.
- For front-speed, keep far-field exactly zero until the front arrives (gating is on by default).
- For dispersion, keep amplitude small (linear regime); use early-time fit window.

Provenance and tagging

- Front-speed: [PROVEN] in [CORRECTIONS.md](CORRECTIONS.md:1) with representative pass.
- Dispersion: [PROVEN]; default (N=1024): med_rel_err≈0.00145, R²_array≈0.99995; refinement (N=2048, m_max=128): med_rel_err≈0.00130, R²_array≈0.9928.

Expected artifacts

- Figures:
  - derivation/code/outputs/figures/rd_front_speed_experiment_<UTC>.png
  - derivation/code/outputs/figures/rd_dispersion_experiment_<UTC>.png
- Logs:
  - derivation/code/outputs/logs/rd_front_speed_experiment_<UTC>.json
  - derivation/code/outputs/logs/rd_dispersion_experiment_<UTC>.json
- Optional sweep CSV:
  - derivation/code/outputs/logs/rd_front_speed_sweep_<UTC>.csv

Open questions / next refinements

- Evaluate sensitivity of c_meas to level choice (0.05-0.2) and fit window; document invariance bands.
- Compare dispersion fit using windowed DFT vs rFFT magnitude; assess bias for near-zero/negative σ.
- Add unit tests for σ_d formula and Laplacian implementations.
- Mirror runners under fum_rt/physics for cross-stack parity.

Appendix: CLI quick refs

- Front speed (PASS example):
  - python code/physics/rd_front_speed_experiment.py --N 1024 --L 200 --D 1.0 --r 0.25 --T 80 --cfl 0.2 --seed 42 --x0 -60 --level 0.1 --fit_start 0.6 --fit_end 0.9
- Sweep:
  - python code/physics/rd_front_speed_sweep.py
- Dispersion:
  - python code/physics/rd_dispersion_experiment.py --N 1024 --L 200 --D 1.0 --r 0.25 --T 10 --cfl 0.2 --seed 42 --amp0 1e-6 --record 80 --m_max 64 --fit_start 0.1 --fit_end 0.4
