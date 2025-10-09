<!-- DOC-GUARD: CANONICAL -->
<!-- RULES for maintaining this file are here: /mnt/ironwolf/git/Prometheus_VDM/prompts/validation_metrics_maintenance.md -->
<!-- markdownlint-disable MD033 MD022 MD032 MD001 -->
# VDM Validation Metrics & KPIs (Auto-compiled)

Last updated: 2025-10-09 (commit f1e74a5)

**Scope:** Single source of truth for validation metrics used in this repository: names, purposes, thresholds/bands, and references to their definitions and implementations.  
**Rules:** Reference-only. Link to equations/constants/symbols/scripts; do not restate formulas here.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing math.

---

## Macro Banner (Headline KPIs)

Key validation metrics explicitly referenced as acceptance gates across the repository:

- [Front Speed Relative Error (RD)](#kpi-front-speed-rel-err)
- [Taylor-Green Viscosity Recovery Error](#kpi-taylor-green-nu-rel-err)
- [Q-Invariant Maximum Drift](#kpi-q-invariant-drift)
- [ΛCDM Residual (w+1)](#kpi-lcdm-residual)
- [Connectome Entropy](#kpi-connectome-entropy)

---

## Core Dynamics Metrics

### Reaction-Diffusion (Fisher-KPP)

#### Front Speed Relative Error  <a id="kpi-front-speed-rel-err"></a>

**Symbol (if any):** $ \text{rel\_err}_c $ <br/>
**Purpose:** Validate pulled-front speed measurement against theoretical prediction for Fisher-KPP equation <br/>
**Defined by:** `EQUATIONS.md#vdm-e-033` <br/>
**Inputs:** [`D`](CONSTANTS.md#const-D) • [`r`](CONSTANTS.md#const-r) <br/>
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:77-119 • 17a0b72` (robust_linear_fit) <br/>
`derivation/code/tests/reaction_diffusion/test_rd_acceptance.py:21-28 • 17a0b72` <br/>
**Pass band / thresholds:** `≤ 0.05` → `CONSTANTS.md#const-acceptance_rel_err` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** `N=1024, L=200, D=1.0, r=0.25, T=80` (default params) <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_*.png` <br/>
**Notes:** Acceptance gate requires `R² ≥ 0.98` on front position linear fit (see [R² Front Position Fit](#kpi-r2-front-fit)) <br/>

#### R² Front Position Fit  <a id="kpi-r2-front-fit"></a>

**Symbol (if any):** $ R^2_{\text{front}} $ <br/>
**Purpose:** Goodness-of-fit for linear regression of front position vs time <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Time series of front positions from `front_position` function <br/>
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:77-119 • 17a0b72` <br/>
**Pass band / thresholds:** `≥ 0.98` → test assertion line 26   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Same as Front Speed Relative Error <br/>
**Primary figure/artifact (if referenced):** Included in JSON metrics output <br/>
**Notes:** Uses robust linear fit with MAD-based outlier rejection <br/>

#### Dispersion Median Relative Error  <a id="kpi-dispersion-med-rel-err"></a>

**Symbol (if any):** $ \text{med\_rel\_err}_{\sigma} $ <br/>
**Purpose:** Validate linear stability analysis by comparing measured vs theoretical growth rates <br/>
**Defined by:** `EQUATIONS.md#vdm-e-035` <br/>
**Inputs:** [`D`](CONSTANTS.md#const-D) • [`r`](CONSTANTS.md#const-r) • mode numbers m → wavenumbers k_m <br/>
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:analyze_dispersion • 17a0b72` <br/>
`derivation/code/tests/reaction_diffusion/test_rd_acceptance.py:30-36 • 17a0b72` <br/>
**Pass band / thresholds:** `≤ 0.10` (10% median relative error) → test assertion line 35   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** `N=1024, L=200, D=1.0, r=0.25, T=10, m_max=64` <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_*.png` <br/>
**Notes:** Growth rates fit from linearized mode amplitudes `σ(k) = r - Dk²` (METRICS.md line 4) <br/>

#### R² Dispersion Array Fit  <a id="kpi-r2-dispersion-array"></a>

**Symbol (if any):** $ R^2_{\sigma} $ <br/>
**Purpose:** Goodness-of-fit for growth rate regression across multiple Fourier modes <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Time series of Fourier mode amplitudes <br/>
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:analyze_dispersion • 17a0b72` <br/>
**Pass band / thresholds:** `≥ 0.98` → test assertion line 36   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Same as Dispersion Median Relative Error <br/>
**Primary figure/artifact (if referenced):** Included in JSON metrics output <br/>
**Notes:** Computed per mode, then aggregated across modes <br/>

### Fluid Dynamics (LBM → Navier-Stokes)

#### Taylor-Green Viscosity Recovery Error  <a id="kpi-taylor-green-nu-rel-err"></a>

**Symbol (if any):** $ \text{rel\_err}_{\nu} $ <br/>
**Purpose:** Certify LBM→NS reduction by recovering kinematic viscosity from energy decay <br/>
**Defined by:** TODO → add equation anchor - source: τ - 0.5 <br/>
**Inputs:** [`τ`](CONSTANTS.md#const-tau-taylor) • grid dimensions → wavenumber correction `K² = k²(1/nx² + 1/ny²)` <br/>
**Computation implemented at:** `derivation/code/tests/fluid_dynamics/test_taylor_green_decay.py:42-83 • 17a0b72` <br/>
`derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py • 17a0b72` <br/>
**Pass band / thresholds:** `≤ 0.05` (5%) at baseline grid `≥ 256²` → test assertion line 83 and BENCHMARKS_FLUIDS.md:19   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** `nx=256, ny=256, τ=0.8 (ν_th=0.1), U0=0.05, steps=3000-5000` <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/fluid_dynamics/taylor_green_benchmark_*.png` <br/>
**Notes:** Refinement test: error decreases with doubled resolution consistent with scheme order (BENCHMARKS_FLUIDS.md:20) <br/>

#### Lid Cavity Divergence Maximum  <a id="kpi-lid-cavity-div-max"></a>

**Symbol (if any):** $ \max_t \|\nabla \cdot \mathbf{v}\|_2 $ <br/>
**Purpose:** Incompressibility constraint verification for LBM flow solver <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Velocity field `(u_x, u_y)` from LBM moments <br/>
**Computation implemented at:** `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:_metrics • 17a0b72` <br/>
**Pass band / thresholds:** `≤ 1e-6` (double precision) → BENCHMARKS_FLUIDS.md:28   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** `nx=128, ny=128, τ=0.7, U_lid=0.1, steps=15000` <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/fluid_dynamics/lid_cavity_benchmark_*.png` <br/>
**Notes:** Monitored over time; max value compared against threshold <br/>

### Conservation Law (QFUM Logistic Invariant)

#### Q-Invariant Maximum Drift  <a id="kpi-q-invariant-drift"></a>

**Symbol (if any):** $ \Delta Q_{\max} = \max_t |Q(t) - Q(0)| $ <br/>
**Purpose:** Verify logarithmic first integral conservation for autonomous logistic ODE <br/>
**Defined by:** `EQUATIONS.md#vdm-e-071` <br/>
**Inputs:** [`r`](CONSTANTS.md#const-r) • `u` • solution trajectory W(t) <br/>
**Computation implemented at:** `derivation/code/physics/conservation_law/qfum_validate.py:118-193 • 17a0b72` (Q_invariant function + plot_Q_drift) <br/>
**Pass band / thresholds:** `≤ 1e-8` for RK4, `≤ 1e-5` for Euler → qfum_validate.py:277 (drift_gate)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** `r=0.15, u=0.25, W0=0.12-0.62, T=40, dt=0.001 (RK4)` <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/conservation_law/qfum_Q_drift_*.png` <br/>
**Notes:** Acceptance routed to pass/stable/arxiv outputs based on drift_gate (lines 277-294) <br/>

#### Convergence Slope (dt)  <a id="kpi-convergence-slope-dt"></a>

**Symbol (if any):** $ p_{\text{conv}} $ (power law exponent) <br/>
**Purpose:** Verify solver order-of-accuracy via convergence study <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Series of dt values and corresponding `ΔQ_max` measurements <br/>
**Computation implemented at:** `derivation/code/physics/conservation_law/qfum_validate.py:153-163 • 17a0b72` (fit_loglog) <br/>
**Pass band / thresholds:** No explicit threshold; informational (expected p ≈ 4 for RK4, p ≈ 1 for Euler)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** `dt ∈ {0.002, 0.001, 0.0005}` for convergence sweep <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/conservation_law/qfum_convergence_*.png` <br/>
**Notes:** Uses `r2` goodness-of-fit; reported in ConvergenceMetrics dataclass (lines 142-150) <br/>

### Memory Steering

#### Memory Steering Pole Fit Error  <a id="kpi-memory-pole-fit-err"></a>

**Symbol (if any):** $ |p_{\text{fit}} - p_{\text{pred}}| $ <br/>
**Purpose:** Verify linear response and stability of discrete leaky integrator <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** [`g`](CONSTANTS.md#const-alpha) (gain) • `λ` (leak) • step response time series <br/>
**Computation implemented at:** `derivation/code/physics/memory_steering/memory_steering_acceptance.py:run_filter • 17a0b72` <br/>
`derivation/code/tests/memory_steering/test_memory_steering.py • 17a0b72` <br/>
**Pass band / thresholds:** `≤ 0.02` (absolute) → memory_steering_acceptance_verification.md:47   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** `g=0.12, λ=0.08 → p_pred=0.80` (default acceptance run) <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/memory_steering/step_response_*.png` <br/>
**Notes:** Fixed point error `|M_final - M*| ≤ 0.01` also checked (line 48) <br/>

#### Memory Steering Canonical Void Target  <a id="kpi-memory-void-target"></a>

**Symbol (if any):** $ M_* = 0.6 $ <br/>
**Purpose:** Validate void equilibrium target W ≈ 0.6 with canonical parameter mapping <br/>
**Defined by:** TODO → add equation anchor - source: g+λ <br/>
**Inputs:** `g=1.5λ` • constant signal `s=1` <br/>
**Computation implemented at:** `derivation/code/tests/memory_steering/test_memory_steering.py:test_canonical_void • 17a0b72` <br/>
**Pass band / thresholds:** `|M_final - 0.6| ≤ 0.02` → memory_steering_acceptance_verification.md:52-53   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Seeds {0,1,2}, 512 steps (step at t=64) <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/memory_steering/canonical_void_*.png` <br/>
**Notes:** Must hold across multiple seeds for reproducibility <br/>

#### Memory Steering SNR Improvement  <a id="kpi-memory-snr-improvement"></a>

**Symbol (if any):** $ \Delta \text{SNR} = \text{SNR}_{\text{out}} - \text{SNR}_{\text{in}} $ <br/>
**Purpose:** Verify noise suppression capability of leaky integrator filter <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Noisy input signal `s(t) = s_sig(t) + n(t)` with `σ_n = 0.05` (default) <br/>
**Computation implemented at:** `derivation/code/physics/memory_steering/memory_steering_acceptance.py • 17a0b72` <br/>
**Pass band / thresholds:** `≥ 3 dB` improvement → memory_steering_acceptance_verification.md:57   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Low-frequency sinusoid + white noise, default noise σ=0.05 <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/memory_steering/noise_suppression_*.png` <br/>
**Notes:** Uses parallel signal-only filter for ground-truth comparison <br/>

### Tachyonic Condensation (Tube)

#### Spectrum Coverage (physically admissible)  <a id="kpi-tube-cov-phys"></a>

**Symbol (if any):** $\mathrm{cov}_{\mathrm{phys}}$  <br/>
**Purpose:** Gate for completeness of the discrete mode spectrum over the physically admissible set (pairs $(R,\ell)$ for which the secular equation admits a root by sign-change scan).  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-096` (coverage metrics; see tube secular equation at `EQUATIONS.md#vdm-e-095`)  <br/>
**Inputs:** Radius grid $R$, orbital index $\ell\in\{0,1,\ldots,\ell_{\max}\}$, admissibility mask from $\theta$-scan sign-change heuristic  <br/>
**Computation implemented at:** `derivation/code/physics/tachyonic_condensation/run_tachyon_tube.py:overview_and_heatmap`  <br/>
**Pass band / thresholds:** $\mathrm{cov}_{\mathrm{phys}} \ge 0.95$ (v1 achieved 1.000)  <br/>
**Units / normalization:** dimensionless fraction  <br/>
**Typical datasets / experiments:** tag `tube-spectrum-v1` with $\mu=1$, $\ell_{\max}=8$, $R\in[1,6]$  <br/>
**Primary figure/artifact (if referenced):** `code/outputs/figures/tachyonic_condensation/*tube_spectrum_overview__<tag>.png` • `.../tube_spectrum_heatmap__<tag>.png` • summary JSON `.../tube_spectrum_summary__<tag>.json`  <br/>
**Notes:** Denominator counts only physically admissible pairs; see transparency metric below for raw denominator.

#### Spectrum Coverage (raw transparency)  <a id="kpi-tube-cov-raw"></a>

**Symbol (if any):** $\mathrm{cov}_{\mathrm{raw}}$  <br/>
**Purpose:** Transparency metric reporting found roots over the full attempted set $(R,\ell)$ irrespective of admissibility; not used for gating.  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-096`  <br/>
**Inputs:** Total attempts vs successes from spectrum solver  <br/>
**Computation implemented at:** `derivation/code/physics/tachyonic_condensation/run_tachyon_tube.py:spectrum_solve`  <br/>
**Pass band / thresholds:** none (informational)  <br/>
**Units / normalization:** dimensionless fraction  <br/>
**Typical datasets / experiments:** Same as above  <br/>
**Primary figure/artifact (if referenced):** Included in spectrum summary JSON  <br/>
**Notes:** Report alongside $\mathrm{cov}_{\mathrm{phys}}$ to preserve comparability with earlier attempts.

#### Secular Max Residual (informational)  <a id="kpi-tube-residual"></a>

**Symbol (if any):** $\max |\mathcal{S}(\kappa)|$  <br/>
**Purpose:** Monitor the maximum absolute value of the secular equation $\mathcal{S}(\kappa)$ at reported roots for diagnostic purposes.  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-095`  <br/>
**Inputs:** Per-root residuals from bracketed solver  <br/>
**Computation implemented at:** `derivation/code/physics/tachyonic_condensation/cylinder_modes.py:secular_residual`  <br/>
**Pass band / thresholds:** none (informational in v1)  <br/>
**Units / normalization:** dimensionless  <br/>
**Typical datasets / experiments:** Same as above  <br/>
**Primary figure/artifact (if referenced):** Included in spectrum summary JSON  <br/>
**Notes:** Consider adding a tolerance gate in v2 (e.g., $\le 10^{-2}$) once bracket refinement policies are finalized.

#### Condensation Finite-Fraction  <a id="kpi-tube-finite-fraction"></a>

**Symbol (if any):** $f_{\mathrm{finite}}$  <br/>
**Purpose:** Fraction of scanned radii with finite, real condensate amplitudes and energies after diagonal quartic projection.  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-097` (condensation energy and fit)  <br/>
**Inputs:** Radius grid $R$, fitted coefficients from quadratic energy fit near minimum  <br/>
**Computation implemented at:** `derivation/code/physics/tachyonic_condensation/run_tachyon_tube.py:run_condensation_scan`  <br/>
**Pass band / thresholds:** $f_{\mathrm{finite}} \ge 0.80$  <br/>
**Units / normalization:** dimensionless fraction  <br/>
**Typical datasets / experiments:** tag `tube-condensation-v1` with $R\in[0.8, 6.0]$  <br/>
**Primary figure/artifact (if referenced):** `code/outputs/figures/tachyonic_condensation/*tube_energy_scan__<tag>.png` • JSON `.../tube_condensation_summary__<tag>.json` • CSV `.../tube_energy_scan__<tag>.csv`  <br/>
**Notes:** Diagonal-mode baseline; off-diagonal quartic couplings deferred.

#### Condensation Curvature/Minimum OK  <a id="kpi-tube-curvature-ok"></a>

**Symbol (if any):** `curvature_ok` (boolean)  <br/>
**Purpose:** Verify interior minimum exists with positive quadratic curvature $a>0$ in local fit $E(R) \approx aR^2 + bR + c$ around $R_{\min}$.  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-097`  <br/>
**Inputs:** Local polynomial fit coefficients $(a,b,c)$ and location $R_{\min}$  <br/>
**Computation implemented at:** `derivation/code/physics/tachyonic_condensation/run_tachyon_tube.py:run_condensation_scan`  <br/>
**Pass band / thresholds:** `curvature_ok = true` and $R_{\min}$ interior to scan range  <br/>
**Units / normalization:** energy in chosen normalization (dimensionless under baseline)  <br/>
**Typical datasets / experiments:** Same as above  <br/>
**Primary figure/artifact (if referenced):** Energy scan figure + CSV; summary JSON includes `fit_coeffs`, `min_R`, `min_E`  <br/>
**Notes:** Report $(a,b,c)$, $R_{\min}$, and $E_{\min}$ in JSON for reproducibility.

---

## Stability & Safety Guards

#### ΛCDM Residual (w+1)  <a id="kpi-lcdm-residual"></a>

**Symbol (if any):** $ |w(z) + 1| $ <br/>
**Purpose:** Validate vacuum equation-of-state against ΛCDM baseline for cosmology channel <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Redshift z, horizon activity events, retarded kernel parameters <br/>
**Computation implemented at:** `fum_rt/physics/vacuum_demographics_harness.py:230-283 • 17a0b72` (_aggregate_metrics) <br/>
**Pass band / thresholds:** `≤ 5e-4` (default residual_tol) → vacuum_demographics_harness.py:383 (CLI arg)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Synthetic horizon activity tape or user-supplied events <br/>
**Primary figure/artifact (if referenced):** w(z)+1 residual plot (figure_path output) <br/>
**Notes:** Harness exits with status `NEEDS_RECAL` when tolerance exceeded (line 233) <br/>

#### FRW Continuity RMS Residual  <a id="kpi-frw-continuity-rms"></a>

**Symbol (if any):** $ \text{RMS}_{\text{FRW}} $  <br/>
**Purpose:** Validate energy continuity in FRW cosmology by measuring RMS of discrete residual $\frac{d}{dt}(\rho a^3) + w\,\rho\,\frac{d}{dt}(a^3)$ (dust baseline $w=0$)  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-0xx` (FRW continuity; reference only)  <br/>
**Inputs:** $\rho(t)$, $a(t)$, $t$  <br/>
**Computation implemented at:** `derivation/code/physics/cosmology/run_frw_balance.py:continuity_residual, run_frw_balance`  <br/>
**Pass band / thresholds:** `≤ tol_rms` (default `1e-6` baseline; dust sanity achieves O(1e-15))  <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md#cosmology`  <br/>
**Typical datasets / experiments:** Dust sanity test `\rho \propto a^{-3}` on uniform `t` grid (201 points)  <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/cosmology/frw_continuity_residual__<tag>.png`  <br/>
**Notes:** Emits CONTRADICTION_REPORT with artifacts on failure; CSV series in logs for audit.

#### A6 Collapse Max Envelope  <a id="kpi-a6-envelope-max"></a>

**Symbol (if any):** $ E_{\max} $  <br/>
**Purpose:** Universality gate for junction logistic collapse; ensures curves at multiple $\Theta$ collapse within a narrow band  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-a6-collapse` (reference only)  <br/>
**Inputs:** Interpolated envelope series over shared $X$ grid  <br/>
**Computation implemented at:** `derivation/code/physics/collapse/run_a6_collapse.py:compute_envelope, run_a6`  <br/>
**Pass band / thresholds:** `\le 0.02` (≤ 2%)  <br/>
**Units / normalization:** dimensionless  <br/>
**Typical datasets / experiments:** $\Theta \in \{1.5, 2.5, 3.5\}$, $\Delta m \in [-2,2]$, trials ≥ 2000 per point  <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/collapse/a6_collapse_overlay__<tag>.png`  <br/>
**Notes:** Logs per-curve raw data and envelope CSV for audit; CONTRADICTION_REPORT on failure.

### Dark Photon Portals

#### Regime Split Annotation Present  <a id="kpi-dp-regime-split"></a>

**Symbol (if any):** -  <br/>
**Purpose:** Ensure noise budget analysis properly annotates regime split (quantum‑ vs thermal‑limited)  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-dp-noise`  <br/>
**Inputs:** SNR curves vs integration time/bandwidth; PSD components  <br/>
**Computation implemented at:** `derivation/code/physics/dark_photons/run_dp_noise_budget.py:run_noise_budget`  <br/>
**Pass band / thresholds:** Annotation present with boundary estimate `t_*`/bandwidth crossover; curve continuity across regimes  <br/>
**Units / normalization:** detector‑native; SNR dimensionless  <br/>
**Typical datasets / experiments:** Detector models spanning quantum and thermal limits  <br/>
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/dark_photons/noise_budget__<tag>.png`  <br/>
**Notes:** Advisory KPI; pairs with Fisher consistency below.
<br/>
**Status:** planned (pre-registered); execution blocked pending proposal approval. Engineering-only smokes must be run with `--allow-unapproved` and are quarantined from RESULTS/KPIs.

#### Fisher Consistency (Finite‑Difference Cross‑Check)  <a id="kpi-dp-fisher-consistency"></a>

**Symbol (if any):** $ \Delta_{\text{FD}} $  <br/>
**Purpose:** Cross‑check quick Fisher estimate for $\varepsilon$ against finite‑difference; guards against analytic mismatch  <br/>
**Defined by:** `EQUATIONS.md#vdm-e-dp-fisher`  <br/>
**Inputs:** Likelihood model, step size `h`, baseline $\varepsilon$  <br/>
**Computation implemented at:** `derivation/code/physics/dark_photons/run_dp_fisher_check.py:run_fisher_check`  <br/>
**Pass band / thresholds:** `\text{rel\_err} \le 0.1` (≤ 10%)  <br/>
**Units / normalization:** dimensionless  <br/>
**Typical datasets / experiments:** Simulated signals with known injection  <br/>
**Primary figure/artifact (if referenced):** JSON log with `sigma_epsilon` and `finite_difference_check` fields  <br/>
**Notes:** Report step size and numerical stability notes in `params`.
<br/>
**Status:** planned (pre-registered); execution blocked pending proposal approval. Engineering-only smokes must be run with `--allow-unapproved` and are quarantined from RESULTS/KPIs.

#### CFL Condition  <a id="kpi-cfl-condition"></a>

**Symbol (if any):** $ \Delta t \lesssim \frac{\Delta x^2}{2dD} $ <br/>
**Purpose:** Stability constraint for explicit finite-difference diffusion schemes <br/>
**Defined by:** `EQUATIONS.md#vdm-e-006` <br/>
**Inputs:** [`D`](CONSTANTS.md#const-D) • [`dx`] • spatial dimension d <br/>
**Computation implemented at:** Throughout RD experiments: `dt = cfl * dx²/(2*D)` pattern <br/>
`derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py • 17a0b72` <br/>
**Pass band / thresholds:** `cfl` guard → `CONSTANTS.md#const-cfl` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** All explicit time-stepping simulations <br/>
**Primary figure/artifact (if referenced):** N/A (stability constraint, not measured) <br/>
**Notes:** Also documented in EQUATIONS.md#VDM-E-006 for agency field; AGENCY_FIELD.md:76 <br/>

#### Drift Gate (Conservation Law)  <a id="kpi-drift-gate"></a>

**Symbol (if any):** $ \text{drift\_gate} $ <br/>
**Purpose:** Acceptance threshold for routing QFUM validation outputs <br/>
**Defined by:** `EQUATIONS.md#vdm-e-073` <br/>
**Inputs:** Solver type (RK4 vs Euler) determines threshold <br/>
**Computation implemented at:** `derivation/code/physics/conservation_law/qfum_validate.py:277 • 17a0b72` <br/>
**Pass band / thresholds:** `1e-8` (RK4), `1e-5` (Euler) → line 277   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Part of QFUM validation acceptance criteria <br/>
**Primary figure/artifact (if referenced):** N/A (threshold constant) <br/>
**Notes:** Pass: `drift_ok` → outputs/stable/; fail → outputs/failed_runs/ (lines 278-294) <br/>

#### B1 Spike Detection (z-score)  <a id="kpi-b1-spike-z"></a>

**Symbol (if any):** $ z_{\text{spike}} $ <br/>
**Purpose:** Threshold for detecting anomalies in cyclomatic complexity time series <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Cyclomatic complexity series, [`speak_z`](CONSTANTS.md#const-speak_z_4) threshold <br/>
**Computation implemented at:** `fum_rt/core/metrics.py:55-116 • 17a0b72` (StreamingZEMA class) <br/>
`fum_rt/nexus.py • 17a0b72` (b1_detector instantiation) <br/>
**Pass band / thresholds:** [`speak_z=3.5`](CONSTANTS.md#const-speak_z_4) for phase 4 (problem-solving) → runtime/phase.py:55 <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry, void-native signals <br/>
**Primary figure/artifact (if referenced):** N/A (streaming detector, no static artifact) <br/>
**Notes:** Uses hysteresis [`speak_hysteresis=1.2`](CONSTANTS.md#const-speak_hysteresis_4) to prevent chatter; cooldown `min_interval_ticks` <br/>

---

## Performance / Efficiency Metrics

#### Average Weight  <a id="kpi-avg-weight"></a>

**Symbol (if any):** $ \bar{W} $ <br/>
**Purpose:** Monitor global connectome activity level <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Connectome weight matrix W <br/>
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics) <br/>
**Pass band / thresholds:** No explicit threshold; informational metric   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry at each tick <br/>
**Primary figure/artifact (if referenced):** Logged in telemetry JSON <br/>
**Notes:** Returned as `avg_weight` in metrics dict (line 24) <br/>

#### Active Synapses  <a id="kpi-active-synapses"></a>

**Symbol (if any):** $ N_{\text{active}} $ <br/>
**Purpose:** Count active edges in connectome graph <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Connectome E (efficacy) and A (adjacency) matrices, threshold <br/>
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics → active_edge_count method) <br/>
**Pass band / thresholds:** No explicit threshold; sparsity/utilization indicator   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry, golden run parity checks <br/>
**Primary figure/artifact (if referenced):** Tracked in tools/golden_run_parity.py:default metric keys <br/>
**Notes:** Alias: `active_edges` in some contexts <br/>

#### Cohesion Components  <a id="kpi-cohesion-components"></a>

**Symbol (if any):** $ C_{\text{comp}} $ <br/>
**Purpose:** Detect graph fragmentation and emergent multi-agent behavior <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Connectome active subgraph (E > threshold & A == 1) <br/>
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics → connected_components method) <br/>
**Pass band / thresholds:** `> 1` triggers emergent GDSP activation → fum_rt/runtime/loop/main.py:comp check   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry, UTD event scans <br/>
**Primary figure/artifact (if referenced):** Logged in emission records, redis outputs <br/>
**Notes:** Key trigger for domain cartography scheduling; part of pathology detection (Blueprint Rule 4.1) <br/>

#### Complexity Cycles  <a id="kpi-complexity-cycles"></a>

**Symbol (if any):** $ \text{cyclomatic\_complexity} $ <br/>
**Purpose:** Proxy for topological complexity; feeds B1 spike detector <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Connectome active subgraph <br/>
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics → cyclomatic_complexity method) <br/>
**Pass band / thresholds:** No direct threshold; first-difference used by [B1 Spike Detection](#kpi-b1-spike-z)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry; augmented by adc_cycle_hits when ADC active <br/>
**Primary figure/artifact (if referenced):** N/A (streaming input to spike detector) <br/>
**Notes:** StreamingZEMA monitors `Δ(complexity_cycles)` for anomalies (fum_rt/core/metrics.py:50-52) <br/>

#### Connectome Entropy  <a id="kpi-connectome-entropy"></a>

**Symbol (if any):** $ H = -\sum p_i \log p_i $ <br/>
**Purpose:** Global pathological structure detection via degree distribution entropy <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Connectome active edges → degree vector → probability distribution <br/>
**Computation implemented at:** `fum_rt/core/metrics.py:31-47 • 17a0b72` (connectome_entropy function) <br/>
**Pass band / thresholds:** No explicit threshold; supports Active Domain Cartography scheduling (Blueprint Rule 7)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry, golden run parity, UTD scans <br/>
**Primary figure/artifact (if referenced):** Logged in emission records <br/>
**Notes:** Formula: `H = -Σ p_i log(p_i)` where p is degree distribution (line 34 comment) <br/>

#### Void Traveler Entropy  <a id="kpi-vt-entropy"></a>

**Symbol (if any):** $ H_{\text{VT}} $ <br/>
**Purpose:** Void-native signal for tracking novelty/diversity in walker behavior <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Void traveler state/trajectory data <br/>
**Computation implemented at:** Void traveler subsystem (specific implementation TODO in sparse-mode connectome) <br/>
**Pass band / thresholds:** No explicit threshold; used in SIE TD proxy and golden run parity   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry, tracked over time for temporal difference signals <br/>
**Primary figure/artifact (if referenced):** Logged in composer, emission, redis outputs <br/>
**Notes:** Previous value tracked in `_prev_vt_entropy` for TD calculation (fum_rt/nexus.py) <br/>

#### Void Traveler Coverage  <a id="kpi-vt-coverage"></a>

**Symbol (if any):** $ \text{vt\_coverage} $ <br/>
**Purpose:** Measure spatial exploration extent of void travelers <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Void traveler trajectory data <br/>
**Computation implemented at:** Void walker traversal metrics (implementation details in walker subsystem) <br/>
**Pass band / thresholds:** No explicit threshold; diagnostic/observability metric   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry, golden run parity comparisons <br/>
**Primary figure/artifact (if referenced):** Logged in emission records <br/>
**Notes:** Used in smoke tests: `obs:vt_coverage↑` (fum_rt/runtime/helpers/smoke.py) <br/>

#### SIE Valence  <a id="kpi-sie-valence"></a>

**Symbol (if any):** $ \text{sie\_valence\_01} $ or $ \text{sie\_v2\_valence\_01} $ <br/>
**Purpose:** Scalar valence metric from Semantic Integration Engine for speak gating <br/>
**Defined by:** TODO → add equation anchor - source: v2 is preferred version with fallback to v1 <br/>
**Inputs:** SIE processing outputs, connectome state <br/>
**Computation implemented at:** SIE subsystem (exact implementation in engine) <br/>
**Pass band / thresholds:** [`speak_valence_thresh`](CONSTANTS.md#const-speak_valence_thresh_4) per phase (e.g., phase 4 threshold) <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry, golden run parity, emission records <br/>
**Primary figure/artifact (if referenced):** Logged in telemetry, redis outputs, composer <br/>
**Notes:** v2 preferred; fallback chain: sie_v2_valence_01 → sie_valence_01 → 0.0 (fum_rt/runtime/helpers/redis_out.py:13-14) <br/>

#### ADC Cycle Hits  <a id="kpi-adc-cycle-hits"></a>

**Symbol (if any):** $ \text{adc\_cycle\_hits} $ <br/>
**Purpose:** Active Domain Cartography cycle detection augmentation to complexity_cycles <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** ADC metrics from get_metrics() call <br/>
**Computation implemented at:** ADC subsystem, aggregated in telemetry: `fum_rt/runtime/telemetry.py:complexity_cycles += adc_cycle_hits • 17a0b72` <br/>
**Pass band / thresholds:** No explicit threshold; augments [Complexity Cycles](#kpi-complexity-cycles)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Runtime telemetry when ADC active <br/>
**Primary figure/artifact (if referenced):** N/A (internal augmentation to complexity_cycles) <br/>
**Notes:** When ADC inactive, adc_cycle_hits=0 → complexity_cycles unaugmented → b1_z flatlined (fum_rt/runtime/loop/main.py comment) <br/>

---

## Domain-Specific Metrics

### Graph Structure (Gravity Regression)

#### Degree Variance  <a id="kpi-degree-variance"></a>

**Symbol (if any):** $ \sigma^2_{\text{deg}} $ <br/>
**Purpose:** Detect ring-lattice topology via uniform degree distribution <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Graph edgelist → degree sequence <br/>
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72` (ring_lattice_suspicion) <br/>
**Pass band / thresholds:** `< 1.0` for ring-lattice suspicion (line 39)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Connectome graph structure validation <br/>
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json` <br/>
**Notes:** Part of ring-lattice detection heuristic with clustering and cycle count <br/>

#### Average Clustering Coefficient  <a id="kpi-avg-clustering"></a>

**Symbol (if any):** $ \bar{C} $ <br/>
**Purpose:** Measure local connectivity density in graph structure <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Graph adjacency structure <br/>
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72` <br/>
**Pass band / thresholds:** `< 0.2` for ring-lattice suspicion (line 39)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Connectome topology analysis <br/>
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json` <br/>
**Notes:** Low clustering indicates lattice-like structure; higher clustering indicates small-world/random <br/>

#### Degree Assortativity  <a id="kpi-degree-assortativity"></a>

**Symbol (if any):** $ r_{\text{deg}} $ <br/>
**Purpose:** Measure tendency of nodes to connect to similar-degree neighbors <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Graph edge structure and node degrees <br/>
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72` (nx.degree_assortativity_coefficient) <br/>
**Pass band / thresholds:** No explicit threshold; informational metric   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Graph structure characterization <br/>
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json` <br/>
**Notes:** Returns NaN gracefully if computation fails (line 35 exception handling) <br/>

#### Cycle Basis Count  <a id="kpi-cycle-basis-count"></a>

**Symbol (if any):** $ N_{\text{cycles}} $ <br/>
**Purpose:** Count fundamental cycles for ring-lattice detection <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Graph structure <br/>
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72` (nx.cycle_basis) <br/>
**Pass band / thresholds:** `≥ N * 0.8` for ring-lattice suspicion (line 39)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Connectome topology validation <br/>
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json` <br/>
**Notes:** High cycle count relative to node count indicates lattice structure <br/>

#### Ring Lattice Suspicion Flag  <a id="kpi-ring-lattice-suspicion"></a>

**Symbol (if any):** $ \text{ring\_lattice\_suspicion} $ <br/>
**Purpose:** Boolean flag for detecting degenerate ring-lattice topology <br/>
**Defined by:** TODO → add equation anchor - source: deg_var < 1.0 <br/>
**Inputs:** [Degree Variance](#kpi-degree-variance), [Average Clustering](#kpi-avg-clustering), [Cycle Basis Count](#kpi-cycle-basis-count) <br/>
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:39 • 17a0b72` <br/>
**Pass band / thresholds:** Boolean (true=suspect, false=ok)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Gravity regression connectome validation <br/>
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json` <br/>
**Notes:** Heuristic for catching pathological toy topologies <br/>

### Fluid Dynamics Announcers (Void Walkers)

#### Divergence Announcer Statistics  <a id="kpi-div-announce-stats"></a>

**Symbol (if any):** $ \text{div\_p50, div\_p90, div\_max} $ <br/>
**Purpose:** Passive diagnostics of incompressibility violations via walker-based sensors <br/>
**Defined by:** TODO → add equation anchor - source: p50, p90, max <br/>
**Inputs:** Velocity field (u_x, u_y) → local divergence at walker positions <br/>
**Computation implemented at:** `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:compute_void_walker_metrics • 17a0b72` <br/>
**Pass band / thresholds:** No enforcement; observe-only mode (default `walker_mode=observe`)   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Lid cavity with `--walker_announce --walkers 210` <br/>
**Primary figure/artifact (if referenced):** Logged in `metrics.void_announcers.announce_stats` JSON field <br/>
**Notes:** Part of void-faithful observability layer; non-interference verified by test_walkers_noninterference.py <br/>

#### Swirl Announcer Statistics  <a id="kpi-swirl-announce-stats"></a>

**Symbol (if any):** $ \text{swirl\_p50, swirl\_p90, swirl\_max} $ <br/>
**Purpose:** Monitor vorticity magnitude distribution via walker sensors <br/>
**Defined by:** TODO → add equation anchor - source: where ω = ∂u_y/∂x - ∂u_x/∂y <br/>
**Inputs:** Velocity field → vorticity at walker positions <br/>
**Computation implemented at:** `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:compute_void_walker_metrics • 17a0b72` <br/>
**Pass band / thresholds:** Advisory target `policy_swirl_target=5e-3` (default) for optional policy mode   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Same as Divergence Announcer <br/>
**Primary figure/artifact (if referenced):** Logged in `metrics.void_announcers.announce_stats` JSON field <br/>
**Notes:** Observe-only by default; advise/act modes apply bounded parameter updates (no forcing) <br/>

### Geometry Probe (Tool Metrics)

#### Activation Matrix Statistics  <a id="kpi-activation-matrix-stats"></a>

**Symbol (if any):** $ \text{mean, std, min, max} $ <br/>
**Purpose:** Validate captured activation matrices from model layer probes <br/>
**Defined by:** TODO → add equation anchor <br/>
**Inputs:** Activation matrix (concepts × features) from adapter.encode_concepts <br/>
**Computation implemented at:** `tools/geom_bundle_builder.py:_compute_stats • 17a0b72` <br/>
**Pass band / thresholds:** No explicit threshold; QC metadata for geometry bundles   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Geometry probe runs capturing layer activations at checkpoints <br/>
**Primary figure/artifact (if referenced):** Stored in `qc/{layer}_step-{step}_stats.json` <br/>
**Notes:** Part of bundle provenance and quality control artifacts <br/>

#### PCA Explained Variance Ratio  <a id="kpi-pca-explained-variance"></a>

**Symbol (if any):** $ \text{explained\_variance\_ratio} $ <br/>
**Purpose:** Dimensionality assessment of activation geometry <br/>
**Defined by:** TODO → add equation anchor - source: n_components=3 default <br/>
**Inputs:** Activation matrix → PCA decomposition <br/>
**Computation implemented at:** `tools/geom_bundle_builder.py:_compute_pca • 17a0b72` <br/>
**Pass band / thresholds:** No explicit threshold; informational for geometry analysis   • TODO → link to `CONSTANTS.md#const-...` <br/>
**Units / normalization:** `UNITS_NORMALIZATION.md` <br/>
**Typical datasets / experiments:** Same as Activation Matrix Statistics <br/>
**Primary figure/artifact (if referenced):** Stored in `qc/{layer}_step-{step}_pca.json` <br/>
**Notes:** Includes principal component vectors for downstream geometry probes <br/>

---

<!-- BEGIN AUTOSECTION: METRICS-INDEX -->
- [Activation Matrix Statistics](#kpi-activation-matrix-stats)
- [Active Synapses](#kpi-active-synapses)
- [ADC Cycle Hits](#kpi-adc-cycle-hits)
- [Average Clustering Coefficient](#kpi-avg-clustering)
- [Average Weight](#kpi-avg-weight)
- [B1 Spike Detection (z-score)](#kpi-b1-spike-z)
- [CFL Condition](#kpi-cfl-condition)
- [Cohesion Components](#kpi-cohesion-components)
- [Complexity Cycles](#kpi-complexity-cycles)
- [Connectome Entropy](#kpi-connectome-entropy)
- [Convergence Slope (dt)](#kpi-convergence-slope-dt)
- [Cycle Basis Count](#kpi-cycle-basis-count)
- [Degree Assortativity](#kpi-degree-assortativity)
- [Degree Variance](#kpi-degree-variance)
- [Dispersion Median Relative Error](#kpi-dispersion-med-rel-err)
- [Divergence Announcer Statistics](#kpi-div-announce-stats)
- [Drift Gate (Conservation Law)](#kpi-drift-gate)
- [Front Speed Relative Error](#kpi-front-speed-rel-err)
- [Lid Cavity Divergence Maximum](#kpi-lid-cavity-div-max)
- [Memory Steering Canonical Void Target](#kpi-memory-void-target)
- [Memory Steering Pole Fit Error](#kpi-memory-pole-fit-err)
- [Memory Steering SNR Improvement](#kpi-memory-snr-improvement)
- [PCA Explained Variance Ratio](#kpi-pca-explained-variance)
- [Q-Invariant Maximum Drift](#kpi-q-invariant-drift)
- [Ring Lattice Suspicion Flag](#kpi-ring-lattice-suspicion)
- [R² Dispersion Array Fit](#kpi-r2-dispersion-array)
- [R² Front Position Fit](#kpi-r2-front-fit)
- [SIE Valence](#kpi-sie-valence)
- [Swirl Announcer Statistics](#kpi-swirl-announce-stats)
- [Taylor-Green Viscosity Recovery Error](#kpi-taylor-green-nu-rel-err)
- [Void Traveler Coverage](#kpi-vt-coverage)
- [Void Traveler Entropy](#kpi-vt-entropy)
- [ΛCDM Residual (w+1)](#kpi-lcdm-residual)
- [FRW Continuity RMS Residual](#kpi-frw-continuity-rms)
- [A6 Collapse Max Envelope](#kpi-a6-envelope-max)
- [Regime Split Annotation Present](#kpi-dp-regime-split)
- [Fisher Consistency (Finite‑Difference Cross‑Check)](#kpi-dp-fisher-consistency)
<!-- END AUTOSECTION: METRICS-INDEX -->

## Change Log

- 2025-10-03 • Initial compilation from repository code and tests • 17a0b72
- 2025-10-04 • Add tachyonic tube KPIs: cov_phys, cov_raw, residual, curvature_ok and finite_fraction
