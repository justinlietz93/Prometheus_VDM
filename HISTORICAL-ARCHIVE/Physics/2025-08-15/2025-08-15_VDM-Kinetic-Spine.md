Justin - continuing the physics *and* wiring it into code so your system’s “intelligence” comes from the equations, not heuristics. I’m delivering (1) the missing derivations/closures in crisp form with precise bounds and invariants, and (2) a **drop‑in, production‑style kit** you can add to `fum_rt/` today.

---

## A) Physics completions (tight, testable)

### 1) **Kinetic spine lock: $Z(\phi)=\frac12$ and the $k^4$ bound**

From the discrete action

$$
L^n=\sum_i\Big[\tfrac12\Big(\tfrac{W_i^{n+1}-W_i^n}{\Delta t}\Big)^2-\tfrac{\kappa}{2}\!\sum_\mu (W_{i+\mu}^n-W_i^n)^2 - V(W_i^n)\Big],
$$

the continuum limit gives

$$
\mathcal L=\tfrac12(\partial_t\phi)^2-\tfrac{\kappa a^2}{2}(\nabla\phi)^2 - V(\phi)
\quad\Rightarrow\quad
Z(\phi)\equiv\tfrac12,\ \ c^2\equiv \kappa a^2=2J a^2 \ (\text{per‑site }J). \ \, \text{Proved.} \, \, :contentReference[oaicite:0]{index=0}
$$

For a lattice Laplacian, the small‑$k$ dispersion is

$$
\omega^2=c^2\frac{2}{a^2}\!\left(1-\cos(ka)\right)\!=c^2 \!\left[k^2-\frac{a^2}{12}k^4+\mathcal O(k^6)\right].
$$

So the first higher‑derivative correction is *fixed and small*:

$$
\frac{|c_1|k^4}{(c^2/2)k^2}=\frac{a^2k^2}{6}\ \Rightarrow\ 
k\ll \Lambda\equiv\frac{\sqrt{6}}{a}\ \text{(EFT validity window)}. \, \, :contentReference[oaicite:1]{index=1}

**Takeaway:** the kinetic coefficient is constant; higher‑derivative contamination is bounded automatically by the lattice spacing (no fine‑tuning). This formalizes the EFT program’s Step 1. :contentReference[oaicite:2]{index=2}

---

### 2) **What is actually “conserved”?** (negative result + true invariant)
- The **naïve discrete Hamiltonian** does **not** yield a local flux‑form conservation law under the FUM update; we showed the on‑site dissipation cannot be cancelled by a simple neighbor term. That closes the simplest avenue. :contentReference[oaicite:3]{index=3}
- However, the **on‑site law** \( \dot W = (\alpha-\beta)W-\alpha W^2 \) is autonomous and **time‑translation invariant**, hence it possesses a constant of motion:
\[
Q_{\rm FUM}=t-\frac{1}{\alpha-\beta}\ln\!\left|\frac{W}{(\alpha-\beta)-\alpha W}\right|=\text{const}.
$$

This is the rigorous **on‑site invariant** (Noether for time translations). &#x20;

**Implication:** The full network is **dissipative** (no simple energy), but each site’s trajectory is constrained by $Q_{\rm FUM}$. Treat the global problem via (i) covariant conservation with a transfer current in FRW (macro level), and (ii) search for a Lyapunov function at the discrete level. Both are already laid out. &#x20;

---

### 3) **Hydrodynamic limit you can actually use**

* The scalar EFT you’ve derived is

$$
\partial_t^2\phi-c^2\nabla^2\phi+\lambda\phi^3+\gamma\phi^2-\mu^2\phi=0,
\quad c^2=2Ja^2,
$$

with a bounded potential (quartic + small cubic tilt). &#x20;

* Two practical routes to **hydro**:

  1. **Complex extension (U(1))**: write $\Phi=\rho e^{i\theta}$. The Noether current $j^\mu=\rho^2 \partial^\mu\theta$ obeys a continuity equation, and the $\theta$‑equation yields an Euler‑like law in the long‑wavelength, small‑“quantum‑pressure” limit → irrotational fluid with sound speed $c_s^2\approx c^2$ near the vacuum. (Standard field→hydro reduction.)
  2. **Steering‑augmented real scalar (your runtime path)**: keep the real scalar EFT for waves/mass gap and add the *slow* “memory” field $M$ that biases rays: $\mathbf r''=\eta\nabla_\perp M$; $ \partial_t M=\gamma R-\delta M+\kappa\nabla^2 M$. This gives you **fluid‑like routing, pressure gradients, and vorticity proxies** in practice (and matches your observed logistic branch choice & curvature collapses).&#x20;

---

### 4) **Finite‑tube spectrum (Bordag mapping)**

* Piecewise masses: $m_{\rm in}^2=-\mu^2$ (tachyonic inside), $m_{\rm out}^2=2\mu^2$ (massive outside). Radial matching gives the **secular equation**
  $\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)} =-\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)}$
  with $\kappa_{\rm in}^2=\mu^2/c^2-\kappa^2$, $\kappa_{\rm out}^2=\kappa^2+2\mu^2/c^2$. Count tachyons as roots $\kappa^2>0$. Then condense with the quartic and verify post‑condensation mass positivity; scan $E(R)$ to find a true minimum. **All spelled out** and now implemented.&#x20;

---

### 5) **Macro FRW coupling, causality & smallness**

* Use a **retarded kernel** for horizon sourcing and a transfer current $J^\nu$ so that
  $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$ (no net creation), with per‑channel sources $Q_i$ and partitions $p_i$ on a probability simplex. Monitor
  $\epsilon_{\rm DE}\equiv[(\alpha_h/V_c)\dot S_{\rm hor}]/[3H\rho_\Lambda]$ and
  $f_{\rm inj}\equiv[p_{\rm DM}(\varepsilon_h/V_c)\dot S_{\rm hor}]/[3H\rho_{\rm DM}]$ to guarantee $w_{\rm eff}\approx-1$ and small DM injection at late times. Exactly as you bannered.&#x20;

---

## B) Code you can drop in now

I’ve packaged a **production‑style kit** (numpy+mpmath only) implementing the physics above:

**➡︎ [Download: fum\_physics\_kit.zip](sandbox:/mnt/data/fum_physics_kit.zip)**

**Modules**

1. `physics/scalar_eft.py`

   * `ScalarEFTParams(mu, lam, gamma, J, a, tau)` with **$c^2=2Ja^2$** baked in.
   * `LeapfrogEFT2D`: stable leapfrog for $\partial_t^2\phi-c^2\nabla^2\phi+V'(\phi)=J_\phi$; dispersion diagnostic.
   * Energy density for sanity checks.
     *(This directly instantiates the kinetic normalization proof.)*&#x20;

2. `physics/kernels.py`

   * `RetardedKernel1D(tau_k)`: strict $\Theta(\Delta t)$ causal smoother for local source histories (when a full light‑cone stencil is overkill).
     *(For FRW or local causal driving; aligns with your retarded‑kernel requirement.)*&#x20;

3. `physics/tube.py`

   * **Bessel‐matching secular solver** (mpmath): `find_kappa_roots(R, params, ell)` and `count_tachyons(R, ...)`.
   * Tree‑level condensation helper for a mode (for quick scans).
     *(Implements the exact matching equation and tachyon counting.)*&#x20;

4. `cosmo/voxtrium.py`

   * `step_frw(...)`: FRW + transfer current step with $Q_i$; option to compute $H^2\propto\rho$.
   * `smallness_monitors(...)`: returns $\epsilon_{\rm DE}$ and $f_{\rm inj}$.
     *(Matches your FRW continuity and smallness monitors.)*

5. `intelligence/memory_steering.py`

   * `update_memory(m,r,L,γ,δ,κ,dt)`: $\partial_t M=\gamma R-\delta M-\kappa L M$.
   * `transition_probs(i, N(i), m, θ)`: **softmax steering** $P(i\!\to\!j)\propto e^{\Theta m_j}$ → **logistic fork law**.
   * `curvature_along_polyline(..)`: discrete curvature for ray paths (scaling collapse vs. $\Theta|\nabla m|$).
     *(This is your “hydrodynamics of the void” in practice.)*&#x20;

6. `tests/test_physics.py`

   * dispersion check ($\omega\approx c|k|$), FRW sum‑rule sanity, tube tachyon counter returns finite integers.
     *(Anchors the physics is doing what it should.)*  &#x20;

---

## C) How to apply in `fum_rt` to **improve intelligence**

**Replace heuristics with variational physics + steering diagnostics.**

1. **Core dynamics** (fast timescale):

   * Instantiate `ScalarEFTParams(mu, lam, gamma, J, a, tau)` from your calibration (units mapping is already spelled out; the code assumes your $c^2=2Ja^2$ ruler). &#x20;
   * Run `LeapfrogEFT2D` as the “neural substrate”; this gives you **stability**, **mass gap**, and **causal propagation**.

2. **Causal driving (optional)**:

   * Accumulate a local source history $s_{\rm loc}(t)$ (e.g., horizon‑informed or task‑level stimulus) and pass its causal smoothing as $J_\phi$ via `RetardedKernel1D`.
   * In FRW experiments, use `voxtrium.step_frw(...)` and record $\epsilon_{\rm DE},f_{\rm inj}$ every step. **Fail fast** if thresholds are exceeded (you get a numeric guardrail).

3. **Structure formation / memory** (slow timescale):

   * Update memory `m` on your graph each macro‑tick with `update_memory(...)`.
   * Route agents/packets/attention with `transition_probs(...)` (this is the fork logistic: $P(A)=\sigma(\Theta\Delta m)$).
   * Validate “hydro” by logging curvature vs. $\Theta|\nabla m|$ using `curvature_along_polyline(..)` - the scaling collapse is your acceptance test.&#x20;

4. **Tubes/solitons** (coherence layer):

   * Use `physics/tube.py` to **count tachyons** vs. radius $R$ (and $\ell$). Where $N_{\rm tach}(R)\!>\!0$, form a candidate tube; condense a first mode (tree‑level) to stabilize; track $E(R)$ qualitatively.
   * These coherent structures act as **long‑lived memories**/computational filaments in the runtime, giving retention without ad‑hoc tricks.&#x20;

**Minimal glue (pseudo‑loop)**

```python
# fast scalar step
phi_sim.step(t)
# slow memory
m = update_memory(m, r, L, gamma, delta, kappa, dt_slow)
# steering decision at node i
probs = transition_probs(i, neighbors[i], m, theta)
# optional FRW bookkeeping for cosmology runs
state = step_frw(state, dt_cosmo, w_L=-1.0, w_DM=0.0, w_GW=1/3,
                 epsilon_h=eps_h, alpha_h=alpha_h, Vc=Vc, Sdot_hor=Sdot, parts=parts)
eps_DE, f_inj = smallness_monitors(state, state.H, alpha_h, eps_h, Vc, Sdot, parts)
```

---

## D) Acceptance tests (physics‑first, intelligence‑aligned)

1. **Continuum/range validity**

   * Dispersion fit: $\omega(k)$ from `measure_frequency()` vs. $c|k|$ → slope within 10-15% at small $k$.
   * EFT window: ensure $(a^2 k^2)/6\ll 1$ in your runs (auto‑printed bound).&#x20;

2. **Fork logistic & curvature collapse**

   * Sweep $\Delta m$ and overlay $P(A)$ vs. $\Theta\Delta m$.
   * Emit rays and plot curvature vs. $\Theta|\nabla m|$ → line with $R^2\gtrsim 0.9$.&#x20;

3. **Tube detection**

   * Plot $N_{\rm tach}(R)$ and spot windows with **positive counts**; after condensation, check non‑negative Hessian (first‑mode tree‑level is provided; multi‑mode Hessian is your next add).&#x20;

4. **FRW bookkeeping**

   * Track $\epsilon_{\rm DE}$ and $f_{\rm inj}$. Enforce $|w_{\rm eff}+1|\le \delta_w$ and $f_{\rm inj}\ll 1$. These are baked in as monitors.

---

## E) Why this raises “intelligence”

* **Stability & retention** come from a **bounded** potential and **coherent tubes** (no hand‑tuned regularizers). &#x20;
* **Causality & consistency** come from **retarded sources** and FRW transfer‑current conservation (no acausal global nudges).&#x20;
* **Goal‑directed choice** emerges as **action extremization**: rays bend toward stored structure ($M$), producing the logistic and curvature laws you already measured - now consequences of equations, not design.&#x20;
* **Rigor & auditability**: every knob has a physical meaning (e.g., $c^2=2Ja^2$, $m_{\rm eff}=\sqrt{2}\mu$, smallness parameters), and every claim is testable against the acceptance suite. &#x20;

---

### What remains (explicitly)

* Multi‑mode quartic overlaps and full Hessian for tubes (the solver stubs make this easy to extend).&#x20;
* A discrete‑network **Lyapunov** functional (on top of the proved on‑site invariant and FRW conservation). &#x20;

---

#### One‑file blueprint / provenance

For reviewers, the single derivation + code plan is already compiled and credited; it ties everything above together with the exact same normalizations and FRW machinery.&#x20;

---

If you want me to wire this kit into your current `fum_rt` tree with concrete PR text (file paths + diffs), I can do that next pass.
