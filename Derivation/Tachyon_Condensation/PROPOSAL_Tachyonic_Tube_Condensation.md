# Tachyonic Tube Condensation and Spectrum (Proposal)

Date: 2025-10-09

## 1. Proposal Title and Date

Tachyonic Tube Condensation and Discrete Spectrum Characterization - 2025-10-09

## 2. Proposers and Institutions

Justin K. Lietz - Neuroca, Inc.

## 3. Abstract

We propose to compute and validate the discrete tachyonic spectrum and condensation profile of a finite-radius cylindrical tube in the FUM scalar EFT with piecewise mass term $m^2(r)$ featuring an unstable interior ($m_{\text{in}}^2=-\mu^2$) and stabilized exterior ($m_{\text{out}}^2=2\mu^2$). We will (1) solve the secular equation for modified Bessel radial modes across a sweep of radii $R$, (2) project the quartic self-interaction $\lambda \phi^4$ onto individual modes (diagonal baseline) to obtain $N4_\ell$, (3) determine condensate amplitudes $v_\ell$ via a tree-level effective potential minimization, and (4) map the post-condensation energy landscape $E(R)$ to identify preferred tube radii. Canon promotion requires reproducible mode spectrum CSVs, condensation energy scans, and figures pinned under approved tags.

## 4. Background & Scientific Rationale

Finite-radius tachyonic domains arise in early-universe symmetry breaking and metastable phase defects. The tube geometry gives a controlled testbed for radial confinement and boundary stabilization relevant to cosmic strings and condensed matter analogues. Existing derivation notes (finite_tube_mode_analysis.md) outline the secular equation:
$$\left(\frac{\kappa_{\text{in}}}{\kappa_{\text{out}}}\right) \frac{I'_{\ell}(\kappa_{\text{in}} R)}{I_{\ell}(\kappa_{\text{in}} R)} + \frac{K'_{\ell}(\kappa_{\text{out}} R)}{K_{\ell}(\kappa_{\text{out}} R)} = 0,$$
with $\kappa_{\text{in}}^2 = \mu^2/c^2 - \kappa^2$ and $\kappa_{\text{out}}^2 = \kappa^2 + 2\mu^2/c^2$. Unstable modes ($\omega^2 < 0$) drive condensation. Determining $E(R)$ post-condensation illuminates whether finite tubes persist, shrink, or expand under the effective field dynamics.

## 5. Intellectual Merit and Procedure

The experiment quantifies confinement energetics and mass lifting for tachyonic modes. It provides a reproducible baseline against which off-diagonal quartic corrections and quantum fluctuations can be layered. Results inform defect stability criteria and scaling relations.

### 5.1 Experimental Setup and Diagnostics

Parameters: $\mu$, $\lambda$, $c$, $\ell_{\max}$. Diagnostics: (a) root-finding convergence counts, (b) per-mode $\kappa_\ell$, $N4_\ell$, $v_\ell$, $M_\ell^2$, (c) energy scan $E(R)$ and minima statistics. Artifacts: spectrum CSV per tag, condensation summary JSON, energy scan figure + CSV. Scripts: `cylinder_modes.py`, new runner `run_tachyon_tube.py`. No new external libraries beyond SciPy.

### 5.2 Experimental Runplan

1. Spectrum phase (tag: tube-spectrum-v1): For a sweep of radii $R \in R_{\text{sweep}}$, compute lowest $\kappa_\ell$ per $\ell \le \ell_{\max}$; output CSV with columns $(R, \ell, \kappa, k_{\text{in}}, k_{\text{out}})$. Gate: root solver success fraction $>95\%$ (finite rows present for $\ell=0..\ell_{\max}$ except tolerable misses at high $\ell$ when $R$ small).
2. Condensation phase (tag: tube-condensation-v1): For each $R$ compute diagonal quartic $N4_\ell$, condensates $v_\ell$, post-condensation masses $M_\ell^2$, and energy $E(R)$. Produce figure $E(R)$ vs $R$. Gate: (a) $E(R)$ finite for $\ge 80\%$ of $R$ samples, (b) identified minimum radius stable under local quadratic fit (second derivative $>0$ within 10% variation).
3. Logging: JSON summary with statistics (min radius, fraction finite, mode count distribution). Failures route to `failed_runs/` per policy.
4. Approval: Tag-specific schemas; HMAC script-based manifest approval required before promotion.
5. Promotion: Once gates pass, produce RESULTS doc summarizing equations and artifact paths; update CANON_PROGRESS row from PLAUSIBLE to PROVEN.

### 5.3 Background energy (optional) and acceptance gates

To model physical surface/core costs consistently with the derivation notes, we optionally include a background term

$$E_{\text{bg}}(R) = 2\pi\,\sigma\,R + \frac{\alpha}{R},$$

with $\sigma \ge 0$ and $\alpha \ge 0$ (documented in the spec when used). This shifts $E(R)$ without altering the diagonal-\(\lambda\) projection mechanics and helps reveal an interior minimum when the diagonal baseline alone is monotone.

Acceptance gates (explicit):

- Spectrum (tube-spectrum-v1): coverage $\ge 0.95$ across $(R,\ell)$ attempts; at least one low-$\ell$ mode (e.g., $\ell\le 2$) detected for some $R$ (robustness check).
- Condensation (tube-condensation-v1): finite fraction $\ge 0.90$ and an interior minimum certified by either (i) a positive quadratic curvature (fit $a>0$) on a local window around the minimum, or (ii) a discrete second difference $\Delta^2 E(R_i) = E_{i+1}-2E_i+E_{i-1} > 0$ at an interior index $i$.

Both tags are pre-registered with JSON Schemas that pin the tag constant; approvals are script-scoped and recorded in `Derivation/code/physics/tachyonic_condensation/APPROVAL.json`.

Success path: Gates satisfied, stable minimum radius identified. Failure path: Insufficient root coverage or ill-conditioned energy integrals; adjust sweep or tolerance and re-run after amendment.

Runtime estimate: < 2 minutes per tag (ell_max=8, modest R grid) on standard workstation.

### Plan for Failed Experiment

Annotate JSON with failure reasons, adjust `num_brackets`, `dr`, or extend $R$ range; re-attempt after parameter refinement. Preserve original logs under `failed_runs/` for audit.

### Publication & Display

Artifacts embedded in RESULTS markdown with MathJax; CSV/JSON path references relative to `Derivation/`.

## 6. Personnel

Justin K. Lietz: design, implementation, approval, analysis, documentation.

## 7. References
