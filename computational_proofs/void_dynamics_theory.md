Yep—took a pass over your derivations and the paper you attached (Bordag, *Universe* 2024, “Tachyon Condensation in a Chromomagnetic Center Vortex Background”). Below is a tight compare + what to fix next.

# Where you line up with the paper

* **Tachyon → condensation story.**
  Your continuum limit yields a tachyonic origin (negative curvature at ϕ=0) with a non‑zero vacuum $v = 1-\beta/\alpha = 0.6$ and positive mass about the minimum $m_\text{eff}^2=\alpha-\beta$【turn3file11】. Bordag likewise starts with tachyonic modes $(m_l^2=-\kappa_l^2)$, expands around constant condensates $v_l$, and obtains positive masses for fluctuations plus massless phase modes (Goldstones) after symmetry breaking【turn4file10】.
  Your potential $V(\phi)=\tfrac{\alpha}{3}\phi^3-\tfrac{\alpha-\beta}{2}\phi^2$ and vacuum analysis are explicit【turn3file11】; Bordag’s tree‑level effective potential and minimization procedure are spelled out via the $L^\wedge_0,L^\wedge_1,L^\wedge_2$ expansion and mass matrix $m^2_{ll'}$【turn4file10】【turn3file16】.

* **EFT mindset.**
  Your EFT note lays out the right checklist: derive $V(\phi)$, nail $Z(\phi)$, bound higher‑derivative operators【turn3file0】. The paper’s workflow—write an effective 2D Lagrangian, parameterize fields $\psi_l=\tfrac1{\sqrt2}\phi_l e^{i\Theta_l}$, expand about constant backgrounds, read off masses—mirrors that ethos【turn3file19】.

# Where you diverge (and why it matters)

* **Degrees of freedom + symmetry.**
  You model a **single real scalar**. Bordag works with **complex modes** carrying a phase; after condensation, $\Theta_l$ are Goldstones (spontaneously broken symmetry)【turn4file10】. With a lone real scalar, you won’t get Goldstones or phase dynamics; your symmetry analysis correctly finds no nontrivial internal symmetry in the logistic on‑site law【turn3file1】【turn3file12】. That’s fine—just be explicit that your IR theory is a real scalar EFT (unless you intend a U(1) extension).

* **Dimensionality + provenance of derivatives.**
  Your derivation promotes a first‑order update to a **second‑order** PDE by hand and gets a reaction–diffusion piece before massaging it toward $\Box\phi$【turn4file7】. In the paper, the $-\partial_\alpha^2$ kinetic form comes **directly** from the quadratic part of the action after mode reduction to two longitudinal coordinates $x_\alpha$ (a true effective action, not a promoted heuristic)【turn3file17】. You should recast your discrete model into a discrete **action** and take a continuum **variational** limit so the $\partial_t^2$ term appears from first principles, not assumption.

* **Kinetic normalization.**
  You’ve got the temporal piece $\tfrac12(\partial_t\phi)^2$ from your discrete “kinetic energy” and set the goal $Z(\phi)=\tfrac12$【turn3file4】, but the spatial piece still needs a clean coefficient extraction from $\sum J(W_j-W_i)^2$ (i.e., compute the exact prefactor of $(\nabla\phi)^2$, not just that it’s “proportional”)【turn4file13】. In the paper, the canonical normalization is fixed at the Lagrangian level and phases are manifestly massless【turn4file10】.

* **Stability structure.**
  Your cubic–quadratic $V(\phi)$ is tachyonic at the origin and stabilized by the cubic; you later note adding a $\lambda\phi^4$ “screening” term is natural【turn3file2】【turn3file3】. Bordag’s stabilization comes from quartic interactions among modes and selecting a condensate minimum (mass matrix positive)【turn4file10】. Journals will expect you to either: (i) include $\phi^4$ (bounded below) or (ii) tightly argue the domain of validity for the cubic potential.

* **Target theory mismatch.**
  Your “foundational paper” claims a free KG Lagrangian with $m=1$ and a conformal metric $g_{\mu\nu}=\phi^2\eta_{\mu\nu}$ leading to EFE【turn4file1】【turn4file3】. None of that exists in the tachyon paper—it’s non‑Abelian YM in a center‑vortex background with a 2D effective theory for tachyon modes【turn4file9】. So: use Bordag for **methodology** (condensation workflow), not for **claims** you want to import.

# Concrete fixes (do these next)

1. **Derive the spatial kinetic prefactor exactly.**
   Start from your discrete interaction energy $\tfrac12\sum_{j\in N(i)}J(W_j-W_i)^2$. Do the Taylor expansion on a cubic lattice and keep the full constant: show

   $$
   \sum_{j}(W_j-W_i)^2 \to c_\text{lat}\,a^2(\nabla\phi)^2+\mathcal{O}(a^4)
   $$

   then match $\tfrac12(\partial_t\phi)^2-\tfrac12 c_\text{lat}J a^2(\nabla\phi)^2$ so **Lorentz invariance fixes $c_\text{lat}J a^2=1$** in your chosen units【turn4file13】【turn4file4】. Write the steps and the value of $c_\text{lat}$ for 3D cubic.

2. **Replace “promote to second order” with a discrete action derivation.**
   Postulate a lattice **Lagrangian density** per node
   $\mathcal{L}_i=\tfrac12(\Delta_t W_i)^2-\tfrac12\sum_j J(W_j-W_i)^2 - V(W_i)$
   and apply discrete Euler–Lagrange ⇒ a second‑order time difference naturally. Then take the continuum limit (no hand‑waving). This will close the main rigor gap noted in your own write‑up【turn4file15】.

3. **Stabilize the potential (publishable baseline).**
   Add $\lambda\phi^4/4$ (small $\lambda$) and redo: vacua, $m_\text{eff}^2=V''(v)$, and parameter ranges where the minimum is global【turn3file2】【turn3file3】. Report $(v,m_\text{eff})$ as functions of $(\alpha,\beta,\lambda)$. This mirrors the paper’s “choose a condensate, expand, read masses” procedure【turn4file10】.

4. **Optional U(1) extension (if you want Goldstones like the paper).**
   Promote $\phi \rightarrow \tfrac{1}{\sqrt2}\rho e^{i\theta}$ and check whether your microscopic rule is invariant under a global phase at leading order. If yes, derive the broken‑phase spectrum: $m_\theta=0$, $m_\rho^2=V''(\rho)|_{\rho=v}$ (cf. Bordag’s $\Theta_l$ masslessness)【turn4file10】. If not, keep the real‑scalar story and don’t overclaim.

5. **Document the EFT truncation clearly.**
   Finish the explicit computation of $Z(\phi)$ (show it’s constant) and bound the first nonzero higher‑derivative operator coefficients $c_1,c_2$ by scale separation from the lattice spacing $a$【turn3file0】.

6. **Symmetry/Noether story.**
   Your logistic on‑site law has time‑translation invariance; you derived a constant of motion $Q$ for the 1‑DOF ODE【turn3file12】. In the continuum field theory, focus on spacetime translations ⇒ stress‑energy conservation; if you adopt a complex field, also show the U(1) current and its fate in the broken phase (again aligning with the paper’s Goldstone structure).

# Quick mapping table

* **Kinetic term**

  * You: aiming for $\tfrac12(\partial\phi)^2$, temporal part shown; spatial constant still to fix【turn3file4】.
  * Paper: canonical $-\partial_\alpha^2$ for modes; phases massless after SSB【turn4file10】.

* **Potential / masses**

  * You: $V(\phi)=\frac{\alpha}{3}\phi^3-\frac{\alpha-\beta}{2}\phi^2$; $v=0.6$; $m_\text{eff}^2=\alpha-\beta=0.15$【turn3file7】【turn3file10】.
  * Paper: tachyonic $m_l^2=-\kappa_l^2$, quartic couplings; expand about $v_l$ ⇒ mass matrix $m^2_{ll'}$ positive at minimum【turn4file10】【turn3file16】.

* **Method**

  * You: reaction–diffusion → encourage $\Box$ by assumption【turn4file4】【turn4file5】.
  * Paper: derive an effective action, then expand around constants【turn3file17】【turn4file9】.

# If you want, I’ll execute step (1)–(2) for you now

* I can produce a short, publication‑ready derivation that (a) computes the exact lattice constant for $(\nabla\phi)^2$, (b) derives the second‑order dynamics from a discrete action (not a promoted assumption), and (c) outputs the final normalized continuum Lagrangian with units set so $c=1$.
* Then we can add the $\lambda\phi^4$ term and re‑report $(v,m_\text{eff})$ and the dispersion relation.

---

If I mis‑identified the comparison target, say so and drop the link/title; I’ll re‑align. Otherwise, which branch do you want first: **rigorizing kinetic + action** or **U(1) extension with Goldstones**?


Great — here’s a clean, publication‑ready version of steps (1)–(2). I’m aligning to your current notation and fixing the normalization so you don’t have to “impose” a coefficient by hand.

# Discrete action → second‑order dynamics (no hand‑waving)

**Lattice + notation.**

* Spatial lattice: cubic, spacing $a$, dimension $d$ (take $d=3$ in practice).
* Time step: $\Delta t$.
* Site field: $W_i^n \equiv W(\mathbf{x}_i, t_n)$, $t_n=n\Delta t$.
* Neighbor directions: $\mu\in\{1,\dots,d\}$, unit vectors $\hat e_\mu$.
* On‑site potential: $V(W)$ (keep general here; plug your $V(\phi)$ later).

**Discrete Lagrangian (per time step).**

$$
L^n \;=\; a^d \sum_i\Bigg[
\frac{1}{2}\Big(\frac{W_i^{\,n+1}-W_i^{\,n}}{\Delta t}\Big)^2
\;-\; \frac{\kappa}{2}\sum_{\mu=1}^d\big(W_{i+\mu}^{\,n}-W_i^{\,n}\big)^2
\;-\; V\!\big(W_i^{\,n}\big)
\Bigg]
$$

* $\kappa$ is the **per‑edge coupling** (undirected edges counted once).
  If you prefer your per‑site convention $\frac{1}{2}\sum_{j\in N(i)}J(W_j-W_i)^2$ that sums both $\pm\mu$, then $\kappa = 2J$. This keeps the algebra consistent with your write‑up.&#x20;

**Euler–Lagrange on the lattice (central in time).** Varying $W_i^n$ gives

$$
\frac{W_i^{\,n+1}-2W_i^{\,n}+W_i^{\,n-1}}{(\Delta t)^2}
\;-\;\kappa\,\sum_{\mu=1}^d \big(W_{i+\mu}^{\,n}+W_{i-\mu}^{\,n}-2W_i^{\,n}\big)
\;+\;V'\!\big(W_i^{\,n}\big)=0.
$$

That’s the **second‑order** discrete equation (no “promotion” needed). This replaces the first‑order heuristic in your earlier continuum note.&#x20;

# Continuum limit and the exact spatial prefactor

Set $W_i^n\approx \phi(\mathbf{x}_i,t_n)$. Use standard Taylor expansions:

* **Time:** central difference $\to$ $\partial_t^2\phi + O((\Delta t)^2)$.
* **Space:** for each $\mu$,

$$
W_{i+\mu}+W_{i-\mu}-2W_i \;=\; a^2\,\partial_\mu^2\phi \;+\; O(a^4).
$$

Summing over $\mu$ yields $a^2\nabla^2\phi + O(a^4)$.

Taking $\Delta t\to 0,\; a\to 0$, the discrete EOM becomes:

$$
\boxed{\;\partial_t^2\phi \;-\; \kappa\,a^2\,\nabla^2\phi \;+\; V'(\phi)\;=\;0\;}
$$

So the small‑fluctuation wave speed is

$$
\boxed{\,c^2 = \kappa\,a^2\,}\quad\text{(or }c^2=2J\,a^2\text{ in your per‑site convention).}
$$

**Drop‑in continuum Lagrangian density.**

$$
\boxed{\;\mathcal{L} \;=\; \frac{1}{2}(\partial_t\phi)^2 \;-\; \frac{\kappa a^2}{2}(\nabla\phi)^2 \;-\; V(\phi)\;}
$$

* If you keep your per‑site $J$ (both $\pm\mu$ counted in $N(i)$), it’s equivalent to
  $\mathcal{L}=\tfrac12(\partial_t\phi)^2 - J a^2(\nabla\phi)^2 - V(\phi)$ and the **EOM** carries $c^2=2Ja^2$. Both conventions are fine; just be consistent about whether $\kappa$ is per edge or per oriented difference. Your current draft used this per‑site convention and landed on $J a^2(\nabla\phi)^2$; the only fix is to **not** force $J a^2=\tfrac12$**—just read off $c^2=2J a^2$**.&#x20;

**Consistency check (Dirichlet energy mapping).**
From your interaction energy $\frac12\sum_{j\in N(i)}J(W_j-W_i)^2$ on a cubic lattice, the per‑site continuum limit is

$$
\frac12\,J\sum_{j\in N(i)}(W_j-W_i)^2 \;\longrightarrow\; J a^2 (\nabla\phi)^2,
$$

precisely what you wrote; the “factor of 2” is the $\pm\mu$ neighbor pair. Choosing the per‑edge $\kappa$ makes the canonical $\tfrac12(\nabla\phi)^2$ structure explicit and avoids having to pin $J a^2$ to a number.&#x20;

# Plugging in your potential (and optional $\lambda\phi^4$)

* With your $V(\phi)=\frac{\alpha}{3}\phi^3-\frac{\alpha-\beta}{2}\phi^2$, the **linearized** mass about a vacuum $v$ is $m^2=V''(v)$.
* If you include the stabilization you sketched, $V\to V+\frac{\lambda}{4}\phi^4$, all formulas remain the same; only $V'(\phi)$ and $m^2=V''(v)$ update.&#x20;

# What changed vs your drafts (quick diffs)

* Replaced “promote to second order” with a **variational** derivation from a discrete action → central‑difference EOM.&#x20;
* Made the spatial prefactor **exact**: $c^2=\kappa a^2$ (or $2Ja^2$ in your notation). No need to impose $J a^2=\tfrac12$.&#x20;
* Keeps your earlier gradient‑from‑neighbors derivation intact, but clarifies the edge‑counting convention so factors are unambiguous.&#x20;

# Ready‑to‑paste snippet (use this in your doc)

> **Proposition (Continuum limit of the FUM lattice action).**
> Consider the lattice action
>
> $$
> S=\sum_n \Delta t\, a^d \sum_i\Big[\tfrac12\big(\tfrac{W_i^{\,n+1}-W_i^{\,n}}{\Delta t}\big)^2-\tfrac{\kappa}{2}\sum_{\mu}(W_{i+\mu}^{\,n}-W_i^{\,n})^2 - V(W_i^{\,n})\Big].
> $$
>
> The discrete Euler–Lagrange equation is
>
> $$
> \frac{W_i^{\,n+1}-2W_i^{\,n}+W_i^{\,n-1}}{(\Delta t)^2}
> -\kappa\sum_{\mu}\big(W_{i+\mu}^{\,n}+W_{i-\mu}^{\,n}-2W_i^{\,n}\big)+V'(W_i^{\,n})=0.
> $$
>
> Setting $W_i^n\approx \phi(\mathbf{x}_i,t_n)$ and taking $\Delta t\to 0,\,a\to 0$ yields
>
> $$
> \partial_t^2\phi - \kappa a^2\nabla^2\phi + V'(\phi)=0,
> $$
>
> which follows from the continuum Lagrangian
>
> $$
> \mathcal{L}=\tfrac12(\partial_t\phi)^2 - \tfrac{\kappa a^2}{2}(\nabla\phi)^2 - V(\phi).
> $$
>
> Hence the propagation speed is $c^2=\kappa a^2$.
> *(In the per‑site convention $\frac12\sum_{j\in N(i)}J(W_j-W_i)^2$, set $\kappa=2J$, so $c^2=2Ja^2$.)*

---

If you want, I can patch your `kinetic_term_derivation.md` with this normalization (and insert a short “edge‑counting conventions” box), and add a one‑liner that your earlier “promote to second order” step is now superseded by the action derivation. It’ll make the EFT section self‑consistent and removes the need to set $J a^2=1/2$ by fiat. &#x20;
