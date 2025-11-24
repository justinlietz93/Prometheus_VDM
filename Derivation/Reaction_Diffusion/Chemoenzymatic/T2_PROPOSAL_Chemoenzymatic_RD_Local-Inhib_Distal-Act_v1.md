# 1. T2 (Instrument) – Chemoenzymatic RD Meter: Local Inhibition & Distal Activation

> Created Date: YYYY‑MM‑DD  
> Commit: <git rev-parse HEAD>  
> Provenance hash (base_sha256, salt_hex, salted_sha256): <to be filled>  
> Proposer contact(s): <justin@neuroca.ai>  
> License: See LICENSE  
> Short summary (TL;DR): Instrument to quantify how short‑range nonlocal activation and local inhibition control pattern scale and coarsening exponents in a chemo‑enzymatic RD system, as an A2/A6 testbed.

## 2. List of proposers and associated institutions/companies

- Justin K. Lietz – Neuroca, Inc. – Principal investigator, implementation, analysis.

## 3. Abstract

This proposal defines a T2 instrument that reimplements the chemo‑enzymatic reaction–diffusion system with **local inhibition and distal activation** described in *“A chemoenzymatic reaction‑diffusion system with local inhibition and distal activation”* as a calibrated VDM testbed. The goal is to measure how the interaction‑kernel range and reaction rates set a dominant pattern length‑scale and modify coarsening exponents β, directly informing A2 (locality) and A6 (dimensionless scaling of hierarchical interfaces). The instrument outputs interface counts, dominant wave number \(q^\*\), and coarsening exponents β as functions of kernel range and control parameters, with explicit PASS/FAIL gates.

## 4. Background & Scientific Rationale

VDM’s M‑limb is anchored by an overdamped RD branch with equation anchors E‑015–E‑018 in `00_EQUATIONS.md`. :contentReference[oaicite:0]{index=0}  A6 concerns how interface hierarchies and coarsening laws depend on interaction length scales and dimensionless groups.   

The chemo‑enzymatic system provides an experimentally realizable RD model where **activation is nonlocal (distal)** and **inhibition is local**, producing tunable patterns and arrested coarsening. This is an ideal meter for A6 because:

- the interaction kernel can be parameterized by an effective range \(\xi\),
- pattern length‑scales and domain counts can be measured as functions of \(\xi\) and reaction parameters,
- the system interpolates between classical coarsening and finite‑length‑scale patterned phases.

The instrument focuses only on **diagnostics** (no new axiom claims): pattern selection, interface counts, and β vs \(\xi\).

## 5. Intellectual Merit and Procedure

The scientific questions:

1. How does the dominant pattern wave number \(q^\*\) depend on the effective activation range \(\xi\)?
2. How does the coarsening law \(L(t)\sim t^{\beta(\xi)}\) or interface‑count decay \(N(t)\sim t^{-\beta(\xi)}\) change as \(\xi\) is varied?
3. Is there a range of parameters where coarsening is effectively arrested (β→0) and patterned phases coexist with homogeneous states?

Importance: directly probes VDM A6 using a physically motivated RD model, and provides a bridge between microscopic RD control parameters and macroscopic interface statistics.

Planned rigor: preregistered parameter grids, fixed seeds, explicit JSON specs/schemas, and PASS/FAIL gates on fit quality (R²) and qualitative regime separation.

## 5.1 Experimental Setup and Diagnostics

**Governing equations.** Dimensionless chemotypes \(u(x,t)\) (substrate) and \(v(x,t)\) (enzyme/activator):

$$[
\partial_t u = D_u \nabla^2 u + f_u(u,v; \theta),
\qquad
\partial_t v = D_v \nabla^2 v + f_v(u, (K_\xi * u); \theta),
]$$

where \(K_\xi\) is a normalized radial kernel of range \(\xi\) encoding distal activation; \(f_u,f_v\) implement local inhibition and activation kinetics consistent with the source paper.

**Parameters.**

- Diffusion: \(D_u, D_v\) (dimensionless after rescaling).
- Reaction rates: \(k_1, k_2, \dots\) in parameter vector \(\theta\).
- Kernel range: \(\xi\) (in grid units).
- Domain size: \(L_x \times L_y\), grid \(N_x\times N_y\), spacing \(\Delta x\).
- Time window \(T\), step \(\Delta t\).
- Seeds \(S\) for noise / initial conditions.

**Diagnostics.**

- Dominant wave number \(q^\*(t)\) from structure factor \(S(q,t)\); late‑time \(q^\*_\infty\).
- Interface count \(N(t)\): number of connected domains above/below threshold.
- Coarsening exponent β from fits \(L(t)\sim t^\beta\) or \(N(t)\sim t^{-\beta}\).
- Pattern‑arrest indicator: slope β and variance of \(N(t)\) over late‑time window.
- Quality metrics: fit R², bootstrap CIs.

**Gates.**

- G1 (Fit quality): R² ≥ 0.98 for β‑fits on log–log spans with ≥1 decade.
- G2 (Regime separation): existence of parameter ranges where β(\(\xi\)) is statistically distinguishable (CIs disjoint) between classical and arrested regimes.
- G3 (Reproducibility): results stable across seeds (β variation ≤ 0.05).

## 5.1.1 Pre‑Run Config Requirements

- `Derivation/code/physics/reaction_diffusion/APPROVAL.json` configured with allowed tags for this instrument.
- Schema file: `Derivation/code/physics/reaction_diffusion/schemas/chemoenzymatic_rd_v1.schema.json`.
- Spec file: `Derivation/code/physics/reaction_diffusion/specs/chemoenzymatic_rd_v1.0.json` including parameter grids, seeds, runtime, and artifact paths.
- PRE‑REGISTRATION manifest for this proposal with salted hashes as per `PROPOSAL_PAPER_TEMPLATE`. :contentReference[oaicite:2]{index=2}  

## 5.2 Experimental runplan

- Sweep \(\xi\) over a log‑spaced grid (e.g. \(\xi \in [1, 16]\)) and reaction parameters \(\theta\) over a small set of regimes.
- For each (\(\xi,\theta\)), run S seeds to time \(T\), sampling snapshots for pattern statistics.
- Compute \(S(q,t)\), \(q^\*(t)\), interface count \(N(t)\), and fit β in a preregistered time window.
- Store PNG dashboards, CSV metrics, JSON summaries under `Derivation/code/outputs/reaction_diffusion/chemoenzymatic_rd/{tag}/`.
- On PASS of G1–G3, certify the meter; on FAIL, file a CONTRADICTION_REPORT and adjust discretization or thresholds in a new tagged iteration.

## 6. Personnel

- Justin K. Lietz — implement RD kernels, analysis meters, specs/schemas, and publish RESULTS; maintain instrument as part of A2/A6 ladder.

## 7. References

- VDM Canon RD equations and A6 documents (`00_EQUATIONS.md`, `CF3_A8_Scaling_Hierarchical_Interfaces.md`, `T8_A8_PROPOSAL_Lietz_A8_Hierarchy_Infinity_Resolution_Conjecture_v1.md`).   
- Original chemo‑enzymatic RD paper: *A chemoenzymatic reaction‑diffusion system with local inhibition and distal activation* (2025).
