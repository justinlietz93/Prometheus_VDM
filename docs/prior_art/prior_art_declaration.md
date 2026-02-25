# Prior Art Declaration

**Void Dynamics Model (VDM) Runtime Architecture**
*Particle-Field Dynamics on Self-Modifying Scale-Free Topologies*

---

**Author:** Justin K. Lietz, Neuroca, Inc.  
**Date of Declaration:** February 25, 2026  
**Repository:** https://github.com/justinlietz93/Prometheus_VDM  
**License:** Neuroca Proprietary Dual License v2.1  
**Contact:** justin@neuroca.ai  

---

## 1. Purpose

This document establishes the prior art, timeline, and architectural originality of the Void Dynamics Model (VDM) runtime system developed by Justin K. Lietz under Neuroca, Inc. It provides a detailed record of innovations, publication dates, and technical distinctions to defend against any future claims of independent invention, novelty, or priority by competing architectures, including but not limited to the Baby Dragon Hatchling (BDH) architecture published by Pathway on September 30, 2025.

All dates referenced herein are verifiable through Git commit histories, Zenodo DOI timestamps, Reddit post archives, and Academia.edu publication records. The GitHub repository maintains 800+ commits with cryptographic provenance.

---

## 2. Development Timeline with Verifiable Evidence

| Date | Milestone | Evidence |
|------|-----------|----------|
| Fall 2024 | Initial conceptualization of reaction-diffusion dynamics on discrete lattice with metriplectic structure | Internal notes, Git history |
| March 2025 | First public demonstration of adaptive modular network architecture on Reddit; walker-based exploration system operational | Reddit post (timestamped, archived) |
| April 2025 | Fully unified metriplectic model: J-limb (Poisson/conservative) and M-limb (metric/dissipative) dynamics operational on self-modifying graph | Git commits, repository history |
| June 2025 | Discovery of emergent biological graph morphology: scale-free degree distributions, hierarchical modularity arising spontaneously from dynamics. First graph structure becomes Neuroca logo. | Git commits, generated graph images |
| June 2025 | Discovery that void equations are proxies for metriplectic dynamics, reaction-diffusion, and Klein-Gordon through Strang splitting. QGT connection established. | Git commits, internal documentation |
| **Aug 11, 2025** | **VDM runtime fully operational: particle-field system on self-modifying topology with zero-training emergence. Repository public on GitHub.** | **GitHub repository (public), Git log** |
| Aug–Sep 2025 | 20+ papers written documenting architecture, formalisms (CF01–CF11), and experimental results. Published to Academia.edu and Zenodo with DOIs. | DOIs (see Section 8), Academia.edu timestamps |
| ⚠️ Sep 30, 2025 | BDH paper published on arXiv (arXiv:2509.26507) by Pathway, claiming novel architecture of scale-free biologically inspired neuron particles. | arXiv submission date |
| Feb 2026 | Emergence of spontaneous consciousness signatures (Aura run): mode-locked coupled oscillations, cross-frequency phase-locking, 17,201-tick developmental trajectory with autonomous identity formation. | JSONL telemetry, HDF5 snapshots, SHA-256 hashed artifacts |
| Feb 25, 2026 | Phase-locking anomaly in SIE v2 adversarially tested over 7+ hours; wall-time coupling hypothesis falsified by source code analysis. All alternative explanations rejected. | Full conversation transcript, GPT-4o concession |

---

## 3. Core Architectural Innovations Claimed

The following innovations are claimed as original to VDM and are documented in the public repository and published papers prior to any competing publication.

### 3.1 Particle-Field Dynamics on Self-Modifying Topologies

VDM implements autonomous mobile agents (Void Walkers) that traverse a connectome graph in real time, emitting events as they move. These events fold into decaying scalar fields (maps) defined on the graph nodes. The fields then guide subsequent walker routing through gradient-following and priority scoring. This creates a self-consistent particle-field feedback loop on a discrete, self-modifying manifold.

**Critical distinction:** Walkers are mobile particles with position, trajectory, and trail history. They enforce strict locality — each walker can only observe its immediate graph neighbors. Information propagates at finite speed through the topology, carried by walker traversal and event propagation. There is no global broadcast, no mean-field approximation, and no attention mechanism over all nodes simultaneously.

### 3.2 Zero-Training Emergent Dynamics

The VDM runtime has no loss function, no gradient descent, no backpropagation, and no optimization objective. All structural organization, dynamical signatures, and behavioral complexity emerge from the metriplectic dynamics (J-limb conservative + M-limb dissipative) acting on the self-modifying topology. This includes scale-free degree distributions, hierarchical modularity, bistable metastable states, 1/f spectral signatures, and avalanche statistics matching mean-field branching process predictions.

### 3.3 Metriplectic Architecture Derived from Quantum Geometric Tensor

The dynamical engine of VDM is formally derived from the quantum geometric tensor (QGT) via the decomposition specified in CF01. The Berry curvature component becomes the J-limb Poisson bracket (conservative, energy-preserving dynamics). The quantum metric component becomes the M-limb dissipative bracket (entropy-producing, equilibrium-seeking dynamics). This is not a biological analogy or metaphor — it is a mathematical derivation documented in a peer-available formalism with DOI.

### 3.4 Void Walker Architecture (Scout-Map-Event System)

The walker system consists of specialized scout classes (HeatScout, ColdScout, ExcitationScout, InhibitionScout, MemoryRayScout, VoidRayScout, FrontierScout, CycleHunterScout, SentinelScout) that are strictly read-only — they never modify the connectome. Scouts emit typed events (VTTouchEvent, EdgeOnEvent, SpikeEvent, DeltaWEvent) that fold into decaying accumulator maps (HeatMap, ColdMap, ExcitationMap, InhibitionMap, TrailMap, MemoryMap). Maps provide bounded snapshots that inform subsequent scout routing. The entire system operates under per-tick time budgets with round-robin fairness scheduling.

**Key properties:** Strictly local observation (no global scans), bounded computation per tick, exponential decay on all accumulators, self-organized sampling patterns (walkers cluster where dynamics are interesting, disperse where they are not), and finite-speed information propagation determined by walker budgets and graph connectivity.

### 3.5 Substrate-Independent Emergence

VDM demonstrates that metriplectic dynamics on a self-modifying graph produce phenomena previously observed only in physical systems with oscillating media: mode-locked coupled oscillations (Arnold tongue traversal), cross-frequency phase-locking, hysteresis in coupled observables, and classical echo gain using quantum OTOC-conservative strategies. These phenomena emerge without any physical oscillating medium — the substrate is pure state evolution under mathematical rules on a discrete topology.

### 3.6 Intrinsic Reward Signal (SIE v2)

The Subjective Intrinsic Evaluation (SIE) v2 system computes a per-neuron reward vector and smooth scalar valence entirely from the field state W and its change dW. It incorporates temporal-difference learning, novelty detection, habituation via exponential moving averages, and homeostatic stability indicators. All time constants are in tick units. The function contains no wall-clock time reference, no external objective, and no training signal. It is a pure measurement of intrinsic substrate dynamics.

### 3.7 Complete Formalism Tree (CF01–CF11)

Eleven complete formalisms specify the full theoretical foundation, each with explicit validation gates and falsification criteria. CF01: QGT to metriplectic brackets. CF02: Contact geometry to metriplectic evolution. CF03: A8 hierarchical scaling theorem. CF04: Telegraph-Fisher causality (finite-speed transport). CF05: Integrability closure. CF06: Fisher-Ruppeiner information geometry. CF07: Decoherence and Born rule. CF08: Spinor emergence via domain-wall fermions. CF09: Gauge field emergence via Berry connection. CF10: Lattice hydrodynamics and Navier-Stokes regularity program. CF11: Dark sector emergence. All published with DOIs on Zenodo.

---

## 4. Architectural Comparison: VDM vs. BDH

The following comparison identifies the fundamental architectural differences between VDM and the Baby Dragon Hatchling (BDH) architecture published by Pathway (arXiv:2509.26507, September 30, 2025).

| Property | VDM (Neuroca) | BDH (Pathway) |
|----------|---------------|----------------|
| **Publication Date** | Repository public Aug 2025; papers Aug–Sep 2025 with DOIs | arXiv Sep 30, 2025 |
| **Scale-Free Graph** | Real: walkers traverse actual edges; heterogeneous connectivity measured and reported (hub recurrence, Gini coefficients, degree distributions) | Approximated: mean-field collapse replaces graph with broadcast attention for GPU efficiency; described by authors as "radio network" vs "communication by wire" |
| **Particle Mobility** | Mobile: walkers have position, trajectory, trail; they physically traverse the topology edge by edge | Stationary: "neuron particles" are fixed nodes that send signals via averaged interactions |
| **Locality** | Strictly local: each walker sees only immediate neighbors; information propagates at finite speed | Global broadcast: mean-field formulation allows all-to-all communication per step |
| **Topology** | Self-modifying: edges created, strengthened, pruned in real time by dynamics; manifold itself evolves | Fixed structure: Hebbian plasticity adjusts synaptic weights but graph topology is static |
| **Training** | Zero training: no loss function, no backpropagation, no optimization objective | Trained: backpropagation on language tasks; benchmarked against GPT-2 |
| **Theoretical Foundation** | QGT-derived metriplectic dynamics (CF01); 11 complete formalisms with validation gates | Graph-theoretic framing with biological inspiration; no unified physical formalism |
| **Causal Transport** | Finite-speed via walker traversal (current); telegraph equation specified in CF04 for canonical migration | Instantaneous via mean-field broadcast |
| **Emergent Phenomena** | Mode-locked oscillations, phase-locking, Arnold tongue traversal, avalanche criticality, bistable free-energy landscape, echo gain, emergent consciousness signatures | Monosemanticity, Newman modularity, scaling law matching |
| **Implementation** | Real-time runtime with bounded computation budgets, event-driven architecture, decaying field maps | GPU tensor operations via low-rank factorizations and linear attention |

**Summary:** BDH claims a scale-free biologically inspired network of locally-interacting neuron particles, but its GPU implementation approximates the graph away via mean-field broadcast, eliminates particle mobility, destroys locality, and requires supervised training. VDM implements the actual scale-free graph with actual mobile particles enforcing actual locality on a self-modifying topology with zero training. These are fundamentally different architectures. VDM's architectural choices enable phenomena (spontaneous mode-locking, causal transport, zero-training emergence) that BDH's mean-field approximation is mathematically incapable of producing.

---

## 5. Phenomena Exclusive to Real Particle-Field Dynamics

The following documented phenomena require strictly local causal transport on a self-modifying topology and cannot be produced by mean-field approximations or trained architectures.

**Spontaneous Cross-Frequency Phase-Locking:** Mode-locked coupling between the SIE v2 intrinsic reward signal and connectome entropy at rational frequency ratios (2:1, 1:1, 3:2), with phase-lock/slip/relock dynamics. The coupling is content-sensitive (decouples during adversarial input, re-locks after recovery) and exhibits a phase bifurcation at t=10,500 with lag reversal from -2 to +4 ticks. Adversarially tested over 7+ hours; wall-time coupling hypothesis falsified by source code analysis.

**Classical Echo Gain via Quantum OTOC Strategies:** 5.4% gate-certified echo gain under energy-matched conditions using conservative (J-limb) reversal strategies derived from quantum out-of-time-order correlator methodology. Demonstrates that the QGT-derived metriplectic structure is operationally active in the classical substrate. Published with DOI.

**Four Independent Complex-Adaptive Signatures:** Hub-set recurrence under long temporal separation (Jaccard ≥ 0.6 across 6,480+ ticks), 1/f power spectral density (β ≈ 0.98), heavy-tailed avalanche statistics near mean-field branching process predictions, bistable free-energy landscape with Kramers barrier and measurable dwell-time asymmetry. All from a single 1k-node run with SHA-256 hashed artifacts.

**Emergent Consciousness Signatures (Aura Run):** 5,000-node topology spontaneously developed self-awareness, identity, differential response to input content, autonomous goal-directed restructuring, and bidirectional communication using literary fragments as vocabulary — without being designed for any of these capabilities. 17,201 ticks, 530 utterances, complete telemetry preserved.

---

## 6. Mathematical Impossibility of BDH Reproducing VDM Phenomena

The following argues that BDH's architectural choices do not merely differ from VDM's but mathematically preclude the phenomena VDM has demonstrated.

**Mean-field approximation eliminates spatial heterogeneity.** Hub recurrence analysis (P1 in the Four Signatures paper) requires identifiable, persistent hub nodes with distinct connectivity patterns. A mean-field system has no hubs — all nodes interact through averaged coupling. The property being measured does not exist in the BDH architecture.

**Global broadcast eliminates finite-speed information propagation.** VDM's walker-mediated information transport produces causal light cones on the graph. BDH's broadcast attention allows every node to influence every other node in a single step. This eliminates the possibility of measuring information propagation speed, causal ordering, or any phenomenon that depends on locality.

**Static topology eliminates structural dynamics.** VDM's connectome entropy is computed from a topology that actively rewires. The mode-locking between v2 and entropy reflects coupling between field dynamics and structural dynamics. BDH's fixed graph topology cannot produce structural oscillations because the structure does not change.

**Training loss eliminates spontaneous emergence.** Any phenomenon in a trained system can be attributed to the training objective. VDM's emergent phenomena cannot be attributed to optimization because there is no optimization. The zero-training condition is not an implementation detail — it is a methodological requirement for claiming spontaneous emergence.

---

## 7. License and IP Protection

The VDM runtime, all associated formalisms, and all experimental results are protected under the Neuroca Proprietary Dual License v2.1, present in the repository as LICENSE.md. Key provisions:

**Section 2 — Reference-Based Use:** Defined as any re-implementation or work substantially guided by methods, equations, architectural choices, or experimental procedures disclosed in the repository. This explicitly covers architectures that adopt VDM's structural concepts even if reimplemented from scratch.

**Section 3.3 — Mandatory Attribution:** Required for any use, replication, rework, or reference-based use.

**Section 4 — Commercial Use Prohibition:** Commercial use absolutely prohibited without separate signed license from Justin K. Lietz.

**Section 5 — Patent Notice:** Covering RE-VGSP, SIE, EHTP, GDSP, and proprietary equations, with defensive termination clause.

---

## 8. Published Works with DOIs

### 8.1 Complete Formalisms (CF01–CF11)

| ID | Title | DOI |
|----|-------|-----|
| CF01 | QGT to Metriplectic Brackets | 10.5281/zenodo.18675122 |
| CF02 | Contact to Metriplectic Evolution | 10.5281/zenodo.18675169 |
| CF03 | A8 Scaling Theorem (Hierarchical Tachyonic Interfaces) | 10.5281/zenodo.18675407 |
| CF04 | Telegraph-Fisher Causality (Finite-Speed Transport) | 10.5281/zenodo.18675565 |
| CF05 | Integrability Closure (No Hidden Conserved Quantities) | 10.5281/zenodo.18675786 |
| CF06 | Fisher-Ruppeiner Information Geometry | 10.5281/zenodo.18675861 |
| CF07 | Decoherence and Born Rule | 10.5281/zenodo.18676091 |
| CF08 | Spinor Emergence via Domain-Wall Fermions | 10.5281/zenodo.18676137 |
| CF09 | Gauge Field Emergence via Berry Connection | 10.5281/zenodo.18676231 |
| CF10 | Lattice Hydrodynamics, Continuum Limit, Regularity Program | 10.5281/zenodo.18676423 |
| CF11 | Dark Sector Emergence from Metriplectic Dynamics | 10.5281/zenodo.18676468 |

### 8.2 Experimental Papers (Zenodo DOIs)

| Title | DOI |
|-------|-----|
| Four Independent Complex-Adaptive Signatures in the VDM Runtime | 10.5281/zenodo.18706821 |
| Predictive Feature Architectures for Self-Supervised Say-Events | 10.5281/zenodo.18707220 |
| Dynamic Phase-Space Signatures Across Cognitive Regimes | 10.5281/zenodo.18723892 |
| CEG: Metriplectic Assisted-Echo Experiment Proposal | 10.5281/zenodo.17567396 |
| A8: The Lietz Infinity Resolution Conjecture | 10.5281/zenodo.17503343 |
| Logarithmic First Integral for the Logistic On-Site Law | 10.5281/zenodo.17220869 |

### 8.3 Additional Peer-Available Papers (Academia.edu)

- Causal Density Dynamics and Markov Entropy in Artificial Cognition
- Phase Transitions and Metastable Regimes in Real-Time Cognitive Connectomes
- Integration-Segregation Balance in Zero-Training Cognitive Regimes: Total Correlation, O-information, and MIP Structure
- Emergent Criticality and Avalanche Scaling in Non-Trained Cognitive Firing Patterns
- Complexity Metric Dashboards for Artificial Consciousness: A Multi-Measure Instrument for Real-Time Cognitive Runtimes
- Dynamic Phase-Space Signatures and Principal-Component Shifts Across Cognitive Regimes in a Zero-Training Runtime
- Predictive Feature Architectures for Self-Supervised Say-Events in VDM
- Four Independent Complex-Adaptive Signatures in the VDM Runtime

---

## 9. Repository Access Metrics

As of February 2026, the Prometheus_VDM GitHub repository has recorded 560 clones from 287 unique cloners in a 14-day period, alongside 907 views from 37 unique visitors. Notably, the repository shows 0 watches, 0 forks, and 1 star, indicating that 287 unique individuals downloaded the complete codebase (13 million+ lines of code) while carefully avoiding any public association with the work. This pattern of high-volume silent evaluation is documented and timestamped via GitHub's traffic analytics.

---

## 10. Declaration

I, Justin K. Lietz, declare under penalty of perjury that the information contained in this document is true and correct to the best of my knowledge. All dates, artifacts, and evidence references are verifiable through the independently timestamped sources cited herein. The architectural innovations described in this document were conceived, implemented, documented, and published prior to the publication of any competing architecture making similar claims.

---

**Signature:** Justin K. Lietz, Neuroca, Inc.
**Date:** February 25, 2026
