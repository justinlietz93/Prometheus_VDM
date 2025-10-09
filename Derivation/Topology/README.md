Short answer: yes-we’re making progress, not circling. You’ve got two “green” pillars already:

* Junction logistic collapse (A6) passes with a tight envelope (≈1.657%), which is exactly the $P(A)=\sigma(\Theta,\Delta m)$ universality we need for decision routing .
* The steering/memory law is already spelled out with the right dimensionless knobs $\Theta, D_a, \Lambda, \Gamma$-that’s our agency substrate ($\mathbf r''=\Theta\nabla_\perp m$; memory PDE with write/decay/spread) .

Below is a compact, self-contained **Phase-2 experiment pack** that lives entirely under `Derivation/code/physics/…` and targets the “intelligence” pieces (SIE, ADC/logistic choice, loops) with falsifiable gates. No FUM runtime involved; only helpers in `Derivation/code/common/` as you requested.

# Classification

Axiom-core (A0–A7) with mixed flows per A4; agency as a slow steering bias on top of fast $\phi$ dynamics.

# Objective recap

Demonstrate that the “intelligence components” are physically measurable laws: (i) memory-steered routing (agency), (ii) decision coupling (ADC) via logistic slope universality, (iii) self-information/invariant behavior (SIE) under controlled perturbations, and (iv) loop pathology is suppressed by dissipation and correlates with Lyapunov drop.

# Action plan (do these in order)

1. **Agency curvature scaling (new).** `physics/agency/run_agency_curvature.py`
   Prepare a smooth $m(x)$; emit narrow $\phi$ pulses; measure path curvature $\kappa_{\rm path}$ vs $X=\Theta|\nabla m|$. Gate: linear fit with $R^2\ge 0.9$ and slope within 10% across $\Theta$ (collapse). Law: $\kappa_{\rm path}\propto\Theta|\nabla_\perp m|$ (from steering) .
2. **Agency stability band (new).** `physics/agency/run_agency_band.py`
   Evolve $m$ with $\partial_t m=\gamma R-\delta m+\kappa\nabla^2 m$; sweep $(\gamma,\delta,\kappa)$; compute $(D_a,\Lambda,\Gamma)$ and a retention metric. Gate: high-fidelity band appears primarily when $D_a\gtrsim\Lambda$ at intermediate $\Gamma$ (prediction) .
3. **ADC response function (tighten A6).** `physics/agency/run_adc_response.py`
   You already passed collapse; now quantify slope. For two-branch forks, verify $P(A)=\sigma(\Theta,\Delta m)$ and that the **measured** logistic slope equals the programmed $\Theta$ within ±5%. Keep the existing A6 overlay and envelope metric as acceptance (already green) .
4. **SIE invariant & novelty pulse (new).** `physics/info/run_sie_invariant.py`
   Use the on-site logistic ODE (reaction-only) and its logarithmic first integral $Q$ (your “logarithmic constant of motion” note) to certify:

   * Control: $|Q(t)-Q(0)|_{\max}$ scales like $\mathcal O(\Delta t^{p+1})$ (RK4 → slope ≈ 5 on two-grid local; Euler → 2). Gate: slope ≥ expected−0.1, $R^2\ge 0.999$.
   * Novelty: inject a brief parameter kick and show **bounded** $Q$ drift that returns to baseline when the kick stops (quantifies “surprise/novelty” without any RL code).
     (This repurposes your $Q$-invariant machinery you already used and keeps it physics-pure.)
5. **Loop quench test (new; topology-lite).** `physics/topology/run_loop_quench.py`
   In 2D RD, threshold an excursion set of $\phi$ (or $m$) and count simple cycles via a grid cycle-basis (no heavy TDA). Track count vs discrete Lyapunov $L_h$. Gate: negative rank correlation $\rho\le-0.7$ between $\Delta L_h<0$ and loop count; plus a fast-decay tail for loop lifetimes. Interpretation: dissipative $M$-sector quenches pathological loops faster than they form-aligns with your “loops as pathology” view while acknowledging their transient utility.
6. **Results pages.** For each runner, emit `RESULTS_*` with MathJax ($…$, $$…$$), pinned artifacts, and gates. Mirror the A6/FRW style you’ve already set (you’re consistent and clean there) .
7. **Optional** (after 1–4): add a one-pager “Agency Field: Minimal Lawbook” that just collates the three dimensionless groups and the two primary plots (junction logistic, curvature scaling) with a single sentence per gate, citing the memory-steering doc .

# Verification (what each proves)

* **Agency (steering):** curvature-vs-gradient collapse and the $D_a$–$\Lambda$ band show a slow field biases routes in the predicted dimensionless way, independent of $\phi$ kinetics .
* **ADC:** A6 is already PASS; the slope-equals-$\Theta$ check nails the coupling constant (not just shape) .
* **SIE:** constant-of-motion in the clean limit + controlled drift under novelty = a measurable “information energy” that behaves lawfully, no RL scaffolding required.
* **Loops:** dissipation correlates with loop suppression, converting your runtime intuition into a physical statement tied to $L_h$ (A5 H-theorem spirit).

# Assumptions / risks

* **Separation of scales:** steering is slow ($m$) while $\phi$ carries fast excitations. If that separation blurs, curvature fits can smear (mitigate by using pulses and modest gradients).
* **Discretization:** curvature on grids is approximated by turning angles; use polyline smoothing so we’re measuring geometry, not stair-casing.
* **Topology-lite:** the cycle-basis counter won’t catch all homology nuance; but for “are loops quenched as $L_h$ drops?” it’s sufficient.

# Next steps

1. Have your agent stand up the four runners above in `Derivation/code/physics/{agency,info,topology}` plus tiny helpers under `…/common/`.
2. Reuse the existing IO/figures/log style and A6/FRW result templates (MathJax: use `$…$` or `$$…$$`).
3. Start with agency curvature (1) and SIE invariant (4)-both are quick wins with crisp gates.
4. Then do the stability band (2) and ADC slope check (3).
5. Close with the loop quench test (5) once the Lyapunov logger is in place.

If you want me to write the exact acceptance blocks you can paste into each runner’s RESULTS.md (or a spec JSON schema for each), I’ll draft them verbatim next.
