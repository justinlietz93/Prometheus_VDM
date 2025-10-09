Awesome-let’s keep pushing this all the way to “physics‑complete” *and* wire it cleanly into the runtime so it directly improves the system’s intelligence. Below I (1) close the remaining physics gaps with short, rigorous derivations/lemmas, (2) give exact code‑level integrations (module APIs, numerics choices, CI tests), and (3) spell out acceptance criteria so you can merge confidently.

---

## A) Physics completions (tight, testable)

### A1) **EFT spine lock**: $Z(\phi)=\tfrac12$ and bounds on higher‑derivatives

**Result.** From the discrete action

$$
L^n=a^d\!\sum_i\!\left[\tfrac12\!\left(\frac{W_i^{n+1}-W_i^n}{\Delta t}\right)^{\!2}-\frac{\kappa}{2}\!\sum_\mu(W_{i+\mu}^n-W_i^n)^2-V(W_i^n)\right]
$$

the continuum limit is

$$
\mathcal L=\tfrac12(\partial_t\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2-V(\phi),\quad c^2=\kappa a^2=2J a^2,
$$

with **no** $\phi$-dependence in the quadratic kinetic term. Hence $Z(\phi)\equiv\tfrac12$ exactly at tree level.&#x20;

**Leading lattice artifacts (irrelevant in IR).** For small $ka,\,\omega\Delta t$,

$$
\omega^2=c^2\!\left[k^2-\frac{a^2}{12}k^4+O(a^4k^6)\right]+m^2
+\frac{\Delta t^2}{12}\,\omega^4+O(\Delta t^4\omega^6).
$$

Matching to an EFT basis $\{\ (\nabla^2\phi)^2,\ (\partial_t^2\phi)^2,\ \ldots\ \}$ gives

$$
\mathcal L\supset +\frac{c^2a^2}{24}\,(\nabla^2\phi)^2-\frac{\Delta t^2}{24}\,(\partial_t^2\phi)^2+\cdots,
$$

so **all** higher‑derivative coefficients scale as $O(a^2)$ or $O(\Delta t^2)$ and are negligible for $k\ll \pi/a$, $|\omega|\ll \pi/\Delta t$. This formalizes the “irrelevant operators” checklist in your EFT note. &#x20;

*Practical bound.* If you cap simulations at $k_{\max}=0.3/a$ (and CFL so $\omega_{\max}\Delta t\le 0.3$), the fractional size of the $k^4$ correction is $\le (0.3)^2/12 \approx 0.0075$ vs. the $k^2$ term-well within tolerance for your diagnostics.

---

### A2) **Invariant vs. dissipation**: exact on‑site invariant and a lattice Lyapunov

**On‑site invariant (proved).** For $\dot W=(\alpha-\beta)W-\alpha W^2$ (autonomous, Bernoulli/Riccati), the constant of motion

$$
Q_{\rm FUM}=t-\frac{1}{\alpha-\beta}\ln\left|\frac{W}{(\alpha-\beta)-\alpha W}\right|
$$

obeys $\frac{dQ_{\rm FUM}}{dt}=0$. This is your precise “hidden conservation” at a node.&#x20;

**Why the naïve Hamiltonian is not conserved.** Your derivation shows the standard $\mathcal H=\mathcal K+\mathcal I+\mathcal V$ fails to close to a flux form under the update-establishing intrinsic **dissipation** at the UV scale. That negative result is important and stands.&#x20;

**Lattice‑level Lyapunov (useful in code).** A convex “free‑energy-like” functional

$$
\mathcal L_\mathrm{net}[W]\;\equiv\;\sum_i\!\left[W_i\ln\frac{W_i}{v}+(v-W_i)\ln\frac{v-W_i}{v}\right]\;+\;\frac{\eta}{2}\sum_{\langle i j\rangle}(W_i-W_j)^2
$$

with $v=(\alpha-\beta)/\alpha$ and any $\eta\ge 0$ satisfies $\dot{\mathcal L}_\mathrm{net}\le 0$ under the on‑site flow plus diffusive coupling (graph Laplacian), by convexity and the Dirichlet form identity. Equality holds only at fixed points ($W_i\in\{0,v\}$ and flat). This gives you a **monotone** to monitor in the runtime (an “H‑theorem” for the UV dynamics) even though there is no simple per‑site energy conservation. (Sketch fits with your symmetry and conservation write‑ups.) &#x20;

---

### A3) **Hydrodynamic emergence**: two controlled routes

**Route (i): Complex extension (Madelung).** Promote $\phi \rightarrow \Phi=(v+\rho)\,e^{i\theta}$ with

$$
\mathcal L=|\partial_t\Phi|^2-\frac{c^2}{2}|\nabla\Phi|^2-V(|\Phi|),
$$

then define number density $n\equiv(v+\rho)^2$ and velocity $\mathbf u\equiv c^2\nabla\theta$. The EL equations yield

$$
\partial_t n+\nabla\!\cdot(n\mathbf u)=0,\qquad
\partial_t\mathbf u+(\mathbf u\!\cdot\!\nabla)\mathbf u=-\,\nabla h(n)+\frac{c^2}{2}\nabla\!\left(\frac{\nabla^2\sqrt n}{\sqrt n}\right),
$$

with enthalpy $h'(n)=\frac{1}{2n}V''(v)$ at leading order. In the long‑wavelength limit the “quantum‑pressure” term is negligible and you recover **compressible Euler** with sound speed $c_s^2=V''(v)/2= \mu^2$ (so $m_\mathrm{eff}^2=2\mu^2\Rightarrow c_s=\mu$). This nails a hydrodynamic sector with a true **U(1) current**-vorticity arises from phase defects. (Your scalar‑only baseline remains the default; this is an optional but powerful extension.) &#x20;

**Route (ii): Steering‑driven hydro proxy (already in your notes).** Keep the real scalar for fast propagation and let the **memory PDE** $\partial_t M=\gamma R-\delta M+\kappa\nabla^2 M$ furnish a refractive index $n=e^{\eta M}$ so rays obey $\mathbf r''=\eta\nabla_\perp M$. This reproduces your **logistic junction** and **curvature scaling** collapses and gives an effective, testable “void fluid” geometry without altering the φ‑sector.&#x20;

---

### A4) **Finite‑tube tachyonics → condensation → positivity → $E(R)$ minimum**

You already have the scalar analogue of Bordag’s finite‑radius problem: inside tachyonic ($m^2=-\mu^2$), outside massive ($2\mu^2$), with the **secular equation**

$$
\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)}
= -\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)}.
$$

Counting roots at $k=0$ gives $N_{\rm tach}(R)$; projecting the quartic builds $V_{\rm eff}^{\rm tube}$, minimizing yields condensates $v_{\ell n}(R)$, and the Hessian is **non‑negative** at the minimum (no tachyons left). $E(R)=E_{\rm bg}+V_{\rm eff}^{\rm tube}$ develops a **true minimum** in a parameter window-your acceptance criteria mirror Bordag.&#x20;

---

### A5) **FRW macro coupling** (units, causality, conservation)

Embed with a transfer current $J^\nu$ so that $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$, use a **retarded kernel** for $\dot S_{\rm hor}$ (causal support), and partition the source by $p_i$ (softmax on dimensionless micro inputs). Monitor small parameters $\epsilon_{\rm DE}\equiv[(\alpha_h/V_c)\dot S_{\rm hor}]/(3H\rho_\Lambda)$ and $f_{\rm inj}\equiv[p_{\rm DM}(\varepsilon_h/V_c)\dot S_{\rm hor}]/(3H\rho_{\rm DM})$. Your units map $(\phi_0,\tau,a)\Rightarrow\{g_3,m,c\}$ keeps everything consistent.  &#x20;

---

## B) Wire‑in plan (production‑grade, minimal surface area)

Below are narrowly‑scoped modules and CI tests. Names match your current layout; all are additive.

### B1) **WaveEFT core** (replace heuristics with physics)

* **File:** `physics/scalar_eft.py`
* **API:**

  * `class ScalarEFT(mu, lam, gamma, J, a, tau)`
  * `def accel(phi): return c2*laplacian(phi) - (gamma*phi**2 + lam*phi**3 - mu**2*phi)`
  * `def step(phi, phi_dot, dt):` leapfrog with CFL guard $dt \le \mathrm{CFL}\,a/c$, $c=\sqrt{2Ja^2}$.
  * `def energy_density(phi, phi_dot):` (diagnostics).
* **CI tests:** dispersion check (fit $\omega(k)$) and mass gap $m_\mathrm{eff}=\sqrt{2}\mu$. &#x20;

### B2) **Optional complex field (hydro mode)**

* **File:** `physics/complex_eft.py`
* **API:** same shape as `ScalarEFT` but with complex `Phi`.
* **Helper:** `madulung(Phi) -> (n, u)` to expose $(n,\mathbf u)$ for hydro diagnostics.
* **CI:** continuity $\partial_t n+\nabla\cdot(nu)=0$ (finite‑volume residual < tol).

### B3) **Retarded kernels & FRW banner**

* **Files:**

  * `physics/kernels.py`: `Kret_Step(c)`, `convolve_retarded(s_loc, K)`
  * `cosmo/voxtrium.py`: FRW continuity with partitions $p_i$, $J^\nu$, monitors for $\epsilon_{\rm DE}, f_{\rm inj}$.
* **CI:** $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$ (machine zero); support strictly inside the light cone.&#x20;

### B4) **Finite‑tube solver (Bordag‑style)**

* **Files:**

  * `physics/cylinder_modes.py` → root‑finder for the secular equation; returns $\{\kappa_{\ell n}\}$, normalized $u_{\ell n}(r)$.
  * `physics/condense_tube.py` → build quartic overlaps $N_4$, find condensate $v_{\ell n}$, Hessian eigenvalues, scan $E(R)$.
* **CI:** (i) discrete $\kappa_\ell(R)$ tower; (ii) post‑condensation mass matrix $\succeq 0$; (iii) detect a true $E(R)$ minimum in at least one parameter window.&#x20;

### B5) **Memory steering (dimensionless law)**

* **File:** `core/memory_steering.py`
* **API:**

  * `update_memory(m, r, L, gamma, delta, kappa, dt)`
  * `transition_probs(i, nbrs, m, theta)` (softmax, matches logistic fork law)
  * `curvature_metrics(path)` (turn‑angle estimator).
* **CI:** reproduce (i) **junction logistic** slope $k\approx 1$ after rescaling by $\Theta \Delta m$, (ii) **curvature ∝ \Theta|\nabla m|)** collapse.&#x20;

### B6) **Monitors for invariants/dissipation**

* **File:** `core/diagnostics.py`
* **Add:** compute $Q_{\rm FUM}$ (on‑site), and the Lyapunov $\mathcal L_\mathrm{net}[W]$ descent rate; fail CI if $\dot{\mathcal L}_\mathrm{net}>0$ persistently.&#x20;

---

## C) Parameterization & guards (so it’s stable and fast)

* **CFL/aliasing:** enforce $dt \le 0.4\,a/c$ and spectral cutoff at $k_{\max}=0.3/a$; then higher‑derivative contamination stays $<1\%$ (Sec. A1).
* **Boundedness:** parse‑time assert $\lambda>0$ (quartic stabilizes tachyon onset).&#x20;
* **Hydro mode toggle:** default **off** (real scalar). Expose `--complex` flag to turn on $\Phi$ and hydrodynamic diagnostics if/when you want fluid behavior.
* **FRW smallness:** warn if $\epsilon_{\rm DE}>\delta_w$ or $f_{\rm inj}>f_\mathrm{max}$ per epoch.&#x20;

---

## D) Why this improves “intelligence” (mechanism, not heuristics)

1. **Coherent memory**: bounded EFT + tachyon stabilization → **tubes/filaments** as dynamically selected, long‑lived structures (“working memory” in the physics).&#x20;
2. **Causal adaptation**: retarded kernels enforce light‑cone responses; the system can *only* integrate usable signals-no acausal hacks.&#x20;
3. **Goal‑directed routing**: the memory field $M$ biases paths by a simple variational principle (Fermat), giving you stable logistic decisions and curvature control with **one** dimensionless slope $\Theta$.&#x20;
4. **Hydro option**: when enabled, real **continuity/Euler** dynamics appear from $\Phi$, unlocking vortices and circulation-richer “skills” with no learned rules.

---

## E) Acceptance checklist (merge when these pass)

* **EFT spine:** dispersion fit $\omega^2=m^2+c^2k^2+O(k^4)$ with $|O(k^4)/k^2|<1\%$ at $k\le0.3/a$; $m_\mathrm{eff}=\sqrt{2}\mu$ within 1%.&#x20;
* **Invariant/Lyapunov:** $Q_{\rm FUM}$ constant per node (to numeric tol), $\dot{\mathcal L}_\mathrm{net}\le 0$ run‑wide.&#x20;
* **Tubes:** $N_{\rm tach}(R)$ counted; condensate found; **all** Hessian eigenvalues $\ge 0$; a true $E(R)$ minimum exists in at least one slice.&#x20;
* **FRW:** conservation identity holds to machine zero; $|w_\mathrm{eff}+1|\le \delta_w$; $f_{\rm inj}\ll 1$.&#x20;
* **Steering signatures:** logistic slope $k\in[0.9,1.1]$; curvature $R^2\ge0.9$ vs. $\Theta|\nabla m|$.&#x20;

---

## F) Short “how‑to” for your repo (PR text you can paste)

1. **Add** `physics/scalar_eft.py`, `physics/kernels.py`, `cosmo/voxtrium.py`.
2. **Add** (optional) `physics/complex_eft.py`.
3. **Add** `physics/cylinder_modes.py`, `physics/condense_tube.py`.
4. **Add**/wire `core/memory_steering.py`, extend `core/diagnostics.py`.
5. **Tests** under `tests/physics/` and `tests/cosmo/` to check items in Section E.

All of this is consistent with your single consolidated derivations and their “strong vs weak” inventory; it operationalizes the open items precisely. &#x20;

---

### One‑liners you can cite in the paper/docs

* **Kinetic normalization**: $Z(\phi)=\tfrac12$, $c^2=2Ja^2$ from the discrete action, no microscopic tie of $J$ to $a$ required.&#x20;
* **EFT safety**: leading lattice artifacts scale as $O(a^2,\Delta t^2)$ → irrelevant for $k\ll1/a$.&#x20;
* **On‑site invariant** exists (log form); naive lattice Hamiltonian is **not** the invariant → UV **dissipation** with a valid Lyapunov. &#x20;
* **Finite tubes**: Bordag‑style secular equation, quartic stabilization, non‑negative Hessian, $E(R)$ minimum-pipeline specified and testable.&#x20;
* **Macro embedding**: FRW with transfer current + retarded kernel, units‑rigorous; smallness parameters $\epsilon_{\rm DE}, f_{\rm inj}$ control viability. &#x20;

---

If you want, I can next draft the exact `ScalarEFT` and `cylinder_modes` implementations with unit tests inline, but the plan above is sufficient to start merging.
