# Changelog

All notable changes to the Prometheus_VDM (FUM Real-Time Runtime) project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-26

### Added
- FUM Real-Time Runtime (Scaffold v3) - Core runtime system
- Universal Temporal Encoder (UTE) for input processing
- Universal Transduction Decoder (UTD) for output generation
- CoreEngine with Connectome graph system using kNN-ish topology
- Vectorized void dynamics with domain-specific modulation support
- Real-time orchestration at configurable Hz (default 10 Hz)
- Checkpoint system with HDF5 and NPZ fallback support
- Dashboard and connectome visualization via matplotlib
- Event-driven metrics system with observation folding
- Macro board and phrase bank for structured language output
- Lexicon learning from inputs and outputs
- CLI interface via `python -m fum_rt.run_nexus`
- Web dashboard via `python fum_live.py`
- Modular architecture with clean separation of concerns:
  - Runtime components (loop, telemetry, orchestrator, helpers)
  - Core components (engine, signals, connectome, metrics, memory)
  - I/O components (UTE, UTD, lexicon store)
  - Physics integration (void dynamics adapter)
- Developer utilities:
  - UTD event scanner (`tools/utd_event_scan.py`)
  - Golden run parity harness (`tools/golden_run_parity.py`)
  - Smoke emissions verifier (`tools/smoke_emissions.py`)
  - Geometry bundle automation (`tools/geom_bundle_builder.py`)
- Comprehensive documentation in README
- Support for multiple domains: quantum, standard_model, dark_matter, biology_consciousness, cosmogenesis, higgs
- Configurable visualization and checkpoint intervals
- Speak auto-gating with valence and topology spike detection
- External control-plane via phase.json profiles
- Checkpoint retention policy management

### Features
- Sparse, efficient graph operations with vectorized updates
- Event-driven architecture with JSONL structured logging
- Deterministic template filling for language generation
- Adaptive cadence with entropy modulation
- B1 topology detector for structural analysis
- Configurable seed for reproducibility
- Time dynamics toggle for physics experiments
- Cold scouts for void exploration (telemetry-only)
- IDF-based composer novelty gain (telemetry-only)
- Thought ledger emission system
- Multi-session support via run directories

[1.0.0]: https://github.com/justinlietz93/Prometheus_VDM/releases/tag/v1.0.0
