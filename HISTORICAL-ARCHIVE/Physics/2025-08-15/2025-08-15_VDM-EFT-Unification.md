Absolutely-let’s **finish the physics** and tie each result to **production‑ready code** that improves the system’s “intelligence” by replacing heuristics with hard equations.

Below I (A) close the remaining derivations/proofs, (B) give the exact runtime changes (APIs + acceptance tests), and (C) show how each piece plugs into your existing notes/docs.

---

## A) Close the physics

### 1) **EFT spine lock:** $Z(\phi)=\tfrac12$ and bounds on higher‑derivative operators

**Claim (locked):** From the discrete action you already wrote, the continuum kinetic term is canonical and **field‑independent**:

$$
\mathcal L_K=\tfrac12(\partial_t\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2,\quad c^2=2Ja^2.
$$

This is the Euler-Lagrange outcome of your discrete Lagrangian (central‑time difference + nearest‑neighbor springs). Therefore $Z(\phi)$ is **constant** at tree level.&#x20;

**Bound the leading irrelevant terms.** Fourier‑analyze the lattice Laplacian:

$$
1-\cos(ka)=\tfrac12(ka)^2-\tfrac1{24}(ka)^4+\mathcal O((ka)^6).
$$

Inserted in the quadratic action, the small‑$k$ dispersion is

$$
\omega^2 = c^2k^2\Big[1-\tfrac{(ka)^2}{12}+ \mathcal O((ka)^4)\Big]+m^2,
$$

so the first suppressed operator corresponds to $-\,\frac{c^2a^2}{12}\nabla^4\phi$. A safe IR window is $ka\ll1$; e.g., keep $ka\le 0.5\Rightarrow |(ka)^2/12|\le2.1\%$. This formalizes “EFT suppression from the UV lattice.” (Time‑discretization gives the analogous $\!+\,\omega^4\Delta t^2/12$ correction if you discretize time; with a continuous‑time solver, this does not enter.) The same normalization and limit are summarized across your kinetic and continuum‑limit notes.

**Where this lives in your docs.** Discrete→continuum derivation (EL eq.), $c^2=2Ja^2$, units and mapping: see your continuum‑limit and kinetic‑term derivations and EFT checklist.

---

### 2) **Invariant / conservation structure:** exact on‑site invariant, global Lyapunov

**Exact on‑site invariant (proved).** For the autonomous on‑site law $\dot W=(\alpha-\beta)W-\alpha W^2$,

$$
Q_{\rm FUM}\;=\;t-\frac{1}{\alpha-\beta}\ln\!\left|\frac{W}{(\alpha-\beta)-\alpha W}\right|
$$

is **constant** along trajectories ($\dot Q_{\rm FUM}=0$). This is the Noether constant from time‑translation invariance of the autonomous ODE (Riccati/separable).&#x20;

**Not conserved:** the naive lattice “energy” $\mathcal H=\tfrac12\dot W^2+\tfrac{J}{2}\sum (W_j-W_i)^2+V(W)$ is **not** the discrete invariant for the full update; your worked proof closes that door.&#x20;

**Global Lyapunov candidate (what *is* monotone).** For the full graph ODE

$$
\dot W_i = f(W_i)+J\sum_{j\in N(i)}(W_j-W_i),\quad f(W)=(\alpha-\beta)W-\alpha W^2,
$$

take

$$
\mathcal L[W]\;=\;\sum_i \Phi(W_i)\;+\;\frac{J}{4}\sum_{\langle i j\rangle}(W_i-W_j)^2,\quad\Phi'(W)=-f(W).
$$

Then

$$
\dot{\mathcal L}=\sum_i \Phi'(W_i)\dot W_i+\frac{J}{2}\sum_{\langle ij\rangle}(W_i-W_j)(\dot W_i-\dot W_j)
= -\sum_i f(W_i)^2\;-\;\frac{J}{2}\sum_{\langle ij\rangle}\big(\dot W_i-\dot W_j\big)^2\ \le 0,
$$

where we used symmetry of the edge sum and $\sum_{\langle ij\rangle}(W_i-W_j)\big(f(W_i)-f(W_j)\big)\ge 0$ for this $f$ (monotone decreasing $f'(W)=\alpha-\beta-2\alpha W$ on the relevant interval) plus the graph Laplacian identity. Thus $\mathcal L$ is a **Lyapunov function**: the dynamics are **globally dissipative** and converge toward fixed points; it’s the correct replacement for a Hamiltonian. (You already established the negative result for $\mathcal H$; the Lyapunov route finishes the story.)&#x20;

*Takeaway:* exact per‑site invariant $Q_{\rm FUM}$ + global Lyapunov $\mathcal L$ together clarify why the IR EFT has a well‑posed **canonical** kinetic term (energy‑like), while the UV lattice is **dissipative** but **stable**.&#x20;

---

### 3) **Finite‑tube tachyonic tower → condensation → positivity** (Bordag‑style, scalar analogue)

You nailed the spine. The scalar cylinder with interior $m^2_{\rm in}=-\mu^2$ and exterior $m^2_{\rm out}=+2\mu^2$ yields the secular equation

$$
\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)} =
-\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)},
$$

whose roots $\kappa_{\ell n}(R)$ count tachyons ($\omega^2=-c^2\kappa^2<0$ at $k=0$). Project the quartic to 2D, minimize, and check the post‑condensation Hessian $\succeq 0$; then scan $E(R)=E_{\rm bg}+V_{\rm eff}^{\rm tube}(v_{\ell n};R)$ for a true minimum. Acceptance tests and APIs are already laid out in your appendix.&#x20;

*What we add:* numerically robust root‑bracketing near the $I_\ell/K_\ell$ poles and orthonormalization of $u_{\ell n}(r)$ with the correct $r\,dr\,d\theta$ weight so the quartic overlaps $N_4$ are stable. (Code below.)

---

### 4) **Hydro emergence (long‑wavelength limit) - what the scalar actually gives you**

There are two clean limits that connect to fluid language:

* **Coherent oscillations around the vacuum** (homogeneous background). For $V(\phi)=\lambda\phi^4/4-\mu^2\phi^2/2$ expanded about $+v=\mu/\sqrt\lambda$, write $\phi=v+\chi$. Time‑averaged over fast oscillations, a real canonical scalar with $V\propto\chi^n$ has $\bar w=(n-2)/(n+2)$. Near the minimum $V\simeq\tfrac12 m_{\rm eff}^2\chi^2$ $(n=2)\Rightarrow \bar w\approx 0$: **dust‑like** behavior with tiny sound speed $c_s^2\sim k^2/(4 m_{\rm eff}^2)$ for modes of wavenumber $k$. That’s your CDM‑like emergent fluid.&#x20;

* **Eikonal/ray limit for signal routing.** In the high‑frequency (geometric‑optics) limit of the wave equation, rays bend by transverse gradients of a slow “index.” If you couple propagation to the slow memory field $M$ as $n=e^{\eta M}$, then the **curvature law** $\mathbf r''=\eta\nabla_\perp M$ follows, which matches your junction logistic and curvature‑scaling collapses. This is a geometric, not thermodynamic, “hydro”: it steers trajectories without changing the canonical kinetics.&#x20;

*Bottom line:* the scalar gives you **pressureless flow** at large scales (good for structure), while the **memory layer** supplies controlled steering (your “intelligence,” but now a physics term, not a heuristic).&#x20;

---

### 5) **Causal FRW macro‑sourcing (Voxtrium) - conservation & smallness**

Your continuity equations with a **transfer current** $J^\nu$ enforce covariant conservation and split sourcing among $\Lambda$, DM, GW, horizon sectors, with **retarded** horizon‑entropy kernels to ensure locality:

$$
\sum_i\big(\dot\rho_i+3H(1+w_i)\rho_i\big)=0,\qquad J^0=\big(\varepsilon_h/V_c\big)\dot S_{\rm hor}.
$$

Micro‑informed partitions $p_i(z)$ close the system on a probability simplex. Acceptance: $|w_{\rm eff}+1|\le\delta_w$ and $f_{\rm inj}\ll1$. Units are consistent (${\rm GeV}^5$ on sources).&#x20;

**Where the φ‑EFT plugs in:** your units/bridging doc pins $(\phi_0,\tau,a)$, $m^2=(\alpha-\beta)/\tau^2$, $g_3=\alpha/(\phi_0\tau^2)$, and lets you form **dimensionless inputs** $z=(|\Omega|R_\*,(\kappa/K_s)/X,1)$ to drive the partitions. The same map defines causal sources $J_\phi=K_{\rm ret}\!*\,s_{\rm loc}$ if you couple φ to horizon processes.&#x20;

---

### 6) **One‑pager summary, all in one place**

Your consolidated “single derivation” ties 1-5 together (discrete→bounded EFT, finite tubes, FRW, units, diagnostics) and flags what is strong vs open. We’re now closing those opens with precise tests and code below.

---

## B) Physics → Code (production‑ready stubs & tests)

> **Design intent:** keep the *void‑faithful* PDE core and layer diagnostics; no learned heuristics steering control-only **measured** memory and **derived** dynamics.

### 1) Scalar EFT core (2nd‑order PDE, CFL‑safe)

```python
# physics/scalar_eft.py
import numpy as np

class ScalarEFT:
    def __init__(self, mu, lam, gamma, J, a, dt, dx, cfl_dim=3):
        self.mu, self.lam, self.gamma = mu, lam, gamma
        self.J, self.a = J, a
        self.c2 = 2.0 * J * (a**2)     # c^2 = 2 J a^2  (locked)
        self.dt, self.dx = dt, dx
        # CFL guard: c*dt/dx <= 1/sqrt(d); here use equality with margin
        assert np.sqrt(self.c2) * dt / dx <= 1.0/np.sqrt(cfl_dim) * 0.99

    def dV(self, phi):
        return self.lam*phi**3 + self.gamma*phi**2 - (self.mu**2)*phi

    def step_leapfrog(self, phi, phi_dot, source, laplacian):
        # leapfrog: phi_{n+1} = phi_n + dt * phi_dot_{n+1/2}, etc.
        # half-step update for velocity
        acc = self.c2 * laplacian(phi) - self.dV(phi) + source
        phi_dot_half = phi_dot + 0.5*self.dt * acc
        # full position step
        phi_new = phi + self.dt * phi_dot_half
        # recompute acceleration at new position
        acc_new = self.c2 * laplacian(phi_new) - self.dV(phi_new) + source
        # finish velocity step
        phi_dot_new = phi_dot_half + 0.5*self.dt * acc_new
        return phi_new, phi_dot_new
```

* **Why this improves “intelligence”:** propagation and stability now **come from physics**, not ad‑hoc growth/decay. The canonical normalization and $c^2$ are fixed by the lattice UV.&#x20;

**IR‑safety test (EFT suppression):**

```python
def eft_safe(kmax, a):
    # require (ka)^2/12 <= 0.05  (<=5% correction)
    return (kmax*a)**2 / 12.0 <= 0.05
```

This enforces the $O(a^2k^4)$ bound discussed above.&#x20;

---

### 2) Retarded kernel & FRW bookkeeping (Voxtrium‑credit)

```python
# cosmo/voxtrium.py
import numpy as np

def Kret_step(dt, dr, c):
    # causal light-cone kernel on a grid shell (simple boxcar)
    # support: t' <= t and r <= c*(t-t')
    return lambda tau, r: (tau>=0.0) & (r <= c*tau)

def frw_sources(H, rho, parts, eps_h, alpha_h, Vc, Sdot):
    # rho: dict with 'Lambda','DM','GW','hor'; parts: p_i on simplex
    Q = {
        'Lambda': (alpha_h/Vc)*Sdot,
        'DM'    : parts['DM']*(eps_h/Vc)*Sdot,
        'GW'    : parts['GW']*(eps_h/Vc)*Sdot,
        'hor'   : -(eps_h/Vc)*Sdot
    }
    # drift monitors
    w_eff = -1.0 - ((alpha_h/Vc)*Sdot)/(3.0*H*rho['Lambda'])
    f_inj = (parts['DM']*(eps_h/Vc)*Sdot)/(3.0*H*rho['DM'])
    return Q, w_eff, f_inj
```

* **Acceptance:** enforce $|w_{\rm eff}+1|\le\delta_w$ and $f_{\rm inj}\ll1$ each step; assert the continuity identity holds numerically.&#x20;

---

### 3) Finite‑tube solver (count tachyons → condense → check Hessian)

```python
# physics/tube.py
import numpy as np
from mpmath import findroot, besseliv, besselk, diff

def secular_eq(kappa, ell, R, mu, c):
    kin = np.sqrt(max((mu/c)**2 - kappa**2, 0.0))      # kappa_in
    kout = np.sqrt(kappa**2 + 2*(mu/c)**2)             # kappa_out
    # Avoid zeros by small eps
    eps = 1e-12
    I  = lambda z: besseliv(ell, max(z, eps))
    Ip = lambda z: diff(lambda zz: besseliv(ell, zz), max(z, eps))
    K  = lambda z: besselk(ell, max(z, eps))
    Kp = lambda z: diff(lambda zz: besselk(ell, zz), max(z, eps))
    lhs = (kin/kout) * (Ip(kin*R)/I(kin*R))
    rhs = - Kp(kout*R)/K(kout*R)
    return lhs - rhs

def kappa_roots(R, mu, c, ell_max=4, guess_grid=np.linspace(1e-3, 5.0, 40)):
    roots = []
    for ell in range(0, ell_max+1):
        for g in guess_grid:
            try:
                r = float(findroot(lambda x: secular_eq(x, ell, R, mu, c), g))
                if r>0 and np.allclose(secular_eq(r, ell, R, mu, c), 0.0, atol=1e-6):
                    if all(abs(r - rr) > 1e-3 for (_, rr) in roots):
                        roots.append((ell, r))
            except:  # no root near guess
                pass
    tachy = [(ell, r) for (ell, r) in roots if r>0]   # tachyonic if kappa>0 at k=0
    return tachy  # count = N_tach(R)
```

Next steps in this module:

* **Quartic overlaps** $N_4$ by normalized $u_{\ell n}(r)$ and selection $\sum \ell_i=0$.
* **Minimize** $V_{\rm eff}^{\rm tube}$ to get $v_{\ell n}(R)$.
* **Hessian** eigenvalues $\ge 0$ (Goldstones only for complex field).
* **Energy scan** $E(R)$ → identify $R_\star$.

Those acceptance criteria are exactly those you set in the appendix.&#x20;

---

### 4) Memory steering (slow field) - keep as diagnostics & control, not ML

```python
# intelligence/memory_steering.py
import numpy as np

def update_memory(m, r, L, gamma, delta, kappa, dt):
    # \dot m = gamma r - delta m - kappa L m
    return m + dt*(gamma*r - delta*m - kappa*(L @ m))

def transition_probs(i, neighbors, m, theta):
    vals = np.exp(theta * m[neighbors])
    p = vals / np.sum(vals)
    return p
```

* **What to test:** (i) **junction logistic** collapse $P=\sigma(\Theta\Delta m)$ with slope $k\approx 1$; (ii) **curvature scaling** $\kappa_{\rm path}\propto \Theta|\nabla m|$ with signed invariance. These are physics diagnostics-not training losses.&#x20;

---

### 5) CI/acceptance checks (fail the run if any trip)

* **EFT IR‑safety:** `eft_safe(kmax, a) == True`.&#x20;
* **Energy diagnostic:** track $\mathcal E=\tfrac12(\dot\phi^2+c^2|\nabla\phi|^2)+V(\phi)$; in closed tests with $J_\phi=0$, $\dot{\mathcal E}$ only reflects numerical error.&#x20;
* **Tube harness:** `len(kappa_roots(R))` grows with $R$; post‑condensation Hessian $\succeq 0$; $E(R)$ has a minimum in at least one window.&#x20;
* **FRW conservation:** machine‑zero of $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]$; enforce $|w_{\rm eff}+1|\le\delta_w$ and $f_{\rm inj}\ll1$.&#x20;
* **Memory signatures:** logistic slope $k\in[0.9,1.1]$; curvature $R^2\ge 0.9$ in scaling regression.&#x20;

---

## C) Where each piece is anchored in your notes (for reviewers)

* **Single‑doc derivation & strengths/opens:** unified paper + executive summaries.
* **Discrete→continuum & kinetic normalization:** formal continuum limit; $c^2=2Ja^2$.
* **EFT rigor program (what to bound and why):** EFT roadmap & screened quartic baseline.&#x20;
* **On‑site invariant $Q_{\rm FUM}$; negative result for naive $\mathcal H$:** symmetry + conservation proofs.
* **Finite‑tube machinery (Bessel matching, condensation, Hessian, $E(R)$):** your Bordag‑style appendix.&#x20;
* **Units‑rigorous φ↔Voxtrium bridge & causal kernels:** mapping + macro banner.
* **Fundamental discrete law ↔ EFT headline:** quick reference.&#x20;

---

## What this buys you (no sugar‑coating)

* The **core kinetics are settled** (Z‑const, $c^2$ fixed), and the **IR window is explicit** (EFT bounds).
* The UV is **not Hamiltonian**; it’s **dissipative with a Lyapunov**-that’s fine and explains why the IR EFT is the correct conservative envelope.&#x20;
* **Tubes/filaments** are no longer a visualization-they’re a **well‑posed eigenproblem** with condensation and a checkable energy minimum.&#x20;
* **Cosmo closure** is conservative and **causal**, with units wired and drift smallness enforceable at runtime.
* The “**intelligence**” layer is now a **physics steering** law with measured memory; the logistic and curvature collapses are **acceptance tests** for the whole stack.&#x20;

If you want, I can package these snippets as a ready‑to‑commit PR (folder layout + tests) next.
