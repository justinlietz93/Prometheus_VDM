<!-- DOC-GUARD: CANONICAL -->
# VDM Validation Metrics & KPIs (Auto-compiled)

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
**Symbol (if any):** `$ \text{rel\_err}_c $`  
**Purpose:** Validate pulled-front speed measurement against theoretical prediction for Fisher-KPP equation  
**Defined by:** `c_{\text{th}} = 2\sqrt{Dr}` (from METRICS.md line 5; theoretical minimal pulled-front speed)  
**Inputs:** [`D`](CONSTANTS.md#const-D) • [`r`](CONSTANTS.md#const-r)  
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:77-119 • 17a0b72` (robust_linear_fit)  
`derivation/code/tests/reaction_diffusion/test_rd_acceptance.py:21-28 • 17a0b72`  
**Pass band / thresholds:** `≤ 0.05` (5% relative error) → see test assertion line 27  
**Units / normalization:** Dimensionless ratio `|c_meas - c_th| / c_th`  
**Typical datasets / experiments:** `N=1024, L=200, D=1.0, r=0.25, T=80` (default params)  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_*.png`  
**Notes:** Acceptance gate requires `R² ≥ 0.98` on front position linear fit (see [R² Front Position Fit](#kpi-r2-front-fit))

#### R² Front Position Fit  <a id="kpi-r2-front-fit"></a>
**Symbol (if any):** `$ R^2_{\text{front}} $`  
**Purpose:** Goodness-of-fit for linear regression of front position vs time  
**Defined by:** Standard coefficient of determination `R² = 1 - SS_res/SS_tot`  
**Inputs:** Time series of front positions from `front_position` function  
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py:77-119 • 17a0b72`  
**Pass band / thresholds:** `≥ 0.98` → test assertion line 26  
**Units / normalization:** Dimensionless, range [0,1]  
**Typical datasets / experiments:** Same as Front Speed Relative Error  
**Primary figure/artifact (if referenced):** Included in JSON metrics output  
**Notes:** Uses robust linear fit with MAD-based outlier rejection

#### Dispersion Median Relative Error  <a id="kpi-dispersion-med-rel-err"></a>
**Symbol (if any):** `$ \text{med\_rel\_err}_{\sigma} $`  
**Purpose:** Validate linear stability analysis by comparing measured vs theoretical growth rates  
**Defined by:** Median of `|σ_meas(k_m) - σ_th(k_m)| / |σ_th(k_m)|` over modes m  
**Inputs:** [`D`](CONSTANTS.md#const-D) • [`r`](CONSTANTS.md#const-r) • mode numbers m → wavenumbers k_m  
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:analyze_dispersion • 17a0b72`  
`derivation/code/tests/reaction_diffusion/test_rd_acceptance.py:30-36 • 17a0b72`  
**Pass band / thresholds:** `≤ 0.10` (10% median relative error) → test assertion line 35  
**Units / normalization:** Dimensionless ratio  
**Typical datasets / experiments:** `N=1024, L=200, D=1.0, r=0.25, T=10, m_max=64`  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_*.png`  
**Notes:** Growth rates fit from linearized mode amplitudes `σ(k) = r - Dk²` (METRICS.md line 4)

#### R² Dispersion Array Fit  <a id="kpi-r2-dispersion-array"></a>
**Symbol (if any):** `$ R^2_{\sigma} $`  
**Purpose:** Goodness-of-fit for growth rate regression across multiple Fourier modes  
**Defined by:** Standard coefficient of determination for mode-by-mode σ fits  
**Inputs:** Time series of Fourier mode amplitudes  
**Computation implemented at:** `derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py:analyze_dispersion • 17a0b72`  
**Pass band / thresholds:** `≥ 0.98` → test assertion line 36  
**Units / normalization:** Dimensionless, range [0,1]  
**Typical datasets / experiments:** Same as Dispersion Median Relative Error  
**Primary figure/artifact (if referenced):** Included in JSON metrics output  
**Notes:** Computed per mode, then aggregated across modes

### Fluid Dynamics (LBM → Navier-Stokes)

#### Taylor-Green Viscosity Recovery Error  <a id="kpi-taylor-green-nu-rel-err"></a>
**Symbol (if any):** `$ \text{rel\_err}_{\nu} $`  
**Purpose:** Certify LBM→NS reduction by recovering kinematic viscosity from energy decay  
**Defined by:** `|ν_fit - ν_th| / ν_th` where `ν_th = (τ - 0.5)/3` and ν_fit from `E(t) = E_0 exp(-2νK²t)`  
**Inputs:** [`τ`](CONSTANTS.md#const-tau-taylor) • grid dimensions → wavenumber correction `K² = k²(1/nx² + 1/ny²)`  
**Computation implemented at:** `derivation/code/tests/fluid_dynamics/test_taylor_green_decay.py:42-83 • 17a0b72`  
`derivation/code/physics/fluid_dynamics/taylor_green_benchmark.py • 17a0b72`  
**Pass band / thresholds:** `≤ 0.05` (5%) at baseline grid `≥ 256²` → test assertion line 83 and BENCHMARKS_FLUIDS.md:19  
**Units / normalization:** Dimensionless ratio; viscosity in LBM units  
**Typical datasets / experiments:** `nx=256, ny=256, τ=0.8 (ν_th=0.1), U0=0.05, steps=3000-5000`  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/fluid_dynamics/taylor_green_benchmark_*.png`  
**Notes:** Refinement test: error decreases with doubled resolution consistent with scheme order (BENCHMARKS_FLUIDS.md:20)

#### Lid Cavity Divergence Maximum  <a id="kpi-lid-cavity-div-max"></a>
**Symbol (if any):** `$ \max_t \|\nabla \cdot \mathbf{v}\|_2 $`  
**Purpose:** Incompressibility constraint verification for LBM flow solver  
**Defined by:** L2 norm of velocity divergence field over time  
**Inputs:** Velocity field `(u_x, u_y)` from LBM moments  
**Computation implemented at:** `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:_metrics • 17a0b72`  
**Pass band / thresholds:** `≤ 1e-6` (double precision) → BENCHMARKS_FLUIDS.md:28  
**Units / normalization:** LBM units, dimensionless  
**Typical datasets / experiments:** `nx=128, ny=128, τ=0.7, U_lid=0.1, steps=15000`  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/fluid_dynamics/lid_cavity_benchmark_*.png`  
**Notes:** Monitored over time; max value compared against threshold

### Conservation Law (QFUM Logistic Invariant)

#### Q-Invariant Maximum Drift  <a id="kpi-q-invariant-drift"></a>
**Symbol (if any):** `$ \Delta Q_{\max} = \max_t |Q(t) - Q(0)| $`  
**Purpose:** Verify logarithmic first integral conservation for autonomous logistic ODE  
**Defined by:** `Q(W,t) = ln(W/(r - uW)) - rt` should be constant for `dW/dt = rW - uW²`  
**Inputs:** [`r`](CONSTANTS.md#const-r) • `u` • solution trajectory W(t)  
**Computation implemented at:** `derivation/code/physics/conservation_law/qfum_validate.py:118-193 • 17a0b72` (Q_invariant function + plot_Q_drift)  
**Pass band / thresholds:** `≤ 1e-8` for RK4, `≤ 1e-5` for Euler → qfum_validate.py:277 (drift_gate)  
**Units / normalization:** Dimensionless  
**Typical datasets / experiments:** `r=0.15, u=0.25, W0=0.12-0.62, T=40, dt=0.001 (RK4)`  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/conservation_law/qfum_Q_drift_*.png`  
**Notes:** Acceptance routed to pass/stable/arxiv outputs based on drift_gate (lines 277-294)

#### Convergence Slope (dt)  <a id="kpi-convergence-slope-dt"></a>
**Symbol (if any):** `$ p_{\text{conv}} $` (power law exponent)  
**Purpose:** Verify solver order-of-accuracy via convergence study  
**Defined by:** Slope of log-log fit `ΔQ_max ~ dt^p` across multiple timesteps  
**Inputs:** Series of dt values and corresponding `ΔQ_max` measurements  
**Computation implemented at:** `derivation/code/physics/conservation_law/qfum_validate.py:153-163 • 17a0b72` (fit_loglog)  
**Pass band / thresholds:** No explicit threshold; informational (expected p ≈ 4 for RK4, p ≈ 1 for Euler)  
**Units / normalization:** Dimensionless exponent  
**Typical datasets / experiments:** `dt ∈ {0.002, 0.001, 0.0005}` for convergence sweep  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/conservation_law/qfum_convergence_*.png`  
**Notes:** Uses `r2` goodness-of-fit; reported in ConvergenceMetrics dataclass (lines 142-150)

### Memory Steering

#### Memory Steering Pole Fit Error  <a id="kpi-memory-pole-fit-err"></a>
**Symbol (if any):** `$ |p_{\text{fit}} - p_{\text{pred}}| $`  
**Purpose:** Verify linear response and stability of discrete leaky integrator  
**Defined by:** Absolute error between fitted exponential decay pole and predicted value `p_pred = 1 - λ - g`  
**Inputs:** [`g`](CONSTANTS.md#const-alpha) (gain) • `λ` (leak) • step response time series  
**Computation implemented at:** `derivation/code/physics/memory_steering/memory_steering_acceptance.py:run_filter • 17a0b72`  
`derivation/code/tests/memory_steering/test_memory_steering.py • 17a0b72`  
**Pass band / thresholds:** `≤ 0.02` (absolute) → memory_steering_acceptance_verification.md:47  
**Units / normalization:** Dimensionless  
**Typical datasets / experiments:** `g=0.12, λ=0.08 → p_pred=0.80` (default acceptance run)  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/memory_steering/step_response_*.png`  
**Notes:** Fixed point error `|M_final - M*| ≤ 0.01` also checked (line 48)

#### Memory Steering Canonical Void Target  <a id="kpi-memory-void-target"></a>
**Symbol (if any):** `$ M_* = 0.6 $`  
**Purpose:** Validate void equilibrium target W ≈ 0.6 with canonical parameter mapping  
**Defined by:** Fixed point `M* = gs/(g+λ)` with `s≡1, g=1.5λ → M*=0.6`  
**Inputs:** `g=1.5λ` • constant signal `s=1`  
**Computation implemented at:** `derivation/code/tests/memory_steering/test_memory_steering.py:test_canonical_void • 17a0b72`  
**Pass band / thresholds:** `|M_final - 0.6| ≤ 0.02` → memory_steering_acceptance_verification.md:52-53  
**Units / normalization:** Memory variable M ∈ [0,1]  
**Typical datasets / experiments:** Seeds {0,1,2}, 512 steps (step at t=64)  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/memory_steering/canonical_void_*.png`  
**Notes:** Must hold across multiple seeds for reproducibility

#### Memory Steering SNR Improvement  <a id="kpi-memory-snr-improvement"></a>
**Symbol (if any):** `$ \Delta \text{SNR} = \text{SNR}_{\text{out}} - \text{SNR}_{\text{in}} $`  
**Purpose:** Verify noise suppression capability of leaky integrator filter  
**Defined by:** SNR difference in dB between filtered output and noisy input signal  
**Inputs:** Noisy input signal `s(t) = s_sig(t) + n(t)` with `σ_n = 0.05` (default)  
**Computation implemented at:** `derivation/code/physics/memory_steering/memory_steering_acceptance.py • 17a0b72`  
**Pass band / thresholds:** `≥ 3 dB` improvement → memory_steering_acceptance_verification.md:57  
**Units / normalization:** Decibels (dB)  
**Typical datasets / experiments:** Low-frequency sinusoid + white noise, default noise σ=0.05  
**Primary figure/artifact (if referenced):** `derivation/code/outputs/figures/memory_steering/noise_suppression_*.png`  
**Notes:** Uses parallel signal-only filter for ground-truth comparison

---

## Stability & Safety Guards

#### ΛCDM Residual (w+1)  <a id="kpi-lcdm-residual"></a>
**Symbol (if any):** `$ |w(z) + 1| $`  
**Purpose:** Validate vacuum equation-of-state against ΛCDM baseline for cosmology channel  
**Defined by:** Residual of equation-of-state parameter w relative to cosmological constant w=-1  
**Inputs:** Redshift z, horizon activity events, retarded kernel parameters  
**Computation implemented at:** `fum_rt/physics/vacuum_demographics_harness.py:230-283 • 17a0b72` (_aggregate_metrics)  
**Pass band / thresholds:** `≤ 5e-4` (default residual_tol) → vacuum_demographics_harness.py:383 (CLI arg)  
**Units / normalization:** Dimensionless  
**Typical datasets / experiments:** Synthetic horizon activity tape or user-supplied events  
**Primary figure/artifact (if referenced):** w(z)+1 residual plot (figure_path output)  
**Notes:** Harness exits with status `NEEDS_RECAL` when tolerance exceeded (line 233)

#### CFL Condition  <a id="kpi-cfl-condition"></a>
**Symbol (if any):** `$ \Delta t \lesssim \frac{\Delta x^2}{2dD} $`  
**Purpose:** Stability constraint for explicit finite-difference diffusion schemes  
**Defined by:** Courant-Friedrichs-Lewy condition limiting timestep relative to spatial resolution  
**Inputs:** [`D`](CONSTANTS.md#const-D) • [`dx`] • spatial dimension d  
**Computation implemented at:** Throughout RD experiments: `dt = cfl * dx²/(2*D)` pattern  
`derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py • 17a0b72`  
**Pass band / thresholds:** [`cfl`](CONSTANTS.md#const-cfl) default 0.2 for safety margin  
**Units / normalization:** Dimensionless Courant number  
**Typical datasets / experiments:** All explicit time-stepping simulations  
**Primary figure/artifact (if referenced):** N/A (stability constraint, not measured)  
**Notes:** Also documented in EQUATIONS.md#VDM-E-006 for agency field; AGENCY_FIELD.md:76

#### Drift Gate (Conservation Law)  <a id="kpi-drift-gate"></a>
**Symbol (if any):** `$ \text{drift\_gate} $`  
**Purpose:** Acceptance threshold for routing QFUM validation outputs  
**Defined by:** Maximum allowed Q-invariant drift to classify run as pass/stable/arxiv  
**Inputs:** Solver type (RK4 vs Euler) determines threshold  
**Computation implemented at:** `derivation/code/physics/conservation_law/qfum_validate.py:277 • 17a0b72`  
**Pass band / thresholds:** `1e-8` (RK4), `1e-5` (Euler) → line 277  
**Units / normalization:** Same as [Q-Invariant Maximum Drift](#kpi-q-invariant-drift)  
**Typical datasets / experiments:** Part of QFUM validation acceptance criteria  
**Primary figure/artifact (if referenced):** N/A (threshold constant)  
**Notes:** Pass: `drift_ok` → outputs/stable/; fail → outputs/failed_runs/ (lines 278-294)

#### B1 Spike Detection (z-score)  <a id="kpi-b1-spike-z"></a>
**Symbol (if any):** `$ z_{\text{spike}} $`  
**Purpose:** Threshold for detecting anomalies in cyclomatic complexity time series  
**Defined by:** Z-score of first-difference relative to EMA baseline  
**Inputs:** Cyclomatic complexity series, [`speak_z`](CONSTANTS.md#const-speak_z_4) threshold  
**Computation implemented at:** `fum_rt/core/metrics.py:55-116 • 17a0b72` (StreamingZEMA class)  
`fum_rt/nexus.py • 17a0b72` (b1_detector instantiation)  
**Pass band / thresholds:** [`speak_z=3.5`](CONSTANTS.md#const-speak_z_4) for phase 4 (problem-solving) → runtime/phase.py:55  
**Units / normalization:** Standard deviations (z-score)  
**Typical datasets / experiments:** Runtime telemetry, void-native signals  
**Primary figure/artifact (if referenced):** N/A (streaming detector, no static artifact)  
**Notes:** Uses hysteresis [`speak_hysteresis=1.2`](CONSTANTS.md#const-speak_hysteresis_4) to prevent chatter; cooldown `min_interval_ticks`

---

## Performance / Efficiency Metrics

#### Average Weight  <a id="kpi-avg-weight"></a>
**Symbol (if any):** `$ \bar{W} $`  
**Purpose:** Monitor global connectome activity level  
**Defined by:** Mean of weight matrix W  
**Inputs:** Connectome weight matrix W  
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics)  
**Pass band / thresholds:** No explicit threshold; informational metric  
**Units / normalization:** Nondimensional weight units  
**Typical datasets / experiments:** Runtime telemetry at each tick  
**Primary figure/artifact (if referenced):** Logged in telemetry JSON  
**Notes:** Returned as `avg_weight` in metrics dict (line 24)

#### Active Synapses  <a id="kpi-active-synapses"></a>
**Symbol (if any):** `$ N_{\text{active}} $`  
**Purpose:** Count active edges in connectome graph  
**Defined by:** Number of synapses above activation threshold  
**Inputs:** Connectome E (efficacy) and A (adjacency) matrices, threshold  
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics → active_edge_count method)  
**Pass band / thresholds:** No explicit threshold; sparsity/utilization indicator  
**Units / normalization:** Integer count  
**Typical datasets / experiments:** Runtime telemetry, golden run parity checks  
**Primary figure/artifact (if referenced):** Tracked in tools/golden_run_parity.py:default metric keys  
**Notes:** Alias: `active_edges` in some contexts

#### Cohesion Components  <a id="kpi-cohesion-components"></a>
**Symbol (if any):** `$ C_{\text{comp}} $`  
**Purpose:** Detect graph fragmentation and emergent multi-agent behavior  
**Defined by:** Number of connected components in active subgraph  
**Inputs:** Connectome active subgraph (E > threshold & A == 1)  
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics → connected_components method)  
**Pass band / thresholds:** `> 1` triggers emergent GDSP activation → fum_rt/runtime/loop/main.py:comp check  
**Units / normalization:** Integer count (≥1)  
**Typical datasets / experiments:** Runtime telemetry, UTD event scans  
**Primary figure/artifact (if referenced):** Logged in emission records, redis outputs  
**Notes:** Key trigger for domain cartography scheduling; part of pathology detection (Blueprint Rule 4.1)

#### Complexity Cycles  <a id="kpi-complexity-cycles"></a>
**Symbol (if any):** `$ \text{cyclomatic\_complexity} $`  
**Purpose:** Proxy for topological complexity; feeds B1 spike detector  
**Defined by:** Cyclomatic complexity or cycle basis count of active subgraph  
**Inputs:** Connectome active subgraph  
**Computation implemented at:** `fum_rt/core/metrics.py:11-29 • 17a0b72` (compute_metrics → cyclomatic_complexity method)  
**Pass band / thresholds:** No direct threshold; first-difference used by [B1 Spike Detection](#kpi-b1-spike-z)  
**Units / normalization:** Integer count  
**Typical datasets / experiments:** Runtime telemetry; augmented by adc_cycle_hits when ADC active  
**Primary figure/artifact (if referenced):** N/A (streaming input to spike detector)  
**Notes:** StreamingZEMA monitors `Δ(complexity_cycles)` for anomalies (fum_rt/core/metrics.py:50-52)

#### Connectome Entropy  <a id="kpi-connectome-entropy"></a>
**Symbol (if any):** `$ H = -\sum p_i \log p_i $`  
**Purpose:** Global pathological structure detection via degree distribution entropy  
**Defined by:** Shannon entropy of degree distribution of active subgraph  
**Inputs:** Connectome active edges → degree vector → probability distribution  
**Computation implemented at:** `fum_rt/core/metrics.py:31-47 • 17a0b72` (connectome_entropy function)  
**Pass band / thresholds:** No explicit threshold; supports Active Domain Cartography scheduling (Blueprint Rule 7)  
**Units / normalization:** Nats (natural log); 0.0 when no active edges  
**Typical datasets / experiments:** Runtime telemetry, golden run parity, UTD scans  
**Primary figure/artifact (if referenced):** Logged in emission records  
**Notes:** Formula: `H = -Σ p_i log(p_i)` where p is degree distribution (line 34 comment)

#### Void Traveler Entropy  <a id="kpi-vt-entropy"></a>
**Symbol (if any):** `$ H_{\text{VT}} $`  
**Purpose:** Void-native signal for tracking novelty/diversity in walker behavior  
**Defined by:** Entropy measure derived from void traveler trajectories  
**Inputs:** Void traveler state/trajectory data  
**Computation implemented at:** Void traveler subsystem (specific implementation TODO in sparse-mode connectome)  
**Pass band / thresholds:** No explicit threshold; used in SIE TD proxy and golden run parity  
**Units / normalization:** Nats or bits depending on implementation  
**Typical datasets / experiments:** Runtime telemetry, tracked over time for temporal difference signals  
**Primary figure/artifact (if referenced):** Logged in composer, emission, redis outputs  
**Notes:** Previous value tracked in `_prev_vt_entropy` for TD calculation (fum_rt/nexus.py)

#### Void Traveler Coverage  <a id="kpi-vt-coverage"></a>
**Symbol (if any):** `$ \text{vt\_coverage} $`  
**Purpose:** Measure spatial exploration extent of void travelers  
**Defined by:** Fraction of graph/space covered by walker trajectories  
**Inputs:** Void traveler trajectory data  
**Computation implemented at:** Void walker traversal metrics (implementation details in walker subsystem)  
**Pass band / thresholds:** No explicit threshold; diagnostic/observability metric  
**Units / normalization:** Fraction [0,1] or percentage  
**Typical datasets / experiments:** Runtime telemetry, golden run parity comparisons  
**Primary figure/artifact (if referenced):** Logged in emission records  
**Notes:** Used in smoke tests: `obs:vt_coverage↑` (fum_rt/runtime/helpers/smoke.py)

---

## Domain-Specific Metrics

### Graph Structure (Gravity Regression)

#### Degree Variance  <a id="kpi-degree-variance"></a>
**Symbol (if any):** `$ \sigma^2_{\text{deg}} $`  
**Purpose:** Detect ring-lattice topology via uniform degree distribution  
**Defined by:** Variance of node degree distribution  
**Inputs:** Graph edgelist → degree sequence  
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72` (ring_lattice_suspicion)  
**Pass band / thresholds:** `< 1.0` for ring-lattice suspicion (line 39)  
**Units / normalization:** Squared degree units  
**Typical datasets / experiments:** Connectome graph structure validation  
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json`  
**Notes:** Part of ring-lattice detection heuristic with clustering and cycle count

#### Average Clustering Coefficient  <a id="kpi-avg-clustering"></a>
**Symbol (if any):** `$ \bar{C} $`  
**Purpose:** Measure local connectivity density in graph structure  
**Defined by:** NetworkX `average_clustering` over all nodes  
**Inputs:** Graph adjacency structure  
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72`  
**Pass band / thresholds:** `< 0.2` for ring-lattice suspicion (line 39)  
**Units / normalization:** Fraction [0,1]  
**Typical datasets / experiments:** Connectome topology analysis  
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json`  
**Notes:** Low clustering indicates lattice-like structure; higher clustering indicates small-world/random

#### Degree Assortativity  <a id="kpi-degree-assortativity"></a>
**Symbol (if any):** `$ r_{\text{deg}} $`  
**Purpose:** Measure tendency of nodes to connect to similar-degree neighbors  
**Defined by:** Pearson correlation of degrees across edges  
**Inputs:** Graph edge structure and node degrees  
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72` (nx.degree_assortativity_coefficient)  
**Pass band / thresholds:** No explicit threshold; informational metric  
**Units / normalization:** Correlation coefficient [-1, 1]  
**Typical datasets / experiments:** Graph structure characterization  
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json`  
**Notes:** Returns NaN gracefully if computation fails (line 35 exception handling)

#### Cycle Basis Count  <a id="kpi-cycle-basis-count"></a>
**Symbol (if any):** `$ N_{\text{cycles}} $`  
**Purpose:** Count fundamental cycles for ring-lattice detection  
**Defined by:** Size of cycle basis from NetworkX for undirected graph  
**Inputs:** Graph structure  
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:26-49 • 17a0b72` (nx.cycle_basis)  
**Pass band / thresholds:** `≥ N * 0.8` for ring-lattice suspicion (line 39)  
**Units / normalization:** Integer count  
**Typical datasets / experiments:** Connectome topology validation  
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json`  
**Notes:** High cycle count relative to node count indicates lattice structure

#### Ring Lattice Suspicion Flag  <a id="kpi-ring-lattice-suspicion"></a>
**Symbol (if any):** `$ \text{ring\_lattice\_suspicion} $`  
**Purpose:** Boolean flag for detecting degenerate ring-lattice topology  
**Defined by:** `(deg_var < 1.0) AND (avg_clustering < 0.2) AND (cycle_count ≥ N*0.8)`  
**Inputs:** [Degree Variance](#kpi-degree-variance), [Average Clustering](#kpi-avg-clustering), [Cycle Basis Count](#kpi-cycle-basis-count)  
**Computation implemented at:** `derivation/gravity_regression/vdm_gravity_regression_pack/scripts/graph_checks.py:39 • 17a0b72`  
**Pass band / thresholds:** Boolean (true=suspect, false=ok)  
**Units / normalization:** Boolean flag  
**Typical datasets / experiments:** Gravity regression connectome validation  
**Primary figure/artifact (if referenced):** `outputs/connectome_metrics.json`  
**Notes:** Heuristic for catching pathological toy topologies

### Fluid Dynamics Announcers (Void Walkers)

#### Divergence Announcer Statistics  <a id="kpi-div-announce-stats"></a>
**Symbol (if any):** `$ \text{div\_p50, div\_p90, div\_max} $`  
**Purpose:** Passive diagnostics of incompressibility violations via walker-based sensors  
**Defined by:** Quantiles (p50, p90, max) of divergence values sampled by advected walkers  
**Inputs:** Velocity field (u_x, u_y) → local divergence at walker positions  
**Computation implemented at:** `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:compute_void_walker_metrics • 17a0b72`  
**Pass band / thresholds:** No enforcement; observe-only mode (default `walker_mode=observe`)  
**Units / normalization:** LBM units, dimensionless  
**Typical datasets / experiments:** Lid cavity with `--walker_announce --walkers 210`  
**Primary figure/artifact (if referenced):** Logged in `metrics.void_announcers.announce_stats` JSON field  
**Notes:** Part of void-faithful observability layer; non-interference verified by test_walkers_noninterference.py

#### Swirl Announcer Statistics  <a id="kpi-swirl-announce-stats"></a>
**Symbol (if any):** `$ \text{swirl\_p50, swirl\_p90, swirl\_max} $`  
**Purpose:** Monitor vorticity magnitude distribution via walker sensors  
**Defined by:** Quantiles of `|ω|` sampled by walkers (where ω = ∂u_y/∂x - ∂u_x/∂y)  
**Inputs:** Velocity field → vorticity at walker positions  
**Computation implemented at:** `derivation/code/physics/fluid_dynamics/lid_cavity_benchmark.py:compute_void_walker_metrics • 17a0b72`  
**Pass band / thresholds:** Advisory target `policy_swirl_target=5e-3` (default) for optional policy mode  
**Units / normalization:** LBM units  
**Typical datasets / experiments:** Same as Divergence Announcer  
**Primary figure/artifact (if referenced):** Logged in `metrics.void_announcers.announce_stats` JSON field  
**Notes:** Observe-only by default; advise/act modes apply bounded parameter updates (no forcing)

### Geometry Probe (Tool Metrics)

#### Activation Matrix Statistics  <a id="kpi-activation-matrix-stats"></a>
**Symbol (if any):** `$ \text{mean, std, min, max} $`  
**Purpose:** Validate captured activation matrices from model layer probes  
**Defined by:** Basic descriptive statistics of activation matrix per layer/step  
**Inputs:** Activation matrix (concepts × features) from adapter.encode_concepts  
**Computation implemented at:** `tools/geom_bundle_builder.py:_compute_stats • 17a0b72`  
**Pass band / thresholds:** No explicit threshold; QC metadata for geometry bundles  
**Units / normalization:** Model-dependent (raw activation units)  
**Typical datasets / experiments:** Geometry probe runs capturing layer activations at checkpoints  
**Primary figure/artifact (if referenced):** Stored in `qc/{layer}_step-{step}_stats.json`  
**Notes:** Part of bundle provenance and quality control artifacts

#### PCA Explained Variance Ratio  <a id="kpi-pca-explained-variance"></a>
**Symbol (if any):** `$ \text{explained\_variance\_ratio} $`  
**Purpose:** Dimensionality assessment of activation geometry  
**Defined by:** Fraction of variance explained by top PCA components (n_components=3 default)  
**Inputs:** Activation matrix → PCA decomposition  
**Computation implemented at:** `tools/geom_bundle_builder.py:_compute_pca • 17a0b72`  
**Pass band / thresholds:** No explicit threshold; informational for geometry analysis  
**Units / normalization:** Fraction [0,1] per component  
**Typical datasets / experiments:** Same as Activation Matrix Statistics  
**Primary figure/artifact (if referenced):** Stored in `qc/{layer}_step-{step}_pca.json`  
**Notes:** Includes principal component vectors for downstream geometry probes

---

<!-- BEGIN AUTOSECTION: METRICS-INDEX -->
<!-- Tool-maintained list of [Metric](#kpi-...) anchors for quick lookup -->

**Quick Index:**
- [Active Synapses](#kpi-active-synapses)
- [Activation Matrix Statistics](#kpi-activation-matrix-stats)
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
- [R² Dispersion Array Fit](#kpi-r2-dispersion-array)
- [R² Front Position Fit](#kpi-r2-front-fit)
- [Ring Lattice Suspicion Flag](#kpi-ring-lattice-suspicion)
- [Swirl Announcer Statistics](#kpi-swirl-announce-stats)
- [Taylor-Green Viscosity Recovery Error](#kpi-taylor-green-nu-rel-err)
- [Void Traveler Coverage](#kpi-vt-coverage)
- [Void Traveler Entropy](#kpi-vt-entropy)
- [ΛCDM Residual (w+1)](#kpi-lcdm-residual)

<!-- END AUTOSECTION: METRICS-INDEX -->

## Change Log
- 2025-01-08 • Initial compilation from repository code and tests • 17a0b72
