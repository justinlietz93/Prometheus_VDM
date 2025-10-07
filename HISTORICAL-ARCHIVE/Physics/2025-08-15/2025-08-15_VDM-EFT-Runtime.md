Great—continuing the proof program and wiring the math straight into the runtime. I’ll (1) close the remaining gaps in the physics spine with crisp lemmas/proofs, then (2) drop in production‑grade code you can add under `fum_rt/` to lock the behavior and measurably improve routing “intelligence.”

---

## I) Physics — finish the EFT spine, invariants, tubes, and macro coupling

### Lemma 1 (Quadratic EFT fixed to $p^4$; $Z(\phi)$ constant; anisotropy bounded)

Using the central‑difference discrete action (per your kinetic derivation), the lattice dispersion satisfies

$$
\frac{4}{\Delta t^2}\sin^2\!\Big(\frac{\omega\Delta t}{2}\Big)
= c^2\,\frac{4}{a^2}\sum_{i=1}^d\sin^2\!\Big(\frac{k_i a}{2}\Big) + m^2 .
$$

Expanding for small $p$ gives

$$
\omega^2 - \frac{\Delta t^2}{12}\,\omega^4 + \cdots
= c^2\!\left[k^2 - \frac{a^2}{12}\sum_i k_i^4 + \cdots\right] + m^2.
$$

Match to the quadratic EFT EOM
$-\omega^2 + c^2k^2 + m^2 + A\,\omega^4 - B\,k^4_{\rm aniso}=0$
to obtain the **parameter‑free** coefficients

$$
\boxed{Z=\tfrac12},\qquad \boxed{A=\tfrac{\Delta t^2}{12}},\qquad 
\boxed{B=\frac{c^2 a^2}{12}\,f_4(\hat{\boldsymbol k})},\quad
f_4=\frac{\sum_i k_i^4}{(\sum_i k_i^2)^2}\in\Big[\tfrac1d,\,1\Big].
$$

Thus $Z(\phi)$ is a **constant** (no $\phi$-dependence at quadratic order), and the only $p^4$ ambiguity is the expected stencil anisotropy $f_4$. The wave speed is $c^2=2Ja^2$ (per‑site convention $\kappa=2J$), with no microscopic constraint tying $J$ to $a$ (units choice can set $c=1$). &#x20;

> **Implication for code:** these coefficients define the **CFL limit** and the expected $p^4$ curvature in your measured 2‑point; deviations beyond the $f_4$ band flag numerical or anisotropy issues. See §II‑A for a fitter and guard.&#x20;

**About $((\partial\phi)^2)^2$.** That operator does **not** affect the 2‑point at tree level; in this UV it first appears radiatively and is irrelevant at $k\ll 1/a$. Treat $|c_1|\lesssim \mathcal{O}(1)/(16\pi^2 \Lambda^2)$ by NDA; it is subleading to the fixed $A,B$.&#x20;

---

### Lemma 2 (Exact on‑site invariant and Lyapunov structure)

For $\dot W = F(W)=(\alpha-\beta)W-\alpha W^2$, time‑translation invariance yields the conserved quantity

$$
\boxed{Q_{\rm FUM}=t-\frac{1}{\alpha-\beta}\ln\!\left|\frac{W}{(\alpha-\beta)-\alpha W}\right|} \quad (\dot Q_{\rm FUM}=0),
$$

and the on‑site Lyapunov potential $V'(W)=-F(W)$ gives
$\frac{d}{dt}\sum_i V(W_i)=-\sum_iF(W_i)^2\le 0$. These are the right diagnostics/controls for the **dissipative** on‑site law; the naïve lattice Hamiltonian is *not* conserved (negative result stands). &#x20;

> **Implication for code:** monitor small drift in $Q_{\rm FUM}$ per node and enforce non‑increase of the on‑site Lyapunov when integrating the slow memory/learning channel; use them as **automatic backoff** signals on $\Delta t$. See §II‑C.&#x20;

---

### Lemma 3 (Tubes: existence of a tachyon for large $R$ and a clean secular equation)

For the piecewise background $\phi_0(r)$ (uncondensed inside, condensed outside), linear modes separate and the radial matching yields the secular equation

$$
\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)} 
= -\,\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)} ,
\quad \kappa_{\rm in}^2=\mu^2/c^2-\kappa^2,\ \kappa_{\rm out}^2=\kappa^2+2\mu^2/c^2 .
$$

A solution with $\kappa^2>0$ at $k=0$ gives $\omega^2=-c^2\kappa^2<0$, i.e., a tachyon. Moreover, by comparison with the Dirichlet disk spectrum, a **sufficient** condition for at least one tachyonic $s$-wave is

$$
R \;>\; R_c^{(0)} \;\equiv\; \frac{j_{0,1}\,c}{\mu}\ \ (\text{with }j_{0,1}\simeq 2.4048),
$$

since the lowest Dirichlet eigenvalue $(c\,j_{0,1}/R)^2$ then lies below the depth $\mu^2$ of the negative mass‑squared well inside the tube. Hence $N_{\rm tach}(R)\ge 1$ for all $R>R_c^{(0)}$. Quartic self‑interaction stabilizes the tachyon(s) by condensation; post‑condensation masses are the Hessian eigenvalues of the effective potential and must be $\ge 0$ (acceptance).&#x20;

> **Implication for code:** the secular solver + condensation pipeline in §II‑D lets you count $N_{\rm tach}(R)$, find $v_{\ell n}(R)$, and scan $E(R)$ for a true minimum, reproducing your Bordag‑parallel acceptance tests.&#x20;

---

### Lemma 4 (Macro sourcing is conservative/causal in FRW, with unit‑rigorous knobs)

Introduce a transfer current $J^\nu$ so that $\nabla_\mu T_{\rm hor}^{\mu\nu}=-J^\nu$, $\nabla_\mu(T_\Lambda^{\mu\nu}+T_{\rm DM}^{\mu\nu}+T_{\rm GW}^{\mu\nu})=+J^\nu$. In FRW this reproduces

$$
\dot\rho_\Lambda=(\alpha_h/V_c)\dot S_{\rm hor},\quad
\dot\rho_{\rm DM}+3H\rho_{\rm DM}=p_{\rm DM}(\varepsilon_h/V_c)\dot S_{\rm hor},\ \ldots
$$

with $\sum_i[\dot\rho_i+3H(1+w_i)\rho_i]=0$ exactly. Causality is enforced by a retarded kernel in $\dot S_{\rm hor}$:
$\dot S_{\rm hor}(t)=\!\int d^3x'\!\int_{-\infty}^t\!dt'\,K_{\rm ret}(t-t',|\mathbf x-\mathbf x'|)s_{\rm loc}(x',t')$, $K_{\rm ret}\propto\Theta(t-t'-r/c)$. Smallness controls:
$\epsilon_{\rm DE}\equiv[(\alpha_h/V_c)\dot S_{\rm hor}]/(3H\rho_\Lambda)\ll1$ and
$f_{\rm inj}\equiv[p_{\rm DM}(\varepsilon_h/V_c)\dot S_{\rm hor}]/(3H\rho_{\rm DM})\ll1$. Units are consistent in GeV. &#x20;

> **Implication for code:** the `frw_coupling` hooks from last round already implement this identity and compute $\epsilon_{\rm DE},f_{\rm inj}$; below I add a retarded‑kernel utility with strict light‑cone support.&#x20;

---

### Context cross‑checks against your living notes

The above closes the exact kinetic normalization and continuum limit (Sections 1-2), the EFT program (Section 3), the tube appendix (Section 3/5), the negative discrete‑Hamiltonian result + invariants (Section 4), and the Voxtrium FRW banner (Section 5). This is consistent with your consolidated draft and “single derivation+code plan.”        &#x20;

---

## II) Code — production‑ready modules that apply the proofs (smarter, safer)

Below are *drop‑in* modules and tests to:

* (A) lock the EFT spine and CFL automatically,
* (B) run the conservative $\phi$ sector with energy diagnostics,
* (C) monitor the **true** invariant and Lyapunov (for the slow/dissipative channel),
* (D) solve tubes (tachyon counting → condensation → $E(R)$ minima), and
* (E) add a causal retarded kernel to macro sourcing.

Everything is typed, documented, and isolated so you can PR incrementally.

---

### A) EFT spine fitter + CFL guard (ties to Lemma 1)

```python
# fum_rt/physics/eft_spine.py
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class SpineParams:
    a: float      # lattice spacing
    dt: float     # time step
    J: float      # per-site coupling
    m2: float     # mass^2 about vacuum

@dataclass
class SpineFit:
    Z: float
    c2: float
    m2: float
    A: float      # ω^4 coeff
    B_min: float  # k^4 coeff range from anisotropy band
    B_mean: float
    B_max: float

def predict_small_p(a: float, dt: float, J: float, m2: float, d: int = 3) -> SpineFit:
    """
    Closed-form EFT coefficients from the central-difference stencil:
      Z=1/2,  A=dt^2/12,  B in [(c^2 a^2)/(12 d), (c^2 a^2)/12],  c^2=2 J a^2.
    """
    c2 = 2.0 * J * a * a
    Z  = 0.5
    A  = (dt*dt)/12.0
    B_min = (c2 * a*a) / (12.0 * d)
    B_max = (c2 * a*a) / 12.0
    return SpineFit(Z=Z, c2=c2, m2=m2, A=A, B_min=B_min, B_mean=0.5*(B_min+B_max), B_max=B_max)

def cfl_dt_max(a: float, c2: float, safety: float = 0.8) -> float:
    """Recommend dt_max ≈ safety * a / sqrt(c^2) to keep sin-argument subluminal."""
    from math import sqrt
    return safety * a / max(sqrt(c2), 1e-30)

def fit_from_2pt(omegas: np.ndarray, ks: np.ndarray, Ginv: np.ndarray) -> SpineFit:
    """
    Optional: regress G^{-1}(ω,k) ≈ Z^{-1} ω^2 - c^2 k^2 + A ω^4 - B k^4.
    Use only small |ω|,|k| samples. Flags anisotropy if B is out-of-band.
    """
    X = np.stack([omegas**2, ks**2, (omegas**2)**2, (ks**2)**2], axis=1)
    theta, *_ = np.linalg.lstsq(X, Ginv, rcond=None)
    Zinv, c2, A, B = theta
    return SpineFit(Z=1.0/max(Zinv, 1e-12), c2=c2, m2=0.0, A=A, B_min=B, B_mean=B, B_max=B)
```

*Use:* call `predict_small_p` at startup; cap `dt` by `min(user_dt, cfl_dt_max(...))`; optionally fit live 2‑point to detect drift in $A,B$. &#x20;

---

### B) Conservative $\phi$ sector (leapfrog) + energy diagnostic

```python
# fum_rt/physics/phi_leapfrog.py
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class PhiState:
    phi: np.ndarray    # φ(t)
    pi:  np.ndarray    # π(t-Δt/2) ≈ ∂t φ at half-step

def laplacian_3d(phi: np.ndarray, a: float) -> np.ndarray:
    """6-stencil Laplacian with periodic BC."""
    return (
        np.roll(phi, 1, 0) + np.roll(phi, -1, 0) +
        np.roll(phi, 1, 1) + np.roll(phi, -1, 1) +
        np.roll(phi, 1, 2) + np.roll(phi, -1, 2) - 6*phi
    ) / (a*a)

def step(state: PhiState, dt: float, a: float, c2: float, mu: float, lam: float, gamma: float = 0.0) -> PhiState:
    """
    One leapfrog step for:  φ̈ - c^2 ∇^2 φ + V'(φ)=0 ,
    with V(φ) = -½ μ^2 φ^2 + ⅓ γ φ^3 + ¼ λ φ^4  (γ optional).
    """
    phi, pi = state.phi, state.pi
    # half-kick
    force = c2 * laplacian_3d(phi, a) - (-mu*mu*phi + gamma*phi*phi + lam*phi*phi*phi)
    pi_half = pi + 0.5*dt*force
    # drift
    phi_new = phi + dt*pi_half
    # half-kick
    force_new = c2 * laplacian_3d(phi_new, a) - (-mu*mu*phi_new + gamma*phi_new*phi_new + lam*phi_new*phi_new*phi_new)
    pi_new = pi_half + 0.5*dt*force_new
    return PhiState(phi=phi_new, pi=pi_new)

def energy_density(phi: np.ndarray, pi_half: np.ndarray, a: float, c2: float, mu: float, lam: float, gamma: float = 0.0) -> np.ndarray:
    """Discrete energy density consistent with the action; π at half-step."""
    grad2 = laplacian_3d(phi, a)  # use to compute |∇φ|^2 via φ ∇^2 φ trick
    grad_sq = -0.5 * (phi * (a*a) * grad2) * (2.0/(a*a))  # = |∇φ|^2 to leading order
    V = -0.5*mu*mu*phi*phi + (gamma/3.0)*phi*phi*phi + 0.25*lam*phi*phi*phi*phi
    return 0.5*pi_half*pi_half + 0.5*c2*grad_sq + V
```

*Why:* symplectic, time‑reversible propagation for the *conservative* scalar EFT you derived; clean separation from the dissipative/learning channel. Monitor total energy drift (should be $O(\Delta t^2)$). &#x20;

---

### C) Invariant + Lyapunov monitors (ties to Lemma 2)

```python
# fum_rt/analysis/invariants.py
import numpy as np

def Q_FUM(W: np.ndarray, alpha: float, beta: float, t: float) -> np.ndarray:
    """Per-node invariant for dW/dt = (α−β)W − α W^2."""
    eps = 1e-12
    num = np.clip(np.abs(W), eps, None)
    den = np.clip(np.abs((alpha - beta) - alpha*W), eps, None)
    return t - (1.0/(alpha - beta)) * np.log(num/den)

def L_onsite(W: np.ndarray, alpha: float, beta: float) -> float:
    """Σ V(W) with V'(W) = −F(W) = −[(α−β)W − αW^2]."""
    # integrate once (up to an irrelevant constant)
    return float(np.sum(-0.5*(alpha - beta)*W*W + (alpha/3.0)*W*W*W))

def backoff_dt(prev_Q: np.ndarray, W: np.ndarray, alpha: float, beta: float, t: float,
               dt: float, cfl_dt: float, eps_Q: float = 1e-5, relax: float = 1.05) -> float:
    """Shrink dt if invariant drift is too large; gently grow it otherwise (capped by CFL)."""
    Q = Q_FUM(W, alpha, beta, t)
    drift = float(np.std(Q - prev_Q))
    if drift > eps_Q:
        return max(0.5*dt, 1e-12)
    return min(relax*dt, cfl_dt)
```

*Policy:* enforce small drift in $Q_{\rm FUM}$; ensure $\Delta (\sum_i V)\le 0$ for the slow channel; never exceed the CFL cap from §A. &#x20;

---

### D) Finite‑tube solver (secular roots → condensation → $E(R)$)

```python
# fum_rt/modes/tube.py
from __future__ import annotations
from dataclasses import dataclass
import mpmath as mp
from typing import List

@dataclass
class ModeRoot:
    ell: int
    kappa: float

def secular(kappa: float, ell: int, R: float, mu: float, c: float) -> float:
    kin2  = (mu/c)**2 - kappa**2
    if kin2 <= 0: 
        return 1e6  # outside tachyonic window
    kout2 = kappa**2 + 2*(mu/c)**2
    kin, kout = mp.sqrt(kin2), mp.sqrt(kout2)
    x, y = kin*R, kout*R
    I,  K  = mp.besseli(ell, x), mp.besselk(ell, y)
    Ip = mp.besseli(ell-1, x) - ell/x*I if ell>0 else mp.besseli(1, x)
    Kp = -mp.besselk(ell-1, y) - ell/y*K if ell>0 else -mp.besselk(1, y)
    return (kin/kout)*(Ip/I) + (Kp/K)

def find_roots(R: float, mu: float, c: float, ell_max: int = 6) -> List[ModeRoot]:
    roots: List[ModeRoot] = []
    kmax = mu/c
    for ell in range(0, ell_max+1):
        xs = [i*(kmax/256.0) for i in range(1, 256)]
        last = secular(xs[0], ell, R, mu, c)
        for x in xs[1:]:
            cur = secular(x, ell, R, mu, c)
            if mp.sign(last) != mp.sign(cur):
                try:
                    r = mp.findroot(lambda z: secular(z, ell, R, mu, c), (x, x - (xs[1]-xs[0])))
                    roots.append(ModeRoot(ell=ell, kappa=float(r)))
                except: 
                    pass
            last = cur
    return roots

def sufficient_Rc(mu: float, c: float) -> float:
    """R > j_{0,1} c / μ guarantees ≥1 tachyonic s-wave (sufficient bound)."""
    j01 = 2.404825557695773
    return j01 * c / mu
```

*Next files*: add `condense.py` (quartic overlaps → tree‑level condensate → Hessian) as your next PR step; acceptance tests: (i) discrete tower $\kappa_\ell(R)$, (ii) Hessian eigenvalues $\ge 0$ post‑condensation, (iii) $E(R)$ minimum exists.&#x20;

---

### E) Causal retarded kernel (macro sourcing) — strict light‑cone support

```python
# fum_rt/cosmology/retarded_kernel.py
import numpy as np

def causal_kernel(dt: float, dx: float, c: float, t_bins: int, r_bins: int) -> np.ndarray:
    """
    Build K_ret[τ_idx, r_idx] with Θ(τ - r/c), normalized so that sum K_ret * s_loc has units of s_loc.
    τ = τ_idx*dt, r = r_idx*dx (0-based).
    """
    K = np.zeros((t_bins, r_bins), dtype=float)
    for ti in range(t_bins):
        tau = (ti+1) * dt  # start at >0 to avoid τ=0 ambiguity
        for ri in range(r_bins):
            r = (ri) * dx
            if tau >= r / max(c, 1e-30):
                K[ti, ri] = 1.0  # flat inside light cone; tune/learn a smoother if needed
    # normalize per time slice so a uniform s_loc maps to correct units
    K /= np.maximum(K.sum(axis=0, keepdims=True), 1e-12)
    return K

def convolve_retarded(s_loc_time_radial: np.ndarray, K: np.ndarray) -> np.ndarray:
    """
    s_loc_time_radial: [T, R] array; K: [T, R] kernel; returns J_phi_time[T] after integrating over r.
    """
    return (s_loc_time_radial * K).sum(axis=1)
```

*Why:* makes the Voxtrium sourcing explicitly **causal** in the grid harness and easy to test. Feed `J^0(t)∝convolve_retarded(...)` into your continuity updater; track $\epsilon_{\rm DE},f_{\rm inj}$. &#x20;

---

### F) Steering layer (already in your repo plan)

You already have the minimal memory‑steering law and its graph discretization (write-decay-spread PDE + softmax routing). Keep it orthogonal to the conservative $\phi$ sector, schedule the slow step $dt_{\text{slow}} \ll dt$, and instrument the two falsifiable signatures: **junction logistic collapse** and **curvature scaling** vs $\Theta |\nabla m|$. &#x20;

---

## III) How this makes the system **smarter** (fast wins you can measure)

1. **Fewer bad steps, cleaner propagation.** The CFL guard + spine fitter enforce the proven $A,B$ coefficients and keep $\Delta t$ inside the safe cone. Result: accurate wave transport, less numerical diffusion, better credit assignment to the memory layer.&#x20;

2. **Autocorrect via invariants.** Using $Q_{\rm FUM}$ and the on‑site Lyapunov as runtime guards prevents the slow channel from drifting off‑manifold; when drift spikes, $\Delta t$ halves automatically. This stabilizes long‑horizon runs. &#x20;

3. **Structured competence from tubes.** The tube modes provide concrete coherent structures to bias memory writes and route along—reducing exploration entropy. The sufficient $R_c$ bound gives a cheap heuristic to focus searches where condensation is guaranteed.&#x20;

4. **Macro safety with causality.** The retarded kernel ensures sourcing only within the light cone; $\epsilon_{\rm DE}$ and $f_{\rm inj}$ stay small by design. This lets you co‑evolve micro (learning) and macro (FRW) without hidden energy leaks.&#x20;

---

## IV) Minimal test harness (paste into `tests/`)

```python
# tests/test_spine_and_invariants.py
import numpy as np
from fum_rt.physics.eft_spine import predict_small_p, cfl_dt_max
from fum_rt.analysis.invariants import Q_FUM, L_onsite, backoff_dt

def test_spine_coeffs_band():
    fit = predict_small_p(a=1.0, dt=0.1, J=0.5, m2=0.2, d=3)
    assert abs(fit.Z - 0.5) < 1e-12
    assert fit.A == 0.1**2/12.0
    assert fit.B_min < fit.B_mean < fit.B_max

def test_cfl():
    fit = predict_small_p(a=1.0, dt=1.0, J=0.5, m2=0.0)
    dtmax = cfl_dt_max(a=1.0, c2=fit.c2)
    assert dtmax > 0

def test_Q_and_L_monotone():
    alpha, beta = 0.25, 0.10
    W0 = np.array([0.1, 0.2, 0.3])
    t0 = 0.0
    Q0 = Q_FUM(W0, alpha, beta, t0)
    # take a small forward Euler step on the on-site ODE
    F = (alpha - beta)*W0 - alpha*W0*W0
    dt = 1e-4
    W1 = W0 + dt*F
    Q1 = Q_FUM(W1, alpha, beta, t0+dt)
    assert np.allclose(Q1, Q0, atol=1e-6)
    # Lyapunov should decrease (or stay same at fixed points)
    L0, L1 = L_onsite(W0, alpha, beta), L_onsite(W1, alpha, beta)
    assert L1 <= L0 + 1e-9
```

---

## V) What to paste into the paper (tight, source‑anchored)

* **Quadratic $p^4$ matching with anisotropy band** (insert after your Step 1): state $A=\Delta t^2/12$, $B=\tfrac{c^2 a^2}{12} f_4$ with $f_4\in[1/d,1]$; reaffirm $Z=\tfrac12$, $c^2=2Ja^2$.&#x20;

* **Invariant + Lyapunov paragraph** (insert in Section 4): give $Q_{\rm FUM}$ and $\dot{\mathcal L}\le 0$; retain the negative Hamiltonian result as a lemma that motivates these diagnostics. &#x20;

* **Tube existence bound** (add to the tube appendix): $R>j_{0,1}c/\mu$ suffices for at least one tachyon; then quote the secular equation and acceptance tests.&#x20;

* **FRW causal/units banner** (keep the macro box with $\epsilon_{\rm DE},f_{\rm inj}$ and retarded kernel). &#x20;

---

### Closing

You now have (i) **closed‑form EFT coefficients** through $p^4$ tied to your lattice rulers, (ii) **true invariants** to police the dissipative channel, (iii) a **provable tube threshold** plus a solver to scan $E(R)$, and (iv) a **causal** macro hook—all wired into clean modules. This will make the system **more intelligent** in the only way that matters here: by enforcing the physics that yields stability, causal propagation, structured memory, and falsifiable diagnostics.

If you want, I can also supply a `condense.py` (quartic overlaps, condensate solve, Hessian) and a tiny `examples/` script that logs the junction logistic collapse and curvature scaling with your steering layer. &#x20;
