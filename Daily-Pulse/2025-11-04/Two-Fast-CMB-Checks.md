Here are two tightly scoped, ready-to-run cosmology tasks you can drop into your pipeline—one on CMB hemispherical asymmetry using Planck PR4 maps, and one to replicate the CatWISE quasar dipole with the newest methodology update.

---

# 1) PR4 R‑metric sanity run (CMB hemispherical asymmetry & rotation‑robustness)

**Goal (one line):** Compute a hemispherical‑asymmetry amplitude (A(\hat n)) on PR4 full‑sky component‑separated maps and measure its **rotation‑robustness** (R) by random 3D rotations of the map.

**Why PR4 now:** The CMB‑S4 Data Portal publicly hosts **Planck PR4 (NPIPE)** full‑sky/low‑res/half‑ring maps with Globus manifests, checksums, and effective beams—easy to fetch reproducibly. ([data.cmb-s4.org][1])

**Reference context:** PR4/NPIPE underpins recent parameter and anomaly studies and remains consistent with PR3 while lowering noise. See PR4 cosmology summaries and PR4-based asymmetry/birefringence analyses. ([aanda.org][2])

## Minimal run plan

* **Data**: Download PR4 **full‑sky** component‑separated temperature map(s) (e.g., SMICA/Commander) and corresponding masks; keep half‑ring splits for noise sanity. (CMB‑S4 portal → Globus collections.) ([data.cmb-s4.org][3])
* **I/O + transforms**: `healpy` for FITS + (a_{\ell m}) I/O; `libsharp` (via `healpy`/`ducc0`) for fast SHTs.
* **Metric definition**:

  * Choose amplitude (A(\hat n)): e.g., dipole‑modulation fit or local‑variance dipole (LVE) on large scales ((\ell\lesssim 64)); both used in the literature. ([arXiv][4])
  * Fix the originally reported axis (\hat n_0) (e.g., maximize (A) on the native map).
  * Draw (N) random SO(3) rotations (R_i); recompute (A_i=A(R_i\hat n_0)).
  * **R‑metric** (rotation‑robustness): (R=\frac{1}{N}\sum_i \mathbf{1}(|A_i-A_0|\le 0.1A_0)). (Threshold 10% is a tunable knob.)
* **Validation gates**:

  * **Noise split check**: repeat on half‑ring differences (should kill the signal). ([data.cmb-s4.org][5])
  * **Mask/beam sensitivity**: vary apodized masks; check QuickPol beam windows if you go to (C_\ell) space. ([data.cmb-s4.org][6])
  * **Axis stability**: report (\hat n_0) scatter under rotations and under small (\ell_{\max}) changes. For prior context on HPA definitions/results: ([arXiv][7])

**Provenance anchors to cite in your PROPOSAL/RESULTS**: CMB‑S4 PR4 portal pages (dataset, manifest, checksums), and PR4 cosmology/birefringence/HPA papers for methodological grounding. ([data.cmb-s4.org][1])

---

# 2) CatWISE quasar dipole replication (bias‑aware, Oct 27, 2025 update)

**Goal (one line):** Reproduce the **quasar number‑count dipole** from CatWISE2020 with explicit higher‑(\ell) control, masks, and color‑selection checks per the **Oct 27, 2025** methodology, which *reaffirms an anomalously high dipole*. ([arXiv][8])

**Why now:** The newest analysis (von Hausegger et al., 2025‑10‑27) carefully tests large‑scale multipoles and local clustering, finding no excess octupole and reaffirming the high dipole; closely related reassessments highlight mask‑induced mode coupling and simulation‑based error budgets to get unbiased dipole amplitudes. ([arXiv][8])

## Minimal run plan

* **Catalog**: CatWISE2020 quasars (1.6M mid‑IR). Apply their recommended **ecliptic‑latitude** trend correction and vetted sky mask. ([arXiv][8])
* **Estimator**:

  * Build a harmonic‑space or real‑space dipole fit **with simultaneous control of (\ell>1)** to avoid leakage (as emphasized in 2025 paper). ([arXiv][8])
  * Quantify and subtract **mode coupling** from the mask using simulations; propagate shot noise + clustering variance. (See the 2025 reassessment for mocks approach.) ([arXiv][9])
* **Systematics**:

  * **Color‑bin test** to flag Galactic contamination (notably strong in certain WISE color bins). ([arXiv][10])
  * **Local‑structure control**: excise low‑(z) cuts / apply weighting to reduce nearby large‑scale structure bias (per the 2025 guidance). ([arXiv][8])
* **Report**: Dipole amplitude (|\mathbf{D}|), direction ((\ell,b)), covariance from mocks; compare to kinematic expectation from the CMB dipole and summarize anomaly significance with all systematics included. Background on the anomaly and prior CatWISE measurements: ([arXiv][11])

---

## Quick “starter kit” (files to add)

* `Derivation/Cosmology/T2_CMB_Asymmetry_PR4/PROPOSAL_PR4_R_metric.md` (cite PR4 portal pages and PR4 anomaly papers). ([data.cmb-s4.org][1])
* `code/cosmology/cmb/rmetric/` with:

  * `rmetric_run.py` (healpy map load, mask, random rotations, compute (A), compute (R))
  * `config/example.pr4.smica.yaml` (dataset URIs from portal; mask paths; (N), (\ell_{\max}))
* `Derivation/Cosmology/T2_LSS_Dipole_CatWISE/PROPOSAL_CatWISE_Dipole.md` (cite the 2025‑10‑27 arXiv and the 2025‑11 reassessment). ([arXiv][8])

---

## Small notes for your stack

* Use AMD‑friendly Python stack (no CUDA). `healpy`/`ducc0` are CPU‑optimized; libsharp bindings come via `healpy`.
* Gate this as **T2 instrument** feeding T4/T8 analyses (baseline axis stability for Gate **G‑CMB‑HPA** as you proposed).

If you want, I can draft both PROPOSAL markdowns (with exact portal links, manifests, and run‑commands) and a minimal `rmetric_run.py` scaffold next.

[1]: https://data.cmb-s4.org/planck_pr4.html?utm_source=chatgpt.com "Planck PR4"
[2]: https://www.aanda.org/articles/aa/pdf/2024/02/aa48015-23.pdf?utm_source=chatgpt.com "Cosmological parameters derived from the final Planck ..."
[3]: https://data.cmb-s4.org/planck_pr4-fullsky.html?utm_source=chatgpt.com "Planck PR4 FULLSKY"
[4]: https://arxiv.org/html/2411.15786v1?utm_source=chatgpt.com "A Reassessment of Hemispherical Power Asymmetry in ..."
[5]: https://data.cmb-s4.org/planck_pr4-half_ring.html?utm_source=chatgpt.com "Planck PR4 HALF_RING"
[6]: https://data.cmb-s4.org/planck_pr4-quickpol.html?utm_source=chatgpt.com "Planck PR4 QUICKPOL"
[7]: https://arxiv.org/abs/2306.14880?utm_source=chatgpt.com "Hemispherical Power Asymmetry in intensity and polarization for Planck PR4 data"
[8]: https://www.arxiv.org/abs/2510.23769?utm_source=chatgpt.com "[2510.23769] Clustering properties of the CatWISE2020 ..."
[9]: https://arxiv.org/html/2511.00822v1?utm_source=chatgpt.com "A Reassessment of the Cosmic Dipole Anomaly"
[10]: https://arxiv.org/html/2405.16853v1?utm_source=chatgpt.com "Color Dependence of Dipole in CatWISE2020 Data"
[11]: https://arxiv.org/html/2405.09762v2?utm_source=chatgpt.com "Reassessment of the dipole in the distribution of quasars ..."

