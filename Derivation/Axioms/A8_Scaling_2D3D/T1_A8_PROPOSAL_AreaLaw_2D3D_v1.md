# T1 (Proto-model) — A8 Area-Law Instrument in 2D/3D Domains

> Created Date: 2025-11-05  
> Commit: cbc3dd1  
> Salted provenance (pre-reg to compute): {base_sha256}:{salt_hex}:{salted_sha256}  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE

Short summary (TL;DR):  
Instrument to measure boundary area-law scaling of the excess energy in $d\in\{2,3\}$ under tachyonic regimes, testing the spec-level relation $E_{\mathrm{exc}}(L)\sim L^{\,d-1}$ with deterministic meters, artifact routing, and acceptance gates.

---

## 1. Scope and Alignment

- Canon anchor equation: [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113) (Excess-energy scaling at boundaries, spec-level)  
- Companion context (tachyonic regime flag and hierarchy program):  
  - [VDM-E-112](Derivation/EQUATIONS.md#vdm-e-112) (tachyonic condition, spec-level)  
  - A8 candidate statements and plans in [T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md](Derivation/Axioms/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md:19)  
- Policy/gates: [VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md:1), [RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md:1), [ARCHITECTURE.md](Derivation/code/ARCHITECTURE.md:1)

This is a T1 instrument proposal (no claims beyond meters). It generalizes the existing 1D instrument to $d=2,3$ and focuses strictly on testing $E_{\mathrm{exc}}(L)\sim L^{\,d-1}$ using reproducible meters and gates.

Assumptions and limitations:

- Homogeneous medium; periodic or no-flux boundaries as specified.  
- Tachyonic regime validation ($V''(0)<0$) is a pre-check for input configurations (instrument logs the check).  
- Instrument does not prove A8; it only measures and evaluates the area-law with quantitative gates.

---

## 2. Background & Rationale

Analogy. In systems where interfaces concentrate energy, the excess energy within a region of linear size $L$ should scale with the size of its boundary, not its volume. In $d$ spatial dimensions, boundary measure scales as $L^{\,d-1}$, hence the area-law hypothesis $E_{\mathrm{exc}}(L)\sim L^{\,d-1}$.

Precise math references:

- Target relation: [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113).  
- Tachyonic regime: [VDM-E-112](Derivation/EQUATIONS.md#vdm-e-112).  
- 1D companion instrument: [T1_PROPOSAL_A8_1D_Scaling_v1.md](Derivation/Axioms/A8_Scaling_1D/T1_PROPOSAL_A8_1D_Scaling_v1.md:1).

---

## 3. Instrument Design

3.1 Measured quantity: Excess energy  
For a field configuration $\phi$ on domain $\Omega_L\subset\mathbb{R}^d$ of linear size $L$, define

- $E[\phi;\Omega_L] = \int_{\Omega_L}\left(\frac{\kappa}{2}\lvert\nabla \phi\rvert^2 + V(\phi)\right)\,dx$  
- $E_{\mathrm{exc}}(L)=E[\phi;\Omega_L]-E_{\min}(\Omega_L)$

Here $E_{\min}(\Omega_L)$ is the minimal bulk reference energy under the same parameters but without interfaces (instrument computes a numerical baseline; its construction and constants are reported in JSON).

3.2 Detectors (interfaces and boundary masks)

- Interface detectors: threshold-crossing on $|\phi|$, total variation (TV) peaks, and multiscale structure-tensor indicators extended to $d=2,3$.  
- Boundary mask for energy attribution near interfaces: an $\epsilon$-neighborhood $\mathcal{N}_\epsilon(\Gamma)$ of detected interface set $\Gamma$, with sensitivity scans over $\epsilon$ (reported).  
- Optional morphological cleanup: opening/closing with scale tied to grid spacing to remove speckles (parameters logged).

3.3 Domain sequences and blocking

- Families of cubic (or square) domains $\Omega_L$ with $L\in\{L_1,\dots,L_m\}$, grid spacing $\Delta x=L/N$ with $N$ proportional to $L$ to keep resolution fixed across scales.  
- Seeds: independent draws of initial noise/perturbations; instrument aggregates across seeds via medians and bootstrap CIs.

3.4 Dynamics (if relaxation run is needed)

- Either direct sampling of steady/metastable snapshots (if precomputed), or short relaxation runs to near-stationary states using a metriplectic M-limb step (documented) without claiming dynamics; this keeps the instrument T1 (meter only).

Artifacts routing (required):

- Figures → Derivation/code/outputs/figures/axioms/a8_area_law_2d3d/  
- Logs (CSV, JSON) → Derivation/code/outputs/logs/axioms/a8_area_law_2d3d/  
All via [io_paths.py](Derivation/code/common/io_paths.py:1).

---

## 4. Acceptance Gates

Primary area-law gate (per dimension $d=2$ or $d=3$):

- Fit $\log E_{\mathrm{exc}}(L)$ vs $\log L$; expected slope $\hat\alpha \approx d-1$.  
- Acceptance band: $|\hat\alpha - (d-1)| \le 0.1$ with $R^2 \ge 0.98$.  
- Report CI for $\hat\alpha$ via bootstrap across seeds; report detector/threshold sensitivity bands.

Secondary gates (quality controls):

- Detector robustness: for the accepted $\epsilon$-neighborhood, detector kind, and threshold, area-law slope must stay within ±0.1 across at least two detector families (e.g., threshold and TV).  
- Resolution robustness: two-resolution check (refined grid) must keep $|\Delta \hat\alpha|\le 0.05$ and preserve $R^2 \ge 0.98$ on the subset evaluated.

Regime gate (tachyonic pre-check):

- Numeric validation that $V''(0)<0$ for the supplied potential $V(\cdot)$; runs failing this check are invalid and quarantined.

---

## 5. Methods

5.1 Domain and BCs  

- $d=2$: square domains; $d=3$: cubic domains. Periodic or no-flux BC; record choice in JSON.  
- $N\in\{256,512\}$ typical for 2D; $N\in\{64,96,128\}$ for 3D baseline (CPU-friendly), with an explicit plan to re-run a subset at finer resolution.

5.2 Detector specifics  

- Threshold detector: count/locate interface voxels where $|\phi|\ge \theta$ (tunable $\theta$), then construct boundary mask $\mathcal{N}_\epsilon(\Gamma)$.  
- TV detector: locate maxima of the discrete gradient magnitude field smoothed at a scale tied to $\Delta x$.  
- Structure tensor (2D/3D): eigen-analysis of local gradient covariance with non-maximum suppression for ridge-like features.

5.3 Energy accounting  

- Compute $E[\phi;\Omega_L]$ on grid via central differences and quadrature matching the scheme order.  
- Estimate $E_{\min}(\Omega_L)$ using uniform bulk phase(s) without interfaces; choose vacuum value(s) from the instrument’s $V(\cdot)$ and parameters and report method (single-phase vs. weighted two-phase) in JSON.  
- Attribute a fraction of $E_{\mathrm{exc}}$ to $\mathcal{N}_\epsilon(\Gamma)$ for diagnostics (informational); the primary fit uses the total $E_{\mathrm{exc}}(L)$.

5.4 Regression and reporting  

- For each $d$ and each detector, regress $\log E_{\mathrm{exc}}$ vs $\log L$ across $L$; report slope, intercept, $R^2$, CIs.  
- Aggregate across seeds by medians; report interquartile ranges and bootstrap CIs.

---

## 6. Variables and Ranges

- Independent: $L$ (domain size), detector kind (threshold/TV/structure-tensor), detector thresholds $(\theta,\epsilon)$, seeds.  
- Dependent: slope $\hat\alpha$, $R^2$, detector robustness score, resolution robustness delta.  
- Controls: $(N, \Delta x)$, BC, potential and coefficients, relaxation step parameters (if used).

Default sweep (example):

- $L\in\{128,256,512,1024\}$ (2D), $L\in\{64,96,128\}$ (3D baseline).  
- Detectors: threshold $(\theta=0.5)$, TV; $\epsilon\in\{1,2,3\}\times \Delta x$.  
- Seeds $=10$.

---

## 7. Risks and Mitigations

- Detector bias: use multiple detector families and report sensitivity bands; gate requires consistency across at least two families.  
- Finite-size artifacts: discard smallest $L$ if it materially degrades $R^2$ (pre-registered rule); document discard in JSON.  
- Under-resolved interfaces: enforce minimum interface thickness in voxels; re-run at refined grid for subset.

---

## 8. Provenance & Approvals

Approvals required before any artifact-emitting run: see [Derivation/code/common/authorization/README.md](Derivation/code/common/authorization/README.md:1).  
Artifacts quarantined on gate failure; contradiction reports include commit, salted proposal hash, seeds, configurations, and diffs.

---

## 9. Pre-registration JSON (template)

```json
{
  "proposal_title": "T1 - A8 Area-Law Instrument (2D/3D)",
  "tier_grade": "T1",
  "commit": "cbc3dd1",
  "salted_provenance": "<to-be-filled>",
  "contact": ["Justin K. Lietz <justin@neuroca.ai>"],
  "hypotheses": [
    { "id": "H1", "statement": "In d=2, slope alpha ≈ 1.0 ± 0.1 with R^2 ≥ 0.98.", "direction": "no-change" },
    { "id": "H2", "statement": "In d=3, slope alpha ≈ 2.0 ± 0.1 with R^2 ≥ 0.98.", "direction": "no-change" },
    { "id": "H3", "statement": "Detector-robustness holds: |Δalpha| ≤ 0.1 across two detector families.", "direction": "no-change" },
    { "id": "H4", "statement": "Resolution-robustness holds: |Δalpha_refined| ≤ 0.05; R^2 stays ≥ 0.98.", "direction": "no-change" }
  ],
  "variables": {
    "independent": ["L","detector_kind","theta","epsilon","seed"],
    "dependent": ["alpha","R2","alpha_delta_detector","alpha_delta_refine"],
    "controls": ["N","dx","BC","potential","coeffs"]
  },
  "pass_fail": [
    { "metric": "alpha_band", "operator": "==", "threshold": true, "unit": "-" },
    { "metric": "R2", "operator": ">=", "threshold": 0.98, "unit": "-" }
  ],
  "spec_refs": ["Derivation/EQUATIONS.md#vdm-e-113", "Derivation/EQUATIONS.md#vdm-e-112"],
  "registration_timestamp": "<ISO-8601>"
}
```

---

## 10. Specs & Schemas (skeleton)

Specs path (example):

- Derivation/code/physics/axioms/a8/specs/a8-area-law-2d3d.v1.json

Schema path:

- Derivation/code/physics/axioms/a8/schemas/a8-area-law-2d3d.v1.schema.json

Schema stub (minimum keys):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "a8-area-law-2d3d.v1.schema.json",
  "title": "A8 Area-Law 2D/3D - v1",
  "type": "object",
  "properties": {
    "dims": { "type": "integer", "enum": [2,3] },
    "L_list": { "type": "array", "items": { "type": "integer", "minimum": 32 }, "minItems": 3 },
    "detectors": { "type": "array", "items": { "type": "string", "enum": ["threshold","tv","structure"] }, "minItems": 1 },
    "theta": { "type": "number", "minimum": 0 },
    "epsilon_vox": { "type": "integer", "minimum": 1 },
    "N": { "type": "integer", "minimum": 32 },
    "bc": { "type": "string", "enum": ["periodic","neumann"] },
    "potential": { "type": "string" },
    "coeffs": { "type": "object" },
    "seeds": { "type": "array", "items": { "type": "integer", "minimum": 0 }, "minItems": 1 }
  },
  "required": ["dims","L_list","detectors","epsilon_vox","N","bc","potential","coeffs","seeds"]
}
```

---

## 11. Deliverables

Per tag, emit:

- 1+ PNGs: log–log fits of $E_{\mathrm{exc}}$ vs $L$ per detector, residuals, detector/threshold sensitivity bands, resolution robustness panels.  
- 1 CSV: per-$L$ and per-detector entries with $E_{\mathrm{exc}}$, slope fit summaries.  
- 1 JSON: full provenance, configurations, gate metrics, verdicts, environment hashes.

Routes:

- Figures → Derivation/code/outputs/figures/axioms/a8_area_law_2d3d/  
- Logs → Derivation/code/outputs/logs/axioms/a8_area_law_2d3d/

---

## 12. Escalation Path

- Promote to T2 (Instrument) upon PASS; freeze specs and extend parameter ranges.  
- Joint analysis with the 1D instrument to build multi-D evidence for A8; if robust, advance to T4 prereg for A8 claims with preregistered gates and broader sweeps.

---

## 13. References (canon anchors)

- [VDM-E-113](Derivation/EQUATIONS.md#vdm-e-113), [VDM-E-112](Derivation/EQUATIONS.md#vdm-e-112)  
- [Derivation/VALIDATION_METRICS.md](Derivation/VALIDATION_METRICS.md:1)  
- [Derivation/Templates/RESULTS_PAPER_STANDARDS.md](Derivation/Templates/RESULTS_PAPER_STANDARDS.md:1)
