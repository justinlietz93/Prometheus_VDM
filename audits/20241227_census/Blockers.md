# Blockers Table

## Void-Faithfulness Risk Assessment

| Issue | Where | Why It Matters | Severity | Effort | Evidence |
|-------|-------|----------------|----------|--------|----------|
| **Global Weight Statistics** | `fum_rt/core/metrics.py:24` | Violates no-dense: `W.mean()` computes over all weights | High | S | [NoDense_Findings.md#high-severity](NoDense_Findings.md) |
| **Dense Adjacency Scanning** | `fum_rt/core/void_b1.py:262` | Violates locality: builds neighbor lists from full adjacency matrix | High | M | [NoDense_Findings.md#high-severity](NoDense_Findings.md) |
| **GPU-CPU Weight Transfer** | `fum_rt/core/substrate/neurogenesis.py:53` | Violates bounded ops: full matrix transfer `W.cpu().numpy()` | High | S | [NoDense_Findings.md#high-severity](NoDense_Findings.md) |
| **NetworkX GDSP Bypasses** | `fum_rt/fum_advanced_math/structural_plasticity/` | Violates single-writer: direct `graph.add_edge()` mutations | High | M | [GDSP_Bypass_Suspects.md#high-risk](GDSP_Bypass_Suspects.md) |
| **Global Visualization Layout** | `fum_rt/core/visualizer.py:82` | Violates bounded ops: `nx.spring_layout()` O(N²) recompute | High | L | [Visualization_Path.md#hot-path](Visualization_Path.md) |
| **Missing UTE/UTD Gates** | `fum_rt/io/ute.py`, `fum_rt/io/utd.py` | Violates event-driven: no B1/ADC integration in text pipeline | Medium | M | [UTE_UTD_Status.md#missing-gate-binding](UTE_UTD_Status.md) |
| **Component Analysis Scans** | `fum_rt/core/sparse_connectome.py:294` | Violates locality: `for i in range(N)` full-node iteration | Medium | M | [NoDense_Findings.md#medium-severity](NoDense_Findings.md) |
| **Evolutionary Weight Mutations** | `fum_rt/fum_advanced_math/evolutionary/` | Violates single-writer: direct weight array mutations | Medium | S | [GDSP_Bypass_Suspects.md#evolutionary-algorithms](GDSP_Bypass_Suspects.md) |
| **Missing Runtime Instrumentation** | Multiple entry points | Violates observability: no telemetry, dry-run, or profiling modes | Medium | L | [Run_Snapshot.md#missing-instrumentation](Run_Snapshot.md) |
| **Simplistic Territory Algorithm** | `fum_rt/core/adc.py` | Limits scalability: composite key clustering vs spatial algorithms | Medium | L | [Heterogeneity_ADC.md#missing-spatial](Heterogeneity_ADC.md) |
| **Physics Memory Steering Bypasses** | `fum_rt/physics/memory_steering/` | Violates single-writer: direct adjacency `A[i,j] = 1` writes | Low | S | [GDSP_Bypass_Suspects.md#physics-memory](GDSP_Bypass_Suspects.md) |
| **Missing Neuron Type Diversity** | `fum_rt/core/substrate/substrate.py` | Limits functionality: only E/I types, no rhythmic/bursting/habituating | Low | L | [Heterogeneity_ADC.md#missing-types](Heterogeneity_ADC.md) |
| **Void-Driven Layout in Hot Path** | `fum_rt/frontend/plugins/fum_visualizer_v1/` | Violates bounded ops: O(iterations × N²) force simulation | Low | S | [Visualization_Path.md#void-driven-layout](Visualization_Path.md) |

## Risk Categories

### 🔴 High Severity (Immediate Action Required)
**Global Operations in Hot Paths**: Break fundamental void-faithful contracts
- Global weight statistics during metrics collection
- Dense adjacency scanning for sparse neighbor extraction  
- Full GPU weight matrix transfers
- NetworkX direct graph mutations bypassing GDSP
- Visualization layout recomputation

**Impact**: Core system violations, performance degradation, contract violations

### 🟡 Medium Severity (Short-term Planning)
**Architecture Gaps**: Missing key integrations and bounded operations  
- UTE/UTD pipeline lacks gate integration with B1/ADC systems
- Component analysis requires full-node iteration
- Missing runtime instrumentation for observability
- Territory algorithms don't leverage spatial structure

**Impact**: Reduced functionality, missed optimization opportunities, debugging difficulties

### 🟢 Low Severity (Long-term Enhancement)
**Feature Limitations**: Missing capabilities that could improve system richness
- Physics modules bypass GDSP (validation context)
- Limited neuron type diversity beyond excitatory/inhibitory
- Advanced visualization not integrated with main loop

**Impact**: Limited feature set, reduced biological plausibility

## Fix ROI Analysis

### High ROI (High Impact, Low Effort)
1. **Replace `W.mean()` with sampling** - Quick win for metrics void-compliance
2. **Flag physics bypasses as validation-only** - Simple containment fix  
3. **Disable visualization in main loop** - Immediate hot path protection

### Medium ROI (Balanced Impact/Effort)
1. **Route evolutionary algorithms through GDSP** - Architectural fix with medium effort
2. **Implement sparse-native B1 calculation** - Avoids dense adjacency scanning
3. **Add B1/ADC gate integration to UTE/UTD** - Enables proper event-driven text processing

### Low ROI (High Effort, Future Value)
1. **Implement spatial territory algorithms** - Major ADC overhaul
2. **Add diverse neuron types** - Extensive substrate enhancement  
3. **Create incremental visualization system** - Complex rendering architecture

## Critical Path Dependencies

### Immediate Fixes Enable
- **Metrics sampling** → Enables hot path void-compliance
- **GDSP bypass containment** → Enables single-writer guarantee
- **Layout computation removal** → Enables bounded visualization

### Sequential Requirements  
1. **Hot path fixes** must precede performance optimization
2. **Single-writer enforcement** must precede advanced plasticity features
3. **Event-driven infrastructure** must precede real-time adaptivity

## Estimated Timeline Impact

### Sprint 1 (2-3 days): Critical Violations
- Fix global statistics (replace with sampling)
- Contain GDSP bypasses (flag as validation-only)
- Remove hot path layout computation

### Sprint 2 (1-2 weeks): Architecture Gaps  
- Implement sparse-native operations
- Add UTE/UTD gate integration
- Create runtime instrumentation infrastructure

### Sprint 3+ (Long-term): Enhancement Features
- Spatial territory algorithms
- Advanced neuron type diversity
- Incremental visualization system

## Success Metrics

### Void-Faithful Compliance
- Zero global operations in hot paths
- All topology/weight mutations via GDSP
- All operations bounded by budgets/TTL
- Event-driven architecture throughout

### Performance Indicators
- Consistent O(E) or better complexity for core operations
- Stable memory usage regardless of network size
- Predictable latency under load
- No dense operation violations in runtime logs