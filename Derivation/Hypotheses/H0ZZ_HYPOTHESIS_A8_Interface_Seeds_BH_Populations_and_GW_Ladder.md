# HYPOTHESIS — A8 Interface Seeds BH Populations and GW Ladder

---

## H0ZZ — BH Population & GW Ladder from A8 (future-work scaffold)

**Classification:** Cosmo/BH-future  
**Owner:** Justin K. Lietz  
**Status:** ACTIVE  
>*This hypothesis is a future-work scaffold. It sets targets and meters but makes no canonical claim until all upstream CF/T instruments and global gates pass and dedicated RESULTS files are published.*

**Stress-test note:** This is a stress-test branch of A8; it is explicitly allowed to die without harming the rest of the program.

**One-line objective:** Translate the A8 interface hierarchy plus EBN-CMB backgrounds into a predictive BH seed and merger population, testable against BH demographics and GW catalogs via existing and future meters.

### Formal statement

Assume:
1. **A8 Two-Gate** (T3) has passed: logarithmic depth scaling and boundary-law excess energy verified with artifacts.
2. **T2 EBN-CMB pipeline** can produce viable FRW/CMB backgrounds from A8 parameters (power spectra, acoustic peaks passing CMB gates).

**Hypothesize** that:

1. **Seed distribution:** The A8 interface hierarchy ([CF3](../Complete-Formalisms/CF3_A8_Scaling_Hierarchical_Interfaces.md)) yields a distribution of "compact seeds" (proto-BH configurations) characterized by a parametric mass function $n(M, z)$ where $M$ is seed mass and $z$ is redshift.

2. **Forward evolution:** Evolving these seeds forward under a generic merger + accretion model (Eddington-limited accretion, dynamical friction, merger trees) produces:
   - BH mass distributions consistent with observed stellar-mass BHs (LIGO/Virgo/KAGRA, $M \sim 5$-$100 \, M_\odot$) and supermassive BHs (quasars, AGN, $M \sim 10^6$-$10^{10} \, M_\odot$).
   - BH spin distributions consistent with observational constraints (e.g., Kerr parameter $a/M \sim 0.7$ median for stellar BHs).

3. **GW event rates:** The merger population produces GW event rates and ringdown spectra that pass existing ringdown meters and are compatible with LIGO/Virgo/KAGRA catalogs (GWTC-1, GWTC-2, GWTC-3) under standard selection effects.

4. **CMB/LSS consistency:** The BH population implied by the seed model is consistent with CMB/LSS fits from T2 EBN-CMB: no catastrophic early energy injection that violates prereg gates on power spectra or acoustic peak positions.

### Predictions (decisive metrics)

These are **targets** the theory must meet, not assumed facts:

- **P1 (Mass function envelope):** VDM's BH mass function $n(M, z)$ stays within pre-registered envelopes for observed distributions:
  - **Stellar-mass:** $n(M, z=0)$ for $M \in [5, 100] \, M_\odot$ overlaps with LIGO/Virgo/KAGRA inferred distributions (e.g., $\chi^2 / \mathrm{dof} \leq 2$ under standard binning).
  - **SMBH:** $n(M, z)$ for $M > 10^6 \, M_\odot$ reproduces quasar luminosity functions and AGN demographics within $\Delta \log(n) \leq 0.5$ dex.

- **P2 (Merger/GW ladder):** There exists at least one parameter region where synthetic GW catalog statistics are not worse than $\Lambda$CDM + standard stellar channels under a common likelihood:
  - **Event rate:** $R_{\mathrm{VDM}}(z)$ within factor of 2 of observed LIGO/Virgo/KAGRA rate. These are target tolerances for a viable parameter region, not assumed matches.
  - **Mass distribution:** Chirp mass distribution $p(\mathcal{M}_c)$ has KS-test $p$-value $\geq 0.05$ against observed samples.
  - **Spin alignment:** Effective spin parameter $\chi_{\mathrm{eff}}$ distribution consistent with observed (median $|\Delta \chi_{\mathrm{eff}}| \leq 0.2$).

- **P3 (CMB/LSS non-disruption):** The BH seed population implied by A8 does not disrupt CMB/LSS fits from T2 EBN-CMB:
  - Power spectrum residuals $\Delta C_\ell / C_\ell \leq 0.05$ for $\ell \in [30, 2000]$.
  - Acoustic peak positions within $\delta \ell / \ell \leq 0.01$ of T2 EBN-CMB baseline.
  - No early energy injection violating $\rho_{\mathrm{BH}}(z > 10) / \rho_{\mathrm{crit}} \leq 10^{-6}$.

- **P4 (Ringdown QNM compatibility, placeholder):** Ringdown spectra from BH mergers pass existing ringdown meters (if available): $|\omega_{\mathrm{VDM}} / \omega_{\mathrm{GR}} - 1| \leq 0.1$ for dominant $\ell=2$ QNM modes.

**Note:** All numeric thresholds in P1–P2 are provisional and will be re-registered in the BH/GW regression proposal once catalogs and meters are fixed. Actual numerical thresholds for P1-P2 will be specified in future T5/T6 BH regression proposal documents. P4 is a placeholder pending ringdown instrument specifications.

### Rationale (bounded)

The A8 interface hierarchy provides a natural mechanism for generating compact seeds without requiring primordial density fluctuations or stellar collapse:

1. **Topological defects as seeds:** Interfaces in the A8 hierarchy (domain walls, cosmic strings, monopoles) carry excess energy $\Delta E \sim \sigma L^{d-1}$ where $\sigma$ is surface tension and $L$ is defect size. For sufficiently high $\sigma$ and large $L$, these defects collapse gravitationally into compact objects (proto-BHs).

2. **Hierarchical mass spectrum:** The A8 logarithmic depth scaling ([CF3](../Complete-Formalisms/CF3_A8_Scaling_Hierarchical_Interfaces.md)) naturally produces a hierarchical mass function: interfaces at level $k$ have mass $M_k \sim M_0 \lambda^k$ where $\lambda < 1$ is the scaling factor. This yields a power-law-like mass function $n(M) \propto M^{-\alpha}$ with $\alpha$ set by A8 parameters.

3. **Early formation:** A8 interfaces form at phase transitions (e.g., tachyon condensation, symmetry breaking) in the early universe, allowing BH seeds to form at $z \gg 1$ without fine-tuning initial conditions.

4. **Merger and accretion:** Standard astrophysical processes (dynamical friction, gas accretion, mergers) grow seeds from $M_{\mathrm{seed}} \sim 10^2$-$10^4 \, M_\odot$ to observed masses.

**Key assumptions:**
- A8 interfaces are gravitationally stable and localize energy (not dispersed by cosmic expansion).
- Merger and accretion rates follow standard astrophysical models (no exotic physics required).
- GW emission from BH mergers is GR-like at leading order (potential small corrections from VDM strong-field effects, see [H0YY](../Gravity/H0YY_HYPOTHESIS_VDM_Horizon_Structure_and_Strong_Field_Gravity.md)).

### Preconditions & scope

**This hypothesis is a future-work scaffold.** It makes **no canonical claim** until:

1. **T3 A8 Two-Gate** passes with artifacts: logarithmic depth and boundary-law excess energy verified.
2. **T2 EBN-CMB pipeline** passes: CMB power spectra and acoustic peaks match observations within prereg gates.
3. **T2 Metriplectic Instruments** pass all global gates (G-J/M, G-Echo, G-H-theorem, G-Locality, G-Artifacts) from [00_HYPOTHESES.md](../z.CANONICAL_Hypotheses/00_HYPOTHESES.md).
4. **T5_BH_GW_Regression** (future BH demographics regression pack) is executed and passes minimal thresholds.

**Domain:**

- Redshift range: $z \in [0, 20]$ (reionization to present).
- Mass range: $M \in [5, 10^{10}] \, M_\odot$ (stellar-mass to SMBH).
- GW frequency: $f \in [10, 10^3]$ Hz (LIGO/Virgo/KAGRA band).

**Scope:**

- **Stellar-mass BHs:** $M \sim 5$-$100 \, M_\odot$ (LIGO/Virgo/KAGRA detections).
- **Intermediate-mass BHs:** $M \sim 10^2$-$10^5 \, M_\odot$ (LISA future targets).
- **Supermassive BHs:** $M \sim 10^6$-$10^{10} \, M_\odot$ (quasars, AGN).
- **GW catalogs:** GWTC-1, GWTC-2, GWTC-3 (LIGO/Virgo/KAGRA observing runs O1-O3).

**Out of scope:**
- Primordial BHs from inflation (different formation mechanism).
- LISA band GW sources ($f < 1$ Hz) until LIGO/Virgo band is validated.
- Exotic compact objects (boson stars, gravastars) unless BH interpretation fails.

### Experiment plan

**Do not execute any experiments for this hypothesis until T3 A8 Two-Gate, T2 EBN-CMB, and T2 Metriplectic Instruments pass their respective gates.**

- **E1 (Seed mass function extraction):** From A8 interface hierarchy, compute energy distribution $\Delta E(k)$ at each level $k$; map to mass function $n(M, z)$.
  - **Gate:** Mass function is well-defined (finite total mass, no divergences); qualitative shape (power-law or log-normal) consistent with observed BH demographics.

- **E2 (Forward merger evolution):** Evolve seeds using merger trees + Eddington-limited accretion; generate synthetic BH population at $z=0$.
  - **Gate:** Population statistics (mass, spin distributions) qualitatively consistent with observations; no catastrophic runaway growth.

- **E3 (Stellar-mass BH comparison):** Compare synthetic population to LIGO/Virgo/KAGRA inferred mass/spin distributions.
  - **Gate:** P1 threshold met for stellar-mass range ($\chi^2 / \mathrm{dof} \leq 2$).

- **E4 (SMBH comparison):** Compare synthetic population to quasar luminosity functions and AGN demographics.
  - **Gate:** P1 threshold met for SMBH range ($\Delta \log(n) \leq 0.5$ dex).

- **E5 (GW event rate prediction):** Compute merger rate $R(z)$ from synthetic population; apply LIGO/Virgo/KAGRA selection function.
  - **Gate:** P2 threshold met ($R_{\mathrm{VDM}}(z)$ within factor of 2 of observed).

- **E6 (CMB/LSS consistency check):** Compute energy density $\rho_{\mathrm{BH}}(z)$ from seed population; verify no disruption to T2 EBN-CMB fits.
  - **Gate:** P3 threshold met (power spectrum residuals $\Delta C_\ell / C_\ell \leq 0.05$, no early energy injection).

- **E7 (Ringdown QNM extraction, optional):** Extract ringdown spectra from synthetic merger population; compare to GR predictions.
  - **Gate:** P4 threshold met ($|\omega_{\mathrm{VDM}} / \omega_{\mathrm{GR}} - 1| \leq 0.1$) *if* ringdown meters are available.

### Dependencies

**Upstream requirements** (explicit dependency wiring):

- **CF3** ([A8 Scaling](../Complete-Formalisms/CF3_A8_Scaling_Hierarchical_Interfaces.md)): Interface hierarchy and energy scaling.
- **T3 A8 Two-Gate** ([T1 PROPOSAL](../Hierarchy/T1_PROPOSAL_G-A8-1_A8-Scaling-Theorem_1D_v1.md), [T2 PROPOSAL](../Axioms/A8_Protein-Packing_Boundary-Law/T2_A8_PROPOSAL_Protein-Packing-Meters_for_Hierarchical_Boundary-Law_v1.md)): Logarithmic depth and boundary-law excess energy gates.
- **T2 EBN-CMB pipeline** ([T2 PROPOSAL](./CMB/T2_PROPOSAL_EBN_CMB_Pipeline_v1.md)): CMB power spectra and acoustic peaks from A8 parameters.
- **T2 Metriplectic Instruments** (cited in [00_HYPOTHESES.md](../z.CANONICAL_Hypotheses/00_HYPOTHESES.md)): Global gates (G-J/M, G-Echo, G-H-theorem, G-Locality).
- **T5_BH_GW_Regression** (future, generic reference): BH demographics and GW catalog regression pack (to be defined in future proposals).

**Dependency killswitch:** This hypothesis is **not executable** until T3 A8 Two-Gate and T2 EBN-CMB pass their gates. If either fails, this hypothesis is **paused** indefinitely.

### Risks & kill-methods

- **R1 (Seed mass divergence):** If A8 interface mass function diverges (infinite total mass or unphysical mass concentration), seed model is invalid. **Kill method:** If E1 shows divergence or total seed mass $> 10\%$ of observable universe mass budget, reject this hypothesis.

- **R2 (Mass function mismatch):** If synthetic BH population is completely inconsistent with observations (e.g., $\chi^2 / \mathrm{dof} > 10$ for all parameter regions), A8 seed model fails. **Kill method:** If E3 and E4 fail with large residuals in three distinct parameter regions, reject this hypothesis.

- **R3 (GW rate catastrophe):** If synthetic GW event rate is off by $> 10\times$ from observed (even accounting for selection effects), merger model is wrong. **Kill method:** If E5 shows rate mismatch in all parameter regions, reject this hypothesis.

- **R4 (CMB disruption):** If BH seed population injects too much energy early ($\rho_{\mathrm{BH}}(z > 10) / \rho_{\mathrm{crit}} > 10^{-4}$), it disrupts CMB/LSS. **Kill method:** If E6 shows power spectrum residuals $\Delta C_\ell / C_\ell > 0.1$ or acoustic peak shifts $\delta \ell / \ell > 0.05$, reject this hypothesis.

**Note:** Rejection of this hypothesis does **not** invalidate CF3, A8 Two-Gate, or core AXIOMS. It only kills the BH seed + GW ladder branch. A8 interface hierarchy may still be valid for other phenomena (e.g., dark matter substructure, cosmic string networks).

### Links

- **H*_**: [H0YY (Horizon/Strong-Field Gravity)](../Gravity/H0YY_HYPOTHESIS_VDM_Horizon_Structure_and_Strong_Field_Gravity.md) (for ringdown QNM connection)
- **CF*_**: [CF3 (A8 Scaling)](../Complete-Formalisms/CF3_A8_Scaling_Hierarchical_Interfaces.md)
- **T*_**: T3 A8 Two-Gate ([T1 PROPOSAL](../Hierarchy/T1_PROPOSAL_G-A8-1_A8-Scaling-Theorem_1D_v1.md)), T2 EBN-CMB ([T2 PROPOSAL](./CMB/T2_PROPOSAL_EBN_CMB_Pipeline_v1.md)), T5_BH_GW_Regression (future, generic reference)
- **Results:** (pending E1-E7 execution after upstream dependencies pass)

### Version history

- v0.1 — 2025-11-21 — created as future-work scaffold
