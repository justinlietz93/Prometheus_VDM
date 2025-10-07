# RD dispersion validation (linear regime)

Purpose

- Empirically validate the linear growth/decay rates of reaction-diffusion (Fisher-KPP linearized about u≈0):
  
$$
u_t = D u_xx + r u, with σ(k) = r - D k²
$$

(continuum) and

$$
σ_d(m) = r - (4D/dx²) sin²(π m/N)
$$

(discrete).

Status

- Solved: measured per-mode growth rates σ_meas match the discrete prediction within tight tolerance on default and refined grids.
- Scripts and outputs follow the same scheme as the front-speed validation.

References (implementation)

- Script: [rd_dispersion_experiment.py](code/physics/rd_dispersion_experiment.py:1)
- Validation plan: [rd_validation_plan.md](rd_validation_plan.md:1)
- Status log: [CORRECTIONS.md](CORRECTIONS.md:1)
- fum_rt parity runner: [rd_dispersion_runner.py](Prometheus_VDM/fum_rt/physics/rd_dispersion_runner.py:1)

Method

- Periodic BCs; explicit Euler on $u_t = D u_xx + r u$ with dt respecting diffusion CFL.
- Start from small iid Gaussian amplitude amp0 ≪ 1 to stay in the linear regime.
- Record snapshots; compute rFFT magnitudes $|Û_m(t)|; fit log|Û_m(t)|$ vs $t$ over a mid-early fraction window to estimate $σ_meas(m)$.
- Compare $σ_meas(m)$ to:
  - Discrete theory (primary): $σ_d(m) = r - (4D/dx²) sin²(π m/N)$
  - Continuum reference: $σ(k) = r - D k², with k = 2π m / L$

Output routing and naming

- Defaults:
  - Figures → derivation/code/outputs/figures/
  - Logs → derivation/code/outputs/logs/
- Filenames: script_name_YYYYMMDDThhmmssZ.ext (UTC timestamp)
- Overridable via CLI: --outdir, --figure, --log

How to run (PowerShell)

- Always activate venv before running commands:
  & .\venv\Scripts\Activate.ps1
- Ensure matplotlib is available (first run):
  python -m pip install matplotlib
- Default run (passes):
  python code/physics/rd_dispersion_experiment.py --N 1024 --L 200 --D 1.0 --r 0.25 --T 10 --cfl 0.2 --seed 42 --amp0 1e-6 --record 80 --m_max 64 --fit_start 0.1 --fit_end 0.4

Recommended defaults

- N=1024, L=200, D=1.0, r=0.25, T=10, cfl=0.2, seed=42, amp0=1e-6, record=80, m_max=64, fit 0.1-0.4
- Use early-mid window to avoid startup transients while staying in linear regime.

Acceptance criteria

- Array-level agreement:
  - median relative error over good modes (R²_mode ≥ 0.95): med_rel_err ≤ 0.10
  - R²_array(measured vs σ_d) ≥ 0.98

Representative results (logged)

- Default (N=1024): $med\_rel\_err ≈ 1.45e-3, R²\_array ≈ 0.99995$ [PASS]
- Refinement (N=2048, m_max=128): $med\_rel\_err ≈ 1.30e-3, R²\_array ≈ 0.9928$ [PASS]

Troubleshooting

- Low R² for some modes:
  - Increase record count, keep fit window away from very early times.
  - Keep amp0 small to remain in linear regime.
- Excess bias at high m:
  - Compare to discrete σ_d(m) (primary); continuum σ(k) deviates near Nyquist.
  - Increase N to push Nyquist higher.

fum_rt parity runner

- Independent mirror (same metrics/output schema) for cross-stack parity:
  - [rd_dispersion_runner.py](Prometheus_VDM/fum_rt/physics/rd_dispersion_runner.py:1)
- Rationale is documented in-file (“CHANGE REASON”): physics proven via derivation; runtime mirror does not alter core dynamics.

Reproduction checklist

1) Activate venv: & .\venv\Scripts\Activate.ps1
2) Install deps once: python -m pip install matplotlib
3) Run default command above; confirm in JSON:
   - metrics.med_rel_err ≤ 0.10
   - metrics.r2_array ≥ 0.98
4) Archive produced JSON/PNG under version control as needed.

Provenance and tagging

- Dispersion is [PROVEN] in [CORRECTIONS.md](CORRECTIONS.md:1) with default and refined grid results.
