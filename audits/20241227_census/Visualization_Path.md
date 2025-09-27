# Visualization Surface (Void Maps)

## Core Visualization Infrastructure

### Basic Visualizer (Core)
**Location**: `fum_rt/core/visualizer.py`
**Classes**: `Visualizer`
**Capabilities**:
- Dashboard plots (sparsity, weights, cohesion, complexity over time)
- Simple graph rendering using NetworkX spring layout
- Static PNG output to run directory

### Advanced Void-Driven Layout
**Location**: `fum_rt/frontend/plugins/fum_visualizer_v1/fum_visualizer.py`
**Function**: `void_driven_layout(W, iterations=50, dim=3)`
**Algorithm**: Void dynamics for organic, biologically plausible positioning

## Coordinate Derivation Methods

### 1. NetworkX Spring Layout (Basic)
**Location**: `fum_rt/core/visualizer.py:82`
```python
pos = nx.spring_layout(G, seed=42, dim=2)
```
**Properties**:
- Force-directed layout with spring constraints
- Fixed seed (42) for reproducible positioning
- 2D coordinates only
- **Global recompute**: Yes - rebuilds entire layout each time

### 2. Void-Driven Layout (Advanced)
**Location**: `fum_rt/frontend/plugins/fum_visualizer_v1/fum_visualizer.py:14`
```python
def void_driven_layout(W, iterations=50, dim=3):
```
**Algorithm Details**:
- Attraction via edge weights and void dynamics
- Repulsion via void pressure (adaptive subsampling for N > 800)
- 3D coordinate space support
- O(E) attraction, O(N²) or O(N×400) repulsion
- **Global recompute**: Yes - iterative force simulation

### 3. Memory Steering Coordinates
**Location**: `fum_rt/physics/memory_steering/memory_steering.py:238`
```python
pos: positions array of shape (N, d) giving coordinates for nodes
```
**Purpose**: Geometric coordinates for heading-aware navigation
**Usage**: Physics experiments and memory steering validation

## Update Frequency Analysis

### Dashboard Updates
**Trigger**: `viz_every` parameter in run profiles
**Example**: `"viz_every": 100` (every 100 ticks)
**Content**: Time series plots, no spatial layout
**Cost**: O(history_length) - safe for hot path

### Graph Visualization Updates  
**Trigger**: Manual/on-demand via visualizer.graph()
**Frequency**: Not integrated into main loop
**Cost**: O(E + N²) for spring layout - expensive

### Void Layout Updates
**Trigger**: Manual invocation of void_driven_layout()
**Iterations**: 50 default (configurable)  
**Cost**: O(iterations × (E + N×400)) - very expensive

## Global Recompute Triggers

### ⚠️ Hot Path Violations

#### 1. NetworkX Spring Layout
```python
pos = nx.spring_layout(G, seed=42, dim=2)
```
**Issue**: Full graph layout recomputation
**Complexity**: O(N²) force simulation
**Trigger**: Each graph() call

#### 2. Void-Driven Force Simulation
```python
for t_idx in range(iterations):
    # Repulsion calculation for all node pairs
    delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
```
**Issue**: N×N distance matrix for repulsion (N ≤ 800)
**Complexity**: O(iterations × N²)
**Mitigation**: Subsampling for N > 800

### Safe Incremental Operations

#### ✅ Dashboard Time Series
- Appends new data points to existing plots
- No layout recomputation
- O(1) per new data point

#### ✅ Memory Steering Coordinates
- Uses provided coordinates, no layout computation
- O(1) coordinate lookup for navigation

## Layout Algorithm Details

### Void-Driven Layout Implementation
**Attraction Force**:
```python
# O(E) sparse accumulation
attraction = np.zeros((num_nodes, dim))
np.add.at(attraction, rows, void_force_direction * weights[:, np.newaxis])
```

**Repulsion Force** (N ≤ 800):
```python
# O(N²) all-pairs repulsion
delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
repulsive_force = (1.0 / distance) * (1.0 - (1.0 / distance))
```

**Repulsion Force** (N > 800):
```python
# O(N×400) subsampled repulsion
P = min(400, num_nodes)
idx = np.random.choice(num_nodes, P, replace=False)
```

### NetworkX Spring Layout
- Uses Fruchterman-Reingold algorithm
- Iterative force-directed positioning
- Fixed number of iterations
- No incremental updates possible

## Hot vs Safe Code Paths

### 🔥 Hot Path (Expensive - Avoid in Main Loop)
1. **nx.spring_layout()** - O(N²) force simulation
2. **void_driven_layout()** - O(iterations × N²) void dynamics
3. **Full graph rendering** - matplotlib figure generation + PNG export
4. **plotly 3D visualization** - interactive plot generation

### ✅ Safe Path (Incremental/Bounded)
1. **Dashboard time series** - append-only data visualization
2. **Coordinate lookup** - O(1) position queries from pre-computed layouts
3. **Statistics plotting** - bounded history buffers
4. **Selective node highlighting** - modify existing visualization

## Visualization Configuration

### Run Profile Settings
**Example**: `run_profiles/1kN_viz.json`
```json
{
  "viz_every": 100,      // Visualization update frequency
  "neurons": 1000,       // Network size (affects layout cost)
  "status_interval": 1   // Dashboard update frequency
}
```

### Output Paths
- **Dashboard**: `{run_dir}/dashboard.png`
- **Graph**: `{run_dir}/connectome.png` (or custom fname)
- **Control URL**: `{run_dir}/control.json` (if available)

## Missing Incremental Features

### Not Implemented
1. **Tile-based layout** - No spatial partitioning for large networks
2. **Incremental force updates** - No delta-based position updates
3. **Level-of-detail rendering** - No adaptive resolution based on zoom
4. **Streaming visualization** - No real-time layout updates
5. **Void map caching** - No position cache/persistence between runs

### Void-Faithful Violations
1. **Global layout recomputation** - violates bounded operation principle
2. **O(N²) repulsion** - scales poorly with network size
3. **Full graph rendering** - no selective update capabilities
4. **Dense visualization** - no sparse-aware rendering optimizations

## Recommendations

### Immediate (Hot Path Safety)
1. **Disable auto-layout** - Remove layout computation from main loop
2. **Pre-compute coordinates** - Calculate layouts offline, load coordinates
3. **Tile-based rendering** - Implement spatial partitioning for large networks

### Short-term (Incremental Updates)
1. **Delta positioning** - Update only moved nodes
2. **Cached layouts** - Persist and reuse coordinate calculations
3. **Adaptive resolution** - Reduce detail for distant/inactive regions

### Long-term (Void-Faithful Visualization)
1. **Sparse rendering** - Visualize only active edges/nodes
2. **Walker-driven updates** - Use walker paths to guide visualization focus
3. **Territory-based views** - Render ADC territories as visual regions
4. **Event-driven updates** - Update visualization based on bus events

## Current Status Summary
- **Basic visualization**: Available but computationally expensive
- **Advanced void layout**: Implemented but not integrated into main loop
- **Incremental updates**: Missing - all visualizations require full recompute
- **Void-faithful compliance**: Poor - violates bounded operation principles
- **Hot path safety**: Dangerous - layout algorithms too expensive for real-time use