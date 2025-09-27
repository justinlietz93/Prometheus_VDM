# GDSP Bypass Suspects

## Summary
Found several paths that mutate topology/weights outside the official GDSP authority. Most concerning are the NetworkX-based structural plasticity functions and direct adjacency matrix writes in physics modules.

## High-Risk Bypasses

### 1. Structural Plasticity Module (NetworkX mutations)
**Location**: `fum_rt/fum_advanced_math/structural_plasticity/apply_structural_plasticity.py`

```python
# Lines 40, 47, 52 - Direct NetworkX graph mutations
for u, v, data in list(graph.edges(data=True)):
    if data.get('weight', 0) < pruning_threshold:
        graph.remove_edge(u, v)  # BYPASS: Direct edge removal
        # ...
        graph.add_edge(u, new_neighbor, weight=pruning_threshold)  # BYPASS: Direct edge addition

if bdnf > growth_threshold and not graph.has_edge(u, v):
    graph.add_edge(u, v, weight=growth_threshold)  # BYPASS: Direct edge addition
```

**Risk**: High - directly mutates graph topology without GDSP coordination
**Impact**: Could conflict with GDSP decisions, break void-faithful contracts

### 2. Evolutionary Algorithms (Direct weight mutation)
**Location**: `fum_rt/fum_advanced_math/evolutionary/`

```python
# apply_recombination.py:39
new_weights[~recombination_mask] = weights2[~recombination_mask]  # BYPASS: Direct weight write

# apply_mutation.py:38  
mutated_weights[mutation_mask] += mutations[mutation_mask]  # BYPASS: Direct weight mutation
```

**Risk**: Medium - operates on weight arrays directly
**Impact**: Could interfere with GDSP weight management

### 3. Physics Memory Steering (Adjacency matrix writes)
**Location**: `fum_rt/physics/memory_steering/memory_steering.py`

```python
# Lines 385-405 - Direct adjacency matrix writes
A[t - 1, t] = 1  # BYPASS: Direct topology write
A[t, t - 1] = 1  # BYPASS: Direct topology write
A[len_in - 1, J] = 1  # BYPASS: Direct topology write
A[J, len_in - 1] = 1  # BYPASS: Direct topology write
```

**Risk**: Medium - physics validation context, but still bypasses GDSP
**Impact**: Creates test/validation graphs outside GDSP control

## Expected GDSP-Routed Operations

### Legitimate GDSP Operations
**Location**: `fum_rt/core/neuroplasticity/gdsp.py`

All weight/topology mutations in GDSP are properly routed:
- Lines 191-196: Homeostatic bridge creation via GDSP
- Lines 277-291: Reinforcement growth via GDSP  
- Lines 316-317: Exploratory growth via GDSP

These follow the pattern:
1. Convert to lil format: `W_lil = substrate.synaptic_weights.tolil()`
2. Make changes: `W_lil[i, j] = value`
3. Convert back: `substrate.synaptic_weights = W_lil.tocsr()`

## Recommendations

1. **Immediate**: Flag structural plasticity module as non-production (physics/validation only)
2. **Short-term**: Route all fum_advanced_math operations through GDSP interface
3. **Long-term**: Implement GDSP budget/permission system for external modules

## Code Pattern Analysis

**Safe Pattern** (GDSP-routed):
```python
def gdsp_operation():
    W_lil = substrate.synaptic_weights.tolil() 
    # mutations via W_lil[i,j] = value
    substrate.synaptic_weights = W_lil.tocsr()
```

**Unsafe Pattern** (Bypass):
```python
def direct_mutation():
    graph.add_edge(u, v)  # or adj[i,j] = value
```

The void-faithful contract requires all topology/weight mutations to flow through GDSP's single-writer authority.