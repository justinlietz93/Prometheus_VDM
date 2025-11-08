# HYPOTHESES

> **Author:** Justin K. Lietz
> **Created Date:** 2025‑10‑30  
> **Commit:** 80ee5476e4f887fed3c34534a99daa878f55382f  
> **Salted hash:** *to be generated from the commit at post*  
> **Contact(s):** ([justin@neuroca.ai](mailto:justin@neuroca.ai))  
> **License:** See LICENSE in repository  
> **TL;DR:** This document summarizes and indexes current state of hypothesis files in the repository. It can be seen as the sole source of truth for VDM hypotheses. Review the [Tier Grade Maturity Ladder](/Derivation/TIER_STANDARDS.md) for more information on what constitutes a hypothesis in this codebase.

## **Status legend:**  

- Note on prefixes: Hypotheses and their files are identified by an H prefix following it's unique 3 digit ID.  

### Status descriptors

 **ACTIVE | PAUSED | REJECTED | PROVEN**  
>*PROVEN requires: all hypothesis‑specific gates PASS **and** global gates PASS, each with figure+JSON artifacts.

---

## Global gates (apply to all hypothesis‑backed experiments, T1+)

- **G‑J/M degeneracies:** ⟨J δΣ, δΣ⟩ ≈ 0 and ⟨M δ𝓘, δ𝓘⟩ ≈ 0 within tolerance; per‑run residuals logged.
- **G‑Echo:** J‑only forward–reverse echo fidelity increases with integrator order; dispersion fits inside the declared J‑window.
- **G‑H‑theorem:** ΔΣ ≥ 0 stepwise for M‑only evolutions; equality at steady state.
- **G‑Locality:** finite‑speed cone audit; zero acausal reads/writes.
- **G‑Artifacts:** Every run emits a **MINIMUM** of 1x `metrics.json`, 1x `trace.csv`, 3x figures (PNG), and a PASS/FAIL table. Any violation opens `CONTRADICTION_REPORT.json`.

---

## H001 — Quantum‑Driven Gradient Descent (QGD)

**Classification:** Axiom‑core  
**Owner:** VDM Core  
**Status:** ACTIVE  
**One‑line objective:** A fast, coherent J‑limb accelerates/regularizes a slow M‑descent by reorienting local geometry without violating metriplectic degeneracies.

### Formal statement

For $ \partial_t q = J(q)\,\delta\mathcal I/\delta q + M(q)\,\delta\Sigma/\delta q $, with $J^\top=-J$, $M^\top=M\!\ge 0$, $J\,\delta\Sigma=0$, $M\,\delta\mathcal I=0$: in a window with timescale ratio $\varepsilon=\tau_J/\tau_M\ll1$, the median time to $\epsilon$-optimality $T_\epsilon$ satisfies the speedup

$$
S \equiv \frac{T_\epsilon^{(M)}}{T_\epsilon^{(J+M)}}>1,
$$

with $S$ increasing as $\varepsilon\downarrow$ and curvature anisotropy $\chi=\lambda_{\max}/\lambda_{\min}\uparrow$.

### Predictions (decisive metrics)

- **P1 (Isotropization):** On anisotropic bowls and Rosenbrock, median $S(\varepsilon,\chi)>1.5$ at fixed compute budget; monotone in $1/\varepsilon$ and $\chi$.
- **P2 (Resonant saddle crossing):** In double‑well tests, crossing probability $p_\text{cross}(\omega_J)$ has a unimodal peak within 30% of $\sqrt{|\lambda_\text{saddle}|}$ with ≥3σ prominence.
- **P3 (Degeneracies):** Per‑step degeneracy residuals below threshold throughout runs.

### Rationale (bounded)

Acceleration emerges in continuous‑time **Bregman‑Lagrangian** flows that couple reversible geometry with descent and admit time‑dilation families; this supports a clean “fast J + slow M” separation and conditioning gains without violating dissipative laws. :contentReference[oaicite:0]{index=0}

### Preconditions & scope

Small‑amplitude J‑window with echo/dispersion fit; stationary noise; finite‑speed transport.

### Experiment plan

- **E1 (Isotropization sweep):** Quadratic bowls with $\chi\in\{3,10,30\}$; sweep $\varepsilon$.
  **Gates:** S‑curve monotone in $1/\varepsilon,\chi$; G‑Echo pass.
- **E2 (Saddle resonance):** ND double‑well; sweep $\omega_J$.
  **Gate:** Peak location within 30% of $\sqrt{|\lambda_\text{saddle}|}$; ≥3σ prominence.
- **E3 (Degeneracies audit):** Log ⟨J δΣ, δΣ⟩ and ⟨M δ𝓘, δ𝓘⟩; thresholds pre‑registered.

### Risks & kill‑methods

Hidden J–M coupling injects entropy → kill on G‑H‑theorem fail. Acausal IO → kill on G‑Locality fail.

### Links

- **CF*_** (derivation): *pending*  
- **T0\_pipelines:** `T0_qgd_isotropization/`, `T0_qgd_saddle/`  
- **Results:** `results/qgd/*.json`

### Version history

- v0.1 — 2025‑11‑06 — created

---

## H002 — Memory‑Steering as a Basis‑Agnostic Born‑Meter

**Classification:** Axiom‑core (meter)  
**Owner:** VDM Core  
**Status:** ACTIVE  
**One‑line objective:** Existing memory‑steering + void‑announcer stack yields outcome frequencies matching $|Ua|^2$ after arbitrary J‑basis rotations.

### H002 — Formal statement

With per‑mode energy proxies $E_k$ estimated **locally** and memory variables $m_k \approx \alpha\log(E_k+\epsilon)$ (fixed $\alpha$), the softmax meter $P(k)\propto e^{\Theta m_k}$ produces empirical frequencies $f_k$ with

$$
\text{KL}\!\left(f,\,|U a|^2\right) \le 10^{-3}
$$

across seeds when $U$ (final measurement basis) is a hidden random J‑rotation.

### H002 — Predictions (decisive metrics)

- **P1 (Born‑meter):** KL ≤ $10^{-3}$ after random $U$; convergence vs. shots shown.
- **P2 (NST witness):** No‑signaling‑in‑time witness $W>0$ with error bars using a **nonselective** M‑blip.
- **P3 (Locality):** Zero global peeking; cone audit clean.

### H002 — Rationale (bounded)

For variational state families, the **real part of the Quantum Geometric Tensor** equals the Fubini–Study metric; in the classical embedding, it reduces to ¼·Fisher Information—supporting log‑probability/energy coordinates as natural meter variables that are basis‑invariant under reparametrization. :contentReference[oaicite:1]{index=1}

### H002 — Preconditions & scope

Echo‑verified J‑window; fixed $\alpha,\Theta$ learned once and frozen; walkers restricted to local features.

### H002 — Experiment plan

- **E1 (KL gate):** Fit $\alpha$ on held‑out; freeze. Hidden random $U$; 10³–10⁵ shots.
  **Gate:** KL ≤ $10^{-3}$ with convergence plot.
- **E2 (NST):** Insert nonselective M‑blip at $t_1$; compute $W$.
  **Gate:** $W>0$ beyond bootstrap bars.

### H002 — Risks & kill‑methods

Meter cheat via global state → enforce API; unit tests mock global access. Basis overfit → draw $U$ post‑evolution.

### H002 — Links

- **CF*_**: *pending*  
- **T0\_pipeline:** `T0_born_meter/`  
- **Results:** `results/born_meter/*.json`

### H002 — Version history

- v0.1 — 2025‑11‑06 — created

---

## H003 — Coherence Meter via Koopman/DMD Spectrum

**Classification:** Runtime‑only (instrumentation)  
**Owner:** VDM Core  
**Status:** ACTIVE  
**One‑line objective:** Use Koopman/DMD spectrum of observables as a coherence meter, not as a physical J/M decomposition.

### H003 — Formal statement

Given time‑series of observables during runs, the fitted linear generator $L$ (via DMD/EDMD under a fixed inner product) exhibits (i) **narrowband imaginary‑axis peaks** (oscillatory/coherent content) and (ii) **negative‑real modes** (dissipative content). Define the **coherence index**

$$
\mathcal{C}=\frac{\sum_{\operatorname{Im}\lambda\neq 0} |\hat x(\lambda)|^2}{\sum_{\operatorname{Re}\lambda<0} |\hat x(\lambda)|^2}.
$$

Predict that QGD speedup $S$ increases with $\mathcal{C}$ in matched conditions.

### H003 — Predictions (decisive metrics)

- **P1:** Positive correlation between $\mathcal{C}$ and $S$ at fixed $\varepsilon,\chi$ (Spearman ρ > 0.6).
- **P2:** Imaginary‑axis peaks persist under window shifts; negative‑real spectrum tracks M‑step scaling.

### H003 — Rationale (bounded)

This is an **instrument**, not a law: we use linear spectral structure in observables to *monitor* coherence vs dissipation, then relate it empirically to speedups from H001.  
**Reference note:** the file previously labeled “Applied Koopmanism” in the workspace (arXiv:1202.2660) is **not** a Koopman reference; it is a neutron‑scattering paper (we include it here solely to avoid citation confusion in the canon). :contentReference[oaicite:2]{index=2}

### H003 — Preconditions & scope

Stationary windows; consistent sampling; fixed inner product for DMD.

### H003 — Experiment plan

- **E1 (Panel meter):** Add DMD panel to all QGD runs; compute $\mathcal{C}$.
  **Gate:** Imaginary peaks narrow and stable; negative‑real mass scales with M.
- **E2 (Correlation):** Joint runs with H001 E1; report ρ and CI.

### H003 — Risks & kill‑methods

Overfitting spectral windows → use pre‑registered windows and cross‑validation. Coordinate‑dependence → report the chosen inner product and show robustness over two alternatives.

### H003 — Links

- **CF*_**: *not applicable*  
- **T0\_pipeline:** `T0_coherence_meter/`  
- **Results:** `results/coherence/*.json`

### H003 — Version history

- v0.1 — 2025‑11‑06 — created

---

## H004 — QNG Geometry as an M‑Limb Instantiation (Optional Path)

**Classification:** Derived‑limit (geometry choice for M)  
**Owner:** VDM Core  
**Status:** ACTIVE  
**One‑line objective:** When the readout reduces the state to a parametric family with KL divergence, instantiating $M$ as **natural gradient** on the manifold with metric Re(QGT) improves convergence vs. Euclidean GD.

### H004 — Formal statement

For variational families where the loss is $\frac12\langle \psi_\theta, H \psi_\theta\rangle$ or KL‑aligned, updates with $g(\theta)=\operatorname{Re}[\text{QGT}(\theta)]$ (quantum natural gradient) yield fewer iterations to reach a fixed tolerance than Euclidean GD, holding quantum evaluations and wall‑time within 10% overhead.

### H004 — Predictions (decisive metrics)

- **P1:** Iteration count reduction ≥ 30% vs. Euclidean GD on matched ansätze/tasks.  
- **P2:** With classical embedding, measured metric approaches ¼·FIM (within reported bounds).

### H004 — Rationale (bounded)

Quantum natural gradient uses the **Fubini–Study metric** (Re(QGT)) to define steepest descent on the state manifold; in the classical embedding, QGT → ¼·FIM. This provides a concrete, well‑studied **M‑metric** that is invariant to reparametrization. :contentReference[oaicite:3]{index=3}

### H004 — Preconditions & scope

Applies only when the VDM readout maps cleanly onto a parametric family; overhead tracked.

### H004 — Experiment plan

- **E1 (QNG vs GD):** Reproduce small‑scale QNG comparison with matched oracle calls; track iterations, wall‑time, quantum evals / proxies.  
  **Gate:** ≥ 30% iteration reduction; overhead ≤ 10%.

### H004 — Risks & kill‑methods

Metric estimation noise → block‑diagonal/diagonal approximations; report sensitivity. Model mis‑spec → revert to VDM‑native $M=\nabla^2\Sigma$.

### H004 — Links

- **CF*_**: *pending*  
- **T0\_pipeline:** `T0_qng_mlimb/`  
- **Results:** `results/qng/*.json`

### H004 — Version history

- v0.1 — 2025‑11‑06 — created

---

## Notes on sources in this file

- **Quantum Natural Gradient / QGT basics** — Re(QGT)=Fubini–Study; classical embedding → ¼·FIM; see main text and Appendix A equations for Re/Im split and Berry connection. :contentReference[oaicite:4]{index=4}  
- **Acceleration via Bregman‑Lagrangian flows** — families of accelerated dynamics; time‑dilation property; discrete/continuous correspondence. :contentReference[oaicite:5]{index=5}  
- **Citation sanity** — The file in the workspace labeled arXiv:1202.2660 is **not** a Koopman/DMD reference; it is a neutron‑scattering paper (we include this note to prevent propagation of a mis‑citation in downstream docs). :contentReference[oaicite:6]{index=6}
