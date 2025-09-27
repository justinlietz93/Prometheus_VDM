# Heterogeneous Neurons & ADC Territories

## Neuron Heterogeneity

### Discovered Neuron Types
Based on substrate implementation (`fum_rt/core/substrate/substrate.py`):

| Parameter | Type | Distribution | Default/Range |
|-----------|------|--------------|---------------|
| **Excitatory/Inhibitory** | Boolean | 80% Exc, 20% Inh | Binary classification |
| **Tau_m** | Membrane time constant | Normal(20.0, √2) ms | Temporal dynamics |
| **V_thresh** | Threshold voltage | Normal(-55.0, √2) mV | Spike threshold |
| **V_rest** | Resting potential | Fixed | -65.0 mV |
| **V_reset** | Reset voltage | Fixed | -70.0 mV |
| **Refractory_period** | Absolute refractory | Fixed | 5.0 ms |
| **R_mem** | Membrane resistance | Fixed | 10.0 Ω |

### Intrinsic Plasticity Parameters
**Location**: `fum_rt/core/substrate/substrate.py:48-54`

| Parameter | Purpose | Value/Range |
|-----------|---------|-------------|
| `ip_target_rate_min` | Min target firing rate | 0.1 Hz |
| `ip_target_rate_max` | Max target firing rate | 0.5 Hz |
| `ip_v_thresh_adjustment` | Threshold adaptation rate | 0.1 mV |
| `ip_tau_m_adjustment` | Time constant adaptation | 0.1 ms |
| `ip_v_thresh_bounds` | Threshold limits | (-60.0, -50.0) mV |
| `ip_tau_m_bounds` | Time constant limits | (15.0, 25.0) ms |

### SIE (Self-Improvement Engine) Components
**Location**: `fum_rt/fum_advanced_math/void_dynamics/sie_formulas.py`

| Component | Function | Purpose |
|-----------|----------|---------|
| **Novelty Score** | `calculate_novelty_score(N_s)` | Experience-based novelty |
| **Habituation** | Weight in SIE formula | Familiarity dampening |
| **Homeostatic Stability** | `calculate_hsi()` | System stability index |
| **TD Error** | Temporal difference | Learning signal |

### Missing Classical Neuron Types
**Not Found**:
- Rhythmic neurons (no intrinsic oscillators)
- Bursting neurons (basic burst detection only)
- Habituating neurons (habituation in SIE, not neuron-specific)
- Mirror neurons (no neighbor-mirroring behavior)
- Novelty detectors (novelty in SIE, not specialized neurons)

### Actual Heterogeneity Sources
1. **Stochastic Parameters**: Tau_m and V_thresh have Gaussian noise
2. **Binary Classification**: Excitatory vs inhibitory (80/20 split)  
3. **Intrinsic Plasticity**: Adaptive thresholds and time constants
4. **Connectivity**: k-NN graph initialization creates structural diversity

## ADC Territory System

### Territory Algorithm
**Location**: `fum_rt/core/adc.py`
**Method**: Composite key clustering, not spatial algorithms

```python
# Territory identity function
territory_key = (domain_hint, coverage_id)
# where coverage_id = int(coverage * 10.0) -> bins 0-9
```

### Territory Tracking Structure
```python
@dataclass
class Territory:
    w_stats: _EWMA        # Weight statistics (alpha=0.05)
    s_stats: _EWMA        # Coupling statistics  
    mass: float           # Evidence accumulation
    confidence: float     # Territory certainty [0,1]
    ttl: int             # Time-to-live countdown
    last_seen: int       # Last reinforcement tick
```

### Territory Parameters & Defaults

| Parameter | Purpose | Default | Notes |
|-----------|---------|---------|-------|
| `alpha` | EWMA decay rate | 0.05 | Statistics smoothing |
| `ttl_default` | Territory lifespan | 120 ticks | Without reinforcement |
| `max_nodes` | Node list limit | 256 | Per observation |
| `capacity` | Bus capacity | 65536 events | Overflow protection |

### Missing Spatial Algorithms
**Not Implemented**:
- Label propagation
- K-hop neighborhood clustering  
- Resistance distance measurement
- Spectral clustering
- Community detection algorithms

### Current Territory Formation
1. **Observation**: Walker emits region_stat event
2. **Key Generation**: `(domain_hint, coverage_id)` composite
3. **Territory Lookup**: Find or create territory for key
4. **EWMA Update**: Smooth statistics into territory
5. **TTL Management**: Refresh lifespan or decay

### Territory Boundary Detection
**Method**: Cut strength between territories
**Trigger**: `boundary_probe` events from walkers
**Storage**: Boundary objects with cut_stats EWMA and TTL

## Growth Direction & Budget Multipliers

### GDSP Territory Integration
**Location**: `fum_rt/core/neuroplasticity/gdsp.py`
**Territory Usage**: Territory indices passed to GDSP operations

### Growth Budgets (Territory-Scoped)
```python
# Exploratory growth budget
max_new = max(8, len(territory_indices) // 16)
# Scales with territory size, minimum 8 connections
```

### Missing Territory Priors
**Not Found**:
- Growth direction preferences per territory
- Budget multipliers per territory type
- Territory-specific plasticity rules
- Spatial growth biases

### Actual Territory Effects
1. **GDSP Scoping**: Operations limited to territory indices
2. **Budget Scaling**: Growth budget proportional to territory size
3. **ADC Tracking**: Territory statistics guide future operations
4. **Event Routing**: Observations route to appropriate territories

## Initialization Distributions

### Neuron Parameter Initialization
```python
# Membrane time constants
tau_m = np.random.normal(loc=20.0, scale=np.sqrt(2.0), size=num_neurons)

# Spike thresholds  
v_thresh = np.random.normal(loc=-55.0, scale=np.sqrt(2.0), size=num_neurons)

# Excitatory/Inhibitory assignment
is_excitatory = np.random.choice([True, False], p=[0.8, 0.2])
```

### Connectivity Initialization
**Method**: k-NN graph with excitatory/inhibitory weights
```python
W = create_knn_graph(num_neurons, k, is_excitatory).toarray()
```

### Territory Initialization
**Dynamic**: Territories created on-demand from walker observations
**No Preset**: No predefined territory structure or parameters

## Summary Tables

### Implemented Neuron Heterogeneity
| Feature | Implementation | Parameters |
|---------|----------------|------------|
| E/I Balance | Binary classification | 80% exc, 20% inh |
| Temporal Diversity | Gaussian tau_m | μ=20ms, σ=√2 |
| Threshold Variance | Gaussian v_thresh | μ=-55mV, σ=√2 |  
| Intrinsic Plasticity | Adaptive thresholds | Target 0.1-0.5 Hz |

### ADC Territory System
| Feature | Implementation | Parameters |
|---------|----------------|------------|
| Territory ID | Composite key | (domain_hint, coverage_id) |
| Statistics | EWMA tracking | α=0.05 smoothing |
| Lifespan | TTL decay | 120 tick default |
| Boundaries | Cut strength | EWMA + TTL |

### Missing Features
- Specialized neuron types (rhythmic, bursting, habituating)
- Spatial territory algorithms (label-prop, k-hop, resistance)
- Territory-specific growth priors and budget multipliers
- Morphological neuron classes beyond E/I
- Complex connectivity patterns beyond k-NN