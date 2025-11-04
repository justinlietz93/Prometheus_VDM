Here’s a tight, end‑to‑end plan to stand up the **T2 CMB‑meter** with two observables on **Planck PR4** maps, plus concrete pass/fail gates and next steps.

---

# What we’re testing (in plain terms)

* **Hemispherical power asymmetry robustness**: does the “north–south” power difference persist if we randomly rotate the sky? (the **R‑metric**). Prior PR4 analyses still see hints of asymmetry, but with method/mask sensitivity—we’ll quantify robustness directly via rotations. ([arXiv][1])
* **Off‑diagonal covariance (C_{\ell,\ell+1})**: inhomogeneous/anisotropic inflation models can create (\Delta\ell=1) couplings; we’ll measure adjacent‑multipole covariance on PR4 component‑separated maps. (Related SI tests and anomaly surveys on PR4 motivate this direction.) ([aanda.org][2])

---

# Data + priors

* **Maps/masks**: Planck **PR4 FULLSKY** component‑separated maps (SMICA, Commander), with masks and noise info from the CMB‑S4 PR4 portal. ([data.cmb-s4.org][3])
* **Lensing products**: include PR4/NPIPE lensing where needed for null/consistency checks. (PR4 improves internal consistency vs PR3.) ([data.cmb-s4.org][4])
* **Large‑scale prior**: lock (\tau) to the **PR4 reionization** constraint when evaluating low‑(\ell) modes (use the April 17, 2025 analysis; v2 Sept 2025). Report main results and (\tau)-prior‑free sensitivity. ([arXiv][5])

---

# Implementation stack

* **SHTs**: fast transforms via **libsharp** (C99; MPI capable). ([arXiv][6])
* **Analysis**: **healpy** for map↔alm, spectra, rotations, masking (e.g., `map2alm`, `anafast`, `alm2map`). ([healpy.readthedocs.io][7])

---

# Observable A — Rotation‑robustness (R) for hemispherical asymmetry

1. Define baseline amplitude (A_0): pick your hemisphere axis (\hat n_0) (e.g., literature axis or ML‑fit dipole‑modulation) and compute (A(\hat n_0)) from local‑variance dipole or power‑split (C_\ell) estimator on the masked map. ([arXiv][1])
2. Randomly rotate the **full‑sky** map (N) times (e.g., (N!=!2000)), re‑compute (A_i) at the **rotated** (\hat n_0).
3. Define (R = \Pr\big(,|A_i-A_0|\le \epsilon A_0,\big)) with (\epsilon!\approx!0.1) (report curve vs (\epsilon)).
4. **Pass** if (R) is (\ge 3\sigma) above null (null from isotropic MCs matched to PR4 noise/mask); **fail** if (R) collapses under rotations or flips sign across component‑separation methods. ([arXiv][1])

---

# Observable B — Off‑diagonal covariance (C_{\ell,\ell+1})

1. Compute alms up to ( \ell_{\max}\sim 600) (temp) with consistent mask apodization; build covariance (\langle a_{\ell m} a^*_{\ell' m'}\rangle).
2. Extract adjacent‑band power (K_{\ell}^{(\Delta\ell=1)}=\sum_m a_{\ell m} a^*_{\ell+1,m}) (and EB/TE variants if desired).
3. Calibrate significance with PR4‑like MC simulations (noise, beams, mask; preserve SI).
4. **Pass** if a **significant** (\Delta\ell=1) excess survives multiple‑testing control (q‑value) and cross‑method consistency (SMICA/Commander); **fail** if it vanishes with stricter masks or (\tau) prior enforcement. (SI studies on PR4 guide masks/systematics checks.) ([aanda.org][2])

---

# Controls & systematics

* **Component‑method cross‑check**: SMICA vs Commander (plus SEVEM/NILC when feasible). ([arXiv][8])
* **Mask ladder**: vary Galactic/point‑source masks to test stability (prior PR4 asymmetry results change with mask—track that explicitly). ([arXiv][1])
* **Lensing & birefringence sanity**: test whether adding lensing or EB systematics moves signals (PR4 birefringence work shows EB sensitivity). ([Physical Review Links][9])
* **Low‑(\ell) priorization**: re‑run low‑(\ell) summaries with (\tau) fixed to PR4 reionization constraints; report delta. ([arXiv][5])

---

# Minimal runbook (healpy/libsharp)

* Load PR4 map + mask → deconvolve beam/pixwin as needed → `map2alm` (per method). ([healpy.readthedocs.io][7])
* **R‑metric**: generate SO(3) rotations → rotate map (or alms) → recompute (A_i) → compare to MC null. ([healpy.readthedocs.io][7])
* **(C_{\ell,\ell+1})**: construct alm covariance bands; estimate significance vs MCs generated with `synalm/synfast` matched to PR4 (C_\ell)+noise. ([healpy.readthedocs.io][10])

---

# Pass/Fail gates (pre‑registered)

* **PASS**:

  * (R) at **≥3σ** above null **and** significant (\Delta\ell=1) couplings after multiple‑testing control, **and** both stable across component methods/masks and with (\tau) prior locked.
* **FAIL**: either metric collapses under rotations, masks, cross‑methods, or with the PR4 (\tau) prior.

---

# What you’ll need (links)

* **Planck PR4 FULLSKY** maps/masks (SMICA/Commander) and manifest/checksums. ([data.cmb-s4.org][3])
* **PR4 overview (NPIPE)** for data characteristics/systematics notes. ([data.cmb-s4.org][4])
* **Reionization ((\tau)) prior** from PR4 analysis (Apr 17, 2025; v2). ([arXiv][5])
* **libsharp** paper and reference entry. ([arXiv][11])
* **healpy** docs for `map2alm/anafast/alm2map/rotator`. ([healpy.readthedocs.io][7])
* **Context papers on SI/asymmetry with PR4**. ([aanda.org][2])

---

# Quick next steps (actionable)

1. **Fetch data** from PR4 FULLSKY portal; record manifest hashes in your PROVENANCE block. ([data.cmb-s4.org][3])
2. **Scaffold** `T2_CMB_meter/` with two modules: `r_metric.py` and `offdiag_clp1.py`; wire libsharp via healpy.
3. **MC bank**: 1–2k isotropic sims (PR4 beam+noise+mask) for both observables. ([healpy.readthedocs.io][12])
4. **Pre‑register** pass/fail and the (\tau)‑locked re‑run in the PROPOSAL; ship the spec before writing artifacts.
5. **Run** SMICA→Commander→(optional SEVEM/NILC) ladder; publish a small stability matrix table.

If you want, I can drop a ready‑to‑run file tree (with stubbed functions and CLI flags) and a 1‑page PROPOSAL insert that matches your template.

[1]: https://arxiv.org/abs/2306.14880?utm_source=chatgpt.com "Hemispherical Power Asymmetry in intensity and polarization for Planck PR4 data"
[2]: https://www.aanda.org/articles/aa/full_html/2024/03/aa48160-23/aa48160-23.html?utm_source=chatgpt.com "Probing the statistical isotropy of the universe with Planck ..."
[3]: https://data.cmb-s4.org/planck_pr4-fullsky.html?utm_source=chatgpt.com "Planck PR4 FULLSKY"
[4]: https://data.cmb-s4.org/planck_pr4.html?utm_source=chatgpt.com "Planck PR4"
[5]: https://arxiv.org/abs/2504.13254?utm_source=chatgpt.com "Reconstructing the epoch of reionisation with Planck PR4"
[6]: https://arxiv.org/abs/1303.4945?utm_source=chatgpt.com "Libsharp - spherical harmonic transforms revisited"
[7]: https://healpy.readthedocs.io/en/1.18.1/healpy_spht.html?utm_source=chatgpt.com "sphtfunc – Spherical harmonic transforms — healpy 1.18.1 ..."
[8]: https://arxiv.org/html/2411.15307v1?utm_source=chatgpt.com "A 5.7⁢𝜎 detection confirming the existence of a possibly ..."
[9]: https://link.aps.org/doi/10.1103/PhysRevLett.128.091302?utm_source=chatgpt.com "Cosmic Birefringence from the Planck Data Release 4"
[10]: https://healpy.readthedocs.io/en/latest/generated/healpy.sphtfunc.synalm.html?utm_source=chatgpt.com "healpy.sphtfunc.synalm - Read the Docs"
[11]: https://arxiv.org/pdf/1303.4945?utm_source=chatgpt.com "Libsharp – spherical harmonic transforms revisited"
[12]: https://healpy.readthedocs.io/en/1.6.3/generated/healpy.sphtfunc.synfast.html?utm_source=chatgpt.com "healpy.sphtfunc.synfast - Read the Docs"

