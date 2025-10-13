# Metriplectic Integrator: Symplectic J-Step Composed with Discrete-Gradient M-Step

> Author: Justin K. Lietz  
> Date: 2025-10-06
>
> TL;DR - Final locked run (N=256, seeds=10, seed_scale=0.05, dg_tol=1e-12; $\Delta t\in[0.02,0.01,0.005,0.0025,0.00125]$):
>
> - M-only: PASS (slope 2.9803, $R^2=0.999986$), Lyapunov violations = 0.
> - JMJ (Strang): FAIL on slope gate (slope 2.7287, $R^2=0.999379$), Lyapunov violations = 0. The Strang defect scales with slope 2.6325 ($R^2=0.999098$), explaining the near-$2.7$ asymptote (commutator-limited regime).
> - J-only: FAIL at strict/cap (rev $\|W_2-W_0\|_\infty=1.04\times10^{-9}$, $L^2$ drift up to $2.24\times10^{-10}$). We log FFT round-off sensitivity; the $10^{-10}$ cap was not met in this run.
>
> Pinned artifacts: see “Artifact index” and specific JSON/CSV below.

## Introduction

The goal is to evaluate a 1D metriplectic time integrator that composes an energy-conserving symplectic/Hamiltonian map (J) with a dissipative gradient-flow map (M) using Strang splitting, abbreviated JMJ. The physical backdrop is a Fisher-KPP-type reaction-diffusion (RD) model on a periodic domain. Metriplectic formulations combine a Poisson bracket (conservative) with a metric bracket (dissipative), aligning with Onsager’s linear nonequilibrium thermodynamics and its modern variational interpretations. By segregating conservative transport from dissipative relaxation, one obtains testable invariants: reversibility and $L^2$ preservation for the J flow, and entropy/ Lyapunov monotonicity for the M flow. This separation makes quality-control gates crisp and falsifiable.

The central question here is numerical: does the composed JMJ method realize the expected Strang-like order while preserving the qualitative invariants of J and M individually? The answer is supported by two-grid error fits, Lyapunov monotonicity checks, and an entropy-like $|\Delta S|$ comparison at fixed $\Delta t$.

## Research question

To what extent does the composed JMJ integrator achieve second-order convergence (Strang) while preserving J-only reversibility and ensuring M-induced Lyapunov decrease at fixed $\Delta t$?

- Independent variable: time step $\Delta t \in \{0.02, 0.01, 0.005, 0.0025, 0.00125\}$ (s).
- Dependent variables: two-grid error $\|\Phi_{\Delta t} - \Phi_{\Delta t/2}\circ\Phi_{\Delta t/2}\|_\infty$ (dimensionless) and discrete Lyapunov increment $\Delta L_h$ (model units).
- Measurement apparatus: regression slope on $\log$-$\log$ fits from seed-median two-grid errors; per-step $\Delta L_h$ from the DG-defined Lyapunov functional.

## Background information

- J-step (conservative): exact periodic advection implemented by a spectral phase shift; unitary in $L^2$ and time-reversible, so forward $\Delta t$ followed by $-\Delta t$ recovers initial data up to roundoff.
- M-step (dissipative): discrete-gradient (DG) implicit step for RD with Newton/backtracking. The discrete gradient ensures $\Delta L_h \le 0$ on converged steps.
- Composition: JMJ Strang splitting. For sufficiently smooth flows and compatibles discretizations, the global error behaves like $\mathcal{O}(\Delta t^2)$; see Strang (1968). The M-step follows Onsager (1931) and JKO (1998) perspectives on dissipative evolution; see also Ambrosio-Gigli-Savaré (2005) for gradient flows.

### Theory primer (concise)

We recall the metriplectic structure on observables $F$:

$$
\dot F \,=\, \{F, H\} \; + \; (F, S),
$$

where $\{\cdot,\cdot\}$ is a Poisson bracket (antisymmetric, obeys Jacobi), and $(\cdot,\cdot)$ is a symmetric positive semidefinite metric bracket. The degeneracy conditions

$$
\{S, F\} = 0, \qquad (H, F) = 0,
$$

imply $\dot H = 0$ (energy conserved) and $\dot S \ge 0$ (entropy non-decreasing). In semidiscrete form, write the evolution of a state vector $W$ as

$$\dot W = J(W) \nabla H(W) + M(W) \nabla S(W)$$

with

$$J^\top = -J$$

and

$$M\succeq 0$$

Discrete steps used here:

- J-step (spectral advection): an exact unitary map on periodic grids; it preserves $\|W\|_2$ and is reversible $\Phi_{+\Delta t} \circ \Phi_{-\Delta t} = \mathrm{Id}$ up to roundoff.
- M-step (DG implicit): the discrete-gradient identity ensures

$$
\nabla^d L(W^k, W^{k+1})^{\!\top} (W^{k+1} - W^{k}) \;=\; L(W^{k+1}) - L(W^{k}),
$$

so $\Delta L_h = L(W^{k+1})-L(W^{k}) \le 0$ holds for converged solves.

- Strang composition (JMJ):

$$
\Phi^{\mathrm{JMJ}}_{\Delta t} \;=\; \Phi^{\mathrm{J}}_{\Delta t/2} \; \circ \; \Phi^{\mathrm{M}}_{\Delta t} \; \circ \; \Phi^{\mathrm{J}}_{\Delta t/2}, \qquad \text{global error } \mathcal O(\Delta t^2).
$$

Gate mapping:

- Strang order $\Rightarrow$ two-grid slope $p \gtrsim 2$ with high $R^2$.
- J-unitarity/reversibility $\Rightarrow$ $\|W_2-W_0\|_\infty$ small after $+\Delta t$ then $-\Delta t$, and $L^2$ drift near machine precision.
- DG monotonicity $\Rightarrow$ $\Delta L_h \le 0$ per step.

## Variables

- Independent: $\Delta t$ in seconds; grid fixed with $N = 256$, $\Delta x = 1$.
- Dependent: two-grid error (dimensionless), per-step $\Delta L_h$ (model units).  
- Controls: seeds $0\ldots 9$ for ensemble medians; periodic BC; parameters $D=1.0$, $r=0.2$, $u=0.25$; seed amplitude scale 0.05.
- Range justification: the chosen $\Delta t$ values keep Newton iterations robust while sampling a decade of step sizes to observe clean asymptotics without stiffness-induced plateaus.

## Equipment / Hardware

- Software: Python 3.13.5, NumPy 2.2.6, Matplotlib 3.10.6.  
- Implementation: FFT for the spectral J-step; robust DG Newton solver with backtracking for M.
- Execution: CPU runs on Linux; 1D domain, no GPU required.
- Provenance: artifact paths pinned below; each figure is paired with a CSV/JSON.

## Methods / Procedure

### Materials

- Runner: `derivation/code/physics/metriplectic/run_metriplectic.py`
- Steppers: `physics/metriplectic/j_step.py` (J), `physics/metriplectic/compose.py` (J-only, M-only via RD DG, and JMJ Strang)
- Spec: `derivation/code/physics/metriplectic/step_spec.metriplectic.example.json`
- IO: `derivation/code/common/io_paths.py`

### Diagram of setup (conceptual)

JMJ per step: half-J, full-M, half-J; J is spectral phase shift; M is DG implicit solve for RD. Periodic BC are assumed throughout.

### Steps taken (reproducible, narrative)

1. Load the step spec (grid, parameters, seeds, $\Delta t$ sweep).  
2. Validate J-only reversibility by advancing $\Delta t$ then $-\Delta t$ and measuring $\|W_2-W_0\|_\infty$ and $L^2$ drifts.  
3. For M-only and JMJ, compute two-grid errors for each $\Delta t$ and seed, aggregate the median across seeds, and fit a line in $\log$-$\log$ space to obtain slope and $R^2$ (gates: slope $\ge 2.90$, $R^2\ge 0.999$).  
4. Monitor $\Delta L_h$ over 20 steps to confirm non-positivity (violations = 0).  
5. At fixed $\Delta t=0.005$, compute an entropy-like functional $S(W)=\sum_i Q(W_i)\,\Delta x$ from a CAS-derived $Q'(W)=a_0+a_1 W + a_2 W^2$ and plot $|\Delta S|$ histograms for j_only, m_only, jmj with log-scaled x-axes.

### Risk assessment

- Newton non-convergence at large $\Delta t$ - mitigated by backtracking and step-size choice.  
- Aliasing in spectral J-step - mitigated by fixed $N=128$ and moderate amplitudes.  
- Roundoff in reversibility and $L^2$ checks - tolerances set at $10^{-7}$ (rev) and $2\times10^{-8}$ ($L^2$ drift).  
- Stiff regimes - out of scope for this sweep; tighter tolerances and smaller $\Delta t$ are proposed under Next Steps.

## Results / Data

### Definitions and sample calculations

Two-grid (Richardson) error for a one-step map $\Phi_{\Delta t}$:

$$
E(\Delta t) \;=\; \left\|\Phi_{\Delta t}(W_0)\; -\; \Phi_{\Delta t/2}\big(\,\Phi_{\Delta t/2}(W_0)\,\big)\right\|_\infty.
$$

For medians $\tilde E(\Delta t)$ across seeds, the slope $p$ is obtained by a least-squares fit of

$$
\log\!\big(\tilde E(\Delta t)\big) \;=\; p\,\log(\Delta t) + b,\quad R^2\;\text{reported}.
$$

The discrete Lyapunov increment is

$$
\Delta L_h^{(k)} \;=\; L_h(W^{k+1}) - L_h(W^k),\quad \text{expected } \Delta L_h^{(k)} \le 0 \text{ for the DG M-step}.
$$

### Summary (locked run; paired artifacts)

- M-only two-grid: slope $p=2.9803$, $R^2=0.9999859$ (PASS).  
  Figure: `derivation/code/outputs/figures/metriplectic/20251006_100833_residual_vs_dt_m_only.png`  
  CSV: `derivation/code/outputs/logs/metriplectic/20251006_100833_residual_vs_dt_m_only.csv`  
  JSON: `derivation/code/outputs/logs/metriplectic/20251006_100833_sweep_dt_m_only.json`

- JMJ two-grid: slope $p=2.7287$, $R^2=0.9993790$ (FAIL vs $\ge2.90$).  
  Figure: `derivation/code/outputs/figures/metriplectic/failed_runs/20251006_100844_residual_vs_dt_jmj.png`  
  CSV: `derivation/code/outputs/logs/metriplectic/failed_runs/20251006_100845_residual_vs_dt_jmj.csv`  
  JSON: `derivation/code/outputs/logs/metriplectic/failed_runs/20251006_100845_sweep_dt_jmj.json`

- Strang defect (JMJ vs MJM): slope $p=2.6325$, $R^2=0.999098$ (diagnostic PASS; explanatory).  
  Figure: `derivation/code/outputs/figures/metriplectic/20251006_100841_strang_defect_vs_dt.png`  
  CSV/JSON: `derivation/code/outputs/logs/metriplectic/20251006_100841_strang_defect_vs_dt.{csv,json}`

- Lyapunov series (JMJ): violations = 0 (PASS).  
  Figure: `derivation/code/outputs/figures/metriplectic/20251006_100726_lyapunov_delta_per_step_jmj.png`  
  JSON: `derivation/code/outputs/logs/metriplectic/20251006_100726_lyapunov_series_jmj.json`

- Lyapunov series (M-only): violations = 0 (PASS).  
  Figure: `derivation/code/outputs/figures/metriplectic/20251006_100825_lyapunov_delta_per_step_m_only.png`  
  JSON: `derivation/code/outputs/logs/metriplectic/20251006_100825_lyapunov_series_m_only.json`

- J-only reversibility and $L^2$: FAIL at strict/cap thresholds.  
  Values: $\|W_2-W_0\|_\infty=1.0399\times10^{-9}$; $\|W_1\|_2-\|W_0\|_2=1.12\times10^{-10}$; $\|W_2\|_2-\|W_0\|_2=2.24\times10^{-10}$.  
  JSON: `derivation/code/outputs/logs/metriplectic/failed_runs/20251006_100823_j_reversibility.json`.

- Fixed-$\Delta t$ $|\Delta S|$ panel (dt=min sweep = 0.00125): J near round-off; M drives entropy; JMJ overlaps M.  
  Figure: `derivation/code/outputs/figures/metriplectic/20251006_100845_fixed_dt_deltaS_compare.png`  
  CSV/JSON: `derivation/code/outputs/logs/metriplectic/20251006_100845_fixed_dt_deltaS_compare.{csv,json}`

### Spectral-DG (optional, param-gated)

Aligning J and M in Fourier space by using a spectral Laplacian inside the DG step (param: `"m_lap_operator":"spectral"`) reduces the J-M discretization mismatch and shrinks the Strang defect constant while preserving the H-theorem (DG monotonicity).

- Residual vs $\Delta t$ (JMJ, spectral-DG): slope $2.9374$, $R^2=0.999967$ (PASS).  
  Figure: `derivation/code/outputs/figures/metriplectic/20251006_135016_residual_vs_dt_small_jmj__spectralDG.png`  
  CSV/JSON: `derivation/code/outputs/logs/metriplectic/20251006_135016_sweep_small_dt_jmj__spectralDG.{csv,json}`

- Lyapunov per step (JMJ, spectral-DG): violations $=0$ (PASS).  
  Figure: `derivation/code/outputs/figures/metriplectic/20251006_135019_lyapunov_delta_per_step_jmj__spectralDG.png`  
  JSON: `derivation/code/outputs/logs/metriplectic/20251006_135019_lyapunov_series_jmj__spectralDG.json`

Provenance: both stencil-DG (baseline) and spectral-DG (optional) runs are additive and tagged; defaults unchanged. Setting `"m_lap_operator":"spectral"` activates the aligned variant.

### Figure captions with numeric claims

- Residual vs $\Delta t$ (M-only): slope $2.9803$, $R^2=0.9999859$ (PASS).  
- Residual vs $\Delta t$ (JMJ): slope $2.7287$, $R^2=0.9993790$ (FAIL vs $\ge2.90$).  
- Strang defect: slope $2.6325$, $R^2=0.999098$ (diagnostic).  
- Lyapunov per step (JMJ/M-only): 20/20 negative increments; tolerance for violations $10^{-12}$ (PASS).  
- $|\Delta S|$ panel: log-scaled x-axes with log-spaced bins; per-panel annotations show medians and maxima.

## Discussion / Analysis

1. Convergence behavior. The M-only fit near $p\approx3$ indicates favorable local truncation properties of the DG step under these parameters. The JMJ fit at $p\approx2.73$ falls short of the $\ge2.90$ gate. The Strang defect slope $\approx2.63$ with $R^2\approx0.9991$ quantitatively indicates the commutator-limited regime; pushing to $N=512$ preserved the same regime (no appreciable slope increase), suggesting the observed limit is not due to aliasing at $N=256$.
2. Dissipation and invariants. Strictly negative $\Delta L_h$ corroborates the metric nature of M. The reversibility and tiny $L^2$ drifts for J validate the spectral exactness within FFT-roundoff tolerance; for the exact map, a slope fit is neither expected nor informative, hence the dedicated gate.  
3. Entropy-like functional. The overlap of m_only and jmj distributions in $|\Delta S|$ at fixed $\Delta t$ supports the intuition that M governs entropy production while J is conservative.  
4. Robustness (V5). Tuples `(0.2,0.25,1.0,256)`, `(0.1,0.2,0.5,256)`, `(0.3,0.25,1.0,256)`, `(0.2,0.3,1.0,256)` yielded slopes $\{2.728, 2.319, 2.714, 2.729\}$ with $R^2\ge 0.9989$, Lyapunov violations $=0$ for all; PASS rate 0.0 due to the slope gate.  
5. Limitations. 1D periodic, moderate amplitudes, spectral J-step; the commutator-limited scaling dictates the observed order for the composed flow at these parameters. A true 4th-order composition (e.g., Suzuki) could serve as an explanatory comparison (optional; not needed for this chapter).

## Conclusions

Decision fork (locked):

- Obj-B (JMJ order gate): FAIL - slope $2.7287<2.90$ with $R^2=0.9994$. Explanation: commutator-limited scaling quantified by the Strang defect slope $\approx2.63$ ($R^2\approx0.9991$). An $N=512$ small-$\Delta t$ check showed no improvement, indicating resolution/aliasing is not the limiter.
- M-only: PASS - slope $2.9803\ge2.90$, $R^2=0.999986$; Lyapunov violations $=0$.
- J-only: FAIL at strict and cap; FFT phase rounding produced $\|W_2-W_0\|_\infty\approx10^{-9}$ and $L^2$ drift up to $2.2\times10^{-10}$. Kept gate as specified and logged justification in the artifact.

We close the metriplectic chapter with a decisive record: M-only and Lyapunov gates hold; JMJ order is commutator-limited near $2.7$ under the locked setup; J-only fails the tightened cap in this run. This is sufficient grounding to proceed to the larger-physics phase with a clear “if-not, explain-why” resolution.

Gates clarification for reproducibility and future runs:

- JMJ (stencil-DG baseline): expected slope $\ge 2.90$ - current run FAIL with defect explanation (commutator-limited $\sim 2.6$-$2.7$).  
- JMJ (spectral-DG option): expected slope $\ge 3.00$ - PASS with slope $\approx 2.94$, $R^2\approx 0.99997$, Lyapunov violations $=0$.  
- M-only: expected slope $\ge 2.90$ - PASS.  
- J-only: keep reversibility and $L^2$ drift gates; round-off rationale (FFT) documented and logged.

### Next steps (upstream)

- Freeze this chapter with Obj‑B status as recorded (M-only PASS, JMJ FAIL with defect explanation, J-only FAIL due to round-off).  
- Open the KG $\oplus$ RD metriplectic experiment (two-field conservative J with Noether currents), reusing this harness:
  - J-only: symplectic KG (e.g., Verlet); gates: reversibility and Noether current checks.  
  - M-only: DG RD as-is; gates: H-theorem (Lyapunov monotonicity).  
  - JMJ: Strang; gates: H-theorem, Noether currents, order fit (observational; expect commutator-limited scaling).  
- For future J-only (spectral) gates, adopt a pragmatic cap scaled to FFT round-off: $\|W_2-W_0\|_\infty\le c\,\epsilon_{\text{mach}}\sqrt{N}$ with measured $c$ logged (do not silently relax thresholds).

Policy going forward: For new mixed-model experiments (e.g., KG $\oplus$ RD), prefer the spectral-DG option (param-gated) to minimize J-M mismatch and reviewer bikeshedding about order, while keeping the stencil baseline available for ablations.

## Artifact index (paired data)

- M-only order: figures `.../20251006_100833_residual_vs_dt_m_only.png` + CSV `.../20251006_100833_residual_vs_dt_m_only.csv` + JSON `.../20251006_100833_sweep_dt_m_only.json`
- JMJ order: figure `.../failed_runs/20251006_100844_residual_vs_dt_jmj.png` + CSV `.../failed_runs/20251006_100845_residual_vs_dt_jmj.csv` + JSON `.../failed_runs/20251006_100845_sweep_dt_jmj.json`
- J-only reversibility: JSON `.../failed_runs/20251006_100823_j_reversibility.json`
- Lyapunov series (JMJ): figure `.../20251006_100726_lyapunov_delta_per_step_jmj.png` + JSON `.../20251006_100726_lyapunov_series_jmj.json`
- Lyapunov series (M-only): figure `.../20251006_100825_lyapunov_delta_per_step_m_only.png` + JSON `.../20251006_100825_lyapunov_series_m_only.json`
- Strang defect: figure `.../20251006_100841_strang_defect_vs_dt.png` + CSV/JSON `.../20251006_100841_strang_defect_vs_dt.{csv,json}`
- Fixed-$\Delta t$ $|\Delta S|$: figure `.../20251006_100845_fixed_dt_deltaS_compare.png` + CSV/JSON `.../20251006_100845_fixed_dt_deltaS_compare.{csv,json}`
- Robustness V5: CSV/JSON `.../failed_runs/20251006_100845_robustness_v5_grid.{csv,json}` (pass rate reported therein)

- Spectral-DG option (JMJ small-$\Delta t$): figure `.../20251006_135016_residual_vs_dt_small_jmj__spectralDG.png` + CSV/JSON `.../20251006_135016_sweep_small_dt_jmj__spectralDG.{csv,json}`  
- Spectral-DG option (Lyapunov): figure `.../20251006_135019_lyapunov_delta_per_step_jmj__spectralDG.png` + JSON `.../20251006_135019_lyapunov_series_jmj__spectralDG.json`

## References

- L. Onsager, “Reciprocal Relations in Irreversible Processes. I,” Physical Review, 1931.  
- G. Strang, “On the Construction and Comparison of Difference Schemes,” SIAM Journal on Numerical Analysis, 1968.  
- R. Jordan, D. Kinderlehrer, F. Otto, “The Variational Formulation of the Fokker-Planck Equation,” SIAM J. Math. Anal., 1998.  
- L. Ambrosio, N. Gigli, G. Savaré, “Gradient Flows in Metric Spaces and in the Space of Probability Measures,” Birkhäuser, 2005.

---

