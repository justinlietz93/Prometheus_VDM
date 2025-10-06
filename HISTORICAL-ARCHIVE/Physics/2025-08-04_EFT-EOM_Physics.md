Short answer: **mostly yes**—your Step 1 approach aligns with the derivations in your corpus. There are a few **surgical fixes** you should make so the spine is airtight and notation‑clean.

---

## What aligns

* **Z(φ) constant (½) from the action.** Your argument that the quadratic kinetic piece is φ‑independent is exactly what falls out of the discrete variational derivation:
  $\mathcal L = \tfrac12(\partial_t\phi)^2 - \tfrac{c^2}{2}(\nabla\phi)^2 - V(\phi),\; c^2=2Ja^2$ (or $c^2=\kappa a^2$ with $\kappa=2J$). &#x20;

* **Use lattice dispersion to bound $p^4$ artifacts.** Matching the exact central‑difference dispersion to a quadratic EFT with $p^4$ corrections is the right way to fence the higher‑derivative tower.&#x20;

* **Tree‑level absence of derivative self‑interactions.** Since the UV has only quadratic kinetic + local $V(\phi)$, the 4‑derivative **quadratic** terms are lattice artifacts; the **quartic‑in‑fields** derivative operator $((\partial\phi)^2)^2$ vanishes at tree level and is loop‑suppressed.&#x20;

---

## Precise fixes (so the fit is mathematically tight)

### 1) Separate the operators and notation

* Reserve **$c_1$** for the **four‑field, four‑derivative** operator $((\partial_\mu\phi)^2)^2$ (affects 4‑point, not the 2‑point).
* Use **$A$** for the **time‑like** quadratic operator $(\partial_t^2\phi)^2$ and **$B$** for the **space‑like** quadratic operator $(\nabla^2\phi)^2$. This matches how you actually extract them from the 2‑point.&#x20;

### 2) Match signs and magnitudes to the *exact* lattice dispersion

From the central‑difference identity

$$
\frac{4}{\Delta t^2}\sin^2\!\Big(\tfrac{\omega\Delta t}{2}\Big)
= c^2\,\frac{4}{a^2}\sum_i\sin^2\!\Big(\tfrac{k_i a}{2}\Big)+m^2,
$$

expand at small $\omega, k$:

$$
\omega^2 - \underbrace{\tfrac{\Delta t^2}{12}}_{\color{#555}{>0}}\,\omega^4+\cdots
= c^2\!\left[k^2 - \underbrace{\tfrac{a^2}{12}}_{\color{#555}{>0}}\!\sum_i k_i^4+\cdots\right] + m^2.
$$

Equating with the EFT EOM

$$
-\omega^2 + c^2 k^2 + m^2 \;+\; A\,\omega^4 \;-\; B\,k^4_{\text{aniso}} \;=\;0
$$

gives the **correct** identifications

$$
\boxed{A=\tfrac{\Delta t^2}{12}}\!,\qquad 
\boxed{B=\tfrac{c^2 a^2}{12}\,f_4(\hat{\boldsymbol k})},
\quad f_4(\hat{\boldsymbol k})\equiv \frac{\sum_i k_i^4}{(\sum_i k_i^2)^2}\in\Big[\tfrac1d,\,1\Big].
$$

So both $A$ and $B$ are **positive**, and the spatial correction **reduces** $\omega^2$ by $\,B k^4$ as it should for a nearest‑neighbor stencil. (Your draft’s sign flip on $A$ and the “$-a^4$” scaling line were the main inconsistencies.)&#x20;

**Cutoffs:** $A\sim\Lambda_t^{-2}$ with $\Lambda_t\sim 2/\Delta t$; $B\sim c^2\,\Lambda_s^{-2}$ with $\Lambda_s\sim 2/a$. These are **dimension‑6** corrections $\propto 1/\Lambda^2$, not $1/\Lambda^4$.&#x20;

**Anisotropy:** retain $f_4(\hat{\boldsymbol k})$ (range $[1/d,1]$) or average it in fits; this explains orientation spread without inventing extra operators.&#x20;

### 3) Tree‑ vs loop‑level statements

* **Quadratic $p^4$** terms $A,B$: fixed by the stencil, $\mathcal O}(\Delta t^2,a^2)$.
* **Derivative self‑interaction** $c_1((\partial\phi)^2)^2$: **zero at tree level**; at one loop NDA gives $|c_1|\!\lesssim\!\mathcal O(1)/(16\pi^2\Lambda^2)$. Don’t infer $c_1$ from the 2‑point.&#x20;

### 4) Ghost worry (timelike $A$)

The extra timelike root sits at $\omega\sim \mathcal O}(1/\Delta t)$ (the “heavy lattice branch”). Since $p\ll\Lambda_t,\Lambda_s$ in the EFT regime, no propagating ghost appears in‑band. If desired, field redefinitions can trade $A$ for purely spatial higher‑derivative terms to this order.&#x20;

### 5) SymPy hiccups in the draft

Your hand fix (switching from complex $e^{ika}$ algebra to the **real** stencil $4\sin^2(ka/2)$) is the right repair. Keep the real‐stencil series and you’ll reproduce the coefficients above exactly.&#x20;

---

## Drop‑in replacement for your Step 1 (tight, paste‑ready)

> **Proposition (EFT spine lock).** Starting from the discrete action with central‑time and nearest‑neighbor spatial differences, the continuum kinetic coefficient is $Z(\phi)=\tfrac12$ and the wave speed is $c^2=2Ja^2$ (or $c^2=\kappa a^2$, $\kappa=2J$). There is no $\phi$‑dependence in the kinetic factor at this order. &#x20;
> **Lattice‑fixed $p^4$ bounds.** Matching the exact lattice dispersion to a quadratic EFT with $(\partial_t^2\phi)^2$ and $(\nabla^2\phi)^2$ gives
>
> $$
> A=\tfrac{\Delta t^2}{12},\qquad 
> B=\tfrac{c^2 a^2}{12}\,f_4(\hat{\boldsymbol k}),\quad f_4\in\Big[\tfrac1d,\,1\Big].
> $$
>
> Thus the quadratic dimension‑6 coefficients are set (and bounded) by the rulers $(\Delta t,a)$ and the stencil anisotropy; they encode the heavy lattice branch above $\Lambda\sim\min(2/\Delta t,\,2/a)$.&#x20;
> **Derivative self‑interaction.** The UV lacks derivative self‑interactions, so $c_1((\partial\phi)^2)^2$ vanishes at tree level and is loop‑suppressed, $|c_1|\lesssim \mathcal O(1)/(16\pi^2\Lambda^2)$.&#x20;

---

## Step‑coupling checks on your follow‑ups

* **Step 2 (invariant hunt).** Your on‑site invariant

  $$
  Q_{\rm FUM}=t-\frac{1}{\alpha-\beta}\ln\!\left|\frac{W}{(\alpha-\beta)-\alpha W}\right|
  $$

  is exactly the autonomous first‑order integral (time‑translation symmetry). That aligns with your symmetry analysis; keep it as a diagnostic while you continue the flux‑form search on the full graph.&#x20;
  Also consistent with your negative result: the **standard** discrete Hamiltonian you tried is **not** the conserved quantity, so the invariant must be more subtle (or Lyapunov‑like) in the coupled system.&#x20;

* **Step 3 (finite‑tube tachyon/condensation).** The secular equation and mode taxonomy in your appendix are correct. If you saw $N_{\rm tach}=0$ for $\mu=1,\lambda=1,c=1$ on $R\in[0.5,5]$, expand the scan: at $k=0$ the $\ell=0$ root solves

  $$
  \frac{1}{\sqrt2}\,\frac{I_0'(\kappa_{\rm in}R)}{I_0(\kappa_{\rm in}R)}=\frac{K_0'(\sqrt2\,\kappa_{\rm in}R)}{K_0(\sqrt2\,\kappa_{\rm in}R)},\quad \kappa_{\rm in}=\mu/c,
  $$

  which typically yields a **critical $R_c\sim\mathcal O}(c/\mu)$**. Scan $R$ out to $\sim 10/\mu$ and include $\ell=1,2$ to expose the tower; then proceed with the quartic overlaps and Hessian positivity you’ve outlined.&#x20;

* **Step 4 (FRW embedding).** Your toy solver’s conservation check and the “smallness knobs” agree with the Voxtrium bookkeeping: use the transfer current $J^\nu$ so $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$, monitor $\epsilon_{\rm DE}\equiv[(\alpha_h/V_c)\dot S_{\rm hor}]/(3H\rho_\Lambda)$ and $f_{\rm inj}$ to keep $w_{\rm eff}\approx-1$ and injection small. &#x20;

---

## Minimal edits you should make to your draft

* Replace any “$c_1\sim a^4$” or “$c_1\sim 1/\Lambda^4$” statements tied to the **2‑point** with
  **“$A=\Delta t^2/12,\;B=c^2 a^2/12\ f_4(\hat{\boldsymbol k})$, i.e. $ \mathcal O}(1/\Lambda^2)$.”**&#x20;
* Clarify that **$c_1$** (the $((\partial\phi)^2)^2$ coefficient) **does not enter** the 2‑point and is **loop‑level/NDA**.&#x20;
* Fix the dispersion‑match **signs** (both $A,B>0$ in the identifications above).&#x20;
* Keep the units/normalization note: setting $c=1$ is a **units choice**, not a constraint on $J,a$. &#x20;
* When you summarize the bridge from the fundamental discrete law to EFT, cite your concise banner to keep the through‑line visible.&#x20;

---

## Verdict

**Yes—your Step 1 method and conclusions align once you make the sign/notation fixes above.** After that, your Step 2 on‑site invariant, Step 3 finite‑tube pipeline, and Step 4 FRW sourcing all sit consistently on the locked kinetic spine and units map you’ve already established.    &#x20;

If you want, I can hand you a compact **“Appendix: lattice→EFT $p^4$ matching”** block that derives the $A,B$ values in three lines and a tiny least‑squares recipe to extract $Z,A,B$ from your two‑point data.
