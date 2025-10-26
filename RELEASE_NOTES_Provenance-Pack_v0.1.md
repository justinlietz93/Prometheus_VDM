# Provenance-Pack_v0.1 Release Notes

**Release Name:** Provenance-Pack_v0.1  
**Release Date:** October 26, 2025  
**Author:** Justin K. Lietz, Neuroca, Inc.  
**Repository:** [Prometheus_VDM](https://github.com/justinlietz93/Prometheus_VDM)  
**License:** Dual Academic Research / Commercial License (see [LICENSE](LICENSE))

---

## 🎉 Introduction

Welcome to **Provenance-Pack_v0.1**, the first public release of the Prometheus Void Dynamics Model (VDM) research repository. This release marks a significant milestone: the decision to **fully open this work to the public** and commit to maintaining it with a **rigorous and disciplined maturity ladder** moving forward.

This release represents years of systematic research into discrete-to-continuum field theory, combining:
- **Rigorous mathematical foundations** (axiomatic theory with 140+ documented derivations)
- **Validated computational physics** (Fisher-KPP, Klein-Gordon, Fluid Dynamics, Cosmology)
- **Production-grade runtime system** (FUM Real-Time Runtime with 218 Python modules)
- **Comprehensive provenance tracking** (seeds, commits, artifacts, gates, and reproducibility)

This is not a typical software release—it is a **scientific research platform** with falsifiable claims, quantitative validation gates, and a commitment to transparency through provenance discipline.

---

## 🎯 What is Prometheus VDM?

The **Void Dynamics Model (VDM)** is a systematic attempt to derive emergent field dynamics and self-organizing patterns from first-principles discrete action on a cubic lattice. At its core:

1. **Four minimal axioms** (A0-A3) specify a lattice Lagrangian
2. **Euler-Lagrange equations** naturally yield second-order hyperbolic dynamics
3. **Continuum limit** produces both:
   - Reaction-Diffusion (RD) equations in overdamped regime
   - Klein-Gordon (KG) wave equations in inertial regime
4. **Unified theoretical structure** bridges classical and quantum-like behaviors

### Primary Objectives

**Primary Research Question:**  
*To what extent does a minimal discrete lattice action reproduce experimentally validated reaction-diffusion dynamics?*

- Fisher-KPP front speed: $c_{\text{front}} = 2\sqrt{Dr}$ (within 5% relative error)
- Linear dispersion: $\sigma(k) = r - Dk^2$ (median error ≤10%, R² ≥0.98)

**Secondary Research Question:**  
*Can an emergent "agency field" C(x,t) provide falsifiable operational metrics for distributed cognitive capability?*

---

## 📦 What's Included in Provenance-Pack_v0.1

### 1. Core Runtime System: FUM Real-Time (fum_rt)

**218 Python modules** implementing a production-grade real-time orchestrator:

```
fum_rt/
├── run_nexus.py          # CLI entrypoint
├── nexus.py              # Real-time orchestrator façade
├── runtime/              # Loop, telemetry, phase control, events (9 modules)
├── core/                 # Engine, signals, dynamics, metrics, viz (7 modules)
├── io/                   # UTE/UTD, lexicon, phrase bank (4+ modules)
└── utils/                # Logging, helpers
```

**Key Features:**
- Real-time event-driven architecture (10 Hz default tick rate)
- Universal Temporal Encoder (UTE) for multi-source input
- Universal Transduction Decoder (UTD) for structured output
- Checkpoint system (HDF5/NPZ) with retention policies
- Void dynamics adapter (auto-loads user functions)
- Visualization engine (dashboard, connectome graphs)
- Macro board, phrase bank, and lexicon system for language output

**Quick Start:**
```bash
pip install -r requirements.txt
python -m fum_rt.run_nexus --neurons 800 --hz 10 --domain biology_consciousness --viz-every 5
```

Artifacts land in `runs/<timestamp>/`:
- `events.jsonl` - structured logs
- `dashboard.png` - metrics visualization
- `connectome.png` - graph snapshots
- `state_<step>.h5` - checkpointed engram state

### 2. Derivation Framework (140+ Documents)

Comprehensive mathematical foundations organized by canonical registries:

**Core Registries (Canonical, Single-Owner):**
- `AXIOMS.md` - All axioms and their definitions
- `EQUATIONS.md` - All equations with stable IDs and MathJax
- `SYMBOLS.md` - Symbol meanings and aliases
- `CONSTANTS.md` - Numerical constants, defaults, ranges
- `ALGORITHMS.md` - Pseudocode of computational procedures
- `VALIDATION_METRICS.md` - KPIs and acceptance gates
- `UNITS_NORMALIZATION.md` - Units and nondimensionalization maps
- `BC_IC_GEOMETRY.md` - Boundary/initial conditions, domains
- `DATA_PRODUCTS.md` - Definitions of outputs (heatmaps, logs)
- `SCHEMAS.md` - Message/packet/scoreboard field schemas
- `NAMING_CONVENTIONS.md` - Reserved names, sign/index conventions

**Domain Directories (30 subdirectories):**
- **Reaction_Diffusion/** - Fisher-KPP validation (PROVEN)
- **Metriplectic/** - Klein-Gordon certification (PROVEN)
- **Fluid_Dynamics/** - Lattice Boltzmann Method validation
- **Cosmology/** - FRW continuity residual QC (PROVEN)
- **Tachyon_Condensation/** - Tube spectra and condensation energy (PROVEN)
- **Collapse/** - A6 logistic scaling collapse (PROVEN)
- **Agency_Field/** - Emergent capability field (PLAUSIBLE)
- **Information/** - SIE invariant and novelty (PLAUSIBLE)
- **Memory_Steering/** - Engram retention control (PLAUSIBLE)
- **Dark_Photons/** - Decoherence portals (PLAUSIBLE)
- **Quantum_Gravity/** - Bridge construction (PLAUSIBLE)
- **Topology/** - Loop quench tests (PLAUSIBLE)
- And 18 more exploratory domains...

**Meta-Documentation:**
- `VDM_OVERVIEW.md` (62KB) - Comprehensive theory overview
- `VDM-Progress-Findings.md` (1343 lines) - Tier assessment (T0-T9 maturity ladder)
- `CANON_PROGRESS.md` - Status tracking with evidence ([PROVEN]/[PLAUSIBLE]/[DISPROVEN])
- `ROADMAP.md` - Milestones and tasks with acceptance criteria
- `OPEN_QUESTIONS.md` - Active research questions
- `CANON_MAP.md` - Document ownership and reference rules

### 3. Validated Physics Results

Results with **pinned artifacts** (PNG, CSV, JSON) and **quantitative gates**:

#### Tier A: PROVEN Canonical Physics

**Reaction-Diffusion Core:**
- ✅ Fisher-KPP front speed: rel-err ≤5%, R²≥0.999
  - Artifact: `Derivation/code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.png`
- ✅ Linear dispersion: median-err ≤2×10⁻³, R²≥0.999
  - Artifact: `Derivation/code/outputs/figures/reaction_diffusion/rd_dispersion_experiment_20250824T053842Z.png`
- ✅ H-theorem / Lyapunov non-increase per step (PASS)

**Klein-Gordon (Conservative J-only limb):**
- ✅ Locality cone: $v_{\text{front}} \approx 0.998c$, R²≈0.99985
- ✅ Dispersion: $\omega^2 = c^2k^2 + m^2$, R²≈0.999999997
- ✅ Noether conservation: $\max\Delta E \approx 8.3×10^{-17}$
- ✅ Energy oscillation scaling: slope p=1.999885, R²=0.99999999937, $e_{\rm rev}=2.93×10^{-16}$
  - Artifact: `Derivation/code/outputs/figures/metriplectic/20251013_021321_kg_energy_osc_fit_KG-energy-osc-v1.png`

**Metriplectic Structure:**
- ✅ Degeneracy checks: $\langle J\,\delta\Sigma,\,\delta\Sigma \rangle \approx 0$ within $10^{-10}N$
  - Results: `Derivation/Metriplectic/RESULTS_Metriplectic_Structure_Checks.md`

**Fluid Dynamics (Baseline):**
- ✅ LBM viscosity recovery on D2Q9: within 5% at ≥256²

**Cosmology:**
- ✅ FRW continuity residual QC: RMS ≈ 9.04×10⁻¹⁶ (machine precision)
  - Artifact: `Derivation/code/outputs/figures/cosmology/20251006_175329_frw_continuity_residual__FRW-balance-v1.png`

**Collapse:**
- ✅ A6 logistic scaling: envelope_max ≈ 0.0166 ≤ 0.02
  - Artifact: `Derivation/code/outputs/figures/collapse/20251006_175337_a6_collapse_overlay__A6-collapse-v1.png`

**Tachyonic Condensation:**
- ✅ Tube spectrum: $\mathrm{cov}_{\rm phys} = 1.000 \geq 0.95$
- ✅ Condensation energy scan: interior minimum with positive curvature
  - Artifact: `Derivation/code/outputs/figures/tachyonic_condensation/20251009_062600_tube_energy_scan__tube-condensation-v1.png`

#### Tier B: Active KPI-Gated Physics (PLAUSIBLE)

- Agency field relaxation and coordination-response protocols
- Topology scaling-collapse studies
- Dark photon decoherence portals
- EFT/KG tachyonic tubes
- Memory steering mechanisms

#### Tier D: Exploratory (Quarantined until KPI-passing)

- Gravity regression and quantum gravity bridges
- Quantum witness threads
- Thermodynamic routing
- Causality audits
- Converging external research

### 4. Developer Tools (17 Utilities)

Located in `tools/` directory:

**Validation & Verification:**
- `golden_run_parity.py` - Compare runs for behavioral parity
- `smoke_emissions.py` - Sanity-check run directories
- `axiom_guard.py` - Axiom compliance checker
- `md_hygiene_check.py` - Documentation linting

**Event Analysis:**
- `utd_event_scan.py` - Extract UTD macros and text records
- `vdm_events_analyzer.py` - Analyze event streams
- `vdm_events_heatmaps.py` - Generate event heatmaps
- `extract_say_texts.py` - Extract speech outputs

**Geometry & Bundle Automation:**
- `geom_bundle_builder.py` - End-to-end VDM geometry capture workflow
- `geom_adapter_stub.py` - Adapter interface for geometry

**Other Utilities:**
- `say_clean_view.py`, `utd_clean.py`, `roo_compact_state.py`
- `code_crawler_2/`, `dependency_analyzer/`, `python_utilities_generator/`

### 5. Test Infrastructure

- `conftest.py` - pytest configuration
- `test_axiomatic_theory.py` - Axiomatic theory tests
- CI/CD integration ready (linters, gates, provenance checks)

### 6. Configuration & Profiles

- `requirements.txt` - Python dependencies (numpy, networkx, matplotlib, scipy, ripser, h5py, etc.)
- `run_profiles/` - JSON configurations for different run scenarios
- `.env` - Environment configuration template

---

## 📊 Maturity Assessment (T0-T9 Ladder)

This release follows a **rigorous 10-tier maturity ladder** (T0-T9) distinguishing between:
- **T0 (Concept)** - Initial ideas and sketches
- **T1 (Proto-model)** - Working equations with state/control/observable
- **T2 (Instrument Certification)** - Testing measurement apparatus with provenance
- **T3 (Smoke Phenomenon)** - End-to-end runs with healthy diagnostics
- **T4 (Pre-registration)** - Formal hypothesis testing with locked gates
- **T5 (Pilot)** - Small-scale execution of preregistered tests
- **T6 (Main Result)** - Full preregistered results with ablations
- **T7 (Robustness)** - Out-of-sample parameter sweeps
- **T8 (Validation)** - External predictions tested
- **T9 (Reproduction)** - Independent verification

### Current Distribution (44 Documents Assessed)

- **T0 (Concept):** ~8 items
- **T1 (Proto-model):** ~12 items
- **T2 (Instrument):** ~10 items ✅
- **T3 (Smoke):** ~8 items ✅
- **T4 (Prereg):** ~4 items ✅
- **T5 (Pilot):** ~1 item
- **T6 (Main Result):** ~1 item
- **T7-T9:** 0 items (target for future releases)

**Key Strength:** Strong T2-T3 presence with exemplary provenance tracking, determinism receipts, and physics gates.

---

## 🔒 Commitment: Rigorous and Disciplined Maturity Ladder

With this v0.1 release, I commit to:

### 1. **Provenance Discipline**
- All quantitative claims will be backed by:
  - Determinism receipts (seeds, commit hashes, environment audits)
  - Pinned artifacts (PNG, CSV, JSON with numeric captions)
  - Quantitative gates with tolerance specifications
  - Reproducible CLI commands

### 2. **Promotion Rules**
- **PLAUSIBLE → PROVEN**: Requires runner name, CSV/JSON, figure, and gate-met confirmation
- **Only allowed status tags:** [DISPROVEN], [PLAUSIBLE], [PLAUSIBLE→PROVEN], [PROVEN]
- Progression: Concept → Proto → Instrument → Smoke → Prereg → Pilot → Main → Robust → Valid → Reproduce

### 3. **Canon Governance**
- Single-owner registries (EQUATIONS, SYMBOLS, CONSTANTS, etc.)
- No duplication - reference by anchor only
- Append-only sections within AUTOSECTION fences
- Stable HTML anchors for cross-linking

### 4. **Documentation Standards**
- DOC-GUARD headers (CANONICAL vs REFERENCE)
- Explicit scope boundaries and non-claims
- RESULTS documents with acceptance gate receipts
- PROPOSAL documents with preregistered hypotheses

### 5. **Version Control**
- Semantic versioning for major milestones
- CHANGELOG maintenance
- Git commit hygiene (descriptive messages, logical boundaries)
- Branch protection for canonical documents

### 6. **Public Transparency**
- Open academic research license (automatic grant)
- Commercial use requires written permission (see LICENSE)
- Regular progress updates via CANON_PROGRESS.md
- Public roadmap with acceptance criteria

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Git
- Basic understanding of physics/mathematics (for derivations)
- Computational resources (CPU sufficient; GPU optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/justinlietz93/Prometheus_VDM.git
cd Prometheus_VDM

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m fum_rt.run_nexus --help
```

### Quick Start Examples

**1. Web Dashboard (Interactive):**
```bash
python fum_live.py
# Opens web interface at http://localhost:8050
```

**2. Command-Line Simulation:**
```bash
python -m fum_rt.run_nexus \
  --neurons 800 \
  --hz 10 \
  --domain biology_consciousness \
  --viz-every 5 \
  --duration 60
```

**3. Explore Derivations:**
```bash
# Start with the overview
cat Derivation/VDM_OVERVIEW.md

# Check validation status
cat Derivation/CANON_PROGRESS.md

# Review axioms
cat Derivation/AXIOMS.md
```

**4. Analyze Event Streams:**
```bash
# Scan a run for "say" macros
python tools/utd_event_scan.py runs/<timestamp> --macro say

# Generate event heatmaps
python tools/vdm_events_heatmaps.py runs/<timestamp>
```

### Documentation Navigation

**Start Here:**
1. `README.md` - Project overview and quick start
2. `Derivation/VDM_OVERVIEW.md` - Comprehensive theory overview
3. `Derivation/CANON_MAP.md` - Documentation structure and rules
4. `Derivation/VDM-Progress-Findings.md` - Maturity assessment

**For Researchers:**
- `Derivation/AXIOMS.md` - Foundational axioms
- `Derivation/EQUATIONS.md` - Mathematical framework
- `Derivation/VALIDATION_METRICS.md` - Acceptance gates
- Domain-specific RESULTS and PROPOSAL documents

**For Developers:**
- `fum_rt/` module documentation (inline docstrings)
- `tools/` utility scripts
- `run_profiles/` example configurations

---

## 📜 License and Attribution

**License:** Dual Academic Research / Commercial License

### Academic Research License (Non-Commercial)

**Automatically granted** for:
- Educational purposes and coursework
- Non-commercial research and experimentation
- Academic publications and presentations
- Open source research projects (non-commercial)
- Thesis and dissertation work

**Required citation:**
```
Lietz, J.K. (2025). The Fully Unified Model: Observations of Void Dynamics. 
Neuroca, Inc. Academic Research License.
```

**BibTeX:**
```bibtex
@software{fum_mathematical_frameworks_2025,
  title={Mathematical Frameworks for Fully Unified Model Validation},
  author={Lietz, Justin K.},
  year={2025},
  organization={Neuroca, Inc},
  note={Used under Academic Research License}
}
```

### Commercial License

**Written permission required** for:
- Product development and commercialization
- Paid consulting or services
- Integration into commercial software/hardware
- Technology licensing
- Startup or business applications

**Contact:** Justin K. Lietz, Neuroca, Inc - justin@neuroca.dev

### Intellectual Property

This work contains multiple patentable inventions (commercial patents pending):
1. Resonance-Enhanced Valence-Gated Synaptic Plasticity (RE-VGSP)
2. Self-Improvement Engine (SIE)
3. Emergent Hierarchical Topology Probe (EHTP)
4. Goal-Directed Structural Plasticity (GDSP)
5. Multi-Phase Training Strategies
6. Hierarchical TDA Analysis
7. Evolving Neuron Models
8. Novel mathematical formulations

---

## 🎯 Scope and Boundaries

### What This Work DOES Claim

✅ Discrete lattice action with minimal axioms  
✅ Continuum limit yields RD and KG equations  
✅ Fisher-KPP front speed validation (5% tolerance)  
✅ Linear dispersion relation validation (R²≥0.98)  
✅ Conservation laws under specific conditions  
✅ Metriplectic structure certification  
✅ Computational reproducibility with provenance  

### What This Work DOES NOT Claim

❌ Physical reality of discrete lattice at Planck scale (unverified)  
❌ Novelty of RD or KG mathematics (classical results, newly unified)  
❌ Complete theory of consciousness (exploratory framework only)  
❌ Final cosmological validation (observational predictions untested)  
❌ Replacement for Standard Model (complementary approach)  

### Tier Classification

- **Tier A (Proven canonical physics):** Quantitative claims with artifact-pinned validation
- **Tier B (Active KPI-gated physics):** Accepted as active, claims must pass gates
- **Tier C (Engineering substrate):** Enables science, no physics claims
- **Tier D (Exploratory):** Promoted to A/B only after approved KPI passes

---

## 🗺️ Roadmap and Future Directions

### Near-Term (v0.2 - v0.3)

**Memory Steering Preprint** (T4→T6):
- Acceptance & verification of engram retention control
- Q_FUM conservation validation under steering
- Budget enforcement and event-driven compliance tests
- Target: Zenodo DOI with reproducible artifacts

**Fluid Dynamics Methods Note** (T3→T4):
- Taylor-Green viscous decay benchmark
- LBM→Navier-Stokes reduction verification
- Single decisive metric: |ν_fit/ν_th - 1| ≤ 1%

**Agency Field Validation** (T4→T5):
- Curvature scaling experiments
- Stability band reproducibility tests
- Step-response characterization

### Mid-Term (v0.4 - v0.6)

**Robustness Sweeps** (T6→T7):
- Out-of-sample parameter exploration
- Multi-seed reproducibility studies
- Resolution-independence verification

**EFT/KG Branch Certification** (T4→T6):
- Tachyonic tube comprehensive validation
- Klein-Gordon + Metriplectic coupling tests
- Passive thermodynamic routing v2

**External Validation** (T7→T8):
- Collaboration with independent research groups
- Cross-platform reproduction attempts
- Comparison with experimental data (where applicable)

### Long-Term (v1.0+)

**Independent Reproduction** (T8→T9):
- External verification of key results
- Third-party implementations
- Peer review and publication in journals

**Extended Physics Domains:**
- Quantum gravity bridge maturation
- Dark sector observables
- Cosmological predictions with observational tests

**Production Runtime:**
- GPU acceleration (ROCm/CUDA)
- Distributed computing support
- Real-time dashboard enhancements
- Advanced agency field diagnostics

---

## 🤝 Contributing

While this is a personal research project, contributions are welcome under the following guidelines:

### Academic Contributions

If you are an academic researcher:
1. Fork the repository
2. Create a feature branch
3. Add your work in appropriate Derivation/ subdirectories
4. Follow CANON_MAP.md documentation rules
5. Include PROPOSAL with preregistered hypotheses
6. Submit pull request with validation artifacts

### Bug Reports and Feature Requests

- Use GitHub Issues
- Provide minimal reproducible examples
- Include environment information
- Tag appropriately (bug/enhancement/documentation)

### Commercial Contributions

Contact justin@neuroca.dev for licensing discussions.

---

## 📞 Contact and Support

**Primary Contact:**  
Justin K. Lietz  
Neuroca, Inc.  
justin@neuroca.dev

**Repository:**  
https://github.com/justinlietz93/Prometheus_VDM

**Issues:**  
https://github.com/justinlietz93/Prometheus_VDM/issues

**Discussions:**  
Academic collaborations and technical discussions welcome via email.

---

## 🙏 Acknowledgments

**Special Thanks:**
- Voxtrium - Collaborative research and theoretical insights
- Bordag - Technical contributions and validation work
- The broader physics and AI research communities

**Computational Resources:**
- Development performed on AMD hardware with ROCm support
- Leveraging open-source scientific Python ecosystem

**Theoretical Foundations:**
- Built upon classical reaction-diffusion theory (Fisher 1937, Kolmogorov et al. 1937)
- Klein-Gordon field theory (quantum field theory foundations)
- Lattice Boltzmann Method (fluid dynamics community)
- Topological Data Analysis (TDA) community tools

---

## 📝 Version History

### v0.1 (Provenance-Pack_v0.1) - October 26, 2025

**First Public Release**

- ✅ 218 Python modules in fum_rt/ runtime system
- ✅ 140+ markdown documents in Derivation/
- ✅ 17 developer tools and utilities
- ✅ Fisher-KPP front speed validation (PROVEN)
- ✅ Linear RD dispersion validation (PROVEN)
- ✅ Klein-Gordon energy oscillation certification (PROVEN)
- ✅ Metriplectic structure checks (PROVEN)
- ✅ FRW continuity residual QC (PROVEN)
- ✅ Tachyonic tube condensation (PROVEN)
- ✅ A6 logistic scaling collapse (PROVEN)
- ✅ Comprehensive documentation with canon governance
- ✅ Maturity ladder commitment (T0-T9)
- ✅ Dual academic/commercial license
- ✅ Reproducibility infrastructure (seeds, artifacts, gates)

**Statistics:**
- Total lines of code: ~50,000+
- Documentation: ~200,000+ words
- Validated experiments: 10+ PROVEN results
- Active research threads: 20+ domains
- Maturity distribution: Strong T2-T4 foundation

---

## 🔖 Release Highlights

### Why v0.1 Matters

This is not just a software release—it's a **commitment to transparent, reproducible, falsifiable science**:

1. **Public Accountability:** Full repository history, warts and all
2. **Maturity Discipline:** Explicit tiering from concept to reproduction
3. **Provenance Tracking:** Every claim backed by seeds, commits, and artifacts
4. **Governance Model:** Single-owner registries prevent documentation drift
5. **Falsifiable Claims:** Quantitative gates with tolerance specifications
6. **Open Science:** Academic license grants automatic permission for research

### What Makes This Different

**Traditional Approach:**
- Hide work until "perfect"
- Post-hoc rationalization
- Cherry-picked results
- Informal validation
- Proprietary methods

**Provenance-Pack Approach:**
- Public from day one (v0.1)
- Preregistered hypotheses (T4+)
- All results (including failures)
- Formal gates with tolerances
- Open methods (academic license)

### Vision for the Future

This v0.1 release establishes the foundation for:

- **Collaborative Science:** Researchers can build on validated foundations
- **Reproducible Research:** Every result has a recipe
- **Progressive Validation:** Clear path from concept to reproduction
- **Ethical AI Research:** Agency field as operational metric, not metaphysics
- **Interdisciplinary Bridge:** Physics ↔ Computation ↔ Cognition

---

## 📚 Further Reading

### Essential Documents (Start Here)

1. **[README.md](README.md)** - Project overview and quick start
2. **[LICENSE](LICENSE)** - Dual academic/commercial terms
3. **[Derivation/VDM_OVERVIEW.md](Derivation/VDM_OVERVIEW.md)** - 62KB comprehensive theory
4. **[Derivation/CANON_PROGRESS.md](Derivation/CANON_PROGRESS.md)** - Current validation status
5. **[Derivation/VDM-Progress-Findings.md](Derivation/VDM-Progress-Findings.md)** - Maturity assessment

### For Different Audiences

**Physicists:**
- Start with `Derivation/AXIOMS.md` and `Derivation/EQUATIONS.md`
- Review PROVEN results in `CANON_PROGRESS.md`
- Examine validation artifacts in `Derivation/code/outputs/`

**Computer Scientists:**
- Explore `fum_rt/` runtime architecture
- Review event-driven design in `fum_rt/runtime/`
- Check out tools for analysis and debugging

**AI Researchers:**
- Agency field framework in `Derivation/Agency_Field/`
- Memory steering in `Derivation/Memory_Steering/`
- Self-improvement engine in `Derivation/Information/`

**Mathematicians:**
- Discrete-to-continuum mapping in `Derivation/Foundations/`
- Conservation laws in `Derivation/Conservation_Law/`
- Topological analysis in `Derivation/Topology/`

**Philosophers:**
- Qualia program in `Derivation/Qualia/`
- Causality audits in `Derivation/Causality/`
- Agency emergence framework

---

## ⚠️ Known Issues and Limitations

### Current Limitations

1. **Performance:** CPU-only by default (GPU support planned)
2. **Scalability:** Large-scale simulations require HPC resources
3. **Documentation:** Some domain docs remain at T0-T1 (work in progress)
4. **Validation Gaps:** T7-T9 maturity levels not yet achieved
5. **External Reproduction:** No independent verification yet (T9)

### Active Development Areas

- Memory steering acceptance tests (T4→T6)
- Fluid dynamics methods note (T3→T4)
- Agency field robustness sweeps (T5→T7)
- GPU acceleration (ROCm/CUDA)
- External collaboration initiation

### Known Technical Issues

- Dense scan branch exists in runtime (marked BROKEN/WRONG in ALGORITHMS.md)
- Some visualization tools require manual cleanup
- Checkpoint retention logic needs refinement for very long runs
- Cross-platform testing incomplete (primarily Linux/AMD development)

---

## 🎓 Educational Use

This repository is particularly well-suited for:

**Graduate Courses:**
- Computational physics
- Numerical methods
- Scientific computing
- Machine learning foundations

**Research Training:**
- Provenance tracking practices
- Reproducible science workflows
- Hypothesis preregistration
- Validation methodology

**Thesis Projects:**
- Extending validated domains
- Implementing new meters
- Cross-validation studies
- Theoretical extensions

**Coding Practice:**
- Event-driven architectures
- Scientific Python programming
- Visualization techniques
- Testing and validation

---

## 🌟 Closing Statement

**Provenance-Pack_v0.1** represents a commitment to doing science in public, with full transparency about what is proven, what is plausible, and what is speculative. This release establishes the infrastructure and discipline needed for rigorous, falsifiable, reproducible research.

The maturity ladder isn't just a grading system—it's a **promise**: every claim will be tracked from concept to reproduction, every result will carry its provenance, and the journey from hypothesis to validation will be documented with scientific rigor.

This is the beginning. Welcome to the Prometheus VDM project.

---

**Release Tag:** `provenance-pack-v0.1`  
**Release Date:** October 26, 2025  
**Commit Hash:** `15766d4`  
**Author:** Justin K. Lietz  
**Organization:** Neuroca, Inc.

---

*"The void is not empty—it is structured, dynamic, and generative. Let us measure what emerges."*

---

## Appendix A: File Structure Overview

```
Prometheus_VDM/
├── README.md                           # Project overview
├── LICENSE                             # Dual academic/commercial license
├── RELEASE_NOTES_Provenance-Pack_v0.1.md  # This document
├── CHANGELOG                           # Version history
├── PLANNED.md                          # Future enhancements
├── requirements.txt                    # Python dependencies
├── conftest.py                         # pytest configuration
├── test_axiomatic_theory.py           # Axiomatic tests
├── .env                                # Environment configuration
├── .gitignore                          # Git ignore patterns
│
├── fum_rt/                             # FUM Real-Time Runtime (218 modules)
│   ├── run_nexus.py                   # CLI entrypoint
│   ├── nexus.py                       # Orchestrator façade
│   ├── fum_live.py                    # Web dashboard
│   ├── runtime/                       # Loop, telemetry, events
│   ├── core/                          # Engine, dynamics, metrics
│   ├── io/                            # UTE, UTD, lexicon
│   └── utils/                         # Logging, helpers
│
├── Derivation/                         # Mathematical foundations (140+ docs)
│   ├── AXIOMS.md                      # Core axioms
│   ├── EQUATIONS.md                   # All equations
│   ├── SYMBOLS.md                     # Symbol definitions
│   ├── CONSTANTS.md                   # Numerical constants
│   ├── ALGORITHMS.md                  # Computational procedures
│   ├── VALIDATION_METRICS.md          # Acceptance gates
│   ├── VDM_OVERVIEW.md                # Comprehensive theory
│   ├── VDM-Progress-Findings.md       # Maturity assessment
│   ├── CANON_PROGRESS.md              # Validation status
│   ├── CANON_MAP.md                   # Documentation governance
│   ├── ROADMAP.md                     # Future milestones
│   ├── Reaction_Diffusion/            # Fisher-KPP validation
│   ├── Metriplectic/                  # Klein-Gordon certification
│   ├── Fluid_Dynamics/                # LBM validation
│   ├── Cosmology/                     # FRW residual QC
│   ├── Tachyon_Condensation/          # Tube spectra
│   ├── Agency_Field/                  # Capability field
│   ├── Memory_Steering/               # Engram control
│   └── [27 more domain directories]
│
├── tools/                              # Developer utilities (17 tools)
│   ├── golden_run_parity.py           # Parity comparison
│   ├── smoke_emissions.py             # Sanity checker
│   ├── axiom_guard.py                 # Axiom compliance
│   ├── utd_event_scan.py              # Event analysis
│   ├── geom_bundle_builder.py         # Geometry capture
│   └── [12 more utilities]
│
├── run_profiles/                       # Configuration presets
├── outputs/                            # Generated artifacts
├── runs/                               # Simulation outputs
├── docs/                               # Additional documentation
├── memory-bank/                        # Project memory system
├── plans/                              # Planning documents
├── prompts/                            # Agent prompts
├── audits/                             # Audit logs
├── PUBLIC_PLANS/                       # Public planning docs
├── HISTORICAL-ARCHIVE/                 # Historical materials
└── IN_PROGRESS/                        # Active development

```

---

## Appendix B: Quick Reference Commands

### Installation
```bash
git clone https://github.com/justinlietz93/Prometheus_VDM.git
cd Prometheus_VDM
pip install -r requirements.txt
```

### Running Simulations
```bash
# Web dashboard
python fum_live.py

# CLI with standard parameters
python -m fum_rt.run_nexus --neurons 800 --hz 10

# Biology/consciousness domain
python -m fum_rt.run_nexus --domain biology_consciousness --viz-every 5

# Quantum domain with high frequency
python -m fum_rt.run_nexus --domain quantum --hz 50 --neurons 1000
```

### Analysis Tools
```bash
# Scan events
python tools/utd_event_scan.py runs/<timestamp> --macro say

# Compare runs
python tools/golden_run_parity.py --run-a runs/A --run-b runs/B

# Check emissions
python tools/smoke_emissions.py --run runs/<timestamp>

# Generate heatmaps
python tools/vdm_events_heatmaps.py runs/<timestamp>
```

### Documentation
```bash
# View overview
less Derivation/VDM_OVERVIEW.md

# Check validation status
cat Derivation/CANON_PROGRESS.md

# Review axioms
cat Derivation/AXIOMS.md

# Check roadmap
cat Derivation/ROADMAP.md
```

---

## Appendix C: Citation Information

### For Academic Papers

**APA Style:**
```
Lietz, J. K. (2025). Prometheus VDM: Provenance-Pack v0.1 [Computer software]. 
Neuroca, Inc. https://github.com/justinlietz93/Prometheus_VDM
```

**Chicago Style:**
```
Lietz, Justin K. 2025. "Prometheus VDM: Provenance-Pack v0.1." 
Computer software. Neuroca, Inc. 
https://github.com/justinlietz93/Prometheus_VDM.
```

**MLA Style:**
```
Lietz, Justin K. Prometheus VDM: Provenance-Pack v0.1. 
Neuroca, Inc., 2025. Software.
```

### For Software Citation (BibTeX)

```bibtex
@software{prometheus_vdm_2025,
  author = {Lietz, Justin K.},
  title = {Prometheus VDM: Provenance-Pack v0.1},
  year = {2025},
  publisher = {Neuroca, Inc.},
  url = {https://github.com/justinlietz93/Prometheus_VDM},
  version = {0.1},
  license = {Dual Academic Research / Commercial},
  note = {First public release with maturity ladder commitment}
}
```

### For Specific Results

When citing specific validated results, include artifact paths:

```bibtex
@misc{vdm_fisher_kpp_2025,
  author = {Lietz, Justin K.},
  title = {Fisher-KPP Front Speed Validation in Prometheus VDM},
  year = {2025},
  howpublished = {Prometheus VDM, Provenance-Pack v0.1},
  note = {Artifact: Derivation/code/outputs/figures/reaction_diffusion/rd_front_speed_experiment_20250824T053748Z.png}
}
```

---

**End of Release Notes**
