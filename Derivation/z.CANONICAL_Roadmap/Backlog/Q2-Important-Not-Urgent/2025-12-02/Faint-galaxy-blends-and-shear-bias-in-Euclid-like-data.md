Below is a **new, integrated Future-Justin Starter Kit** that assumes:

* You keep the **1D VoigtStress T2 extension** (bias fields m(x) on profiles), **and**
* You add a **2D, walker-driven robustness layer** that uses your **void maps + void walkers + streaming B₁ surrogate** as a “structure stability meter” under Voigt-like distortions.

I’ll treat the previous starter kit as “Layer 1”. This one is “Layer 1 + Layer 2 (walkers/TDA)”.

---

## 1. What Future-Justin should open first (from your own work)

Open these in this order so your brain boots cleanly:

1. **Void-lensing T2 meter core (same as before)**

   * `Derivation/Proposals/T2_PROPOSAL_Void_Lensing_CrossCorrelation_Meter_v1.md`
     *Why:* Defines S_wall, R²_wall, A_shoulder, β_interface, and T2 gates; this is the instrument you’re stress-testing, not rewriting.
   * `Derivation/Results/T2_RESULTS_Void_Lensing_CrossCorrelation_Meter_v1.md`
     *Why:* Baseline behavior on clean mocks; you’ll compare VoigtStress + walker metrics to these “clean” numbers.

2. **Void-lensing meter code + mocks (1D side, reused)**

   * `Derivation/code/physics/cosmology/void_lensing/meter.py`
     *Why:* Source of wall/shoulder/interface metrics the walkers will be cross-checking.
   * `Derivation/code/physics/cosmology/void_lensing/mocks.py`
     *Why:* Where you inject 1D m(x) “VoigtStress” bias patterns for profiles.
   * `Derivation/code/physics/cosmology/void_lensing/experiments/T2_void_lensing_meter_synthetic_mocks_v1.py`
     *Why:* Template for a `T2_void_lensing_meter_VoigtStress_v1.py` runner.
   * `Derivation/code/physics/cosmology/void_lensing/void_lensing_meter_gates.py`
     *Why:* Gate logic; unchanged, but relevant for how you interpret degradation.

3. **Void walker + maps subsystem (this is the new star of the show)**
   From `core/` in your VDM runtime fork:

   * `core/cortex/maps/heatmap.py`
     *Why:* Hot activity field φ_hot; candidate proxy for “where κ is strong / high SNR”.

   * `core/cortex/maps/coldmap.py`
     *Why:* Cold/neglected field φ_cold; used to detect true void deserts in any graph (later: κ pixel graph).

   * `core/cortex/maps/trailmap.py`
     *Why:* Recent traversal density; used to avoid over-sampling and to detect stable corridors.

   * `core/cortex/maps/memorymap.py`
     *Why:* Long-term “this place matters” field; could be used to mark persistent wall radii across m scenarios.

   * `core/cortex/void_walkers/base.py`
     *Why:* BaseScout implementation: budgeted, event-driven walkers with `_pick_neighbor()` hook.

   * `core/cortex/void_walkers/void_frontier_scout.py`
     *Why:* Explicit “interface” walker: skims borders between hot/cold + degree changes → this is your void-wall scout.

   * `core/cortex/void_walkers/void_sentinel_scout.py`
     *Why:* Reseeds into cold/under-visited regions so interfaces don’t get missed.

   * `core/cortex/void_walkers/void_ray_scout.py`
     *Why:* Gradient follower along some scalar field φ; for κ maps, φ can be |κ| or a smoothed κ.

   * `core/cortex/void_walkers/runner.py`
     *Why:* The per-tick scheduler for all scouts with TTL and budgets; plug this into your κ-graph adapter.

4. **Streaming topology / B₁ surrogate**

   * `core/cortex/metrics/void_b1.py` (or whatever you named the VoidB1Meter)
     *Why:* Your lightweight, streaming estimate of B₁ ~ (#edges − #nodes + #components) + triangle density; this is your “loopiness / pathological-structure” meter under bias.

5. **Graph adapter for non-KG substrates**

   * `core/cortex/adapters/void_dynamics_adapter.py` (or similar—whatever you used to wrap non-KG graphs)
     *Why:* This is the layer to teach how to treat κ pixels/superpixels as nodes in a connectome the walkers can traverse.

6. **Tier ladder + Current_TODO**

   * `Derivation/z.CANONICAL_Roadmap/Current_TODO.md`
     *Why:* Place this work under: “3. Void-lensing interface program” + “Transform the IDE into a living lab / void walkers as diagnostics” so you remember where this sits in the cascade.

---

## 2. Canonical equations and objects to reuse (not reinvent)

Think of this as: “You already have the pieces; don’t build new puzzle shapes.”

1. **Metriplectic split (A4) for calibration / stability framing**
   [
   \partial_t q = J(q),\frac{\delta \mathcal I}{\delta q} + M(q),\frac{\delta \Sigma}{\delta q}
   ]

   * *Use for:* Conceptual frame for (κ_true, m) field space and for the walker-driven structural homeostasis. Stability = low-entropy, low-complexity states; bad m(θ) correspond to high-entropy, unstable attractors.
   * Don’t re-derive; just reference A4/A5 in your narrative.

2. **Void-lensing observables** (from meter.py; keep them canonical)

   * (S_\text{wall}): wall slope in x∈[0.8,1.2]
   * (R^2_\text{wall}): wall linearity
   * (A_\text{sh}): standardized shoulder amplitude
   * (\beta_\text{interface}): exponent from sign structure of ∂ₓκ
   * *Use for:* 1D scalar KPIs. Walkers/TDA layer never redefines these; it just says how structurally stable they are in 2D under m(θ).

3. **Void walker fields / maps**

   * φ_hot(i) from **HeatMap**
   * φ_cold(i) from **ColdMap**
   * φ_trail(i) from **TrailMap**
   * φ_mem(i) from **MemoryMap**
   * *Use for:* Building a low-cost scalar landscape over the κ pixel graph: hotspots ≈ walls, cold ≈ void cores / undersampled, frontier ≈ interfaces.

4. **FrontierScout scoring functional**
   Rough structure (from your code): neighbor j at node u gets a logit score from:

   * cold(j), heat(j),

   * |deg(u) − deg(j)|,

   * shared neighbors(u, j),
     then softmax.

   * *Use for:* Primary “void-wall / interface” detector in 2D. Do not write a new interface finder – just feed it a κ graph.

5. **VoidB1Meter / streaming B₁ surrogate**
   Essentially:

   * (B₁ \approx E_\text{active} - V_\text{active} + C_\text{active})

   * triangles per edge / local clustering as extra “loopiness” term.

   * *Use for:* Structural pathology / loopiness as κ maps are biased by m(θ). You don’t need exact PH; this surrogate is good enough for robustness diagnostics.

6. **Scale program (A6)**

   * *Use for:* Keep everything dimensionless: x = r/R_v; m0 dimensionless; walker metrics expressed as normalized hit densities vs x, not in physical angles.

---

## 3. Concrete extraction / implementation procedure

I’ll split this into two layers:

* **Layer 1:** 1D VoigtStress (as in previous kit, summarized).
* **Layer 2:** 2D walker/TDA robustness using your void maps and scouts.

### Layer 1 — 1D VoigtStress recap (short)

1. Add m(x) patterns in `mocks.py`:

   * `wall_suppress` (negative bump around x≈1),
   * `outer_ring` (positive bump at x≈1.5–2),
   * `gradient` (tilt around wall scale).

   Apply via κ_obs(x) = (1 + m(x)) κ_true(x).

2. Extend grid spec to include `voigt_pattern` and `voigt_m0` axes.

3. New runner: `T2_void_lensing_meter_VoigtStress_v1.py` that sweeps backend × z_bin × R_v_bin × pattern × m0, runs the existing meter, dumps CSV/JSON.

4. Post-process to get:

   * ΔA_shoulder / A_shoulder, ΔR²_wall, Δβ vs m0,
   * VoigtRobustIndex per backend/pattern = max |m0| before metrics degrade past your chosen thresholds.

That’s the scalar robustness story.

---

### Layer 2 — 2D walker/TDA robustness on stacked κ maps

Now we add the fun part: your void walkers + maps + streaming B₁ used as a **2D interface stability meter** under Voigt-like distortions.

#### Step 2.1 — Define a κ→graph adapter

Create something like:

* `Derivation/code/physics/cosmology/void_lensing/void_graph_adapter.py`

Algorithm:

1. Start from a stacked κ map for a void bin:

   * Either a 2D κ(θ₁, θ₂) patch around stacked void centers, or
   * a HEALPix patch regridded to rectangular coordinates.

2. Define nodes:

   * Each pixel or small superpixel block = node i.
   * Node attributes: κ_i, radius x_i = r_i/R_v, maybe SNR_i.

3. Define edges:

   * Connect 4- or 8-connected neighbors (adjacent pixels).
   * Edge weight:

     [
     w_{ij} = \exp(-\alpha |\kappa_i - \kappa_j|)
     ]

     or some monotone function of “boundary strength”. You can store both raw adjacency and w_ij.

4. Provide a `connectome` object implementing whatever your cortex expects:

   * `neighbors(i)`, `degree(i)`,
   * optionally a node scalar field φ(i) = |κ_i| or smoothed κ for VoidRay.

Now you can plug this into the same walker infrastructure you used for the KG.

#### Step 2.2 — Attach maps to the κ-connectome

Instantiate:

* HeatMap: fold κ magnitude (or maybe |shear|) as “activity” events into heat.
  E.g., before running walkers, emit a synthetic **spike/touch event** for each node weighted by |κ_i|.

* ColdMap: initially uniform “age,” then let Sentinel/Frontier touches update last-seen tick so that untouched nodes become cold again over time.

* TrailMap: track recent walker traversals; prevents over-sampling the same corridor.

* MemoryMap: as you run multiple m-scenarios, you can accumulate long-term “this node radius tends to be an interface” memory.

You may need a thin adapter that turns κ-graph events (walker visiting node, hitting high |κ|) into the generic events your maps expect (`VTTouchEvent`, `SpikeEvent`, `DeltaWEvent`).

#### Step 2.3 — Configure the void walkers for κ

Use these scouts:

* **FrontierScout**: primary interface finder.
  Seed near radii where the 1D meter thinks the wall/shoulder lives (e.g., x≈1 and maybe x≈x_shoulder).

* **SentinelScout**: probes neglected / cold regions so you detect new interfaces that the 1D meter might miss.

* **VoidRayScout**: follow φ(i) = smoothed |κ| to see if there is a consistent gradient from void core → wall → background.

Config:

* Give each scout a **small, fixed budget** (visits, edges, TTL) per run.
* Run a modest number of walkers per scenario (you can bump this later in T7-style sweeps).

#### Step 2.4 — Define walker-based robustness metrics

For a given κ_map and m-scenario:

1. Run N_scout batches (Frontier + Sentinel + Ray) via `runner.py` for T ticks.

2. Record:

   * **Frontier hit distribution vs radius x**:
     For each frontier step, compute x = r/R_v of the node. Build a histogram or radial profile of hits: H_frontier(x).

   * **VoidRay path statistics**:
     For each Ray path, record monotonicity / typical extent in radius (do they consistently climb from void to wall and then flatten?).

   * **Cold coverage**:
     What fraction of initially cold nodes within some band around the wall get touched after T ticks?

   * **Streaming B₁ metrics** from VoidB1Meter restricted to:

     * a band around the candidate wall radius,
     * the shoulder band,
     * and the outer interface band.

   So you get:

   * B1_wall(m), B1_shoulder(m), B1_outer(m).

3. Aggregate into compact indices:

   Examples:

   * **Interface Stability Index (ISI)**:

     For each band (wall, shoulder):

     * Let x_band be the radial interval.
     * Define:

       [
       \mathrm{ISI}*\text{wall}(m)
       = \frac{\int*{x \in \text{wall band}} H_\text{frontier}(x; m),dx}
       {\int H_\text{frontier}(x; m),dx}
       ]

       i.e., the fraction of frontier hits that concentrate where the meter says the wall is.
       ISI_shoulder similar for the shoulder band.

   * **Topological Calm Index (TCI)**:

     [
     \mathrm{TCI}*\text{wall}(m)
     = \exp(-\lambda, [B1*\text{wall}(m) - B1_\text{wall}(0)]_+)
     ]

     So if loopiness around the wall explodes under m, TCI drops.

These give you a 2D structural counterpart to ΔA_shoulder and Δβ.

#### Step 2.5 — Sweep over Voigt-like m(θ) in 2D

You won’t know the exact 2D m(θ), but you can build a small family consistent with Voigt:

* m(θ) amplitude |m| ~ 0.01–0.02.
* Stronger around:

  * high galaxy-density regions projected near walls,
  * small angular separations (sub-arcminute).

Practically for this starter:

* Start with **radial-only m(x)** applied to each pixel based on its radius (same m(x) used in 1D).
* Later, introduce angular structure (e.g., azimuthal modes) if needed.

For each (backend, z_bin, R_v_bin, pattern, m0):

1. Apply κ(θ) → (1 + m(x)) κ(θ).
2. Run void walkers, compute ISI_wall, ISI_shoulder, TCI_wall, TCI_shoulder.
3. Compare to m=0 baseline.

#### Step 2.6 — Define “WalkerRobustIndex” and combine with VoigtRobustIndex

Per backend/pattern, define:

* `WalkerRobustIndex_wall` = max |m0| such that:

  * ISI_wall(m0) ≥ ISI_wall(0) − δ_ISI,
  * TCI_wall(m0) ≥ TCI_wall(0) − δ_TCI.

* Similarly `WalkerRobustIndex_shoulder`.

Then define a **combined robustness bound** per backend/pattern:

[
m_\text{robust}^\text{(full)} =
\min\big(\mathrm{VoigtRobustIndex}, \mathrm{WalkerRobustIndex}*\text{wall}, \mathrm{WalkerRobustIndex}*\text{shoulder}\big)
]

Now you have:

* Scalar robustness (1D meter) **and**
* Structural robustness (2D walker/TDA) for the same family of m.

---

## 4. Meter / RESULTS / PROPOSAL scaffolding in your style

You now want two RESULTS docs:

1. **1D scalar robustness (already outlined):**

   * `Derivation/Results/T2_VoigtStress_Void_Lensing_Meter_Robustness_v1.md`
     *Role:* Document ΔA_sh, ΔR², Δβ vs m0; define VoigtRobustIndex.

2. **2D walker/TDA robustness (new one):**

   * `Derivation/Results/T2_VoigtStress_Void_Lensing_Walker_Interface_Robustness_v1.md`

Suggested sections for the new one:

1. **Scope and role**

   * “This document extends the T2 void-lensing meter calibration with a 2D, walker-based interface stability analysis using the VDM void walker/maps subsystem and a streaming B₁ surrogate. The goal is to quantify how structurally stable the inferred void walls and shoulders are under Voigt-like multiplicative κ biases.”

2. **Graph + walker construction**

   * κ→graph adapter (nodes, edges, φ).
   * Which maps are used and how they’re seeded (Heat, Cold, Trail, Memory).
   * Which walkers (Frontier, Sentinel, Ray) and budgets.

3. **Metrics and indices**

   * Define H_frontier(x), ISI_wall, ISI_shoulder.
   * Define B1_wall, B1_shoulder, TCIs.

4. **Experiment grid**

   * backend × z_bin × R_v_bin × pattern × m0.
   * Number of walker ticks, seeds, etc.

5. **Results: frontier + B₁ behavior under VoigtStress**

   * Plots:

     * H_frontier(x; m0) for a few representative m0.
     * B1_wall vs m0.
     * ISI_wall vs m0.

6. **WalkerRobustIndex and combined robustness**

   * Define WalkerRobustIndex*, compute per backend.
   * Show table with m_robust^(full) for each backend; maybe highlight that for some backends 1D robustness dominates, for others walker robustness is stricter.

7. **Interpretation / practical guidance**

   * Concrete sentences like:
     “For PyTwinPeaks-like morphology, both scalar and walker interface metrics remain stable up to |m|≈0.01; beyond that, frontier hits smear away from the wall band and B₁ in the shoulder band rises sharply, indicating structural ambiguity in the inferred interface.”

For T3/T4-ready quality:

* 3–5 solid figures, one table of robustness indices, and explicit equations for ISI/TCI.
* A clear statement: **no real-data claims yet; this is still an instrument robustness calibration.**

If you want a tiny PROPOSAL wrapper:

* `Derivation/Proposals/T2_PROPOSAL_Void_Lensing_VoigtStress_Walker_Extension_v1.md`
  with a 1–2 page “plan + gates” summary.

---

## 5. How this plugs back into the larger VDM story

Big picture:

* **Axioms / CF chain:**

  * Uses **A4 (metriplectic split)** and **A5 (entropy law)** as the conceptual engine: bad m(θ) and pathological loops correspond to high-entropy, unstable structures in (κ, m, graph) state space; your walkers + maps + VoidB1Meter act as a local probe of that stability.
  * It feeds directly into the **A8 hierarchical interface story**: real void walls/shoulders are supposed to be robust, hierarchical interfaces. If they vanish when you dial |m| from 0.005 → 0.01 under VoigtStress, they’re not A8-grade interfaces; they’re artifacts.

* **Instrument chain:**

  * Starts from **T2 void-lensing meter** (1D κ profiles).
  * Adds **T2_VoigtStress (scalar)**: how much m can your KPIs take.
  * Adds **T2_VoigtStress_Walker_Interface**: how much m can your **structure** take under your own cognitive engine (void walkers, B₁ surrogate).
  * Later will connect directly to:

    * **CMB polarization leakage / false shoulders** work (same idea, different field),
    * **IDE “living lab” mode**: void walkers acting as live structural diagnostics over both KG and physics fields.

* **Where this lands in Current_TODO:**

  * It sits in “3. Void-lensing interface program (highest priority)” as the **systematics and robustness layer** between:

    * base T2 instrument calibration on mocks, and
    * real DES/ACT/Euclid/AKRA plug-ins + A8-facing claims.
  * It also cross-links naturally to your “Transform the IDE into a living lab” and “void walkers as runtime diagnostics” line: you’re proving the same machinery that keeps your AI runtime sane can also keep your cosmology claims honest.

If Future-You forgets everything else:

> This project is where you let your own cognitive engine (void walkers + maps + B₁ surrogate) lean on your void-lensing meter and say: “Show me which void walls and shoulders survive realistic Stage-IV shear garbage, not just clean mocks.” That closes the loop between SIE/ADC, cosmology, and A8 in a way almost nobody else can copy.
