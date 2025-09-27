# Runtime Probe Results

## Instrumented Run Status
**Attempted**: No ready-made dry-run or instrumented flags detected
**Configuration Searched**: `run_profiles/*.json`, main entry points  
**Result**: No zero-code-change instrumentation available

## Missing Instrumentation
- No `--dry-run` flag in `fum_live.py`
- No `--debug` or `--instrument` modes
- No telemetry-only execution modes
- No built-in performance profiling flags

## Alternative Approach Not Taken
Could potentially run smallest config (`1kN_sparse.json`) for 60-120s, but this would:
1. Require actual system execution (not read-only audit)
2. Risk modifying system state during census
3. Violate audit constraints (read-only, no changes)

## What Would Be Available With Instrumentation

### Expected Metrics (If Run Were Possible)
Based on code analysis, a 60-120s instrumented run would likely capture:

**Tick Rate**:
- Target: 10Hz (from `"hz": 10` in configs)
- Actual performance: depends on system load and sparse vs dense mode

**Active Fraction**:
- Walker budget utilization: 256 walkers × 16 visits × 8 edges
- Active edges/total edges ratio from sparse connectome
- Territory occupancy from ADC

**Gate Triggers**:
- B1 spike events (threshold: 3.0, hysteresis: 0.5)  
- GDSP homeostatic repairs, growth, pruning decisions
- ADC territory creation/decay events

**Edits Per Minute**:
- GDSP synaptic weight modifications
- Territory boundary updates
- Walker-driven topology changes

**Potential Errors**:
- Dense operation violations (if any triggered)
- Bus overflow events (65536 capacity)
- Memory allocation failures
- Network connectivity issues

## Blocked by Missing Infrastructure

### Required for Runtime Probe
1. **Instrumentation Flags**: Command-line options for telemetry-only mode
2. **Metrics Export**: Structured output of performance counters
3. **Dry-Run Mode**: Execute walker/GDSP logic without state persistence
4. **Profile Output**: JSON/CSV export of runtime statistics
5. **Error Capturing**: Structured logging of violations and failures

### Smallest Runnable Configuration Analysis
**File**: `run_profiles/1kN_sparse.json`
- **Scale**: 1000 neurons, sparse mode, 8 average degree
- **Performance**: 256 walkers, 5 hops, 10Hz target rate
- **Logging**: Every tick (`"log_every": 1`)
- **Duration**: Unlimited (`"duration": null`)
- **Dependencies**: Standard Python scientific stack (numpy, scipy, networkx)

**Estimated Runtime Requirements**:
- Memory: ~100MB for 1K neuron sparse network
- CPU: Moderate load for walker/GDSP operations  
- Disk: Minimal logging output
- Time: 60-120s would provide meaningful statistics

## What Could Be Learned (Hypothetical)

### Performance Characteristics
1. **Walker Efficiency**: Actual visits/edges vs budget allocations
2. **GDSP Activity**: Frequency of homeostatic/growth/pruning operations
3. **ADC Dynamics**: Territory creation rate, boundary formation patterns
4. **Bus Utilization**: Event generation rate, queue depth statistics
5. **B1 Behavior**: Spike detection frequency, hysteresis effectiveness

### Void-Faithful Compliance
1. **Dense Violations**: Count of operations triggering global scans
2. **Budget Overruns**: Walker/GDSP operations exceeding budget limits
3. **Event Locality**: Verification that operations remain local/bounded
4. **TTL Effectiveness**: Walker walk depths, territory lifetimes

### System Health Indicators
1. **Component Connectivity**: Graph fragmentation over time
2. **Weight Distribution**: Synaptic strength evolution patterns
3. **Territory Stability**: ADC region persistence and boundaries
4. **Queue Health**: Bus event flow and potential bottlenecks

## Recommendations for Future Instrumentation

### Immediate Additions
1. **Add `--probe` flag** to main entry points for telemetry-only mode
2. **Implement metrics export** to JSON/CSV for offline analysis
3. **Create dry-run mode** that simulates without state persistence
4. **Add performance counters** for key operations (walker steps, GDSP edits)

### Telemetry Infrastructure  
1. **Structured logging** with configurable verbosity levels
2. **Performance profiling** hooks for hot path analysis
3. **Memory tracking** for resource utilization monitoring
4. **Error classification** system for violation detection

### Configuration Enhancement
1. **Probe-specific configs** with minimal overhead settings
2. **Time-bounded execution** for controlled measurement periods
3. **Metric selection** flags to focus on specific subsystems
4. **Output formatting** options for different analysis tools

## Current Limitation Impact
Without runtime probing capability:
- Cannot validate actual performance vs theoretical analysis
- Missing empirical verification of void-faithful compliance
- No baseline metrics for optimization efforts
- Limited ability to detect real-world bottlenecks or violations