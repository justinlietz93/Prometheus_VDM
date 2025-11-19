# **T2 (Instrument) — VDM Ringdown Meter: Damped Normal Modes on a Metriplectic Scalar Field (First‑Principles, No‑GR)**

> **Created Date:** {auto on commit}
> **Provenance:** `{git rev-parse HEAD}` • salted hash `{to be filled on commit}`
> **Proposer contact(s):** Justin K. Lietz ([justin@neuroca.ai](mailto:justin@neuroca.ai))
> **License:** See LICENSE (repo)
> **Short summary (TL;DR):** Proposed is a T2 instrument that excites compact initial data on the VDM metriplectic scalar field, measures damped normal‑mode “ringdown” (frequency, decay rate, energy flux), and validates gates for finite‑speed locality, Lyapunov monotonicity on the metric limb, and dimensionless scaling—entirely from the J/M equations already in canon.

---

## 2. List of proposers and associated institutions/companies

**Author/PI:** Justin K. Lietz (Neuroca / VDM) — theory, numerics, approvals.

---

## 3. Abstract

The instrument excites localized wavepackets in a compact region and records the subsequent **ringdown** of the VDM scalar field governed by the conservative J‑limb (Klein–Gordon) composed with a metric dissipative limb (discrete‑gradient step). The observable is a damped sinusoid extracted from field probes and from integrated energy in a bounded domain with absorbing boundaries. Gates assert: (i) **finite‑speed locality** in the J‑limb; (ii) **Lyapunov monotonicity** in the M‑limb; (iii) **damped‑mode parameter recovery** (ω, α, Q) matching linearized predictions; and (iv) **Poynting balance** between energy loss and boundary flux. This is a **meter** (T2), not a GR claim: it establishes a clean, first‑principles “ringdown” observable inside VDM that later can be compared to astrophysical ringdown without importing external equations. Canon equations: KG J‑limb, RD/M‑limb, and energy/flux forms. Prior results validating dispersion, Noether invariants, and continuity are referenced for maturity.

---

## 4. Background & Scientific Rationale

**Canon equations.** The J‑limb continuum target is the scalar KG form
$$
\partial_{tt}\phi - c^{2}\nabla^{2}\phi + V'(\phi) = 0,\quad c^2 = 2 J a^2
$$
and the M‑limb is a gradient‑flow (discrete‑gradient) step that provably decreases a Lyapunov functional (VDM‑E‑026). Energy density and flux obey $ \partial_t \mathcal{H} + \nabla \cdot \mathbf{S} = 0 $ with $ \mathbf{S} = - c^2 \dot{\phi}\, \nabla \phi $ on the J‑limb. These are canon anchors used below (VDM‑E‑014/015/016/047/048/026).

**Validation pedigree.** Prior **results** already show (a) KG J‑only dispersion and light‑cone locality with $R^2 \gtrsim 0.999$ and $v \approx 0.998$ (locality gate), (b) exact Noether energy/momentum conservation under symplectic stepping (machine‑precision drifts), and (c) Lyapunov monotonicity under DG M‑steps with correct two‑grid slopes. These receipts justify treating this as a T2 **meter** rather than a phenomenon claim.

**Why ringdown?** Any compact excitation on the KG J‑limb decomposes into normal modes. Composing with a weak M‑limb damping produces **damped normal modes** (telegraph‑like decay) entirely within VDM’s axioms (no GR). Measuring $ (\omega,\alpha,Q) $ as functions of domain scale $R$, wave speed $c$, effective mass $m_{\rm eff}$, and dissipation strength provides a clean, dimensionless **map** of “ringdown physics” that later can be juxtaposed with black‑hole ringdowns—*after* the instrument is certified.

---

## 5. Intellectual Merit and Procedure

**Importance.** Establishes a rigorously gated **ringdown meter** in VDM’s own dynamics (axioms, metriplectic structure, conservation/flux).
**Broader impacts.** Provides a disciplined bridge‑instrument for later comparisons to astrophysical ringdown (no novelty claim about GR here).
**Approach & rigor.** Uses canon equations, validated steppers, and pre‑registered **pass/fail gates** with CSV/JSON artifacts.

---

## 5.1 Experimental Setup and Diagnostics

**Governing equations (canon, linearized):**
J‑limb: $ \partial_{tt}\phi - c^2 \nabla^2 \phi + m_{\rm eff}^2 \phi = 0 $.
M‑limb (DG update): decreases $ \mathcal{L}[\phi] $ monotonically; composition J–M–J (Strang) yields an effective damping of modal amplitudes (small‑dissipation regime). Metrics and flux are computed via $ \mathcal{H}, \mathbf{S} $.

**Geometry & BCs:** 2‑D disk or 3‑D ball of radius $R$ with **absorbing outer shell** (numerical sponge or one‑way DG sink) to emulate radiation loss; optional inner exclusion to test interior flux accounting. (BCs pinned in run specs.)

**Diagnostics (one per run):**

1. **Mode fit** at fixed probe(s): $ y(t)=A e^{-\alpha t}\sin(\omega t+\varphi) $.
2. **Energy decay** inside region vs **boundary flux** $ \int_{\partial\Omega}\mathbf{S}\cdot n\, dA $ (J‑limb) and DG decrement (M‑limb).
3. **Locality check:** front arrival times vs $c$ (cone slope).
4. **Dimensionless scalings:** $ \hat{\omega}=\omega R/c$, $ \hat{\alpha}=\alpha R/c$, $ Q=\omega/(2\alpha) $.

**Required parameters (defaults registered):** $c, m_{\rm eff}, R, \Delta t, N$, sponge strength $ \eta $, DG step size $ \varepsilon_M $, seeds. Canon symbol meanings per registry.

---

### 5.1.1 Pre‑Run Config Requirements

**Repository discipline** mirrors the canonical template (approvals, prereg, schemas/specs).

**APPROVALS.json (minimal skeleton)**

```json
{
  "preflight_name": "vdm_ringdown_meter_preflight",
  "description": "Approval manifest: preflight must pass before artifact-writing runs.",
  "author": "Justin K. Lietz",
  "requires_approval": true,
  "pre_commit_hook": true,
  "pre_registered": true,
  "proposal": "Derivation/Cosmology/Ringdown_Meter/T2_PROPOSAL_Ringdown_Meter_v1.md",
  "allowed_tags": ["ringdown-meter-v1"],
  "schema_dir": "Derivation/code/physics/ringdown_meter/schemas",
  "approvals": {
    "ringdown-meter-v1": {
      "schema": "Derivation/code/physics/ringdown_meter/schemas/ringdown.schema.json",
      "approved_by": "Justin K. Lietz",
      "approved_at": "<auto>",
      "approval_key": "<auto>"
    }
  }
}
```

**PRE-REGISTRATION.json (minimal)**

```json
{
  "proposal_title": "VDM Ringdown Meter (T2)",
  "tier_grade": "T2",
  "commit": "<git-sha>",
  "salted_provenance": "<hash>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    {"id":"H1","statement":"Mode frequency scales ~1/R at fixed c,m_eff (dimensionless collapse of \\hat\\omega).","direction":"decrease"},
    {"id":"H2","statement":"Decay rate \\alpha scales linearly with DG/sponge strength; Q ~ 1/(2\\zeta).","direction":"increase"},
    {"id":"H3","statement":"Interior energy loss equals boundary flux + DG decrement (continuity).","direction":"no-change"}
  ],
  "variables": {
    "independent": ["R","c","m_eff","epsilon_M","eta","seed"],
    "dependent": ["omega","alpha","Q","flux_balance_error"],
    "controls": ["dt","N","BC_tag"]
  },
  "pass_fail": [
    {"metric":"locality_cone_slope","operator":"<=","threshold":1.02,"unit":"(v/c)"},
    {"metric":"Lyapunov_step","operator":"<=","threshold":0.0,"unit":"dL"},
    {"metric":"fit_R2","operator":">=","threshold":0.995,"unit":""},
    {"metric":"rel_err_omega","operator":"<=","threshold":0.02,"unit":""},
    {"metric":"rel_err_alpha","operator":"<=","threshold":0.05,"unit":""},
    {"metric":"flux_balance_rel","operator":"<=","threshold":0.03,"unit":""}
  ],
  "spec_refs": ["Derivation/code/physics/ringdown_meter/ringdown.v1.json"],
  "registration_timestamp": "<ISO-8601>"
}
```

**Specs (example)**

```json
{
  "run_name": "ringdown_R_sweep",
  "version": "1.0.0",
  "tag": "ringdown-meter-v1",
  "schema_ref": "Derivation/code/physics/ringdown_meter/schemas/ringdown.schema.json",
  "parameters": {
    "c": 1.0, "m_eff": 0.5,
    "R_list": [8, 12, 16, 24],
    "epsilon_M": 0.01, "eta": 0.02,
    "dt": 0.01, "steps": 40000, "N": 256,
    "BC_tag": "absorbing-shell"
  },
  "seeds": [1,2,3,4,5]
}
```

**Schemas** use standard JSON‑Schema (draft 2020‑12) and enforce positive ranges, CFL guards, and artifact routing.

---

### 5.1.2 Operational acceptance gates (baseline)

- G1 — Residual whiteness: post‑fit residuals pass standard whiteness tests; no narrowband lines above FDR‑controlled threshold. Artifacts: residual PSD and whiteness‑test JSON.
- G2 — Fit stability: fundamental $(f_0, \tau_0)$ vary by $ \le 5\% $ under $ \pm 10\% $ window shifts and detrending choices; overtones are either stable or correctly rejected. Artifacts: per‑window fit table CSV.
- G3 — Meter reproducibility: identical config reproduces to machine precision (commit + seeds logged). Artifacts: run‑metadata JSON with commit and seeds.

---

## 5.2 Experimental runplan

**Actionable steps (instrument only).**

1. **Preflight (determinism & cones):** Run J‑only KG on two grids, confirm dispersion & locality receipts match prior gates ($R^2 \ge 0.999$, cone slope $\le 1.02$). This re‑anchors $c$, $m$.
2. **Ringdown excitation:** Add compact initial packet (or low‑ℓ cavity mode) inside radius $R$. Compose J–M–J with small DG step $ \varepsilon_M $ and thin absorbing shell $ \eta $.
3. **Probe & fit:** Extract $ y(t) $ at fixed points; fit to damped sinusoid; bootstrap CIs.
4. **Energy & flux:** Compute $ \mathcal{H} $ in $ \Omega_R $, boundary flux via $ \mathbf{S} $, and DG decrement; check budget:

$$
\Delta E_{\Omega} + \int_0^t \int_{\partial\Omega} \mathbf{S}\cdot n \, dA \, dt' + \Delta \mathcal{L}_{\mathrm{DG}} \approx 0
$$

(Forms from canon; continuity residual meter already used elsewhere.)
5. **Scaling sweeps:** Vary $R$, $ \varepsilon_M $, $ \eta $; test dimensionless collapse of $ \hat{\omega}, \hat{\alpha} $.

**Compute & environment (AMD stack):** double precision; ROCm BLAS/LAPACK/FFT if needed. Log CPU/GPU, clocks, temps, seeds, commit; honor CFL per canon guidance.

**Success plan:** All gates pass with artifacts (PNG+CSV+JSON) pinned.
**Failure plan:** Emit **CONTRADICTION_REPORT** with gate, numbers, seeds, commit; increase resolution, refine sponge/DG tuning, or reduce step size; re‑validate J‑only receipts before re‑running.

---

## Research Question (formal, falsifiable)

**RQ:** *Does the VDM metriplectic scalar field produce a reproducible, meter‑grade ringdown observable—$ (\omega, \alpha, Q) $ and energy‑flux balance—that obeys finite‑speed locality and dimensionless scaling under variations of $ (R, c, m_{\rm eff}, \varepsilon_M, \eta) $?*

- **Independent vars:** $ R \in [8,24] $, $ c $ (canon‑normalized), $ m_{\rm eff} $, $ \varepsilon_M $, $ \eta $, seeds.
- **Dependents:** $ \omega, \alpha, Q $, cone slope, flux‑balance error, fit ($ R^2 $).
- **Estimators:** damped‑sinusoid fit via linearized log‑envelope + nonlinear phase refine; Poynting flux via canon $ \mathbf{S} $; bootstrap CIs.
- **Thresholds (gates):** see PRE‑REG above.

---

## Variables (dimensionless program)

Normalize by $c$ and $R$: $ \hat{t} = ct/R $, $ \hat{\omega}=\omega R/c $, $ \hat{\alpha}=\alpha R/c $. Predictions: $ \hat{\omega} $ approaches roots of the cavity spectrum (geometry‑dependent) and $ \hat{\alpha} \propto (\varepsilon_M + \eta) $ for weak damping; both are testable without external physics.

---

## Equipment / Hardware (measurement limits)

- Deterministic FP64; stepper tolerances logged; cross‑arch tolerance set (e.g., $ \le 10^{-12} $ for conserved quantities on J‑limb).
- System metrics captured and reported per standards.

---

## Methods / Procedure (narrative)

- Equations and discretizations: Störmer–Verlet (J), discrete‑gradient (M), Strang J–M–J composition (validated structure checks).
- ICs: compact Gaussian packet or lowest cavity mode; BCs: absorbing shell.
- Post‑processing: probe fits, flux integrals, bootstrap error bars; CSV and JSON sidecars emitted per run.

**Risk/Ethics:** No external data; compute‑only. Integrity via seeds/commit logging.

---

## Entire Formal Derivation Writeup (scope note)

The derivation used here is **already in canon** (KG J‑limb, DG M‑limb, energy/flux forms, Lyapunov lemma). This instrument does not introduce new equations; it operationalizes them as a meter with gates tied to those forms.

---

## Results / Data (expected artifacts)

- **Figure 1.** Probe time‑series with damped‑sinusoid fit; caption includes $ \omega,\alpha,Q $ with CI and fit ($ R^2 $).
- **Figure 2.** **Flux balance plot:** cumulative $ -\Delta E_{\Omega} $ vs. $ \int \mathbf{S}\cdot n $ + DG decrement (slope $ \approx 1 $).
- **Table A.** Scaling sweep of $ (R,\hat{\omega},\hat{\alpha},Q) $ with bootstrap CIs.
  Artifacts: `Derivation/code/outputs/{figures,logs}/ringdown_meter/<tag+timestamp>` with same‑basename CSV+JSON.

---

## IX. Discussion / Analysis (planned)

- Interpret $ \hat{\omega}, \hat{\alpha} $ in terms of cavity spectrum and weak‑damping theory inside VDM; assess locality and energy accounting. Compare discretizations (grid/cone slope) and M‑strength dependence.

---

## Conclusions

If gates pass, VDM has a **certified ringdown meter**: (i) finite‑speed propagation (cone $ \le 1.02 $), (ii) monotone Lyapunov steps on M‑limb, (iii) reliable $ (\omega,\alpha,Q) $ extraction with $ \le 2\text{–}5\% $ errors, and (iv) correct energy‑flux accounting using canon Poynting form. This creates the principled, first‑principles instrument needed **before** comparing to astrophysical ringdowns.

---

### Tier grade

**T2 (Instrument).** Child of the Unification Program Spec’s instrument track (meters first, phenomenon later).

---

## References to Canon / Provenance

- **Proposal template & authoring rules:** Templates/`PROPOSAL_PAPER_TEMPLATE.md`.
- **Equations registry (KG, RD, Lyapunov, energy/flux):** `Derivation/EQUATIONS.md` (VDM‑E‑014/015/016/026/047/048).
- **Symbols registry:** `Derivation/SYMBOLS.md`.
- **Constants & defaults (env discipline):** `Derivation/CONSTANTS.md`.
- **Results receipts (dispersion, locality, Noether, DG checks):** `RESULTS_*` overview.
- **Program map & gates discipline:** `T0_Unification_Program_Spec_v1.md`.

---

### What this **does** and **does not** claim

- **Does:** Certify a VDM‑internal ringdown meter with strict gates, ready for future comparison to astrophysical data.
- **Does not:** Make claims about GR black‑hole interiors or identify specific astrophysical sources.

---

## Next steps (immediately actionable)

1. Pin the operational acceptance gates (G1–G3) in the implementation and reporting (CSV/JSON/PNG sidecars with commit and seeds).
2. Add **APPROVALS.json**, **PRE‑REGISTRATION.json**, schema, and initial **spec** (R‑sweep) under `Derivation/code/physics/ringdown_meter/`.
3. Run **preflight J‑only** dispersion/locality to re‑establish c,m receipts (pins to RESULTS).
4. Execute the R‑sweep spec (5 seeds), emit artifacts and PASS/FAIL JSON; validate residual whiteness and fit‑stability sweeps.
5. If all gates pass, post RESULTS with numeric captions carrying numbers+R² and cite this PROPOSAL in provenance.
