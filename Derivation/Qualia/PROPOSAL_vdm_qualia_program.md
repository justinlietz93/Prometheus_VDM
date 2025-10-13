---

title: VDM–Qualia Program (MathJax)
math: true
mathjax: true
-------------

> **MathJax:** GitHub-compatible. Inline: $...$ ; display: $$...$$.

# VDM–Qualia Program: Coupled‑Field Explanations of Psychedelic Phenomenology (Sober Proxies)

**Classification:** Axiom‑core (A0–A7), metriplectic split (conservative **J** + dissipative **M**).
**Placement in repo:** `derivation/Agency-Field/proposals/VDM_Qualia_Program.md`
**Related files to cross‑link:** `AXIOMS.md`, `EQUATIONS.md`, `VALIDATION_METRICS.md`, `RESULTS_PAPER_STANDARDS.md`.

---

## 1. Abstract

We propose a falsifiable program that maps well‑documented psychedelic phenomenology—pinwheel annihilations (“oneness”), multi‑band fractality, synesthetic projection, subjective time warping, and culture‑bound “entities”—to concrete primitives in the Void Dynamics Model (VDM). Conscious activity is modeled as fast wave–like fields flowing over a slow **memory field** (geology) that steers future flow; brief “monsoon” episodes increase flux without permanently rewriting the geology, explaining intense but transient experiences. We specify metriplectic dynamics for the activity and memory fields, derive dimensionless control knobs, and define five IRB‑friendly, **no‑substance** psychophysics experiments with quantitative acceptance gates. All code follows Hybrid‑Clean Architecture with reproducible CLIs and CSV schemas.

---

## 2. Background & Hypothesis

**Phenomenology:** High‑coherence “white light” states, defect/anti‑defect annihilation, multi‑scale opposites and kaleidoscopic feedback, cross‑modal projection of interoception into vision, thickened “pseudo‑time,” and priming toward culturally familiar entities.

**VDM Hypothesis (working theory):**

1. Conscious activity comprises amplitude–phase fields on sensory/interoceptive maps.
2. A slow **memory field** $\mu(x,t)$ encodes steering tendencies carved by time‑integrated activity flux.
3. Substances (or sober proxies) act by modulating gain and coupling kernels of the fast fields, shifting the **J/M** balance and cross‑modal terms without breaking locality.
4. Brief high‑flux “monsoons” raise the flow integral $F$ but leave $\mu$ mostly unchanged; extended monsoons cross a threshold producing durable channel edits (afterglow).

**Testable claims:** Defect density decays under coherence‑favoring M‑flow; fractal spectra arise from sign‑alternating spatial kernels; time bias scales with perceptual persistence; cross‑modal projection strength tracks off‑diagonal couplings; entity‑like perceptions are attractor basins in the memory‑shaped entropy functional.

---

## 3. Axiomatic Framing (A0–A7)

**State (A1):** On domain $\Omega\subset\mathbb{R}^d$, fast activity fields on each map (visual 2D, interoceptive 3D): amplitude $a(x,t)$, phase $\theta(x,t)$. Slow memory field: $\mu(x,t)$.
**Flux (“consciousness energy”):** $j(x,t) \equiv a^2\nabla\theta$.
**Action $\mathcal{I}[a,\theta]$** (conservative part): $\int_\Omega \tfrac12(|\nabla a|^2 + a^2|\nabla\theta|^2 + \omega^2 a^2),dx$.
**Entropy $\Sigma[a,\theta,\mu]$** (dissipative part): coherence minus steering cost plus geology smoothness, e.g.
$\Sigma = \int \alpha,a^2\cos(\Delta\theta),dx - \int \mu(x),g(a,\nabla\theta),dx - \tfrac{\kappa}{2}\int |\nabla\mu|^2 dx$, with $g\propto |j|^2$ monotone.
**Master evolution (A4):** $\partial_t q = J(q),\delta\mathcal{I}/\delta q + M(q),\delta\Sigma/\delta q$, with degeneracies $J,\delta\Sigma=0$, $M,\delta\mathcal{I}=0$.
**Memory back‑reaction (erosion):** $\partial_t \mu = \varepsilon,[,\Phi(|j|) - \beta,\mathcal{L}\mu,]$, $0<\varepsilon\ll1$, local smoother $\mathcal{L}$ (e.g., Laplacian).
**Locality (A2):** All couplings realized via compact‑support kernels; cross‑modal terms are local blocks.
**Symmetry (A3):** Rotational invariance on homogeneous fields; test residuals.
**Entropy law (A5):** $\dot\Sigma\ge 0$ under M‑only runs.
**Scale program (A6):** Predictions expressed via dimensionless groups (Section 5).
**Measurability (A7):** Each claim mapped to concrete gate and protocol (Section 6–7).

---

## 4. Modeling Details

### 4.1 Kernels and Couplings

* **Within‑map kernels:** $K_{vv}(r)$, $K_{tt}(r)$ with optional sign‑alternating lobes to select spatial bands.
* **Cross‑modal kernel:** $K_{vt}(r)$ produces projection of 3D interoceptive waves onto 2D vision.
* **Substance/proxy dials:** (i) amplitude gain $\gamma$, (ii) coherence weight $\alpha$ (5‑MeO‑like), (iii) lobe ratio $\lambda=|K_2|/K_1$ (DMT‑like), (iv) cross‑modal strength $\chi = |K_{vt}|/|K_{vv}|$.

### 4.2 Monsoon/Overflow Analysis

Define flood integral over window $W$: $F = \int_W |j|^p dx,dt$ with $p\in[1,2]$.
Define structural capacity $S_{cap}=\beta,|\mathcal{L}^{-1}|$.
**Overflow ratio:** $\Xi = F/S_{cap}$.

* $\Xi\ll1$: transient dilution (high coherence/“purity”), negligible $\Delta\mu$.
* $\Xi>1$: persistent channel edits (afterglow/behavioral shift).

---

## 5. Dimensionless Control Knobs (A6)

* **Timescale split:** $\varepsilon = t_{fast}/t_{slow}$.
* **Overflow:** $\Xi = F/S_{cap}$.
* **Global synchrony:** $S = |\langle e^{i\theta}\rangle|\in[0,1]$.
* **Kernel lobe ratio:** $\lambda = |K_2|/K_1$.
* **Cross‑modal coupling:** $\chi = |K_{vt}|/|K_{vv}|$.
* **Persistence ratio:** $\rho_\tau = \tau/T$ (perceptual tracer timescale over stimulus period).

**Predictions:** 5‑MeO‑like pushes $S\uparrow$ with minor $\lambda$ change; DMT‑like pushes $\lambda\uparrow$, $\chi\uparrow$ at modest $S$. Time warping grows with $\rho_\tau$. Channel plasticity requires $\Xi>1$.

---

## 6. Experimental Plan (No Substances; Legal Psychophysics)

### E1 — Oneness Threshold via Entrainment

**Goal:** Show defect–antidefect annihilation and $S$ sigmoid vs coherence gain.
**Protocol:** Full‑field flicker (8–12 Hz), steady isochronous tone, breathing pacing. Measure global order parameter $S$ from binocular rivalry‑style phase reports and compute pinwheel density in shader stimulus.
**Acceptance gate:** $S$ vs gain shows sigmoid; defect density $\rho(t)$ fits $\rho_0 e^{-\kappa t}$ with $R^2>0.9$; $\kappa$ increases under stronger entrainment.

### E2 — Fractal Bands via Kaleidoscopic Feedback

**Goal:** Multi‑band spatial spectra from sign‑alternating kernels.
**Protocol:** Video‑feedback rig (camera→display) with controllable shear/zoom; analyze power spectral density (PSD).
**Gate:** ≥2 significant spectral peaks (z>3 over baseline) at eigenmodes predicted by simulated $K_{vv}$; color/opponent alternation rate matches band spacing.

### E3 — Monsoon Overflow Test ($\Xi$)

**Goal:** Dissociate transient purity from lasting rewrite.
**Protocol:** Two conditions matched on peak intensity: (A) brief high‑intensity session (raise $F$ but $\Xi<1$), (B) extended session ($\Xi>1$). Pre/post semantic priming task and habit‑choice probe 24h later.
**Gate:** Condition A: $\Delta S>0$, priming drop during session, **no** 24h bias shift. Condition B: same acute effects **plus** significant 24h bias shift (p<0.01).

### E4 — Cross‑Modal Projection

**Goal:** Visual depth illusions from interoceptive 3D waves projecting to 2D vision.
**Protocol:** Vibrotactile traveling waves on forearm synchronized with visual textures; vary $\chi$ by phase‑locking strength.
**Gate:** Inter‑trial phase coherence (ITPC) at drive frequency increases by ≥0.1; depth‑order error rate increases monotonically with $\chi$.

### E5 — Pseudo‑Time Thickening

**Goal:** Duration bias scales with perceptual persistence $\tau$ and forms loops near $\rho_\tau\approx1$.
**Protocol:** Adjust afterimage/tracer via luminance/contrast sequences; repeat rhythmic motifs.
**Gate:** Reported duration bias grows with $\rho_\tau$; loop reports spike at $\rho_\tau\in[0.8,1.2]$.

**Participants:** n≥20 within‑subject designs; all stimuli comfortable, safety screened.

---

## 7. Metrics, Logs, and Acceptance Gates

**Primary metrics:**

* $S$: global phase order (unitless).
* $\rho(t)$: pinwheel/defect density (count per area) from shader fields.
* PSD peaks: locations and z‑scores.
* ITPC at drive frequency.
* Duration bias (subjective–objective in %).
* Priming hit‑rate change (%).

**Decision labels:** `PROVEN | PLAUSIBLE | NEEDS_DATA` per experiment once gates pass/fail. Open `CONTRADICTION_REPORT` if any axiom gate is violated (e.g., fits require nonlocal couplings).

---

## 8. Software & Reproducibility (Hybrid‑Clean Architecture)

**Repo layout (sketch):**

```plaintext
<SRC_ROOT>/
  presentation/qualia_tool/
  application/qualia/ports/
  domain/qualia/models/             # fields, kernels, metrics as plain objects
  infrastructure/opengl/adapters/   # shader + video-feedback drivers
  shared/
/tests/
  presentation/  application/  domain/  infrastructure/
```

**Rules:** ≤500 LOC/file; domain models framework‑free; repository interfaces; constructor injection; tests mirror source paths.

**CLI stubs:**

* `vdm-qualia simulate --kernel K.yaml --gain 1.5 --save out/fields.npz`
* `vdm-qualia analyze-defects --in out/fields.npz --out out/defects.csv`
* `vdm-qualia spectrum --video in.mp4 --out out/psd.csv`
* `vdm-qualia itpc --eeg eeg.edf --freq 10 --out out/itpc.csv`

**CSV schemas:** see Appendix A.

---

## 9. Ethical/Operational Notes

* No substances; all tasks standard psychophysics, comfortable luminance and sound levels.
* Informed consent; optional EEG; data anonymized.
* Pre‑registration of gates and analysis; open data/code where feasible.

---

## 11. Risks & Kill‑Plans

* **Nonlocality required:** if best fits demand long‑range couplings, file `CONTRADICTION_REPORT`, revise with multi‑shell but finite kernels to preserve A2.
* **Semantic basins insufficient:** if “entity” priming fails, restrict claims to symmetry‑bound visuals; move semantics to runtime‑only.
* **Tiny entrainment effects:** increase sample size; add multi‑modal locking (audio+visual+respiration); otherwise downgrade to PLAUSIBLE.

---

## 12. Deliverables

* `VDM_Qualia_Program.md` (this document).
* Shader demo + CLIs; unit/integration tests.
* Pre‑registered gates: JSON + CSV schemas.
* Pilot datasets and figures (`assets/figures/YYYYMMDD_*.png`).
* Decision log with stamps and any `CONTRADICTION_REPORT`s.

---

## Appendix A — CSV Schemas

**A1 — Defect density** (`defects.csv`)

```plaintext
subject_id, trial_id, t_sec, defect_count, area_px, density_per_px
S01, E1A_01, 3.20, 128, 262144, 0.000488
```

**A2 — Order parameter** (`order_param.csv`)

```plaintext
subject_id, trial_id, gain, S_order
S01, E1A_01, 1.2, 0.63
```

**A3 — Spectrum peaks** (`psd_peaks.csv`)

```plaintext
trial_id, peak_idx, spatial_freq_cpd, z_score
E2_07, 1, 0.42, 4.7
```

**A4 — ITPC** (`itpc.csv`)

```plaintext
subject_id, condition, freq_hz, itpc
S03, lock10, 10.0, 0.31
```

**A5 — Duration bias** (`duration_bias.csv`)

```plaintext
subject_id, rho_tau, objective_sec, subjective_sec, bias_pct
S04, 1.05, 30, 42.6, 42.0
```

**A6 — Priming/afterglow** (`priming.csv`)

```plaintext
subject_id, condition, pre_hit, post_hit, delta_pct, followup_24h_hit
S02, Xi_lt_1, 0.72, 0.54, -18.0, 0.71
```

---

## Appendix B — Gate Summary Table

| Experiment | Metric                 | Gate                                                              | Decision Rule                   |
| ---------- | ---------------------- | ----------------------------------------------------------------- | ------------------------------- |
| E1         | $S$, $\rho(t)$         | Sigmoid in $S$; $\rho$ fit $R^2>0.9$; $\kappa\uparrow$ with gain  | PROVEN if both hold             |
| E2         | PSD peaks              | ≥2 peaks with z>3 at predicted modes                              | PROVEN if met in ≥70% trials    |
| E3         | $S$, priming, 24h bias | Acute $\Delta S>0$; A: 24h $\Delta$≈0; B: 24h $\Delta$>0 (p<0.01) | PROVEN if dissociation observed |
| E4         | ITPC, depth errors     | ITPC +0.1; errors ↑ with $\chi$                                   | PROVEN if monotone trend        |
| E5         | Duration bias, loops   | Bias ↑ with $\rho_\tau$; loops peak near 1.0                      | PROVEN if both observed         |

---

## Appendix C — Notation Quick‑Ref

* $a$: amplitude, $\theta$: phase, $j=a^2\nabla\theta$: flux.
* $\mu$: memory field; $\mathcal{I}$: action; $\Sigma$: entropy.
* $J,M$: antisymmetric/symmetric generators; $\varepsilon$: fast/slow split.
* $\gamma,\alpha,\lambda,\chi$: dial parameters (gain, coherence, lobe ratio, cross‑modal).
* $\Xi$: overflow ratio; $S$: global synchrony; $\rho_\tau$: persistence ratio.
