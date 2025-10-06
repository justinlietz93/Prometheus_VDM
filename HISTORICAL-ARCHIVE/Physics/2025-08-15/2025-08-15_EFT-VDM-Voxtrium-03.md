Great—continuing with concrete deliverables and proofs. I assembled your **single derivation document** that ties the discrete FUM → bounded scalar EFT → finite‑tube tachyon analysis → causal FRW (Voxtrium) in one place, with a physics‑first → code mapping and a “strong vs weak” assessment.

**Download:**
[**FUM\_Voxtrium\_Derivation\_Justin\_Lietz.md**](sandbox:/mnt/data/FUM_Voxtrium_Derivation_Justin_Lietz.md)

It credits **Voxtrium** wherever his macro‑sourcing framework is used and credits **you (Justin Lietz)** for the derivations, diagnostics, and implementation plan.

---

## Executive summary of what’s now *proven* and how to implement it in code

### 1) Discrete → Continuum (action-based, second order in time)

* Starting from the per‑node rule $\dot W_i=(\alpha-\beta)W_i-\alpha W_i^2$ with nearest‑neighbor coupling, a variational coarse‑graining yields the **canonical kinetic term** and wave speed:

  $$
  \mathcal L_K=\tfrac12(\partial_t\phi)^2-\tfrac{c^2}{2}(\nabla\phi)^2,\quad c^2=2Ja^2.
  $$

  This fixes the *second‑order* time evolution; no ad‑hoc “RD surrogate” is needed.&#x20;

* The EFT potential that is both **bounded** and **faithful** to the discrete asymmetry is:

  $$
  V(\phi)=-\tfrac12\mu^2\phi^2+\tfrac{\lambda}{4}\phi^4+\tfrac{\gamma}{3}\phi^3,\quad \mu^2>0,\ \lambda>0,\ |\gamma|\ll\mu^2\sqrt\lambda.
  $$

  Vacua at $v=\mu/\sqrt{\lambda}$, and small fluctuations have $m_{\rm eff}^2\simeq 2\mu^2$. Mapping back to discrete coefficients clarifies $\mu^2\leftrightarrow(\alpha-\beta)$, $\gamma\leftrightarrow\alpha$.&#x20;

* EFT consistency (why higher‑derivative terms are suppressed and $Z(\phi)$ is effectively constant) is laid out in your EFT guide/checklist and aligned to the UV (the FUM lattice).&#x20;

**Code change (void‑faithful):** switch the simulator to a leapfrog/Verlet PDE integrator of

$$
\partial_t^2\phi-c^2\nabla^2\phi+\gamma\phi^2+\lambda\phi^3-\mu^2\phi=J_\phi,
$$

with explicit $c^2=2Ja^2$, and enforce $\lambda>0$ at parse time. (Plan section 8 in the doc.)

---

### 2) Finite‑tube tachyon tower → condensation → positivity (Bordag‑style, scalar analogue)

* For a finite cylinder where the interior is near the uncondensed state and the exterior is condensed, the radial eigenproblem gives a **secular equation** (matching $I_\ell$ and $K_\ell$ at radius $R$) whose roots $\kappa_\ell(R)$ count the **tachyonic modes** ($\omega^2<0$ for $k=0$). This reproduces the *tachyonic tower* structure qualitatively.&#x20;

* Expanding in these modes, minimizing the quartic tree potential yields **condensates** $v_{\ell n}(R)$; the post‑condensation mass matrix (Hessian) has **non‑negative eigenvalues**, i.e., the tachyons acquire real masses (Goldstones only if you promote to complex). Energy $E(R)=E_{\rm bg}+V_{\rm eff}^{\rm tube}$ develops a **true minimum** in a window, mirroring Bordag’s flux‑tube minimum (Fig. 5 there).&#x20;

**Code change:** add a **cylindrical test harness** that (i) solves the Bessel‑matching equation to count tachyon roots, (ii) builds mode overlaps for the quartic, (iii) minimizes tree‑level energy and checks Hessian eigenvalues ≥0. (Plan §8, item 4.)

---

### 3) Macro‑sourcing (Voxtrium) → causal FRW bookkeeping with units

* Sectoral continuity with a **transfer current** $J^\nu$ enforces covariant conservation:

  $$
  \sum_i\big(\dot\rho_i+3H(1+w_i)\rho_i\big)=0,\ \ J^0=(\varepsilon_h/V_c)\dot S_{\rm hor}.
  $$

  Λ, DM, and GW source terms are proportional to $(\alpha_h/V_c)\dot S_{\rm hor}$ and $(\varepsilon_h/V_c)\dot S_{\rm hor}$ with a **partition closure** $p_\Lambda+p_{\rm DM}+p_{\rm GW}=1$. Units are internally consistent (${\rm GeV}^5$ for sources).&#x20;

* **Locality** is restored by a **retarded kernel** for horizon entropy production, removing any acausal global update. Micro→macro coefficients tie to Skyrme scales $R_\*,m$ and establish falsifiable relations (e.g., velocity‑dependent self‑interaction curve).&#x20;

**Code change:** implement the FRW “banner” and **retarded source stencil** (toggleable), plus automated monitors for $w_{\rm eff}$ drift and injection fraction $f_{\rm inj}$. (Plan §8, items 3, 9.)

---

### 4) Memory steering & invariances (empirical tests that the kinetics are right)

* Your junction data collapse to a **logistic** with slope $k\approx1$ after rescaling by $\theta\Delta m$, consistent with the field’s normalized “temperature”.
* Curvature scales roughly linearly with $\Theta\cdot\|\nabla m\|$ and shows **signed invariance** when flipping gradient/phase, matching the expected second‑order variational dynamics.

**Code change:** keep these as **physics diagnostics** (not ML): automatically fit $k,\,b$ and curvature slope each run; fail CI if they stray beyond tolerance (Plan §8, item 7).

---

## What’s strong vs weak (cleanly stated)

**Strong:**

* Canonical kinetic normalization and second‑order PDE from the lattice action; derivative expansion rationale.
* Bounded EFT with tachyon stabilization and well‑defined vacua/masses; discrete→continuum mapping of $(\alpha,\beta)$.&#x20;
* Finite‑tube tachyon counting and post‑condensation positivity; energy minimum (Bordag‑parallel).
* FRW transfer‑current formalism with units‑safe, causal sourcing and partition closure.&#x20;

**Weak/open:**

* A **true discrete invariant** is not yet identified; your analysis shows the standard $\mathcal H$ is **not** conserved—either the system is dissipative or it conserves a non‑trivial quantity (next: symmetry/Lyapunov search).&#x20;
* Loop corrections/thermal dependences in the EFT are not yet computed; higher‑derivative coefficients need explicit UV matching (beyond the checklist).&#x20;
* Vector/complex extension (vorticity, Goldstones) and quantitative astrophysics calibration remain to be implemented.&#x20;

---

## Immediate code tasks (surgical and production‑ready)

1. **PDE core:** add a `WaveEFT` integrator (leapfrog) with CFL guard, explicit $c=\sqrt{2Ja^2}$.
2. **Potential module:** `V(phi)`, `dV_dphi(phi)` with $\{\mu,\lambda,\gamma\}$ and runtime positivity check on $\lambda$.
3. **Causal source:** implement $K_{\rm ret}$-convolution and sector bookkeeping; provide `--retarded` flag.
4. **Tube harness:** Bessel matching, count $N_{\rm tach}(R)$, minimize tree energy, check Hessian ≥0.
5. **Units:** centralize $\{\phi_0,\tau,a\}$, export GeV/cgs; print `c`, `m_eff`, and $v$ per run.
6. **Diagnostics:** compute $\mathcal E$ and the FRW sum rule each step; keep your logistic/curvature probes as CI tests.
7. **Optionals:** complex $\Phi$ for Goldstones; thermal mass $m^2(T)\sim m^2+c_T\lambda T^2$ if you want to test restoration.

---

### Where each claim ties to your documents

* Continuum limit and kinetic normalization: your **discrete→continuum** and **kinetic** derivations (action‑based, $c^2=2Ja^2$).&#x20;
* EFT rigor checklist and suppression of higher‑derivative terms: **EFT approach** doc.&#x20;
* Finite‑tube scalar analogue and acceptance criteria: **finite\_tube\_mode\_analysis** (your write‑up) + Bordag’s Universe paper for the SU(2) reference anatomy.
* FRW macro sourcing and units: **macro banner / Voxtrium mapping** (causal kernel, partitions, dimensional analysis).&#x20;
* Discrete conservation attempt and outcome (not the right $\mathcal H$): **discrete\_conservation**.&#x20;

---

### Final note on credit

* **Justin K. Lietz** — discrete→continuum derivations; bounded EFT choice/mapping; finite‑tube scalar analysis; memory‑steering experiments; code plan.
* **Voxtrium** — macro **Voxtrium** sourcing idea, FRW transfer‑current bookkeeping, and the micro→macro parameter ties (all credited in the doc).
* **M. Bordag** — tachyon condensation methodology in flux tubes; used as an analogue and explicitly cited.

If you want, I can now turn the “tube harness” equations into production Python (Bessel matching + quartic minimization + Hessian), or wire up the `WaveEFT` core—your choice which to land first.
