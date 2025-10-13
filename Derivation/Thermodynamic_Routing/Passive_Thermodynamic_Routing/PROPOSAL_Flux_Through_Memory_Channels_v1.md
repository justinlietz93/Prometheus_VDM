<!-- ATTENTION! This proposal is whitepaper-grade per template: full structure, MathJax, explicit pass/fail gates, provenance, and artifact policy. Keep length ≤ 5 pages including figures/references. -->
# Flux Through Memory Channels (Frozen Landscape) — Passive Thermodynamic Routing v2 (Pre‑Registration)

> Commit: 9c27e65a34a87eae875ed49b419ad4e2030c7e89
> Salted hash: 1e6555fff132d77448269d4b968934741587ff43d29fca521192f7f6a392b9c6

Author: Justin K. Lietz  
Date: 2025-10-13  
Tag: thermo-routing-v2-ftmc

## 1. Proposal Title and date

Flux Through Memory Channels (Frozen Landscape) — Passive Thermodynamic Routing v2

Date: 2025-10-13

## 2. Proposers and affiliations

- Justin K. Lietz — Prometheus VDM Project

## 3. Abstract

We will test whether a fast transport field (“river”) selectively follows a fixed channel landscape derived from a separate “memory” field (or any exogenous map). Unlike Memory Steering, the channel map is frozen (read-only) during the run. We pre‑register KPIs that quantify adherence and selectivity to the channels—channel‑adherence efficiency $\eta_{\rm ch}$, bias change relative to a geometry baseline $\Delta B_{\rm ch}$, and anisotropy $\mathcal A$ (parallel vs. transverse flux)—along with instrument checks (H‑theorem, determinism). Explicit nulls (geometry‑only, shuffled map, mirror) establish identifiability. Success requires 95% CIs excluding null with preregistered thresholds; RJ appears as a diagnostic only.

## 4. Background & Scientific Rationale

Passive thermodynamic routing (metric descent) in structured domains can bias outflux without active control. Here we probe a stronger form of passive selectivity: adherence to pre‑declared channels (e.g., high mobility $\mu(x,y)$ or low potential $U(x,y)$ corridors) representing the “memory” landscape but not evolving during the experiment. This isolates the claim “the river follows the channels” from Memory Steering’s online write/read feedback. A metriplectic RD model for the fast field $\phi$ is sufficient:

$$
\partial_t \phi \,=\, \nabla\!\cdot\!\big(D\,\nabla\phi\big)\;+
\begin{cases}
-\,\nabla\!\cdot\!\big(\mu(x,y)\,\nabla\phi\big), & \text{map\_mode = mobility}\\[4pt]
-\,\nabla\!\cdot\!\big(\phi\,\nabla U(x,y)\big), & \text{map\_mode = potential}
\end{cases}
\; +\; R(\phi). \quad (1)
$$

We require interior no‑flux walls and open outlets; outflux is counted only at outlet faces. RJ fits are retained as spectrum sanity checks, not success criteria.

## 5. Intellectual Merit and Procedure

- Importance: Demonstrates selective routing due to a structured channel landscape beyond bare geometry—an essential stepping stone to Memory Steering and J‑dominant self‑steering.
- Impact: Establishes preregistered, auditable KPIs for adherence/selectivity with explicit nulls and a compliance snapshot that prevents false positives.
- Rigor: Preflight compliance checks; operator/BC alignment for diagnostics; CI‑based gates; strict IO/provenance policy.

## 5.1 Experimental Setup and Diagnostics

- Domain & BCs: 2‑outlet geometry; reflecting sidewalls; open right boundary with two outlet segments A/B. Port closure ablation yields zero outflux by construction.
- Channel map: either mobility $\mu(x,y)$ or potential $U(x,y)$ supplied as an input raster; treated as immutable during runs (content hash recorded at start/end; must match).
- Dynamics: Eq. (1) with bounded $(D, r, u)$ for $R(\phi)$ if used. Deterministic stepper and plans; single‑thread computation.
- Inputs the runner must accept:
  - `channel_map` (2D array), `map_mode` in {"mobility","potential"}, auto `map_hash`.
  - Grid, BCs, $\Delta t$, horizon $T$, checkpoints $K$.
  - Injection parameters, seeds; RJ window and $k$‑band (diagnostic only).
- Compliance Snapshot (printed before stepping; any FAIL aborts):
  1) boundary_model = no‑flux interior + open outlets → OK/FAIL  
  2) flux_convention = outflux‑only (clip <0), total outflux $>\varepsilon$ → OK/FAIL  
  3) map_mode + map_hash start=end (immutability) → OK/FAIL  
  4) RJ operator/BC basis matches stepper (diagnostic) → OK/FAIL  
  5) determinism receipts (threads/BLAS/FFT/plan, checkpoint equality clause) → OK/FAIL
  6) probe‑limit runtime: scout list excludes any actuators (e.g., GDSP/RevGSP); runner passes bus=None to scouts; event whitelist observed (vt_touch, edge_on, optional spike only); no writes/mutations → OK/FAIL  
  7) frozen map coupling: MemoryMap has an attached external field; MemoryMap.fold is a no‑op and snapshots delegate to the field; recorded `map_hash` is pinned in receipts → OK/FAIL  
  8) budget mapping receipts: with $W$ walkers and $H$ hops, budgets satisfy $\texttt{ttl}=H$, $\texttt{visits}=W\times H$, and $\texttt{edges}\approx\texttt{visits}$ (reported explicitly) → OK/FAIL

## 5.2 Experimental runplan

- Baseline/nulls:
  - Geometry‑only null: replace channel map by uniform $\mu$ or flat $U$.
  - Shuffled‑map null: spatial permutation that preserves histogram but destroys corridor coherence.
  - Mirror test: reflect the map laterally; expected outlet preference flips sign.
- Channelized runs: same geometry/injection as nulls; frozen map applied.
- Seeds and windows: preregister a small seed band for pilot thresholding, then fix thresholds and rerun. RJ windows/bands are registered but diagnostic only.
- Runtime: comparable to passive v2 per seed; multiplied by number of nulls + channelized runs.
- Success plan: KPIs meet gates with CIs excluding null; meter checks green.  
- Failure plan: If compliance green yet KPIs fail, report falsification at these settings; optionally adjust map contrast or extend horizon $T$ under a new tag.

## 6. KPIs and Pass/Fail Gates (pre‑registered)

- Channel‑adherence efficiency $\eta_{\rm ch}$: fraction of cumulative flux aligned to the channel skeleton (or within a corridor mask built from high‑$\mu$ / low‑$U$ ridges).  
  Gate: $\eta_{\rm ch} \ge \theta$ and 95% CI excludes the geometry‑only null. ($\theta$ to be set from pilot; target $\ge 0.60$ for strong maps.)
- Selectivity over geometry baseline $\Delta B_{\rm ch}$: difference in outlet bias between channelized vs geometry‑only runs at identical settings,  
  $\Delta B_{\rm ch} = B_{\rm with\,map} - B_{\rm baseline}$.  
  Gate: CI excludes 0 and $|\Delta B_{\rm ch}| \ge \delta$ (pilot‑set, e.g., $0.05\!\text{–}\!0.10$).
- Anisotropy $\mathcal A$: ratio of flux components parallel vs transverse to channel tangents (or gradient‑aligned measure),  
  $\mathcal A = \frac{\mathrm{flux}_{\parallel}}{\mathrm{flux}_{\perp}}$.  
  Gate: $\mathcal A \ge \gamma$ with CI excluding 1 (pilot‑set, start $\gamma \approx 1.5$).
- Meter checks (instrument only): H‑theorem violations = 0 (if metric step applies); no‑switch determinism receipts; RJ R² reported but not gated.

Notes on construction:

- Skeleton/mask: compute channel corridors via ridge finding (e.g., high‑$\mu$ ridges or low‑$U$ valleys) and store both the binary mask and local tangent vectors for alignment.
- Alignment metric: decompose local flux into $\parallel$ and $\perp$ components relative to tangents; aggregate over time to compute $\eta_{\rm ch}$ and $\mathcal A$ with CIs.

## 7. Discrete Stability, Determinism, and Provenance

- $\Delta t$ ladder preregistered with $\Delta t_0 < 0.8/\omega_{\max}$ (discrete), checkpoints every $K$ steps; equality clause = bitwise or $\ell_\infty\!\le 10^{-12}$.
- Receipts: environment threads, BLAS/FFT names, plan mode; policy block with approval status; artifact SHA‑256s.
- IO policy: PNG/CSV/JSON via `Derivation/code/common/io_paths.py`; failed gates route to `failed_runs/`; diagnostic RJ badge on figure.

## 8. Required Artifacts (figures/logs)

1) Geometry + channel map: left panel map (\mu or U) with skeleton overlay; right panel late‑time field with outlet‑row flux arrows and a histogram of $\mathrm{flux}_{\parallel}$ vs $\mathrm{flux}_{\perp}$.  
2) Adherence/Selectivity dashboard: $\eta_{\rm ch}$ time series + final CI bar; $\Delta B_{\rm ch}$ CI bar; $\mathcal A$ CI bar; receipts (map hash, mode, boundary model, total outflux).  
3) Meter plot: Lyapunov monotonicity (and $\Delta L$), checkpoint ticks, equality clause; RJ panel marked “diagnostic only.”  

All figures include numeric captions tied to JSON fields; logs include per‑seed CSVs and a summary JSON with the gate matrix.

## 9. Approval and Governance

- Requires pre‑approval in `Derivation/code/physics/thermo_routing/APPROVAL.json` (script‑scoped HMAC).  
- Unapproved runs are quarantined and excluded from canon.  
- RESULTS must follow `Derivation/Writeup_Templates/RESULTS_PAPER_STANDARDS.md`.

## 10. Personnel

- Justin K. Lietz: design, approvals, execution, analysis, and RESULTS authorship. Additive analyzers only; no divergence from IO/policy.

## 11. References

- Passive thermodynamic routing v2 (instrument calibration) internal docs.  
- Device‑based optical thermodynamic routing as passive analogs (Derivation/References/Photonics/…).  
- Discrete gradient integrators and metriplectic background (canonical references in Derivation/EQUATIONS.md).
