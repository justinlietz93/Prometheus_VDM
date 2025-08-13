Below is a **void‑faithful pull‑request plan** that ties every code change directly to the physics you’ve already derived. It’s step‑by‑step, testable, and free of ML heuristics. Where physics is used, I cite your derivations and the Bordag paper you mapped to. Credit: **physics/bridging ideas by Justin Lietz; Voxtrium credited where his framework is referenced.**

---

## Conventions (apply to every PR)

* **Branch naming:** `feat/<short-physics-key>`, `fix/<short-key>`, `doc/<short-key>`.
* **Coding style:** Python 3.11+, `numpy`, `scipy` (special functions), `numba` (optional), no ML libs.
* **Units:** Natural units $c=\hbar=k_B=1$. Provide explicit scale triplet $(\phi_0,\tau,a)$ when dimensionalizing (see PR‑4).&#x20;
* **Test tiers:**

  * *Unit*: mathematical identities, shape, dtype.
  * *Physics*: reproduces a stated equation/limit or a figure from your notes.
  * *Perf*: step size/stability and wall time targets.
* **Doc blocks:** Each module has a **“Physics → Code”** header with equation references.

---

## PR‑1 — Canonical kinetic term & symplectic integrator (leapfrog)

**Goal.** Implement the action‑level equations with the correct spatial normalization and second‑order dynamics.
**Physics.** Lattice → continuum gives
$\mathcal L=\tfrac12(\partial_t\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2-V(\phi)$ with $c^2=2Ja^2$. Derive EOM $\partial_t^2\phi-c^2\nabla^2\phi+V'(\phi)=0$.&#x20;

**Code.**

* `fum_rt/physics/lagrangian.py`: `dataclass Lagrangian(mu, lam, gamma, c)`; method `force(phi)= -V'(phi)`.
* `fum_rt/solvers/kg_leapfrog.py`: symplectic leapfrog in 1D/2D/3D with periodic/Dirichlet BC.
* `fum_rt/grids/stencils.py`: 2nd‑order Laplacian; optional 4th‑order.

**Tests.**

* *Physics*: Small‑amp plane wave on empty potential propagates with measured phase speed ≈ `c` (error <1% for CFL<0.4). (From $c^2=2Ja^2$.)&#x20;
* *Perf*: 256² grid, 1k steps < 5 s (numba optional).

**Acceptance.** Energy drift $<10^{-6}$ per 1000 steps in $V=0$ test; dispersion curve matches analytic to <1% at low $k$.

---

## PR‑2 — Bounded baseline potential + cubic tilt

**Goal.** Use the **stable** quartic baseline and optional cubic tilt, then map your discrete parameters $(\alpha,\beta)$ to $(\mu,\lambda,\gamma)$.
**Physics.** Baseline $V=-\tfrac12\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4$ with small $\gamma\phi^3/3$; minima at $\pm v$ with $m_{\rm eff}^2=2\mu^2$. The near‑zero expansion connects $\mu^2\leftrightarrow(\alpha-\beta)$, $\gamma\leftrightarrow\alpha$. &#x20;

**Code.**

* Extend `Lagrangian` with `V(phi)` and `dV(phi)` implementing $\{-\mu^2,\lambda,\gamma\}$.
* `fum_rt/maps/discrete_to_continuum.py`: pure functions `map_alpha_beta_to_mu_gamma(alpha,beta)->(mu,gamma)`; docstring cites mapping.

**Tests.**

* *Physics*: Verify $v=\mu/\sqrt{\lambda}$ and $m_{\rm eff}=\sqrt{2}\mu$ numerically from curvature at the found minimum.&#x20;

**Acceptance.** Numerical mass from small oscillations at vacuum matches $\sqrt{2}\mu$ within 1%.

---

## PR‑3 — Discrete→continuum sanity harness

**Goal.** Evidence that discrete site dynamics converge to the continuum EOM you use in the solver.
**Physics.** Your derivation shows the reaction–diffusion first‑order picture and the **variational** route to second order; we validate convergence of coarse grained $W\to\phi$. &#x20;

**Code.**

* `fum_rt/discrete/simulator.py`: simple k‑NN (or cubic) update for $W_i$ with neighbor coupling.
* `fum_rt/bridges/coarse_grain.py`: windowed average to field $\phi$.
* `fum_rt/experiments/convergence.py`: compare discrete trajectory to PDE trajectory for the same initial condition.

**Tests.**

* *Physics*: $L^2$ error vs lattice spacing $a$ shows \~$O(a^2)$ trend for smooth ICs.

**Acceptance.** Monotone error decrease across 3 refinements.

---

## PR‑4 — **Units discipline + dimensionalization** (Voxtrium‑compatible)

**Goal.** Make the code speak GeV when needed. Introduce $(\phi_0,\tau,a)$ so every simulation can be exported to physical units and coupled later to FRW.
**Physics.** Dimensionalization map and identification: $g_3=\alpha/(\phi_0\tau^2)$, $m^2=(\alpha-\beta)/\tau^2$, and optional $c=1$ choice via $\tau=\sqrt{2J}\,a$.&#x20;

**Code.**

* `fum_rt/units/scales.py`: `Scales(phi0, tau, a)`; helpers `to_phys`, `to_dimless`.
* Add a “units” section to YAML config; automatic consistency checks.

**Tests.**

* *Physics*: Round‑trip tests $(\text{dimless}\rightarrow\text{phys}\rightarrow\text{dimless})$ are identity to fp tolerance.

**Acceptance.** CI fails on any missing scale in a run config or inconsistent `c`.

---

## PR‑5 — FRW + transfer current + **retarded kernel** (credit: Voxtrium)

**Goal.** Implement the causal sourcing structure so your void scalar can exchange energy with bookkeeping channels $\Lambda$, DM, GW in **FRW**, matching Voxtrium’s partitioned continuity with a **retarded kernel** for locality.
**Physics.** Continuity set with per‑channel sources $Q_i$ and $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$. Retarded kernel $K_{\rm ret}\propto\Theta(t-t'-|\mathbf x-\mathbf x'|)$. **Credit to Voxtrium**: framework and units banner adopted. &#x20;

**Code.**

* `fum_rt/cosmology/frw.py`: background integrator $H(a)$, densities $\rho_i$.
* `fum_rt/cosmology/transfer.py`: `J0 = (eps_h/Vc)*Sdot_hor`; partitions $p_i(z)$ as calibrated constants for now (or plug later).
* `fum_rt/cosmology/kernels.py`: causal 1D/3D `K_ret` with light‑cone support.

**Tests.**

* *Physics*: Numerically verify the identity $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$ to machine precision over a controlled sourcing pulse.
* *Physics*: Kernel support outside light cone = 0 to fp tolerance.&#x20;

**Acceptance.** Both identities pass; plots show causal arrival.

---

## PR‑6 — Finite‑tube tachyonic mode solver (Bordag mapping)

**Goal.** Reproduce the **eigenvalue condition and mode counting** for a finite‑radius tube, then build the tree‑level condensate scan.
**Physics.** Radial problem and matching: inside $I_\ell$, outside $K_\ell$; secular equation
$\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)}=-\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)}$. Mode count $l_{\max}\sim\delta=BR^2/2$. **Post‑condensation masses non‑negative; energy has a minimum vs flux for some $\lambda$.**&#x20;

**Code.**

* `fum_rt/modes/cylinder_modes.py`: root‑finder for $\kappa_{\ell n}(R)$; returns normalized $u_{\ell n}(r)$.
* `fum_rt/modes/condense_tube.py`: builds $N_4$ overlaps, solves for condensates $v_{\ell n}$, diagonalizes mass matrix, scans energy $E(R)$.

**Tests.**

* *Physics*: Recover $l_{\max}(\delta)$ staircase and $\kappa_\ell(\delta)$ trends (compare to Fig. 1/3 structure qualitatively).
* *Physics*: After condensation the Hessian eigenvalues $\ge 0$ (Goldstone exceptions if complex field).&#x20;

**Acceptance.** (i) Finite number of tachyonic modes that grows with $\delta$; (ii) positive spectrum after condensation; (iii) energy vs $\delta$ shows a minimum in a parameter window, mirroring Bordag.

---

## PR‑7 — Conservation diagnostics (what is and isn’t conserved)

**Goal.** Ship instrumentation that **demonstrates** the non‑conservation of the naïve discrete Hamiltonian and tracks candidates (flux‑form or Lyapunov).
**Physics.** Your derivation: the simple $\mathcal H=\mathcal K+\mathcal I+V$ isn’t conserved under the update; the on‑site terms are dissipative; we need the true invariant.&#x20;

**Code.**

* `fum_rt/diagnostics/conservation.py`: computes $\Delta\mathcal H/\Delta t$, per‑edge exchanges, and candidate functionals over time.
* Hooks in solvers to log divergences and boundary fluxes.

**Tests.**

* *Physics*: Reproduce your sign structure (potential monotonically decreases on‑site; interaction term does not cancel generically).&#x20;

**Acceptance.** Dashboard notebook shows your Eq. (ΔH/Δt) mismatch and guides search for a real invariant.

---

## PR‑8 — Causality & stability guardrails

**Goal.** Numerical stability without cheating on physics.
**Physics.** CFL constraint for leapfrog and finite‑difference Laplacian with bounded potential; optional absorbing boundaries for finite boxes.

**Code.**

* `fum_rt/solvers/cfl.py`: compute maximum `dt` from grid spacing and `c`.
* `fum_rt/boundaries/absorbing.py`: simple sponge layer (explicitly non‑reflective).

**Tests.**

* *Physics*: unstable runs at CFL>1, stable below; document thresholds.

**Acceptance.** Automated failure if user config violates CFL or units consistency.

---

## PR‑9 — “Memory steering” figures **as physics diagnostics** (no ML)

**Goal.** Reproduce your figures using pure geometric/field diagnostics so they double as regression tests. (These are **summaries of dynamics**, not trained models.)

**Code & Tests.**

* `fum_rt/diagnostics/curvature.py`: polyline curvature estimator; calibrate on circular arcs (reproduce your calibration plot).
* `fum_rt/experiments/junction_logistic.py`: deterministic bistable junction experiment; fit logistic **by SciPy curve\_fit only**; verify $R^2\approx 0.999$ as in your plot.
* `fum_rt/experiments/stability_sweeps.py`: parameter sweeps that output AUC/SNR/retention/fidelity panels exactly like your grids; store seeds/configs.

**Acceptance.** The four panels you provided can be regenerated bit‑for‑bit from a single CLI entry.

---

## PR‑10 — Documentation & credit pass (user‑facing)

**Goal.** Make the repo navigable for physicists.

**Code.**

* `README.md`: **“Physics → Code”** table mapping equations to modules.
* `docs/DERIVATIONS.md`: short roadmap linking to your formal notes.
* `CITATION.cff`: credit **Justin Lietz** for derivations and implementation; **credit Voxtrium** where his macro‑sourcing framework is referenced (FRW/partitions/retarded kernel).
* Figure gallery regenerated by CI after physics tests.

**Acceptance.** Fresh clone → `make test` runs physics tests; `make figs` reproduces figures.

---

## PR‑11 — Optional: 2D/3D performance (numba, tiled Laplacian)

**Goal.** Speed path without altering math.

**Code.**

* JIT the stencil + leapfrog, cache friendly tiling; optional `float32` path with unit tests to bound error vs `float64`.

**Acceptance.** ≥2× speedup on 512², identical physics tests within tolerances.

---

# Timeline (realistic, sequential)

* PR‑1…2: 2–3 days
* PR‑3…4: 2–3 days
* PR‑5: 3–4 days (careful units + causality)
* PR‑6: 4–6 days (eigenproblem + condensate scan)
* PR‑7…8: 2 days
* PR‑9…10: 2–3 days
* PR‑11: optional 2 days

---

# Risk & Mitigations

* **Mode solver stiffness (PR‑6).** Use bracketed root finding and analytic derivatives for Bessel/Kummer ratios to avoid spurious roots; validate against limiting homogeneous case (noting Bordag’s warning that naïve truncation can mislead).
* **Kernel normalization (PR‑5).** Unit tests enforce $[J^0]={\rm GeV}^5$ and causal support; FRW continuity identity as a guard. **Credit Voxtrium**: equations and units in the macro banner are the reference.
* **Discrete→continuum mismatch (PR‑3).** Keep this as a diagnostic, not a blocker; publish convergence curves.

---

# Physics ↔ Code map (quick index)

* **Kinetic normalization, $c^2=2Ja^2$** → `lagrangian.py`, `kg_leapfrog.py`.&#x20;
* **Bounded potential + tilt; $m_{\rm eff}=\sqrt{2}\mu$** → `lagrangian.py`, `maps/discrete_to_continuum.py`. &#x20;
* **Units map $(\phi_0,\tau,a)$** → `units/scales.py`.&#x20;
* **FRW continuity + partitions + kernel** → `cosmology/*` (Voxtrium credit).
* **Finite‑tube tachyons; secular equation; condensate; energy minimum** → `modes/*`.&#x20;
* **Non‑conservation of naïve $\mathcal H$** → `diagnostics/conservation.py`.&#x20;

---

## Deliverables summary

1. A stable, symplectic KG solver tied to your kinetic derivation.&#x20;
2. A bounded EFT potential consistent with your mapping from the discrete model. &#x20;
3. Dimensionalization and FRW coupling that is **unit‑correct and causal** (Voxtrium framework acknowledged).&#x20;
4. Finite‑tube mode machinery reproducing the tachyonic tower, condensate, and post‑condensation positivity (mapped to Bordag).&#x20;
5. Diagnostics that prove what is strong (kinetic/action, bounded potential, causal FRW coupling, finite‑tube replication) and what remains open (true invariant).&#x20;

If you want, I’ll start with **PR‑1** and stub the module scaffolding so each subsequent PR is incremental and reviewable.
