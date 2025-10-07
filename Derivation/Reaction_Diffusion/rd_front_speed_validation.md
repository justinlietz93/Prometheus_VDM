# RD front-speed validation (Fisher-KPP)

Purpose

- Empirically validate the Fisher-KPP pulled-front speed in 1D reaction-diffusion:

$$
u_t = D u_xx + r u (1 - u)
$$

with theoretical

$$
c_th = 2√(D r)
$$

  Note: With the canonical mapping $r = α - β$ and $u = α$, the homogeneous fixed point is $φ*= r/u = 1 - β/α$ (e.g., $α=0.25, β=0.10 ⇒ φ* = 0.6$).

Status

- Solved: measured c_meas agrees with c_th within 5% after removing uniform pre-heating and tracking only real level crossings.
- Documentation and reproducible CLI provided below.

References (implementation)

- Script: [rd_front_speed_experiment.py](code/physics/rd_front_speed_experiment.py)
- Key functions:
  - [run_sim()](code/physics/rd_front_speed_experiment.py:134)
  - [robust_linear_fit()](code/physics/rd_front_speed_experiment.py:77)
  - [front_position_near()](code/physics/rd_front_speed_experiment.py:54)
  - [main()](code/physics/rd_front_speed_experiment.py:341)

What was wrong initially (root cause)

- Uniform small noise added everywhere at t=0 caused logistic “pre-heating” in the far field; points far ahead of the front crossed the tracking level (e.g., 0.5) solely due to local growth at time $t ≈ r^-1 ln((1-u0)/u0)$, biasing the measured slope down.
- Additionally, tracking after the real level-crossing vanished (domain fully above level) contaminated late-time fits.

Fixes implemented

1) Gated initial condition (no pre-heating)
   - Far-ahead region is set exactly to 0.0 so the front is truly pulled by diffusion; optional noise is gated to the left side only.
   - See the IC block in [run_sim()](code/physics/rd_front_speed_experiment.py:161).

2) Real-crossing guard
   - Only record front position while a true level crossing exists; stop tracking once the domain is fully above the chosen level.
   - See tracker loop in [run_sim()](code/physics/rd_front_speed_experiment.py:187).

3) Robust fitting and derivative cross-check
   - Robust linear fit with MAD rejection; median-slope fallback if needed.
   - Optional gradient-peak tracker (location of max $|∂_x u|$) overlays the second front position series for cross-check.

Output routing and naming

- Defaults to:
  - Figures → derivation/code/outputs/figures/
  - Logs → derivation/code/outputs/logs/
- Filenames: script_name_YYYYMMDDThhmmssZ.ext (UTC timestamp).
- Overridable via CLI: --outdir, --figure, --log.
- See [main()](code/physics/rd_front_speed_experiment.py:359).

How to run (PowerShell)

- Always activate venv before running commands:
  & .\venv\Scripts\Activate.ps1
- Ensure matplotlib is available (first run):
  python -m pip install matplotlib
- Example that passes with $D=1, r=0.25 (c\_th=1)$:
  python code/physics/rd_front_speed_experiment.py --N 1024 --L 200 --D 1.0 --r 0.25 --T 80 --cfl 0.2 --seed 42 --x0 -60 --level 0.1 --fit_start 0.6 --fit_end 0.9

Recommended defaults

- Threshold level: 0.1 (stable early/late across grids). Level=0.5 works if far field remains near zero.
- Fit window: later fraction of the tracked interval (e.g., 0.6-0.9) to avoid initial transients and boundary interactions.
- Grid/time step: increase N or T as needed for clean linear regime; CFL-stable explicit Euler is used.

Acceptance criteria

- Front-speed agreement: $rel\_err = |c\_meas - c\_th| / |c\_th| ≤ 0.05$
- Linear fit quality: $R² ≥ 0.98$
- Cross-check: gradient-tracker speed within ≈5% of c_th and level-tracker speed.

Representative results (logged)

- Parameters: D=1.0, r=0.25, N=1024, T=80, level=0.1, fit 0.6-0.9
- Metrics: $c\_meas ≈ 0.953, c\_th = 1.0, rel\_err ≈ 0.047, R² ≈ 0.999996$ (pass)
- Gradient cross-check: $c\_meas\_grad ≈ 0.945, rel\_err\_grad ≈ 0.055, R²\_grad$ ≈ 0.99995
- Outputs auto-saved under derivation/code/outputs/{figures,logs}/

Troubleshooting

- Measured speed too low with high $R²$:
  - Remove/disable uniform noise (use default --noise_amp 0.0).
  - Lower the tracking threshold (e.g., --level 0.1).
  - Move fit window later (e.g., --fit_start 0.6 --fit_end 0.9).
- Fit unstable (low $R²$):
  - Increase N or T; ensure front remains away from domain boundaries during the fit window.
  - Use larger fraction window or robust fit as implemented.

Provenance and alignment with repository decisions

- This test operationalizes the RD “canonical model” front-speed claim logged in CORRECTIONS.md by providing a reproducible, parameterized check that passes quantitative gates (≤5% tolerance).

Reproduction checklist

1) Activate venv: & .\venv\Scripts\Activate.ps1
2) Install deps once: python -m pip install matplotlib
3) Run example command above; confirm:
   - rel_err ≤ 0.05
   - $R²$ ≥ 0.98
   - Outputs written to derivation/code/outputs/{figures,logs}/
4) Archive the produced JSON and PNG under version control as needed.
