# Coding Rules Distilled from Multiscale VDM System Specifications and Scientific Validations

**Generated on:** October 25, 2025 at 9:59 PM CDT

---

## **Architecture & Design**

* Use a discrete gradient (DG) integrator for the reaction-diffusion metric descent step.
* Implement J-step as exact periodic advection by a spectral phase shift.
* Implement M-step as discrete-gradient (DG) implicit step for RD with Newton/backtracking.
* Implement Strang composition as $\Phi^{\mathrm{JMJ}}_{\Delta t} \;=\; \Phi^{\mathrm{J}}_{\Delta t/2} \; \circ \; \Phi^{\mathrm{M}}_{\Delta t} \; \circ \; \Phi^{\mathrm{J}}_{\Delta t/2}$.
* Use leapfrog (Störmer–Verlet) as time integrator.
* Stagger $\pi$ at half-steps when using leapfrog.
* Sample energy density compatibly with staggering when using leapfrog.
* Use second-order centered differences for spatial discretization of $\nabla$ and $\nabla^2$.
* Implement J-step as exact periodic advection by a spectral phase shift.
* Implement M-step as discrete-gradient (DG) implicit step for RD with Newton/backtracking.
* Compose a metriplectic integrator by pairing a symplectic J-step with the DG M-step.
* Target discrete Noether invariants for the conservative sector when composing metriplectic integrators.
* Target exact entropy monotonicity for the dissipative sector when composing metriplectic integrators.
* Represent walls via potential $V$.
* Parameterize spectral vs stencil Laplacian options via `m_lap_operator`.
* Prefer the spectral-DG option (param-gated) for new mixed-model experiments (e.g., KG $\oplus$ RD) to minimize J-M mismatch.
* Keep the stencil baseline available for ablations.
* Implement prereg geometry with no-flux walls and open outlets (biased widths).
* For Phase B (Wave Flux Meter), add two outlets and absorber/PML.
* For Phase B (Wave Flux Meter), check conservation on the interior rectangle.
* For Phase B (Wave Flux Meter), place ports at the left/right boundaries of the interior rectangle.
* For Phase B (Wave Flux Meter), auto-detect narrow bands for ports on the left/right interior boundaries.
* For Phase B (Wave Flux Meter), ports must be within the predefined port window.
* For Phase B (Wave Flux Meter), ports must be aligned to the $\mu$ channel corridors.
* For Phase C (Wave Flux Meter), use frozen $V(x,y)$.
* For Phase C (Wave Flux Meter), compare $\mu$-aligned port energy capture against shuffled-$\mu$ control.
* For Phase C (Wave Flux Meter), investigate directionality under mirrored drive.
* Router functional form for scaling collapse must be logistic $\sigma(X)$.
* Collapse coordinate for scaling collapse must be $X=\Theta\,\Delta m$.
* Use a shared $X$-grid for interpolation in scaling collapse analysis.
* Restric study of Discrete Conservation vs Balance in Reaction-Diffusion (RD) Steppers to periodic boundary conditions for Obj-A/B order and balance tests.
* Use logistic reaction as standard nonlinearity for RD systems.
* Test explicit Euler scheme for RD systems.
* Test Strang splitting scheme (CN half-steps in diffusion with exact reaction) for RD systems.
* Test discrete-gradient RD scheme (implicit, AVF reaction + midpoint Laplacian with Newton/backtracking) for RD systems.
* Use small amplitudes to maintain linear regime for dispersion in KG J-only Validations.
* Initialize a single Fourier mode for dispersion analysis.
* Initialize a narrow Gaussian for light cone analysis.
* For Phase C, propose target X and N.

## **Configuration & Parameters**

* BLAS implementation must be 'openblas'.
* FFT implementation must be 'numpy.pocketfft'.
* FFT plans must be deterministic.
* The number of threads must be 32.
* The no-switch clause must be "bitwise".
* Use dimensionless program with normalization $\mu=1$ and $c=1$ unless stated otherwise.
* For Tachyonic Tube v1, Radius $R$ must be within $[0.5,6.0]$.
* For Tachyonic Tube v1, Azimuthal index $\ell$ must be within $\{0,1,\dots,8\}$.
* For Tachyonic Tube v1, $\mu$ parameter must be 1.
* For Tachyonic Tube v1, $c$ parameter must be 1.
* For Tachyonic Tube v1, $\sigma$ parameter must be 0.6.
* For Tachyonic Tube v1, $\alpha$ parameter must be 12.0.
* For Tachyonic Tube v1, $\lambda$ parameter must be 0.5.
* For Wave Flux Meter A-Phase, Grid dimensions must be $N_x=128, N_y=64$.
* For Wave Flux Meter A-Phase, Domain dimensions must be $L_x=8, L_y=4$.
* For Wave Flux Meter A-Phase, Time step $\Delta t$ must be $2.5\times10^{-4}$.
* For Wave Flux Meter A-Phase, Duration $T$ must be $2.0$.
* For Wave Flux Meter A-Phase, Wave speed $c$ must be $1$.
* Use double precision.
* Use single-threaded BLAS/FFT.
* Use deterministic seeds.
* For Wave Flux Meter Phase B, Grid dimensions must be 256×128.
* For Wave Flux Meter Phase B, Domain must be Lx×Ly=8×4.
* For Wave Flux Meter Phase B, Interior box must exclude an `n_abs=8`-cell sponge on each side.
* CFL guard must be 0.35.
* Warm-up exclusion must be 10% of the record for metrics.
* `use_mu_weighting` must be false.
* If using $\mu$-weighted dynamics, increase warm-up to 20%.
* If using $\mu$-weighted dynamics, thicken absorber to 12–16 cells.
* If using $\mu$-weighted dynamics, set $\sigma_{\text{max}}\approx 3$.
* If using $\mu$-weighted dynamics, increase resolution to 512×256.
* For FRW Continuity Residual, Equation of state parameter $w$ must be fixed to 0 (dust).
* For FRW Continuity Residual, Scaling law $\rho(a)$ must be $\rho_0 a^{-3}$ analytically.
* For FRW Continuity Residual, Time grid must be uniform $\Delta t$.
* Use IEEE-754 double precision for floating-point.
* RNG must not be used (use deterministic synthetic control).
* For KG Energy Oscillation v1, use linear KG on periodic 1D lattice.
* For KG Energy Oscillation v1, use spectral gradient/Laplacian.
* For KG Energy Oscillation v1, parameter $c$ must be 1.0.
* For KG Energy Oscillation v1, parameter $m$ must be 0.5.
* For KG Energy Oscillation v1, $N$ must be 256.
* For KG Energy Oscillation v1, $dx$ must be 1.0.
* For KG Energy Oscillation v1, $\Delta t$ values must be $\{0.25148, 0.12574, 0.062871, 0.031435, 0.015718\}$.
* For KG Energy Oscillation v1, seeds per band must be 2.
* For KG Energy Oscillation v1, bands must be $[1,8],[9,24],[25,48]$.
* For KG Energy Oscillation v1, use periodic Boundary Conditions (BC).
* For KG Energy Oscillation v1, use spectral operators.
* For KG Energy Oscillation v1, use deterministic FFT plans.
* For KG Energy Oscillation v1, use fixed seeds.
* For KG Energy Oscillation v1, record checkpoints at steps [0,64,128,256,512].
* For KG J-only Locality and Dispersion, $N$ must be 256.
* For KG J-only Locality and Dispersion, $\Delta x$ must be 1.
* For KG J-only Locality and Dispersion, use periodic Boundary Conditions (BC).
* For KG J-only Locality and Dispersion, parameter $c$ must be 1.0.
* For KG J-only Locality and Dispersion, parameter $m$ must be 0.5.
* For KG J-only Locality and Dispersion, use fixed RNG seeds.
* For KG J-only Locality and Dispersion, `seed_scale` must be 0.05.
* For KG Noether Invariants, Energy drift $\max \Delta E$ must be $\le 10^{-12}$ OR $\max \Delta E \le 10\,\epsilon\sqrt{N}$.
* For KG Noether Invariants, Momentum drift $\max \Delta P$ must be $\le 10^{-12}$ OR $\max \Delta P \le 10\,\epsilon\sqrt{N}$.
* For KG Noether Invariants, Reversibility $\|\Delta\|_{\infty}$ must be $\le 10^{-10}$.
* For KG Noether Invariants, $N$ must be 256.
* For KG Noether Invariants, Machine epsilon for float64 is $\approx 2.22\times10^{-16}$.
* For KG Noether Invariants, Grid $\Delta x$ must be 1.0.
* For KG Noether Invariants, Parameter $c$ must be 1.
* For KG Noether Invariants, Parameter $m$ must be 1.
* For KG Noether Invariants, $\Delta t$ must be 0.005.
* For KG Noether Invariants, perform 512 Störmer–Verlet steps for integration.
* For KG Noether Invariants, `seed_scale` must be 0.05.
* For KG⊕RD Metriplectic QC, use a fixed grid.
* For KG⊕RD Metriplectic QC, use a $\Delta t$ sweep.
* For KG⊕RD Metriplectic QC, Time step $\Delta t$ must be chosen from {0.04, 0.02, 0.01, 0.005}.
* For KG⊕RD Metriplectic QC, Small-$\Delta t$ set for diagnostics must be {0.02, 0.01, 0.005, 0.0025}.
* For KG⊕RD Metriplectic QC, Grid $N$ must be 256.
* For KG⊕RD Metriplectic QC, Grid $\Delta x$ must be 1.
* For KG⊕RD Metriplectic QC, use 10 seeds.
* For KG⊕RD Metriplectic QC, `seed_scale` must be 0.05.
* For KG⊕RD Metriplectic QC, Parameter $c$ must be 1.0.
* For KG⊕RD Metriplectic QC, Parameter $m$ must be 0.5.
* For KG⊕RD Metriplectic QC, Parameter $D$ must be 1.0.
* For KG⊕RD Metriplectic QC, Parameter $r$ must be 0.2.
* For KG⊕RD Metriplectic QC, Parameter $u$ must be 0.25.
* For KG⊕RD Metriplectic QC, `m_lap_operator` must be "spectral".
* For KG⊕RD Metriplectic QC, DG tolerance must be $10^{-12}$.
* For KG⊕RD Metriplectic QC, primary composition must be JMJ.
* For KG⊕RD Metriplectic QC, diagnostic composition must be MJM.
* For Metriplectic Integrator JMJ RD, Time step $\Delta t$ must be chosen from $\{0.02, 0.01, 0.005, 0.0025, 0.00125\}$.
* For Metriplectic Integrator JMJ RD, Grid $N$ must be 256.
* For Metriplectic Integrator JMJ RD, Grid $\Delta x$ must be 1.
* For Metriplectic Integrator JMJ RD, use seeds $0\ldots 9$ for ensemble medians.
* For Metriplectic Integrator JMJ RD, use periodic Boundary Conditions (BC).
* For Metriplectic Integrator JMJ RD, Parameter $D$ must be 1.0.
* For Metriplectic Integrator JMJ RD, Parameter $r$ must be 0.2.
* For Metriplectic Integrator JMJ RD, Parameter $u$ must be 0.25.
* For Metriplectic Integrator JMJ RD, Seed amplitude scale must be 0.05.
* For Metriplectic Integrator JMJ RD, Tolerance for reversibility check must be $10^{-7}$.
* For Metriplectic Integrator JMJ RD, Tolerance for $L^2$ drift check must be $2\times10^{-8}$.
* For Metriplectic Structure Checks, Default number of draws must be 100.
* For Metriplectic Structure Checks, Tolerance for `neg_count` must be $10^{-12}$.
* For A6 Scaling Collapse, use three curves with $\Theta\in\{1.5,2.5,3.5\}$.
* For A6 Scaling Collapse, use 25 points over $\Delta m\in[-2,2]$ for each curve.
* For A6 Scaling Collapse, use 4000 trials per point.
* For RD Discrete Conservation, Grid size $N$ must be fixed.
* For RD Discrete Conservation, Domain length $L$ must be fixed.
* For RD Discrete Conservation, $\Delta x$ must be $L/N$.
* For RD Discrete Conservation, Final time $T$ must be fixed.
* For RD Discrete Conservation, Diffusion $D$ must be fixed.
* For RD Discrete Conservation, Reaction rate $r$ must be fixed.
* For RD Discrete Conservation, Random seed must be varied across trials and reported.
* For RD Discrete Conservation, Boundary condition must be periodic.

## **Metrics & Gates**

* **Passive Thermodynamic Routing v2**
  * H-theorem monotonicity must be enforced for the metric step in the smoke gate set.
  * No-switch identity must be enforced in the smoke gate set.
  * The discrete gradient (DG) integrator must ensure $\Delta L_h \le 0$.
  * H-theorem violations must be 0.
  * Maximum positive $\Delta L_h$ must be 0.0.
  * No-switch identity must have 40 checkpoints.
  * No-switch identity status must be 'ok = true'.
  * Reinstate RJ gate with $R^2 \ge 0.99$.
* **Tachyonic Tube v1**
  * `cov_phys` must be $\ge 0.95$ for pass.
  * `finite_fraction` must be $\ge 0.80$.
  * `R_star` must be an interior minimum.
  * `a` (quadratic coefficient) must be $>0$.
  * Consider adding a residual tolerance (e.g., $\max|f|\le 10^{-10}$) in v2.
* **Wave Flux Meter A-Phase**
  * $E_{\text{rel, max}}$ must be $\le \text{tol}_E$.
  * $\text{tol}_E$ must be calculated as $C_E\,(\Delta t/a)^2$ with $C_E=200$ and $a=L_x/N_x$.
  * $\max\,\|r\|_2$ must be $\le \text{tol}_B$.
  * $\text{tol}_B$ must be calculated as $C_B\,a^2 + C_D\,(\Delta t/a)^2$ with $C_B=3$ and $C_D=20$.
* **Wave Flux Meter Phase B (Open Ports) v1**
  * Power balance $R^2$ must be $\ge 0.9995$.
  * Relative imbalance $\langle|\mathrm{dE}/\mathrm{dt} + P_{\mathrm{out}}|\rangle / \langle|P_{\mathrm{out}}|\rangle$ must be $\le 0.5\%$.
  * Absorber efficiency $E_{\text{diss\_abs}} / \int P_{\text{out}} dt$ must be $\ge 0.9$.
  * Symmetry sanity metric is applicable only when $\mu$ and ports are symmetric.
  * Re-test gates after implementing changes for $\mu$-weighted dynamics.
  * For Phase C, include a preset effect-size gate and Confidence Interval (CI).
* **Decoherence Portals**
  * Fisher consistency relative error must be $\le 10\%$.
  * Noise budget residuals must be within spec.
* **FRW Continuity Residual - Quality Check (v1)**
  * $\mathrm{RMS}_{\mathrm{FRW}}$ must be $\le 10^{-6}$.
  * $\mathrm{RMS}_{\mathrm{FRW}}$ must be dimensionless after normalization for gate comparison.
* **KG Energy Oscillation Scaling and Time-Reversal (QC)**
  * Fit slope $p$ must be in $[1.95,2.05]$.
  * $R^2$ must be $\ge 0.999$.
  * Relative amplitude $(A_H/\bar H)$ at smallest $\Delta t$ must be $\le 10^{-4}$.
  * Time-reversal error $e_{\mathrm{rev}}$ must be $\le 10^{-12}$.
* **KG J-only Validations - Dispersion and Locality**
  * $\omega^2$ vs $k^2$ regression slope must be approximately $c^2$.
  * $\omega^2$ vs $k^2$ regression intercept must be approximately $m^2$.
  * $\omega^2$ vs $k^2$ regression $R^2$ must be $\ge 0.999$.
  * Fitted front speed $v$ must be $\le c(1+\epsilon)$.
  * $\epsilon$ for light-cone gate must be $0.02$.
* **KG Noether Invariants - Discrete Energy & Momentum Conservation**
  * Energy drift $\max \Delta E$ must be $\le 10^{-12}$ OR $\max \Delta E \le 10\,\epsilon\sqrt{N}$.
  * Momentum drift $\max \Delta P$ must be $\le 10^{-12}$ OR $\max \Delta P \le 10\,\epsilon\sqrt{N}$.
  * Reversibility $\|\Delta\|_{\infty}$ must be $\le 10^{-10}$.
* **KG⊕RD Metriplectic QC - Spectral‑DG Primary Profile**
  * $\Delta L \le 0$ must be enforced for M and JMJ steps.
  * Identity residuals for M and JMJ steps must be $\le 10^{-12}$.
  * Two-grid slope must be $\ge 2.90$ for Strang composition.
  * $R^2$ must be $\ge 0.999$ for Strang composition.
  * Defect slope must be near 3 for Strang composition.
  * J-step reversibility must be $\le 10^{-12}$.
  * J-step energy drift must be $\le 10^{-12}$ (strict).
  * Enforce $\Delta L \le 0$.
  * Enforce identity residuals $\le 10^{-12}$.
  * Enforce slope $\ge 2.90$ with $R^2 \ge 0.999$.
  * Enforce reversibility $\le 10^{-12}$.
* **Metriplectic Integrator: Symplectic J-Step Composed with Discrete-Gradient M-Step**
  * Two-grid slope $p$ for Strang order must be $\gtrsim 2$ with high $R^2$.
  * $\|W_2-W_0\|_\infty$ must be small after $+\Delta t$ then $-\Delta t$.
  * $L^2$ drift must be near machine precision.
  * $\Delta L_h$ must be $\le 0$ per step.
  * Slope must be $\ge 2.90$.
  * $R^2$ must be $\ge 0.999$.
  * Confirm non-positivity of $\Delta L_h$ (violations = 0).
  * JMJ (stencil-DG baseline) expected slope must be $\ge 2.90$.
  * JMJ (spectral-DG option) expected slope must be $\ge 3.00$.
  * M-only expected slope must be $\ge 2.90$.
  * Keep J-only reversibility and $L^2$ drift gates.
* **Metriplectic Structure Checks - J Skew and M PSD**
  * Median $|\langle v, J v\rangle|$ over random draws must be $\le 10^{-12}$.
  * Count of negative $\langle u, M u\rangle$ must be 0 across draws.
  * `neg_count` must be 0.
* **A6 Scaling Collapse - Junction Logistic Universality (v1)**
  * $\mathrm{env\_max}$ must be $\le 0.02$.
  * Quantify scaling collapse by $\mathrm{env\_max}=\max_X \{Y_{\max}(X)-Y_{\min}(X)\}$.
* **RD Discrete Conservation vs Balance**
  * Euler fit slope $\hat\beta$ must be $\approx 2.000$ with $R^2 \approx 1.000000000$.
  * Strang fit slope $\hat\beta$ must be $2.9436$ with $R^2 = 0.99997$.
  * DG RD fit slope $\hat\beta$ must be $2.9422$ with $R^2 = 0.99997$.

## **Procedure & Workflow**

* Ensure $\Delta L_h \le 0$ at every step.
* The no-switch identity must use bitwise comparison at checkpoints.
* The no-switch identity must use SHA-256 of field buffers.
* Ensure bitwise no-switch identity (40/40 checkpoints identical).
* Record checkpoint hashes.
* Ensure deterministic execution under the documented environment (threads, BLAS, FFT plan mode).
* Emit a `CONTRADICTION_REPORT` with gate, threshold, seed, and artifact IDs upon any future gate failure.
* Add injection-site sweep trend as a robustness gate.
* Add two-source split invariance as a robustness gate.
* Report Confidence Intervals (CIs) and whiteness diagnostics.
* Produce full prereg RESULTS with contradiction handling upon gate failure.
* Update canonical registries after acceptance.
* Codify $\mathrm{cov}_{\rm phys}$ as primary KPI in schema/specs.
* Artifacts must be written via `io_paths`.
* Tags must be pre-registered.
* Use quarantine paths automatically if unapproved.
* Validate that the discrete continuity relation holds to high accuracy on an open interior rectangle with ports.
* Validate that the absorber removes outflowing energy efficiently.
* Use face-based flux for power calculation.
* Use $\mu$ map to find corridor-aligned port segments.
* Use uniform face-$\mu$ dynamics (`use_mu_weighting=false`).
* Use discrete bookkeeping with face-based fluxes aligned with energy accounting on the interior rectangle.
* Disable $\mu$-weighted dynamics at this grid resolution (256x128).
* If using $\mu$-weighted dynamics, re-test gates after implementing changes.
* Draft preregistration for Phase C under approvals policy.
* Load or generate a small benchmark with 1-4 bins (CSV).
* Compare relative error $|\hat\epsilon-\epsilon_\text{true}|/\epsilon_\text{true}$ to the 10% gate.
* For noise budget, compute residuals against modeled noise components.
* Check noise budget residuals against spec.
* For FRW Continuity Residual, use central differences for numerical differentiation.
* For FRW Continuity Residual, if gate fails, route artifacts to `failed_runs/`.
* For FRW Continuity Residual, if gate fails, emit a contradiction report.
* For FRW Continuity Residual, introduce source terms.
* For FRW Continuity Residual, verify residuals remain within a tightened tolerance derived from analytic expectations or manufactured solutions.
* Calculate discrete $\omega\_\max$ from actual spatial operator $\omega_k^2 = m^2 + c^2\,\lambda_k$.
* Set $\Delta t\_\max = 0.8/\omega\_\max$.
* Log checkpoint buffer hashes in JSON sidecar.
* Use approval-gated tag KG-energy-osc-v1.
* Perform JSON schema validation.
* Log results to DB.
* Produce artifacts PNG/CSV/JSON with common IO helper.
* Run KG-noether-v1 as a cross-check on this grid.
* Proceed to Passive Thermodynamic Routing v2 with strict gates.
* Log determinism receipts (checkpoint buffer hashes) for identity audits.
* Report fit $R^2$ for light-cone gate.
* Run short windows to estimate $\omega$ for dispersion.
* Sweep a small set of $k$ for dispersion.
* Fit $\omega^2$ vs $k^2$ for dispersion.
* Log dispersion fit (slope/intercept/$R^2$).
* Threshold on $|\phi|$ to measure radius $R(t)$ over steps for light cone.
* Fit $R(t)$ vs $t$ for speed for light cone.
* Log light cone slope and $R^2$.
* Stamp unapproved runs with `{ engineering_only:true, quarantined:true }`.
* Route artifacts from unapproved runs under `failed_runs/`.
* Rerun with approved tags to remove quarantine routing.
* Pin final paths.
* Initialize random initial field & momentum with small amplitude (seed_scale=0.05).
* Capture metrics for $E_d$ and $P_d$ midpoints every step.
* Record per-step absolute drift.
* Integrate forward 512 steps for reversibility test.
* Integrate backward 512 steps (dt → −dt) for reversibility test.
* Measure sup-norm difference for reversibility test.
* Approve manifest using script-scoped HMAC.
* Monitor whether dissipative channel perturbations preserve Poisson part invariants within expected interaction corrections for Coupled KG⊕RD.
* Pair all claims with equations and/or gates and artifacts.
* Measure two-grid residual E(Δt) using L2 norm of state difference.
* Perform linear regression on log E vs. log Δt to get slope.
* Measure KG energy drift per step $\Delta H$.
* Measure reversibility error in max-norm.
* Use spectral gradient for J-step (KG).
* Use Störmer-Verlet on ($\phi$, $\pi$) for J-step (KG).
* Use periodic BCs for J-step (KG).
* Use discrete-gradient (AVF) for M-step (RD).
* Use spectral Laplacian for M-step (RD).
* Use JMJ as primary composition.
* Use MJM as defect diagnostic composition.
* Generate periodic Initial Conditions (ICs) for ($\phi$, $\pi$) using seeded noise (seed_scale = 0.05).
* Fix grid, parameters, and tolerances.
* Route failures under `failed_runs/`.
* Log FFT round-off sensitivity.
* Document and log round-off rationale (FFT).
* Monitor $\Delta L_h$ over 20 steps.
* At fixed $\Delta t=0.005$, compute an entropy-like functional $S(W)=\sum_i Q(W_i)\,\Delta x$.
* Use CAS-derived $Q'(W)=a_0+a_1 W + a_2 W^2$.
* Plot $|\Delta S|$ histograms for j_only, m_only, jmj with log-scaled x-axes.
* Document algebraic structure tests for metriplectic system.
* Document skew-symmetry of canonical J operator.
* Document Positive Semidefiniteness (PSD) of metric operator M on RD channel.
* Extend M operator check blockwise for coupled KG⊕RD states to confirm block-PSD.
* Re-evaluate $\mathrm{env\_max}$ if router mechanics or discretization scheme changes.
* Fix trials per curve (e.g., 4000) for scaling collapse.
* If a gate fails, route artifacts to `failed_runs/`.
* If a gate fails, produce a contradiction report.
* Evaluate effect of $\Delta t$ on two-grid global error $E_\infty$.
* Evaluate if any stepper conserves a nonlinear global invariant $S[W]$ exactly at one step under periodic boundary conditions.
* Compute measurements numerically in Python (double precision).
* Fit $\log E_\infty$ vs $\log \Delta t$ to obtain slope $\beta$ and $R^2$.
* For Obj-A balance, build candidate $S=\sum_i Q(W_i)\,\Delta x$.
* Use CAS-like linear system over a basis $Q'(W)$ up to quadratic with antisymmetric polynomial flux.
* Evaluate fixed-step $|\Delta S|$ distribution at a common $\Delta t$ across schemes.
* For DG RD, monitor discrete Lyapunov decrement $\Delta L$ each step.
* For DG RD, monitor DG identity residuals each step.
* Confirm $\Delta L\le 0$.
* Confirm residuals near machine precision.
* Verify diffusion-only mass conservation.
* Verify reaction-only order via RK4 two-grid convergence.

## **Syntax & Output**

* Policy for this run must be approved=true.
* Policy for this run must be quarantined=false.
* The run must be approved.
* The run must not be quarantined.
* `approved` must be `true`.
* `quarantined` must be `false`.
* Solvers must produce standards-compliant artifacts (PNG/CSV/JSON).
* Solvers must produce artifacts that are fully reproducible from the repository.
* Produce PNG + CSV + JSON sidecars via `common/io_paths.py`.
* Adhere to approvals/quarantine policy for IO.
* Units of $\mathrm{RMS}_{\mathrm{FRW}}$ are energy density times volume per unit time.
* $\mathrm{RMS}_{\mathrm{FRW}}$ must be dimensionless after normalization for gate comparison.
* Measurement must use a synthetic analytic series sampled uniformly in time.
* Pin figure/CSV/log artifacts.
* CSV must provide full time series of residuals.
* Log checkpoint buffer hashes in JSON sidecar.
* Log checkpoint hashes at fixed checkpoints (0, 64, 128, 256, 512).
* Perform JSON schema validation.
* Log results to DB.
* Each figure must have CSV/JSON sidecars with the same basename.
* Artifacts must be stored under `Derivation/code/outputs/{figures,logs}/metriplectic`.
* Artifacts must be tagged `kgRD‑v1`.
* Rule: Log fit (slope/intercept/$R^2$) for dispersion.
* Rule: Log slope and $R^2$ for light cone.
* For KG Noether Invariants, capture metrics for $E_d$ and $P_d$ midpoints every step.
* For KG Noether Invariants, record per-step absolute drift.
* For Metriplectic Integrator JMJ RD, use regression slope on log-log fits from seed-median two-grid errors for measurement.
* For Metriplectic Integrator JMJ RD, use per-step $\Delta L_h$ from the DG-defined Lyapunov functional for measurement.
* For Metriplectic Integrator JMJ RD, compute two-grid errors for M-only and JMJ for each $\Delta t$ and seed.
* For Metriplectic Integrator JMJ RD, aggregate median across seeds.
* For Metriplectic Integrator JMJ RD, fit a line in log-log space to obtain slope and $R^2$.
* For Metriplectic Integrator JMJ RD, monitor $\Delta L_h$ over 20 steps.
* For Metriplectic Integrator JMJ RD, at fixed $\Delta t=0.005$, compute an entropy-like functional $S(W)=\sum_i Q(W_i)\,\Delta x$.
* For Metriplectic Integrator JMJ RD, use CAS-derived $Q'(W)=a_0+a_1 W + a_2 W^2$.
* For Metriplectic Integrator JMJ RD, plot $|\Delta S|$ histograms for j_only, m_only, jmj with log-scaled x-axes.
* Specify grid (N, $\Delta x$), parameters (D, c, m, m_lap_operator), and number of draws for Metriplectic Structure Checks.
* Route PNGs under `figures/` for RD Discrete Conservation.
* Route CSV/JSON under `logs/` for RD Discrete Conservation.
* For RD Discrete Conservation, log results (CSV/JSON).
* All artifacts must follow the pairing policy (figure + CSV/JSON).
* At least one artifact path must be pinned in text for reproducibility.

## **Security & Compliance**

* Commercial use of this research requires citation.
* Commercial use of this research requires written permission from Justin K. Lietz.
* For KG Noether Invariants, use pre-registered tag `KG-noether-v1`.
* For KG Noether Invariants, manifest for `KG-noether-v1` must be `Derivation/code/physics/metriplectic/APPROVAL.json`.
* For KG Noether Invariants, schema for `KG-noether-v1` must be `Derivation/code/physics/metriplectic/schemas/KG-noether-v1.schema.json`.
* For KG Noether Invariants, proposal for `KG-noether-v1` must be `Derivation/Metriplectic/PROPOSAL_Metriplectic_SymplecticPlusDG.md`.
* For KG Noether Invariants, Approval Key (HMAC) must match DB secret with message `metriplectic:kg_noether:KG-noether-v1`.

## **Software/Tools**

* For Tachyonic Tube v1, Python environment must conform to `requirements.txt`.
* For Decoherence Portals, use `run_dp_fisher_check.py` for Fisher estimation.
* For Decoherence Portals, use `run_dp_noise_budget.py` for noise budget.
* For FRW Continuity Residual, use `Derivation/code/physics/cosmology/run_frw_balance.py` as runner.
* For KG Noether Invariants, use `Derivation/code/physics/metriplectic/kg_noether.py` as runner.
* For Metriplectic Structure Checks, use `Derivation/code/physics/metriplectic/metriplectic_structure_checks.py` as runner.
* For Metriplectic Structure Checks, use `Derivation/code/common/io_paths.py` for IO.
* For RD Discrete Conservation, use `run_rd_conservation.py` as custom harness.
* For RD Discrete Conservation, use `io_paths.py` for artifact routing.
* For RD Discrete Conservation, use `Derivation/code/physics/rd_conservation/run_rd_conservation.py`.
* For RD Discrete Conservation, use `Derivation/code/physics/reaction_diffusion/reaction_exact.py`.
* For RD Discrete Conservation, use `Derivation/code/common/io_paths.py`.

## Key Highlights

* The core numerical strategy involves composing a metriplectic integrator by pairing a symplectic J-step with a discrete-gradient (DG) M-step.
* The design explicitly targets discrete Noether invariants for the conservative sector and exact entropy monotonicity for the dissipative sector.
* Critical validation gates enforce H-theorem monotonicity for the metric step and bitwise no-switch identity across checkpoints.
* All computations must use IEEE-754 double precision, with execution strictly deterministic and verifiable through recorded checkpoint hashes.
* Upon any gate failure, a `CONTRADICTION_REPORT` must be emitted, and artifacts routed to `failed_runs/` with full preregistration results.
* For new mixed-model experiments, the spectral-DG option is preferred to minimize J-M mismatch, while the stencil baseline remains available for ablations.
* Metriplectic structure must be rigorously verified by confirming skew-symmetry of the canonical J operator and positive semi-definiteness of the M operator.
* Commercial use of this research requires both citation and written permission from Justin K. Lietz.
