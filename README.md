<h1 align="center">Void Dynamics Model (VDM)</h1>
<h4 align="center">A background‑independent, unified metriplectic field theory with an emergent causal cone and an epistemological J→M projection.</h4>
<h6 align="center">AMN-->FUM-->VDM</h6>

---

***Current Status:*** Active development.

> **Author:** Justin K. Lietz  
> **Contact:** <justin@neuroca.ai>  
> <a href="https://orcid.org/0009-0008-9028-1366"><img src="https://img.shields.io/badge/ORCID-0009--0008--9028--1366-blue?" alt="ORCID: 0009-0008-9028-1366"></a>  
> **Zenodo Community:** [Void Dynamics Model](https://zenodo.org/communities/void-dynamics-model/records?q=&l=list&p=1&s=10&sort=newest)
>
> **Created:** August 9, 2025  
> **Last Updated:** November 8, 2025  
>
> This research is protected under a dual-license to foster open academic  
> research while ensuring commercial applications are aligned with the project's ethical principles.  
> Commercial use requires written permission from the author.  
>
> ![Static Badge](https://img.shields.io/badge/Academic%2FCommercial%20Dual-License?label=LICENSE&color=%23fff200&link=https%3A%2F%2Fgithub.com%2FNeuroca-Inc%2FPrometheus_Void-Dynamics_Model%2Fblob%2Fmain%2FLICENSE.md)  
>
> See LICENSE file or click the LICENSE badge above for full terms.  

## 🔥News

- **November 6, 2025**
  - 7 complete [formalisms](/Derivation/Complete-Formalisms) have been derived for VDM and documented as some of the final remaining pieces in the work to T8 Axiom 8 candidate.
- **November 4, 2025**
  - [Assisted‑Echo T4 (prereg v1c)](/Derivation/Metriplectic/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md) rerun with instrument + plotting fixes:
    - Per‑seed plotting for A2/A5/B11 removes cross‑seed “seed‑chord” artifacts in overlays (error, ΔΣ, λ‑telemetry).
    - Noether (G1) tolerance scaled to instrument level: tol = max(1e-12, 10·eps·√N·max(h0,1)); routing remains governed by G1–G4 aggregation.
    - Reruns launched for N∈{512,1024}, dt∈{0.01,0.02,0.04}. Early results: N=512 dt=0.01 and N=512 walker dt=0.02 routed to main outputs with G1–G4 **PASS**; dt=0.04 routed to failed_runs pending CFL tightening.
    - Artifacts (PNG/CSV/JSON + figure packs) under Derivation/code/outputs/{figures,logs}/metriplectic, tag: assisted-echo-t4-prereg-v1c.
  - **Next:** upgrade G4 measurement to a multi‑point Δt fit (same thresholds) to harden RP‑1 decisions.
- **November 1, 2025**
  - Published early draft of the proposed A8 Axiom candidate to [Zenodo](https://zenodo.org/records/17503344) for provenance.
- **October 31, 2025**
  - Added a T8 grade proposal for a new Axiom candidate as [A8 - Lietz Infinity Conjecture](/Derivation/T8_A8_PROPOSAL_Lietz_Infinity_Conjecture_v1.md) which provides an elegant explanation for hierarchy and structure.
- **October 30, 2025**  
  - Added a [historical/](/docs/historical) folder including early original work like:
    - A self healing knowledge graph using [Topological Data Analysis](/docs/historical/Emergent_TDA/20250402_TDA_KG_Metrics_ProtocolOutput.md)
    - As well as a [Self Improvement Engine](/docs/historical/SIE/20250402_SIE_Stability_Analysis_ProtocolOutput.md) that integrates multiple reward components like novelty, self benefit, habituation, and TD error into a single "total reward" signal used to modulate its own neural plasticity for stable self-improvement that avoids weight saturation.
  - Validated the Counterfactual Echo Gain [hypothesis](/Derivation/Metriplectic/T4_PROPOSAL_CEG_Metriplectic_Assisted-Echo_Experiment.md) by proving the trustworthiness and accuracy of the instrument, and showing that echo assist does modulate and improve the performance of a self aware system with 0 difference in cost compared to baseline.
- **October 28, 2025**  
  - Published an [article](https://medium.com/p/2b4f5c7d23c9/edit) on Medium about upcoming work.
    - Published a ["The Physics of Choice"](https://youtu.be/tR3G9Z2ScAc?si=ZFdQVBaqBck06YSW) video, along with a couple other videos on YouTube.
- **October 23, 2025:**  
  - Created a sparsely populated [CANON_PROGRESS.md](/CANON_PROGRESS.md) document to post updates on private work to prevent this public repo from going stale.
- **September 29, 2025:**  
  - First public code release + creation of private Void Dynamics package which can now be imported and run in this repository using workflows and repository secrets.
- **September 28, 2025:**  
  - Posted two pre-prints to [Zenodo](https://doi.org/10.5281/zenodo.17220869). If you've published similar or relevant work on Reaction-Diffusion in the past 3 years on arXiv and want to support this work by endorsing me in a related category, submit an issue, post in the discussion board, or send me an email with `Subject: RD Endorsement` to get my attention. It would be much appreciated!
- **August 21, 2025:** Launched public repo
- ...
- **March, 2025**  
  - Released first falsifiable, reproducible simulations that validated initial claims.
- **February, 2025**  
  - SIE and Emergent KG + Real-Time TDA show very strong statistically significant findings, making feasible the entire model
- **October, 2024**  
  - Initial realization of the idea.

## 🎯Planned

- Request endorsements to publish to a related category on ArXiv for latest validations.
- Post recent validations as pre-print to Zenodo.
- Publish a working demo of the VDM AI with a real-time self-organizing spiking neural network and self-healing emergent knowledge graph that performs topological data analysis on it's own graph during runtime.
- Continue working toward other areas of Physics, like agency and determine how much the metriplectic findings affect other areas of physics
- Once published to arXiv, take steps towards a peer reviewed journal and gather criticisms to refine my work.

## DOIs

***T4. Counterfactual Echo Gain (CEG): A Metriplectic Assisted-Echo Experiment Proposal in VDM***
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17525915.svg)](https://doi.org/10.5281/zenodo.17525915)

***T8. Axiom 8 Candidate: The Lietz Infinity Resolution Conjecture***  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17503343.svg)](https://doi.org/10.5281/zenodo.17503343)

***A Logarithmic First Integral for the Logistic On Site Law in Void Dynamics***  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17220869.svg)](https://doi.org/10.5281/zenodo.17220869)

<div style="text-align: center;">
<img width="800" height="800" alt="logo" src="https://github.com/user-attachments/assets/b22adc5d-f126-4865-9e47-71af5fa4f7f7" />
</div>

---

## ❗NOTE

> **This organization is currently managed and operated by me (J. Lietz) alone as a solo developer / researcher. I may not respond by email right away. If you want to get my attention post in the discussion board briefly about what you'd like to talk about and let me know you sent me an email.**

### 💬**Discussion Board:**

- <https://github.com/orgs/Neuroca-Inc/discussions>

---

This repository includes provides a public view of the Void Dynamics Model.
It includes the theory, write-ups, code, notebooks, figures, logs, and validations for review by physicists,
applied mathematicians, learners, students, and scientifically minded engineers.  
Reproducible code released for the public is now available.
Remaining proprietary work must be requested directly.

> **Classified notice**
>
> I reserve the right to certain executable simulations and modules.
>
> Contact the maintainer for access or questions.

## 🧭What this is

- A set of derivation papers that establish a clean baseline physics slice starting from a discrete lattice, to a metriplectic split and cosmology.
- Additional documents that explore future work (proposals).
- Each paper separates what is proven from what is plausible or speculative
  and, where applicable, includes acceptance criteria for simple numerical
  checks.

## 🤖Why it relates to AI (brief)

- The project studies how simple, but opposite metriplectic type rules yield stable, interpretable
  global behavior under resource constraints.
- That design philosophy is relevant to AI systems that favor locality,
  event-driven updates, and transparent evaluation instead of opaque
  heuristics.
- “Memory steering” (covered separately) frames slow routing bias and
  retention/decay as structured influences over faster dynamics, an analogy
  for directing computation without black-box shortcuts.

## ⚖️Licensing and scope

- These materials are shared for academic review and discussion. Commercial
  use requires prior written permission. See the project’s license notice in
  the distribution or parent repository materials.
- I reserve all legal rights to ownership of any custom or proprietary assets.
- The scope stays within theoretical physics and simulation. Broad
  cosmological claims are withheld or clearly labeled until backed by
  derivation + numeric checks.

## 🔖Citations

- When referencing specific results, cite the overview and the relevant
  validation paper, for example:
  - [VDM_Overview.md](VDM_Overview.md)
  - [rd_front_speed_validation.md](write_ups/reaction_diffusion/rd_front_speed_validation.md)
  - [rd_dispersion_validation.md](write_ups/reaction_diffusion/rd_dispersion_validation.md)

## 📫Contact

- For scope questions or clarifications about acceptance criteria, refer to the
  headers in the overview and topic files listed above. If you are reading this
  as part of a paper-only bundle, the maintainer’s contact is provided alongside
  the distribution materials.
