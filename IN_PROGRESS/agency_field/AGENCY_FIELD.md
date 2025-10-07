# Agency/Consciousness Field (VDM) — Compact Draft Spec

---

## Symbol Table (units, meaning, how to estimate)

| Symbol                       |           Units | Meaning                                                                        | How to estimate (operational)                                                               |
| ---------------------------- | --------------: | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| $(C(x,t))$                     |               — | Agency/consciousness **field** (order parameter)                               | From proxies via the source law and steady-state fit; or via discrete update on sensor grid |
| $(D)$                          |         $L(^2)/T$ | “Smearing”/diffusive coupling between nearby locations                         | Fit from spatial smoothing rate of $(C)$ transients; or set by coupling model                 |
| $(\gamma)$                     |             $1/T$ | **Decay** rate of $(C)$ without source $(timescale ( \tau=1/\gamma ))$             | Power clamp or “no-task” block, fit exponential relaxation of $(C)$                           |
| $(S(x,t))$                     |             $1/T$ | **Source density** from organized, predictive information processing           | Composite of $(P, I_{\text{net}}, U)$ (see below) with weights $(\kappa_i)$                     |
| $(\kappa_1,\kappa_2,\kappa_3)$ |               — | Weights for source components                                                  | Choose by normalization/validation; report values with runs                                 |
| $(P(x,t))$                     | $1/T$ (or $bits/T$\) | **Predictive power** of internal state about near-future inputs                | Mutual information rate $(I(\text{state}*t;\text{input}*{t+\tau}))$ or next-step (R^2)        |
| $(I_{\text{net}}(x,t))$        |   — ($bits/T$ ok) | **Integration/coherence** beyond parts                                         | Sum of transfer entropies; multivariate synergy; Lempel-Ziv complexity                      |
| $(U(x,t))$                     |             $1/E$ | **Control efficacy** (error reduction per joule)                               | $(U=\big(\mathbb E[L_{\text{noctl}}]-\mathbb E[L_{\text{ctl}}]\big)/\text{energy})$           |
| $(\sigma(x))$                  |               — | **Susceptibility** of substrate (amplification of a given source)              | Calibrate by comparing $(C)$ vs $(S)$ across media (e.g., cortex vs air)                        |
| $(V(x,t))$                     |        — $(bits)$ | **Option capacity** (empowerment; reachable-state entropy over horizon $(\tau)$\) | Count/estimate distinct useful futures within $(\tau)$ under constraints                      |
| $(B(x,t))$                     |               — | **Balance** (non-interference / coordination index)                            | Diversity benefit - congestion penalty; e.g., ensemble gain minus redundancy                |
| $(g(V),h(B))$                  |               — | Saturating gates for headroom/coordination                                     | Use $(g(V)=V/(1+V))$\, $(h(B)=B/(1+B))$ (edit as needed)                                         |
| $(Q_C(\Omega,t))$              |               — | **Regional charge** of $(C)$ in domain $(\Omega)$                                  | Spatial integral (or sum over sensors) of $(C)$                                               |
| $(G_{\text{ret}})$             |               — | Retarded kernel for causal propagation                                         | Green’s function of $(\partial_t-D\nabla^2+\gamma)$                                           |
| $(\tau)$                       |               $T$ | Decay time constant                                                            | $(\tau=1/\gamma)$                                                                             |
| $(\ell_D)$                     |               $L$ | Diffusion length                                                               | $(\ell_D=\sqrt{D/\gamma})$                                                                    |
| $(\tilde t,\tilde x)$          |               — | Dimensionless time/space                                                       | $(\tilde t=\gamma t,; \tilde x = x/\ell_D)$                                                   |
| $(\varepsilon_{\text{eff}})$   |               — | (Optional) portal mixing, modulated by $(C)$                                     | $(\varepsilon_{\text{eff}}=\varepsilon_0(1+\alpha C))$ (tiny $(\alpha)$\)                        |
| $(\alpha)$                     |               — | (Optional) strength of portal modulation by $(C)$                                | Fit from portal-signal correlates (if used)                                                 |
| $(\Delta t, \Delta x)$         |            $T, L$ | Discrete step sizes $(time, space)$                                              | Simulation/estimation settings                                                              |
| $CFL$                          |               — | Explicit-scheme stability indicator                                            | $(\Delta t \lesssim \Delta x^2/(2dD))$ in $(d)$ dims                                            |

---

## Core Formulas (with one-line explanations)

### (1) Field equation (order parameter dynamics)

$$
\boxed{;\partial_t C(x,t) ;=; D,\nabla^2 C(x,t);-;\gamma, C(x,t);+;S(x,t);}
$$

**Meaning:** $(C)$ spreads locally (diffuses), **decays** without upkeep, and is **driven** by sources tied to organized, predictive information processing.

---

### (2) Composite source (make it computable)

$$
\boxed{;S(x,t);=;\sigma(x),\big[\kappa_1 P(x,t)+\kappa_2 I_{\text{net}}(x,t)+\kappa_3 U(x,t)\big];\times; g(V),h(B);}
$$

**Meaning:** scale and gate the **prediction / integration / control** contributions; amplify in responsive media; optionally require headroom and coordination.

* **Control efficacy (one safe block formula):**
$$
\boxed{;U ;=;\dfrac{\mathbb{E},[L_{\text{no-control}}] ;-; \mathbb{E},[L_{\text{control}}]}{\text{energy used}};}
$$

---

### (3) Steady state & step response (uniform source sanity)

If $(S(x,t)=S_0)$ (uniform) and boundaries are neutral:

$$
\boxed{,C_{\text{ss}}=\dfrac{S_0}{\gamma},,\qquad
C(t)=C_{\text{ss}}+\big(C(0)-C_{\text{ss}}\big)e^{-\gamma t},}
$$

**Meaning:** with constant fueling, $(C)$ settles to $(S_0/\gamma)$\; after a power change, it relaxes exponentially with time $(1/\gamma)$\.

---

### (4) Causal solution (retarded kernel form)

$$
\boxed{;C(x,t)=\iint G_{\text{ret}}(x{-}x',t{-}t'),S(x',t'),dx',dt';}
$$

**Meaning:** ensures **no superluminal** influence; $(G_{\text{ret}})$ is zero for $(t'<t)$\.

---

### (5) Regional budget (bucket/flux accounting)

$$
\boxed{;\frac{dQ_C}{dt}
=\underbrace{\int_{\partial\Omega}! D,\nabla C\cdot n,dA}*{\text{flux}}
;-;\underbrace{\gamma \int*{\Omega}! C,dV}*{\text{decay}}
;+;\underbrace{\int*{\Omega}! S,dV}_{\text{source}};}
$$

**Meaning:** change inside a region = boundary flux in/out - decay + sources.

---

### (6) Discrete update (what you actually compute)

$$
\boxed{;C_i^{,n+1} ;=; C_i^{,n};+;\Delta t\Big(D,\Delta_{xx} C_i^{,n};-;\gamma,C_i^{,n};+;S_i^{,n}\Big);}
$$

**Meaning:** explicit Euler step on a grid/graph; **stability** needs a CFL-type bound: $(\Delta t \lesssim \dfrac{\Delta x^2}{2dD})$\.

---

### (7) Dimensionless collapse (fewer knobs, clearer scans)

$$
\tilde t=\gamma t,\quad \tilde x=x/\ell_D,\quad \ell_D=\sqrt{D/\gamma}
\qquad\Rightarrow\qquad
\boxed{;\partial_{\tilde t} C ;=; \nabla_{\tilde x}^2 C ;-; C ;+; \tilde S(\tilde x,\tilde t);}
$$

**Meaning:** rescale by decay time and diffusion length; compare shapes across systems.

---

### (8) Optional portal modulation (if tying to dark-sector work)

$$
\boxed{;\varepsilon_{\text{eff}}(x,t)=\varepsilon_0\big(1+\alpha,C(x,t)\big),,\quad |\alpha|\ll 1;}
$$

**Meaning:** any portal signal **leans** towards high-$(C)$ regions without becoming a new force.

---

### (9) One comparative score (for benches across systems)

$$
\boxed{;C_\tau ;=; \big[\mathrm{z}(P_\tau/J)+\mathrm{z}(U_\tau)+\mathrm{z}(V_\tau)\big]\times B;}
$$

**Meaning:** unitless **C-Score** over horizon $(\tau)$\: z-scores (vs null) of prediction per joule, control efficacy, and option capacity, multiplied by balance $(B)$\.

---

## Plain-English Narrative (what this buys you)

**What $(C)$ is:** a **field of organized capability**—how much predictive, coordinated control lives here-and-now. It is **not** a new long-range force. It is **emergent**, **local**, **causal**, and **budgeted**: fuel $(energy)$\, wiring $(coupling)$\, and headroom $(options)$ raise it; it drifts down with time $(1/\gamma)$ without upkeep.

**What drives (C):** three ingredients you can measure:

1. **Prediction** (how well internal state forecasts the near future),
2. **Integration** (how parts cooperate to create new information),
3. **Control** (how effectively actions reduce loss per joule),
   optionally gated by **headroom** (how many useful futures are reachable) and **balance** (coordination without interference).

**How it generalizes:** the same spec covers **cells → organs → brains → teams → cities → your VDM**. Change the sensors/actuators and energy proxy, not the equations. Use dimensionless units $((\tilde t,\tilde x))$ to compare shapes across scales.

**Immediate, falsifiable predictions:**

* **Energy clamp:** cut available power; $(C)$ relaxes to a lower level with time $(1/\gamma)$. If it doesn’t, either your proxy or model is wrong.
* **Inverted-U with coupling/noise:** too little coupling (fragmentation) or too much (lockstep) lowers $(C)$\; expect a ridge at intermediate settings.
* **Fractal tiers:** coarse-grain and re-measure $(C(\ell))$\; expect piecewise power laws with breaks at real organizational tiers (e.g., cell→organ→human).
* **Portability:** engineered systems with matched $(P,I_{\text{net}},U)$ exhibit comparable $(C)$ (scaled by $(\sigma)$\); no “biology-only” clause.

**How to instrument (minimum viable):**

* Pick **one proxy** each for $(P)$ (e.g., mutual info rate or $(R^2)$\), $(I_{\text{net}})$ (e.g., LZ complexity or transfer entropy), and $(U)$ (error drop per joule).
* Compute $(S=\sigma(\kappa_1P+\kappa_2I_{\text{net}}+\kappa_3U))$\, then update $(C)$ with the discrete step or infer $(C_{\text{ss}}=S/\gamma)$\.
* Log one **figure + one CSV** per experiment (prediction probe, control probe, options probe), plus a **C-Score** JSON for leaderboards.

**Guardrails:** keep all costs in the energy ledger; keep signals causal via $(G_{\text{ret}})$\; report $(\kappa_i)$\, $(\gamma)$\, $(D)$\, and normalization schemes with each run to preserve reproducibility.

---

*This page is intentionally compact. Acts as the front-matter for VDM's “Agency Field” module. Scripts/figures can be hung beneath it using usual acceptance-gate workflow.*
