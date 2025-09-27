# Architectural Map

## Core Components Overview

### RD Field Engine (Discrete Update, Reaction Terms)
- **Location**: `fum_rt/physics/rd_dispersion_runner.py`
- **Classes**: `run_linear_sim()` function
- **Summary**: Validates reaction-diffusion field dynamics with dispersion relation σ(k) = r - D k^2
- **Interaction**: Standalone validation; mirrors proven physics from derivation scripts

### Void Walkers (Policy; Hotspot Selection)
- **Location**: `fum_rt/core/cortex/void_walkers/`
- **Base Class**: `BaseScout` in `base.py`
- **Implementations**:
  - `HeatScout` - Heat-driven walker using heat_head/heat_dict priorities
  - `VoidRayScout` - Physics-aware routing along φ gradients  
  - `MemoryRayScout` - Memory-driven with Boltzmann choice P(i→j) ∝ exp(Theta * m[j])
  - Additional scouts: cold, cycle, excitation, inhibition, frontier, sentinel
- **Summary**: TTL-limited local exploration (budgeted visits/edges), emit compact events
- **Interaction**: Read connectome neighbors, consume maps, emit VTTouchEvent/EdgeOnEvent

### Event Bus (Topics, Schema)
- **Location**: `fum_rt/core/bus.py` + `fum_rt/core/announce.py`
- **Class**: `AnnounceBus` (bounded deque, overwrite-on-full)
- **Schema**: `Observation` events with kinds:
  - `region_stat` - aggregate stats (w_mean, w_var, s_mean, coverage_id)
  - `boundary_probe` - low-coupling cut evidence
  - `cycle_hit` - loop closure (B1 proxy)
  - `novel_frontier` - novelty ridge detection
- **Summary**: Lock-free FIFO for void-walker observations → ADC input
- **Interaction**: Walkers publish(), ADC/Nexus drain(max_items)

### Scoreboard (TTL, Quorum, Hysteresis)
- **Location**: `fum_rt/core/adc.py` (Active Domain Cartography)
- **Class**: `ADC` with internal `_EWMA` and territory tracking
- **Components**: 
  - Territories: `(domain_hint, coverage_id)` → stats, mass, confidence, TTL
  - Boundaries: cut_strength EWMA, churn, TTL between territories
- **Summary**: Incremental reducer consuming bus events, O(1) per event
- **Interaction**: Consumes AnnounceBus observations, provides map metrics

### GDSP (Single Topology/Weight Writer)
- **Location**: `fum_rt/core/neuroplasticity/gdsp.py`
- **Class**: `GDSPActuator`
- **Operations**:
  - `trigger_homeostatic_repairs()` - bridge fragmented components
  - `trigger_performance_growth()` - reinforcement/exploratory growth
  - `trigger_maintenance_pruning()` - weak synapse removal
- **Summary**: Exclusive authority for synaptic_weights/persistent_synapses mutation
- **Interaction**: Consumes substrate + analysis, returns modified substrate

### UTE/UTD (Encoder/Decoder Pipeline; Gates)
- **Location**: `fum_rt/io/ute.py` + `fum_rt/io/utd.py`
- **Classes**: `UTE` (encoder), `UTD` (decoder)
- **Summary**: Text encoding/decoding pipeline with gates
- **Interaction**: Text ↔ internal representations, integrated in Nexus

### ADC Territories (Analog Brain Sections)
- **Location**: `fum_rt/core/adc.py`
- **Algorithm**: Territory assignment by `(domain_hint, coverage_id)` composite key
- **Features**: EWMA stats, confidence tracking, TTL decay
- **Summary**: Coarse concept regions with incremental boundary detection

### Neuron Heterogeneity (Traits/Params; Distributions)
- **Location**: Distributed across connectome implementations
- **Traits**: Firing rates, synaptic weights, persistent synapses
- **Summary**: Sparse matrices store heterogeneous neuron parameters

### Void Map Visualization (Incremental Layout)
- **Location**: `fum_rt/core/visualizer.py`
- **Class**: `Visualizer`
- **Summary**: Rendering infrastructure for void map displays
- **Interaction**: Consumes connectome state, provides visual representations

## Flow Diagram (ASCII)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  UTE/UTD    │    │ Void Walkers│    │ RD Engine   │
│ (Pipeline)  │    │  (Scouts)   │    │(Validation) │
└──────┬──────┘    └──────┬──────┘    └─────────────┘
       │                  │
       │                  │ emit events
       │                  ▼
       │           ┌─────────────┐
       │           │ AnnounceBus │
       │           │  (Events)   │
       │           └──────┬──────┘
       │                  │ drain()
       │                  ▼
       │           ┌─────────────┐         ┌─────────────┐
       │           │     ADC     │◄────────┤    Maps     │
       │           │(Scoreboard) │         │ (Heat/Mem)  │
       │           └──────┬──────┘         └─────────────┘
       │                  │
       │                  │ territories/metrics
       │                  ▼
┌──────▼──────┐    ┌─────────────┐         ┌─────────────┐
│    Nexus    │◄───┤    GDSP     │◄────────┤ Connectome  │
│(Orchestrator│    │(Single      │         │(Sparse/     │
│   Loop)     │    │ Writer)     │         │ Dense)      │
└─────────────┘    └─────────────┘         └─────────────┘
```

## Key Interactions

1. **Nexus** orchestrates the main loop, coordinates all components
2. **Void Walkers** explore connectome locally, publish observations to bus
3. **AnnounceBus** provides event-driven messaging between walkers and ADC
4. **ADC** maintains incremental territory maps from walker observations
5. **GDSP** has exclusive write authority for topology/weight changes
6. **UTE/UTD** handle text encoding/decoding with gating mechanisms
7. **RD Engine** provides physics validation (standalone)
8. **Connectome** (sparse/dense) stores network state, provides neighbor queries

## Control Flow

1. Nexus initializes components (walkers, ADC, GDSP, connectome)
2. Main loop: walkers step() → emit events → bus collects → ADC processes
3. GDSP triggered based on analysis (homeostasis, growth, pruning)
4. UTE/UTD process text I/O with gating
5. Metrics/telemetry collected from all components
6. Visualization updated from connectome state