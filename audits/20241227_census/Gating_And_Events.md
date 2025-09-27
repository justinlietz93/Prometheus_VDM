# Event-Driven & Gating Inventory

## Event Types and Schema

### Bus Event Types (AnnounceBus)
| Event | Producer | Consumer | TTL | Hysteresis | Refractory | Budget |
|-------|----------|----------|-----|------------|------------|--------|
| region_stat | Void walkers | ADC | N/A | N/A | N/A | visits/edges |
| boundary_probe | Void walkers | ADC | N/A | N/A | N/A | visits/edges |
| cycle_hit | Void walkers | ADC | N/A | N/A | N/A | visits/edges |
| novel_frontier | Void walkers | ADC | N/A | N/A | N/A | visits/edges |

### Internal Event Types (Proprioception)
| Event | Producer | Consumer | TTL | Hysteresis | Refractory | Budget |
|-------|----------|----------|-----|------------|------------|--------|  
| VTTouchEvent | Void walkers | EventDrivenMetrics | N/A | N/A | N/A | visits |
| EdgeOnEvent | Void walkers | EventDrivenMetrics | N/A | N/A | N/A | edges |
| EdgeOffEvent | GDSP | EventDrivenMetrics | N/A | N/A | N/A | N/A |
| DeltaEvent | Learning | EventDrivenMetrics | N/A | N/A | N/A | N/A |
| SpikeEvent | Neurons | EventDrivenMetrics | N/A | N/A | N/A | N/A |
| ADCEvent | ADC | Telemetry | N/A | N/A | N/A | N/A |
| BiasHintEvent | Various | Consumers | ttl field | N/A | N/A | N/A |

## Gate Signal Computation

### B1 Gate (void_b1.py)
**Location**: `fum_rt/core/void_b1.py`
**Computation**: Euler-rank estimate: `E_active - V_active + C_active`
**Thresholds**: Not explicitly gated; provides continuous signal
**Hysteresis**: None detected
**Budget**: Sampling-based to keep O(E_active)

### Spike Detection Gate (metrics.py)  
**Location**: `fum_rt/core/metrics.py:65`
**Thresholds**: 
- `z_spike: float = 3.0` - threshold to enter spiking
- `hysteresis: float = 1.0` - subtracted from z_spike to exit
**Hysteresis**: `low = max(0.0, self.z_spike - self.hysteresis)`
**Refractory**: `min_interval_ticks: int = 10` - minimum ticks between spikes
**Budget**: None

### Walker Budget Gates
**Location**: `fum_rt/core/cortex/void_walkers/base.py`
**Budgets**:
- `budget_visits: int = 16` - node touches per step
- `budget_edges: int = 8` - edge probes per step  
- `ttl: int = 64` - max walk depth per seed
**Enforcement**: Hard limits in walker step() functions

## ADC Territory Management

### Territory TTL
**Location**: `fum_rt/core/adc.py`
**Mechanism**: Each territory has TTL that decays unless reinforced
**Values**: TTL configured in ADC constructor, decremented per tick
**Hysteresis**: Confidence-based territory creation/deletion

### Boundary TTL
**Location**: `fum_rt/core/adc.py`  
**Mechanism**: Boundaries between territories have separate TTL
**Decay**: Boundary strength decays without reinforcement
**Hysteresis**: Cut strength thresholds for boundary creation/removal

## Refractory Windows

### Spike Refractory
**Location**: `fum_rt/core/metrics.py:65`
**Window**: `min_interval_ticks: int = 10`
**Mechanism**: Prevents spike detection for 10 ticks after previous spike
**Implementation**: Tracks `last_spike_tick` per detector

### No Global Refractory Detected
- No system-wide refractory periods found
- No per-node refractory windows in connectome
- No ADC territory creation cooldowns

## Budget Envelopes

### Walker Budgets (Per-Step)
- **Visits**: 16 node touches maximum per walker step
- **Edges**: 8 edge probes maximum per walker step
- **TTL**: 64 steps maximum walk depth from each seed

### System-Level Budgets
- **AnnounceBus**: 65536 event capacity (overwrite-on-full)
- **ADC Drain**: 2048 events maximum per drain operation
- **GDSP Operations**: No explicit budgets detected

### Territory-Specific Budgets
- **ADC Territory Mass**: Tracked but no hard limits
- **Boundary Count**: No explicit limits per territory
- **Memory Allocation**: No detected memory budgets

## Event-Local Verification

### Local Operation Compliance
✅ **Void Walkers**: TTL-limited local exploration, neighbor-only access
✅ **GDSP**: Local sparse matrix operations (tolil/tocsr pattern)  
✅ **ADC**: O(1) per-event territory updates
✅ **Event Bus**: FIFO with bounded capacity

### Externalization Gates
✅ **Walker Events**: All operations emit events rather than direct writes
✅ **Bus Decoupling**: Producers/consumers decoupled via event bus
✅ **Metrics**: Event-driven metrics fold events instead of scanning structures

## Gate Signal Sources

### B1 Persistence Signal
**Location**: Various GDSP triggers
**Source**: `b1_persistence: float` parameter in GDSP operations
**Usage**: Triggers pruning when > 0.9 threshold
**Hysteresis**: None detected

### Domain Modulation
**Location**: `fum_rt/core/void_dynamics_adapter.py`
**Function**: `get_domain_modulation()`
**Usage**: Modulates connectome step operations
**Gates**: Applied to SIE drive and time dynamics

## Missing Gating Elements

- No explicit refractory windows for GDSP operations
- No budget limits on ADC territory creation
- No hysteresis for walker budget adaptation
- No system-wide backpressure mechanisms beyond bus capacity