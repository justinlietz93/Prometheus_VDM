# PROPOSAL_Thermodynamic_Routing_NoSwitch_v2.md

## 1) Title & date

**Passive Thermodynamic Routing (No-Switch Control) in Metriplectic RD** - 2025-10-09

## 2) Proposers

Justin K. Lietz - VDM Project

## 3) Abstract

We pre-register a **passive routing** experiment in a metriplectic reaction–diffusion (RD) medium that certifies **thermodynamic, no-switch control**. The field ( \phi(\mathbf{x},t) ) evolves by a discrete-gradient (DG) **metric** step that monotonically decreases a discrete Lyapunov functional ( L_h[\phi] ); **no rule-based controllers or switches** are used. A 2-channel geometry creates a controlled **free-energy bias** favoring outlet ( \mathcal O_{\mathrm A} ) over ( \mathcal O_{\mathrm B} ). We test whether mass/phase **routes itself** to ( \mathcal O_{\mathrm A} ) purely via thermodynamic descent, and we certify: (G1) zero Lyapunov violations, (G2) an **energy-floor witness** versus a local baseline, (G3) a statistically significant outlet-bias, (G4) **no-switch invariance** (bit-identical code path), and (G5) **Rayleigh–Jeans (RJ)** modal **thermodynamic fits** in a post-collapse window. Optional tagged variant: JMJ (symplectic–metric–symplectic) composition logged alongside DG to compare Strang-defect scaling.

---

## 4) Background & scientific rationale

We consider an RD evolution on a 2-D domain,
$$
\partial_t \phi ;=; D \nabla^2 \phi + f(\phi),
$$
with a discrete **energy** (Lyapunov) functional
$$
L_h[\phi] ;=; \sum_{i}\Big(\tfrac{D}{2},|\nabla_h \phi_i|^2 + \hat V(\phi_i)\Big),\Delta x^d,
\qquad \hat V'(\phi) \equiv -f(\phi).
$$
A DG step ensures ( \Delta L_h \le 0 ) (H-theorem) under periodic/no-flux boundaries. We embed a **thermodynamic funnel** (geometry + potential bias) so that descending ( L_h ) **passively** steers flux to ( \mathcal O_{\mathrm A} ) without switches. In addition to routing/bias metrics, we project onto Laplacian eigenmodes ( {-\Delta\psi_k=\lambda_k\psi_k} ), form modal occupancies ( \langle |c_k|^2\rangle ), and fit a **Rayleigh–Jeans** law
$$
\langle |c_k|^2 \rangle ;\approx; \frac{T}{\lambda_k - \mu},
$$
within a **post-collapse** time window to estimate effective ( (T,\mu) ). These analyses jointly certify **thermodynamic routing** by descent in ( L_h ) with **no external control**.

---

## 5) Objectives & hypotheses

* **H1 (H-theorem):** For the DG **M-only** step, ( \Delta L_h \le 0 ) at every time step (violations (=0)).
* **H2 (Energy-floor witness):** At matched wall-clock horizon (T) and identical initial conditions, the passive DG run achieves a strictly **lower** ( L_h ) than a matched **local baseline** ( L_h^{\text{base}} ) by ( \ge 5\sigma ) (bootstrap over seeds).
* **H3 (Routing bias):** Outlet flux to ( \mathcal O_{\mathrm A} ) exceeds ( \mathcal O_{\mathrm B} ) by a pre-registered margin; report ( B \equiv F_{\mathrm A} - F_{\mathrm B} ) and fraction ( \varrho \equiv \frac{F_{\mathrm A}}{F_{\mathrm A}+F_{\mathrm B}} ).
* **H4 (No-switch invariance):** A **controller-disabled** flag yields trajectories and metrics identical (within machine epsilon) to the default path; logs include `no_switch:true`, stepper SHA, and code-path identity.
* **H5 (Thermalization fit):** In a pre-registered **post-collapse** window, the modal spectrum admits an RJ fit with ( R^2 \ge 0.99 ); report ( (T,\mu) ) and stability across the window.

**Optional (tagged JMJ variant):** For JMJ (Strang) composition, report two-grid slope (expect near-cubic) and the Strang **defect** scaling between JMJ and MJM.

---

## 6) Variables (pre-registered)

**Independent**

* **Geometry:** 2-channel mask with outlet widths (w_{\mathrm A}\ge w_{\mathrm B}), channel length (L_c), obstacles; no-flux walls; outlet segments at right boundary.
* **RD parameters:** ( D, r, u ) for ( f(\phi)=r\phi-u\phi^2 ) (or alternative (f) with ( \hat V'=-f )).
* **Grid/discretization:** ( (N_x,N_y)\in{(256,128),(512,256)} ), ( \Delta x ); stencil ( \in{\text{FD-3pt},\text{spectral}} ) (param-gated).
* **Stepper:** primary **DG M-only**; optional **JMJ** (symplectic half-steps around DG).
* **Time:** ( \Delta t ), horizon (T).
* **Seeds:** number of random initializations; **injection** position(s) and (optional) two-source split ratios.
* **Tags:** string for artifact suffixing.

**Dependent**

* **Lyapunov series:** ( L_h(t) ), per-step ( \Delta L_h ).
* **Outlet fluxes:** ( F_{\mathrm A}, F_{\mathrm B} ) (integrated normal flux through outlet edges).
* **Efficiencies:** ( \eta_{\text{route}}\equiv \frac{F_{\mathrm A}}{F_{\mathrm A}+F_{\mathrm B}} ), ( \eta_{\text{shed}}\equiv 1-\eta_{\text{route}} ) (shed to side walls or ( \mathcal O_{\mathrm B} )).
* **Modal thermodynamics:** ( {\lambda_k,\langle |c_k|^2\rangle} ) and RJ fit ( (T,\mu,R^2) ) in post-collapse window.
* **Defect (optional JMJ):** two-grid slope and JMJ vs MJM defect scaling.

**Controls**

* **Symmetric geometry:** ( w_{\mathrm A}=w_{\mathrm B} \Rightarrow B\approx 0 ).
* **Local baseline:** explicit **local descent** on ( -\nabla L_h ) (no DG correction), same stencil and ( \Delta t ), no switches.
* **Injection robustness:** (i) injection-site sweep (distance to funnel apex), (ii) two-source superposition test (split ratio invariance).

---

## 7) Equipment / Hardware

CPU; optional FFT backend if spectral Laplacian is toggled. All code **additive** under `Derivation/code/physics/thermo_routing/` with shared helpers in `Derivation/code/common/`. No edits to prior experiments or results.

---

## 8) Methods & procedure

### 8.1 Geometry, BCs, and initial state

* Rectangular domain; **two outlets** on the right boundary ( (\mathcal O_{\mathrm A},\mathcal O_{\mathrm B}) ); walls are **no-flux**; outlets are **open** (flux accounting).
* Funnel bias via ( w_{\mathrm A} > w_{\mathrm B} ) and/or a mild potential corridor (reduced ( \hat V )) toward ( \mathcal O_{\mathrm A} ).
* Initial condition: compact “packet” (or uniform slab) injected from the left; **injection-site sweep** varies the packet’s center.

### 8.2 Steppers

* **DG M-only (primary):** implicit discrete-gradient update with Newton solve, backtracking, and logging of identity residuals.
* **Local baseline:** explicit local descent on ( -\nabla L_h ), same ( \Delta t )/stencil, no DG correction.
* **JMJ (optional):** Störmer–Verlet half-J, DG M, half-J; same geometry; used only for tagged comparison.

### 8.3 Flux & efficiency accounting

* Use antisymmetric edge fluxes to ensure consistent conservation accounting at outlets.
* Record per-step and integrated fluxes ( F_{\mathrm A},F_{\mathrm B} ); compute (B), ( \varrho ), ( \eta_{\text{route}} ), ( \eta_{\text{shed}} ).

### 8.4 Collapse detector & RJ fit

* **Collapse time (t_c)**: first time where ( \partial_t L_h ) crosses a pre-set curvature threshold or when the **potential** term drop exceeds a fraction ( \zeta ) of its total change.
* **RJ window:** analyze ( t \in [t_c+\Delta t_c, t_c+\Delta t_c+\Delta T_{\mathrm RJ}] ).
* Project ( \phi(\cdot,t) ) onto Laplacian eigenmodes; compute ( \langle |c_k|^2\rangle ) (time-averaged in the window).
* Fit ( \langle |c_k|^2 \rangle \approx \frac{T}{\lambda_k - \mu} ) (nonlinear least-squares) and report ( (T,\mu,R^2) ).

### 8.5 No-switch invariance

* Runner accepts `--no-switch` (default true). When enabled, it **asserts** the same code path, stamps `no_switch:true`, and records a **SHA** of the stepper configuration.
* We require **bit-level identity** (or machine-epsilon equivalence) of ( L_h(t) ), fluxes, and RJ outputs with/without the flag.

### 8.6 Injection robustness controls

* **Site sweep:** run multiple injection centers; regress ( \eta_{\text{route}} ) vs distance to funnel apex; gate on monotone slope sign and CI.
* **Two-source superposition:** split the total mass between two injection sites at fixed total mass; gate on ( \le 5% ) change in ( \eta_{\text{route}} ) vs split ratio.

---

## 9) Metrics & acceptance gates

**Primary routing / thermodynamics**

* **G1 (H-theorem):** all steps satisfy ( \Delta L_h \le 0 ); identity residuals ( \le 10^{-12} ); violations (=0).
* **G2 (Energy-floor witness):** ( \Delta L_{\mathrm{floor}} \equiv L_h^{\text{base}}(T) - L_h^{\text{DG}}(T) \ge 5\sigma ) (bootstrap CI excludes 0).
* **G3 (Routing bias):** ( B \ge \delta ) and ( \varrho \ge 0.5+\eta ) with 95% CI excluding the null (pre-register ( \delta,\eta ); e.g., ( \delta=0.1, \eta=0.1 )).
* **G4 (No-switch):** default vs `--no-switch` outputs identical (bitwise or within (10^{-12}) in ( \infty )-norms) and logs include `no_switch:true` and stepper SHA.
* **G5 (RJ fit in post-collapse window):** ( R^2 \ge 0.99 ); report ( (T,\mu) ) stability across sub-windows.

**Controls / robustness**

* **G6 (Symmetric geometry):** ( |B| \le 2\sigma ); ( \varrho \approx 0.5 ) (CI contains 0.5).
* **G7 (Injection site sweep):** monotone trend in ( \eta_{\text{route}} ) vs distance; report slope and CI with pre-registered sign.
* **G8 (Two-source split):** ( \le 5% ) variation in ( \eta_{\text{route}} ) across splits at fixed total mass (CI excludes larger change).

**Optional numerics (JMJ tag)**

* Two-grid slope ( \approx 3 ) with ( R^2 \ge 0.999 ); Strang-defect slope logged in a sidecar.
* **Failure plan:** any failed gate emits `CONTRADICTION_REPORT__{tag}.json` with per-seed distributions, geometry masks, collapse logs, and RJ residuals.

---

## 10) Data products & artifact paths (PAPER_STANDARDS)

**Domain:** `thermo_routing`

**Figures** → `Derivation/code/outputs/figures/thermo_routing/`

* `energy_vs_time__{tag}.png` (annotate violations; numeric caption).
* `outlet_flux_bias__{tag}.png` (bars/curves with (B,\varrho) and CIs).
* `routing_streamlines__{tag}.png` (optional, same color map and bounds).
* `rj_fit__{tag}.png` (spectrum + RJ curve; caption with (T,\mu,R^2)).
* `injection_sweep__{tag}.png` and `two_source_split__{tag}.png`.
* **Optional JMJ:** `residual_vs_dt__jmj__{tag}.png`, `strang_defect_vs_dt__{tag}.png`.

**Logs/CSVs/JSON** → `Derivation/code/outputs/logs/thermo_routing/`

* `lyapunov_series__{tag}.csv|json` (include identity terms).
* `flux_timeseries__{tag}.csv`, `flux_summary__{tag}.json` ((F_{\mathrm A},F_{\mathrm B},B,\varrho,\eta_{\text{route}},\eta_{\text{shed}})).
* `energy_floor_witness__{tag}.json` (bootstrap CI, effect size).
* `collapse_detector__{tag}.json` ((t_c,\Delta t_c,\Delta T_{\mathrm RJ})).
* `rj_fit__{tag}.json` ((T,\mu,R^2), window bounds; residuals).
* `injection_sweep__{tag}.csv|json`; `two_source_split__{tag}.csv|json`.
* `spec_snapshot__{tag}.json` (records `no_switch:true`, stepper SHA).
* On fail: `failed_runs/CONTRADICTION_REPORT__{tag}.json`.

All figures carry **numeric captions** (gate statistics). Every figure has CSV/JSON sidecars.

---

## 11) Implementation plan (additive; no edits to prior chapters)

**Code layout**

* `Derivation/code/physics/thermo_routing/run_thermo_routing.py` - CLI (`--spec path.json`).
* `Derivation/code/physics/thermo_routing/geometry.py` - channel masks & flux accounting.
* `Derivation/code/physics/thermo_routing/modal_thermo.py` - Laplacian eigenmaps, modal occupancies, RJ fit.
* `Derivation/code/physics/thermo_routing/collapse.py` - collapse detector, windowing.
* Optional JMJ reuse from existing metriplectic components (param-gated).
* Shared I/O & bootstrap live in `Derivation/code/common/`.

**StepSpec (example)** - `Derivation/specs/thermo_routing/tr_v2.json`

```json
{
  "grid": {"Nx": 256, "Ny": 128, "Lx": 8.0, "Ly": 4.0, "stencil": "fd3"},
  "geometry": {"w_A": 0.6, "w_B": 0.3, "wall_gap": 0.1},
  "rd": {"D": 1.0, "r": 0.2, "u": 0.25},
  "ic": {"type": "packet", "x0": 0.5, "y0": 2.0, "sigma": 0.3, "amplitude": 1.0},
  "time": {"T": 10.0, "dt": 0.01},
  "analysis": {
    "collapse": {"zeta": 0.6, "dt_after": 0.5, "rj_window": 2.0},
    "rj_fit": {"kmin": 3, "kmax": 64, "r2_gate": 0.99}
  },
  "controls": {
    "symmetric_geometry": true,
    "injection_sweep": {"y_list": [1.0, 1.5, 2.0, 2.5, 3.0]},
    "two_source_split": {"ratios": [0.5, 0.6, 0.7, 0.8]}
  },
  "baseline": {"type": "local_descent"},
  "no_switch": true,
  "seeds": 40,
  "gates": {"delta_bias": 0.1, "eta_fraction": 0.1},
  "tag": "TR-v2"
}
```

---

## 12) Risks & mitigations

* **Boundary artifacts:** use antisymmetric fluxes; validate on the **symmetric geometry** control.
* **Weak bias:** increase ( w_{\mathrm A}-w_{\mathrm B} ) or deepen the ( \hat V ) corridor; extend (T).
* **Solver tolerance:** DG Newton with backtracking; log identity residuals; reduce ( \Delta t ) if needed.
* **RJ fit instability:** enforce **post-collapse** window and (k)-band selection; report fit window and residuals.
* **Baseline choice:** same local operators and ( \Delta t ) as DG (fair comparison); no switches.

---

## 13) Evidence & reproducibility

Pre-registered spec; `spec_snapshot__{tag}.json` records geometry hash, `no_switch:true`, and stepper SHA. All figures have numeric captions with gate values. CSV/JSON sidecars accompany every figure. **Failed** gates produce a `CONTRADICTION_REPORT` with ablations. No post-hoc tuning beyond the pre-registered grids.

---

## 14) Timeline

Implementation & smoke: 1 day. Full seeds/site-sweep: hours on CPU. RESULTS assembly: half-day.

---

## 15) References

* Discrete-gradient / metriplectic evolution (H-theorem for (L_h)).
* RD Lyapunov monotonicity and prior VDM validation artifacts (for implementation parity).
* Modal RJ analysis (Rayleigh–Jeans-type occupancy fits) adapted to Laplacian eigenmodes in the post-collapse regime.
