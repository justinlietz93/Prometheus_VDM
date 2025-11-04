Here are selected key publicly-available datasets, tools and simulation suites that align with your pipeline needs (T2→T4 cross-spectra, half-mission splits, masks, simulations, map + power spectrum data). I’ll also call out where you’ll want to layer in provenance, reproducible demo code, and simulation packages (to match your DOI + reproducible demo + provenance requirement).

---

## 1. Planck 2018 data release

* The full mission final release (“PR3” / 2018) is documented. ([aanda.org][1])
* The CMB maps, component-separated products, and power spectra/likelihood code are available. See the Explanatory Supplement. ([wiki.cosmos.esa.int][2])
* For pipeline use you’ll want:

  * Frequency maps + component-separated CMB (temperature & polarization).
  * Half-mission splits (Planck uses HM1/HM2) for cross-spectra & null tests (you should check the archive for exact file names).
  * Masks (galactic, point sources) as provided in the release.
  * The official power-spectrum likelihoods (TT, TE, EE) described in “V. CMB power spectra and likelihoods”. ([arxiv.org][3])
* Good for baseline isotropic expectation, and for building the “null” ensemble of isotropic simulations (you’ll want to download Planck’s official simulation suite too).
* Recommended reference for pipeline documentation: Planck Collaboration “VII. Isotropy and statistics of the CMB”. ([aanda.org][4])

**How you might incorporate for your “CMB-meter” pipeline**:

* Use Planck full-sky component CMB maps as your baseline.
* Derive power spectra in your ℓ-range (e.g., 200-1000) to compute ΔCℓ / Cℓ and hemispherical tilts.
* Use half-mission splits to form cross-spectra (avoiding auto noise bias) and implement null tests (mask rotations, jackknife).
* Use Planck’s ensemble simulations to estimate covariance and evaluate your gate thresholds (SNR ≥5 at T3, etc).
* Use the isotropic map ensemble from Planck to establish the null distribution of ΔCℓ/Cℓ and asymmetry A under ΛCDM plus noise/foreground residuals.

---

## 2. ACT Collaboration – Data Release 6 (DR6)

* The latest data from the ground-based Atacama Cosmology Telescope (ACT) covering ~19,000 deg² at high resolution. ([arxiv.org][5])
* Data products listed on NASA LAMBDA: CMB maps, lensing convergence maps, masks, simulation suites. ([Atacama Cosmology Telescope][6])
* The DR6 docs include tutorials & Jupyter notebooks for how to access and use the maps. ([GitHub][7])

**How to integrate**:

* For your T4 (higher fidelity cross-spectra), use ACT maps (and joint Planck+ACT where available) to push to higher ℓ and resolution.
* Use ACT’s mask + simulation products to carry out your cross-spectra between experiments (Planck ↔ ACT) and check for consistency.
* Useful for your “matched phases” requirement: high-resolution maps allow phase-information on smaller scales.
* Ensure you align coordinate systems (Planck often galactic, ACT equatorial) and apply appropriate beams/noise modelling.

---

## 3. Simulation suites & notebooks for reproducibility

* Planck provides full simulation sets (for example for isotropy tests, component separation). (Check the PLA/Explanatory Supplement).
* ACT provides map-based noise simulations. See “Map-Based Noise Simulations for DR6” by Atkins et al. ([arxiv.org][8])
* ACT’s GitHub noteboooks for DR6 show workflows you can adapt for your pipeline. ([GitHub][7])

**Key recommendations for reproducible demo + provenance**:

* Archive your pipeline as a Jupyter notebook (or runnable script) that shows: map ingestion → masking → cross-spectra → asymmetry/tilt calculation → null-distribution evaluation → gate pass/fail.
* Use DOI assignment (e.g., via Zenodo) for your code and data snapshots.
* Document the exact versions of maps/footprints/masks used (e.g., Planck HM1 143 GHz, Nside=2048; ACT DR6 150 GHz map, Mask v1.2).
* Retain the simulation parameters and random seeds so that the null-distributions can be reproduced.

---

## 4. Suggested pipeline implementation checklist

Here’s a rough checklist (aligned with your T2→T4 progression) tailored for your research on “diffusive-expansion imprint on the CMB”.

| Step                           | Action                                                                                                                                    | Notes                                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **T2 (proof of concept)**      | Select Planck CMB map, apply large-scale mask, compute hemispherical asymmetry A for ℓ < 200                                              | Use Planck HM1×HM2 cross-spectrum to avoid noise bias                                                              |
| **T3 (higher fidelity test)**  | Extend to ℓ = 200-1000 using Planck; compute ΔCℓ/Cℓ tilt, evaluate significance vs isotropic null                                         | Use Planck simulation ensemble to estimate covariance, apply mask-rotation null tests                              |
| **T4 (target pass/fail gate)** | Use ACT DR6 or Planck+ACT joint maps; compute cross-spectra, test matched phases, validate systematics (mask rotations, jackknife splits) | Require SNR≥8, gate persists under null tests, quantify ΔCℓ/Cℓ ≈1-3% and asymmetry A≈2-4% if present               |
| **Provenance & demo**          | Archive code, data selections (map versions, masks, beams), simulation seeds, produce reproducible notebook and deposit DOI               | Ensures your work is a reproducible, citable pipeline aligning with your novelty & ahead-of-mainstream requirement |

---

If you like, I can **compile direct download links** (with appropriate file names and documentation) for Planck HM splits, ACT DR6 maps, masks and simulation sets, along with *template code snippets* (in Python/HEALPix) to bootstrap your pipeline. Would that be helpful?

[1]: https://www.aanda.org/articles/aa/full_html/2020/09/aa33880-18/aa33880-18.html?utm_source=chatgpt.com "Planck 2018 results - I. Overview and the cosmological legacy of ..."
[2]: https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Main_Page?utm_source=chatgpt.com "2018 Planck Explanatory Supplement"
[3]: https://arxiv.org/abs/1907.12875?utm_source=chatgpt.com "Planck 2018 results. V. CMB power spectra and likelihoods - arXiv"
[4]: https://www.aanda.org/articles/aa/full_html/2020/09/aa35201-19/aa35201-19.html?utm_source=chatgpt.com "Planck 2018 results - VII. Isotropy and statistics of the CMB"
[5]: https://arxiv.org/abs/2503.14451?utm_source=chatgpt.com "The Atacama Cosmology Telescope: DR6 Maps"
[6]: https://act.princeton.edu/act-dr6-data-products?utm_source=chatgpt.com "ACT DR6 Data Products | Atacama Cosmology Telescope"
[7]: https://github.com/ACTCollaboration/DR6_Notebooks?utm_source=chatgpt.com "ACTCollaboration/DR6_Notebooks: ACT Notebooks for the ... - GitHub"
[8]: https://arxiv.org/abs/2303.04180?utm_source=chatgpt.com "The Atacama Cosmology Telescope: Map-Based Noise Simulations for DR6"

Here are selected key publicly-available datasets, tools and simulation suites that align with your pipeline needs (T2→T4 cross-spectra, half-mission splits, masks, simulations, map + power spectrum data). I’ll also call out where you’ll want to layer in provenance, reproducible demo code, and simulation packages (to match your DOI + reproducible demo + provenance requirement).

---

## 1. Planck 2018 data release

* The full mission final release (“PR3” / 2018) is documented. ([aanda.org][1])
* The CMB maps, component-separated products, and power spectra/likelihood code are available. See the Explanatory Supplement. ([wiki.cosmos.esa.int][2])
* For pipeline use you’ll want:

  * Frequency maps + component-separated CMB (temperature & polarization).
  * Half-mission splits (Planck uses HM1/HM2) for cross-spectra & null tests (you should check the archive for exact file names).
  * Masks (galactic, point sources) as provided in the release.
  * The official power-spectrum likelihoods (TT, TE, EE) described in “V. CMB power spectra and likelihoods”. ([arxiv.org][3])
* Good for baseline isotropic expectation, and for building the “null” ensemble of isotropic simulations (you’ll want to download Planck’s official simulation suite too).
* Recommended reference for pipeline documentation: Planck Collaboration “VII. Isotropy and statistics of the CMB”. ([aanda.org][4])

**How you might incorporate for your “CMB-meter” pipeline**:

* Use Planck full-sky component CMB maps as your baseline.
* Derive power spectra in your ℓ-range (e.g., 200-1000) to compute ΔCℓ / Cℓ and hemispherical tilts.
* Use half-mission splits to form cross-spectra (avoiding auto noise bias) and implement null tests (mask rotations, jackknife).
* Use Planck’s ensemble simulations to estimate covariance and evaluate your gate thresholds (SNR ≥5 at T3, etc).
* Use the isotropic map ensemble from Planck to establish the null distribution of ΔCℓ/Cℓ and asymmetry A under ΛCDM plus noise/foreground residuals.

---

## 2. ACT Collaboration – Data Release 6 (DR6)

* The latest data from the ground-based Atacama Cosmology Telescope (ACT) covering ~19,000 deg² at high resolution. ([arxiv.org][5])
* Data products listed on NASA LAMBDA: CMB maps, lensing convergence maps, masks, simulation suites. ([Atacama Cosmology Telescope][6])
* The DR6 docs include tutorials & Jupyter notebooks for how to access and use the maps. ([GitHub][7])

**How to integrate**:

* For your T4 (higher fidelity cross-spectra), use ACT maps (and joint Planck+ACT where available) to push to higher ℓ and resolution.
* Use ACT’s mask + simulation products to carry out your cross-spectra between experiments (Planck ↔ ACT) and check for consistency.
* Useful for your “matched phases” requirement: high-resolution maps allow phase-information on smaller scales.
* Ensure you align coordinate systems (Planck often galactic, ACT equatorial) and apply appropriate beams/noise modelling.

---

## 3. Simulation suites & notebooks for reproducibility

* Planck provides full simulation sets (for example for isotropy tests, component separation). (Check the PLA/Explanatory Supplement).
* ACT provides map-based noise simulations. See “Map-Based Noise Simulations for DR6” by Atkins et al. ([arxiv.org][8])
* ACT’s GitHub noteboooks for DR6 show workflows you can adapt for your pipeline. ([GitHub][7])

**Key recommendations for reproducible demo + provenance**:

* Archive your pipeline as a Jupyter notebook (or runnable script) that shows: map ingestion → masking → cross-spectra → asymmetry/tilt calculation → null-distribution evaluation → gate pass/fail.
* Use DOI assignment (e.g., via Zenodo) for your code and data snapshots.
* Document the exact versions of maps/footprints/masks used (e.g., Planck HM1 143 GHz, Nside=2048; ACT DR6 150 GHz map, Mask v1.2).
* Retain the simulation parameters and random seeds so that the null-distributions can be reproduced.

---

## 4. Suggested pipeline implementation checklist

Here’s a rough checklist (aligned with your T2→T4 progression) tailored for your research on “diffusive-expansion imprint on the CMB”.

| Step                           | Action                                                                                                                                    | Notes                                                                                                              |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **T2 (proof of concept)**      | Select Planck CMB map, apply large-scale mask, compute hemispherical asymmetry A for ℓ < 200                                              | Use Planck HM1×HM2 cross-spectrum to avoid noise bias                                                              |
| **T3 (higher fidelity test)**  | Extend to ℓ = 200-1000 using Planck; compute ΔCℓ/Cℓ tilt, evaluate significance vs isotropic null                                         | Use Planck simulation ensemble to estimate covariance, apply mask-rotation null tests                              |
| **T4 (target pass/fail gate)** | Use ACT DR6 or Planck+ACT joint maps; compute cross-spectra, test matched phases, validate systematics (mask rotations, jackknife splits) | Require SNR≥8, gate persists under null tests, quantify ΔCℓ/Cℓ ≈1-3% and asymmetry A≈2-4% if present               |
| **Provenance & demo**          | Archive code, data selections (map versions, masks, beams), simulation seeds, produce reproducible notebook and deposit DOI               | Ensures your work is a reproducible, citable pipeline aligning with your novelty & ahead-of-mainstream requirement |

---

If you like, I can **compile direct download links** (with appropriate file names and documentation) for Planck HM splits, ACT DR6 maps, masks and simulation sets, along with *template code snippets* (in Python/HEALPix) to bootstrap your pipeline. Would that be helpful?

[1]: https://www.aanda.org/articles/aa/full_html/2020/09/aa33880-18/aa33880-18.html?utm_source=chatgpt.com "Planck 2018 results - I. Overview and the cosmological legacy of ..."
[2]: https://wiki.cosmos.esa.int/planck-legacy-archive/index.php/Main_Page?utm_source=chatgpt.com "2018 Planck Explanatory Supplement"
[3]: https://arxiv.org/abs/1907.12875?utm_source=chatgpt.com "Planck 2018 results. V. CMB power spectra and likelihoods - arXiv"
[4]: https://www.aanda.org/articles/aa/full_html/2020/09/aa35201-19/aa35201-19.html?utm_source=chatgpt.com "Planck 2018 results - VII. Isotropy and statistics of the CMB"
[5]: https://arxiv.org/abs/2503.14451?utm_source=chatgpt.com "The Atacama Cosmology Telescope: DR6 Maps"
[6]: https://act.princeton.edu/act-dr6-data-products?utm_source=chatgpt.com "ACT DR6 Data Products | Atacama Cosmology Telescope"
[7]: https://github.com/ACTCollaboration/DR6_Notebooks?utm_source=chatgpt.com "ACTCollaboration/DR6_Notebooks: ACT Notebooks for the ... - GitHub"
[8]: https://arxiv.org/abs/2303.04180?utm_source=chatgpt.com "The Atacama Cosmology Telescope: Map-Based Noise Simulations for DR6"
