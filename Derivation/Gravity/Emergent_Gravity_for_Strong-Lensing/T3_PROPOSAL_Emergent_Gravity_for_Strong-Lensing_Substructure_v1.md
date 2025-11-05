# **T3→T4 — VDM Emergent Gravity for Strong‑Lensing Substructure (B1938+666‑class)**

> **Created:** 2025‑11‑05
> **Provenance:** will record `git rev-parse HEAD`, salted hashes, and tag per §5.1.1 (pre‑run config) when the repo commit is ready.  
> **Contact:** Justin K. Lietz (PI) • [justin@neuroca.ai](mailto:justin@neuroca.ai)
> **License:** dual license per canon (commercial use requires written permission).  
> **TL;DR:** Formalize and test a *local, metriplectic‑consistent* mapping from the VDM field to an **effective lensing potential**, then fit it to a B1938+666‑class Einstein‑ring anomaly using a preregistered *instrument → phenomenon* pipeline. The pass/fail gates compare VDM against MOND‑like and ΛCDM baselines on image‑plane residuals, ring‑mode distortions, and Bayesian evidence.  

---

## 1. Tier grade

**This document proposes a composite T2→T4 program:**

* **T2 (Instrument):** Build and verify a VDM‑consistent *Lensing Meter* (solver + diagnostics) that maps a 3‑D VDM field $,\phi(x),$ to a thin‑lens potential $,\psi(\theta),$ and image residual metrics; instrument QC is physics‑agnostic except for A0–A7 compliance.  
* **T3 (Smoke):** Show that a compact VDM excitation (tachyonic KG branch) produces the qualitative “ring‑pinch” seen in B1938+666‑class systems.  
* **T4 (Prereg):** Register hypotheses, parameter priors, gates, and analysis scripts; run blinded fits against a held‑out observed ring or a communityvetted mock with comparable SNR/PSF, then unblind.  

---

## 2. Proposers & roles

**Justin K. Lietz** — PI, theory & QC owner; approver for Axiom gates & RESULTS conformance.

---

## 3. Abstract (≤200 words)

VDM posits a single field with metriplectic dynamics (A0–A7) whose discrete action yields an inertial KG branch and an overdamped RD branch. The KG branch supports compact, tube‑like excitations from a tachyonic origin of the potential; the RD branch provides dissipative relaxation (M‑limb). This proposal derives a **local, effective lensing potential** as a *functional of the VDM field* without importing external forces, then tests whether a single compact VDM excitation superposed on a macro lens reproduces the **Einstein‑ring “pinch”** anomaly class. The instrument is preregistered, metrics and thresholds are declared, and comparisons against MOND‑like and ΛCDM subhalo baselines are run identically for fairness. Passing the preregistered gates would **quantitatively** favor VDM’s *J→M causality* over entropic‑gravity/MOND variants in this regime; failing gates will generate a CONTRADICTION_REPORT and demote the claim.  

---

## 4. Background & scientific rationale

**VDM canon & equations.** The lattice action and Euler–Lagrange limit define the KG equation with $c^2=2Ja^2$ (J‑only limb), while the overdamped limit yields RD with diffusion $D$ (M‑limb). These are the *only* allowed building blocks at the axiom level (A0–A7).    The tachyonic mechanism ($V''(0)<0$) produces compact excitations and a characteristic length $R^\ast\sim\pi/\sqrt{\alpha-\beta}$; this is our *VDM substructure* template.  

**Why lensing?** Strong lensing probes *projected curvature* regardless of photons’ non‑interaction with matter—an ideal falsification ground for emergent gravity versus CDM lumps or MOND‑like laws. The project explicitly positions VDM’s prediction against MOND‑like (Verlinde‑style) excess gravity in a preregistered bake‑off.  

**Prior VDM maturity.** RD front speed and dispersion are Tier‑A validated (meters, KPI gates). EFT/KG is active/KPI‑gated; metriplectic identity and H‑theorem style monitors exist in canon algorithms. We build on those meters and gates.  

**Program integration.** The effort aligns with **T0_Unification_Program_Spec** milestones L0–L2 for discrete→continuum proofs and metriplectic operator degeneracies; contact‑/QGT‑bridge notes are tracked as gaps (not imported as axioms).  

---

## 5. Intellectual merit & procedure

**(1) Importance.** Distinguishing *excess gravity from geometry* (VDM) vs *cold subhalos* (ΛCDM) vs *MOND‑like laws* is decisive and *quantitative* in strong lensing.
**(2) Broader impacts.** Provides a falsifiable gravitational program grounded in VDM’s axioms, with open instruments and reproducible artifacts.
**(3) Approach clarity.** Derive a **thin‑lens mapping** from the VDM field to the image plane consistent with A0–A7; preregistered QC enforces meter validity before claims.  
**(4) Rigor.** We use *pre‑run approvals, salted hashes, signed tags, and RESULTS gating standards*; uncertainties and χ² are reported with explicit confidence semantics.  

### 5.1 Experimental setup & diagnostics (T2 instrument)

**State & equations (canon):**
Discrete action → KG branch (J‑only):
[
\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi)=0,\quad c^{2}=2Ja^{2}.
]
Overdamped RD (M‑limb): (
\partial_t \phi = D\nabla^{2}\phi + f(\phi)
). (Used for relaxation/seeding only—no external forces added.)  

**Effective lensing mapping (derived‑limit, *runtime only*):**
We adopt the *thin‑lens, geometric‑optics* approximation as a *test meter*, not a new axiom. Light rays follow null geodesics of an **effective metric** functionally dependent on $\phi$; in the weak‑field/eikonal limit this reduces to a 2‑D potential $\psi$ on the lens plane. Operationally we posit a **local** VDM → lens potential map:
[
\boxed{\ \Phi_{\text{eff}}(\mathbf{x}*\perp,z);=;\Lambda^{-4}\left[\tfrac{1}{2}\dot\phi^2 + \tfrac{c^2}{2}\lvert\nabla\phi\rvert^2 + V(\phi)\right]\ +\ \xi,\nabla^2 V(\phi)\ }\tag{M1}
]
with small, dimensionless $(\Lambda^{-4},\xi)$ under KPIs. The **thin‑lens potential** and **deflection** are
[
\psi(\boldsymbol{\theta})=\frac{2}{c^{2}}\frac{D*{ls}}{D_l D_s}\int \Phi_{\text{eff}}(D_l\boldsymbol{\theta},z),dz,\qquad
\boldsymbol{\alpha}(\boldsymbol{\theta})=\nabla_{\boldsymbol{\theta}}\psi,\quad
\kappa=\tfrac{1}{2}\nabla_{\boldsymbol{\theta}}^{2}\psi.\tag{M2}
]
This uses GR’s standard lensing *as a meter* to compare image morphologies; GR itself is not imported as a foundational axiom of VDM. (For notation and GR conventions used by the meter, see Wald; for field‑theoretic action/Noether structure, see QFT rules.)  

**Compact VDM excitation template (tachyonic KG branch):**
Using the canon potential (V(\phi)=\tfrac{\alpha}{3}\phi^{3}-\tfrac{r}{2}\phi^{2}+\tfrac{\lambda}{4}\phi^{4}) with (V''(0)=-r<0), we generate stationary, localized tubes/balls characterized by a scale (R^\ast\sim \pi/\sqrt{r}) and concentration parameter $\nu$ read off from $T_{00}[\phi]$. These act as the **VDM substructure** near the macro lens.  

**Diagnostics (meters):**

* **Identity & metriplectic residuals:** $g_1,g_2\le 10^{-10}$ grid‑refined (J/M degeneracy checks).  
* **Locality/causality:** cone check on KG limb; no superluminal support growth.  
* **H‑theorem (RD limb):** $\Delta\mathcal{L}\le 0$ during relaxation.  
* **Lensing meter QC:** Poisson solver residual ≤1e‑10 (FFT/finite‑diff cross‑check); image remapping reversible to ≤1e‑3 pixels RMS.

#### 5.1.1 Pre‑run config (approvals, hashes, schemas)

* **Required:** `Derivation/code/physics/gravity_regression/APPROVAL.json`, `schemas/` (run + metrics), `specs/` (prereg JSON), salted SHA‑256 manifest, signed tag `prereg.vdm.gravlens.v1.YYYYMMDDThhmmZ` committed **before** any run; proposal lists all hashes verbatim. Authorization fails otherwise.  

---

## 6. Formal hypotheses, falsifiable metrics, and gates

**H1 (Local functional suffices).** The **local** functional (M1) produces an image‑plane potential whose best‑fit *single* compact VDM excitation + smooth macro model explains the ring pinch without invoking CDM subhalos or MOND‑like laws.

* **Metric:** image‑plane *residual RMS* (arcsec) and *mode‑by‑mode ring distortion* $\Delta m$ from a Fourier decomposition of ring brightness.
* **Gate (T4):**

  * *Instrument pass:* on mocks with known truth, recover parameters with median relative error ≤5% and reduced $\chi^2\in[0.8,1.2]$.
  * *Phenomenon pass:* on B1938+666‑class data, VDM achieves ΔAIC ≤ −10 and log‑evidence ΔlnZ ≥ +5 versus (i) smooth+CDM NFW subhalo and (ii) MOND‑like law with standard priors. **Fail → CONTRADICTION_REPORT.**

**H2 (Concentration scaling).** The recovered VDM excitation has a **projected** profile slope $\beta$ that falls in the family predicted by tachyonic tubes parameterized by $(\alpha,\lambda)$.

* **Metric:** posterior over $(R^\ast,\beta)$ vs. the KG‑tube library; two‑sample test of CDFs (KS distance).
* **Gate:** KS $p>0.1$ and posterior overlap ≥0.5 with the nearest KG‑tube family.

**H3 (J/M integrity).** The fit is **stable** under mesh refinement and J/M splitting diagnostics; identity residuals remain within gates and no hidden body force enters the PDE.

* **Metric:** $g_1,g_2$ degeneracy checks; action drift; RD Lyapunov monotonicity (relaxation only).
* **Gate:** $g_1,g_2\le 10^{-10}$ (refined), $\Delta S\ge0$ in M‑step; locality cone slope matches $c=\sqrt{2Ja^2}$ within 1%.  

**H4 (Model selection versus MOND‑like).** Against MOND‑like/entropic‑gravity meters, VDM’s *geometric* functional yields superior evidence on the same data and baselines, addressing the mutually exclusive causal arrows (J→M vs M→J).  

* **Metric:** ΔlnZ (VDM minus MOND‑like) under identical data, PSF, and priors.
* **Gate:** ΔlnZ ≥ +5 (decisive) or, minimally, ΔlnZ ≥ +3 (strong).

---

## 7. Methods (derivation → discretization → implementation)

### 7.1 Governing equations (canon; used limbs)

* **KG limb (J‑only):** $,\partial_{tt}\phi-c^{2}\nabla^{2}\phi+V'(\phi)=0,; c^2=2Ja^2$. (Used to generate stationary compact excitations.)
* **RD limb (M‑part):** $,\partial_t\phi=D\nabla^2\phi+f(\phi)$ for controlled relaxation; Lyapunov functional strictly decreases.  

### 7.2 Mapping to lens plane (meter, not axiom)

* **Energy‑density proxy:** $T_{00}[\phi]=\tfrac{1}{2}(\dot\phi^2+c^2\lvert\nabla\phi\rvert^2)+V(\phi)$. The functional (M1) is a dimensionally consistent local scalar; $(\Lambda,\xi)$ are KPIs (priors: broad log‑uniform).
* **Thin‑lens:** compute $\psi$ via (M2); deflection, convergence, and shear via image‑plane derivatives; fit lensed ring pixels via forward ray‑tracing (same meter used for all models). (GR lensing conventions for the meter follow Wald.)  

### 7.3 Numerical scheme & stability

* **KG solver:** second‑order leapfrog; CFL based on $c=\sqrt{2Ja^2}$; reversible J‑step checks.
* **Poisson/FFT:** periodic pad + zero‑flux variant; cross‑validate residuals.
* **QC:** identity residuals, H‑theorem, locality cones; *all* meters log seeds, commit, and JSON config.  

### 7.4 Dimensionless analysis (A6)

Scale by $R^\ast$ and $c$:
[
\tilde{x}=x/R^\ast,;\tilde{t}=t,c/R^\ast,;\tilde{\phi}=\phi/\phi_\star,
]
so that the only dimensionless fit parameters in (M1) are $\tilde{\Lambda}^{-4}$ and $\tilde{\xi}$ plus macro‑lens terms; this supports *scaling collapse* across mocks and real systems.  

---

## 8. Data, priors, and preregistration

* **Mocks (T2/T3):** macro‑SIE lens + ring source; inject one compact VDM excitation at random offset/PA; render with instrument PSF/noise.
* **Observed ring (T4):** one B1938+666‑class dataset with public PSF/noise model and mask; meta recorded in prereg JSON.
* **Priors:** compact VDM location (uniform in annulus), $R^\ast$ log‑uniform, concentration $\nu$ broad; $\tilde{\Lambda}^{-4},\tilde{\xi}$ log‑uniform on [1e‑6,1].
* **Blinding:** freeze masks/PSF and hyperparameters before any fit; unblind only after instrument passes T2 gates.
* **Reporting:** χ², AIC, BIC, ΔlnZ; parameter posteriors with bootstrap/ESS; uncertainties rounded and reported per lab‑rules.  

---

## 9. Quality gates (physics & software)

**Axiom‑level gates** — symmetry/locality/H‑theorem/Noether diagnostics as above; cone speed within 1%; no body forces.  
**Derived‑limit checks** — KG locality cone, RD Lyapunov monotonicity; meter reversibility tests.  
**Software gates** — Clean Architecture; ≤500 LOC/file; repository pattern; tests mirror source; no outer→inner deps; constructor injection for ports/adapters. (Directory skeleton below.)
**RESULTS discipline** — white‑paper grade narrative, figure captions with numbers and CSV/JSON, pass/fail JSON, contradiction protocol.  

---

## 10. Implementation plan (Hybrid‑Clean Architecture)

```plaintext
src/
  domain/gravity_regression/
    models.py             # POCOs: FieldConfig, LensParams, VDMPotentialParams
    interfaces.py         # Ports: FieldSolver, LensingMeter, InferenceEngine
  application/gravity_regression/
    use_cases/
      fit_single_excitation.py   # Orchestrates run; DI for ports
      validate_instrument.py     # T2 gates
    ports/
      repositories.py      # ArtifactRepo, DataRepo
  infrastructure/numpy_gpu/gravity_regression/adapters/
    kg_solver.py           # Leapfrog KG; J-step checks
    lensing_meter.py       # (M1)-(M2) + FFT Poisson
    inference.py           # NUTS/VI; evidence calc
  presentation/cli/
    gravlens_cli.py        # `vdm gravlens --spec <json>`
tests/
  domain/... ; application/... ; infrastructure/... ; presentation/...
```

* **CLI:** `vdm gravlens run --spec specs/b1938_prereg.v1.json --out outputs/b1938_vdm_v1/`
* **Artifacts:** CSV/JSON (parameters, posteriors), PNG (figures), parquet (samples), SHA‑256 manifest.
* **Approvals:** `APPROVAL.json`, schemas for metrics (`residuals.schema.json`, `evidence.schema.json`).  

---

## 11. Assumptions, risks, and kill‑methods

* **Assumption:** The *local* functional (M1) is sufficient at the ring’s scale; non‑local corrections (retardation/disformal terms) are negligible. **Kill:** if (M1) cannot pass T2 recovery on mocks or fails ΔlnZ gates on real rings under any reasonable prior.
* **Risk:** Metric degeneracy (VDM excitation mimics NFW). **Mitigation:** ring‑mode analysis and multi‑band PSF tests; require ΔlnZ evidence threshold.
* **Risk:** KG limb numerics bias. **Mitigation:** reversibility tests, step‑halving, two‑grid order ≥ 2.9.  
* **Risk:** Overfitting. **Mitigation:** preregistered priors/metrics; blind/unblind protocol; report χ̄² and SDOM per lab rules.  

---

## 12. Success criteria & expected outcomes

* **Instrument (T2) PASS:** mock recovery ≤5% median error; lensing meter residuals ≤1e‑10; gates satisfied.
* **Smoke (T3):** qualitative pinch reproduced by *one* compact VDM excitation + macro lens at plausible offset.
* **Prereg (T4) PASS:** decisive evidence (ΔlnZ ≥ +5) for VDM‑functional over MOND‑like and over CDM‑subhalo at fixed macro model; otherwise **FAIL** with CONTRADICTION_REPORT and de‑escalation to gap‑study.  

---

## 13. Provenance & citation policy

* **Axioms (A0–A7) & metriplectic split:** source of truth.  
* **Equations (KG/RD, potentials, action):** canonical VDM E‑list.  
* **Canon overview & tiers:** validation tiers, KPI gates.  
* **Proposal & RESULTS standards; prereg hashing and approvals:** authoring template and policy.  
* **Classical GR conventions for the meter:** Wald.  
* **QFT variational structure (action→currents):** standard rules.  
* **Constants & defaults registry:** single source of numerical defaults, ranges.  
* **Comparative program note (VDM vs MOND/Verlinde):** decisive test framing.  

---

### Appendix A — Formal notes (compact)

**Axioms used.** Closure, Void primacy, Locality, Symmetry/Noether, Dual generators (J/M with degeneracy), Entropy law, Scale program, Measurability. All observables are functionals of $\Psi!\leftrightarrow!\phi$; *no external forces are added*.  

**Canonical equations referenced.** Discrete action (VDM‑E‑011); continuum KG (VDM‑E‑014); RD gradient flow & Lyapunov (VDM‑E‑015/E‑016); EFT mass and tachyonic mechanism per canon notes.  

**Lens meter status.** GR lensing is used **only** as an observational *meter* to compare morphology across models; it is not imported as a foundational axiom of VDM.  

---

## What this proposal does **not** claim

* It does not claim a finished cosmological solver or a universal replacement of ΛCDM; it targets a **specific** lensing anomaly class.
* It does not claim novelty for KG/RD math; novelty is the **VDM→lensing local functional** plus the metriplectic‑compliant instrument and falsifiable bake‑off.  

---

### Next steps (immediately actionable)

1. Land the `gravity_regression` module skeleton and tests per §10.
2. Commit `APPROVAL.json`, schemas, and the prereg `specs/*v1.json`; create salted hashes and signed tag per §5.1.1.  
3. Generate T2 mocks; run recovery and meter QC; publish RESULTS with pass/fail JSON.
4. Lock priors; run T3 smoke; refine only by documented knobs.
5. Freeze prereg; unblind T4 run on the chosen ring; report ΔlnZ and gates.
