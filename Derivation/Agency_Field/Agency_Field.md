# Agency/Consciousness Field (VDM) - Canon-Aligned Compact Spec

---

## Symbol Table (units, meaning, how to estimate)

| Symbol                       |                                   Units | Meaning                                                                        | How to estimate (operational)                                                                                |        |    |
| ---------------------------- | --------------------------------------: | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------ | -- |
| $C(x,t)$                     |                                       - | Agency/consciousness **field** (order parameter)                               | From proxies via the source law and steady-state fit; or via discrete update on a sensor grid.               |        |    |
| $D$                          |                               $L^{2}/T$ | Diffusive coupling (“smearing”) between nearby locations                       | Fit from spatial smoothing rate of $C$ transients; or set by coupling model.                                 |        |    |
| $\gamma$                     |                                   $1/T$ | **Decay** rate of $C$ without source (timescale $\tau=1/\gamma$)               | Power clamp / “no-task” block; fit exponential relaxation of $C$.                                            |        |    |
| $S(x,t)$                     |                                   $1/T$ | **Source density** from organized, predictive information processing           | Composite of $P,I_{\text{net}},U$ with weights $\kappa_i$; optional gates $g(V),h(B)$.                       |        |    |
| $\kappa_1,\kappa_2,\kappa_3$ |                                       - | Weights for source components                                                  | Choose by normalization/validation; report with runs.                                                        |        |    |
| $P(x,t)$                     |                       $1/T$ (bits/s ok) | **Predictive power** of internal state about near-future inputs                | Mutual-information rate $I(\text{state}*t;\text{input}*{t+\tau})$ or next-step $R^2$.                        |        |    |
| $I_{\text{net}}(x,t)$        |                           - (bits/s ok) | **Integration/coherence** beyond parts                                         | Sum of transfer entropies; multivariate synergy; Lempel–Ziv complexity.                                      |        |    |
| $U(x,t)$                     |                                   $1/E$ | **Control efficacy** (error reduction per joule)                               | $U=\big(\mathbb E[L_{\text{noctl}}]-\mathbb E[L_{\text{ctl}}]\big)/\text{energy}$. Define the energy ledger. |        |    |
| $\sigma(x)$                  |                                       - | **Susceptibility** of substrate (amplification of a given source)              | Calibrate by comparing $C$ vs $S$ across media.                                                              |        |    |
| $V(x,t)$                     |                                - (bits) | **Option capacity** (empowerment; reachable-state entropy over horizon $\tau$) | Count or estimate distinct useful futures (log base 2).                                                      |        |    |
| $B(x,t)$                     |                                       - | **Balance** (coordination without interference)                                | Diversity benefit − congestion penalty; ensemble gain − redundancy.                                          |        |    |
| $g(V),,h(B)$                 |                                       - | Saturating gates for headroom/coordination                                     | e.g., $g(V)=\frac{V}{1+V}$, $h(B)=\frac{B}{1+B}$.                                                            |        |    |
| $Q_C(\Omega,t)$              |                                       - | **Regional charge** of $C$ in domain $\Omega$                                  | Spatial integral (or sensor sum) of $C$.                                                                     |        |    |
| $G_{\text{ret}}$             |                                       - | Retarded kernel for causal propagation (parabolic)                             | Green’s function of $\partial_t-D\nabla^2+\gamma$, with $G_{\text{ret}}(t<0)=0$.                             |        |    |
| $\tau$                       |                                     $T$ | Decay time constant                                                            | $\tau=1/\gamma$.                                                                                             |        |    |
| $\ell_D$                     |                                     $L$ | Diffusion length                                                               | $\ell_D=\sqrt{D/\gamma}$.                                                                                    |        |    |
| $\tilde t,\tilde x$          |                                       - | Dimensionless time/space                                                       | $\tilde t=\gamma t,;\tilde x=x/\ell_D$.                                                                      |        |    |
| $\varepsilon_{\text{eff}}$   |                                       - | (Optional) portal mixing, modulated by $C$                                     | $\varepsilon_{\text{eff}}=\varepsilon_0(1+\alpha C)$ with small $\|\alpha\|$  |
| $\alpha$                     |                                       - | Portal-modulation strength                                                     | Fit from portal-signal correlates (if used).                                                                 |        |    |
| $\Delta t,\Delta x$          |                                   $T,L$ | Discrete step sizes (time, space)                                              | Simulation settings.                                                                                         |        |    |
| CFL                          |                                       - | Explicit-scheme stability indicator                                            | $\Delta t \lesssim \Delta x^2/(2dD)$ in $d$ dimensions.                                                      |        |    |
| $c$                          | $L/T$ (unitless under normalized grids) | **Signal speed** (conservative KG transport)                                   | From locality-cone fit: slope of the front trajectory.                                                       |        |    |
| $m$                          |                                   $1/T$ | **Mass parameter** (KG dispersion intercept)                                   | From linear fit of $\omega^2$ vs $k^2$: intercept $= m^2$.                                                   |        |    |

---

## Core Formulas (with one-line explanations)

### (1) Diffusive field equation (order-parameter dynamics)

$$
\boxed{;\partial_t C(x,t)=D,\nabla^2 C(x,t)-\gamma,C(x,t)+S(x,t);}
$$

**Meaning:** $C$ spreads locally (diffusion), **decays** without upkeep, and is **driven** by sources tied to organized, predictive information processing.

---

### (2) Composite source (make it computable)

$$
\boxed{;S(x,t)=\sigma(x),\big[\kappa_1 P(x,t)+\kappa_2 I_{\text{net}}(x,t)+\kappa_3 U(x,t)\big]\times g(V),h(B);}
$$

**Control efficacy (safe block):**
$$
\boxed{;U=\dfrac{\mathbb{E},[L_{\text{no-control}}]-\mathbb{E},[L_{\text{control}}]}{\text{energy used}};}
$$

---

### (3) Steady state & step response (uniform source sanity)

If $S(x,t)=S_0$ (uniform) and boundaries are neutral,
$$
\boxed{,C_{\text{ss}}=\dfrac{S_0}{\gamma},\qquad
C(t)=C_{\text{ss}}+\big(C(0)-C_{\text{ss}}\big)e^{-\gamma t},}
$$
**Meaning:** with constant fueling, $C$ settles to $S_0/\gamma$; after a power change, it relaxes exponentially with time $1/\gamma$.

---

### (4) Causal solution for the parabolic model

$$
\boxed{;C(x,t)=\iint G_{\text{ret}}(x{-}x',t{-}t'),S(x',t'),dx',dt';}
$$

**Meaning:** **retarded** (no $t'<t$ contribution). Parabolic diffusion has infinite support but remains causal in the Green’s-function sense.

---

### (5) Regional budget (bucket/flux accounting)

$$
\boxed{;\frac{dQ_C}{dt}
=\int_{\partial\Omega} D,\nabla C\cdot n,dA
-\gamma \int_{\Omega} C,dV
+\int_{\Omega} S,dV;}
$$

---

### (6) Discrete diffusive update (what is computed)

$$
\boxed{;C_i^{,n+1}=C_i^{,n}
+\Delta t\Big(D,\Delta_{xx}C_i^{,n}-\gamma,C_i^{,n}+S_i^{,n}\Big);}
$$

**Stability:** CFL-type bound $\Delta t \lesssim \Delta x^2/(2dD)$.

---

### (7) Dimensionless collapse

$$
\tilde t=\gamma t,\quad \tilde x=\frac{x}{\ell_D},\quad \ell_D=\sqrt{\frac{D}{\gamma}}
;\Rightarrow;
\boxed{;\partial_{\tilde t} C=\nabla_{\tilde x}^2 C - C + \tilde S(\tilde x,\tilde t);}
$$

---

### (8) Optional portal modulation

$$
\boxed{;\varepsilon_{\text{eff}}(x,t)=\varepsilon_0\big(1+\alpha,C(x,t)\big),\quad |\alpha|\ll 1;}
$$

---

### (9) Comparative score (benches across systems)

$$
\boxed{;C_\tau=\big[\mathrm z(P_\tau/J)+\mathrm z(U_\tau)+\mathrm z(V_\tau)\big]\times B;}
$$

**Meaning:** unitless **C-score** over horizon $\tau$: z-scores (vs null) of prediction per joule, control efficacy, and option capacity, multiplied by balance $B$.

---

## Optional Conservative Transport Module (KG J-only)

This module captures finite-speed signal transport used in the **locality-cone** and **dispersion** validations. It augments diagnostics; it does **not** replace the diffusive $C$-field.

**Hamiltonian (semi-discrete, normalized grid):**
$$
H(\phi,\pi)=\tfrac12|\pi|_2^2+\tfrac12 c^2|\nabla_h\phi|_2^2+\tfrac12 m^2|\phi|_2^2.
$$

**Linear dispersion (gate target):**
$$
\boxed{;\omega^2=c^2 k^2+m^2;}
$$

**Local causality (front bound):**
$$
\boxed{;v_{\text{front}}\le c(1+\varepsilon),\quad \varepsilon\ \text{set by discretization tolerance};}
$$

> **Parabolic vs hyperbolic:** Diffusive $C$ has infinite-speed support (parabolic). The **finite cone** applies only to the KG transport used for conservative diagnostics.

---

## Plain-English Narrative (what this buys)

**What $C$ is:** a **field of organized capability**-how much predictive, coordinated control exists here and now. It is **emergent, local, causal (retarded), and budgeted**: fuel (energy), wiring (coupling), and headroom (options) raise it; without upkeep it decays on $1/\gamma$.

**What drives $C$:** three measurable inputs-**Prediction** $P$, **Integration** $I_{\text{net}}$, **Control** $U$-optionally gated by **headroom** $V$ and **balance** $B$.

**How it generalizes:** the same spec spans **cells → organs → teams → engineered systems**. Sensors/actuators and the energy ledger may change; the equations do not. Use $(\tilde t,\tilde x)$ to compare across scales.

---

## Axiom-Level Quality Gates (including the new validations)

### Diffusive (M step) - H-theorem

* **Gate M-Lyapunov:** discrete Lyapunov decreases per converged step
  $$\boxed{;\Delta L_h \le 0;\ \text{per step};}$$

### Strang composition (JMJ) - order behavior

* **Primary gate (aligned spectral gradients):** two-grid slope $\ge 2.90$, $R^2\ge 0.999$.
* **Explained-by-defect fallback (baseline stencil):** if slope $<2.90$ but the **Strang-defect diagnostic** (commutator-based) regresses to $\approx 3$ with high $R^2$, stamp **EXPLAINED-BY-DEFECT** instead of fail. Document the gradient mismatch and keep the pass contingent on M-Lyapunov holding.

### Conservative KG (J-only) - **validated** gates

* **KG dispersion:** regress $\omega^2$ on $k^2$; require

  * slope $= c^2 \pm 2%$,
  * intercept $= m^2 \pm 2%$,
  * $R^2 \ge 0.999$.
* **Locality cone:** fit front radius $R(t)$ from a narrow pulse; require

  * $v\le c(1+\varepsilon)$ with $\varepsilon=0.02$,
  * $R^2 \ge 0.999$.

> **Status:** Recent runs meet these thresholds; the KG J-only module is **validated** and should be referenced when transport matters.

---

## Evidence & Reproducibility

* **One artifact path pinned in the text** (repository commit + data directory).
* **Per-figure sidecars:** CSV/JSON with the same basename containing seed, commit, and metrics (e.g., slope/intercept/$R^2$, $v$, $\Delta L_h$ series, two-grid slope).
  Example (JSON):

  ```json
  {
    "gate": "KG-dispersion",
    "commit": "abcd1234",
    "seed": 42,
    "slope": 1.0007,
    "intercept": 0.9989,
    "r2": 0.999997,
    "c_CI": [0.999, 1.002],
    "m_CI": [0.998, 1.002]
  }
  ```
* **Contradiction report on failure:** gate name, threshold, seed, commit, artifact pointer, brief post-mortem.

---

## Runtime & Scaling (reporting minima)

* **Scaling claims** use log–log slopes: report $\beta \pm$ CI for step-time vs work/active sites.
* **Latency:** P50/P95/P99 with jitter; drift over long runs.
* **Sparsity:** fraction of cells/agents touched per tick; maintain a budget.
* **Environment ledger:** CPU/GPU (AMD/ROCm), RAM peak, VRAM, utilization, temps, non-experiment process count, wall-clock by stage, storage footprint.

---

## Scope & Boundaries

* No novelty claim is made for classical RD or KG results; they are used as **QC invariants**.
* The KG module is **optional** and diagnostic; $C$’s governing PDE remains diffusive unless explicitly coupled to conservative transport.

---

## Posting Flow (operational)

1. **TL;DR + one artifact path.**
2. **Boxed lemma or boxed gate** near the top.
3. **End with one invitation:** “Propose a tighter threshold; it will be run and posted.”

---

## Appendix A - RD ↔ Discrete Mapping (sanity)

For the logistic RD variant used in some checks:
$$
\partial_t \phi
= D,\nabla^2\phi + r,\phi - u,\phi^2
\quad(\text{optional } -\lambda\phi^3),
$$
with independent $r>0$, $u>0$. A common discrete mapping:
$$
D \approx J,a^2 \quad (\text{continuous-time RW}), \qquad
\text{or}\quad D \approx \frac{J,a^2}{\Delta t}\quad (\text{discrete-time update}),
$$
under small-$k$ and unit-mass conventions.

**Front speed (KPP limit):** $c_{\text{front}}=2\sqrt{D,r}$ (for monostable regimes).

---

## Appendix B - Strang-defect diagnostic (order sanity)

If $A$ (J-step generator) and $B$ (M-step generator) do not commute, the Strang error scales with the commutator:
$$
\mathrm{Err}_{\text{Strang}}=\mathcal O!\left(\Delta t^3,\big([A,[A,B]]+[B,[B,A]]\big)\right).
$$
When gradients differ (stencil vs spectral), the commutator size explains observed slopes $<3$ even when M-Lyapunov holds; this diagnostic supports classification **EXPLAINED-BY-DEFECT**.

---

**This page is intentionally compact and canon-aligned.** It is the front-matter for the VDM “Agency Field” module; notebooks and acceptance-gate scripts live under `Derivation/Notebooks` and emit CSV/JSON artifacts with figure-ready captions.
