# HYPOTHESIS — VDM Horizon Structure and Strong-Field Gravity

---

## H0YY — Horizon-Scale / Strong-Field Gravity (future-work scaffold)

**Classification:** Gravity-future  
**Owner:** Justin K. Lietz  
**Status:** ACTIVE  
>*This hypothesis is a future-work scaffold. It sets targets and meters but makes no canonical claim until all upstream CF/T instruments and global gates pass and dedicated RESULTS files are published.*

**One-line objective:** Relate VDM's causal structure and effective metric to GR-like horizon behavior near compact objects, using Analog Horizon and weak-field Gravity Regression as constraints.

### Formal statement

Reference:
- [CF4](../Complete-Formalisms/CF4_Telegraph_Fisher_Causality.md) (Telegraph-Fisher causality)
- [CF1](../Complete-Formalisms/CF1_QGT_to_Metriplectic_Brackets.md) (metric/QGT side)
- [AXIOMS](../AXIOMS.md) (J-cone, local causality)

**Hypothesize** that there exists an effective metric $g_{\mu\nu}^{\mathrm{VDM}}(x)$ such that:

1. **Weak-field limit:** Linearized $g_{\mu\nu}^{\mathrm{VDM}}$ reproduces the gravitational potential used in T5 Gravity Regression fits (rotation curves, lensing profiles) within AIC/BIC gates.

2. **Strong-field regime:** Near compact configurations (high void-debt $D$ or tachyonic collapse), there exist surfaces $\mathcal{H}$ that satisfy trapped-surface / apparent-horizon criteria analogous to GR:
   - **J-limb signal trapping:** Outgoing null rays (in the effective metric) fail to escape to asymptotic observers, within a tolerance on J-cone slack.
   - **Expansion sign change:** The expansion $\theta$ of outgoing null congruences changes sign at $\mathcal{H}$, matching the GR apparent horizon condition.

3. **Lorentz signature preservation:** The effective metric maintains Minkowski signature $(-,+,+,+)$ everywhere outside singularities, consistent with [VDM-AX-C02](../AXIOMS.md#vdm-ax-c02).

### Predictions (decisive metrics)

These are **targets** the theory must meet, not assumed facts:

- **P1 (Weak-field consistency):** Linearized $g_{\mu\nu}^{\mathrm{VDM}}$ yields rotation curves and lensing profiles compatible with T5 Gravity Regression forward model: $\Delta \mathrm{AIC} \leq 5$ compared to GR-based fits on matched data.

- **P2 (Horizon equivalence — trapping):** There exist surfaces $\mathcal{H}$ where:
  - J-limb signal propagation (from Analog Horizon tests) cannot escape to asymptotic observers, with cone slack $\delta c/c \leq 0.01$.
  - Photon sphere / light ring radius $r_{\mathrm{ph}}$ satisfies $|r_{\mathrm{ph}} / r_{\mathrm{GR}} - 1| \leq 0.05$ for Schwarzschild-like configurations.

- **P3 (Horizon equivalence — expansion):** The expansion of outgoing null congruences $\theta_{\mathrm{out}}$ changes sign at $\mathcal{H}$: $\theta_{\mathrm{out}}(r < r_{\mathcal{H}}) < 0$ and $\theta_{\mathrm{out}}(r > r_{\mathcal{H}}) > 0$, with sign-change location within $10\%$ of GR horizon radius.

- **P4 (Ringdown compatibility, optional placeholder):** Perturbations of compact configurations produce quasi-normal mode (QNM) spectra that pass existing ringdown/DSI meters: $|\omega_{\mathrm{VDM}} / \omega_{\mathrm{GR}} - 1| \leq 0.1$ for dominant $\ell=2$ modes.

**Note:** P4 is a placeholder target; actual thresholds will be set by ringdown instrument specifications once available. Thresholds for P1-P3 are provisional and may tighten after weak-field gravity (T5) passes.

### Rationale (bounded)

VDM's effective metric $g_{\mu\nu}^{\mathrm{VDM}}$ emerges from the Quantum Geometric Tensor (CF1) and is modified by void-debt $D$ and tachyonic potential gradients. In the weak-field limit, linearized perturbations reproduce Newtonian gravity with post-Newtonian corrections (T5 Gravity Regression). In the strong-field regime, causal structure from CF4 (Telegraph-Fisher) imposes finite-speed constraints on signal propagation; when these constraints become severe (high $D$, steep gradients), they mimic GR horizons.

The **horizon analogy** rests on:
1. **Causal dominance:** J-cone tipping (from Analog Horizon tests) shows that regions with $D \gg D_{\mathrm{crit}}$ act as causal barriers.
2. **Metric singularity:** If $g_{\mu\nu}^{\mathrm{VDM}}$ develops coordinate singularities (analogous to Schwarzschild $r=2M$), standard GR horizon criteria apply.
3. **Penrose trapped-surface theorem:** If outgoing null congruences have negative expansion inside a compact region, the configuration is gravitationally trapped.

**Key assumptions:**
- The effective metric $g_{\mu\nu}^{\mathrm{VDM}}$ is smooth and non-degenerate outside singularities.
- Lorentz invariance holds at low energy (VDM-AX-C02).
- Weak-field gravity (T5) is validated before testing strong-field regime.

### Preconditions & scope

**This hypothesis is a future-work scaffold.** It makes **no canonical claim** until:

1. **T2 Metriplectic Instruments** pass all global gates (G-J/M, G-Echo, G-H-theorem, G-Locality, G-Artifacts) from [00_HYPOTHESES.md](../z.CANONICAL_Hypotheses/00_HYPOTHESES.md).
2. **CF1** (QGT/metric) is validated with passing gates in RESULTS.
3. **CF3 / CF4** (A8 + Telegraph-Fisher) pass their respective gates, confirming causal structure.
4. **T5 Analog Horizon** (causal dominance tests) is at least partially validated, showing J-cone tipping.
5. **T5 Gravity Regression** (weak-field fits) is validated with rotation curves and lensing profiles passing AIC/BIC gates.

**Domain:**

- Weak-field: $\Phi/c^2 \ll 1$ (Newtonian regime, T5 Gravity Regression).
- Strong-field: $\Phi/c^2 \sim 0.1$-$1$ (near compact objects, BH/NS configurations).
- Asymptotic flatness assumed for boundary conditions.

**Scope:**

- Schwarzschild-like (spherically symmetric) configurations initially.
- Rotating (Kerr-like) configurations are **out of scope** until spherical case passes.
- Cosmological horizons (de Sitter, FRW) are **out of scope** (see H_BHPop for cosmological applications).
- **Note:** All GR quantities (horizon radius, photon sphere, QNM frequencies) are used as comparison baselines; this hypothesis does not assert exact metric equivalence with GR.

### Experiment plan

**Do not execute any experiments for this hypothesis until T2 Metriplectic, CF1, CF3/CF4, T5 Analog Horizon, and T5 Gravity Regression are at least partially validated.**

- **E1 (Effective metric extraction):** From VDM field evolution (CF1 + CF4), extract $g_{\mu\nu}^{\mathrm{VDM}}(x)$ via QGT-based procedure.
  - **Gate:** Metric signature $(-,+,+,+)$ verified; no coordinate singularities outside expected horizon.

- **E2 (Weak-field consistency):** Linearize $g_{\mu\nu}^{\mathrm{VDM}}$ around flat space; compare to T5 Gravity Regression potential.
  - **Gate:** P1 threshold met ($\Delta \mathrm{AIC} \leq 5$).

- **E3 (Photon sphere / light ring):** Trace null geodesics in $g_{\mu\nu}^{\mathrm{VDM}}$; locate unstable circular orbits.
  - **Gate:** P2 threshold met ($|r_{\mathrm{ph}} / r_{\mathrm{GR}} - 1| \leq 0.05$).

- **E4 (Trapping test via Analog Horizon):** Use Analog Horizon J-cone audit; identify regions where outgoing signals fail to escape.
  - **Gate:** P2 threshold met (cone slack $\delta c/c \leq 0.01$).

- **E5 (Null congruence expansion):** Compute $\theta_{\mathrm{out}} = \nabla_\mu k^\mu$ for outgoing null vectors $k^\mu$; identify sign change.
  - **Gate:** P3 threshold met (expansion sign change within $10\%$ of GR horizon).

- **E6 (Ringdown QNM extraction, optional):** Perturb compact configuration; extract QNM spectrum via time-series fitting.
  - **Gate:** P4 threshold met ($|\omega_{\mathrm{VDM}} / \omega_{\mathrm{GR}} - 1| \leq 0.1$) *if* ringdown meters are available.

### Dependencies

**Upstream requirements** (explicit dependency wiring):

- **CF1** ([QGT/Metric](../Complete-Formalisms/CF1_QGT_to_Metriplectic_Brackets.md)): Effective metric construction from QGT.
- **CF3** ([A8 Scaling](../Complete-Formalisms/CF3_A8_Scaling_Hierarchical_Interfaces.md)): Interface hierarchy and energy scaling.
- **CF4** ([Telegraph-Fisher Causality](../Complete-Formalisms/CF4_Telegraph_Fisher_Causality.md)): Finite-speed signal propagation, J-cone constraints.
- **T2 Metriplectic Instruments** (cited in [00_HYPOTHESES.md](../z.CANONICAL_Hypotheses/00_HYPOTHESES.md)): Global gates (G-J/M, G-Echo, G-H-theorem, G-Locality).
- **T5 Analog Horizon** ([Causal Dominance](../Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md)): J-cone tipping and causal barrier tests.
- **T5 Gravity Regression** ([Weak-field fits](./Gravity_Regression/)): Rotation curves, lensing profiles, AIC/BIC validation.

**Dependency killswitch:** This hypothesis is **not executable** until weak-field gravity (T5 Gravity Regression) and causal dominance (T5 Analog Horizon) are at least partially validated. If either fails, this hypothesis is **paused** indefinitely.

### Risks & kill-methods

- **R1 (Weak-field failure):** If linearized $g_{\mu\nu}^{\mathrm{VDM}}$ does not reproduce T5 Gravity Regression fits ($\Delta \mathrm{AIC} \gg 5$), the effective metric construction is inconsistent. **Kill method:** If E2 fails in three distinct weak-field configurations, reject this hypothesis.

- **R2 (No trapping):** If J-limb signals escape from all configurations (no cone slack, no photon sphere), there is no horizon-like structure. **Kill method:** If E3 and E4 fail to find trapping in compact configurations with $\Phi/c^2 > 0.3$, reject this hypothesis.

- **R3 (Expansion anomaly):** If $\theta_{\mathrm{out}}$ does not change sign or changes sign far from expected horizon ($|r_{\mathcal{H}} / r_{\mathrm{GR}} - 1| > 0.5$), the horizon analogy breaks. **Kill method:** If E5 fails in two distinct configurations, reject this hypothesis.

- **R4 (Lorentz violation):** If $g_{\mu\nu}^{\mathrm{VDM}}$ develops wrong signature or violates Lorentz invariance (detectable in weak-field tests), VDM is incompatible with GR. **Kill method:** If E1 shows signature violation, reject this hypothesis and flag VDM-AX-C02 for review.

**Note:** Rejection of this hypothesis does **not** invalidate CF1, CF3, CF4, or core AXIOMS. It only kills the strong-field gravity branch. VDM may still describe weak-field gravity (Newtonian + post-Newtonian) without compact object horizons.

### Links

- **H*_**: (no prior horizon-specific hypotheses)
- **CF*_**: [CF1](../Complete-Formalisms/CF1_QGT_to_Metriplectic_Brackets.md), [CF3](../Complete-Formalisms/CF3_A8_Scaling_Hierarchical_Interfaces.md), [CF4](../Complete-Formalisms/CF4_Telegraph_Fisher_Causality.md)
- **T*_**: T5 Analog Horizon ([PROPOSAL](../Causality/PROPOSAL_Metriplectic_Causal_Dominance_v1.md)), T5 Gravity Regression ([directory](./Gravity_Regression/))
- **Results:** (pending E1-E6 execution after upstream dependencies pass)

### Version history

- v0.1 — 2025-11-21 — created as future-work scaffold
