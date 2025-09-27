# Bus / Scoreboard / GDSP Contracts

## Event Bus Schema (AnnounceBus)

### Core Bus Interface
**Location**: `fum_rt/core/bus.py`

```python
class AnnounceBus:
    def __init__(self, capacity: int = 65536)
    def publish(self, obs: Any) -> None
    def drain(self, max_items: int = 2048) -> List[Any]
    def size(self) -> int
    def capacity(self) -> int
```

### Message Schema (Observation)
**Location**: `fum_rt/core/announce.py`

```python
@dataclass
class Observation:
    tick: int                                    # Event timestamp
    kind: str                                   # Event type (see below)
    nodes: List[int] = []                       # Visited nodes (≤256)
    centroid: Optional[Tuple[float, float, float]] = None
    w_mean: float = 0.0                         # Mean weight in sample
    w_var: float = 0.0                          # Weight variance in sample  
    s_mean: float = 0.0                         # Mean coupling strength
    cut_strength: float = 0.0                   # Boundary cut strength
    loop_len: int = 0                           # Cycle length
    loop_gain: float = 0.0                      # Cycle gain
    coverage_id: int = 0                        # Coverage bin (0-9)
    domain_hint: str = ""                       # Domain label
    meta: Dict[str, Any] = {}                   # Extension metadata
```

### Valid Event Kinds
- `"region_stat"` - Aggregate statistics over visited region
- `"boundary_probe"` - Evidence of territory boundary
- `"cycle_hit"` - Loop closure detection (B1 proxy)
- `"novel_frontier"` - New territory/domain discovery

## Scoreboard (ADC) Contracts

### ADC Interface
**Location**: `fum_rt/core/adc.py`

```python
class ADC:
    def __init__(self, alpha: float = 0.05, ttl_default: int = 120)
    def ingest(self, obs: Observation) -> None
    def snapshot(self) -> Dict[str, Any]
    def decay_step(self) -> None
```

### Territory Tracking
```python
@dataclass
class Territory:
    w_stats: _EWMA                              # Weight statistics (mean/var)
    s_stats: _EWMA                              # Coupling statistics  
    mass: float                                 # Support/evidence mass
    confidence: float                           # Territory confidence [0,1]
    ttl: int                                    # Time-to-live counter
    last_seen: int                              # Last reinforcement tick
```

### Boundary Tracking  
```python
@dataclass  
class Boundary:
    cut_stats: _EWMA                            # Cut strength statistics
    churn: float                                # Boundary instability
    ttl: int                                    # Time-to-live counter
    last_seen: int                              # Last evidence tick
```

### Quorum Logic
- **Territory Creation**: Single observation creates territory (no quorum)
- **Territory Decay**: TTL-based; decays without reinforcement
- **Boundary Formation**: Requires evidence of cut between territories
- **Confidence Updates**: EWMA-based reinforcement learning

### Hysteresis Mechanisms
- **Territory Deletion**: Confidence < threshold AND TTL expired
- **Boundary Removal**: Cut strength < threshold AND TTL expired  
- **Territory Merging**: Not implemented (future capability)

### Reason Codes
No explicit reason codes detected in current implementation. Territories tracked by composite key `(domain_hint, coverage_id)`.

## GDSP Contracts

### GDSP Interface
**Location**: `fum_rt/core/neuroplasticity/gdsp.py`

```python
class GDSPActuator:
    def run(self, substrate, sie_report, probe_analysis, territory_indices, 
           B_growth, B_prune, T_prune, b1_persistence=0.0) -> substrate
    def trigger_homeostatic_repairs(self, substrate, probe_analysis) -> substrate
    def trigger_performance_growth(self, substrate, sie_report, territory_indices, b1_persistence) -> substrate  
    def trigger_maintenance_pruning(self, substrate, T_prune, pruning_threshold) -> substrate
    def status_report(substrate) -> dict
```

### Substrate Requirements
```python
# Expected substrate attributes:
substrate.synaptic_weights          # scipy.sparse matrix
substrate.persistent_synapses       # scipy.sparse boolean matrix
substrate.firing_rates              # vector of firing rates
substrate.eligibility_traces        # eligibility trace matrix (optional)
```

### Available Patch Operations

#### 1. Homeostatic Bridge Creation
**Function**: `_grow_connection_across_gap()`
**Purpose**: Connect fragmented components
**Budget**: Single bridge per tick
**Pattern**: Random component pair → bridge with weight 0.01

#### 2. Reinforcement Growth  
**Function**: `_execute_reinforcement_growth()`
**Purpose**: Strengthen high-eligibility connections
**Budget**: Territory-scoped, eligibility-threshold gated
**Pattern**: `W[i,j] *= 1.1` where eligibility > threshold

#### 3. Exploratory Growth
**Function**: `_execute_exploratory_growth()`  
**Purpose**: Create new connections across territory boundaries
**Budget**: `max(8, len(territory_indices) // 16)` new edges
**Pattern**: Firing-rate similarity → bidirectional edges at weight 0.01

#### 4. Maintenance Pruning
**Function**: `trigger_maintenance_pruning()`
**Purpose**: Remove weak, non-persistent connections
**Budget**: Timer-based, threshold-gated
**Pattern**: Remove edges where `weight < threshold AND !persistent AND timer > T_prune`

### Budget Accounting
- **Bridge Budget**: 1 per tick during fragmentation
- **Growth Budget**: Territory-size proportional (territory_indices // 16)
- **Prune Budget**: Timer-based (T_prune cycles)
- **No global GDSP budget**: Operations are condition-triggered

### Counterfactual Pre-checks
- **Component Analysis**: Check connectivity before bridging
- **Eligibility Thresholding**: Check traces before reinforcement
- **Firing Rate Similarity**: Filter candidates by rate similarity
- **Persistence Check**: Avoid pruning persistent synapses

### Write Authority Pattern
All GDSP operations follow the same pattern:
1. **Read**: Access current state (substrate.synaptic_weights, etc.)
2. **Convert**: `W_lil = W.tolil()` for efficient modification
3. **Modify**: Local sparse updates `W_lil[i,j] = value`
4. **Commit**: `substrate.synaptic_weights = W_lil.tocsr()`

### Validation Interface
```python
def status_report(substrate) -> dict:
    return {
        "n_components": int,                    # Connected components count
        "total_synapses": int,                  # Total synapse count  
        "total_neurons": int,                   # Total neuron count
        "avg_degree": float,                    # Average degree
        "persistent_synapses": int,             # Persistent synapse count
        "persistence_ratio": float              # Persistent/total ratio
    }
```

## Contract Violations

### Bus Contract Issues
- No explicit message size limits beyond nodes (≤256)
- No rate limiting or backpressure beyond capacity  
- No message ordering guarantees

### ADC Contract Issues  
- Territory identity function is simplistic (domain_hint, coverage_id)
- No explicit territory capacity limits
- No boundary strength normalization

### GDSP Contract Issues
- No explicit operation budgets or rate limits
- No atomic transaction semantics across operations
- No rollback mechanism for failed operations
- substrate mutations occur in-place without backup