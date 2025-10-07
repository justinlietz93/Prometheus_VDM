# Proposal: Decoherence Portals via Dark-Photon Mixing (DP-Portal-v1)

Date: 2025-10-06



Decoherence Portals via Dark-Photon Mixing: Noise-Spectrum and Fisher-Budget Tests of Kinetic Mixing in Shielded Cavities (DP-Portal-v1) — 2025-10-06

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz (Independent Researcher)

## 3. Abstract

We propose a disciplined, pre-registered investigation of dark-photon (DP) kinetic mixing as a decoherence portal that leaves measurable imprints in precision electromagnetic noise spectra and parameter-estimation Fisher budgets in shielded resonant cavities. The central hypothesis is that a small kinetic-mixing parameter $\varepsilon$ produces: (i) a predictable modification of the power spectral density (PSD) in well-characterized frequency bands, and (ii) a reproducible scaling of information content (Fisher matrix elements) with integration time and bandwidth under stationary Gaussian assumptions. We define falsifiable key performance indicators (KPIs) a priori, specify calibration and control runs, and separate modeling from execution. No experimental results are reported in this proposal; only testable predictions and a rigorous plan. Success would constrain or detect portal-like decoherence consistent with DP mixing, with clear follow-up pathways to stronger limits and systematics stress tests.

## 4. Background & Scientific Rationale

Dark photons arise from an additional $U(1)$ gauge sector with kinetic mixing with the Standard Model photon parameterized by $\varepsilon$ [Holdom 1986]. Precision laboratory searches often target resonant enhancement or low-noise readout to reveal feeble signals [Jaeckel & Ringwald 2010; Fabbrichesi et al. 2020]. A pragmatic intermediate step toward discovery is to pre-register robust, instrument-level signatures that are insensitive to detailed UV model choices yet directly test kinetic-mixing consequences: noise-spectrum perturbations and consistent parameter-estimation scaling.

We pursue two orthogonal, model-minimal probes:

1) PSD portal signature: In a cryogenic, shielded cavity with well-calibrated readout chain, DP mixing effectively introduces a weak, broadband or narrow-band excess consistent with an additional, stationary Gaussian source coupled proportionally to $\varepsilon^2$. After accounting for known floors (Johnson–Nyquist $4k_BTR$, amplifier white floor, and $1/f$ knees), a DP-compatible excess induces a frequency-localized deviation bounded by calibration priors.

2) Fisher-budget consistency: For a parameterized spectral model (background + DP component), the Fisher information $\mathcal{I}(\theta)$ for parameter(s) $\theta$ (e.g., amplitude of a template with central frequency $f_\star$ and width $\Delta f$) should scale with integration time $\tau$ and bandwidth $B$ as predicted under stationary Gaussian noise. Any systematic departure beyond pre-registered tolerance indicates unmodeled systematics and falsifies the DP interpretation.

Intellectual Merit: The plan targets instrument-level, falsifiable predictions grounded in inference theory and RF metrology, providing a clean split between modeling and execution and supplying robust null results should no signal be present. Broader Impacts: The approach yields re-usable calibration datasets and standardized KPIs for related searches (hidden photons, axionlike particles coupled to EM, precision sensing).

### Questions considered

- Novelty: This proposal couples spectrally explicit, pre-registered PSD signatures with a Fisher-consistency gate, emphasizing disciplined falsifiability before data-taking.
- Why now: Modern low-noise RF chains and open protocols enable clean separation of modeling and execution; pre-registration prevents bias and p-hacking.
- Target findings: Either a bounded excess consistent across calibration states or tightened constraints on $\varepsilon$ in the explored band; Fisher scaling adherence within tolerance.
- Impacted areas: Precision electromagnetism, beyond-Standard-Model portals, quantum sensing.
- Fundamental question: Does kinetic mixing leave a detectable, reproducible decoherence footprint in controlled EM environments?
- Potential criticisms: Instrumental systematics masquerading as excess; we address with calibration ladders, line-injection checks, and strict tolerance gates.

## 5.1 Experimental Setup and Diagnostics

Instrumentation (baseline):

- Shielded resonant RF cavity (Q characterized), tunable center frequency covering $f\in[\,10^3,10^6\,]$ Hz (example band; exact band to be set by available hardware).
- Cryogenic front-end with known $T_{\mathrm{phys}}$ and calibrated readout chain; spectrum analyzer or digitizer with anti-alias filters.
- Calibration injection path (synthesizer) for known narrowband tones and broadband noise of known PSD.

Parameters to control/record:

- Physical temperature $T$, load resistance $R$, gain and noise figure vs frequency, sampling rate, BW $B$, integration time $\tau$, cavity Q and coupling, shield state.

Diagnostics and counts:

- PSD measurements across $N_f$ logarithmically spaced frequencies per setting (frequency sweep), with repeated runs for stability (at least 3 repeats per configuration).
- Calibration ladder: thermal-only, amplifier-only, injected-tone(s), injected-broadband at known levels.
- Housekeeping logs: environmental monitors, EMI surveys, shield integrity checks.

## 5.2 Experimental runplan

Pre-registration (this document):

- Models: Background PSD $S_{\mathrm{bg}}(f)$ comprising thermal + amplifier white + $1/f$ knees; DP component $S_{\mathrm{DP}}(f;\varepsilon, f_\star, \Delta f)$.
- KPIs and tolerance gates (defined below) fixed before data collection.

Execution phases:

1) Calibration characterization: Fit $S_{\mathrm{bg}}(f)$ under thermal-only and amplifier-only settings; validate monotone/shape expectations within tolerance.
2) Injection validation: Verify recovery of known injected tones and broadband; confirm Fisher scaling with $\tau$ and $B$.
3) Science run(s): Acquire shielded-cavity data across the target band with consistent settings; blind any DP-parameter channels if applicable.

Contingencies:

- Success path: KPIs pass; proceed to parameter inference and constraints on $\varepsilon$ with systematic budget.
- Failure path: Any gate fails triggers a CONTRADICTION_REPORT with raw artifacts and root-cause analysis; no claims about DP signals are made.

### Pre-registered KPIs (no results claimed here)

1) PSD sanity and regime annotation (background-only):
   - Finite and non-negative PSD across all bins; $1/f$ component monotone for low-$f$ segment.
   - Annotate $f_\star$ where $S_{\mathrm{inst}}(f_\star) \approx S_{\mathrm{thermal}}(f_\star)$ by closest approach; used for reporting only.

2) Fisher consistency gate (injection or background-only as appropriate):
   - For parameter $\theta$ representing a template amplitude, analytic Fisher $\mathcal{I}_{\mathrm{an}}(\theta)$ matches finite-difference Hessian $\mathcal{I}_{\mathrm{fd}}(\theta)$ within relative error $\leq 10\%$ under stationary Gaussian assumptions.
   - Scaling: $\mathcal{I} \propto \tau\,B$ within tolerance band set by calibration uncertainties.

3) DP template test (science run, model comparison only):
   - Reported only if (1) and (2) PASS. Perform likelihood ratio or information criteria comparison between $S_{\mathrm{bg}}$ and $S_{\mathrm{bg}}+S_{\mathrm{DP}}$; claims require predefined evidence thresholds.

All KPIs are falsifiable without prior data; thresholds are fixed herein.

## 6. Personnel

Proposer: Justin K. Lietz — responsible for modeling, pre-registration, runplan compliance, data acquisition oversight, and open-artifacts publication following the PAPER_STANDARDS.

## 7. References

- B. Holdom, Two U(1)’s and Epsilon Charge Shifts, Phys. Lett. B 166 (1986) 196–198.
- J. Jaeckel and A. Ringwald, The Low-Energy Frontier of Particle Physics, Ann. Rev. Nucl. Part. Sci. 60 (2010) 405–437.
- M. Fabbrichesi, E. Gabrielli, and G. Lanfranchi, The Physics of the Dark Photon, SpringerBriefs in Physics (2020), arXiv:2005.01515.

