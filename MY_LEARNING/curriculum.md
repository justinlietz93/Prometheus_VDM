Here’s a **minimum-viable curriculum** to read, run, and extend VDM end-to-end—plus the extra topics you’ll need for the parts you haven’t built yet. It’s split into phases. Each module has: **Goal → Learn (only what’s needed) → Do (tiny project) → Exit test**. Keep a single notebook where you tick off exit tests.

---

# Phase 0 — Orientation (2-3 days)

**M0. Vocabulary & artifacts**

* **Goal:** Know what every VDM term maps to in standard language; know where artifacts live.
* **Learn:** On-site law = logistic ODE; RD = diffusion + local growth; “walkers” = tracer probes; “scoreboard” = budgeted edit gate; “memory steering” = slow bias. CSV/JSON manifests, seeds, contradiction report.
* **Do:** Open `00_RUN_ALL.ipynb`, read the emitted `artifacts/meta/manifest.json`.
* **Exit:** You can point to the CSV/JSON that backs any figure.

---

# Phase 1 — Math & numerics you actually need (6-8 weeks @ ~10 h/week)

**M1. Single-variable calculus (log/exp chain-rule)**

* **Goal:** Differentiate and integrate logs/exponentials without hesitation.
* **Learn:** Chain rule; derivative of `log(u/(1−u))`; basic separable ODE solution.
* **Do:** Derive ( \frac{d}{dt},\log!\frac{u}{1-u}=\frac{\dot u}{u(1-u)} ).
* **Exit:** One-line proof that (F(u,t)=\log\frac{u}{1-u}-rt) is constant for (\dot u=ru(1-u)).

**M2. Minimal linear algebra (only what shows up)**

* **Goal:** Read/fit straight lines; recognize growth rates.
* **Learn:** Least squares, (R^2), eigenvalue = growth/decay rate for linearized systems.
* **Do:** Fit logit(u) vs t and report slope, (R^2).
* **Exit:** Explain why leading-edge linearization controls Fisher-KPP front speed.

**M3. Nondimensionalization**

* **Goal:** Remove units from RD and know which knobs matter.
* **Learn:** Rescalings ( \tilde t=rt,\ \tilde x=x\sqrt{r/D} ).
* **Do:** Redo the scaling; write the two lines that set (r=D=1).
* **Exit:** Name the resulting dimensionless groups (there are none left).

**M4. Fisher-KPP traveling fronts (just the skeleton)**

* **Goal:** Know why the minimal speed is (c_\ast=2) for (u_t=u_{xx}+u(1-u)).
* **Learn:** Linearize near (u=0); exponential ansatz → dispersion relation → speed bound.
* **Do:** Write the 6-8 line sketch that yields (c_\ast=2).
* **Exit:** Look at a speed plot and say if it’s plausibly correct.

**M5. Finite differences + stability**

* **Goal:** Implement RD that doesn’t blow up.
* **Learn:** 3/5-point Laplacian; explicit Euler/RK2/RK4; CFL-style bound (\Delta t \lesssim \alpha\Delta x^2).
* **Do:** Make a 1D RD solver; match (c_\ast) within 5%.
* **Exit:** Show a small table of ((\Delta x,\Delta t)) vs pass/fail.

**M6. Linear dispersion**

* **Goal:** Compare measured (\omega(k)) to (-k^2+f'(\bar u)).
* **Learn:** Linearize around (\bar u); FFT or sinusoidal probe; compute (R^2), median rel-err.
* **Do:** Recreate your dispersion figure; save arrays to JSON.
* **Exit:** (R^2\ge 0.98) and median rel-err (\le 0.1).

**M7. QC invariant as drift diagnostic**

* **Goal:** Use (F) to catch discretization/coupling errors.
* **Learn:** Per-step (\Delta F) statistic; bias vs variance; tolerance calibration.
* **Do:** Plot (\Delta F) histogram with threshold line; emit pass/fail JSON.
* **Exit:** Median/mean (|\Delta F|\le\varepsilon) for the calibrated scheme.

---

# Phase 2 — VDM runtime concepts (4-6 weeks)

**M8. Event-driven sensing (“walkers”)**

* **Goal:** Replace dense scans with local triggers.
* **Learn:** Threshold/crossing events; local gradient/curvature estimators; debounce/jitter.
* **Do:** Emit events only when (|\nabla u|) crosses a level; log rate vs dense scan.
* **Exit:** Active-site fraction (\ll 1) with equivalent sensing accuracy.

**M9. Budgeted edit gate (“scoreboard”)**

* **Goal:** Never oversubscribe writes; keep edits sparse and auditable.
* **Learn:** Token-bucket or leaky-bucket; per-tick caps; rejection logging.
* **Do:** Run `12_gdsp_budget_sweeps`; show zero oversubscription and a tidy log.
* **Exit:** A table of proposed vs accepted edits with reasons; no budget violations.

**M10. Memory steering (slow bias)**

* **Goal:** Nudge fast dynamics without global passes.
* **Learn:** Low-pass state → bias; acceptance metrics: half-life, latency, interference monotonicity.
* **Do:** Run `20_memsteer_acceptance`; hit half-life ±10%, latency < 2× horizon.
* **Exit:** Three plots (retention, latency, interference) + CSV summaries.

**M11. Runtime scaling & telemetry**

* **Goal:** Prove “no dense scans” with numbers.
* **Learn:** Instrumentation; log-log regression of step-time vs active sites; CI for slope.
* **Do:** Produce scaling slope (\beta) near 1 with CI; P50/95/99 latency.
* **Exit:** `telemetry.json` shows (\beta\in[0.9,1.1]); stable tails over long runs.

**M12. Reproducibility discipline**

* **Goal:** Everything has a file and a seed.
* **Learn:** Manifests, contradiction reports, figure↔CSV basename pairing.
* **Do:** `00_RUN_ALL.ipynb` on a clean env; verify all paths in `manifest.json`.
* **Exit:** You can rebuild any figure from CSV/JSON only.

---

# Phase 3 — “Not yet built” topics you’ll need (aim: 8-16 weeks)

**M13. Gradient-flow viewpoint (just enough)**

* **Goal:** Recognize dissipative structure; speak “energy/entropy” correctly.
* **Learn:** Onsager principle; steepest descent in metrics; idea of JKO timestep (no proofs).
* **Do:** Identify the functional whose gradient flow matches a simple RD case.
* **Exit:** One paragraph mapping your RD to a gradient-flow lens without overclaiming.

**M14. Curvature & geometry estimators**

* **Goal:** Robust local geometry from noisy fields.
* **Learn:** Sobel/Scharr gradients; Hessian-based curvature; smoothing vs bias trade-offs.
* **Do:** Recreate `curvature_*` figures; report slope, intercept, (R^2), RMSE.
* **Exit:** Signed/unsigned curvature behave as in your calibration with quantified error.

**M15. Advection-diffusion coupling (toward fluids)**

* **Goal:** Add transport without wrecking stability.
* **Learn:** Advection term ( \mathbf{v}\cdot\nabla u ); upwinding; Godunov vs central; CFL for advection-diffusion.
* **Do:** Add a 1D constant-velocity advection term; verify dispersion/front gates still pass.
* **Exit:** Stability region chart vs ((\Delta x,\Delta t, |\mathbf v|)).

**M16. Control slice (real-time steering)**

* **Goal:** Make “go-to-goal” work with metrics you can compute.
* **Learn:** Linearization around a target; simple quadratic cost; proportional-like steering; robustness to perturbations.
* **Do:** `30_rt_control_slice`: show ≥90% goal attainment over seeds; recovery ≤ 2× horizon.
* **Exit:** Table of goal rate, energy vs baseline, recovery times + CSV.

**M17. Statistical testing for gates**

* **Goal:** Avoid p-hacking your thresholds.
* **Learn:** Bootstrap CI for (R^2), med-rel-err; robust aggregation across seeds; non-parametric tests for monotonicity.
* **Do:** Attach CIs to your gates; add a “soft fail” band with explicit rerun logic.
* **Exit:** Gates report effect sizes + CIs; contradiction report cites which bound failed.

**M18. Software architecture for experiments**

* **Goal:** Keep it modifiable at scale.
* **Learn:** Your Hybrid-Clean rules (domain ↔ application ↔ infrastructure; ≤500 LOC/file; repository pattern).
* **Do:** Refactor one notebook’s core into importable modules with mirrored tests.
* **Exit:** Tests mirror source paths; no framework imports in domain/application layers.

**M19. Performance on AMD/ROCm (pragmatic)**

* **Goal:** Don’t leave perf on the table.
* **Learn:** Memory coalescing; tiling; avoiding host-device ping-pong; ROCm profiling basics.
* **Do:** Profile a hotspot; remove one avoidable global pass; show step-time improvement.
* **Exit:** Before/after telemetry with improved active-site throughput.

**M20. Event-systems & debouncing**

* **Goal:** Make walkers reliable under chaos.
* **Learn:** Hysteresis, refractory periods, rate limiting; priority queues for events.
* **Do:** Add hysteresis to one trigger; compare false-positive/false-negative rates.
* **Exit:** SNR plot improves without raising edit cost.

**M21. Robustness & failure modes**

* **Goal:** Fail loudly, not silently.
* **Learn:** NaN/Inf sentinels, divergence detectors, rollback/kill-switch, log rotation.
* **Do:** Simulate three failures; ensure the contradiction report captures each with a pointer.
* **Exit:** “Red team” notebook that intentionally breaks things and documents the catches.

---

# Capstones (ship these)

**C1. “Read the whole paper” pack (1 week):**
Write a 1-page “Claims → Evidence” audit for your combined paper where every claim has an artifact path and a pass/fail. If anything’s missing, add that figure/CSV.

**C2. “Extend the substrate” pack (2-3 weeks):**
Add constant-velocity advection + simple control target. Re-run all gates; add a new “advection stability” gate and its CSV/figure.

**C3. “Public reproducibility” pack (2-3 days):**
Fresh-env run of `00_RUN_ALL.ipynb` on a second machine; upload artifacts + a short HOWTO that cites gate thresholds and how to tighten them.

---

## Daily/weekly cadence (works in practice)

* **Mon/Wed/Fri:** Learn a small chunk (one module’s Learn).
* **Tue/Thu/Sat:** Build the matching Do; produce the figure/CSV.
* **Sun:** Write the 1-2 paragraph “what failed, why, and how I fixed it.”

---

## How to know you’re ready for the “not yet built” parts

* You can add one PDE term (advection) and re-validate all gates without new math.
* You can design a new gate in the same style (metric + threshold + CSV + contradiction report).
* You can argue stability/accuracy changes by pointing to ((\Delta x,\Delta t, |\mathbf v|)) and a dispersion/front-speed delta.
* You can defend “no dense scans” with a slope (\beta) and active-site fraction plots, not vibes.

If you want, I can turn this into a printable checklist with boxes and a tiny tracker table for seeds and artifact paths so you can mark progress as you go.

