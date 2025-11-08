# T1 (Proto-model) - Telegraph From Relaxation Instrument

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See [LICENSE](/LICENSE)

Short summary (one sentence TL;DR):  
Quantify the telegraph characteristic speed emerging from relaxation by testing the spec-level relation $c=\sqrt{D/\tau}$ with deterministic meters, artifact routing, and acceptance gates.

---

## 1. Scope and Alignment

- Canon anchor equation: [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105) (Telegraph characteristic speed from relaxation)  
- Program context: [T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:326)  
- Policy and gates: [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md), [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md), [ARCHITECTURE.md](Derivation/code/ARCHITECTURE.md)

This is a T1 instrument proposal (no claims beyond meters). It provides a reproducible way to test whether finite-speed transport measured from pulses satisfies $c\approx\sqrt{D/\tau}$ across controlled sweeps of $(D,\tau)$.

Assumptions and limitations:

- Linear regime for transport meter (small-amplitude pulses).  
- Homogeneous medium; periodic or no-flux boundaries as specified.  
- The experiment measures speed empirically; it does not claim a derivation beyond [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105).

---

## 2. Background & Rationale

Analogy. Diffusion spreads “infinitely fast” in PDE idealization, while a relaxed (telegraph-like) medium exhibits finite wavefront speed. The spec-level map $c=\sqrt{D/\tau}$ asserts that a relaxation time $\tau$ regularizes transport, permitting a causal cone.

Precise math references:

- Speed definition and target relation: [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105).  
- Metering discipline (cones, fronts, regressions): KG/J-only locality and dispersion meters in [RESULTS_KG_Jonly_Locality_and_Dispersion.md](Derivation/Metriplectic/KG_Jonly_Locality_and_Dispersion/RESULTS_KG_Jonly_Locality_and_Dispersion.md:1) and structure checks in [RESULTS_Metriplectic_Structure_Checks.md](Derivation/Metriplectic/RESULTS_Metriplectic_Structure_Checks.md:1).

---

## 3. Instrument Design

Measured quantities:

- Empirical front speed $\hat c$ from time-of-flight of a narrow pulse between sensor pairs.  
- Diffusivity proxy $D$ (controlled).  
- Relaxation time $\tau$ (controlled).

Experimental configurations:

- 1D uniform grid with spacing $\Delta x$, size $N$; periodic or no-flux BC.  
- Initial condition: small-amplitude Gaussian pulse centered at $x_0$; background zero.  
- Two families of dynamics (select exactly one per run profile):
  1) Canonical telegraph PDE runner (control meter).  
  2) Relaxation-closure runner (moment-based or reduced model) that induces effective telegraph behavior (instrument-under-test).

Detectors:

- Threshold-crossing at fixed fraction of peak to extract arrival times (hysteresis and min-gap to avoid chatter).  
- Cross-correlation peak time between reference and downstream sensors (robust to noise).  
- Optional linear fit of space–time ridge in a space–time intensity plot.

Artifact routing (required):

- Figures → Derivation/code/outputs/figures/transport/telegraph_relaxation/  
- Logs (CSV, JSON) → Derivation/code/outputs/logs/transport/telegraph_relaxation/  
All via [io_paths.py](Derivation/code/common/io_paths.py:1).

---

## 4. Acceptance Gates

Let runs sweep $(D,\tau)$ over a grid and compute $(\hat c, D, \tau)$ tuples.

Primary gate (speed law):

- Fit $\log \hat c$ vs $\tfrac12(\log D - \log \tau)$:
  - Slope $\hat s$ within $[0.95, 1.05]$  
  - $R^2 \ge 0.98$

Secondary gates (stability and repeatability):

- Across seeds, coefficient of variation for $\hat c$ at fixed $(D,\tau)$ ≤ 5%.  
- Front detectability fraction ≥ 95% across (D, τ) grid (non-detections logged).  
- Numerical tolerances: ensure time-step and grid convergences do not shift $\hat c$ beyond ±2% (two-resolution check).

Logging requirements (JSON/CSV):

- Record commit, salted proposal hash, code_hashes, seeds, (D, τ) lists, all fits (slope, intercept, R², CI), and pass/fail.

---

## 5. Methods

5.1 Domain and BC  

- Domain length $L=N\Delta x$, typical $N\in\{512,1024\}$; $\Delta x$ chosen to resolve pulse width by ≥ 10 points.  
- BC: periodic or Neumann; record in JSON.

5.2 Initial pulse  

- Gaussian: $A\exp\!\big(-\frac{(x-x_0)^2}{2\sigma^2}\big)$ with $A\ll 1$ to remain in linear regime.

5.3 Steppers and stability  

- Explicit/implicit as applicable to the runner; CFL and stiffness constraints documented (runner emits dt, stability flags).  
- Two-resolution check: $(\Delta x, \Delta t)$ and $(\Delta x/2, \Delta t/2)$ for a subset of points.

5.4 Speed measurement  

- Sensor pairs at known separations.  
- Two estimators per run: threshold-crossing time-of-flight and cross-correlation lag.  
- Aggregate by median across seeds; CI via bootstrap.

---

## 6. Variables and Ranges

- Independent: $D \in [D_{\min}, D_{\max}]$, $\tau \in [\tau_{\min}, \tau_{\max}]$; seeds.  
- Dependent: $\hat c$ (per estimator), slope $\hat s$, intercept $\hat b$, $R^2$, CoV.  
- Controls: $(N, \Delta x, \Delta t)$, BC, pulse parameters $(A,\sigma)$, estimator thresholds.

Default sweep (example):

- $D \in \{0.05, 0.1, 0.2, 0.4\}$, $\tau \in \{0.25, 0.5, 1.0, 2.0\}$, seeds = 10.  
- $N=1024$, periodic; $\sigma=6\Delta x$, $A=10^{-3}$.

---

## 7. Risks and Mitigations

- Pulse dispersion at small $\tau$: prefer cross-correlation estimator; report both.  
- Aliasing/noise: windowed filters for correlation; enforce min-gap between detections.  
- Parameter corners (very small/large $D/\tau$): flag low-SNR points; exclude per prereg window if justified.

---

## 8. Provenance & Approvals

Approvals required before any artifact-emitting run: see [authorization/README.md](Derivation/code/common/authorization/README.md:1).  
Artifacts quarantined on gate failure; contradiction reports emitted.

---

## 9. Pre-registration JSON (template)

```json
{
  "proposal_title": "T1 - Telegraph From Relaxation Instrument",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "c scales as sqrt(D/τ) with slope 1.0±0.05 on log axes; R² ≥ 0.98.", "direction": "increase" },
    { "id": "H2", "statement": "Two-resolution convergence keeps |Δc|/c ≤ 0.02.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["D","tau","seed"],
    "dependent": ["c_hat","slope","intercept","R2","CoV"],
    "controls": ["N","dx","dt","BC","A","sigma","estimator"]
  },
  "pass_fail": [
    { "metric": "slope_in_range", "operator": "==", "threshold": true, "unit": "-" },
    { "metric": "R2", "operator": ">=", "threshold": 0.98, "unit": "-" },
    { "metric": "cov_percent", "operator": "<=", "threshold": 5.0, "unit": "%" }
  ],
  "spec_refs": [
    "Derivation/EQUATIONS.md#vdm-e-105",
    "Derivation/Unification/T0_Unification_Program_Spec_v1.md"
  ],
  "registration_timestamp": "<ISO-8601>"
}
```

---

## 10. Runner Specs and Paths (skeleton)

Specs file (example):

```json
{
  "run_name": "telegraph-relaxation-v1",
  "version": "1.0.0",
  "tag": "telegraph-relaxation-v1",
  "schema_ref": "Derivation/code/physics/transport/schemas/telegraph-from-relaxation.v1.schema.json",
  "parameters": {
    "D_list": [0.05,0.1,0.2,0.4],
    "tau_list": [0.25,0.5,1.0,2.0],
    "N": 1024,
    "bc": "periodic",
    "pulse": { "A": 1e-3, "sigma_dx": 6 },
    "estimators": ["threshold","xcorr"]
  },
  "seeds": [0,1,2,3,4,5,6,7,8,9]
}
```

Schema stub (minimum keys):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "telegraph-from-relaxation.v1.schema.json",
  "title": "Telegraph From Relaxation - v1",
  "type": "object",
  "properties": {
    "D_list": { "type": "array", "items": { "type": "number", "exclusiveMinimum": 0 } },
    "tau_list": { "type": "array", "items": { "type": "number", "exclusiveMinimum": 0 } },
    "N": { "type": "integer", "minimum": 64 },
    "bc": { "type": "string", "enum": ["periodic","neumann"] },
    "pulse": {
      "type": "object",
      "properties": {
        "A": { "type": "number", "exclusiveMinimum": 0 },
        "sigma_dx": { "type": "number", "exclusiveMinimum": 0 }
      },
      "required": ["A","sigma_dx"]
    },
    "estimators": { "type": "array", "items": { "type": "string", "enum": ["threshold","xcorr"] }, "minItems": 1 }
  },
  "required": ["D_list","tau_list","N","bc","pulse","estimators"]
}
```

---

## 11. Deliverables

Minimum artifacts per run (per tag):

- 1 PNG: regression plot(s) of $\log \hat c$ vs $\tfrac12(\log D-\log \tau)$ and residuals.  
- 1 CSV: per-point $(D,\tau,\hat c,\text{estimator})$ plus fit summary.  
- 1 JSON: full provenance, gates, verdicts, and environment hashes.

All routed via [io_paths.py](Derivation/code/common/io_paths.py:1) with seeds and commit recorded.

---

## 12. Escalation Path

- If T1 passes gates, promote to T2 (Instrument) by freezing specs and extending parameter ranges.  
- For cross-domain validation, compare pulse cone with KG J-only locality meters; ensure no violations of $v\le c(1+\varepsilon)$ per [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md:1).

---

## 13. References (canon anchors)

- [VDM-E-105](Derivation/EQUATIONS.md#vdm-e-105)  
- [Derivation/Unification/T0_Unification_Program_Spec_v1.md](Derivation/Unification/T0_Unification_Program_Spec_v1.md:326)  
- [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md:1)  
- [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md:1)
