# FUM Real-Time Runtime (fum_rt) Architecture Documentation

## Overview

The FUM Real-Time Runtime (fum_rt) is a minimal, production-oriented runtime system that implements the Nexus ⇄ UTE/UTD vision for continuous operation with void dynamics. It runs at configurable frequencies (default 10Hz), ingests input through Universal Temporal Encoder (UTE), updates the connectome using void equations, logs metrics, and renders dashboards and connectome images.

**Entry Point**: [`python -m fum_rt.run_nexus`](fum_rt/run_nexus.py:1)

## Core Architecture

The system follows a modular monolith architecture with clean separation of concerns:

```
Presentation Layer (API/CLI) → Business Logic (Core Engine) → Domain Models ← Infrastructure (Data Access)
```

### Key Architectural Principles

- **Dependency Rule**: Outer layers depend on inner layers only through abstractions
- **File Size Limit**: No file exceeds 500 LOC (enforced through modular design)
- **Framework Independence**: Business logic contains no framework-specific code
- **Repository Pattern**: All data access through repository interfaces

## Directory Structure and Components

### Core Runtime Modules (`fum_rt/core/`)

#### 1. Substrate System (`fum_rt/core/substrate/`)

The computational medium representing the FUM's neural substrate:

- **[`substrate.py`](fum_rt/core/substrate/substrate.py:1)**: Main Substrate class (V4 merged architecture) with GPU/CPU support
  - Manages Computational Units (CUs) with 80% excitatory/20% inhibitory ratio
  - Handles neuron parameters: tau_m, v_rest, v_thresh, refractory periods
  - Device-aware backend (NumPy for CPU, PyTorch for GPU)

- **[`neurogenesis.py`](fum_rt/core/substrate/neurogenesis.py:1)**: Growth manager for adding new neurons
  - Expands connectome using void dynamics for connection formation
  - Maintains structural integrity during growth operations
  - CPU-first initialization with device-specific transfer

- **[`structural_homeostasis.py`](fum_rt/core/substrate/structural_homeostasis.py:1)**: Self-regulating structural maintenance
  - Adaptive pruning based on mean weight thresholds
  - Cohesion-driven growth to heal fragmentation
  - Bundle-based bridging between disconnected components

#### 2. Neuroplasticity Algorithms (`fum_rt/core/neuroplasticity/`)

- **[`gdsp.py`](fum_rt/core/neuroplasticity/gdsp.py:1)**: Goal-Directed Structural Plasticity actuator
  - Homeostatic repairs with component-bridging caps
  - Performance-driven growth via eligibility percentiles
  - Maintenance pruning of weak, non-persistent synapses
  - Budget-controlled operations with territory scoping

- **[`revgsp.py`](fum_rt/core/neuroplasticity/revgsp.py:1)**: Resonance-Enhanced Valence-Gated Synaptic Plasticity
  - Reward-sigmoid scaled learning with PI kernel parameters
  - Budgeted pair sampling (no global candidate sweeps)
  - CSR-safe updates for eligibility traces and weights

#### 3. Cortex System (`fum_rt/core/cortex/`)

**Maps** (`fum_rt/core/cortex/maps/`):
- **[`heatmap.py`](fum_rt/core/cortex/maps/heatmap.py:1)**: Recency-weighted activity map with short half-life
- **[`memorymap.py`](fum_rt/core/cortex/maps/memorymap.py:1)**: Memory-driven scoring with percentile tracking
- **[`excitationmap.py`](fum_rt/core/cortex/maps/excitationmap.py:1)**: Excitation-focused scoring
- **[`inhibitionmap.py`](fum_rt/core/cortex/maps/inhibitionmap.py:1)**: Inhibition-driven scoring
- **[`coldmap.py`](fum_rt/core/cortex/maps/coldmap.py:1)**: Low-activity region tracking
- **[`trailmap.py`](fum_rt/core/cortex/maps/trailmap.py:1)**: Exploration path history

**Void Walkers** (`fum_rt/core/cortex/void_walkers/`):
- **[`base.py`](fum_rt/core/cortex/void_walkers/base.py:1)**: Base scout class with bounded TTL-limited exploration
- **Specialized Scouts**:
  - [`void_heat_scout.py`](fum_rt/core/cortex/void_walkers/void_heat_scout.py:1): Activity-driven routing
  - [`void_memory_ray_scout.py`](fum_rt/core/cortex/void_walkers/void_memory_ray_scout.py:1): Memory-steered navigation
  - [`void_excitation_scout.py`](fum_rt/core/cortex/void_walkers/void_excitation_scout.py:1): Excitation-focused routing (+1 spike events)
  - [`void_inhibition_scout.py`](fum_rt/core/cortex/void_walkers/void_inhibition_scout.py:1): Inhibition-driven routing (-1 spike events)
  - [`void_cycle_scout.py`](fum_rt/core/cortex/void_walkers/void_cycle_scout.py:1): Short-cycle detection
  - [`void_frontier_scout.py`](fum_rt/core/cortex/void_walkers/void_frontier_scout.py:1): Frontier exploration with cold/heat balancing
  - [`void_sentinel_scout.py`](fum_rt/core/cortex/void_walkers/void_sentinel_scout.py:1): Coverage monitoring
  - [`void_cold_scout.py`](fum_rt/core/cortex/void_walkers/void_cold_scout.py:1): Low-activity region exploration
  - [`void_ray_scout.py`](fum_rt/core/cortex/void_walkers/void_ray_scout.py:1): Physics-aware φ gradient routing

- **[`runner.py`](fum_rt/core/cortex/void_walkers/runner.py:1)**: Scout execution orchestrator with microsecond budgeting
- **[`scouts.py`](fum_rt/core/cortex/scouts.py:1)**: Scout factory and management

#### 4. Engine and Memory Components

- **[`core_engine.py`](fum_rt/core/engine/core_engine.py:1)**: Main execution engine with step processing (531 LOC)
  - **CoreEngine Class**: Temporary adapter to Nexus internals with stable API definition
  - **Step Processing**: [`step()`](fum_rt/core/engine/core_engine.py:82) folds event-driven reducers and stages maps/frame for telemetry
    - External events folding with cold-map updates
    - VOID cold-scout reads and event generation
    - Heat/excitation/inhibition maps folding
    - Maps/frame staging for UI bus
    - Event-driven snapshot refresh
  - **Initialization**: [`_ensure_evt_init()`](fum_rt/core/engine/core_engine.py:264) lazily initializes event-driven reducers and scouts
  - **Connectome Interface**: Stimulation, stepping, metrics computation, and snapshotting
  - **Numeric Helpers**: Active edge density, TD signal, firing variance computations
  - **Engram Operations**: [`engram_load()`](fum_rt/core/engine/core_engine.py:500) and [`engram_save()`](fum_rt/core/engine/core_engine.py:509) pass-through to legacy loaders/savers
- **[`connectome.py`](fum_rt/core/connectome.py:1)**: kNN-style graph with vectorized updates and cyclomatic complexity metrics
- **[`sparse_connectome.py`](fum_rt/core/sparse_connectome.py:1)**: Sparse matrix implementation for large-scale networks (705 LOC)
- **[`memory.py`](fum_rt/core/memory.py:1)**: Engram snapshot management (.npz/.h5 formats)
- **[`engram_io.py`](fum_rt/core/memory/engram_io.py:1)**: Persistent state save/load operations
- **[`field.py`](fum_rt/core/memory/field.py:1)**: Memory field management and access

#### 5. Support Modules

- **[`void_dynamics_adapter.py`](fum_rt/core/void_dynamics_adapter.py:1)**: Dynamic loading of void equations with fallback stubs
- **[`metrics.py`](fum_rt/core/metrics.py:1)**: Sparsity, cohesion, and complexity metrics
- **[`visualizer.py`](fum_rt/core/visualizer.py:1)**: Dashboard and graph rendering (matplotlib)
- **[`signals.py`](fum_rt/core/signals.py:1)**: Signal processing and event handling
- **[`adc.py`](fum_rt/core/adc.py:1)**: Analog-to-Digital conversion utilities
- **[`guards/invariants.py`](fum_rt/core/guards/invariants.py:1)**: System invariant checks and validation

### API and Integration Layers (`fum_rt/api/`)

#### LLM Providers Integration
- **Google**: [`fum_rt/api/llms/providers/google/`](fum_rt/api/llms/providers/google/)
- **OpenAI**: [`fum_rt/api/llms/providers/openai/`](fum_rt/api/llms/providers/openai/)
- **Ollama**: [`fum_rt/api/llms/providers/ollama/`](fum_rt/api/llms/providers/ollama/)
- **XAI**: [`fum_rt/api/llms/providers/xai/`](fum_rt/api/llms/providers/xai/)
- **OpenRouter**: [`fum_rt/api/llms/providers/openrouter/`](fum_rt/api/llms/providers/openrouter/)

#### Server and Routes
- **[`server/`](fum_rt/api/server/)**: HTTP API server implementation
- **[`routes/`](fum_rt/api/routes/)**: REST endpoint definitions

### I/O System (`fum_rt/io/`)

- **[`ute.py`](fum_rt/io/ute.py:1)**: Universal Temporal Encoder (stdin, queue, synthetic tick sources)
- **[`utd.py`](fum_rt/io/utd.py:1)**: Universal Transduction Decoder (stdout, file sinks)
- **Lexicon Management**: Macro board, phrase bank, and vocabulary persistence

### Runtime Orchestration (`fum_rt/runtime/`)

- **[`nexus.py`](fum_rt/nexus.py:1)**: Main real-time orchestrator with phase control
- **[`loop/main.py`](fum_rt/runtime/loop/main.py:1)**: Core event processing loop (933 LOC)
- **[`telemetry.py`](fum_rt/runtime/telemetry.py:1)**: Comprehensive metrics collection and emission system (651 LOC)
  - **Frame Quantization**: [`_quantize_frame_v2_u8()`](fum_rt/runtime/telemetry.py:35) converts Float32 LE planar payloads to uint8 using per-channel max scaling
  - **Tile Metadata**: [`_add_tiles_meta()`](fum_rt/runtime/telemetry.py:138) injects tiling configuration for large-N visualization
  - **Macro Why Base**: [`macro_why_base()`](fum_rt/runtime/telemetry.py:240) constructs base telemetry dict for macro emissions
  - **Status Payload**: [`status_payload()`](fum_rt/runtime/telemetry.py:269) builds open UTD status payload with identical keys and casts
  - **Tick Processing**: [`tick_fold()`](fum_rt/runtime/telemetry.py:337) orchestrates per-tick telemetry folding:
    - Bus draining and void topic symbol derivation
    - ADC metrics updating and event-driven metrics folding
    - Maps/frame publishing with FPS limiting and u8 quantization
    - Memory field telemetry exposure
    - B1 detector application via callback seam
- **[`phase.py`](fum_rt/runtime/phase.py:1)**: Dynamic profile switching system
- **[`orchestrator.py`](fum_rt/runtime/orchestrator.py:1)**: Thin façade over Nexus instance

## Key Functionalities

### 1. Real-Time Operation
- **10Hz default tick rate** with configurable frequency
- **Continuous input ingestion** through UTE
- **Vectorized connectome updates** using void dynamics
- **Structured logging** to `events.jsonl`
- **Automated checkpointing** with HDF5/NPZ fallback

### 2. Domain Modulation
- **Domain-specific scaling** of void equations
- **Supported domains**: quantum, standard_model, dark_matter, biology_consciousness, cosmogenesis, higgs
- **Custom modulation** through `FUM_Void_Debt_Modulation.py`

### 3. Phase Control System
- **File-driven profile switching** via `phase.json`
- **Live parameter adjustment** without restart
- **Speak gating controls**: z-threshold, hysteresis, cooldown, valence
- **Connectome traversal tuning**: walkers, hops, bundle_size, prune_factor

### 4. Language Output System
- **Macro board registry** with auto-persistence
- **Phrase bank templates** for rich sentence generation
- **Lexicon learning** from input/output streams
- **Template placeholders**: {keywords}, {top1}, {top2}, metrics values

### 5. Topology Complexity Metrics
- **Cyclomatic complexity** as B1 proxy for speaking gates
- **Active edge counting** with component awareness
- **Streaming z-score detection** for event triggering

## Operational Characteristics

### Performance Constraints
- **Budget-controlled operations** across all subsystems
- **CSR-safe updates** for sparse matrix operations
- **Microsecond-level budgeting** for scout execution
- **Device-aware computation** (CPU/GPU transparent)

### Memory Management
- **Engram snapshots** with efficient serialization
- **Sparse matrix storage** for large connectomes
- **Streaming processing** to avoid full-memory loading

### Extension Points
- **Void equations** through external `FUM_Void_Equations.py`
- **Domain modulation** via `FUM_Void_Debt_Modulation.py`
- **Custom scouts** through base class inheritance
- **Profile definitions** in Nexus phase system

## Usage Examples

### Basic Execution
```bash
python -m fum_rt.run_nexus --neurons 800 --hz 10 --domain biology_consciousness --viz-every 5
```

### Phase Control
```json
// runs/<timestamp>/phase.json
{
  "phase": 1,
  "speak": {
    "speak_z": 2.5,
    "speak_hysteresis": 0.8,
    "speak_cooldown_ticks": 10,
    "speak_valence_thresh": 0.35
  },
  "connectome": {
    "walkers": 384,
    "hops": 4,
    "bundle_size": 3,
    "prune_factor": 0.10
  }
}
```

### Output Analysis
```bash
# Extract speaking events
python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --macro say

# Build vocabulary lexicon
python tools/utd_event_scan.py runs/2025-08-10_21-00-00 --emit-lexicon lexicon.json
```

## Compliance with Architecture Rules

The fum_rt implementation follows the Hybrid-Clean Architecture principles with some exceptions:

- ✅ **No outer→inner dependencies**: Presentation layers depend on core through interfaces
- ⚠️ **500 LOC limit**: Several files exceed 500 LOC limit:
  - [`fum_rt/runtime/loop/main.py`](fum_rt/runtime/loop/main.py:1) (933 LOC) - Core event processing loop
  - [`fum_rt/core/sparse_connectome.py`](fum_rt/core/sparse_connectome.py:1) (705 LOC) - Sparse matrix implementation
  - [`fum_rt/runtime/telemetry.py`](fum_rt/runtime/telemetry.py:1) (651 LOC) - Telemetry system
  - [`fum_rt/core/engine/core_engine.py`](fum_rt/core/engine/core_engine.py:1) (531 LOC) - Core execution engine
- ✅ **Framework-independent business logic**: Core algorithms use only NumPy/SciPy
- ✅ **POCO domain models**: All data objects are plain old Python objects
- ✅ **Repository pattern**: Data access through well-defined interfaces
- ✅ **Dependency injection**: Constructor-based injection throughout

### Architectural Violations and Refactoring Suggestions

**Files exceeding 500 LOC limit should be refactored:**

1. **`fum_rt/runtime/loop/main.py` (933 LOC)**
   - Split into: main loop orchestrator, phase handlers, and tick processors
   - Extract UTE ingestion, connectome updates, and output handling to separate modules

2. **`fum_rt/core/sparse_connectome.py` (705 LOC)**
   - Separate sparse matrix operations from graph analytics
   - Extract connectivity metrics (components, cyclomatic complexity) to dedicated module

3. **`fum_rt/runtime/telemetry.py` (651 LOC)**
   - Split frame quantization and tile metadata into `visualization/quantization.py`
   - Separate telemetry payload builders from tick processing logic
   - Move maps ring handling to I/O visualization module

4. **`fum_rt/core/engine/core_engine.py` (531 LOC)**
   - Decouple engine steps into phase-specific handlers
   - Extract memory field operations and scout execution to separate modules

This architecture ensures maintainability, testability, and the ability to evolve individual components without system-wide impact.

## Parameter Reference and Default Values

### Core System Parameters

**Network Structure:**
- `neurons`: 1000 - Total number of computational units (neurons)
- `k`: 12 - Average connectivity (edges per neuron)
- `neuron_type_ratio`: 80% excitatory, 20% inhibitory - Fixed ratio of neuron types

**Operational Timing:**
- `hz`: 10 - Default tick frequency (Hz)
- `status_interval`: 1 - Status reporting interval (ticks)
- `b1_half_life_ticks`: 50 - Half-life for B1 complexity metric decay

**Domain Configuration:**
- `domain`: 'biology_consciousness' - Default void dynamics domain
- `use_time_dynamics`: True - Enable time-based dynamics

### Connectome Traversal Parameters

**Walker Configuration:**
- `walkers`: 256 - Number of void walkers active per tick
- `hops`: 3 - Maximum hops per walker traversal
- `bundle_size`: 3 - Size of connection bundles for growth
- `candidates`: 64 - Number of candidate pairs for plasticity

**Structural Maintenance:**
- `threshold`: 0.15 - Weight threshold for pruning
- `lambda_omega`: 0.1 - Omega decay rate for plasticity
- `prune_factor`: 0.10 - Fraction of edges to consider for pruning

### Stimulation Parameters

**Text-to-Connectome Input:**
- `stim_group_size`: 4 - Neuron group size for symbol stimulation
- `stim_amp`: 0.05 - Stimulation amplitude
- `stim_decay`: 0.90 - Stimulation decay rate per tick
- `stim_max_symbols`: 64 - Maximum symbols processed per input

### Speech Generation Parameters

**Automatic Speaking:**
- `speak_auto`: True - Enable automatic speech generation
- `speak_z`: 1.0 - Z-score threshold for speaking triggers
- `speak_hysteresis`: 1.0 - Hysteresis buffer for speech gating
- `speak_cooldown_ticks`: 10 - Cooldown period between speeches
- `speak_valence_thresh`: 0.01 - Valence threshold for emotional content

### Announcement Bus Parameters

**ADC Tuning:**
- `bus_capacity`: 65536 - Maximum bus capacity for announcements
- `bus_drain`: 2048 - Drain rate per tick from bus
- `r_attach`: 0.25 - Attachment rate for new announcements
- `ttl_init`: 120 - Initial time-to-live for announcements
- `split_patience`: 6 - Patience threshold for topic splitting

### Visualization and Logging

**Output Control:**
- `viz_every`: 10 - Visualization update interval (ticks)
- `log_every`: 1 - Logging interval (ticks)
- `checkpoint_every`: 0 - Checkpoint interval (ticks, 0=disabled)
- `checkpoint_keep`: 5 - Number of checkpoints to retain

### Environment Variables

**Runtime Overrides:**
- `ENABLE_EVENT_METRICS=1` - Enable event-driven metrics (default)
- `ENABLE_COLD_SCOUTS=1` - Enable void cold scouts (default)
- `FORCE_DENSE=0` - Use sparse connectome (default), set to 1 for dense

### Memory and Learning Parameters

**EWMA Smoothing:**
- `alpha=0.15` - Smoothing factor for weight statistics
- `alpha=0.2` - Smoothing factor for cut statistics and churn

**Neurogenesis:**
- `seed=42` - Default random seed for reproducible growth

### Parameter Interactions and Dynamics

The system's behavior emerges from complex interactions between these parameters:

1. **Connectome Density**: Controlled by `k`, `prune_factor`, and `threshold` - higher values create denser, more connected networks with increased computational cost.

2. **Exploration vs Exploitation**: Balanced by `walkers`, `hops`, and `bundle_size` - more walkers with longer hops increase exploration but reduce depth.

3. **Plasticity Rates**: `lambda_omega` and `candidates` determine how quickly the connectome adapts to new information versus maintaining stability.

4. **Speech Generation**: Governed by `speak_z`, `speak_hysteresis`, and `b1_half_life_ticks` - higher z-thresholds produce fewer but more significant utterances.

5. **Input Processing**: `stim_amp` and `stim_decay` control how strongly and persistently external stimuli affect the connectome.

6. **Memory Formation**: Influenced by `ttl_init` and `split_patience` - longer TTL allows richer topic development while patience controls topic segmentation.

These parameters are designed to work together within the void dynamics framework, where domain-specific modulation (`domain` parameter) scales the underlying equations appropriately for different physical regimes.
