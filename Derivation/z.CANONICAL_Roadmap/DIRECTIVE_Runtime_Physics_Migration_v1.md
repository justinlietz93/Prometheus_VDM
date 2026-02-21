# Runtime Physics Migration Directive v1

**Author:** Justin K. Lietz  
**Date:** 2026-02-15  
**Status:** APPROVED — implement in order  
**Scope:** Three coupled fixes to the runtime hot path. All three must land together or none of them matter individually.

---

## Problem Statement

The runtime has three interconnected failures that collectively prevent the substrate from processing temporal information:

1. **UTE strips temporal microstructure.** Input events are flattened into a bag of up to 32 dicts per tick with no timestamps, no ordering, no inter-arrival intervals. The *when* is destroyed before it reaches the substrate.

2. **The field update has no causal transport.** The void equations (VDM-E-086) use logistic growth + uniform noise + a global sine clock. There is no spatial coupling, no finite-speed propagation, no causal cone. Signals don't travel through the connectome — they appear everywhere simultaneously via the global modulation.

3. **RE-VGSP has no resonance.** Despite the name "Resonance-Enhanced Valence-Gated Synaptic Plasticity," the actual implementation is `α W (1 - W) + noise` with a global phase multiplier. The function signature accepts `spike_train`, `spike_phases`, `plv`, `time_window_ms` but `delta_re_vgsp` in `Void_Equations.py` never uses them. Every edge gets the same temporal modulation regardless of when pre/post activity occurred. The eligibility trace `E` exists as a CSR matrix with identical sparsity to `W` but is not populated with timing-dependent values.

**Why they're coupled:** If you fix UTE to preserve temporal data but the field update can't transport it causally, the timing information dies at the receptor. If you fix the field update to use Telegraph-Fisher but RE-VGSP can't detect temporal correlations, the substrate can't learn from the causal structure. If you fix RE-VGSP to be timing-dependent but UTE already destroyed the timing, there's nothing to learn from. All three or none.

---

## Fix 1: UTED — Preserve Temporal Microstructure in I/O

### What exists now

`vdm_rt/io/ute.py`: Reads stdin lines → `{type:'text', msg: line}`. Tails `chat_inbox.jsonl`. Injects synthetic `{type:'tick', msg:'tick'}` at 1 Hz. `poll()` returns up to 32 items per tick as unordered dicts.

### What must change

Create `vdm_rt/io/uted/` with:

**`ports.py`** — Port specification (no semantics, just physical coupling):
```python
@dataclass
class PortSpec:
    port_id: str          # stable identifier, e.g. "imu/accel", "mic/raw"
    direction: str        # "in" or "out"
    dtype: str            # "f32", "i16", "u8", "bytes"
    shape: tuple | None   # tensor shape or None for byte streams
    rate_hz: float        # native sample rate of the source
    range_min: float      # clamp bounds
    range_max: float
```

**`frames.py`** — Time-indexed data containers:
```python
@dataclass
class SensorFrame:
    tick: int                    # runtime tick this frame belongs to
    timestamp_us: int            # microsecond-resolution timestamp from source
    port_id: str                 # which port produced this
    payload: np.ndarray | bytes  # raw samples, full temporal resolution
    n_samples: int               # how many samples in this frame
    dt_us: int                   # inter-sample interval in microseconds
```

**`ute_mux.py`** — Multiplexer that collects frames from all registered input ports, preserving temporal order across ports within a tick.

**`utd_demux.py`** — Demultiplexer for output ports (ActuatorFrame).

### Compatibility wrappers

Current behavior preserved via adapters:
- `StdinAdapter` → `SensorFrame(port_id="stdin/text", ...)`
- `InboxTailAdapter` → `SensorFrame(port_id="ui/text", ...)`
- `HeartbeatAdapter` → `SensorFrame(port_id="clock/tick", ...)`

### Critical requirement

**A SensorFrame is NOT "here are N samples that happened this tick." It is "here is a time-indexed sequence where the inter-sample intervals are first-class data."** The receptor layer must be able to reconstruct the full temporal waveform within each tick and inject sub-tick stimulation events with preserved relative timing onto receptor neurons.

### Files touched
- New: `vdm_rt/io/uted/ports.py`, `frames.py`, `ute_mux.py`, `utd_demux.py`
- Modified: `vdm_rt/io/ute.py` (wrap existing behavior)
- Modified: `vdm_rt/io/utd.py` (wrap existing behavior)
- Modified: VDM-A-009 step 7 (process inbound via UTED mux, not raw poll)

---

## Fix 2: Telegraph-Fisher Field Update — Replace Proxy Void Equations

### What exists now

`vdm_rt/core/Void_Equations.py` lines 22-55 (`delta_re_vgsp`):
```python
base_delta = effective_alpha * W * (1 - W) + noise  # logistic growth, no spatial coupling
# optional: base_delta * (1 + phase_sens * sin(2π f_ref t))  # GLOBAL clock, not endogenous
```

`vdm_rt/core/sparse_connectome.py` step() around line 280:
```python
dW = universal_void_dynamics(W, t, ...)  # reaction-only, no transport
self.W = clip(W + gate * dW, 0, 1)      # first-order Euler, no inertia
```

### What must change

This is specified in detail in the Telegraph-Fisher implementation document (the Gini-Coefficient-Claude.md file). The core changes:

**`Void_Equations.py`** — `delta_re_vgsp` gets `adj_lists` parameter and conservative coupling term (`gamma`). `delta_gdsp` gets `adj_lists` parameter and diffusive Laplacian coupling term (`kappa`). These become the J-limb and M-limb respectively.

**`sparse_connectome.py`** — New state variables: `W_prev`, `W_curr`, `telegraph_tau`, `gamma`, `kappa`, `debt` array. The field update becomes second-order telegraph timestepping:

```
tau * (W_new - 2*W_curr + W_prev)/dt^2 + (W_new - W_curr)/dt = delta_J + delta_M
```

With debt-throttled J-limb: `throttle = exp(-0.5 * beta * debt)`.

**The global sine modulation `sin(2π f_ref t)` gets removed.** Oscillatory dynamics become endogenous via the telegraph equation's second-order inertial term. This eliminates `F_REF` and `PHASE_SENS` as external knobs.

### Validation gates (run 50,000 ticks)
- No NaN values
- Gini coefficient rises from ~0.41 toward 0.50-0.55
- Four macrostates persist in PCA of scalar telemetry
- Field stays in [0, 1]

### Files touched
- Modified: `vdm_rt/core/Void_Equations.py` (both functions)
- Modified: `vdm_rt/core/sparse_connectome.py` (__init__ + step)
- Modified: run profile schemas (new params: telegraph_tau, gamma, kappa)

---

## Fix 3: RE-VGSP — Implement Actual Resonance

### What exists now

`delta_re_vgsp` computes `α W (1-W) + noise` per edge. The `RevGSP().adapt_connectome` call signature accepts timing parameters (`spike_train`, `spike_phases`, `plv`, `time_window_ms`) but the underlying delta function ignores them. The eligibility trace `E` (CSR, same pattern as `W`) exists but is not populated with timing-dependent values. Every edge gets identical temporal modulation from the global clock.

### What must change

RE-VGSP must become an actual spike-timing-dependent plasticity rule where the weight change on edge (i,j) depends on:

**1. Temporal correlation between pre and post activity.**

When a SensorFrame injects sub-tick stimulation events onto receptor neurons, those events propagate through the Telegraph-Fisher field. Node `i` and node `j` receive activation at different times depending on their distance from the stimulus source and the propagation speed `c = sqrt(D/tau)`. The weight change must depend on the *relative timing* of activation at `i` vs `j`, not just on their current field values.

Concretely: maintain per-node activation timestamps (or a decaying trace that encodes recency). The eligibility trace `E[i,j]` should reflect the temporal overlap between node `i`'s recent activation and node `j`'s recent activation, with a sign that depends on causal ordering (did `i` fire before or after `j`?).

**2. Resonance with local field oscillation.**

Once Telegraph-Fisher provides endogenous oscillatory dynamics (replacing the global sine), "resonance" means: plasticity is strongest when the input timing *matches the substrate's natural frequency at that location*. The local oscillation period is set by the telegraph parameters. Edges carrying signals that arrive in-phase with the local oscillation get enhanced. Edges carrying signals that arrive out-of-phase get weakened (or at least not reinforced).

This replaces the current `(1 + phase_sens * sin(2π f_ref t))` global modulation with a *local* phase relationship between each edge's activity pattern and the local field dynamics.

**3. Valence gating stays.**

The three-factor rule (eligibility × reward signal) is already correct in principle. The SIE total_reward composite (TD_error + novelty - habituation + self_benefit) gates whether timing-correlated edges actually get strengthened. This doesn't need to change — it just needs actual timing data to gate.

### Implementation sketch

```python
def compute_eligibility(W_curr, W_prev, activation_times, row, col, tau_e):
    """
    Compute timing-dependent eligibility for each edge.
    
    activation_times: per-node array of most recent activation timestamp (sub-tick resolution)
    row, col: CSR edge indices
    tau_e: eligibility decay time constant
    """
    dt_pre_post = activation_times[col] - activation_times[row]  # causal direction
    
    # STDP-like window: positive for pre-before-post, negative for post-before-pre
    eligibility = np.exp(-np.abs(dt_pre_post) / tau_e) * np.sign(dt_pre_post)
    
    # Modulate by local field change (resonance with endogenous dynamics)
    local_oscillation = W_curr[row] - W_prev[row]  # local field velocity
    resonance = eligibility * local_oscillation
    
    return resonance
```

The existing `E.data` array (CSR, same sparsity as `W`) stores these values. VDM-A-006 step 6 already multiplies `(d_re + d_gd) * E.data` — that pathway is correct, it just needs `E.data` to contain timing-dependent eligibility instead of whatever it currently holds.

### Per-node activation timestamps

This is new state. Each node needs a `last_activation_us` timestamp updated whenever:
- A SensorFrame injects stimulation at that node
- The Telegraph-Fisher field update pushes the node's field value past a threshold
- A void walker visits the node

This timestamp must be at sub-tick resolution (microseconds from UTED) so that timing differences between nodes within a single tick are preserved.

### Files touched
- Modified: `vdm_rt/core/Void_Equations.py` (delta_re_vgsp becomes timing-aware)
- Modified: `vdm_rt/core/sparse_connectome.py` (new: activation_times array, eligibility computation per tick)
- Modified: VDM-A-006 pseudocode (eligibility trace populated from timing, not just existence)
- New: eligibility computation function

---

## Implementation Order

**Phase 1 — Telegraph-Fisher field update (Fix 2)**

Do this first because it's the most self-contained and has the clearest validation gates. The existing UTE still works (just poorly). You can verify telegraph dynamics with the current text input before adding rich sensors. Run the 50k-tick validation on desktop.

**Phase 2 — UTED temporal preservation (Fix 1)**

Build the port/frame infrastructure. Wire the compatibility adapters so current text input still works but now carries timestamps. Verify that SensorFrames flow through the runtime without breaking anything. No behavior change yet — just infrastructure.

**Phase 3 — RE-VGSP resonance (Fix 3)**

Now that the field has causal transport (Fix 2) and input carries temporal microstructure (Fix 1), implement timing-dependent eligibility. Verify that eligibility traces show meaningful temporal correlations by comparing runs with temporally structured vs shuffled input — if RE-VGSP resonance works, shuffled input should produce lower Gini and less territory structure.

**Phase 4 — Embodied deployment (S5)**

Only after all three fixes pass on desktop. Port the corrected runtime to Android. Build phone sensor adapters as UTED ports. The substrate now receives temporally-rich sensor data, propagates it causally through Telegraph-Fisher, and learns temporal correlations via RE-VGSP resonance.

---

## What NOT to change

- **Void walker / scout system** — already bounded, sparse, correct in principle
- **SIE / SIE v2** — reward computation stays; it gates the now-correct plasticity
- **ADC / territory system** — reads from whatever the substrate produces
- **GDSP structural plasticity** — structural rewiring triggered by B1/TD/cohesion stays
- **Speak / emission pathway** — composer + valence gating stays (for now)
- **Checkpoint / telemetry** — add new fields (activation_times, eligibility stats) to existing schemas

---

## Debts to resolve before or during migration

1. **Remove dense-mode branch** (VDM-A-009 debt): Code has dense path for N≤4096. Remove entirely — crash risk on constrained hardware, violates sparse-only policy.

2. **Fix non-deterministic RNG in GDSP**: Structural rewiring RNG not seeded from run seed. Blocks reproducible analysis.

3. **Tune stim_amp and stim_decay for sensor input**: Current values (0.08 amp, 0.92 decay) calibrated for text. Sensor streams are higher bandwidth and may saturate. Expose these as per-port parameters in UTED PortSpec.

---

## Success criteria

After all three fixes, run the substrate with temporally structured input (e.g., a repeating rhythmic pattern injected via UTE). Compare against the same input with timestamps shuffled within each tick. The corrected runtime should show:

- Higher Gini coefficient with structured input (temporal correlations → sharper territory structure)
- Eligibility traces that are correlated with input timing (not random)
- Telegraph field propagation visible in activation timestamp gradients (nodes closer to stimulus activate earlier)
- Macrostate transitions that correlate with changes in input temporal structure

If shuffled and structured input produce identical substrate behavior, the temporal processing pipeline is still broken somewhere.
