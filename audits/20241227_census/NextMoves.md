# Top-3 Next-Moves Menu

## Move 1: Eliminate Hot Path Global Operations

**What**: Replace global statistics with bounded sampling in metrics collection
**Why Now**: Unlocks void-faithful compliance and enables safe hot path operation  
**Scope**: `fum_rt/core/metrics.py`, `fum_rt/core/void_b1.py`
**Risk**: Low - sampling maintains statistical validity with bounded cost
**Timebox**: 2 days

### Specific Changes
- Replace `connectome.W.mean()` with sampled weight statistics (budget: 1000 edges)
- Replace `np.where(A[i] > 0)` neighbor extraction with sparse adjacency iteration
- Add EWMA accumulators for streaming statistics instead of global recomputation
- Implement budget-bounded B1 calculation using active edge iterator

### Unlocked Value
- Enables consistent O(E) complexity regardless of network size
- Removes biggest violation of void-faithful bounded operations contract
- Unblocks hot path performance optimization efforts
- Provides foundation for real-time metrics monitoring

---

## Move 2: Enforce Single-Writer Authority Through GDSP

**What**: Route all topology/weight mutations through GDSP interface, contain bypasses
**Why Now**: Establishes structural integrity guarantees for advanced plasticity features
**Scope**: `fum_rt/fum_advanced_math/structural_plasticity/`, `fum_rt/core/neuroplasticity/gdsp.py`
**Risk**: Medium - requires interface design but preserves existing functionality  
**Timebox**: 3 days

### Specific Changes
- Mark `fum_advanced_math/structural_plasticity/` as validation-only (add FORCE_STRUCTURAL flag)
- Create GDSP operation interface for external modules requiring weight/topology mutations
- Route evolutionary algorithms through GDSP budget system instead of direct array access
- Add GDSP pre-checks and rollback capability for failed operations

### Unlocked Value
- Guarantees single-writer contract for all production code paths
- Enables atomic operations and transactional plasticity updates
- Provides foundation for advanced homeostatic and learning algorithms
- Simplifies debugging by centralizing all structural changes

---

## Move 3: Integrate Event-Driven Gates Into Text Pipeline

**What**: Connect B1 signals and ADC territories to UTE/UTD text processing decisions
**Why Now**: Enables adaptive text behavior and closes major architecture gap
**Scope**: `fum_rt/io/ute.py`, `fum_rt/io/utd.py`, `fum_rt/core/void_b1.py`, `fum_rt/core/adc.py`
**Risk**: Low - additive feature that enhances existing pipeline without breaking changes
**Timebox**: 2 days

### Specific Changes
- Add B1 signal consumption to UTD emission thresholds (higher B1 = more selective output)
- Implement territory-aware message routing in UTE (route by domain_hint from ADC)
- Create quality gates using walker coverage and territory confidence scores
- Add macro system integration with ADC territory boundaries for context-aware responses

### Unlocked Value
- Enables self-regulating text behavior based on internal system state
- Provides natural feedback loop between structural learning and communication
- Creates foundation for territory-specific language and adaptive responses  
- Demonstrates end-to-end event-driven architecture from walkers to output

## Implementation Priority

### Week 1: Hot Path Safety (Move 1)
Critical foundation work that unblocks all subsequent optimization efforts. Required before any performance-sensitive features can be safely deployed.

### Week 2: Structural Integrity (Move 2)  
Architectural fix that enables advanced plasticity while maintaining system invariants. Required before complex learning algorithms can be trusted.

### Week 3: System Integration (Move 3)
Feature enhancement that demonstrates cohesive architecture and enables adaptive behaviors. Provides immediate user-visible benefits.

## Success Criteria

### Move 1 Success
- [ ] All metrics operations run in O(E) or better complexity
- [ ] No global scans detected in hot path profiling
- [ ] B1 calculation bounded by sampling budget
- [ ] Streaming statistics maintain accuracy within 5% of global computation

### Move 2 Success  
- [ ] Zero direct weight/topology mutations outside GDSP in production code
- [ ] All structural changes logged and attributable to GDSP operations
- [ ] Evolutionary/physics modules contained with validation flags
- [ ] GDSP interface supports external module requirements

### Move 3 Success
- [ ] UTE/UTD respond to B1 signal changes within 1 tick
- [ ] Text output quality correlates with territory confidence scores
- [ ] Message routing reflects ADC territory boundaries
- [ ] Macro system provides territory-specific contextual responses

## Risk Mitigation

### Technical Risks
- **Sampling accuracy**: Validate statistical properties of bounded sampling vs global computation
- **Interface complexity**: Keep GDSP external interface minimal and well-documented  
- **Integration complexity**: Phase gate integration incrementally with fallbacks

### Performance Risks
- **Overhead introduction**: Profile all changes to ensure no performance regression
- **Memory usage**: Monitor memory consumption during streaming statistics implementation
- **Latency impact**: Ensure gate integration doesn't add significant processing delays

### Functional Risks
- **Behavior changes**: Thoroughly test that sampling doesn't alter system dynamics
- **Compatibility**: Ensure existing configurations continue to work unchanged
- **Validation preservation**: Maintain physics/validation module functionality under containment