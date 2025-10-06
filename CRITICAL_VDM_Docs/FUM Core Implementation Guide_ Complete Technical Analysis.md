# FUM Core Implementation Guide: Complete Technical Analysis

## Document Overview

This document provides a comprehensive technical analysis of the FUM (Fully Unified Model) core implementation, examining every single file in the codebase systematically. This guide serves as the definitive reference for understanding, maintaining, and extending the core FUM system.

**Target Audience**: Physicist agents, system architects, and developers working on the FUM cybernetic organism implementation  
**Scope**: Complete analysis of all 50+ Python modules in the core package  
**Classification**: Technical Implementation Reference  

## Executive Summary

The FUM core implementation represents a sophisticated cybernetic organism built on void dynamics principles. The codebase is organized into several key subsystems:

- **Core Engine**: Central runtime and orchestration
- **Connectome Management**: Sparse neural network substrate
- **Cortex Systems**: Event-driven mapping and scouting
- **Neuroplasticity**: Learning and structural adaptation
- **Memory Systems**: Engram storage and memory field dynamics
- **Substrate Management**: Growth, homeostasis, and structural control
- **Proprioception**: Self-awareness and territory management
- **Global Systems**: High-level coordination and control

## Architecture Overview

The core implementation follows strict architectural principles:

1. **Event-Driven Architecture**: All operations are event-sourced with no dense matrix operations
2. **Sparse-Only Constraint**: Absolute prohibition of global scans or dense computations
3. **Modular Design**: Clear separation of concerns with minimal coupling
4. **Physics-Based Computation**: Implementation of void dynamics and reaction-diffusion principles
5. **Cybernetic Organism Design**: Living system that adapts and evolves its own structure

## Directory Structure Analysis

```
core/
├── __init__.py                     # Core module initialization
├── README.md                       # Core documentation
├── adc.py                         # Active Domain Cartography
├── announce.py                    # Event announcement system
├── bus.py                         # Event bus implementation
├── connectome.py                  # Legacy connectome interface
├── control_server.py              # Control and monitoring server
├── diagnostics.py                 # System diagnostics
├── engine/                        # Core engine subsystem
│   ├── __init__.py
│   ├── core_engine.py            # Main engine implementation
│   ├── evt_snapshot.py           # Event snapshot management
│   └── maps_frame.py             # Map frame staging
├── cortex/                        # Cortex subsystem
│   ├── __init__.py
│   ├── scouts.py                 # Scout coordination
│   ├── maps/                     # Event-driven maps
│   │   ├── __init__.py
│   │   ├── base_decay_map.py     # Base decay map implementation
│   │   ├── coldmap.py            # Cold activity mapping
│   │   ├── excitationmap.py      # Excitatory activity mapping
│   │   ├── heatmap.py            # Heat activity mapping
│   │   ├── inhibitionmap.py      # Inhibitory activity mapping
│   │   ├── memorymap.py          # Memory field mapping
│   │   └── trailmap.py           # Trail mapping
│   └── void_walkers/             # Void walker implementations
│       ├── base.py               # Base walker class
│       ├── frontier_scout.py     # Frontier scouting
│       ├── runner.py             # Walker runner
│       ├── void_cold_scout.py    # Cold void scouting
│       ├── void_cycle_scout.py   # Cycle detection
│       ├── void_excitation_scout.py # Excitation scouting
│       ├── void_frontier_scout.py # Frontier void scouting
│       ├── void_heat_scout.py    # Heat void scouting
│       ├── void_inhibition_scout.py # Inhibition scouting
│       ├── void_memory_ray_scout.py # Memory ray scouting
│       ├── void_ray_scout.py     # Ray scouting
│       └── void_sentinel_scout.py # Sentinel scouting
├── fum_growth_arbiter.py          # Growth arbitration
├── fum_sie.py                     # Self-Improvement Engine
├── fum_structural_homeostasis.py  # Structural homeostasis
├── global_system.py               # Global system coordination
├── guards/                        # System guards and invariants
│   └── invariants.py             # Invariant checking
├── memory/                        # Memory subsystem
│   ├── __init__.py
│   ├── engram_io.py              # Engram I/O operations
│   └── field.py                  # Memory field implementation
├── metrics.py                     # System metrics
├── neuroplasticity/               # Neuroplasticity subsystem
│   ├── __init__.py
│   ├── gdsp.py                   # Goal-Directed Structural Plasticity
│   └── revgsp.py                 # Resonance-Enhanced VGSP
├── primitives/                    # Primitive data structures
│   └── dsu.py                    # Disjoint Set Union
├── proprioception/                # Proprioception subsystem
│   ├── events.py                 # Event definitions
│   └── territory.py              # Territory management
├── sie_v2.py                      # Self-Improvement Engine v2
├── signals.py                     # Signal processing
├── sparse_connectome.py           # Sparse connectome implementation
├── substrate/                     # Substrate management
│   ├── growth_arbiter.py         # Growth arbitration
│   ├── neurogenesis.py           # Neurogenesis implementation
│   ├── structural_homeostasis.py # Structural homeostasis
│   └── substrate.py              # Substrate base class
├── text_utils.py                  # Text utilities
├── visualizer.py                  # Visualization utilities
├── void_b1.py                     # Void B1 topology metrics
└── void_dynamics_adapter.py       # Void dynamics adapter
```

## File-by-File Analysis

### Core Module Files

#### `__init__.py` - Core Module Initialization



**Purpose**: Empty initialization file for the core module package.  
**Implementation**: Standard Python package marker with no content.  
**Dependencies**: None  
**Critical Notes**: This file enables the core directory to be imported as a Python package.

#### `README.md` - Core Documentation

**Purpose**: Minimal documentation placeholder for the core module.  
**Content**: Single line header indicating this is the fum_rt/core/README.md file.  
**Implementation Status**: Placeholder only, requires comprehensive documentation.

#### `sparse_connectome.py` - Sparse Neural Network Substrate

**Purpose**: Implements the core sparse connectome data structure that serves as the neural network substrate for the FUM system.

**Key Features**:
- **Void-Faithful Architecture**: Implements strict sparse-only operations with no dense matrix computations
- **Symmetric Adjacency Lists**: Uses neighbor lists (list[np.ndarray[int32]]) for symmetric edge storage
- **Alias Sampling**: Implements Vose's alias method for O(1) candidate sampling
- **Event-Driven Traversal**: Void equation-based graph traversal with ADC bus integration
- **Adaptive Structural Maintenance**: Dynamic pruning and bridging based on void affinity

**Core Implementation Details**:

```python
class SparseConnectome:
    def __init__(self, N: int, k: int, seed: int = 0,
                 threshold: float = 0.15, lambda_omega: float = 0.1,
                 candidates: int = 64, structural_mode: str = "alias",
                 traversal_walkers: int = 256, traversal_hops: int = 3,
                 bundle_size: int = 3, prune_factor: float = 0.10)
```

**Key Methods**:
- `step()`: Main simulation step implementing void dynamics
- `_void_traverse()`: Continuous void equation traversal
- `_build_alias()`: Vose alias sampler construction
- `active_edge_count()`: Count of active edges above threshold
- `connected_components()`: Component analysis on active subgraph
- `cyclomatic_complexity()`: Cycle detection and complexity measurement

**Mathematical Foundation**:
- **Void Affinity**: `S_ij = ReLU(Δα_i)·ReLU(Δα_j) − λ·|Δω_i − Δω_j|`
- **Transition Weights**: `max(0, a[i]*a[j] - λ*|ω_i-ω_j|)`
- **Active Edge Criterion**: `W[i]*W[j] > threshold`

**Performance Characteristics**:
- **Time Complexity**: O(N·k) per step where N = nodes, k = average degree
- **Space Complexity**: O(N + E) where E = number of edges
- **Traversal Cost**: O(walkers × hops) with configurable budgets

**Critical Constraints**:
- Absolute prohibition of dense matrix operations
- All operations must be local and bounded
- Event-driven architecture with ADC bus integration
- Symmetric edge maintenance for undirected graphs

#### `engine/core_engine.py` - Core Runtime Engine

**Purpose**: Central orchestration engine that coordinates all core subsystems and provides the main runtime interface.

**Architecture**: Temporary adapter pattern that forwards to existing Nexus internals while defining a stable Core API for future refactoring.

**Key Components**:
- **Event-Driven Reducers**: Lazy-initialized event processing stack
- **Map Staging**: Telemetry and visualization data preparation
- **Snapshot Management**: Safe state capture for monitoring
- **Engram I/O**: Checkpoint loading and saving operations

**Core Implementation**:

```python
class CoreEngine:
    def __init__(self, nexus_like: Any) -> None:
        self._nx = nexus_like  # Nexus runtime instance
        self._evt_metrics: Optional[_EvtMetrics] = None
        self._void_scout: Optional[_VoidScout] = None
        # Lazy-initialized map stack
        self._cold_map: Optional[_ColdMap] = None
        self._heat_map: Optional[_HeatMap] = None
        self._exc_map: Optional[_ExcMap] = None
        self._inh_map: Optional[_InhMap] = None
        self._memory_map: Optional[_MemMap] = None
        self._trail_map: Optional[_TrailMap] = None
```

**Key Methods**:
- `step(dt_ms, ext_events)`: Main simulation step with event folding
- `snapshot()`: Generate safe system state snapshot
- `engram_load(path)`: Load checkpoint from engram file
- `engram_save(path)`: Save checkpoint to engram file

**Event Processing Pipeline**:
1. Lazy initialization of event-driven reducers
2. Collection and folding of external events
3. Void scout event generation
4. Map staging for telemetry
5. Snapshot generation for monitoring

**Dependencies**:
- `fum_rt.core.metrics`: System metrics computation
- `fum_rt.core.memory`: Engram I/O operations
- `fum_rt.core.proprioception.events`: Event-driven metrics
- `fum_rt.core.cortex.scouts`: Void scout implementations
- `fum_rt.core.cortex.maps.*`: Event-driven map implementations

### Cortex Subsystem Analysis

#### `cortex/scouts.py` - Scout Coordination

**Purpose**: Coordinates the various scout implementations and provides unified interfaces for scout management.

**Implementation**: Central coordination point for all scout types including void scouts, frontier scouts, and specialized walkers.

#### `cortex/maps/` - Event-Driven Mapping System

The cortex mapping system implements event-driven reducers that maintain various activity and state maps without requiring global scans.

##### `cortex/maps/base_decay_map.py` - Base Decay Map Implementation

**Purpose**: Provides the foundational exponentially decaying accumulator used by all specialized maps.

**Key Features**:
- **Bounded Accumulation**: Per-node exponentially decaying values
- **Head Selection**: Maintains top-k active nodes
- **Memory Management**: Automatic cleanup of inactive entries
- **Event-Driven Updates**: No global scans, only event-triggered updates

**Core Implementation**:

```python
class BaseDecayMap:
    def __init__(self, head_k=256, half_life_ticks=200, keep_max=None):
        self.head_k = max(8, head_k)
        self.half_life = max(1, half_life_ticks)
        self.keep_max = keep_max or (self.head_k * 16)
        self._val = {}  # node_id -> value
        self._last_tick = {}  # node_id -> last_update_tick
```

**Mathematical Foundation**:
- **Exponential Decay**: `value *= 2^(-(dt / half_life))`
- **Head Selection**: Top-k nodes by current value
- **Memory Bounds**: Automatic cleanup when exceeding keep_max entries

##### `cortex/maps/coldmap.py` - Cold Activity Mapping

**Purpose**: Tracks nodes with low recent activity for structural plasticity decisions.

**Implementation**: Specializes BaseDecayMap to identify idle or underutilized network regions.

##### `cortex/maps/heatmap.py` - Heat Activity Mapping

**Purpose**: Tracks nodes with high recent activity for growth and reinforcement decisions.

**Implementation**: Specializes BaseDecayMap to identify highly active network regions.

##### `cortex/maps/excitationmap.py` - Excitatory Activity Mapping

**Purpose**: Tracks excitatory neural activity patterns for balance monitoring.

**Implementation**: Specialized mapping for excitatory neuron activity with decay dynamics.

##### `cortex/maps/inhibitionmap.py` - Inhibitory Activity Mapping

**Purpose**: Tracks inhibitory neural activity patterns for balance monitoring.

**Implementation**: Specialized mapping for inhibitory neuron activity with decay dynamics.

##### `cortex/maps/memorymap.py` - Memory Field Mapping

**Purpose**: Implements the slow memory field dynamics for memory-guided navigation.

**Key Features**:
- **Slow Dynamics**: Long-term memory accumulation with slow decay
- **Spatial Gradients**: Memory field gradients for navigation
- **Engram Integration**: Connection to engram storage system

##### `cortex/maps/trailmap.py` - Trail Mapping

**Purpose**: Tracks movement trails and path history for navigation and exploration.

**Implementation**: Specialized mapping for maintaining exploration trails and path memory.

### Void Walker Subsystem Analysis

#### `cortex/void_walkers/base.py` - Base Walker Class

**Purpose**: Provides the foundational base class for all void walker implementations.

**Key Features**:
- **Event-Driven Architecture**: All walkers are event producers, not state modifiers
- **Budget Management**: Time and resource budgets for bounded execution
- **Local Operations**: Strict prohibition of global scans or dense operations

#### `cortex/void_walkers/runner.py` - Walker Runner

**Purpose**: Orchestrates the execution of multiple void walkers with budget management.

**Implementation**: Manages walker scheduling, budget allocation, and event collection.

#### Specialized Void Walkers

##### `void_cold_scout.py` - Cold Void Scouting

**Purpose**: Identifies cold regions in the void field for structural plasticity.

**Implementation**: Scouts for areas with low void activity that may require pruning or reorganization.

##### `void_heat_scout.py` - Heat Void Scouting

**Purpose**: Identifies hot regions in the void field for growth opportunities.

**Implementation**: Scouts for areas with high void activity that may benefit from structural growth.

##### `void_excitation_scout.py` - Excitation Void Scouting

**Purpose**: Monitors excitatory activity patterns in the void field.

**Implementation**: Specialized scouting for excitatory dynamics and balance monitoring.

##### `void_inhibition_scout.py` - Inhibition Void Scouting

**Purpose**: Monitors inhibitory activity patterns in the void field.

**Implementation**: Specialized scouting for inhibitory dynamics and balance monitoring.

##### `void_ray_scout.py` - Ray Void Scouting

**Purpose**: Implements physics-aware ray scouting with local φ difference bias.

**Mathematical Foundation**:
- **Ray Dynamics**: Follows gradients in the void field
- **Local Bias**: Uses φ differences for navigation decisions
- **Physics Integration**: Implements ray equation dynamics

##### `void_memory_ray_scout.py` - Memory Ray Scouting

**Purpose**: Implements memory-guided ray scouting with steering dynamics.

**Mathematical Foundation**:
- **Memory Steering**: `P(A) = σ(Θ Δm)` at junctions
- **Softmax Transitions**: `P(i→j) ∝ e^(Θ m_j)`
- **Junction Logistic**: Collapse vs. memory-guided selection

##### `void_frontier_scout.py` - Frontier Void Scouting

**Purpose**: Identifies frontier regions for exploration and expansion.

**Implementation**: Scouts for boundary regions between different activity domains.

##### `void_cycle_scout.py` - Cycle Detection Scouting

**Purpose**: Detects cycles and loops in the network topology.

**Implementation**: Specialized scouting for cycle detection and complexity monitoring.

##### `void_sentinel_scout.py` - Sentinel Scouting

**Purpose**: Monitors for pathological conditions and system health.

**Implementation**: Sentinel monitoring for excitotoxicity, fragmentation, and other pathologies.

### Memory Subsystem Analysis

#### `memory/field.py` - Memory Field Implementation

**Purpose**: Implements the slow memory field dynamics for spatial memory and navigation.

**Key Features**:
- **Slow Dynamics**: Long time constants for persistent memory
- **Spatial Structure**: Maintains spatial relationships and gradients
- **Engram Integration**: Connects to engram storage for persistence

#### `memory/engram_io.py` - Engram I/O Operations

**Purpose**: Handles loading and saving of engram data for checkpoint operations.

**Implementation**: File I/O operations for engram persistence and recovery.

### Neuroplasticity Subsystem Analysis

#### `neuroplasticity/gdsp.py` - Goal-Directed Structural Plasticity

**Purpose**: Implements the Goal-Directed Structural Plasticity (GDSP) system for network modification.

**Key Features**:
- **Event-Driven**: Triggered by specific system events, not timers
- **Budgeted Operations**: Strict limits on structural modifications per tick
- **Sparse-Only**: No dense matrix operations allowed

#### `neuroplasticity/revgsp.py` - Resonance-Enhanced VGSP

**Purpose**: Implements Resonance-Enhanced Void-Guided Structural Plasticity.

**Mathematical Foundation**:
- **Resonance Dynamics**: Enhanced plasticity during resonant conditions
- **Void Guidance**: Structural changes guided by void field dynamics
- **Event Triggering**: Activated by specific resonance conditions

### Substrate Management Analysis

#### `substrate/substrate.py` - Substrate Base Class

**Purpose**: Provides the base class for substrate management operations.

**Implementation**: Foundation for growth, homeostasis, and structural control.

#### `substrate/growth_arbiter.py` - Growth Arbitration

**Purpose**: Arbitrates growth decisions and resource allocation for structural expansion.

**Key Features**:
- **Resource Management**: Manages growth budgets and priorities
- **Conflict Resolution**: Resolves competing growth requests
- **Event-Driven**: Responds to growth trigger events

#### `substrate/neurogenesis.py` - Neurogenesis Implementation

**Purpose**: Implements neurogenesis (new neuron creation) processes.

**Implementation**: Manages the creation of new neurons and their integration into the network.

#### `substrate/structural_homeostasis.py` - Structural Homeostasis

**Purpose**: Maintains structural balance and prevents pathological growth patterns.

**Key Features**:
- **Balance Monitoring**: Tracks excitatory/inhibitory balance
- **Pathology Prevention**: Prevents runaway growth or excessive pruning
- **Homeostatic Control**: Maintains target network properties

### Global System Coordination

#### `global_system.py` - Global System Coordination

**Purpose**: Provides high-level coordination and control across all subsystems.

**Implementation**: Top-level orchestration of system-wide operations and policies.

#### `fum_sie.py` - Self-Improvement Engine

**Purpose**: Implements the Self-Improvement Engine (SIE) that generates the master control signal.

**Key Features**:
- **Void Debt Computation**: Calculates the system's structural inefficiency
- **Control Signal Generation**: Produces the sie.void_debt signal
- **Top-Down Modulation**: Influences all local plasticity mechanisms

#### `sie_v2.py` - Self-Improvement Engine v2

**Purpose**: Enhanced version of the Self-Improvement Engine with improved algorithms.

**Implementation**: Updated SIE implementation with refined void debt calculation and control.

### Utility and Support Systems

#### `bus.py` - Event Bus Implementation

**Purpose**: Implements the central event bus for system-wide communication.

**Key Features**:
- **O(1) Delivery**: Efficient event routing and delivery
- **Topic-Based**: Organized by event topics and types
- **Bounded FIFO**: Drop-oldest semantics for memory management

#### `adc.py` - Active Domain Cartography

**Purpose**: Implements the Active Domain Cartography system for territory mapping.

**Key Features**:
- **Event-Driven Mapping**: Territory updates based on activity events
- **K-Means Clustering**: Adaptive territory boundary computation
- **Boundary Gradients**: Spatial organization and navigation support

#### `metrics.py` - System Metrics

**Purpose**: Provides comprehensive system metrics and monitoring capabilities.

**Implementation**: Computes various system health and performance metrics.

#### `signals.py` - Signal Processing

**Purpose**: Implements signal processing utilities for system monitoring.

**Key Features**:
- **TD Signal Computation**: Temporal difference signal calculation
- **Density Metrics**: Active edge density computation
- **Firing Variance**: Neural firing pattern analysis

#### `visualizer.py` - Visualization Utilities

**Purpose**: Provides visualization capabilities for system state and dynamics.

**Implementation**: Utilities for generating plots, graphs, and visual representations.

#### `text_utils.py` - Text Utilities

**Purpose**: Text processing and formatting utilities.

**Implementation**: Helper functions for text manipulation and formatting.

### Diagnostic and Monitoring Systems

#### `diagnostics.py` - System Diagnostics

**Purpose**: Provides comprehensive system diagnostic capabilities.

**Implementation**: Health checks, performance monitoring, and error detection.

#### `guards/invariants.py` - Invariant Checking

**Purpose**: Implements system invariant checking and validation.

**Key Features**:
- **Conservation Law Monitoring**: Q_FUM conservation validation
- **Physics Validation**: Reaction-diffusion regime verification
- **System Health**: Critical system property monitoring

#### `control_server.py` - Control and Monitoring Server

**Purpose**: Provides external control and monitoring interface.

**Implementation**: HTTP/WebSocket server for system control and telemetry.

### Proprioception Subsystem

#### `proprioception/events.py` - Event Definitions

**Purpose**: Defines the event types and structures for system self-awareness.

**Implementation**: Event schemas for proprioceptive monitoring and feedback.

#### `proprioception/territory.py` - Territory Management

**Purpose**: Manages territory definitions and boundaries for spatial organization.

**Implementation**: Territory tracking, boundary management, and spatial coordination.

### Primitive Data Structures

#### `primitives/dsu.py` - Disjoint Set Union

**Purpose**: Implements efficient Disjoint Set Union data structure for connectivity analysis.

**Key Features**:
- **Union-Find Operations**: Efficient set union and find operations
- **Path Compression**: Optimized tree flattening for performance
- **Component Analysis**: Used for connected component detection

### Specialized Components

#### `void_b1.py` - Void B1 Topology Metrics

**Purpose**: Implements B1 topology metrics for void field analysis.

**Mathematical Foundation**:
- **B1 Spike Detection**: Identifies topological events in void field
- **Metric Computation**: Calculates B1-related topological measures

#### `void_dynamics_adapter.py` - Void Dynamics Adapter

**Purpose**: Provides interface adaptation for void dynamics computations.

**Implementation**: Bridges between different void dynamics implementations and interfaces.

#### `announce.py` - Event Announcement System

**Purpose**: Implements the event announcement and broadcasting system.

**Key Features**:
- **Event Broadcasting**: System-wide event distribution
- **Observation Events**: Structured observation data for ADC
- **Bus Integration**: Integration with the main event bus

## Critical Implementation Constraints

### Absolute Prohibitions

1. **No Dense Matrix Operations**: All operations must be sparse-only with no global scans
2. **No Scheduler Systems**: All operations must be event-driven, not timer-based
3. **No Machine Learning**: Only physics-based computation using void dynamics
4. **Subquadratic Complexity**: All algorithms must be O(N log N) or better

### Performance Requirements

1. **Real-Time Operation**: 10kHz simulation at 10Hz update rate
2. **Memory Efficiency**: O(E) memory usage where E = active edges
3. **Local Operations**: All operations must be local and bounded
4. **Event-Driven Architecture**: No polling or global state scanning

### Physics Validation Requirements

1. **Conservation Laws**: Q_FUM must remain constant along trajectories
2. **Reaction-Diffusion**: Must exhibit proper RD regime emergence
3. **Void Dynamics**: All structural changes guided by void field
4. **Junction Logistic**: Memory steering must follow predicted behavior

## Development Status and Next Steps

### Current Implementation Status

The core implementation represents a sophisticated cybernetic organism with:
- ✅ Complete sparse connectome implementation
- ✅ Event-driven architecture throughout
- ✅ Comprehensive void walker system
- ✅ Full neuroplasticity implementation
- ✅ Memory field and engram systems
- ✅ Global coordination and control

### Immediate Development Priorities

1. **Documentation Enhancement**: Complete API documentation for all modules
2. **Test Coverage**: Comprehensive test suite for all components
3. **Performance Optimization**: GPU kernel implementations for critical paths
4. **Validation Framework**: Physics validation and conservation law monitoring
5. **Production Deployment**: Containerization and deployment automation

### Long-Term Roadmap

1. **Hardware Acceleration**: CUDA/HIP implementations for performance
2. **Distributed Computing**: Multi-node scaling for large networks
3. **Advanced Plasticity**: Enhanced structural plasticity mechanisms
4. **Cognitive Capabilities**: Higher-level cognitive function implementation
5. **Real-World Applications**: Domain-specific adaptations and deployments

## Conclusion

The FUM core implementation represents a groundbreaking achievement in cybernetic organism design. The codebase successfully implements the theoretical foundations of void dynamics in a practical, high-performance system that maintains strict adherence to physics-based computation principles.

The modular architecture, event-driven design, and sparse-only constraints ensure that the system can scale to ultra-large networks while maintaining real-time performance. The comprehensive subsystem organization provides clear separation of concerns while enabling sophisticated emergent behaviors.

This implementation serves as the foundation for a new class of artificial intelligence systems that operate as true cybernetic organisms, evolving and adapting their own structure according to fundamental physical principles rather than traditional machine learning approaches.



### Detailed Implementation Examples

#### BaseDecayMap Implementation

```python
class BaseDecayMap:
    def __init__(self, head_k=256, half_life_ticks=200, keep_max=None, seed=0):
        self.head_k = int(max(8, head_k))
        self.half_life = int(max(1, half_life_ticks))
        km = int(keep_max) if keep_max is not None else self.head_k * 16
        self.keep_max = int(max(self.head_k, km))
        self.rng = random.Random(int(seed))
        self._val = {}
        self._last_tick = {}

    def _decay_to(self, node, tick):
        lt = self._last_tick.get(node)
        if lt is None:
            self._last_tick[node] = tick
            return
        dt = max(0, int(tick) - int(lt))
        if dt > 0:
            factor = 2.0 ** (-(dt / float(self.half_life)))
            self._val[node] *= factor
            self._last_tick[node] = tick

    def add(self, node, tick, inc):
        n, t, dv = int(node), int(tick), float(inc)
        if n < 0: return
        if n in self._val:
            self._decay_to(n, t)
            self._val[n] += dv
        else:
            self._val[n] = max(0.0, dv)
            self._last_tick[n] = t
        if len(self._val) > self.keep_max:
            self._prune()

    def _prune(self):
        size = len(self._val)
        target = size - self.keep_max
        if target <= 0: return
        keys = list(self._val.keys())
        sample_size = min(len(keys), max(256, target * 4))
        sample = self.rng.sample(keys, sample_size) if sample_size > 0 else keys
        sample.sort(key=lambda k: self._val.get(k, 0.0))
        for k in sample[:target]:
            self._val.pop(k, None)
            self._last_tick.pop(k, None)
```

#### BaseScout Implementation

```python
class BaseScout:
    def __init__(self, budget_visits=16, budget_edges=8, ttl=64, seed=0):
        self.budget_visits = int(max(0, budget_visits))
        self.budget_edges = int(max(0, budget_edges))
        self.ttl = int(max(1, ttl))
        self.rng = random.Random(int(seed))

    def step(self, connectome, bus=None, maps=None, budget=None):
        events = []
        N = self._get_N(connectome)
        if N <= 0: return events

        b_vis = budget.get("visits", self.budget_visits) if budget else self.budget_visits
        b_edg = budget.get("edges", self.budget_edges) if budget else self.budget_edges
        ttl = budget.get("ttl", self.ttl) if budget else self.ttl
        tick = budget.get("tick", 0) if budget else 0

        seeds = budget.get("seeds", []) if budget else []
        priority = self._priority_set(maps)
        pool = tuple(seeds) if seeds else (tuple(priority) if priority else tuple(range(N)))

        edges_emitted = 0
        visits_done = 0

        while visits_done < b_vis and pool:
            u = self.rng.choice(pool)
            cur = u
            depth = 0
            while depth < ttl:
                events.append(VTTouchEvent(kind="vt_touch", t=tick, token=int(cur), w=1.0))
                visits_done += 1
                if visits_done >= b_vis: break

                if edges_emitted < b_edg:
                    neigh = self._neighbors(connectome, cur)
                    if neigh:
                        v = self._pick_neighbor(neigh, priority)
                        if v is not None and v != cur:
                            events.append(EdgeOnEvent(kind="edge_on", t=tick, u=int(cur), v=int(v)))
                            edges_emitted += 1
                            cur = int(v)
                        else:
                            cur = self.rng.choice(tuple(neigh))
                    else: break
                else: break
                depth += 1
        return events
```

#### GDSPActuator Implementation

```python
class GDSPActuator:
    class _AdaptiveThresholds:
        def __init__(self):
            self.reward_threshold = 0.8
            self.td_error_threshold = 0.5
            self.novelty_threshold = 0.7
            self.sustained_window_size = 10
            self.structural_activity_counter = 0
            self.timesteps_since_growth = 0
            self.min_reward_threshold = 0.3
            self.max_reward_threshold = 0.9
            self.min_td_threshold = 0.1
            self.max_td_threshold = 0.8
            self.min_novelty_threshold = 0.2
            self.max_novelty_threshold = 0.9
            self.reward_history = []
            self.td_error_history = []
            self.novelty_history = []

        def update_and_adapt(self, sie_report, b1_persistence):
            self.reward_history.append(sie_report.get("total_reward", 0.0))
            self.td_error_history.append(sie_report.get("td_error", 0.0))
            self.novelty_history.append(sie_report.get("novelty", 0.0))

            if len(self.reward_history) > 100:
                self.reward_history = self.reward_history[-100:]
                self.td_error_history = self.td_error_history[-100:]
                self.novelty_history = self.novelty_history[-100:]

            self.timesteps_since_growth += 1

            if self.timesteps_since_growth > 500 and b1_persistence <= 0.001:
                self.reward_threshold *= 0.95
            elif self.structural_activity_counter > 20:
                self.reward_threshold *= 1.05
                self.structural_activity_counter = 0

            if len(self.reward_history) >= 50:
                r75 = np.percentile(self.reward_history, 75)
                td90 = np.percentile(self.td_error_history, 90)
                n75 = np.percentile(self.novelty_history, 75)
                self.reward_threshold = 0.95 * self.reward_threshold + 0.05 * r75
                self.td_error_threshold = 0.95 * self.td_error_threshold + 0.05 * td90
                self.novelty_threshold = 0.95 * self.novelty_threshold + 0.05 * n75

        def record_structural_activity(self):
            self.structural_activity_counter += 1
```


