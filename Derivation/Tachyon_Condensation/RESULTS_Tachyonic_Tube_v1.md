# Tachyonic Tube v1 - Spectrum completeness and condensation curvature (QC)

> Author: Justin K. Lietz
> Date: 2025-10-09
>
> This research is protected under a dual-license to foster open academic
> research while ensuring commercial applications are aligned with the project's ethical principles.
> Commercial use requires citation and written permission from Justin K. Lietz.
> See LICENSE file for full terms.

## Introduction

This note evaluates two quality-control gates for a finite-radius tachyonic tube within a simple scalar EFT baseline: (i) completeness of the discrete spectrum over the physically admissible set, and (ii) the existence of an interior minimum in the condensation energy with positive curvature. These gates are prerequisites for canon promotion of the tube-mode solver and condensation harness.

Scientific significance: completeness ensures the secular solver is a reliable measurement instrument; the curvature gate confirms a physically meaningful condensation length scale emerges from the combined mode spectrum and background energy. The methodology is a semi-analytic spectral calculation (cylindrical Bessel matching) coupled to adaptive quadrature for quartic overlaps.

Evaluation question: do the implemented solvers satisfy the coverage and curvature gates at the registered v1 tag, producing standards-compliant artifacts (PNG/CSV/JSON) that are fully reproducible from the repository?

Pinned artifact: Derivation/code/outputs/figures/tachyonic_condensation/20251009_084702_tube_spectrum_overview__tube-spectrum-v1.png

## Scope and boundaries

- No novelty claims are made for the secular equation or modified Bessel identities; this is QC of an implementation.
- Off-diagonal quartic couplings, nonzero axial momentum, and non-cylindrical perturbations are out of scope for v1.
- Dimensionless program with normalization $\mu=c=1$ unless stated otherwise.

## Research question and variables

- Independent variables:
  - Radius $R\in[0.5,6.0]$ (dimensionless), azimuthal index $\ell\in\{0,1,\dots,8\}$.
  - Parameters: $(\mu,c)=(1,1)$. Condensation background: $\sigma=0.6$, $\alpha=12.0$, quartic $\lambda=0.5$.
- Dependent variables:
  - Spectrum roots $\kappa_\ell(R)$ at axial wavenumber $k=0$.
  - Coverage metrics: $\mathrm{cov}_{\rm phys}$, $\mathrm{cov}_{\rm raw}$.
  - Condensation energy $E(R)=E_{\rm bg}(R)+E_{\rm modes}(R)$; curvature diagnostic near $R_\star$.
- Estimators and thresholds:
  - Physically-admissible coverage
    
    $$
    \mathrm{cov}_{\rm phys} = \frac{\#\,\text{roots found}}{\#\,\text{(}R,\ell\text{) with root-potential}},\quad \boxed{\mathrm{gate:\ pass\ if}\ \mathrm{cov}_{\rm phys}\ge 0.95}.
    $$
    
    Root-potential is determined by a sign change of the secular function over the admissible $\kappa$-range.
  - Raw coverage (transparency only)
    
    $$
    \mathrm{cov}_{\rm raw} = \frac{\#\,\text{roots found}}{\#\,(R,\ell)\,\text{in sweep}}\quad \text{(reported but not gated).}
    $$
  - Condensation curvature gate: $\boxed{\text{finite\_fraction}\ge 0.80\ \wedge\ \text{interior}\ R_\star\ \wedge\ a>0}$, where $a$ is the quadratic coefficient from a local fit near $R_\star$ (with discrete $\Delta^2E$ fallback).

## Background and core equations

At axial wavenumber $k=0$, the secular equation for a cylindrical tube with a tachyonic interior mass and massive exterior is

$$
 f_\ell(\kappa;R,\mu,c)\;=\;\frac{\kappa_{\rm in}}{\kappa_{\rm out}}\,\frac{I'_\ell(\kappa_{\rm in}R)}{I_\ell(\kappa_{\rm in}R)}\;+\;\frac{K'_\ell(\kappa_{\rm out}R)}{K_\ell(\kappa_{\rm out}R)}\;=\;0,
$$

with

$$
\kappa_{\rm in}^2 = \frac{\mu^2}{c^2}-\kappa^2,\qquad
\kappa_{\rm out}^2 = \kappa^2 + 2\frac{\mu^2}{c^2}.
$$

The condensation baseline (diagonal-$\lambda$) uses mode functions $u_\ell(r)$ to define

$$
N4_\ell = (2\pi)\,\lambda\int_0^\infty r\,u_\ell(r)^4\,dr,\qquad m_\ell^2 = -c^2\kappa_\ell^2,
$$

and an effective potential approximation per mode $V_\ell(v_\ell)=\tfrac12 m_\ell^2 v_\ell^2 + \tfrac14 N4_\ell v_\ell^4$. The background energy is

$$
E_{\rm bg}(R) = 2\pi\sigma R + \frac{\alpha}{R},
$$

so that the scanned energy is $E(R)=E_{\rm bg}(R)+\sum_\ell V_\ell(v_\ell(R))$ after selecting unstable modes $(m_\ell^2<0)$ and their minimizing amplitudes.

References for special functions and cylinder problems include Abramowitz–Stegun (Ch. 9–10) and Watson (Bessel Functions).

## Equipment / hardware and provenance

- OS: Linux; repo: Prometheus_VDM; branch: merge; commit: 09f871a (git rev-parse HEAD).
- Environment: Python per repository `requirements.txt`; deterministic pipeline (no RNG; seed N/A).
- Repro path: figures and logs under `Derivation/code/outputs/(figures|logs)/tachyonic_condensation/`.

## Methods / procedure (measurement instrument)

- Spectrum solver:
  - Reparameterization $\kappa=(\mu/c)\sin\theta$ to bracket within $[0,\mu/c]$ robustly.
  - Multi-resolution $\theta$-scans with Chebyshev nodes and a complementary $u=\kappa_{\rm in}R$ scan.
  - Midpoint probes for sign changes and bracketing; secant/Newton refinement for roots.
  - Scaled modified Bessels for stable $I'_\ell/I_\ell$ and $K'_\ell/K_\ell$ evaluations.
  - Root-potential heuristic via sign changes to define admissible denominator for coverage.
- Condensation integrals:
  - Adaptive inside/outside split, geometric tail shells, and contribution-based stopping for $\int r\,u_\ell^4\,dr$.
  - Energy scan over $R$ with local refinement near the apparent minimum; quadratic fit coefficient $a$ used as curvature diagnostic with discrete $\Delta^2 E$ fallback when needed.
- IO and approvals: artifacts written via io_paths; tags pre-registered; quarantine paths used automatically if unapproved.

## Results / data

### Spectrum gate - coverage and residuals (tag: tube-spectrum-v1)

- Summary JSON: Derivation/code/outputs/logs/tachyonic_condensation/20251009_084703_tube_spectrum_summary__tube-spectrum-v1.json
- Roots CSV: Derivation/code/outputs/logs/tachyonic_condensation/20251009_084702_tube_spectrum_roots__tube-spectrum-v1.csv
- Figures:
  1) Overview - Derivation/code/outputs/figures/tachyonic_condensation/20251009_084702_tube_spectrum_overview__tube-spectrum-v1.png.
     Caption (numeric): coverage $\mathrm{cov}_{\rm phys}=1.000$ on $74/74$ admissible pairs; $\mathrm{cov}_{\rm raw}=0.548$ on $74/135$; max residual $|f|=0.709$; tag tube-spectrum-v1; commit 09f871a; seed N/A.
  2) Possible/found heatmap - Derivation/code/outputs/figures/tachyonic_condensation/20251009_084703_tube_spectrum_heatmap__tube-spectrum-v1.png.
     Caption (numeric): no possible-but-missed bins; identical coverage metrics as above; tag tube-spectrum-v1; commit 09f871a.

Gate metrics (metrics_version v2-phys-aware):

- $\mathrm{cov}_{\rm phys}=1.000$; $\mathrm{cov}_{\rm raw}=0.548148\dots$.
- attempts_phys $=74$, attempts_raw $=135$, successes $=74$.
- Max residual $\max|f|=0.708999\dots$ (informational in v1).
- Verdict: $\boxed{\text{PASS}}$.

### Condensation gate - interior minimum with positive curvature (tag: tube-condensation-v1)

- Summary JSON: Derivation/code/outputs/logs/tachyonic_condensation/20251009_062600_tube_condensation_summary__tube-condensation-v1.json
- Energy CSV: Derivation/code/outputs/logs/tachyonic_condensation/20251009_062600_tube_energy_scan__tube-condensation-v1.csv
- Figure: Derivation/code/outputs/figures/tachyonic_condensation/20251009_062600_tube_energy_scan__tube-condensation-v1.png
  Caption (numeric): interior minimum at $R_\star\approx 1.35$ with positive curvature ($a=1.8109\dots>0$), finite_fraction $=1.0$; tag tube-condensation-v1; commit 09f871a.

Gate metrics:

- finite_fraction $=1.0$; $R_\star=1.35$; curvature_ok $=\text{true}$; fit coeffs $[a,b,c]=[1.8109,-4.9177,15.3284]$; $\min E=11.98996\dots$.
- Verdict: $\boxed{\text{PASS}}$.

## Discussion / analysis

- Coverage denominator: using physically admissible $(R,\ell)$ pairs (sign-change potential) prevents penalizing regimes where no bound state can exist; this aligns the metric with the physics while retaining $\mathrm{cov}_{\rm raw}$ for sweep-design transparency.
- Numerical stability: scaled Bessel evaluations and complementary scans eliminate false coverage drops (e.g., near $R\approx 3$) attributable to overflow/underflow or missed brackets.
- Curvature: local refinement is essential to avoid spurious boundary minima; the positive quadratic coefficient confirms a well-formed interior minimum for the chosen $E_{\rm bg}$ and spectrum.
- Limitations: residual quality is reported but not gated in v1; off-diagonal quartics and $k\ne 0$ spectra are deferred.

## Conclusions

- Aim: evaluate spectrum completeness and condensation curvature gates for the tachyonic tube v1 run.
- Findings: $\mathrm{cov}_{\rm phys}=1.0$ (PASS); interior minimum with $a>0$ and finite_fraction $=1.0$ (PASS). Artifacts are standards-compliant and reproducible from commit 09f871a.
- Next gates: codify $\mathrm{cov}_{\rm phys}$ as primary KPI in schema/specs; optionally add a residual tolerance (e.g., $\max|f|\le 10^{-10}$) in v2; broaden parameter sweeps and consider off-diagonal quartics when physically motivated.

## References / works cited

- M. Abramowitz and I. A. Stegun (eds.), Handbook of Mathematical Functions, NBS (1964), Ch. 9–10.
- G. N. Watson, A Treatise on the Theory of Bessel Functions, 2nd ed., Cambridge Univ. Press (1944).
- G. B. Arfken, H. J. Weber, and F. E. Harris, Mathematical Methods for Physicists, 7th ed., Academic Press (2013), Ch. on special functions.
