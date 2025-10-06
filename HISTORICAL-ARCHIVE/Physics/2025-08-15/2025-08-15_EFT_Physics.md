Got it—continuing with **Step 1: lock the EFT spine**. Below is a tight proof + explicit bounds you can drop into Section 11.

---

## Step 1 — $Z(\phi)=$ const and bounds on $c_1, c_2$

### Claim A (Kinetic normalization).

At tree level, the continuum kinetic coefficient is a **constant**

$$
Z(\phi)=\tfrac12,
$$

with spatial wave‑speed $c^2=2Ja^2$ (or $c^2=\kappa a^2$ if you couple per edge), coming **directly** from the discrete variational principle.&#x20;

**Proof (one line).** Start from the discrete action (central in time, nearest‑neighbor in space)

$$
L^n=a^d\!\sum_i\!\Big[\tfrac12\!\Big(\tfrac{W_i^{n+1}-W_i^n}{\Delta t}\Big)^2-\tfrac{\kappa}{2}\sum_{\mu}(W_{i+\mu}^n-W_i^n)^2 - V(W_i^n)\Big].
$$

Take the continuum limit $W_i^n\!\to\!\phi(\mathbf x,t)$, $\Delta t\!\to\!0$, $a\!\to\!0$. One obtains

$$
\mathcal L=\tfrac12(\partial_t\phi)^2-\tfrac{\kappa a^2}{2}(\nabla\phi)^2-V(\phi)\equiv\tfrac12(\partial\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2-V(\phi),
$$

so $Z(\phi)$ is field‑independent and equals $1/2$. No microscopic relation ties $J$ to $a$; setting $c=1$ is a **units choice**, not a constraint.&#x20;
(Consistent with your continuum EOM and baseline potential choices. )

---

### Claim B (Tree‑level absence of derivative self‑interaction).

At tree level the discrete UV has **no** derivative self‑interactions, so the EFT coefficient of $((\partial_\mu\phi)^2)^2$ vanishes:

$$
c_1^{\text{(tree)}}=0.
$$

**Reason.** The UV action contains only quadratic kinetic terms and a local potential $V(\phi)$; coarse‑graining cannot generate derivative quartics at tree level. Any $((\partial\phi)^2)^2$ appears only radiatively (see bound below). This matches your EFT checklist (write most‑general EFT; then **derive** coefficients from the known UV).&#x20;

---

### Claim C (Sharp $p^4$ bounds from the lattice dispersion).

All dimension‑6 **quadratic** derivative operators in the EFT are fixed—and bounded—by the small‑momentum expansion of the **exact** lattice propagator. For a standard second‑order scheme,

$$
\frac{4}{\Delta t^2}\sin^2\!\Big(\frac{\omega \Delta t}{2}\Big)
= c^2 \frac{4}{a^2}\sum_{i=1}^d\sin^2\!\Big(\frac{k_i a}{2}\Big)+ m^2 .
$$

Expanding at small $\omega,\,k$ gives

$$
\underbrace{\omega^2 - \frac{\Delta t^2}{12}\,\omega^4 + \cdots}_{\text{time}}
=\ c^2 \underbrace{\Big[k^2 - \frac{a^2}{12}\sum_i k_i^4 + \cdots\Big]}_{\text{space}}
+ m^2 .
$$

Match this to the quadratic EFT (choose a basis with separate time/space operators)

$$
\mathcal L_{\!2}=\tfrac12(\partial_t\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2-\tfrac12 m^2\phi^2
\;+\;\tfrac12 A\,(\partial_t^2\phi)^2\;-\;\tfrac12 B\,(\nabla^2\phi)^2\;+\cdots,
$$

whose EOM in Fourier space reads

$$
-\omega^2 + A\,\omega^4 + c^2 k^2 + B\,k^4 - m^2 = 0 .
$$

Matching term‑by‑term yields the **exact** small‑$p$ identifications

$$
A = -\,\frac{\Delta t^2}{12},\qquad
B = -\,\frac{c^2 a^2}{12}\;\frac{\sum_i k_i^4}{k^4}.
$$

Hence the **bounds** (for $d$ spatial dims; here $d=3$):

$$
\boxed{\;|A|=\frac{\Delta t^2}{12}\;},\qquad
\boxed{\;\frac{c^2 a^2}{12d}\ \le\ |B|\ \le\ \frac{c^2 a^2}{12}\;} .
$$

The anisotropy factor satisfies $\frac{1}{d}\le\frac{\sum_i k_i^4}{k^4}\le 1$ (Cauchy; worst/best orientation), so the EFT **must** take $|B|$ within that interval.
Interpretation in your preferred basis $c_2(\Box\phi)^2$: by field redefinitions one trades the separate $A,B$ for a single covariant $c_2\sim\mathcal O\!\big(\Delta t^2, a^2\big)$ up to order‑one geometry factors; either way the size is locked by the lattice rulers. &#x20;

---

### Corollaries and safety checks

* **No ghosts within validity.** The negative signs $A<0, B<0$ encode the **lattice** higher‑branch; they generate an extra root at $\omega\sim \sqrt{12}/\Delta t$ and/or $k\sim\pi/a$. That mode is above the EFT cutoff $\Lambda\sim \min(\pi/\Delta t,\,\pi/a)$ and is not propagated in the IR theory; within $p\ll\Lambda$ the physical branch has $\omega^2>0$. (Same conclusion follows from the exact discrete propagator.)&#x20;
* **Mode positivity after condensation** (context for later steps): post‑condensation masses are non‑negative in the bounded quartic baseline, with $m_{\rm eff}^2=2\mu^2$; see your finite‑tube appendix for how the tachyonic tower resolves when condensation is included.&#x20;

---

### Claim D (Loop‑level/NDA bound on $c_1$ and wavefunction renorm).

At loop level (from $V(\phi)$ interactions), derivative quartics and field‑independent wavefunction renormalization appear with standard EFT suppression:

$$
|c_1| \;\lesssim\; \frac{\mathcal O(1)}{16\pi^2}\,\frac{1}{\Lambda^2},\qquad
Z\;=\;\tfrac12\,(1+\delta Z),\ \ |\delta Z|\lesssim \frac{\mathcal O(1)}{16\pi^2}\log\frac{\Lambda}{\mu},
$$

with $\Lambda\sim \min(\pi/a,\ \pi/\Delta t)$. Any **field dependence** $Z(\phi)$ beyond a constant is higher order in the derivative expansion (e.g., $(\partial\phi)^2\phi^n/\Lambda^n$) and thus suppressed in the IR. This is exactly what your EFT roadmap calls for (derive $Z$, show higher‑derivative terms are irrelevant).&#x20;

---

## What to paste into the paper (succinct “EFT spine lock”)

> **Proposition 11.1 (Kinetic spine).** From the discrete action with central‑time and nearest‑neighbor spatial differences, the continuum kinetic coefficient is $Z(\phi)=\tfrac12$ and the wave‑speed is $c^2=2Ja^2$ (or $c^2=\kappa a^2$). This follows by direct variation and continuum limiting; no $\phi$‑dependence appears at this order.&#x20;
>
> **Proposition 11.2 (Irrelevant tower and bounds).** The exact lattice dispersion fixes the coefficients of all quadratic $p^4$ operators. In the basis $\{(\partial_t^2\phi)^2,\,(\nabla^2\phi)^2\}$,
>
> $$
> A=-\frac{\Delta t^2}{12},\qquad 
> -\frac{c^2 a^2}{12}\le B \le -\frac{c^2 a^2}{12d}.
> $$
>
> Equivalently, any covariant $c_2(\Box\phi)^2$ representation has $|c_2|=\mathcal O(a^2,\Delta t^2)$. These are lattice artifacts (the “heavy branch”) and remain safely above the EFT cutoff $\Lambda\sim \min(\pi/a,\pi/\Delta t)$.&#x20;
>
> **Proposition 11.3 (Absence of derivative self‑interaction at tree level).** The UV contains no derivative self‑interactions, so $c_1((\partial\phi)^2)^2$ vanishes at tree level. Loop‑induced $c_1$ respects $|c_1|\lesssim \mathcal O(1)/(16\pi^2\Lambda^2)$.&#x20;

---

## Numerical confirmation protocol (2‑point fit; quick to implement)

* **Compute** the lattice 2‑point in momentum space at small $(\omega,k)$:
  $G^{-1}(\omega,\mathbf k)=\dfrac{4}{\Delta t^2}\sin^2\!\big(\frac{\omega\Delta t}{2}\big)-c^2\dfrac{4}{a^2}\sum_i\sin^2\!\big(\frac{k_i a}{2}\big)-m^2$.
* **Fit** to the EFT form $G^{-1}\approx Z^{-1}\big[\omega^2-c^2k^2-m^2\big]-A\omega^4 - Bk^4$ using data with $k a,\ \omega\Delta t\ll 1$.
  Acceptance: $Z=0.5\pm\varepsilon$ and $A,B$ within the bounds above, across orientations (check $\langle \sum k_i^4/k^4\rangle$ spread).
* **Optional improvement:** choose $\Delta t$ such that $|A| \simeq |B|/c^2$ (reduces isotropy breaking of the $p^4$ residue).

This verifies $Z$ and nails the $p^4$ envelope **without** relying on potential‑dependent details. &#x20;

---

## How this plugs into Steps 2–4 (one‑liners)

* **Step 2 (finite‑tube tachyon→condensate):** use the locked $Z, c$ to populate the radial eigenvalue problem and the post‑condensation Hessian; positivity of masses after condensation follows the appendix workflow.&#x20;
* **Step 3 (units / Voxtrium mapping):** promote $a,\Delta t$ to $(\phi_0,\tau,a)$ and keep $c^2=2Ja^2$; $m^2=(\alpha-\beta)/\tau^2$; all bookkeeping remains GeV‑consistent.&#x20;
* **Step 4 (FRW embedding & conservation):** with the EFT spine fixed, couple via a retarded transfer current $J^\nu$ to preserve covariant conservation and keep $|w_\text{eff}+1|$ and $f_\text{inj}$ small.&#x20;

---

### Context notes (addressing prior findings)

* The “standard” discrete Hamiltonian you tested is not the conserved quantity (intrinsic dissipation at the on‑site level); conservation lives elsewhere (hidden invariant / Lyapunov) and in covariant transfer at the macro level. This is consistent with locking the EFT kinetic spine via the action route rather than a guessed Hamiltonian. &#x20;

---

If you want, I’ll draft the exact “Appendix: lattice‑to‑EFT $p^4$ matching” text with the above dispersion expansion, plus the tiny code stub to perform the $Z,A,B$ fit on your run logs.
