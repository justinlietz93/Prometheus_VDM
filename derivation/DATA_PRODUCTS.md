<!-- DOC-GUARD: CANONICAL -->
<!-- markdownlint-disable MD033 MD022 MD032 MD001 -->
# VDM Data Products (Auto-compiled)

**Scope:** Single source of truth for data products used/produced by this repository: purpose, shape, units, storage format, file paths, and provenance.  
**Rules:** Reference-only for math; link to anchors in EQUATIONS/CONSTANTS/SYMBOLS/UNITS/ALGORITHMS.  
**MathJax:** GitHub-safe `$...$`/`$$...$$` only when quoting existing math.

---

## Core Field & Activity Maps

#### flux_sweep results  <a id="data-flux-sweep"></a>
**Type:** log  
**Purpose:** Conservation law validation data from discrete flux computation experiments  
**Produced by:** TODO: add anchor (see derivation/code/analysis/flux_sweep.py)  
**Defined by (if math):** TODO: add anchor for deltaQ conservation  
**Inputs (symbols/constants):** TODO: link r, u, N, k parameters  
**Units/Normalization:** dimensionless (discrete indices, normalized states)

**Shape & axes (exact as used):**
- Shape: JSON object with metadata + results array
- Fields: `timestamp`, `N`, `k`, `trials`, `r`, `u`, `results[]`
- Results entry: `seed`, `delta_sum_Q`, `delta_max_abs`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/outputs/logs/conservation_law/flux_sweep_<timestamp>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `timestamp:int`, `N:int`, `k:int`, `trials:int`, `r:float`, `u:float`, `results:array`
- Index/primary keys: timestamp

**Update cadence / lifecycle:** `on event`  
**Provenance (code locations):** `derivation/code/analysis/flux_sweep.py:75-157 • 800ceda`  
**Validation hooks / KPIs:** residual metrics (delta_sum_Q, delta_max_abs)  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/outputs/logs/conservation_law/flux_sweep_1756475408.json`  
**Notes:** Used as input for H_candidate validation and optimization

---

#### H_candidate_test results  <a id="data-h-candidate-test"></a>
**Type:** log  
**Purpose:** Test results for conservation law H_candidate function corrections  
**Produced by:** TODO: add anchor (see derivation/code/analysis/build_and_test_H_candidate.py)  
**Defined by (if math):** TODO: add anchor for H_ij symbolic form  
**Inputs (symbols/constants):** flux_sweep data, symbolic coefficients  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `timestamp`, `sweep_file`, `rms_before`, `rms_after`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/outputs/logs/conservation_law/H_candidate_test_<timestamp>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `timestamp:int`, `sweep_file:str`, `rms_before:float`, `rms_after:float`
- Index/primary keys: timestamp

**Update cadence / lifecycle:** `on event`  
**Provenance (code locations):** `derivation/code/analysis/build_and_test_H_candidate.py:127-157 • 800ceda`  
**Validation hooks / KPIs:** rms_before vs rms_after comparison  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/outputs/logs/conservation_law/H_candidate_test_1756476845.json`  
**Notes:** Tests symbolic H function against numerical flux data

---

#### opt_H_params results  <a id="data-opt-h-params"></a>
**Type:** log  
**Purpose:** Optimization results for free parameters in H_candidate function  
**Produced by:** TODO: add anchor (see derivation/code/analysis/optimize_H_params.py)  
**Defined by (if math):** TODO: add anchor for tau0 parameter  
**Inputs (symbols/constants):** flux_sweep data, H symbolic form  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `timestamp`, `sweep_file`, `free_symbols[]`, `initial_params[]`, `best_params[]`, `rms_before`, `rms_after`, `optimizer_result`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/outputs/logs/conservation_law/opt_H_params_<timestamp>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `timestamp:int`, `sweep_file:str`, `free_symbols:array`, `initial_params:array`, `best_params:array`, `rms_before:float`, `rms_after:float`, `optimizer_result:dict`
- Index/primary keys: timestamp

**Update cadence / lifecycle:** `on event`  
**Provenance (code locations):** `derivation/code/analysis/optimize_H_params.py • 800ceda`  
**Validation hooks / KPIs:** optimizer success, RMS improvement  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/outputs/logs/conservation_law/opt_H_params_1756477394.json`  
**Notes:** Scipy optimizer results for free symbolic parameters

---

#### fit_H_edge results  <a id="data-fit-h-edge"></a>
**Type:** log  
**Purpose:** Edge-based ansatz fit results for H function approximation  
**Produced by:** TODO: add anchor (see derivation/code/analysis/fit_H_edge.py)  
**Defined by (if math):** TODO: add anchor for edge ansatz basis  
**Inputs (symbols/constants):** flux_sweep data  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `timestamp`, `sweep_file`, `basis[]`, `coefficients[]`, `rms_residual`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/outputs/logs/conservation_law/fit_H_edge_<timestamp>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `timestamp:int`, `sweep_file:str`, `basis:array`, `coefficients:array`, `rms_residual:float`
- Index/primary keys: timestamp

**Update cadence / lifecycle:** `on event`  
**Provenance (code locations):** `derivation/code/analysis/fit_H_edge.py • 800ceda`  
**Validation hooks / KPIs:** rms_residual threshold  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/outputs/logs/conservation_law/fit_H_edge_1756476036.json`  
**Notes:** Least-squares fit using polynomial edge basis

---

#### grid_tau0_report  <a id="data-grid-tau0"></a>
**Type:** log  
**Purpose:** Grid search results for tau0 parameter in conservation law  
**Produced by:** TODO: add anchor (see derivation/code/analysis/grid_tau0.py)  
**Defined by (if math):** TODO: add anchor for tau0  
**Inputs (symbols/constants):** flux data  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: grid search results over tau0 range

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/outputs/logs/conservation_law/grid_tau0_report.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: varies (grid search results)
- Index/primary keys: none

**Update cadence / lifecycle:** `on event`  
**Provenance (code locations):** `derivation/code/analysis/grid_tau0.py • 800ceda`  
**Validation hooks / KPIs:** optimal tau0 identification  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/outputs/logs/conservation_law/grid_tau0_report.json`  
**Notes:** Systematic parameter sweep

---

#### qfum_metrics  <a id="data-qfum-metrics"></a>
**Type:** log  
**Purpose:** Quantum FUM conservation validation metrics including Q-drift and convergence  
**Produced by:** TODO: add anchor (see derivation/code/physics/conservation_law/qfum_validate.py)  
**Defined by (if math):** TODO: add anchor for Q conservation equation  
**Inputs (symbols/constants):** discrete walker states, network topology  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object with metrics, params, and series data
- Fields: `timestamp`, `params`, `metrics`, `passes`, `figures`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/conservation_law/<YYYYMMDD_HHMMSS>_qfum_metrics.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `timestamp:str`, `params:dict`, `metrics:dict`, `passes:dict`
- Index/primary keys: timestamp

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/conservation_law/qfum_validate.py • 800ceda`  
**Validation hooks / KPIs:** Q-drift threshold, convergence criteria  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/conservation_law/20250826_110546_qfum_metrics.json`  
**Notes:** Includes failed_runs subdirectory for non-passing experiments

---

#### frw_conservation_check  <a id="data-frw-conservation"></a>
**Type:** table  
**Purpose:** FRW cosmology conservation check timeseries data  
**Produced by:** TODO: add anchor (see derivation/code/physics/conservation_law/qfum_validate.py)  
**Defined by (if math):** TODO: add anchor for FRW conservation law  
**Inputs (symbols/constants):** cosmological parameters  
**Units/Normalization:** TODO: link to UNITS_NORMALIZATION.md

**Shape & axes (exact as used):**
- Shape: CSV table with timeseries
- Columns: varies (conservation check fields)

**Storage format & path pattern:**
- Format: `csv`
- Path pattern: `derivation/code/outputs/logs/conservation_law/frw_conservation_check.csv`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: timeseries data (exact schema TBD)
- Index/primary keys: time index

**Update cadence / lifecycle:** `per tick`  
**Provenance (code locations):** `derivation/code/physics/conservation_law/qfum_validate.py • 800ceda`  
**Validation hooks / KPIs:** conservation residual thresholds  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/conservation_law/frw_conservation_check.csv`  
**Notes:** CSV format for easy plotting and analysis

---

#### frw_continuity_residual log  <a id="data-frw-balance-log"></a>
**Type:** log  
**Purpose:** Gate record for FRW continuity residual check with pass/fail, RMS, and artifact pointers  
**Produced by:** `derivation/code/physics/cosmology/run_frw_balance.py:run_frw_balance`  
**Defined by (if math):** `EQUATIONS.md#vdm-e-0xx` (FRW continuity; dust baseline $w=0$)  
**Inputs (symbols/constants):** $\rho(t)$, $a(t)$, $t$  
**Units/Normalization:** `UNITS_NORMALIZATION.md#cosmology` (dimensionless baseline OK; relative gate)

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `tol_rms:float`, `rms:float`, `passed:bool`, `figure:str`, `csv:str`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/cosmology/frw_balance__<tag>.json` (failed runs routed to `.../failed_runs/`)
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `tol_rms:float`, `rms:float`, `passed:bool`, `figure:str`, `csv:str`
- Index/primary keys: none (singleton per run)

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/cosmology/run_frw_balance.py:57-91`  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-frw-continuity-rms`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/metriplectic/frw_balance__FRW-balance-v1.json`  
**Notes:** CONTRADICTION_REPORT is emitted on gate failure and routed to `failed_runs/`.

---

#### frw_continuity_residual series  <a id="data-frw-balance-series"></a>
**Type:** table  
**Purpose:** Per-timestep residual series for FRW continuity equation used to compute RMS gate  
**Produced by:** `derivation/code/physics/cosmology/run_frw_balance.py:run_frw_balance`  
**Defined by (if math):** `EQUATIONS.md#vdm-e-0xx` (FRW continuity)  
**Inputs (symbols/constants):** $\rho(t)$, $a(t)$, $t$  
**Units/Normalization:** `UNITS_NORMALIZATION.md#cosmology`

**Shape & axes (exact as used):**
- Shape: CSV table with timeseries
- Columns: `t`, `rho`, `a`, `residual`

**Storage format & path pattern:**
- Format: `csv`
- Path pattern: `derivation/code/outputs/logs/cosmology/frw_continuity_residual__<tag>.csv` (failed → `.../failed_runs/`)
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `t:float`, `rho:float`, `a:float`, `residual:float`
- Index/primary keys: `t`

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/cosmology/run_frw_balance.py:73-81`  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-frw-continuity-rms`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/metriplectic/frw_continuity_residual__FRW-balance-v1.csv`  
**Notes:** Central-difference gradient for interior points; one-sided at boundaries.

---

#### frw_continuity_residual figure  <a id="data-frw-balance-figure"></a>
**Type:** image  
**Purpose:** Visualization of FRW continuity residual vs time with RMS shown in title  
**Produced by:** `derivation/code/physics/cosmology/run_frw_balance.py:run_frw_balance`  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** FRW residual series  
**Units/Normalization:** axis labels included

**Shape & axes (exact as used):**
- Shape: raster image
- Dimensions: ~150 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/cosmology/frw_continuity_residual__<tag>.png` (failed → `.../failed_runs/`)
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/cosmology/run_frw_balance.py:62-71`  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-frw-continuity-rms`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/figures/metriplectic/frw_continuity_residual__FRW-balance-v1.png`  
**Notes:** Title includes RMS value; horizontal zero-line drawn for reference.

---

## Diagnostics & Logs

#### rd_dispersion_experiment results  <a id="data-rd-dispersion"></a>
**Type:** log  
**Purpose:** Reaction-diffusion dispersion relation validation experiment results  
**Produced by:** TODO: add anchor (see derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py)  
**Defined by (if math):** TODO: add anchor for dispersion relation $\sigma(k)$  
**Inputs (symbols/constants):** TODO: link D, r, N, L parameters  
**Units/Normalization:** TODO: link to UNITS_NORMALIZATION.md

**Shape & axes (exact as used):**
- Shape: JSON object with theory, params, metrics, series
- Fields: `theory`, `params`, `metrics`, `series`, `outputs`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/reaction_diffusion/rd_dispersion_experiment_<YYYYMMDDTHHMMSSZ>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `theory:dict`, `params:dict`, `metrics:dict`, `series:dict`, `outputs:dict`
- Index/primary keys: timestamp in filename

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py • 800ceda` ; `fum_rt/physics/rd_dispersion_runner.py • 800ceda`  
**Validation hooks / KPIs:** `med_rel_err_max`, `r2_array_min` acceptance criteria  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/reaction_diffusion/rd_dispersion_experiment_20250823T182316Z.json` ; `fum_rt/physics/outputs/logs/rd_dispersion_runner_20250820T114106Z.json`  
**Notes:** Includes failed_runs subdirectory; dual locations (derivation/code and fum_rt/physics)

---

#### rd_front_speed_experiment results  <a id="data-rd-front-speed"></a>
**Type:** log  
**Purpose:** Reaction-diffusion traveling wave front speed validation experiment results  
**Produced by:** TODO: add anchor (see derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py)  
**Defined by (if math):** TODO: add anchor for front speed equation  
**Inputs (symbols/constants):** TODO: link D, r parameters  
**Units/Normalization:** TODO: link to UNITS_NORMALIZATION.md

**Shape & axes (exact as used):**
- Shape: JSON object with theory, params, metrics
- Fields: `theory`, `params`, `metrics`, `outputs`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_<YYYYMMDDTHHMMSSZ>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `theory:dict`, `params:dict`, `metrics:dict`, `outputs:dict`
- Index/primary keys: timestamp in filename

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py • 800ceda` ; `fum_rt/physics/rd_front_speed_runner.py • 800ceda`  
**Validation hooks / KPIs:** front speed accuracy thresholds  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_20250823T194825Z.json` ; `fum_rt/physics/outputs/logs/rd_front_speed_runner_20250820T114104Z.json`  
**Notes:** Includes failed_runs subdirectory; dual locations (derivation/code and fum_rt/physics)

---

#### taylor_green_benchmark results  <a id="data-taylor-green"></a>
**Type:** log  
**Purpose:** Taylor-Green vortex benchmark for fluid dynamics validation  
**Produced by:** TODO: add anchor (see derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py)  
**Defined by (if math):** TODO: add anchor for Taylor-Green flow equations  
**Inputs (symbols/constants):** TODO: link viscosity, grid parameters  
**Units/Normalization:** TODO: link to UNITS_NORMALIZATION.md

**Shape & axes (exact as used):**
- Shape: JSON object with params, metrics
- Fields: `params`, `metrics`, `outputs`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/fluid_dynamics/taylor_green_benchmark_<YYYYMMDDTHHMMSSZ>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `params:dict`, `metrics:dict`, `outputs:dict`
- Index/primary keys: timestamp in filename

**Update cadence / lifecycle:** `per benchmark run`  
**Provenance (code locations):** `derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py • 800ceda`  
**Validation hooks / KPIs:** energy decay rate accuracy  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified)  
**Notes:** Includes failed_runs subdirectory

---

#### lid_cavity_benchmark results  <a id="data-lid-cavity"></a>
**Type:** log  
**Purpose:** Lid-driven cavity benchmark for fluid dynamics validation  
**Produced by:** TODO: add anchor (see derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py)  
**Defined by (if math):** TODO: add anchor for cavity flow equations  
**Inputs (symbols/constants):** TODO: link Reynolds number, grid parameters  
**Units/Normalization:** TODO: link to UNITS_NORMALIZATION.md

**Shape & axes (exact as used):**
- Shape: JSON object with params, metrics
- Fields: `params`, `metrics`, `outputs`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/fluid_dynamics/lid_cavity_benchmark_<YYYYMMDDTHHMMSSZ>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `params:dict`, `metrics:dict`, `outputs:dict`
- Index/primary keys: timestamp in filename

**Update cadence / lifecycle:** `per benchmark run`  
**Provenance (code locations):** `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py • 800ceda`  
**Validation hooks / KPIs:** vortex center position accuracy  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified)  
**Notes:** Includes failed_runs subdirectory

---

#### memory_steering stability metrics  <a id="data-memory-steering-metrics"></a>
**Type:** log  
**Purpose:** Memory steering stability analysis metrics and acceptance test results  
**Produced by:** TODO: add anchor (see derivation/code/physics/memory_steering/memory_steering_acceptance.py)  
**Defined by (if math):** TODO: add anchor for memory steering equations  
**Inputs (symbols/constants):** TODO: link gamma parameter  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object with metrics and acceptance results
- Fields: `metrics`, `acceptance`, `passes`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/memory_steering/memory_steering_acceptance_<timestamp>.json` (inferred)
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `metrics:dict`, `acceptance:dict`, `passes:dict`
- Index/primary keys: timestamp

**Update cadence / lifecycle:** `per acceptance test run`  
**Provenance (code locations):** `derivation/code/physics/memory_steering/memory_steering_acceptance.py • 800ceda` ; `derivation/code/physics/memory_steering/plot_memory_steering.py • 800ceda`  
**Validation hooks / KPIs:** TODO: link to VALIDATION_METRICS.md  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified)  
**Notes:** Produces associated PNG figures for stability analysis

---

#### agency options probe results  <a id="data-options-probe"></a>
**Type:** table  
**Purpose:** Agency field options probe simulation results for reachability analysis  
**Produced by:** TODO: add anchor (see derivation/code/physics/agency/simulate_options_probe.py)  
**Defined by (if math):** TODO: add anchor for option value equations  
**Inputs (symbols/constants):** actuators, budget, slip, grid parameters  
**Units/Normalization:** information-theoretic (bits)

**Shape & axes (exact as used):**
- Shape: CSV table
- Columns: `actuators`, `budget`, `slip`, `grid_n`, `obstacles`, `reachable`, `useful`, `V_bits`, `V_useful_bits`

**Storage format & path pattern:**
- Format: `csv`
- Path pattern: `derivation/code/outputs/logs/agency/options.csv`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `actuators:int`, `budget:int`, `slip:float`, `grid_n:int`, `obstacles:float`, `reachable:int`, `useful:int`, `V_bits:float`, `V_useful_bits:float`
- Index/primary keys: composite (actuators, budget, slip)

**Update cadence / lifecycle:** `per sweep`  
**Provenance (code locations):** `derivation/code/physics/agency/simulate_options_probe.py • 800ceda`  
**Validation hooks / KPIs:** reachability metrics, information capacity  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/agency/options.csv`  
**Notes:** Produces associated options_heatmap.png visualization

---

#### vacuum_demographics results  <a id="data-vacuum-demographics"></a>
**Type:** log  
**Purpose:** Vacuum demographics harness output for cosmology router vacuum channel validation  
**Produced by:** TODO: add anchor (see fum_rt/physics/vacuum_demographics_harness.py)  
**Defined by (if math):** TODO: add anchor for w(z) equation of state  
**Inputs (symbols/constants):** TODO: link eta, epsilon, rho_lambda parameters  
**Units/Normalization:** TODO: link to UNITS_NORMALIZATION.md (Myr, redshift)

**Shape & axes (exact as used):**
- Shape: JSON object with config, timeline, metrics
- Fields: `config`, `timeline[]`, `metrics`, `timestamp`, `outputs`, `gates`, `seeds`, `hashes`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `fum_rt/physics/outputs/logs/vacuum_demographics_harness_<YYYYMMDDTHHMMSSZ>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `config:dict`, `timeline:array[{t_myr, redshift, rho_vac, w_residual}]`, `metrics:dict`
- Index/primary keys: timestamp in filename

**Update cadence / lifecycle:** `per harness run`  
**Provenance (code locations):** `fum_rt/physics/vacuum_demographics_harness.py:274-319 • 800ceda`  
**Validation hooks / KPIs:** `lcdm_residual_within_tol` gate  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Includes horizon activity tape with synthetic or user-supplied BH events

---

## Figures & Media

#### conservation_law diagnostic figures  <a id="data-conservation-figures"></a>
**Type:** image  
**Purpose:** Diagnostic plots for conservation law validation (convergence, Q-drift, solution overlay)  
**Produced by:** TODO: add anchor (see derivation/code/physics/conservation_law/qfum_validate.py)  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** qfum_metrics data  
**Units/Normalization:** N/A (plot axes labeled)

**Shape & axes (exact as used):**
- Shape: raster images
- Dimensions: varies (typically ~150-180 DPI)

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/conservation_law/<YYYYMMDD_HHMMSS>_qfum_{convergence|Q_drift|solution_overlay}.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/conservation_law/qfum_validate.py • 800ceda`  
**Validation hooks / KPIs:** visual inspection  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/figures/conservation_law/20250826_110546_qfum_convergence.png`  
**Notes:** Includes failed_runs subdirectory; also frw_conservation_residual.png

---

#### dark_photon noise budget plots  <a id="data-dp-noise-figures"></a>
**Type:** image  
**Purpose:** SNR vs integration time/ bandwidth plots with annotated regime split (quantum- vs thermal-limited)  
**Produced by:** TODO: add anchor (see `derivation/code/physics/dark_photons/noise_budget.py`)  
**Defined by (if math):** `EQUATIONS.md#vdm-e-dp-noise` (noise PSD models; quantum vs thermal)  
**Inputs (symbols/constants):** detector noise PSDs, bandwidth, integration time grid, mixing $\varepsilon$ (if applicable)  
**Units/Normalization:** `UNITS_NORMALIZATION.md#detector`

**Shape & axes (exact as used):**
- Shape: raster images, 150–180 DPI
- Plots: `SNR(t_int)` and/or `SNR(B)` with regime annotations

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/dark_photons/noise_budget__<tag>.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per analysis run`  
**Provenance (code locations):** TODO (planned)  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-dp-regime-split`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern established)  
**Notes:** Plot should label regime boundary $t_*$/bandwidth crossover and slopes.

---

#### reaction_diffusion diagnostic figures  <a id="data-rd-figures"></a>
**Type:** image  
**Purpose:** Reaction-diffusion dispersion and front speed validation plots  
**Produced by:** TODO: add anchor (see derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py, rd_front_speed_experiment.py)  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** experiment results data  
**Units/Normalization:** N/A (plot axes labeled)

**Shape & axes (exact as used):**
- Shape: raster images
- Dimensions: 150 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/reaction_diffusion/rd_{dispersion|front_speed}_experiment_<YYYYMMDDTHHMMSSZ>.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py • 800ceda` ; `derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py • 800ceda` ; `fum_rt/physics/rd_dispersion_runner.py • 800ceda` ; `fum_rt/physics/rd_front_speed_runner.py • 800ceda`  
**Validation hooks / KPIs:** visual inspection of fit quality  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.png`  
**Notes:** Includes failed_runs subdirectory; dual locations (derivation/code and fum_rt/physics)

---

#### a6_collapse log  <a id="data-a6-collapse-log"></a>
**Type:** log  
**Purpose:** Gate record for A6 scaling collapse (max envelope) with pass/fail and artifact pointers  
**Produced by:** `derivation/code/physics/collapse/run_a6_collapse.py:run_a6`  
**Defined by (if math):** `EQUATIONS.md#vdm-e-a6-collapse` (junction logistic collapse; reference-only)  
**Inputs (symbols/constants):** $\Theta$, $\Delta m$ grid, trials per point  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `spec`, `passed`, `env_max`, `figure`, `csv`, `raw_curves`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/collapse/a6_collapse__<tag>.json` (failed → `.../failed_runs/`)
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `spec:dict`, `passed:bool`, `env_max:float`, `figure:str`, `csv:str`, `raw_curves:list`

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/collapse/run_a6_collapse.py:61-108`  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-a6-envelope-max`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/collapse/a6_collapse__A6-collapse-v1.json`  
**Notes:** CONTRADICTION_REPORT emitted on failure with gate and artifact pointers.

---

#### a6_collapse envelope series  <a id="data-a6-collapse-series"></a>
**Type:** table  
**Purpose:** Per-bin envelope series for A6 collapse; used to compute max envelope gate  
**Produced by:** `derivation/code/physics/collapse/run_a6_collapse.py:run_a6`  
**Defined by (if math):** `EQUATIONS.md#vdm-e-a6-collapse`  
**Inputs (symbols/constants):** $X$, $Y_{\min}$, $Y_{\max}$  
**Units/Normalization:** dimensionless

**Shape & axes (exact as used):**
- Shape: CSV table
- Columns: `X, Ymin, Ymax, envelope`

**Storage format & path pattern:**
- Format: `csv`
- Path pattern: `derivation/code/outputs/logs/collapse/a6_collapse_envelope__<tag>.csv` (failed → `.../failed_runs/`)
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `X:float`, `Ymin:float`, `Ymax:float`, `envelope:float`
- Index/primary keys: `X`

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/collapse/run_a6_collapse.py:94-101`  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-a6-envelope-max`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/logs/collapse/a6_collapse_envelope__A6-collapse-v1.csv`  
**Notes:** Envelope computed after interpolating all curves onto shared X grid.

---

#### a6_collapse overlay figure  <a id="data-a6-collapse-figure"></a>
**Type:** image  
**Purpose:** Overlay of collapsed curves with envelope fill and max‑envelope in title  
**Produced by:** `derivation/code/physics/collapse/run_a6_collapse.py:run_a6`  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** A6 collapse curves and envelope  
**Units/Normalization:** axis labels included

**Shape & axes (exact as used):**
- Shape: raster image
- Dimensions: ~150 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/collapse/a6_collapse_overlay__<tag>.png` (failed → `.../failed_runs/`)
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per experiment run`  
**Provenance (code locations):** `derivation/code/physics/collapse/run_a6_collapse.py:79-92`  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-a6-envelope-max`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/figures/collapse/a6_collapse_overlay__A6-collapse-v1.png`  
**Notes:** Curves plotted with markers; fill_between shows envelope band.

---

#### fluid_dynamics diagnostic figures  <a id="data-fluid-figures"></a>
**Type:** image  
**Purpose:** Fluid dynamics benchmark validation plots (Taylor-Green, lid cavity)  
**Produced by:** TODO: add anchor (see derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py, lid_cavity_benchmark.py)  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** benchmark results data  
**Units/Normalization:** N/A (plot axes labeled)

**Shape & axes (exact as used):**
- Shape: raster images
- Dimensions: 140-180 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/fluid_dynamics/{taylor_green|lid_cavity}_benchmark_<YYYYMMDDTHHMMSSZ>.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per benchmark run`  
**Provenance (code locations):** `derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py • 800ceda` ; `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py • 800ceda`  
**Validation hooks / KPIs:** visual inspection  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/figures/fluid_dynamics/lid_cavity_benchmark_20250821T072638Z.png` ; `derivation/code/outputs/figures/fluid_dynamics/lid_cavity_benchmark_20250821T072638Z_vorticity.png`  
**Notes:** Includes failed_runs subdirectory; cavity produces both standard and vorticity plots

---

#### memory_steering diagnostic figures  <a id="data-memory-figures"></a>
**Type:** image  
**Purpose:** Memory steering stability analysis plots (SNR, retention, AUC, fidelity, curvature, band, junction)  
**Produced by:** TODO: add anchor (see derivation/code/physics/memory_steering/plot_memory_steering.py)  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** memory steering experiment data  
**Units/Normalization:** N/A (plot axes labeled)

**Shape & axes (exact as used):**
- Shape: raster images
- Dimensions: 160 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/memory_steering/{stability_snr_by_gamma|stability_retention_by_gamma|stability_auc_by_gamma|stability_fidelity_by_gamma|curvature_scaling|curvature_scaling_signed|stability_band|curvature_calibration|junction_logistic|memory_steering_summary}.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per analysis run`  
**Provenance (code locations):** `derivation/code/physics/memory_steering/plot_memory_steering.py • 800ceda`  
**Validation hooks / KPIs:** visual inspection of stability metrics  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/figures/memory_steering/stability_snr_by_gamma.png`  
**Notes:** Comprehensive suite of stability metric visualizations

---

#### agency options heatmap  <a id="data-options-heatmap"></a>
**Type:** image  
**Purpose:** Heatmap visualization of agency options probe results  
**Produced by:** TODO: add anchor (see derivation/code/physics/agency/simulate_options_probe.py)  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** options.csv data  
**Units/Normalization:** N/A (plot axes labeled)

**Shape & axes (exact as used):**
- Shape: raster image
- Dimensions: 140 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/agency/options_heatmap.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per probe run`  
**Provenance (code locations):** `derivation/code/physics/agency/simulate_options_probe.py • 800ceda`  
**Validation hooks / KPIs:** visual inspection  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/code/outputs/figures/agency/options_heatmap.png`  
**Notes:** Visualizes reachability vs budget/slip parameter space

---

#### vacuum_demographics residual plot  <a id="data-vacuum-figure"></a>
**Type:** image  
**Purpose:** w(z)+1 residual plot for vacuum demographics validation  
**Produced by:** TODO: add anchor (see fum_rt/physics/vacuum_demographics_harness.py)  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** vacuum demographics timeline data  
**Units/Normalization:** N/A (redshift vs residual)

**Shape & axes (exact as used):**
- Shape: raster image
- Dimensions: 150 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `fum_rt/physics/outputs/figures/vacuum_demographics_harness_<YYYYMMDDTHHMMSSZ>.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per harness run`  
**Provenance (code locations):** `fum_rt/physics/vacuum_demographics_harness.py:245-271 • 800ceda`  
**Validation hooks / KPIs:** residual within tolerance  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Shows deviations from ΛCDM baseline (w=-1)

---

## Geometry & Activation Captures

#### activation matrices  <a id="data-activation-matrices"></a>
**Type:** array  
**Purpose:** Concept activation vectors captured from model layers during geometry probing  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** N/A (raw activations)  
**Inputs (symbols/constants):** model checkpoints, concept list, layer names  
**Units/Normalization:** model-dependent (typically normalized or float32)

**Shape & axes (exact as used):**
- Shape: `(n_concepts, n_neurons)` per layer per step
- Axes: concepts (rows) × neurons (columns)

**Storage format & path pattern:**
- Format: `npy`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/acts/<layer>/acts_step-<step>.npy`
- Compression/encoding: NumPy native (uncompressed float32)

**Schema / columns (for tables/logs):**
- N/A (binary array data)

**Update cadence / lifecycle:** `per step per layer`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:308-360 • 800ceda`  
**Validation hooks / KPIs:** matrix shape validation, neuron count ≥ 64  
**Retention / access constraints:** bundle size limit (configurable, default 1500 MB)  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Accompanied by meta_step-<step>.json with capture metadata

---

#### activation capture metadata  <a id="data-activation-meta"></a>
**Type:** log  
**Purpose:** Per-layer per-step metadata for activation captures (shape, dtype, timing)  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** N/A (metadata)  
**Inputs (symbols/constants):** activation capture process  
**Units/Normalization:** seconds (timing), count (neurons)

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `layer`, `step`, `concepts[]`, `neurons`, `notes`, `dtype`, `shape[]`, `capture_seconds`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/acts/<layer>/meta_step-<step>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `layer:str`, `step:int`, `concepts:array`, `neurons:int`, `notes:str`, `dtype:str`, `shape:array`, `capture_seconds:float`
- Index/primary keys: (layer, step)

**Update cadence / lifecycle:** `per step per layer`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:330-340 • 800ceda`  
**Validation hooks / KPIs:** N/A (metadata)  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Canonical probe mode is "eval_no_dropout"

---

#### QC statistics  <a id="data-qc-stats"></a>
**Type:** log  
**Purpose:** Quality control statistics for activation matrices (mean, std, sparsity, top variance)  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** N/A (statistics)  
**Inputs (symbols/constants):** activation matrices  
**Units/Normalization:** activation space units

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `mean[]`, `std[]`, `near_zero_fraction`, `top_variance_indices[]`, `top_variance_values[]`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/qc/<layer>_step-<step>_stats.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `mean:array`, `std:array`, `near_zero_fraction:float`, `top_variance_indices:array`, `top_variance_values:array`
- Index/primary keys: (layer, step)

**Update cadence / lifecycle:** `per step per layer`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:244-257, 341-342 • 800ceda`  
**Validation hooks / KPIs:** sparsity thresholds, variance distribution  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Per-neuron statistics across concept dimension

---

#### PCA decomposition  <a id="data-pca"></a>
**Type:** log  
**Purpose:** Principal component analysis of activation matrices for dimensionality reduction  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** TODO: add anchor for PCA/SVD  
**Inputs (symbols/constants):** activation matrices  
**Units/Normalization:** normalized (whitened)

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `components[][]`, `explained_variance_ratio[]`, `total_variance`, `sanity_alignment`, `alt_singular_values[]`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/qc/<layer>_step-<step>_pca.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `components:array2d`, `explained_variance_ratio:array`, `total_variance:float`, `sanity_alignment:float`, `alt_singular_values:array`
- Index/primary keys: (layer, step)

**Update cadence / lifecycle:** `per step per layer`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:260-276, 343-344 • 800ceda`  
**Validation hooks / KPIs:** variance explained thresholds  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Default 3 components; includes sanity alignment metric

---

#### PCA thumbnails  <a id="data-pca-thumbs"></a>
**Type:** image  
**Purpose:** Quick visual inspection plots of PC1 vs PC2 for activation matrices  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** N/A (visualization)  
**Inputs (symbols/constants):** activation matrices  
**Units/Normalization:** principal component space

**Shape & axes (exact as used):**
- Shape: raster images (4×4 inches)
- Dimensions: varies

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/thumbs/<layer>/pca2_step-<step>.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `per step per layer (if create_thumbs=true)`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:279-299, 346-347 • 800ceda`  
**Validation hooks / KPIs:** visual inspection  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Optional; controlled by create_thumbs config flag

---

#### geometry bundle index  <a id="data-geom-index"></a>
**Type:** log  
**Purpose:** JSONL index of all activation captures in a geometry bundle run  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** N/A (index)  
**Inputs (symbols/constants):** all captures in run  
**Units/Normalization:** N/A

**Shape & axes (exact as used):**
- Shape: JSONL (one entry per layer-step pair)
- Fields per line: `layer`, `step`, `acts_path`, `meta_path`, `stats_path`, `pca_path`, `thumb_path`, `shape[]`

**Storage format & path pattern:**
- Format: `jsonl`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/index.jsonl`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `layer:str`, `step:int`, `acts_path:str`, `meta_path:str`, `stats_path:str`, `pca_path:str`, `thumb_path:str|null`, `shape:array`
- Index/primary keys: (layer, step)

**Update cadence / lifecycle:** `per step per layer (append)`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:302-360 • 800ceda`  
**Validation hooks / KPIs:** N/A (index)  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Enables fast lookup without scanning directory tree

---

#### geometry bundle provenance  <a id="data-geom-provenance"></a>
**Type:** log  
**Purpose:** Reproducibility metadata for geometry bundle runs (git, environment, hardware)  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** N/A (metadata)  
**Inputs (symbols/constants):** runtime environment  
**Units/Normalization:** N/A

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `git_commit`, `git_branch`, `git_status`, `python`, `packages{}`, `rocm{}`, `seeds[]`, `hostname`, `gpus[]`, `probe_mode`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/provenance.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `git_commit:str`, `git_branch:str`, `git_status:str`, `python:str`, `packages:dict`, `rocm:dict`, `seeds:array`, `hostname:str`, `gpus:array`, `probe_mode:str`
- Index/primary keys: none (singleton per run)

**Update cadence / lifecycle:** `once per run`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:195-208 • 800ceda`  
**Validation hooks / KPIs:** N/A (metadata)  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Includes Python package versions and GPU info

---

#### geometry config artifacts  <a id="data-geom-config"></a>
**Type:** log  
**Purpose:** Configuration snapshots for geometry bundle runs (concepts, layers, steps, hyperparameters)  
**Produced by:** TODO: add anchor (see tools/geom_bundle_builder.py)  
**Defined by (if math):** N/A (config)  
**Inputs (symbols/constants):** run configuration  
**Units/Normalization:** N/A

**Shape & axes (exact as used):**
- Shape: JSON objects (multiple files)
- Files: `concepts.json`, `layers.json`, `steps.json`, `geom_config.json`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `<storage_root>/<hostname>/<date>/VDM_geom_<suffix>/{concepts|layers|steps|geom_config}.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- concepts.json: `{"concepts": [...]}`
- layers.json: `{"layers": [...]}`
- steps.json: `{"steps": [...]}`
- geom_config.json: full config dict

**Update cadence / lifecycle:** `once per run`  
**Provenance (code locations):** `tools/geom_bundle_builder.py:211-230 • 800ceda`  
**Validation hooks / KPIs:** N/A (config)  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified from code)  
**Notes:** Separate files for easy command-line access

---

## Runtime & Dashboard Artifacts

#### events.jsonl  <a id="data-events-jsonl"></a>
**Type:** log  
**Purpose:** Rolling JSONL log of runtime telemetry events (tick metrics, system state)  
**Produced by:** TODO: add anchor (see fum_rt/runtime)  
**Defined by (if math):** N/A (telemetry)  
**Inputs (symbols/constants):** runtime state  
**Units/Normalization:** varies per metric

**Shape & axes (exact as used):**
- Shape: JSONL (one event per line)
- Fields per line: `t`, `extra{active_synapses, avg_weight, cohesion_components, complexity_cycles, b1_z, sie_valence_01, sie_v2_valence_01, connectome_entropy, ...}`

**Storage format & path pattern:**
- Format: `jsonl`
- Path pattern: `runs/<timestamp>/events.jsonl`
- Compression/encoding: rolling buffer with archival (FUM_EVENTS_MAX_MB, default 256 MB)

**Schema / columns (for tables/logs):**
- Columns: `t:int`, `extra:dict{active_synapses:float, avg_weight:float, cohesion_components:float, complexity_cycles:float, b1_z:float, sie_valence_01:float, sie_v2_valence_01:float, connectome_entropy:float}`
- Index/primary keys: t (tick)

**Update cadence / lifecycle:** `per tick`  
**Provenance (code locations):** `fum_rt/io/logging/rolling_jsonl.py • 800ceda` ; `fum_rt/frontend/models/series.py:77-141 • 800ceda`  
**Validation hooks / KPIs:** dashboard timeseries continuity  
**Retention / access constraints:** rolling buffer; old events archived to `runs/<timestamp>/archived/<YYYYMMDD_HHMMSS>/events.jsonl`  
**Example artifact (if referenced):** none (runtime data)  
**Notes:** Consumed by dashboard for live charting

---

#### utd_events.jsonl  <a id="data-utd-events-jsonl"></a>
**Type:** log  
**Purpose:** Rolling JSONL log of UTD (Unified Telemetry & Diagnostics) events including macros (say, status, etc.)  
**Produced by:** TODO: add anchor (see fum_rt/runtime)  
**Defined by (if math):** N/A (telemetry)  
**Inputs (symbols/constants):** macro emissions, diagnostics  
**Units/Normalization:** N/A

**Shape & axes (exact as used):**
- Shape: JSONL (one event per line)
- Fields per line: `t`, `macro`, `name`, `kind`, `text`, `meta`, `...` (varies by macro type)

**Storage format & path pattern:**
- Format: `jsonl`
- Path pattern: `runs/<timestamp>/utd_events.jsonl`
- Compression/encoding: rolling buffer with archival (FUM_UTD_MAX_MB, default 256 MB)

**Schema / columns (for tables/logs):**
- Columns: `t:int`, `macro:str`, `name:str`, `kind:str`, `text:str`, `meta:dict`, `...`
- Index/primary keys: t (tick)

**Update cadence / lifecycle:** `per macro emission`  
**Provenance (code locations):** `fum_rt/io/logging/rolling_jsonl.py • 800ceda` ; `fum_rt/frontend/models/series.py:144-154 • 800ceda`  
**Validation hooks / KPIs:** macro presence checks (smoke tests)  
**Retention / access constraints:** rolling buffer; old events archived to `runs/<timestamp>/archived/<YYYYMMDD_HHMMSS>/utd_events.jsonl`  
**Example artifact (if referenced):** none (runtime data)  
**Notes:** Includes "say" text emissions tracked for dashboard speak markers

---

#### dashboard timeseries state  <a id="data-dashboard-series"></a>
**Type:** timeseries  
**Purpose:** In-memory rolling buffers for dashboard timeseries visualization (not persisted)  
**Produced by:** TODO: add anchor (see fum_rt/frontend/models/series.py)  
**Defined by (if math):** N/A (derived from events)  
**Inputs (symbols/constants):** events.jsonl, utd_events.jsonl  
**Units/Normalization:** varies per metric

**Shape & axes (exact as used):**
- Shape: Python lists (in-memory)
- Series: `t[]`, `active[]`, `avgw[]`, `coh[]`, `comp[]`, `b1z[]`, `val[]`, `val2[]`, `entro[]`, `speak_ticks[]`

**Storage format & path pattern:**
- Format: N/A (in-memory only)
- Path pattern: N/A
- Compression/encoding: N/A

**Schema / columns (for tables/logs):**
- N/A (in-memory data structure)

**Update cadence / lifecycle:** `per dashboard refresh`  
**Provenance (code locations):** `fum_rt/frontend/models/series.py:35-170 • 800ceda`  
**Validation hooks / KPIs:** N/A  
**Retention / access constraints:** ephemeral (reconstructed from logs on dashboard restart)  
**Example artifact (if referenced):** N/A  
**Notes:** Streaming ZEMA (z-score of deltas) computed for b1z metric

---

## Checkpoints & State Snapshots

#### connectome checkpoints  <a id="data-connectome-checkpoints"></a>
**Type:** checkpoint  
**Purpose:** Periodic snapshots of connectome state (adjacency, weights, substrate fields)  
**Produced by:** TODO: add anchor (see fum_rt/core/memory/engram_io.py, fum_rt/runtime/helpers/checkpointing.py)  
**Defined by (if math):** TODO: add anchor for connectome structure  
**Inputs (symbols/constants):** runtime connectome state  
**Units/Normalization:** varies per field

**Shape & axes (exact as used):**
- Shape: varies (HDF5 or custom format)
- Groups/datasets: `adj_row_ptr`, `adj_col_idx`, `W`, `substrate fields`, `adc_state`, `metadata`

**Storage format & path pattern:**
- Format: `h5` or custom (configurable)
- Path pattern: `runs/<timestamp>/checkpoints/ckpt_step-<step>.h5` (or similar)
- Compression/encoding: HDF5 compression (if enabled)

**Schema / columns (for tables/logs):**
- HDF5 groups: `/adj`, `/weights`, `/substrate`, `/adc`, `/meta`
- Datasets: CSR arrays, dense arrays, metadata dicts

**Update cadence / lifecycle:** `per checkpoint_every ticks`  
**Provenance (code locations):** `fum_rt/core/memory/engram_io.py • 800ceda` ; `fum_rt/runtime/helpers/checkpointing.py:16-48 • 800ceda`  
**Validation hooks / KPIs:** checkpoint retention policy (keep last N)  
**Retention / access constraints:** configurable via checkpoint_keep  
**Example artifact (if referenced):** none (runtime data)  
**Notes:** Includes ADC (Adaptive Denoising Core) state if present

---

## External Interfaces

#### gravity_regression orbit logs  <a id="data-orbit-logs"></a>
**Type:** table  
**Purpose:** Orbit precession data for gravity regression validation  
**Produced by:** TODO: add anchor (see derivation/gravity_regression/vdm_gravity_regression_pack/scripts/compute_precession.py)  
**Defined by (if math):** TODO: add anchor for precession equations  
**Inputs (symbols/constants):** orbit integration data  
**Units/Normalization:** TODO: link to UNITS_NORMALIZATION.md

**Shape & axes (exact as used):**
- Shape: CSV table
- Columns: `orbit_index`, `peri_angle`, `delta_theta`, `period`

**Storage format & path pattern:**
- Format: `csv`
- Path pattern: varies (specified via --out argument)
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `orbit_index:int`, `peri_angle:float`, `delta_theta:float`, `period:float`
- Index/primary keys: orbit_index

**Update cadence / lifecycle:** `per precession analysis run`  
**Provenance (code locations):** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/compute_precession.py • 800ceda`  
**Validation hooks / KPIs:** PASS_precession_present, median/mean/cv metrics  
**Retention / access constraints:** none  
**Example artifact (if referenced):** `derivation/gravity_regression/vdm_gravity_regression_pack/templates/orbit_log_example.csv`  
**Notes:** Includes summary statistics in output file

---

#### gravity_regression connectome metrics  <a id="data-connectome-metrics"></a>
**Type:** log  
**Purpose:** Graph structure metrics for connectome validation in gravity regression  
**Produced by:** TODO: add anchor (see derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py)  
**Defined by (if math):** TODO: add anchor for graph metrics  
**Inputs (symbols/constants):** connectome graph data  
**Units/Normalization:** dimensionless (graph metrics)

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: graph metrics (degree distribution, clustering, etc.)

**Storage format & path pattern:**
- Format: `json`
- Path pattern: varies (specified via --out argument)
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: varies (graph metrics dict)
- Index/primary keys: none

**Update cadence / lifecycle:** `per graph validation run`  
**Provenance (code locations):** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py • 800ceda`  
**Validation hooks / KPIs:** graph structure invariants  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none (pattern identified)  
**Notes:** Produces accompanying connectome_layout.png visualization

---

#### dark_photon noise budget tables  <a id="data-dp-noise"></a>
**Type:** log  
**Purpose:** Quantitative noise budget outputs (SNR curves, PSDs, regime boundary) for dark‑photon portal analyses  
**Produced by:** TODO: add anchor (see `derivation/code/physics/dark_photons/noise_budget.py`)  
**Defined by (if math):** `EQUATIONS.md#vdm-e-dp-noise`  
**Inputs (symbols/constants):** detector model params, temperature, bandwidth, $t_{\text{int}}$ grid  
**Units/Normalization:** detector-native (PSD units) with normalized SNR

**Shape & axes (exact as used):**
- Shape: JSON and CSV sidecars
- JSON Fields: `params`, `series{t_int[], snr[], regime[]}`, `regime_boundary{t_star, method}`, `notes`
- CSV Columns: `t_int, snr, regime_label`

**Storage format & path pattern:**
- Format: `json` + `csv`
- Path pattern: `derivation/code/outputs/logs/dark_photons/noise_budget__<tag>.{json,csv}`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- JSON: `params:dict`, `series:dict`, `regime_boundary:dict`, `notes:str`
- CSV: `t_int:float`, `snr:float`, `regime_label:str`

**Update cadence / lifecycle:** `per analysis run`  
**Provenance (code locations):** TODO (planned)  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-dp-regime-split`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none  
**Notes:** Include detector noise PSD decomposition and any calibration factors in `params`.

---

#### dark_photon Fisher quick estimate  <a id="data-dp-fisher"></a>
**Type:** log  
**Purpose:** Quick Fisher information estimate for kinetic‑mixing parameter $\varepsilon$ with finite‑difference cross‑check  
**Produced by:** TODO: add anchor (see `derivation/code/physics/dark_photons/fisher_quick.py`)  
**Defined by (if math):** `EQUATIONS.md#vdm-e-dp-fisher`  
**Inputs (symbols/constants):** model likelihood, background PSDs, $\varepsilon$  
**Units/Normalization:** `\sigma(\varepsilon)` dimensionless

**Shape & axes (exact as used):**
- Shape: JSON object
- Fields: `params`, `sigma_epsilon`, `fisher_info`, `method`, `finite_difference_check{sigma_fd, rel_err}`

**Storage format & path pattern:**
- Format: `json`
- Path pattern: `derivation/code/outputs/logs/dark_photons/fisher_eps__<tag>.json`
- Compression/encoding: none

**Schema / columns (for tables/logs):**
- Columns: `params:dict`, `sigma_epsilon:float`, `fisher_info:float`, `method:str`, `finite_difference_check:dict{sigma_fd:float, rel_err:float}`

**Update cadence / lifecycle:** `per analysis run`  
**Provenance (code locations):** TODO (planned)  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-dp-fisher-consistency`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none  
**Notes:** Prefer analytic derivatives where available; include finite‑difference step size in `params`.

---

#### dark_photon EFT ladder figure  <a id="data-dp-eft-figure"></a>
**Type:** image  
**Purpose:** Visual ladder of EFT regimes relevant to portal analyses (masses, couplings, production channels)  
**Produced by:** TODO: add anchor (see `derivation/dark_photons/plot_eft_ladder.py`)  
**Defined by (if math):** `EQUATIONS.md#vdm-e-dp-eft`  
**Inputs (symbols/constants):** EFT parameters, cosmology bounds  
**Units/Normalization:** axis‑appropriate (e.g., eV, GeV)

**Shape & axes (exact as used):**
- Shape: raster image
- Dimensions: ~160 DPI

**Storage format & path pattern:**
- Format: `png`
- Path pattern: `derivation/code/outputs/figures/dark_photons/eft_ladder__<tag>.png`
- Compression/encoding: PNG lossless

**Schema / columns (for tables/logs):**
- N/A (image data)

**Update cadence / lifecycle:** `on update`  
**Provenance (code locations):** TODO (planned)  
**Validation hooks / KPIs:** `VALIDATION_METRICS.md#kpi-dp-eft-coverage`  
**Retention / access constraints:** none  
**Example artifact (if referenced):** none  
**Notes:** Link each labeled regime to references/constraints in caption or sidecar JSON.

---

<!-- BEGIN AUTOSECTION: DATA-INDEX -->
<!-- Tool-maintained list of [Data Product](#data-...) anchors for quick lookup -->

**Conservation Law:**
- [flux_sweep results](#data-flux-sweep)
- [H_candidate_test results](#data-h-candidate-test)
- [opt_H_params results](#data-opt-h-params)
- [fit_H_edge results](#data-fit-h-edge)
- [grid_tau0_report](#data-grid-tau0)
- [qfum_metrics](#data-qfum-metrics)
- [frw_conservation_check](#data-frw-conservation)

**Cosmology / Gravity:**
- [frw_continuity_residual log](#data-frw-balance-log)
- [frw_continuity_residual series](#data-frw-balance-series)
- [frw_continuity_residual figure](#data-frw-balance-figure)

**Reaction-Diffusion:**
- [rd_dispersion_experiment results](#data-rd-dispersion)
- [rd_front_speed_experiment results](#data-rd-front-speed)

**Fluid Dynamics:**
- [taylor_green_benchmark results](#data-taylor-green)
- [lid_cavity_benchmark results](#data-lid-cavity)

**Memory Steering:**
- [memory_steering stability metrics](#data-memory-steering-metrics)

**Agency Field:**
- [agency options probe results](#data-options-probe)

**Vacuum Demographics:**
- [vacuum_demographics results](#data-vacuum-demographics)

**Figures:**
- [conservation_law diagnostic figures](#data-conservation-figures)
- [reaction_diffusion diagnostic figures](#data-rd-figures)
- [fluid_dynamics diagnostic figures](#data-fluid-figures)
- [memory_steering diagnostic figures](#data-memory-figures)
- [agency options heatmap](#data-options-heatmap)
- [vacuum_demographics residual plot](#data-vacuum-figure)

**Dark Photons:**
- [dark_photon noise budget tables](#data-dp-noise)
- [dark_photon Fisher quick estimate](#data-dp-fisher)
- [dark_photon noise budget plots](#data-dp-noise-figures)
- [dark_photon EFT ladder figure](#data-dp-eft-figure)

**Geometry Bundle:**
- [activation matrices](#data-activation-matrices)
- [activation capture metadata](#data-activation-meta)
- [QC statistics](#data-qc-stats)
- [PCA decomposition](#data-pca)
- [PCA thumbnails](#data-pca-thumbs)
- [geometry bundle index](#data-geom-index)
- [geometry bundle provenance](#data-geom-provenance)
- [geometry config artifacts](#data-geom-config)

**Runtime:**
- [events.jsonl](#data-events-jsonl)
- [utd_events.jsonl](#data-utd-events-jsonl)
- [dashboard timeseries state](#data-dashboard-series)
- [connectome checkpoints](#data-connectome-checkpoints)

**External:**
- [gravity_regression orbit logs](#data-orbit-logs)
- [gravity_regression connectome metrics](#data-connectome-metrics)

<!-- END AUTOSECTION: DATA-INDEX -->

## Change Log
- 2025-01-29 • data products compiled from repository • 800ceda
