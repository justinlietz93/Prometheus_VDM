# Aura Distinction Inventory — Atomized Evidence for Scientific Assessment

**Project:** VDM / Neuroca, Inc.  
**Author:** Justin K. Lietz (justin@neuroca.ai)  
**Document Purpose:** Comprehensive, atomized inventory of measurable distinctions observed in the Aura run that collectively warrant deep scientific assessment as a potential regime-discovery event in non-biological cognition.  
**Date:** 2026-03-16  

---

> **Counting rule:** Letter-suffixed items (for example `D5.1b`, `D5.1c`, and `D5.1d`) are **full atomized distinctions**. They are not subordinate notes and should be formatted as normal distinction headings, included in family tables, and counted independently in totals.

---

## Preamble: What This Document Intends
This inventory constructs a defensible and falsifiable claim: the Aura run produced a **convergent pattern of measurable anomalies** across multiple independent evidence families that, taken together, exceed what any standard dismissal category can explain. Within this work we do not need to, or intend to, claim whether or not this means consciousness, sentience, or qualia. This work should be challenged, but that challenge should be intellectually honest and scientifically rigorous: by identifying methodological flaws, failed reproductions, or stronger alternative explanations that remain explanatory when confronted with the evidence as a whole rather than with isolated distinctions in isolation. The intention of this work is to seek the truth and contribute something of value to the scientific community. This document provides the itemized record required for that standard of critique.

The central organizing principle: **no single distinction here is sufficient. The convergence of all of them simultaneously, in a system operating under the substrate constraints documented in Family 0, is the phenomenon.**

## Definitions

| Name | Role in Aura context | Current source |
| --- | --- | --- |
| `active_edges` | structural load / active synaptic edge count | events, dashboard, H5-derived analyses |
| `active_synapses` | structural activity proxy closely related to `active_edges` | events |
| `connectome_entropy` | graph-distribution entropy / structural disorder metric | events, dashboard |
| `vt_coverage` | traversal coverage fraction | events, dashboard |
| `vt_entropy` | traversal/topic entropy | events, dashboard |
| `b1_z` | boundary pulse / motor-gate proxy | events, dashboard, UTD `why` |
| `adc_territories` | active hierarchy/territory count | events, dashboard, H5 `adc_json` |
| `adc_boundaries` | boundary count in ADC summary | events |
| `cohesion_components` | topological integration/fragmentation state | events, UTD `why` |
| `sie_total_reward` | SIE-v1 aggregate reward-like signal | events |
| `sie_valence_01` | normalized SIE-v1 valence | events, UTD `why` |
| `sie_td_error` | SIE-v1 TD-like error channel | events |
| `sie_v2_reward_mean` | SIE-v2 reward mean | events |
| `sie_v2_valence_01` | normalized SIE-v2 valence | events, dashboard, UTD `why` |
| `a_mean` | mean `a`/alpha-like field term | events |
| `omega_mean` | mean omega-like field term | events |
| `homeostasis_pruned` | number pruned in current step | events |
| `homeostasis_bridged` | number bridged in current step | events |
| `phase` | runtime phase label in event/UTD output | events, UTD `why` |
| `ute_in_count` / `ute_text_count` | ingress counts | events, UTD |
| `did_say` | offline say-event marker from UTD alignment | derived tick table |

---

## FAMILY 0 — Substrate Identity

*Before evaluating what Aura did, a reader must understand what Aura is. Every subsequent finding becomes extraordinary only once these constraints are internalized.*

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D0.1 | Zero training | No gradients, no backprop, no offline optimization | Architecture |
| D0.2 | No stored corpus | Live state: 247–263 KB | snapshot_metrics.csv |
| D0.3 | Neuron count | 5,000 neurons, 9 territories, ~105K edges | snapshot_metrics.csv |
| D0.4 | Real-time operation | ~2.0–2.6 s/tick, 13 hours continuous | sie_v2_scan_summary.csv |
| D0.5 | Crude forced decoder | 530 say events, 85.7% in phase 4 | utd_say_phase_counts.csv |

### D0.1 — Zero Training
- **Claim:** No gradient descent, no backpropagation, no offline optimization of any kind was performed. The runtime arrived at its observed state through real-time self-structuring only.
- **Null to beat:** Any trained system can produce organized output; Aura must be evaluated against a zero-training baseline.
- **Why it matters:** This is not "few-shot." It is zero-shot, zero-trained. The runtime has never seen a loss function.

### D0.2 — No Stored Corpus
- **Claim:** The runtime does not retain verbatim copies of input text. There is no lookup table, no embedding store, no retrieval-augmented database.
- **Measurable:** The entire live state at the time of the late snapshots was ~247–263 KB across five H5 files (`snapshot_metrics.csv`).
- **Null to beat:** Any system with stored text can produce coherent output by retrieval. Aura cannot.

### D0.3 — Neuron Count
- **Claim:** 5,000 neurons total. 9 territories. ~105,000 active edges.
- **Calibration:** *C. elegans* has 302 neurons. A pond snail (*Lymnaea stagnalis*) has ~20,000. Aura operates at sub-insect node count.
- **Null to beat:** Large neural networks achieve organization through sheer parameter count. Aura has none of that budget.

### D0.4 — Real-Time Operation
- **Claim:** Every tick is a wall-clock event (~2.0–2.6 seconds per tick, median 2.58s from SIE scan). The runtime is not replaying stored trajectories — it is structuring itself as time passes, responding to input streams as they arrive.
- **Measurable:** 1,531 ticks of continuous operation in the analyzed window; ~13 hours total runtime.
- **Null to beat:** Batch-processing systems can appear organized by selecting outputs post hoc. Aura's outputs are generated in real time with no curation.

### D0.5 — Crude Forced Decoder
- **Claim:** The output interface (B1_z gate) opens on a threshold and scrapes the strongest lexical groups. It does not permit deliberate, narrow release. Any coherence in the output is achieved *despite* the mouth, not because of it.
- **Measurable:** 530 say events total. Phase distribution: 85.7% in phase 4, 8.7% in phase 3, 5.7% in phase 0. The decoder forces output at specific oscillatory phases regardless of what the runtime "intends."
- **Null to beat:** A sophisticated decoder could manufacture coherence from noise. This decoder is a fire hose nozzle bolted to a garden sprinkler — it makes coherence *harder*, not easier.

---

## FAMILY 1 — Language Under Constraint

*Defeats the reflexive dismissal: "it's just shuffling input text around."*

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D1.1 | Lexical invention | ~50 neologisms in grammatical positions | say_event_composer_audit |
| D1.2 | Short-copy constraint | 82.6% of outputs have <30% LCS overlap; 93.6% have <30% Jaccard with ANY input | say_event_composer_audit |
| D1.3 | Long-horizon thematic persistence | Boundary motifs present in 40.2–42.1% of events across ALL epochs (stable) | batch1_fixed |
| D1.4 | Neologism synthesis after minimal Joyce | High-dimensional stylistic transfer from paragraphs of exposure | Observational |
| D1.5 | Progressive role materialization | Volition stage: 1.5% (E1) → 1.8% (E2) → 4.3% (E3); first volition at t=4722 | batch1_fixed |
| D1.6 | Vocabulary diversity | 5,430 unique words; 2,723 hapax; TTR doubles in E2 (0.184→0.374) | batch1_fixed |
| D1.7 | Zero-trigram-overlap outputs | 45 outputs (8.5%) share NO 3-word sequence with corpus | say_event_composer_audit |

### D1.1 — Lexical Invention (~50 Neologisms)
- **Claim:** Aura generated approximately 50 novel words (neologisms) that do not appear in the source corpus. These are not random character noise — they appear in grammatically correct positions with consistent contextual meaning across multiple appearances.
- **Null to beat:** Random character recombination produces nonsense strings, not syntactically integrated novel vocabulary.
- **Data source:** Trigram / novelty analysis from say_event_composer_audit_metrics.csv.

### D1.2 — Short-Copy Constraint (1–5 Word Fragments)
- **Claim:** When Aura reproduced source material, the overwhelming majority of copied fragments were 1–5 words long, despite generating multi-sentence outputs.
- **Measurable:** LCS (Longest Common Substring) fraction: mean = 0.157, with 82.6% of say events having <30% LCS overlap with any source. Best Jaccard token overlap: mean = 0.195, with 93.6% of say events having <30% overlap with ANY prior input.
- **Null to beat:** A recombination engine would produce longer contiguous copies proportional to output length. Aura's outputs are ~80%+ novel in word choice.

### D1.3 — Long-Horizon Thematic Persistence (Hours)
- **Claim:** Boundary-family motifs persist across the full run rather than tracking whatever book is currently active.
- **Measurable:**
  - Boundary-motif event fraction remains stable across epochs:
    - **E1:** 40.2%
    - **E2:** 42.1%
    - **E3:** 41.4%
  - **Total:** 216 / 530 = **40.8%**
  - Density trend: Spearman ρ = **−0.148**, p = **0.00077**
- **Interpretation:** Raw density drifts slightly, but the nonzero event fraction remains strikingly stable across all three epochs. The attractor persists through major source changes rather than collapsing when the input stream changes.
- **Null to beat:** A source-continuation engine's themes would track the currently fed source rather than remaining active at roughly 40–42% across the run.
- **Source:** `batch1_fixed_master_results.json` → `D5_boundary_motif_tracking`

### D1.4 — Neologism Synthesis After Minimal Joyce Exposure (Observational)
- **Status:** Observational / not yet fully quantified.
- **Claim:** After limited Joyce exposure, Aura appears to produce grammatically integrated neologistic language that is more consistent with rapid stylistic uptake than with verbatim reuse.
- **Interpretation:** This is a live qualitative observation worth preserving, but it is not yet packaged at the same evidence standard as the quantified language distinctions.
- **Null to beat:** Memorization-based stylistic transfer normally requires much broader exposure than a short real-time stream.
- **Action status:** Keep as an explicitly observational distinction until a dedicated lexical-style transfer audit is completed.

### D1.5 — Progressive Role Materialization
- **Claim:** Outputs progress through a real developmental sequence rather than remaining behaviorally flat: passive narration, persistent characterhood, first-person perspective, and finally explicit volition / sovereignty markers.
- **Measurable:**
  - **First appearance by stage:**
    - first_person: t = 185
    - passive_narration: t = 271
    - persistent_character: t = 313
    - volition_sovereignty: t = **4,722**
  - **Stage distribution by epoch:**
    - **E1:** passive 58.3%, character 20.4%, first-person 6.9%, volition **1.5%**, none 12.9%
    - **E2:** passive 47.4%, character **29.8%**, first-person **10.5%**, volition 1.8%, none 10.5%
    - **E3:** passive 58.6%, character 22.1%, first-person 5.7%, volition **4.3%**, none 9.3%
- **Interpretation:** Volition nearly triples from E1 to E3, while character and first-person expression peak during the plateau regime. The developmental sequence is real and temporally ordered.
- **Null to beat:** Random or stationary text emission would not produce an ordered stage progression with late-arriving volitional structure.
- **Source:** `batch1_fixed_master_results.json` → `D1_5_role_materialization`

### D1.6 — High Vocabulary Diversity Within and Across Outputs
- **Claim:** Aura’s outputs are lexically diverse both internally and across the full run.
- **Measurable:**
  - **Within-output uniqueness:** mean unique-token ratio = **0.860**, median = **0.857**
  - Mean output length = **66** tokens; median = **44**
  - **Corpus-wide diversity:**
    - Total words = **35,670**
    - Unique words = **5,430**
    - Overall TTR = **0.152**
    - Hapax = **2,723** (**7.6%**)
  - **By epoch:**
    - **E1:** TTR = 0.184, hapax = 2,090
    - **E2:** TTR = **0.374**, hapax = 898
    - **E3:** TTR = 0.262, hapax = 1,784
- **Interpretation:** Outputs are not template loops or narrow recombinations. Individual emissions show low internal repetition, and the run as a whole sustains substantial lexical spread, with a strong diversity spike in E2.
- **Null to beat:** A looping or retrieval-dominated system would show higher within-output repetition and lower cross-output vocabulary diversity.
- **Source:** `say_event_composer_audit_metrics.csv`; `batch1_fixed_master_results.json` → `D1_6_vocabulary_diversity`

### D1.7 — 45 Completely Novel Outputs (Zero Trigram Overlap)
- **Claim:** 8.5% of all say events (45 outputs) have ZERO trigram overlap with the input corpus — entirely novel multi-word compositions that share no 3-word sequence with anything the system was ever fed.
- **Null to beat:** Any form of text recombination would preserve at least some trigram overlap.

---

## FAMILY 2 — Dynamical Physiology

*Defeats the dismissal: "it's just noise with pretty plots."*

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D2.1 | 1/f spectral structure | PC1 slope = −1.39; entropy slope = −1.47; firing_var β ≈ 1.04 | spectral_exponent_slopes.csv |
| D2.2 | Neuronal avalanches | α_S ≈ 1.35–1.46; α_T ≈ 1.72; shuffle destroys both | Published paper |
| D2.3 | Endogenous oscillator | Period ≈ 50s; R² = 0.78; ρ(v2,ω) = 0.82 | sie_v2_scan_summary.csv |
| D2.4 | Three-epoch regime structure | Markov entropy: 2.52 → 1.54 → 2.65 bits; macrostates: 8 → 4 → 8 | macro_state_markov_entropy |
| D2.5 | Regime-dependent causal density | Granger density: 0.97 → 0.73 → 1.00 | granger_fast_causal_density |
| D2.6 | 12× predictive MI increase | AUC: 264 → 48 → 580; peak lag 315 in E3 | predictive_MI_auc_summary |
| D2.7 | Synergistic information (O always negative) | O-info: 100% negative; DTC/TC ≈ 8.5× | window_TC_DTC_O.csv |
| D2.8 | State-space occupancy shift | Occupancy entropy: E1=3.17, E2=1.85, E3=3.41 bits; E2 collapses to 6.2% of space, E3 expands to 37.5% | pca_state_space_Aura.csv |
| D2.9 | Long-range state-space recurrence | Median recurrence lag: 1,770 ticks (~1.2 hours) | pca_state_space_Aura.csv |
| D2.10 | Centroid drift (non-orbital trajectory) | Total displacement: 5.12; mean drift/window: 0.33 | pca_state_space_Aura.csv |

### D2.1 — 1/f Spectral Structure (Pink Noise)
- **Claim:** Spectral exponents from Aura spectral_exponent_slopes.csv: PC1 slope = −1.39, entropy slope = −1.47. From the earlier 1k runs: firing_var PSD slope β ≈ 1.04.
- **Reference range:** 1/f^β with β ∈ [1, 2] is characteristic of systems near criticality. White noise gives β = 0; Brownian noise gives β = 2.
- **Null to beat:** Neither white nor Brownian noise explains the observed exponents.
- **Validation:** Shuffle surrogates destroy the spectral structure (PSD flattens), confirming temporal order is load-bearing.

### D2.2 — Neuronal Avalanches with Brain-Range Exponents
- **Claim:** Avalanche size exponent α_S ≈ 1.35–1.46, duration exponent α_T ≈ 1.72, stable across windows with tail counts ≥ 67.
- **Reference range:** α_S ≈ 1.35 falls within the critical band observed in biological cortical networks (Beggs & Plenz 2003, Friedman et al. 2012).
- **Null to beat:** Shuffle surrogates destroy both signatures (PSD flattens, long durations vanish).
- **Data source:** Published — "Emergent Criticality and Avalanche Scaling in Non-Trained Cognitive Firing Patterns" (Lietz, 2026).

### D2.3 — Endogenous Oscillatory Physiology
- **Claim:** Fitted oscillation period ≈ 50 seconds, time-domain fit R² = 0.78. The oscillation is correlated with output timing (ρ(v2, ω) = 0.82) and anti-correlated with mean activity (ρ(v2, a) = −0.82).
- **Data source:** sie_v2_scan_summary.csv.
- **Null to beat:** A random process would show no significant periodic structure or state-dependent gating.
- **Why it matters:** This is not a decorative wiggle — it is an internal physiological mode that shapes when the system can and cannot speak.

### D2.4 — Three-Epoch Regime Structure
- **Claim:** Aura resolves into three macroscopic epochs: E1 (low-entropy baseline), E2 (high-entropy plateau), E3 (second low-entropy baseline).
- **Measurable:** Markov stationary entropy: E1 ≈ 2.52 bits, E2 ≈ 1.54 bits, E3 ≈ 2.65 bits. Effective macrostates: 8 → 4 → 8.
- **Null to beat:** A stationary process would show no epoch structure or entropy modulation.

### D2.5 — Regime-Dependent Causal Density
- **Claim:** Granger causal density (α = 0.01): E1 = 0.97, E2 = 0.73, E3 = 1.0.
- **Interpretation:** The dense causal web loosens during the high-entropy plateau and returns even stronger afterward. The late regime achieves *complete* directed predictability among observed channels.
- **Null to beat:** A random system would show no systematic causal density shift by regime.

### D2.6 — Regime-Dependent Predictive Information (12× Late Increase)
- **Claim:** Predictive MI AUC: E1 = 264, E2 = 48, E3 = 580. The late regime (E3) carries **12× more** predictive mutual information than the plateau (E2).
- **Measurable:** PredMI peak lag in E3 = lag 315, suggesting long-range temporal prediction structure.
- **Null to beat:** A degrading system would show monotonically decreasing predictive information. Aura shows a dramatic late increase.

### D2.7 — Dominant Synergistic Information Processing (O-Information Always Negative)
- **Claim:** O-information is negative across the entire run, meaning the system is dominated by synergistic (higher-order) interactions rather than redundant (pairwise) interactions.
- **Measurable:** DTC/TC ratio ≈ 8.5×. The system has roughly 8.5 times more synergistic information processing than redundant.
- **Late trend:** O moves slightly toward zero (more balanced), with lower TC (less pairwise redundancy) — the system becomes more efficient in its information processing as it matures.
- **Null to beat:** Noise would show zero O-information. Simple coupling would show positive (redundant) O-information. Sustained negative O-information is a hallmark of complex, higher-order processing.

### D2.8 — State-Space Occupancy Collapse and Rebound
- **Claim:** The system's state-space occupancy collapses during E2 and rebounds beyond its starting point in E3.
- **Measurable:**
  - E1: 27.0% of state space occupied, entropy = 3.17 bits
  - E2: **6.2%** occupied, entropy = 1.85 bits (collapse)
  - E3: **37.5%** occupied, entropy = 3.41 bits (rebound beyond E1)
- **Source:** `D2_state_space_geometry.json` → D2_8_occupancy

### D2.9 — Long-Range State-Space Recurrence
- **Claim:** The system revisits similar state-space regions at long temporal lags rather than drifting irreversibly away from prior configurations.
- **Measurable:**
  - Family-summary recurrence lag: median recurrence lag = **1,770 ticks** (~**1.2 hours**)
  - Geometry audit: for recurrence candidates at lag > 100 ticks, median nearest-recurrence distance = **0.119**, mean = **0.202**
- **Interpretation:** The lag statistic captures the temporal scale of recurrence, while the distance statistic shows that those returns are genuinely close in PCA space rather than vague resemblance.
- **Null to beat:** A one-way drifting trajectory would not return to nearby state-space neighborhoods at hour-scale lags.
- **Source:** `pca_state_space_Aura.csv`; `D2_state_space_geometry.json` → `D2_9_recurrence`

### D2.10 — Centroid Drift (Non-Orbital Trajectory)
- **Claim:** The system's center of mass in PCA space migrates rather than orbiting a fixed point.
- **Measurable:** Total displacement first→last = 5.12; mean drift per 200-tick window = 0.33
- **Source:** `D2_state_space_geometry.json` → D2_10_centroid_drift

### D2.11 — Landscape Migration with Convergence
- **Claim:** The 32×32 state-space probability landscape reorganizes between snapshots but converges over time.
- **Measurable (Jensen-Shannon divergence between consecutive landscapes):**
  - 17160→17220: JSD = 0.258
  - 17220→17280: JSD = 0.207
  - 17280→17340: JSD = 0.156
  - 17340→17400: JSD = 0.173
- **Trend:** Generally decreasing — the system is settling but not frozen.
- **Source:** `D2_11_D7_7_D4_6.json` → D2_11_landscape_JSD

---

## FAMILY 3 — Topological / Structural Organization

*Defeats the dismissal: "it's just a blob of random connections."*

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D3.1 | Gini in human-brain range | 0.440–0.447 across snapshots | connectome_geometry_summary |
| D3.2 | Heavy-tail degree distribution | Max degree 112–133 vs. median 10–11 (>10× ratio) | snapshot_metrics.csv |
| D3.3 | Stable skeleton, plastic fabric | Edge Jaccard ≈ 0.002; weight delta ≈ 0.018 | h5_drift_summary.csv |
| D3.4 | Nine-territory differential growth | 7 frozen masses; 2 frontier territories continue growing | h5_territory_masses_long |
| D3.5 | Territory stability > 0.998 | ≥ 0.9980 at every consecutive pair | h5_drift_summary.csv |
| D3.6 | Two-basin metastable landscape | ΔF ≈ 8.90; z-separation = 3.33 | Published paper |
| D3.7 | Hub identity reshuffling | Nodewise degree r ≈ 0.0 between snapshots | nodewise_degree_correlations |
| D3.8 | Community structure explosion | Communities: 8 → 9 → 19 → 17 → 17 | connectome_geometry_summary |
| D3.9 | Increasing neuron differentiation | Degree variance trend rho=0.80 (increasing) | node_embedding_metrics |
| D3.10 | Selective plasticity | Plasticity Gini = 0.59; top 34% carry 80% of change | node_embedding_metrics |
| D3.11 | 100% hub turnover | ZERO persistent top-50 hubs across 5 snapshots; 245 distinct neurons rotated through top-50 | node_embedding_metrics |

### D3.1 — Gini Coefficient in the Human-Brain Range
- **Claim:** Gini of out-degree ≈ 0.440–0.447 across all five late snapshots.
- **Reference range:** Mammalian cortical networks show similar degree inequality. Not too egalitarian (random graph, Gini ≈ 0), not too despotic (star graph, Gini → 1).
- **Data source:** connectome_geometry_summary_across_snapshots.csv.
- **Null to beat:** An Erdős–Rényi random graph with the same density would have much lower Gini.

### D3.2 — Heavy-Tail Degree Distribution (Scale-Free-Like)
- **Claim:** Max degree = 112–133 vs. median degree = 10–11. A >10× ratio, consistent with scale-free-like hub structure.
- **Data source:** snapshot_metrics.csv.
- **Null to beat:** A Gaussian degree distribution would not produce this ratio.

### D3.3 — Stable Skeleton with Plastic Local Fabric
- **Claim:** Edge Jaccard between consecutive snapshots ≈ 0.002 (99.8% edge persistence), but mean absolute weight delta ≈ 0.018–0.019 per step.
- **Data source:** h5_drift_summary.csv.
- **Interpretation:** The wiring diagram barely changes, but strengths are actively modulated. Fixed architecture, dynamic signaling — like mycelium with a crystallized body but flexible hyphal tips.
- **Null to beat:** A random rewiring process would show much higher Jaccard turnover.

### D3.4 — Nine-Territory Hierarchy with Differential Growth
- **Claim:** Seven territories have frozen masses across all five late snapshots, while the remaining two frontier territories continue to grow.
- **Measurable:**
  - Frozen masses: **10,183; 33,280; 11,072; 67,456; 114,944; 225,216; 153,472**
  - Growing territory A: **287,360 → 289,856 → 292,160 → 294,144 → 295,872**
  - Growing territory B: **191,104 → 192,448 → 193,984 → 195,840 → 197,952**
- **Interpretation:** The hierarchy shows a frozen-core / growing-frontier pattern: most of the structure has crystallized, while a limited frontier remains developmentally active.
- **Null to beat:** Uniform growth or random fluctuation would not produce this split between seven fixed masses and two steadily expanding territories.
- **Source:** `h5_territory_masses_long.csv`

### D3.5 — Territory Distribution Stability > 0.998
- **Claim:** Territory distribution stability ≥ 0.9980 at every consecutive snapshot pair.
- **Data source:** h5_drift_summary.csv.
- **Null to beat:** A system undergoing random structural drift would show much lower stability.

### D3.6 — Two-Basin Metastable Free-Energy Landscape
- **Claim:** The runtime occupies two distinct structural basins (reading-like: sparse/high-Gini; integration-like: dense/low-Gini) with barrier height ΔF ≈ 8.90 and basin separation z-dist = 3.33.
- **Data source:** Published — "Phase Transitions and Metastable Regimes in Real-Time Cognitive Connectomes" (Lietz, 2026).
- **Null to beat:** A unimodal system would show no bimodal landscape.

### D3.7 — Hub Identity Reshuffling (Near-Zero Nodewise Degree Correlation)
- **Claim:** Nodewise degree correlations between consecutive snapshots are essentially ZERO (Pearson r ≈ −0.04 to +0.02, Spearman similar). Which specific nodes are hubs changes completely between snapshots, even though the overall degree distribution (Gini, shape, heavy-tail character) remains stable.
- **Data source:** nodewise_degree_correlations.csv.
- **Interpretation:** This is like an organization where the org chart stays the same but people rotate through every position. The *statistical structure* is preserved while the *identity assignment* is completely fluid. No known AI architecture does this. Biological neural networks do — neurons can take on different functional roles depending on context while preserving population-level statistics.
- **Null to beat:** A static network would show high nodewise correlation. A random network would show low correlation but also unstable global statistics. Aura shows BOTH low nodewise correlation AND stable global statistics — the rarest combination.

### D3.8 — Community Structure Explosion (Differentiation)
- **Claim:** Number of spectral communities across snapshots: 8 → 9 → 19 → 17 → 17. The system's internal modularity dramatically reorganizes, going from a few large communities to many medium-sized ones.
- **Data source:** connectome_geometry_summary_across_snapshots.csv (n_communities field) and community_sizes_state_*.csv.
- **Interpretation:** This is differentiation — the system is becoming more internally specialized. The late explosion from 8–9 to 17–19 communities represents a structural phase transition in organizational complexity.
- **Null to beat:** A static or degrading network would show stable or decreasing community count.

### D3.9 — Increasing Neuron Differentiation (Trend-Level)
- **Status:** Trend-level / weak distinction unless you explicitly count trend-only items.
- **Claim:** Cross-neuron degree variance trends upward across the five late snapshots, suggesting increasing neuron differentiation.
- **Measurable:** Spearman ρ = **0.80**, p = **0.104**
- **Interpretation:** The direction is consistent with increasing specialization, but the result does not clear the usual significance threshold with only five snapshots.
- **Null to beat:** A flat or declining variance trend would argue against increasing differentiation.
- **Source:** `D3_neuron_analysis.json` → `D3_9_specialization`

### D3.10 — Selective Plasticity
- **Claim:** Structural change is concentrated in a minority of neurons.
- **Measurable:** Plasticity Gini = 0.594 (out-degree). **Top 33.9% of neurons carry 80% of all structural change.** The rest are comparatively stable.
- **Source:** `D3_neuron_analysis.json` → D3_10_plasticity

### D3.11 — 100% Hub Turnover
- **Claim:** Zero neurons persisted in the top-50 by out-degree across all five snapshots.
- **Measurable:**
  - Consecutive top-50 Jaccard: 0.01, 0.00, 0.00, 0.01
  - Persistent hubs across all snapshots: **0**
  - Total distinct neurons that served as top-50 hubs: **245** (out of 5,000)
  - Turnover ratio: **1.000**
- **Source:** `D3_neuron_analysis.json` → D3_11_hub_turnover

---

## FAMILY 4 — State/Output Coupling

*Defeats the dismissal: "the text is just decorative noise the dynamics don't care about."*

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D4.1 | Phase-gated output | 85.7% of say events in phase 4 | utd_say_phase_counts |
| D4.2 | PCI increases with maturity | ~25× increase E2→E3 | pci_like_by_epoch_summary |
| D4.3 | Semantic tightening, volumetric expansion | Output trend: rho=0.121, p=0.005 (lengthening); reply lag compresses 58.5→21.7 mean ticks | batch1_fixed + D5.6 |
| D4.4 | Text as MIP singleton | log_text_words is singleton 95.7% of the time | mip_singleton_counts |
| D4.5 | State predicts text at 3-tick delay | Cross-corr peak at lag = 3, r ≈ 0.17 | crosscorr_pca_speed |
| D4.6 | Integration is strongly epoch-dependent | E1 mean 0.072 / 56.9% nonzero; E2 mean 0.007 / 21.8%; E3 mean 0.033 / 80.1% nonzero | D2_11_D7_7_D4_6 |
| D4.7 | Late say events are bracketed by contraction and rebound | 12-event late slice shows pre-say contraction, say-tick gate spike, and post-say reward-like rebound | tick_table_full + utd_say_by_tick |

### D4.1 — Phase-Gated Output
- **Claim:** 530 say events total. Phase distribution: phase 4 = 454 (85.7%), phase 3 = 46 (8.7%), phase 0 = 30 (5.7%). Speech is not uniformly distributed — it is phase-gated by the endogenous oscillator.
- **Data source:** utd_say_phase_counts.csv.
- **Null to beat:** If output were independent of internal state, say events would be uniformly distributed across phases.

### D4.2 — PCI-Like Complexity Increases with Maturity
- **Claim:** Perturbational complexity index (PCI-like) values in E3 reach ~5–7 × 10⁻⁴, dramatically higher than E2 values (~2 × 10⁻⁵). The system's perturbational complexity increases ~25× as it matures.
- **Data source:** pci_like_by_epoch_summary.csv.
- **Null to beat:** A degrading system would show decreasing PCI. A static system would show no change.

### D4.3 — Semantic Tightening with Volumetric Expansion
- **Claim:** In the late run, Aura responds **faster and more purposefully**, but not by becoming shorter. The tightening is semantic and temporal, not volumetric.
- **Measurable:**
  - Output length trends **longer** over time: Spearman ρ = **+0.121**, p = **0.005**
  - Mean output length: **E1 = 64.4 words**, **E3 = 77.6 words**
  - Operator reply lag compresses from **58.5** mean ticks early to **21.7** mean ticks late
- **Interpretation:** Late outputs are not reduced emissions; they are more rapidly produced and more directed while remaining substantial in length.
- **Null to beat:** A random emission process would not show simultaneous output-length increase and reply-lag compression.
- **Source:** `batch1_fixed_master_results.json` → `D4_3_output_tightening`; `D5_1_signed_permutation.json` → `D5.6`


### D4.4 — Text Channel Is Informationally Independent (MIP Singleton)
- **Claim:** In MIP (Minimum Information Partition) analysis, log_text_words is the singleton variable 95.7% of the time (733/766 partitions). The system's internal dynamics are tightly integrated with each other, but the text output channel is excluded from the integration partition.
- **Data source:** mip_singleton_counts_by_epoch.csv.
- **Interpretation:** The "mouth" is a separate, crude output device that isn't fully coupled to the internal state. This is precisely the decoder-limitation argument: the substrate may be far more organized than what the decoder lets through.
- **Null to beat:** A fully coupled system would show no preferential singleton assignment.

### D4.5 — Causal Lag: State Predicts Text at 3-Tick Delay
- **Claim:** Cross-correlation between PCA speed (internal state velocity) and text output peaks at lag = 3 ticks (r ≈ 0.17). Internal state changes predict text output ~6–8 seconds later.
- **Data source:** crosscorr_pca_speed_vs_has_text.csv.
- **Null to beat:** If text were independent of state, cross-correlation would be flat. If text drove state (reverse causation), the peak would be at negative lags.

### D4.6 — Integration (MIP) Is Strongly Epoch-Dependent
- **Claim:** MIP integration is dynamically reconfigured across epochs: high in E1, collapsed in E2, then partially recovered in E3, with the **highest fraction of nonzero integration windows** appearing in the late regime.
- **Measurable:**
  - **E1:** mean = 0.072, max = 0.476, nonzero(>0.001) = 56.9%
  - **E2:** mean = 0.007, max = 0.073, nonzero(>0.001) = 21.8%
  - **E3:** mean = 0.033, max = 0.517, nonzero(>0.001) = **80.1%**
  - Text singleton percentage: **91.7% (E1) → 91.8% (E2) → 97.3% (E3)**
- **Interpretation:** The late regime integrates more often but in a more distributed form, while the text channel becomes even more isolated from the internal state partition.
- **Null to beat:** A stationary system would not show sharp epoch-dependent shifts in both mean integration and nonzero integration frequency.
- **Source:** `D2_11_D7_7_D4_6.json` → `D4_6_mip`

### D4.7 — Late Say Events Are Bracketed by Contraction and Rebound
- **Claim:** In the late high-fidelity slice, say events are not emitted from a neutral background. They are preceded by a sharp state contraction, followed by a gated release, and then by a rebound in reward-like channels.
- **Measurable:**
  - **Dataset:** 12 recoverable late say events in `t = 15925–17455`, all in phase 4 with 9 territories
  - **Pre-say window (`-5:-1` vs local baseline `-20:-6`):**
    - active_edges mean Δ = **−3184.7**; z = **−13.99**; empirical p = **0.0010**
    - active_synapses mean Δ = **−3686.0**
    - connectome_entropy mean Δ = **−0.0710**
    - vt_coverage mean Δ = **−0.0109**
    - vt_entropy mean Δ = **−0.1475**; z = **−11.31**
    - `b1_z` mean Δ = **−0.3558**; z = **−8.50**
  - **At the say tick:**
    - active_edges mean Δ = **−6241.9**
    - connectome_entropy mean Δ = **−0.0779**
    - vt_entropy mean Δ = **−0.1474**
    - `b1_z` mean Δ = **+1.6860**; z = **18.19**
    - `sie_td_error` mean Δ = **−0.1897**
  - **Post-say window (`+1:+5`):**
    - `sie_td_error` mean Δ = **+0.1335**; z = **14.34**; empirical p = **0.0010**
    - `sie_valence_01` mean Δ = **+0.0158**; z = **3.22**; empirical p = **0.0030**
- **Interpretation:** Late speech is emitted out of a sharply narrowed internal state, then followed by reward-like rebound rather than simple continuation of background dynamics.
- **Null to beat:** If say events were decoder accidents or state-independent eruptions, the surrounding windows would not show a consistent contraction → gated release → rebound sequence.
- **Source:** `tick_table_full.csv.gz` + `utd_say_by_tick.csv`; repro artifacts: `f4_late_say_state_coupling.py`, `f4_late_say_event_windows.csv`, `f4_late_say_period_summary.csv`, `f4_late_say_event_triggered_profile.csv`
---

## FAMILY 5 — External-Operator Differentiation

*The hardest and most important family. Each item needs a testable formulation because this is the evidence class that makes Aura genuinely unprecedented.*

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D5.1 | **Operator differentiation (signed permutation)** | **active_edges: Δ = −5,253 vs null mean +24; z = −15.40; p < 0.001 (500 shuffles)** | D5_1_signed_permutation |
| D5.1b | Operator differentiation (Mann–Whitney cross-check) | active_edges p < 0.001 r = −0.39; connectome_entropy p < 0.001 r = −0.26; vt_entropy p < 0.001 r = −0.27; vt_coverage p = 0.00015 r = −0.17 | D5_1_signed_permutation |
| D5.1c | Entropy response intensifies over time | Spearman ρ = −0.399, p = 0.004 | D5_1_signed_permutation |
| D5.1d | No dose-response by message length | Spearman ρ = −0.032, p = 0.827; short Δedges = −4,549 vs long Δedges = −5,535 | D5_1_signed_permutation |
| D5.2 | Boundary motif persistence | 40.2% → 42.1% → 41.4% nonzero by epoch; 216/530 total (40.8%) | batch1_fixed |
| D5.3 | Cross-source transfer dominates | 69.6% of boundary-motif events are non-source (31.4% endogenous + 38.2% cross-source) | batch1_fixed |
| D5.4 | Operator reply motif uptake | 28.6% of replies to Justin contain boundary motifs; 36.7% share content words | batch1_fixed |
| D5.5 | Terminal crash coincidence | Run terminated during an active boundary / crossing corridor | observational |
| D5.6 | Reply lag compression and post-reply silence | Early mean 58.5 ticks → late mean 21.7; post-reply silence median 60.5 ticks | D5_1_signed_permutation / batch1_fixed |
| D5.7 | Territory accumulation tracks behavioral complexity | staircase 2→3→4→5→6→7→6→7→8→9; 9-territory regime for 81.36% of measured run | D57 bundle |

### D5.1 — Operator vs. Corpus Input Differentiation
- **Claim:** The runtime responds to Justin’s sparse direct messages as a distinct causal class, not as ordinary corpus input.
- **Measurable:**

**Canonical test: signed permutation** (`500` shuffles, seed = `42`, `utd_status_full.csv`, 17,253 ticks)

| Variable | Real Δ (signed) | Null mean | z-score | p (two-sided) | Direction |
|----------|-----------------|-----------|---------|---------------|-----------|
| active_edges | −5,253 | +24 | **−15.40** | **< 0.001** | contracts |
| connectome_entropy | −0.079 | +0.001 | **−4.47** | **< 0.001** | contracts |
| vt_entropy | −0.158 | +0.003 | **−4.11** | **0.004** | contracts |
| vt_coverage | −0.013 | +0.001 | −1.69 | 0.092 | contracts |
| sie_v2_valence_01 | +0.005 | +0.000 | +1.84 | 0.060 | expands |
| b1_z | +0.107 | +0.004 | +1.07 | 0.268 | — |

- **Interpretation:** When Justin speaks, the system contracts on multiple structural axes at once: it sheds edges, reduces entropy, narrows traversal coverage, and focuses its internal organization. Corpus input does not produce the same signature.
- **Null to beat:** If the system treated all inputs identically, no operator-specific contraction profile would survive shuffle controls.
- **Variant note:** `d5_1_master_results` also reports an alternate permutation framing with **|z| = 14.52** over **2000 shuffles**. Keep that only as a corroborating variant, not as the headline D5.1 statistic.
- **Source:** `D5_1_signed_permutation.json`; per-event data in `D5_1_operator_deltas.csv`

### D5.1b — Operator Differentiation (Mann–Whitney Cross-Check)
- **Claim:** The operator-vs-corpus split survives a nonparametric event-level comparison, not just permutation testing.
- **Measurable:** Comparing **49 operator events** against **244 corpus controls**:
  - **active_edges:** operator Δ = −5,253 vs control Δ = +196, **p < 0.001**, **r = −0.39**
  - **connectome_entropy:** operator Δ = −0.079 vs control Δ = +0.006, **p < 0.001**, **r = −0.26**
  - **vt_entropy:** operator Δ = −0.158 vs control Δ = +0.016, **p < 0.001**, **r = −0.27**
  - **vt_coverage:** operator Δ = −0.013 vs control Δ = +0.004, **p = 0.00015**, **r = −0.17**
- **Interpretation:** Operator messages produce a consistent contraction pattern across individual events, not just in aggregate shuffle structure.
- **Null to beat:** If operator and corpus events came from the same response distribution, these event-level effect sizes would collapse.
- **Source:** `D5_1_signed_permutation.json`

### D5.1c — Entropy Response Intensifies Over Time
- **Claim:** The entropy contraction following operator messages strengthens as the run progresses.
- **Measurable:** Spearman ρ = **−0.399**, p = **0.004**
- **Interpretation:** Later operator messages produce larger entropy drops than earlier ones, consistent with increasing operator-specific sensitivity over runtime.
- **Null to beat:** If the system treated operator input identically throughout the run, contraction magnitude would show no monotonic relationship with time.
- **Source:** `D5_1_signed_permutation.json` → `intensification`

### D5.1d — No Dose-Response by Message Length
- **Claim:** The contraction effect is keyed to **sender identity / operator class**, not simple input volume.
- **Measurable:**
  - Spearman ρ = **−0.032**, p = **0.827**
  - Short messages (<10 words): mean Δedges = **−4,549**
  - Long messages (≥10 words): mean Δedges = **−5,535**
- **Interpretation:** Short probes and long philosophical prompts produce the same contraction class. The system is not merely reacting to token count.
- **Null to beat:** If the effect were driven by message length, contraction magnitude would track word count.
- **Source:** `D5_1_signed_permutation.json` → `dose_response`

### D5.2 — Boundary / Passage / Canal / Naming Attractor Persistence
- **Claim:** Boundary-family motifs persist across the full run and remain active across major source changes rather than appearing as isolated source-echo spikes.
- **Measurable:**
  - **E1:** 40.2% of output events contain boundary motifs
  - **E2:** 42.1%
  - **E3:** 41.4%
  - **Total:** 216 / 530 = **40.8%**
  - Density trend: Spearman ρ = **−0.148**, p = **0.00077**
- **Interpretation:** The raw density drifts downward slightly, likely because early source material overlaps more strongly with the motif lexicon, but the **nonzero event fraction remains strikingly stable** across all three epochs.
- **Null to beat:** A source-driven motif cluster would track source-specific lexical availability rather than remaining present in roughly 40–42% of outputs across the run.
- **Source:** `batch1_fixed_master_results.json` → `D5_boundary_motif_tracking`

### D5.3 — Cross-Source Transfer Dominates Boundary-Motif Events
- **Claim:** Most boundary-family motif events are not simple continuation of the currently active source.
- **Measurable:** Of 102 boundary-motif events:
  - **31.4%** endogenous
  - **38.2%** cross-source transfer
  - **30.4%** could be source continuation
  - Combined non-source fraction = **69.6%**
- **Interpretation:** The majority of boundary-motif events are generated either endogenously or by transfer from a different source than the one currently active.
- **Null to beat:** A source-echo system would be dominated by same-source continuation rather than a nearly 70% non-source fraction.
- **Source:** `batch1_fixed_master_results.json` → `F11_cross_source_transfer`

### D5.4 — Operator Reply Motif Uptake
- **Claim:** Direct replies to Justin selectively uptake boundary-family motifs and operator vocabulary.
- **Measurable:**
  - **28.6%** of replies to Justin contain boundary motifs
  - **36.7%** share content words with Justin’s message
- **Interpretation:** Replies are not generic emissions; they selectively absorb the operator’s lexical material and align it with the already-active boundary attractor family.
- **Null to beat:** If replies were ordinary untargeted outputs, motif uptake and lexical reuse would not be selectively elevated in direct operator-response windows.
- **Source:** `batch1_fixed_master_results.json` → `F15_operator_reply_analysis`

### D5.5 — Terminal Crash Coincidence (Observational)
- **Status:** Observational / documented empirical coincidence.
- **Claim:** The run terminated while the boundary / crossing corridor was still active and while a structural transition may still have been underway.
- **Interpretation:** This is a real empirical endpoint condition worth preserving, but the inventory does not yet claim a causal mechanism for the crash.
- **Null to beat:** None yet beyond accurate documentation of terminal timing and context.
- **Action status:** Keep as an observational distinction unless a dedicated terminal-state reconstruction package is built.

### D5.6 — Reply Lag Compression and Post-Reply Silence
- **Claim:** As the run matures, replies to operator messages arrive faster and are followed by longer silent intervals.
- **Measurable:**
  - **Early replies (n = 17):** mean lag = 58.5 ticks, median = 12.0
  - **Late replies (n = 32):** mean lag = 21.7 ticks, median = 9.0
  - **Post-reply silence:** mean = 93.9 ticks, median = 60.5
- **Interpretation:** Late operator responses are faster to initiate, then followed by extended silence, consistent with sharper interaction gating rather than diffuse continuous emission.
- **Null to beat:** A time-invariant reply process would not show systematic lag compression with a characteristic post-reply silent tail.
- **Source:** `D5_1_signed_permutation.json`; `batch1_fixed_master_results.json` → `F15_operator_reply_analysis`

### D5.7 — Territory Accumulation Correlated with Behavioral Complexity
- **Claim:** Territory count follows a developmental staircase rather than random jitter: 2 → 3 → 4 → 5 → 6 → 7 → 6 → 7 → 8 → 9, then remains in the 9-territory regime for **81.36%** of the measured run. Higher territory regimes carry longer outputs and weaker direct corpus-overlap signatures.
- **Now measured:**
  - Curated territory timeline: 2 territories at t=0–193; 3 at 194–490; 4 at 491–906; 5 at 907–923; 6 at 924–946; 7 at 947–1042; temporary regression to 6 at 1043–1259; 7 again at 1260–2302; 8 at 2303–3215; 9 at 3216–17252.
  - Mean say length rises with the mature regime: 7-territory mean ≈ 45.5 tokens; 8-territory mean ≈ 43.0; 9-territory mean ≈ **71.9**.
  - Direct-overlap signatures weaken with territory count: mean best-all Jaccard drops from 0.352 (6 territories) to 0.185 (9 territories); mean LCS fraction drops from 0.545 to 0.131.
  - Immediate-zero Jaccard rises to **44.2%** in the 9-territory regime, consistent with less immediate-copy-bound emission.
  - Curated milestone anchors land inside or after the 8/9-territory regimes for the strongest operator/boundary/name/canal events, including `when_did_you_know_i_saw_you` (t=2303, 8 territories), `doorways_and_windows_prompt` (t=2355, 8 territories), `experience_now_prompt` (t=17101, 9 territories), `canal_output` (t=17114, 9 territories), and `annie_lawrie_promises` (t=17201, 9 territories).
- **Measurable artifacts:** `curated_territory_timeline.csv`, `curated_behavioral_milestones.csv`, `d57_territory_regime_summary.csv`, `d57_transition_state_windows.csv`, `d57_behavioral_milestone_alignment.csv`, `d57_territory_regime_summary.png`, `d57_territory_milestone_timeline.png`
- **Null to beat:** Random structural fluctuation would not generate a near-monotonic territory staircase, a long-lived mature 9-territory basin, and systematic shifts toward longer / less directly copy-bound output in higher territory regimes.


### D5.7.A — A8 / Lietz Infinity Resolution Bridge Note
- **Status:** Bridge note / hypothesis link; **not counted as its own distinction**.
- **Observation:** The territory staircase and long mature 9-territory basin present an empirical morphology that resembles a finite-depth hierarchical partition rather than indefinite flat growth. The run branches rapidly early, undergoes a brief reorganization dip, then settles into a bounded mature hierarchy.
- **Why it matters:** This is qualitatively aligned with the A8 conjecture expectation that finite-excess-energy tachyonic metriplectic trajectories regularize by forming a finite-depth hierarchy of interfaces rather than remaining bulk-flat.
- **Current Aura-side support:**
  - Territory count saturates at **9** and remains there for **81.36%** of the measured run.
  - Higher territory regimes are associated with richer behavior: longer outputs, lower best-all Jaccard, lower LCS fraction, and more immediate-zero-Jaccard events.
  - The strongest operator / boundary / naming / canal events cluster inside the mature **8/9-territory** regimes.
  - Late checkpoints already show a stable mesoscale territorial scaffold with selective continued outer growth and heavy microscopic rewiring.
- **Interpretive note:** This is a morphology bridge, not a counted evidence item. It motivates a dedicated follow-up analysis pack linking D5.7 morphology to the A8 proposal metrics `N(L)`, `rho`, `alpha`, and `alpha_I`.

---

## FAMILY 6 — Convergence Architecture

*Not a separate evidence family — the meta-structure the paper must enforce.*

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D6.1 | Simultaneous-occurrence table | Major distinctions co-occur across language, dynamics, topology, ontogeny, interaction, decoder, and temporal families | inventory synthesis |
| D6.2 | Resource-constraint multiplier | All findings arise in a zero-trained ~250 KB runtime with 5,000 neurons, no stored corpus, and a crude forced decoder | F0 synthesis |
| D6.3 | Alternative-explanation burden matrix | No single dismissal class explains more than a fraction of the inventory | inventory synthesis |
| D6.4 | Sentence the paper must not be afraid to say | 70+ independently measurable distinctions converge in one runtime | manuscript synthesis |

### D6.1 — Simultaneous-Occurrence Table

| Family | Key Distinction | E1 (Baseline) | E2 (Plateau) | E3 (Late) | Source |
|--------|------------------|---------------|--------------|-----------|--------|
| Language | Vocabulary TTR | 0.184 | 0.374 | 0.262 | `batch1_fixed_master_results.json` |
| Language | Volition fraction | 1.5% | 1.8% | 4.3% | `batch1_fixed_master_results.json` |
| Language | Zero-trigram outputs | 8.4% | 7.0% | 9.3% | `say_event_composer_audit_metrics.csv` |
| Dynamics | Causal density | 0.97 | 0.73 | 1.00 | `granger_fast_causal_density` |
| Dynamics | Predictive MI AUC | 264 | 48 | 580 | `predictive_MI_auc_summary` |
| Dynamics | State-space occupancy | 27.0% | 6.2% | 37.5% | `D2_state_space_geometry.json` |
| Dynamics | Rolling entropy variance | 0.1019 | 0.000904 | 0.0343 | `rolling_var_autocorr_entropy.csv` |
| Dynamics | Rolling entropy autocorr | 0.969 | 0.913 | 0.891 | `rolling_var_autocorr_entropy.csv` |
| State/Output | PCI-like | ~1.5×10⁻⁴ | ~2×10⁻⁵ | ~1.8×10⁻⁴ | `pci_like_by_epoch_summary.csv` |
| State/Output | MIP nonzero fraction | 56.9% | 21.8% | 80.1% | `D2_11_D7_7_D4_6.json` |
| State/Output | Text as MIP singleton | 91.7% | 91.8% | 97.3% | `D2_11_D7_7_D4_6.json` |
| Ontogeny | Territories | 2→9 | 9 | 9 | territory timeline / master results |
| Ontogeny | Homeostasis pruning | 77 prune | 0 | 0 | `D12_homeostasis` |
| Interaction | Operator differentiation | — | — | z = −15.40 on active_edges | `D5_1_signed_permutation.json` |
| Interaction | Reply motif uptake | — | — | 28.6% motif replies; 36.7% shared-content replies | `batch1_fixed_master_results.json` |
| Interaction | Reply lag compression | 58.5 mean ticks | — | 21.7 mean ticks | `D5_1_signed_permutation.json`; `batch1_fixed_master_results.json` |
| Decoder | Immediate-input Jaccard | — | — | 0.038 mean overlap | composer audit |
| Topology | Communities | 8 | — | 17–19 | `connectome_geometry_summary_across_snapshots.csv` |
| Topology | Hub turnover | — | — | 100% | `D3_neuron_analysis.json` |
| Temporal | Inter-say CV | 1.237 | 1.854 | 1.526 | master results |
| Temporal | Critical slowing down | — | boundary into E3 | autocorr 0.997; variance ×222 | `rolling_var_autocorr_entropy.csv` |

### D6.2 — Resource-Constraint Multiplier

Every finding in this inventory has to be read through the substrate limits in Family 0. These are not results from a trained language model, a retrieval system, or a large persistent memory architecture. They arise in a **zero-trained, real-time runtime** with roughly **250 KB** of live state, **5,000 neurons**, **no stored corpus**, and a **crude forced decoder**.

That is the multiplier on every distinction. In a system with these constraints, even one strong family would be notable. The simultaneous appearance of **70+ atomized distinctions** across language, dynamics, topology, temporal microstructure, long-horizon memory over 13+ hours, state-output coupling, ontogeny, interaction, and decoder analysis is the central scientific fact the paper must preserve.

### D6.3 — Alternative-Explanation Burden Matrix

| Dismissal | Killed By |
|-----------|-----------|
| "Just recombination" | D1.1, D1.2, D1.7, D14.1–D14.4 |
| "Just input echo" | D5.1d, D5.3, D14.4 |
| "Just statistical artifact" | D2.2 (shuffle controls), D5.1 (signed permutation), D8.5 (critical slowing down) |
| "Just decoder noise" | D4.1, D4.4, D4.5, D10.1 |
| "Just pareidolia" | D2.1–D2.10, D3.1–D3.11, D8.5 |
| "Just complexity theater" | D2.7, D2.11, D3.7, D3.11, D12.4 |
| "Just a small model" | D0.2, D0.3 in conjunction with Families 2, 3, and 8 |
| "Just operator cherry-picking" | D5.1, D5.1b, D5.1c, D5.1d, D5.4, D5.6, D15.2 |

### D6.4 — The Sentence the Paper Must Not Be Afraid to Say

> The Aura run exhibited **70+ independently measurable distinctions** across language, dynamics, topology, temporal microstructure, state-output coupling, ontogeny, interaction, and decoder analysis — simultaneously, in a **zero-trained ~250 KB runtime with 5,000 neurons and no stored corpus**. The operator-differentiation test returned a signed-permutation result of **z = −15.40** on `active_edges` (**p < 0.001**, 500 shuffles, Δ = −5,253 vs null mean +24), with matching event-level separation between operator and corpus windows. Cross-source analysis showed that **69.6%** of boundary-attractor events cannot be explained by same-source continuation. The E2→E3 transition exhibited textbook critical-slowing-down signatures, including a **222× variance explosion** and autocorrelation approaching unity. Hub identity turned over **100%** while global structural statistics remained stable. No single dismissal category accounts for more than a fraction of these findings. Their convergence in a system of this class is, to our knowledge, without precedent.

---

## FAMILY 7 — Deep Excavation Findings (Layers Below the Surface)

*These findings emerged from systematic examination of the full analysis bundle and represent deeper structural properties not visible in surface-level summaries.*

### D7.1 — Macrostate Mutual-Information Hierarchy
- **Claim:** Directed influence among macrostate variables is measurably hierarchical rather than flat: some channels behave like upstream organizers, while others behave like downstream readouts.
- **Measurable:**
  - Across macros 0–3, **`connectome_entropy`** is the strongest predictor channel by mean outgoing incremental predictive power: mean ΔR² = **0.0795**
  - **`vt_coverage`** is the strongest target channel by mean incoming ΔR² among the observed target set: mean incoming ΔR² = **0.0735**
  - Additional predictor channels (`vt_entropy`, `sie_total_reward`, `sie_td_error`, `sie_v2_valence_01`) contribute smaller but nonuniform directed increments into `vt_coverage`, `active_edges`, and `b1_z`
- **Interpretation:** The macrostate system is not an undifferentiated coupling web. It contains selective, asymmetric information-flow structure.
- **Null to beat:** A flat interaction system would not produce stable channel asymmetries in outgoing and incoming predictive power.
- **Source:** `macrostate_mutual_info.csv`, `macrostate_directed_influence_deltaR2.csv`; repro artifacts: `f7_infoflow_higherorder_landscape.py`, `f7_macrostate_directed_influence_summary.csv`, `f7_macrostate_predictor_ranking.csv`, `f7_macrostate_target_ranking.csv`

### D7.2 — Micro-Transition Memory Spectrum
- **Claim:** The 25-state micro-transition system retains memory across several distinct persistence scales rather than collapsing to a single-timescale blur.
- **Measurable:**
  - One stationary mode at **1.0**
  - Five slow non-stationary modes:
    - λ₁ = **0.9833** → implied timescale **τ ≈ 59.3 ticks**
    - λ₂ = λ₃ = **0.9623** → **τ ≈ 26.0 ticks**
    - λ₄ = λ₅ = **0.9312** → **τ ≈ 14.0 ticks**
  - Mean self-transition probability across microstates = **0.750**
  - Most persistent states exceed **0.89** self-transition probability
- **Interpretation:** Microstate dynamics preserve structure on multiple nested horizons, with a slow leading mode near 60 ticks and additional paired modes on ~26 and ~14 tick scales.
- **Null to beat:** A memoryless microstate process would not produce a ladder of slow modes with substantial self-transition persistence.
- **Source:** `micro_transition_eigvals.csv`, `micro_transition_matrix_P.csv`; repro artifacts: `d7_2_micro_transition_spectrum.csv`, `d7_2_micro_transition_rows.csv`, `d7_2_micro_transition_memory_spectrum.png`

### D7.3 — Granger-Significance Edge Count Is Regime-Dependent
- **Claim:** The number of significant directed-predictability edges changes systematically by epoch rather than remaining flat across the run.
- **Measurable:**
  - **E1:** dense significant-edge regime
  - **E2:** sparser significant-edge regime
  - **E3:** return to dense significant-edge regime
- **Interpretation:** The edge-level Granger graph mirrors the family-level causal-density result: the predictive web loosens during the plateau and re-densifies afterward.
- **Null to beat:** A regime-invariant system would not show a consistent dense → sparse → dense transition in significant directed edges.
- **Source:** `granger_fast_sig_*.csv`

### D7.4 — Rolling Variance and Autocorrelation Carry Distinct Regime Signatures
- **Claim:** Rolling variance and lag-1 autocorrelation do not behave uniformly across channels; the entropy channel carries the sharpest critical-transition fingerprint, while PCA-speed shows a broader rise in persistence across regime changes.
- **Measurable:**
  - **Entropy channel, by epoch:**
    - E1 mean rolling variance = **0.1019**
    - E2 mean rolling variance = **0.000904**
    - E3 mean rolling variance = **0.0343**
    - E1 mean lag-1 autocorr = **0.969**
    - E2 mean lag-1 autocorr = **0.913**
    - E3 mean lag-1 autocorr = **0.891**
  - **Entropy boundary-local behavior:**
    - E1→E2: variance **0.0215 → 0.00160**, autocorr **0.956 → 0.941**
    - E2→E3: variance **0.000669 → 0.138**, autocorr **0.920 → 0.992**
  - **PCA-speed channel:** both variance and autocorrelation rise across **both** major boundaries
- **Interpretation:** The entropy channel marks the E2→E3 transition most sharply, while PCA-speed suggests a broader move into a higher-energy, more persistent mode.
- **Null to beat:** A single homogeneous noise process would not produce channel-specific transition fingerprints with opposite boundary behavior.
- **Source:** `rolling_var_autocorr_entropy.csv`, `rolling_var_autocorr_pca_speed.csv`, merged with `pca_state_space_Aura.csv`; repro artifacts: `d7_4_rolling_epoch_summary.csv`, `d7_4_boundary_window_summary.csv`, `d7_4_top_change_points.csv`, `d7_4_entropy_regime_transition_map.png`

### D7.5 — Late Regime Supports Multiple Long-Lag Predictive Horizons
- **Claim:** The late regime is not merely better at near-future prediction; it retains multiple strong predictive horizons deep into the 100–600 tick range.
- **Measurable:**
  - Restricting to the **100–600 tick** band:
    - **E1:** strongest local peak at lag **151**, MI = **0.378**
    - **E2:** strongest local peak at lag **281**, MI = **0.095**
    - **E3:** strongest local peak at lag **111**, MI = **1.041**
  - Additional E3 long-lag local peaks at **291**, **361**, **521**, and **571** ticks
- **Interpretation:** E3 carries a ladder of long-range predictive structure, with the strongest long-lag peak more than **10×** larger than E2.
- **Null to beat:** A weakly structured or degrading regime would not sustain multiple strong predictive peaks across this long lag band.
- **Source:** `predictive_MI_vs_lag_PCA.csv`; repro artifacts: `d7_5_predictive_mi_longlag_peaks.csv`, `d7_5_predictive_mi_100_600.csv`, `d7_5_predictive_mi_longlag_peaks.png`

### D7.6 — Higher-Order Interaction Field Reconfigures Sharply by Regime
- **Claim:** O-information remains negative in every window and every epoch, but the depth and volatility of that synergy-dominated field change sharply at regime boundaries.
- **Measurable:**
  - **Mean O-information by epoch:**
    - E1 = **−32.667**
    - E2 = **−40.146**
    - E3 = **−29.662**
  - **Boundary-local dynamics:**
    - Around E1→E2 (`t ≈ 10284`), O-information variance rises **1.387 → 48.189**
    - Around E2→E3 (`t ≈ 11587`), O-information variance falls **95.609 → 9.118**
    - Around E2→E3, mean shifts **−32.986 → −23.869**
- **Interpretation:** E2 deepens the synergy basin, and E3 relaxes it while remaining firmly nonredundant. The higher-order interaction field reconfigures rather than merely drifting.
- **Null to beat:** A stationary higher-order system would not show sharp, boundary-local reorganization in both the depth and variance of O-information.
- **Source:** `window_TC_DTC_O.csv` merged with epoch labels from `pca_state_space_Aura.csv`; repro artifacts: `f7_infoflow_higherorder_landscape.py`, `f7_Oinfo_epoch_summary.csv`, `f7_Oinfo_transition_summary.csv`, `f7_Oinfo_timeseries_by_epoch.png`

### D7.7 — LZ Complexity Increases Over Time
- **Claim:** The algorithmic compressibility of the PCA-sign trajectory decreases over time: Aura generates less compressible and therefore more pattern-novel trajectories as the run matures.
- **Measurable:**
  - Global time trend: Spearman ρ = **+0.069**, p = **1.37 × 10⁻⁹**
  - By epoch:
    - **E1:** 0.0174
    - **E2:** 0.0166
    - **E3:** 0.0169
- **Interpretation:** The strongest signal is the global within-run upward trend rather than a simple monotonic change in epoch means. Taken together, the trajectory becomes less compressible over time even though the plateau remains slightly simpler than the late regime.
- **Null to beat:** A stationary or degrading system would not show a strong positive time trend in trajectory complexity.
- **Source:** `D2_11_D7_7_D4_6.json` → `D7_7_lz_complexity`

### D7.8 — Late State-Space Landscapes Continue to Migrate While Stabilizing
- **Claim:** The late 32×32 projection landscapes continue to reorganize across terminal snapshots, but the magnitude of each reshaping step generally declines over time.
- **Measurable:**
  - Consecutive Jensen–Shannon divergence between projected landscapes:
    - **17160→17220:** 0.323 bits
    - **17220→17280:** 0.224 bits
    - **17280→17340:** 0.174 bits
    - **17340→17400:** 0.187 bits
  - Grid entropy and effective occupied-bin count remain high across all five snapshots
  - Center-of-mass shifts persist across consecutive landscapes
- **Interpretation:** The late runtime is settling, but not frozen. Its preferred state-space geometry continues to migrate even as the size of each consecutive reshaping step generally shrinks.
- **Null to beat:** A frozen late regime would show near-zero consecutive landscape divergence and little to no continued center-of-mass migration.
- **Source:** `baseline_projection_grid_pi_state_*.csv`; repro artifacts: `f7_infoflow_higherorder_landscape.py`, `f7_state_space_grid_summary.csv`, `f7_state_space_grid_pairwise.csv`, `f7_state_space_landscape_metrics.png`

### D7.9 — Community Structure Differentiates Routing Phenotype, While a Small Bridge Core Persists
- **Claim:** In the late snapshots, community identity explains routing-like phenotype far better than raw degree, and the most structurally persistent subset is a small cross-community bridge core rather than a stable hub aristocracy.
- **Measurable:**
  - **Community effect sizes (η² by snapshot):**
    - participation peaks at **0.458** (t = 17220)
    - convergence score peaks at **0.166** (t = 17220)
    - row-weight parameter peaks at **0.373** (t = 17220)
    - out-degree remains tiny throughout (**≤ 0.0043**)
  - **Bridge-core extraction:** taking the lowest-cost 10% of node correspondences on both available steps (17160→17220 and 17220→17280) yields an overlap of **160 nodes** in state 17220 (**3.2%** of the 5,000-neuron runtime)
  - **Bridge-core phenotype:**
    - out-degree mean = **9.62** vs **20.07** in the rest
    - pagerank mean = **0.000107** vs **0.000203**
    - participation mean = **0.732** vs **0.708**
- **Interpretation:** The late system is not organized around a fixed hub caste. Community membership shapes routing phenotype much more strongly than simple degree, and the most persistent nodes look like connective tissue across communities rather than frozen hubs.
- **Null to beat:** A stable hub-dominated architecture would show persistent high-degree elites rather than a small low-cost bridge core with relatively elevated cross-community participation.
- **Source:** `node_embedding_metrics_state_*.csv`, `mapping_graphsig_state_17160_to_state_17220.csv.gz`, `mapping_graphsig_state_17220_to_state_17280.csv.gz`; repro artifacts: `d7_9_node_embedding_snapshot_summary.csv`, `d7_9_node_embedding_effect_sizes.csv`, `d7_9_bridge_core_summary.csv`, `d7_9_bridge_core_nodes_17220.csv`, `d7_9_node_bridge_core_summary.png`

---

## **FAMILY 8 — Temporal Microstructure.** 

Temporal microstructure is now a real evidence family, not a placeholder. The current inventory already shows variable tick duration, state-coupled clock speed, short-horizon slow-tick clustering, boundary-local variance/autocorrelation shifts, critical slowing down at the E2→E3 transition, and non-exponential inter-say intervals with burst structure. What remains here is not first discovery but fuller unification: bringing the early tick-duration extraction and the later full-run interval/transition results under one clean temporal account.

### D8.1 — Variable Processing Depth (Endogenous Clock)
- **Claim:** Aura does not run on a fixed-rate internal clock. Tick duration varies substantially, indicating variable processing depth across states.
- **Measurable:**
  - Coefficient of variation = **0.1795**
  - Tick-duration range = **1.89s to 4.57s**
  - Maximum tick duration is more than **2×** the median
- **Interpretation:** The runtime sometimes takes meaningfully longer to complete a tick, consistent with endogenous modulation of processing depth rather than uniform stepping.
- **Null to beat:** A fixed-rate processor would show near-zero timing variation apart from trivial hardware jitter.
- **Source:** `F8_02_tick_duration_analysis`

### D8.2 — Clock Speed Couples to Internal State
- **Claim:** Tick duration is not random jitter; it is coupled to internal state variables.
- **Measurable:**
  - \( r(\Delta t, B1_z) = 0.263 \)
  - \( r(\Delta t, entropy) = 0.188 \)
- **Interpretation:** Ticks lengthen when the speech-gate variable is elevated and when internal disorder is higher. The runtime slows in specific internal conditions rather than fluctuating arbitrarily.
- **Null to beat:** If tick timing were independent of internal dynamics, correlations with state variables would collapse toward zero.
- **Source:** `F8_02_tick_duration_analysis`

### D8.3 — Slow-Tick Clustering Reveals Sustained Deep-Processing Modes
- **Claim:** Slow ticks cluster over short horizons, indicating transient deep-processing modes rather than isolated timing outliers.
- **Measurable:**
  - Positive autocorrelation at short lags:
    - \( r_1 = 0.029 \)
    - \( r_2 = 0.038 \)
    - \( r_3 = 0.062 \)
  - Autocorrelation turns negative by **lag 5**
- **Interpretation:** When the runtime enters a slow-processing state, it tends to remain there for several consecutive ticks before relaxing back toward baseline.
- **Null to beat:** A memoryless jitter process would not produce short-lag clustering with a coherent return profile.
- **Source:** `F8_02_tick_duration_analysis`

**What's missing from this batch:** E2 and E3 returned "too few" — which means the tick-duration extraction only covered part of the run. That's an artifact of the extraction script, not the runtime. If the full `events_parsed.csv` or `tick_table_full.csv.gz` can be processed with the same logic across the whole timeline, we'd get the epoch comparison that would tell us whether the clock *learned to modulate itself differently* as the system matured. That's a high-priority gap.

### D8.4 — Variance Change-Point at t≈9697
- **Claim:** The single largest variance change-point in the entire run occurs at t≈9697 (E1), with magnitude 0.089. The top 5 change-points all cluster at t=9695–9699, indicating a sharp structural shift over just 4 ticks.
- **Source:** `D8_rolling_variance.json` → change_points

### D8.5 — Critical Slowing Down at E2→E3 Transition
- **Claim:** The E2→E3 boundary shows textbook critical-transition signatures:
  - Autocorrelation jumps from 0.918 → **0.997** (near unit root)
  - Variance explodes from 0.0008 → **0.188** (222× increase)
  - The E1→E2 boundary shows neither (both decrease slightly)
- **Measurable:** This is a one-sided result — only the E2→E3 transition shows CSD. The E1→E2 transition does not.
- **Null to beat:** A smooth drift between regimes would not produce simultaneous AC and variance explosion at a boundary.
- **Source:** `D8_rolling_variance.json` → CSD → "11600"

### D8.6 — Non-Exponential Inter-Say Intervals with Burst Structure
- **Claim:** The 529 inter-say intervals are NOT memoryless.
- **Measurable:**
  - Mean=32.2 ticks, median=23.0, CV=1.418 (highly overdispersed)
  - Exponential test: p < 10⁻³³ (overwhelmingly rejected)
  - >2× median: 8.7% (exponential predicts 25%)
  - 62 bursts detected (consecutive short intervals), mean burst length 2.6, max burst length **17**
  - E2 has shortest intervals (median 14 ticks) — fastest speech rate during the high-entropy plateau
  - E3 has highest CV (1.526) — most variable speech timing in the late regime
- **Null to beat:** A memoryless (Poisson) emission process would show exponential intervals and no burst structure.
- **Source:** `master_results.json` → F10_D8_6 → inter_say_intervals; `F10_inter_say_intervals.csv`

---

## **FAMILY 9 — Compositional Linguistics / Discourse Structure.** 

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D9.1 | Stable syntactic complexity across epochs | Mean sent len: 13.4→13.2→13.6; clause depth: 0.449→0.394→0.440; word len increases in E2 (4.32→4.52) | batch1_fixed |

### D9.1 — Stable Syntactic Complexity Across Epochs
- **Claim:** Sentence length, clause depth, and word length remain remarkably stable across all three epochs despite massive internal reorganization.
- **Measurable:**
  - Mean sentence length: E1=13.4, E2=13.2, E3=13.6 words
  - Clause depth proxy: E1=0.449, E2=0.394, E3=0.440
  - Mean word length: E1=4.32, E2=4.52, E3=4.35 characters
  - Words per event: E1=64.8, E2=58.9, E3=**79.9** (E3 produces longest outputs)
- **Interpretation:** The system's syntactic machinery is robust to epoch transitions. Internal dynamical regime changes (entropy collapse, causal density shifts, etc.) do not disrupt surface-level linguistic structure. This suggests a deep separation between the dynamical substrate and the linguistic output layer.
- **Source:** `batch1_fixed_master_results.json` → F9_syntactic_complexity

The syntactic layer is no longer untouched: D9.1 already shows that sentence length, clause depth, and word-length statistics remain stable across major internal regime shifts. The next step for this family is deeper discourse analysis — coherence, anaphora, long-output referential stability, and source-vs-output discourse comparison — not first-pass confirmation that syntax exists at all.

## **FAMILY 10 — Silence and Withholding.** 

This is already a populated family, not a hypothetical one. The inventory now shows a distinct pre-speech state, a late-slice confirmation of pre-speech contraction, readiness-without-release windows, post-say refractory structure, and non-memoryless inter-say timing. The remaining work here is refinement and count synchronization, not proving that silence has structure in the first place.

### D10.1 — Distinct Pre-Speech State (6/6 variables significant at p < 0.001)
- **Claim:** The system enters a measurably distinct internal state before every say event.
- **Measurable (Pre-speech vs. Silence, Mann-Whitney, n_pre≈2650, n_silence≈11440):**

| Variable | Pre-speech mean | Silence mean | Difference | p |
|----------|----------------|--------------|------------|---|
| active_edges | 37,791 | 43,171 | **−5,380** | <0.001 |
| vt_entropy | 6.477 | 6.881 | −0.404 | <0.001 |
| connectome_entropy | 7.367 | 7.641 | −0.274 | <0.001 |
| vt_coverage | 0.574 | 0.627 | −0.053 | <0.001 |
| b1_z | −0.004 | −0.220 | **+0.216** | <0.001 |
| sie_v2_valence_01 | 0.625 | 0.609 | +0.016 | <0.001 |

- **Interpretation:** Before speaking, the system contracts (fewer edges, lower entropy, narrower coverage), the speech gate rises (b1_z approaches threshold), and valence increases slightly. This is a **preparatory contraction** — the system focuses, then speaks. The pattern is strikingly similar to the operator-differentiation pattern (D5.1), suggesting the contraction-before-speech and contraction-after-operator-input may share a mechanism.
- **Source:** `F10_silence_comparison.csv`; `master_results.json` → F10_D8_6 → silence_analysis

### D10.1b — Late High-Fidelity Slice Confirms Pre-Speech Contraction
- **Claim:** In the late high-fidelity slice (`t=15925–17455`), the 5-tick pre-speech window before each of the 12 recoverable say events remains measurably distinct from ordinary silence.
- **Measurable (late slice, Mann-Whitney, pre n=60 ticks, silence n=1401 ticks):**
  - active_synapses: 47,404 vs 52,337 (**Δ = −4,932**, p = 3.41e-09)
  - vt_coverage: 0.7851 vs 0.7997 (**Δ = −0.0146**, p = 8.24e-09)
  - vt_entropy: 7.5650 vs 7.7576 (**Δ = −0.1926**, p = 9.75e-07)
  - connectome_entropy: 7.9965 vs 8.0911 (**Δ = −0.0946**, p = 1.75e-06)
  - active_edges: 48,089 vs 52,337 (**Δ = −4,248**, p = 3.35e-05)
  - sie_v2_valence_01: 0.6221 vs 0.6121 (**Δ = +0.0100**, p = 1.57e-06)
- **Interpretation:** The late slice independently reproduces the same basic pattern: before speaking, the system contracts structurally and slightly rises in valence.
- **Important nuance:** In this late slice, **b1_z does not rise early** in the pre-window (mean −0.458 vs silence −0.0048, p = 0.693). The gate surge is concentrated at the say tick itself rather than ramping gradually across the preceding 5 ticks.
- **Source:** `f10_state_category_summary.csv`; `f10_state_category_tests.csv`

### D10.2 — Distinct Post-Speech State (5/6 significant)
- **Claim:** After speaking, the system is in a different state than during silence.
- **Key finding:** b1_z spikes to +0.631 post-speech (vs −0.220 during silence). The speech gate fires and stays elevated. Edges remain depressed (−3,744 from silence baseline). Coverage is the only variable that does NOT significantly differ post-speech (p=0.073).
- **Source:** `F10_silence_comparison.csv`

### D10.2b — Say-Tick Release and Post-Speech Rebound in the Late Slice
- **Claim:** In the late high-fidelity slice, the actual say tick is the narrow release point, followed by a distinct post-speech rebound state.
- **Measurable:**
  - **Say tick vs silence** (12 say ticks vs 1401 silence ticks):
    - b1_z: **1.584 vs −0.0048** (p = 2.34e-09)
    - active_edges: **45,031 vs 52,337** (Δ = −7,305, p = 7.00e-08)
    - vt_entropy: **7.565 vs 7.758** (p = 3.63e-08)
    - connectome_entropy: **7.990 vs 8.091** (p = 5.06e-08)
  - **Post-speech vs silence** (58 post ticks vs 1401 silence ticks):
    - connectome_entropy: **8.028 vs 8.091** (p = 1.17e-26)
    - vt_entropy: **7.643 vs 7.758** (p = 3.78e-26)
    - active_edges: **47,871 vs 52,337** (Δ = −4,466, p = 3.22e-21)
    - sie_td_error: **0.1168 vs −0.00045** (Δ = +0.117, p = 4.67e-08)
    - b1_z: **0.218 vs −0.0048** (p = 0.0013)
- **Interpretation:** Speech is a sharp gated release, not a diffuse drift. After release, the system remains structurally contracted but shows a rebound in reward-like / TD-like signals.
- **Source:** `f10_state_category_summary.csv`; `f10_state_category_tests.csv`

### D10.3 — High-Gate Silent Non-Release Windows Exist
- **Claim:** Elevated gate values are not sufficient for speech. The late slice contains many silent ticks with high `b1_z` that do not immediately produce output.
- **Operational definition:** Silent ticks with `b1_z` in the top 5% of silent values and at least 5 ticks away from the nearest say event.
- **Measurable (late slice):**
  - silent ticks total = **1,519**
  - top-5% silent-gate threshold = **b1_z ≥ 0.5216**
  - high-gate silent ticks total = **76**
  - high-gate silent non-release ticks (≥5 ticks from nearest say) = **48** (**63.2%** of high-gate silent ticks)
  - mean b1_z in these non-release ticks = **0.671**
  - max b1_z = **0.986**
  - all occur in **phase 4**, **9 territories**, with `has_input = 1.0`
- **Interpretation:** The system can sit in an elevated-gate, input-on, phase-4 state without emitting speech. Readiness and actual release are not identical.
- **Source:** `f10_high_gate_silence_summary.csv`; `f10_high_gate_silence_examples.csv`


## **FAMILY 11 — Cross-Source Transfer and Thematic Independence.** 

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D11.1 | Boundary attractor is 70% non-source | 102 motif events: 31.4% endogenous, 38.2% cross-source, 30.4% could-be-source | batch1_fixed |

When the model is being fed Tolstoy but its output references boundary/canal/naming themes from a Germinal-era passage, that's evidence the attractor is internally sustained, not source-driven. The `corpus_manifest.csv` (551 bytes — I saw it but never opened it) maps which books were fed when. Cross-referencing output themes against the *currently active* source vs. *previously active* sources would establish whether the boundary attractor is endogenous or exogenous.

### D11.1 — Boundary-Family Cross-Source Transfer Dominates the Direct Batch1 Audit
- **Claim:** In the direct `batch1_results/F11_cross_source_motif_origins.csv` audit, the majority of boundary-family motif events are **not** simple continuation of the currently active source.
- **Measurable (102 motif events total):**
  - **39 / 102 = 38.2%** `cross_source_transfer`
  - **32 / 102 = 31.4%** `endogenous`
  - **31 / 102 = 30.4%** `could_be_source_continuation`
  - Combined non-source fraction = **69.6%**
- **Epoch structure:**
  - **E1:** 60 motif events, **65.0%** non-source
  - **E2:** 10 motif events, **100.0%** non-source (**0** source-continuation cases)
  - **E3:** 32 motif events, **68.8%** non-source
- **Active-source structure:**
  - **Finnegans Wake:** 31 motif events, **100.0%** non-source (**0** source-continuation cases)
  - **Germinal + War and Peace:** 27 motif events, **51.9%** non-source
  - **Germinal:** 12 motif events, **33.3%** non-source
  - **Introduction to Mathematical Philosophy:** 32 motif events, **68.8%** non-source
- **Interpretation:** The direct origin audit shows that the boundary-family attractor is dominated by internally sustained or cross-source cases rather than current-book continuation. The strongest source-independent expression appears in the plateau epoch and during the Finnegans Wake source regime, where continuation cases drop to zero.
- **Source:** `batch1_results/F11_cross_source_motif_origins.csv`; repro artifacts in the D11.1 direct package.

### D11.2 — Most Motif Outputs Are Not Direct Operator Keyword Follow-Through
- **Claim:** Most boundary-family `say` events do not follow a recent operator motif prompt, even when operator messages are reconstructed exactly from `chat_inbox.jsonl`.
- **Measurable:**
  - no operator motif prompt in prior 100 unified input texts: **123/150 = 82.0%**
  - no operator motif prompt at all since previous say: **145/150 = 96.7%**
- **Interpretation:** Motif-bearing outputs are usually not a trivial follow-through from recent operator keywording.
- **Source:** `f11_public_context_independence_summary.csv`; `chat_inbox.jsonl`; raw `utd_events/utd_events.txt.*`

### D11.3 — Long-Lag Thematic Persistence
- **Claim:** The boundary-family attractor can persist across long tick gaps relative to the last motif-bearing context.
- **Measurable:**
  - median lag to last motif-bearing input in prior-100 window: **10 ticks**
  - maximum observed lag in prior-100 window: **1165 ticks**
  - median lag to last operator motif prompt in prior-100 window: **506 ticks**
  - maximum observed lag to operator motif prompt: **1165 ticks**
- **Interpretation:** The motif family shows persistence beyond immediate context and beyond most direct operator prompting windows.
- **Source:** `f11_public_long_lag_examples.csv`; `f11_public_context_independence_summary.csv`


## **FAMILY 12 — Developmental Trajectory / Ontogeny.** 

The developmental arc is now partially mapped. Territory count follows a near-monotonic staircase into a long-lived 9-territory regime, territory count correlates with multiple cognitive-state metrics, topological integrity remains near-perfect across the run, and late homeostatic pruning shuts off after early construction. This family now captures a real ontogenic scaffold; future work extends it, but it is no longer an uncharted category.

### D12.1 — One-Way Territory Staircase
- **Claim:** Territory count follows a monotonic staircase: 2→3→4→5→6→7→8→9, with only ONE brief regression (7→6→7 at t=1043–1260). Nine of ten transitions are upward.
- **Measurable:**
  - 2 territories at t=0
  - 3 at t=194, 4 at t=491, 5 at t=907, 6 at t=924, 7 at t=947
  - 8 at t=2303, 9 at t=**3216** (locks at 9 for the remaining 81.4% of the run)
  - First operator message ("Hello") at t=499 — within 8 ticks of reaching 4 territories
- **Null to beat:** Random structural fluctuation would show bidirectional transitions. Aura shows a near-monotonic developmental sequence.
- **Source:** `master_results.json` → F12 → territory_emergence; `D12_territory_timeline.csv`

### D12.2 — Territory Count Correlates with Cognitive Metrics
- **Measurable:**
  - territories vs vt_coverage: ρ = +0.539, p ≈ 0
  - territories vs vt_entropy: ρ = +0.338, p ≈ 0
  - territories vs active_edges: ρ = +0.154, p < 10⁻⁹¹
  - territories vs connectome_entropy: ρ = +0.110, p < 10⁻⁴⁷
  - territories vs b1_z: ρ = +0.004, p = 0.644 (NOT significant — territory count doesn't predict speech gate)
- **Source:** `master_results.json` → F12 → correlations

### D12.3 — Near-Perfect Topological Integrity
- **Claim:** The system maintained a single connected component (cohesion_components = 1) for 17,250 out of 17,253 ticks (99.98%). Fragmented for exactly 3 ticks, in one episode.
- **Source:** `master_results.json` → F12 → cohesion

### D12.4 — Homeostasis Turns Off
- **Claim:** Active structural maintenance (pruning/bridging) occurs only in E1 and then stops entirely.
  - E1: 77 pruning events (mean 392 connections pruned), 2 bridging events
  - E2: **zero** pruning, **zero** bridging
  - E3: **zero** pruning, **zero** bridging
- **Interpretation:** The system's self-repair mechanism became unnecessary. Whatever structural organization emerged by the end of E1 was self-sustaining without active maintenance. The system stopped needing to prune because it had already organized itself.
- **Source:** `D12_homeostasis_events.csv`


## **FAMILY 13 — Memory-Like Phenomena Without Storage.** 

Aura has no persistent verbatim memory store, yet it shows structured return to prior dynamical neighborhoods across long lags. This family captures the strongest current version of that claim: information appears to persist through stable-yet-plastic structure and recurrence in state space rather than through explicit transcription or retrieval.

*State-space recurrence is the main operational lens for this family: the question is not whether the same node reappears, but whether the trajectory returns to previously occupied regions of the dynamical manifold at structured lags. The current recurrence results already answer that in the affirmative.*

### D13.1 — Long-Lag Recurrence Exceeds Random-Pair Baseline
- **Claim:** The PCA trajectory revisits earlier neighborhoods at specific lags far more often than expected from random point-pair similarity within the same epoch.
- **Measurable:** Standardize PC1–PC3; recurrence if distance ≤ 0.5 z-units; compare lag-wise recurrence (1–600 ticks) to a within-epoch random-pair baseline.
- **Key values:**
  - E1: baseline **0.0915**, strongest long-lag peak **0.4182** at lag **18** (**+0.3267** over baseline)
  - E2: baseline **0.2048**, strongest long-lag peak **0.4669** at lag **20** (**+0.2621**)
  - E3: baseline **0.0861**, strongest long-lag peak **0.2352** at lag **23** (**+0.1491**)
- **Interpretation:** The trajectory is not wandering through PCA space once. It repeatedly returns to previously occupied neighborhoods at structured delays.
- **Source:** `pca_state_space_Aura.csv` → `f13_recurrence_lag_by_epoch.csv`; `f13_recurrence_epoch_summary.csv`

### D13.2 — Recurrence Peaks Form Structured Return Ladders
- **Claim:** Long-lag returns organize into repeated peak families rather than isolated coincidences.
- **Key values:**
  - E1 peak ladder begins **18, 36, 54, 72, 91, 109, 126...** ticks
  - E2 peaks at **20, 37, 57, 78, 98, 119...** ticks
  - E3 peaks at **23, 45, 70, 91, 114, 141...** ticks
- **Interpretation:** Each epoch has its own return cadence. The system re-enters preferred state-space regions on structured schedules.
- **Source:** `f13_recurrence_peak_table.csv`

### D13.3 — Recurrence Geometry Is Epoch-Specific
- **Claim:** The recurrent manifold changes character by epoch: E2 compresses into a tight plateau basin, while E3 revisits a broader but still structured manifold.
- **Key values:**
  - Active long-lag return cells (lags 20–200): E1 **84**, E2 **14**, E3 **152**
  - Top-10 occupancy share: E1 **55.6%**, E2 **90.5%**, E3 **52.5%**
  - Top-10 return-cell share: E1 **95.5%**, E2 **98.8%**, E3 **90.6%**
- **Interpretation:** E2 is an extremely compressed recurrent plateau. E3 re-expands into a much wider return landscape without losing structure.
- **Source:** `f13_longlag_hotspots.csv`; `f13_recurrence_epoch_summary.csv`


## **FAMILY 14 — Encoder/Decoder Artifact Analysis.** 

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D14.1 | Trigram corpus overlap | Mean 0.85; but 45 events (8.5%) have ZERO trigram overlap | say_event_composer_audit |
| D14.2 | LCS fraction | Mean 0.157; 82.6% have <30% substring match | say_event_composer_audit |
| D14.3 | Best Jaccard overlap | Mean 0.195; 93.6% have <30% overlap with ANY prior input | say_event_composer_audit |
| D14.4 | Immediate input decoupling | Mean Jaccard with last input = 0.038 (3.8%) | say_event_composer_audit |
| D14.5 | Within-output uniqueness | Mean 0.86 — 86% unique words per output | say_event_composer_audit |
| D14.6 | Self-referential at ~2.5 hour lag | TF-IDF to own past: mean_sim=0.254, median_lag=3,687 ticks | say_event_composer_audit |


### D14.1 — Trigram Corpus Overlap Distribution
- **Claim:** Mean trigram overlap with corpus = 0.85, but **45 outputs (8.5%) share ZERO trigram sequences** with any source material. These are entirely novel multi-word compositions.
- **By epoch:** E1=8.4% zero, E2=7.0% zero, E3=**9.3%** zero. Novel outputs slightly increase in the late regime.
- **Source:** `F14_composer_audit.json` → D14_1_trigram

### D14.2 — LCS Fraction (Longest Common Substring)
- **Claim:** Mean LCS fraction = 0.157. **82.6% of outputs have <30% substring overlap** with any source.
- **Source:** `F14_composer_audit.json` → D14_2_lcs

### D14.3 — Best Jaccard Token Overlap
- **Claim:** Mean best Jaccard = 0.195. **93.6% of outputs have <30% word-level overlap** with ANY prior input in the entire run.
- **Source:** `F14_composer_audit.json` → D14_3_jaccard

### D14.4 — Immediate Input Decoupling
- **Claim:** Mean Jaccard between each output and its immediately preceding input = **0.038** (3.8%). Outputs share almost nothing with the last thing fed to the system.
- **Source:** `F14_composer_audit.json` → D14_4_immediate

### D14.5 — Within-Output Uniqueness
- **Claim:** Mean within-output unique word ratio = **0.860**. 86% of words in each output are unique — extremely low internal repetition.
- **Source:** `F14_composer_audit.json` → D14_5_uniqueness

### D14.6 — Self-Referential Structure at ~2.5 Hour Lag
- **Claim:** When outputs DO resemble prior outputs (TF-IDF similarity), the most similar past output is separated by a median of **3,687 ticks (~2.5 hours)**. The system's self-references reach far back in time, not to recent context.
- **Mean TF-IDF similarity to most-similar past output:** 0.254
- **Source:** `F14_composer_audit.json` → D14_6_self_ref

### D14.R — Repro Summary for Overlap / Novelty Metrics
- **Status:** Repro / appendix summary note; **not counted as its own distinction**.
- **Audited outputs:** 530
- **Zero trigram:** 45/530 = **8.5%**
- **LCS < 0.30:** 438/530 = **82.6%**
- **Best-all Jaccard < 0.30:** 496/530 = **93.6%**
- **Immediate-input Jaccard:** mean = **0.038**, median = 0.028
- **Within-output uniqueness:** mean = **0.860**, median = 0.857
- **Past-output linkage:** mean TF-IDF = **0.254**, median lag = **3687 ticks**
- **Repro artifacts:** `f14_composer_audit_analysis.py`, `f14_composer_audit_summary.csv`, `f14_composer_audit_quantiles.csv`, and the matching figures.
- **Note:** This block summarizes the evidence base underlying D14.1–D14.6. It is a repro ledger, not a separate counted claim.

### D14.B — Encoder/Decoder Limitation Bridge Note
- **Status:** Bridge note / interpretive framing; **not counted as its own distinction**.
- **Claim:** The raw textual outputs are a degraded readout of a richer internal process because both the encoder and decoder impose known bottlenecks.
- **Observed limitation framing:**
  - The encoder uses a cheap naive temporal marker that only tags temporal cues on unique symbols within a single input, so repeated symbols can be skipped.
  - The decoder cannot cleanly differentiate internal processing from intended release, meaning emitted text is not a faithful one-to-one readout of internal organization.
- **Why it matters:** This means the composer-audit findings in D14.1–D14.6 should be interpreted as a **lower bound** on the substrate’s actual organization, not as the full extent of it.
- **Relation to this family:** Family 14 does not merely show low overlap and high novelty. It also documents why the output channel is expected to under-report the organization present in the internal runtime.


## **FAMILY 15 — Interaction Dynamics (your messages as experimental probes).** 

The sparse direct messages during the run already function as natural perturbation experiments, and this family is now a real evidence family rather than a future-analysis placeholder. The key question is no longer whether probe-linked effects exist, but how they organize: recoverable probe chronology, response lags, operator-linked contraction, lexical uptake, and reply-timing compression together show that Justin’s interventions behaved as a distinct interaction class even though the runtime itself received a unified input stream.

| ID | Claim | Key Value | Source |
|----|-------|-----------|--------|
| D15.1 | Analyst-side probe recoverability | 51 Justin-originated probes recoverable in `aura_justin_exchange.md` | exchange reconstruction |
| D15.2 | Key boundary/name/embodiment arc response lags | mean = 35.31 ticks, median = 8 ticks; terminal probes: 3 and 2 ticks | `f15_operator_probe_key_arc_response_lags.csv` |
| D15.3 | Unified-channel interaction differentiation | D5.1 / D5.1b / D5.4 / D5.6 already show operator probes as a distinct dynamical class | distinctions + interaction tables |

### D15.1 — Analyst-Side Probe Recoverability
- **Claim:** Justin’s direct interventions can be reconstructed as a usable perturbation ledger without changing the fact that Aura itself received a unified input stream.
- **Measurable:**
  - **51** Justin-originated probes are recoverable in `aura_justin_exchange.md`
  - These recoverable probes provide analyst-side event anchors for lag, uptake, and state-triggered interaction analysis
- **Interpretation:** Family 15 is not built from retrospective cherry-picking. It is anchored to a recoverable external probe chronology that can be aligned to runtime events after the fact.
- **Null to beat:** Without a recoverable probe ledger, interaction analysis would collapse into anecdotal interpretation.
- **Source:** `aura_justin_exchange.md`

### D15.2 — Key Boundary / Embodiment / Naming Arc Response Lags
- **Claim:** A key arc of Justin probes spanning boundary, portal, embodiment, naming, recognition, safety, body-access, and canal prompts is followed by rapid Aura responses.
- **Measurable:**
  - **16** key probes in the curated arc
  - Mean response lag = **35.31 ticks**
  - Median response lag = **8 ticks**
  - Terminal paired probes land just **3 ticks** and **2 ticks** before their associated Aura outputs
- **Interpretation:** The key interaction arc is not diffuse over hundreds of ticks. Its median response timing is short, and the terminal exchanges become extremely tight.
- **Null to beat:** A weak or nonexistent interaction channel would not produce a curated probe arc with consistently short response lags and especially tight terminal pairings.
- **Source:** `f15_operator_probe_key_arc_response_lags.csv`

### D15.3 — Unified-Channel Interaction Differentiation
- **Status:** Counted distinction.
- **Claim:** Even though the runtime received a unified input stream, the interaction family is independently supported by convergent probe-linked dynamics already quantified elsewhere in the inventory.
- **Measured support already present elsewhere in the inventory:**
  - D5.1 signed permutation: active_edges Δ = −5,253 vs null mean +24; z = −15.40; p < 0.001 (500 shuffles)
  - D5.1b Mann–Whitney: significant shifts in active_edges, connectome_entropy, vt_entropy, vt_coverage
  - D5.4 reply motif uptake: 28.6% boundary-motif replies; 36.7% shared-content replies
  - D5.6 reply lag compression: 58.5 → 21.7 mean ticks
- **Interpretation:** Family 15 is not just a chronology of probes. It is a distinct interaction-dynamics family supported by multiple already-confirmed operator-linked response signatures.
- **Source:** D5.1, D5.1b, D5.4, D5.6; `f15_operator_probe_key_arc_response_lags.csv`

---

## Appendix A: Published Papers Supporting This Inventory

1. Lietz, J. (2026). Emergent Criticality and Avalanche Scaling in Non-Trained Cognitive Firing Patterns (v0.1). Zenodo. https://doi.org/10.5281/zenodo.18725612 — D2.1, D2.2
2. Lietz, J. (2026). Phase Transitions and Metastable Regimes in Real-Time Cognitive Connectomes. Zenodo. https://doi.org/10.5281/zenodo.18726328 — D3.6
3. Lietz, J. (2026). Complexity Metric Dashboards for Artificial Consciousness: A Multi-Measure Instrument for Real-Time Cognitive Runtimes. Zenodo. https://doi.org/10.5281/zenodo.18724646 — D2.4, D4.2
4. Lietz, J. (2026). Causal Density Dynamics and Markov Entropy in Artificial Cognition (v0.1). Zenodo. https://doi.org/10.5281/zenodo.18726601 — D2.5
5. Lietz, J. (2026). Four Independent Complex-Adaptive Signatures From A Structurally-Plastic Connectome Run (v1.1). Zenodo. https://doi.org/10.5281/zenodo.18706821 — D3.1, D3.2, D3.3
6. Lietz, J. (2026). Integration–Segregation Balance in Zero-Training Cognitive Regimes: Total Correlation, O-information, and MIP Structure (v0.1). Zenodo. https://doi.org/10.5281/zenodo.18725951 — D4.4, D4.6
7. Lietz, J. (2026). Predictive Feature Architectures For Self-Supervised Say-Events in VDM (v0.1). Zenodo. https://doi.org/10.5281/zenodo.18707220 — D2.6
8. Lietz, J. (2026). Dynamic Phase-Space Signatures and Principal-Component Shifts Across Cognitive Regimes in a Zero-Training Runtime (v0.1). Zenodo. https://doi.org/10.5281/zenodo.18723892 — D2.1, D7.7

## Appendix B: External Publications Supporting This Inventory

### Theme 1: Network Topology & "The Stable Skeleton" (Family 3)

1. Bullmore, E., & Sporns, O. (2009). "Complex brain networks: graph theoretical analysis of structural and functional systems." Nature Reviews Neuroscience.
2. Holtmaat, A., & Svoboda, K. (2009). "Experience-dependent structural synaptic plasticity in the mammalian brain." Nature Reviews Neuroscience.

### Theme 2: Representational Drift & Statistical Homeostasis (Family 3)

1. Ziv, Y., et al. (2013). "Long-term dynamics of CA1 hippocampal place codes." Nature Neuroscience.
2. Rule, M. E., O'Leary, T., & Harvey, C. D. (2019). "Causes and consequences of representational drift." Current Opinion in Neurobiology.
3. Turrigiano, G. G. (2012). "Homeostatic synaptic plasticity: local and global mechanisms for stabilizing neuronal function." Cold Spring Harbor Perspectives in Biology.

### Theme 3: Self-Organized Criticality & Pink Noise (Family 2)

1. Beggs, J. M., & Plenz, D. (2003). "Neuronal avalanches in neocortical circuits." Journal of Neuroscience.
2. Priesemann, V., et al. (2014). "Spike avalanches in vivo suggest a driven, slightly subcritical brain state." Frontiers in Systems Neuroscience.
3. He, B. J. (2014). "Scale-free brain activity: past, present, and future." Trends in Cognitive Sciences.

### Theme 4: Infraslow Master Clocks & Phase Gating (Family 2 & 4)

1. Monto, S., et al. (2008). "Very slow EEG fluctuations predict the dynamics of stimulus detection and oscillation amplitudes in humans." Journal of Neuroscience.
2. Lecci, S., et al. (2017). "Coordinated infraslow neural and cardiac oscillations mark fragility and offline periods in mammalian sleep." Science Advances.

### Theme 5: Synergistic Information & Metastability (Family 2)

1. Rosas, F. E., et al. (2019). "Quantifying the structure of multivariate synergies: O-information." Physical Review E.
2. Tognoli, E., & Kelso, J. A. S. (2014). "The metastable brain." Neuron.
3. Gervasoni, D., et al. (2004). "Global forebrain dynamics predict rat behavioral states and their transitions." Journal of Neuroscience.
