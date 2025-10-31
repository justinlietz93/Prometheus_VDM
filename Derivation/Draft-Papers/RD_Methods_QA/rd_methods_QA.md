# VDM RD baseline: validated methods and QA invariants
Author: Justin K. Lietz
Date: 2025-08-26

Classification: RD

Overview
- Package the on-site logarithmic invariant as a QA diagnostic within a validated reaction-diffusion (RD) methods slice.
- Lead with proven RD validations (front speed, dispersion) with acceptance gates and PASS metrics.
- Provide a minimal, per-node runtime guard based on the invariant drift for use in CI/runtime.

Context (VDM): Void Dynamics (VDM) is an event-driven, sparse framework; the RD sector provides the canonical physics slice with reproducible gates. The QA invariant serves as a per-node drift diagnostic. Second‑order/EFT branches are explicitly out of scope here and quarantined to separate notes.

References (code)
- Front speed experiment: [Derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py](../../code/physics/reaction_diffusion/rd_front_speed_experiment.py)
- Dispersion experiment: [Derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py](../../code/physics/reaction_diffusion/rd_dispersion_experiment.py)
- Front speed sweep: [Derivation/code/physics/reaction_diffusion/rd_front_speed_sweep.py](../../code/physics/reaction_diffusion/rd_front_speed_sweep.py)
- Logistic invariant validation: [Derivation/code/physics/conservation_law/qfum_validate.py](../../code/physics/conservation_law/qfum_validate.py)
- IO helpers: [figure_path()](../../code/common/io_paths.py:49), [log_path()](../../code/common/io_paths.py:53), [write_log()](../../code/common/io_paths.py:57)


1. Model and acceptance gates

1.1 Fisher-KPP baseline
The scalar RD model is the Fisher-KPP equation

$$\partial_t u = D\,\partial_{xx} u + r\,u\,(1-u),$$

with $D>0$, $r>0$, $u\in[0,1]$. Two canonical validations are enforced:

- Front speed (pulled front), theoretical minimal speed:

$$c_{\mathrm{th}} = 2\sqrt{D\,r}.$$

Acceptance gate: coefficient of determination $R^2 \ge 0.9999$ on a robust late-time linear fit and relative error $|c_{\mathrm{meas}}-c_{\mathrm{th}}|/|c_{\mathrm{th}}| \le 5\%$.

- Linear dispersion about $u\approx 0$:

$$\sigma_c(k) = r - D k^2,\qquad \sigma_d(m) = r - \frac{4D}{\Delta x^2}\sin^2\!\Big(\frac{\pi m}{N}\Big).$$

Acceptance gate: median relative error across well-fitted modes $\le 1\times 10^{-1}$ and array-level $R^2 \ge 0.98$; typical observed values are much tighter.


1.2 On-site QA invariant (logistic)
The nodewise on-site ODE is logistic:

$$\dot W = r W - u W^2.$$

A first integral is

$$Q(W,t) = \ln\!\left|\frac{W}{\,r - u W\,}\right| - r t,$$

with branch domain restrictions $W\neq 0$ and $r-uW \neq 0$; for RD states within $u\in[0,1]$ and $r,u>0$, the natural branch is $W>0$, $r-uW>0$.

Drift test and gates (double precision):
- Time integrator RK4: $\,\max_t|Q(t)-Q(0)| \le 10^{-8}.$
- Convergence study over $dt$: observed order $p \approx 4 \pm 0.4$, with fit $R^2 \ge 0.98$. For Euler, $p\approx 1\pm 0.2$.

Implementations: [Q_invariant()](../../code/physics/conservation_law/qfum_validate.py:118), [fit_loglog()](../../code/physics/conservation_law/qfum_validate.py:153), [plot_Q_drift()](../../code/physics/conservation_law/qfum_validate.py:179).


2. Proven RD validations (PASS)

2.1 Front speed
- Figure: [Derivation/code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.png](../../code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.png)
- Log: [Derivation/code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.json](../../code/outputs/logs/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.json)
- Key metrics: $c_{\mathrm{meas}}=0.9529$, $c_{\mathrm{th}}=1.0000$, $\mathrm{rel\_err}=4.71\times 10^{-2}$, $R^2=0.999996$ → PASS (within 5%, $R^2\ge 0.9999$).

Reproduce:
```
python Derivation/code/physics/reaction_diffusion/rd_front_speed_experiment.py \
  --N 1024 --L 200 --D 1.0 --r 0.25 --T 80 --cfl 0.2 --seed 42 \
  --x0 -60 --level 0.1 --fit_start 0.6 --fit_end 0.9
```

2.2 Linear dispersion
- Figure: [Derivation/code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.png](../../code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.png)
- Log: [Derivation/code/outputs/logs/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.json](../../code/outputs/logs/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.json)
- Key metrics: median rel-err $1.45\times 10^{-3}$, $R^2_{\text{array}}=0.999946$ → PASS (tight vs gates).

Reproduce:
```
python Derivation/code/physics/reaction_diffusion/rd_dispersion_experiment.py \
  --N 1024 --L 200 --D 1.0 --r 0.25 --T 10 --cfl 0.2 --seed 42 \
  --record 80 --m_max 64 --fit_start 0.1 --fit_end 0.4
```


3. QA invariant (no figures in RD packaging)
- The on-site invariant is used solely as a per-node QA drift gate in RD pipelines. Figures are intentionally omitted here.
- Acceptance (double precision RK4): $\max_t|Q(t)-Q(0)| \le 10^{-8}$ at $dt\approx 10^{-3}$; convergence slope $p\approx 4\pm 0.4$ with fit $R^2\ge 0.98$ on a $dt$ sweep.
- Use the validator to produce audit logs when needed. Numerical caveat: at extremely small step sizes, ΔQ approaches machine precision and the observed slope p from a log-log fit can degrade; evaluate gates in the truncation‑dominated regime (moderate dt). Proof and figures: see [logarithmic_constant_of_motion.md](./logarithmic_constant_of_motion.md).
```
python Derivation/code/physics/conservation_law/qfum_validate.py \
  --r 0.15 --u 0.25 --W0 0.12 0.62 --T 40 \
  --dt 0.002 0.001 0.0005 --solver rk4
```


4. Runtime/CI guard (per-node)
The following minimal guard computes $Q(W,t)$ on-the-fly and enforces the drift and (optionally) order-convergence gate. Integrate this check into any per-node update in RD codes.

Python snippet:
```python
import numpy as np, math

def Q_invariant_runtime(r, u, W, t):
    denom = r - u*W
    denom = denom if abs(denom) > 1e-16 else math.copysign(1e-16, denom)
    Ws = W if abs(W) > 1e-16 else math.copysign(1e-16, W)
    # difference-of-logs form improves numerical stability near poles
    return math.log(abs(Ws)) - math.log(abs(denom)) - r*t

class QDriftGuard:
    def __init__(self, r, u, tol=1e-8):
        self.r, self.u, self.tol = float(r), float(u), float(tol)
        self.Q0 = None
    def reset(self, W0, t0=0.0):
        self.Q0 = Q_invariant_runtime(self.r, self.u, float(W0), float(t0))
    def check(self, W, t):
        if self.Q0 is None:
            self.reset(W, t)
        Q = Q_invariant_runtime(self.r, self.u, float(W), float(t))
        return abs(Q - self.Q0) <= self.tol
```

Usage inside a time loop (schematic):
```python
guard = QDriftGuard(r=0.25, u=0.25, tol=1e-8)
guard.reset(W0, t0)
for n in range(steps):
    # ... update W -> Wn1 ...
    if not guard.check(Wn1, t0 + (n+1)*dt):
        raise RuntimeError("Q-invariant drift gate violated")
```


5. Notes on numerical details
- Robust linear fits use a simple moving-average smoothing and MAD-based outlier rejection; see [robust_linear_fit()](../../code/physics/reaction_diffusion/rd_front_speed_experiment.py:77) and [robust_linear_fit()](../../code/physics/reaction_diffusion/rd_dispersion_experiment.py:40).
- RD experiments route outputs to repo-standard locations; failed runs go to a failed_runs subfolder; see code above.
- Invariant figures and metrics are produced via repository helpers; see [figure_path()](../../code/common/io_paths.py:49) and [log_path()](../../code/common/io_paths.py:53).


6. Acceptance checklist
- Algebraic signs and units verified for $c_{\mathrm{th}}$ and $\sigma(k)$.
- Dimensional consistency: $[c]=L/T$, $[\sigma]=1/T$; $Q$ is dimensionless.
- Limits: $\sigma_c(0)=r$; $\sigma_c(k)\to -\infty$ as $k\to\infty$; $c_{\mathrm{th}}\to 0$ as $D\to 0$ or $r\to 0$.
- Numerical sanity: PASS metrics match or exceed gates in the linked logs.


7. Reproducibility summary
- Front speed: PASS with $R^2=0.999996$, rel-err $4.7\%$.
- Dispersion: PASS with median rel-err $1.45\times 10^{-3}$, $R^2_{\text{array}}=0.999946$.
- Invariant drift: PASS thresholds as specified above (see figures and JSON metrics produced by [qfum_validate.py](../../code/physics/conservation_law/qfum_validate.py)).


8. Code availability and provenance
- The source code for the reaction-diffusion validations is archived privately at a signed commit/tag. This distribution intentionally omits source code to protect proprietary implementations; only the figures and machine logs necessary to verify the results are included in this note.
- A reference implementation will be released at a stable tag at the author's discretion (e.g., v1.0.0).
- Provenance (cryptographic): commit/tag = v1.0.0; private archive digest SHA-256 = TO_BE_PROVIDED.
- The CLI recipes above reference bare script names (no local paths). VDM/void internals (e.g., QA validator and runtime scaffolding) are not included in this distribution.

Appendix: direct links
- Figures (RD): [Derivation/code/outputs/figures/reaction_diffusion](../../code/outputs/figures/reaction_diffusion)
- Logs (RD): [Derivation/code/outputs/logs/reaction_diffusion](../../code/outputs/logs/reaction_diffusion)
- Invariant validator logs: Derivation/code/outputs/logs/conservation_law (figures omitted in RD packaging)
- Scripts: [Derivation/code/physics/reaction_diffusion](../../code/physics/reaction_diffusion), [Derivation/code/physics/conservation_law](../../code/physics/conservation_law)

Citations
- Fisher, R.A. (1937). “The wave of advance of advantageous genes.” Ann. Eugenics 7: 355-369.
- Kolmogorov, A.N.; Petrovsky, I.; Piskunov, N. (1937). “Study of the diffusion equation with growth of the quantity of matter.” Bull. Univ. Moscow, Ser. A 1: 1-25.