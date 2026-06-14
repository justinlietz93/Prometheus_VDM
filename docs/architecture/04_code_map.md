# Code Map - Key Modules & Responsibilities

**Repository**: Prometheus_VDM  
**Commit**: ae49a391acf2183242e4d96bda49e066beec7680

---

## PRIMARY ENTRYPOINTS

### 1. `vdm_rt/run_nexus.py` [99 LOC]
**Role**: CLI entrypoint for headless VDM execution  
**Responsibilities**:
- Parse argparse flags (N, k, hz, domain, seed, checkpoint_every, etc.)
- Resolve `--load-engram` path (supports directory → latest checkpoint)
- Instantiate `Nexus` class with configuration
- Call `Nexus.run(duration_s=...)`

**Key Functions**:
- `main()` - entry point
- `_resolve_latest_ckpt_in_dir(d)` - find latest checkpoint in directory

**Dependencies**: `vdm_rt.nexus.Nexus`, `vdm_rt.cli.args.make_parser`

---

### 2. `vdm_live.py` [40 LOC]
**Role**: Dash dashboard launcher for live run monitoring  
**Responsibilities**:
- Parse CLI args (--runs-root, --host, --port)
- Set environment variables (RUNS_ROOT, DASH_HOST, DASH_PORT)
- Build Dash app via `vdm_rt.frontend.app.build_app()`
- Start server on http://127.0.0.1:8060 (default)

**Key Functions**:
- `main()` - builds and runs Dash app (debug=False to avoid duplicate callbacks)

**Dependencies**: `vdm_rt.frontend.app.build_app`

---

### 3. `vdm_rt/frontend/__main__.py` [~20 LOC]
**Role**: Frontend-only entrypoint (alternative to vdm_live.py)  
**Responsibilities**:
- Build and run Dash app on port 8050
- Uses RUNS_ROOT from environment

**Dependencies**: `vdm_rt.frontend.app.build_app`

---

## CORE ORCHESTRATION

### 4. `vdm_rt/nexus.py` [~600 LOC]
**Role**: Main `Nexus` class - orchestrator façade over runtime layers  
**Responsibilities**:
- Initialize all subsystems: UTE, UTD, CoreEngine, ADC, SIE, AnnounceBus
- Load lexicon, phrase templates
- Configure emitters (MacroEmitter, ThoughtEmitter)
- Expose `run(duration_s)` → delegates to `runtime.loop.run_loop()`
- Maintain backward compatibility (deprecated inline orchestrator logic removed)

**Key Classes**:
- `Nexus` - main entry class with ~40 init params

**Key Methods**:
- `__init__(run_dir, N, k, hz, domain, ...)` - initialization
- `run(duration_s)` - execution
- `_emit_why()` - provenance telemetry

**Dependencies**: `core.*`, `runtime.*`, `io.*`, `cli.args`

---

### 5. `vdm_rt/runtime/loop/__init__.py` (main.py) [~500 LOC]
**Role**: Main execution loop (heartbeat of VDM)  
**Responsibilities**:
- Iterate ticks from start_step to (duration_s * hz)
- Call `stepper.compute_step_and_metrics()` each tick
- Apply phase profiles (phase control)
- Poll user input (UTE), process messages
- Emit telemetry, macros, thoughts
- Conditionally visualize, checkpoint, emit status
- Smoke test gates (diagnostics)

**Key Functions**:
- `run_loop(state, config, ...)` - main loop entry

**Dependencies**: `runtime.stepper`, `runtime.phase`, `runtime.telemetry`, `runtime.helpers.*`, `core.engine`, `io.*`

---

### 6. `vdm_rt/runtime/stepper.py` [~150 LOC]
**Role**: Single-tick computation executor  
**Responsibilities**:
- Call `CoreEngine.step()`
- Collect proprioception events
- Compute metrics via `compute_metrics()`
- Apply signals (B1 detector)
- Return observation dict

**Key Functions**:
- `compute_step_and_metrics(engine, ...)` - single step

**Dependencies**: `core.engine`, `core.metrics`, `core.signals`, `core.proprioception.events`

---

## CORE RUNTIME ENGINE

### 7. `vdm_rt/core/engine/core_engine.py` [~800 LOC]
**Role**: Main computational kernel  
**Responsibilities**:
- Execute void walker system (coordinate scouts)
- Update cortical maps (heat, trail, memory, excitation, inhibition)
- Apply neuroplasticity (GDSP, RevGSP)
- Emit proprioception events (VTTouch, Spike, DeltaW, EdgeOn)
- Manage sparse connectome state

**Key Classes**:
- `CoreEngine` - main simulation engine

**Key Methods**:
- `step()` - single simulation tick
- `_execute_void_walkers()` - coordinate scouts
- `_apply_neuroplasticity()` - weight updates

**Dependencies**: `core.sparse_connectome`, `core.cortex.void_walkers`, `core.cortex.maps`, `core.neuroplasticity.*`, `core.proprioception.events`

---

### 8. `vdm_rt/core/sparse_connectome.py` [~1,200 LOC]
**Role**: Sparse adjacency matrix (default backend)  
**Responsibilities**:
- CSR sparse matrix (scipy.sparse) for edges
- Edge weights (`w`), bias vectors (`b`)
- Efficient O(E) traversal, updates
- KNN initialization, edge addition/removal
- Neurogenesis support

**Key Classes**:
- `SparseConnectome` - sparse graph implementation

**Key Methods**:
- `__init__(N, k, seed)` - initialization
- `step_activations(...)` - update neuron states
- `add_edge(i, j, w)`, `remove_edge(i, j)` - topology changes
- `save_state(path)`, `load_state(path)` - persistence

**Dependencies**: `numpy`, `scipy.sparse`, `networkx`

---

### 9. `vdm_rt/core/cortex/void_walkers/runner.py` [~400 LOC]
**Role**: Void walker coordinator  
**Responsibilities**:
- Initialize all scouts (Heat, Ray, Memory, Frontier, CycleHunter, Sentinel, Cold, Excitation, Inhibition)
- Execute scouts in sequence
- Aggregate events

**Key Functions**:
- `run_void_walkers(connectome, maps, config, ...)` - execute all scouts

**Dependencies**: `core.cortex.void_walkers.*`, `core.cortex.maps.*`, `core.proprioception.events`

---

### 10. `vdm_rt/core/cortex/void_walkers/base_scout.py` [~100 LOC]
**Role**: Abstract base scout  
**Responsibilities**:
- Define scout interface
- Common utilities (random walk, deposit)

**Key Classes**:
- `BaseScout` - abstract base

**Key Methods**:
- `run()` - abstract; implemented by subclasses

---

### 11. Concrete Scouts (~100-300 LOC each)
- `void_heat_scout.py` - `HeatScout` - heat diffusion, gradient ascent
- `void_ray_scout.py` - `RayScout` - directed exploration
- `void_memory_ray_scout.py` - `MemoryRayScout` - memory-guided exploration
- `void_frontier_scout.py` - `FrontierScout` - boundary expansion
- `void_cycle_hunter_scout.py` - `CycleHunterScout` - cycle detection
- `void_sentinel_scout.py` - `SentinelScout` - guard duty
- `void_cold_scout.py` - `ColdScout` - cold region exploration (feature-flagged)
- `void_excitation_scout.py` - `ExcitationScout` - excitation field
- `void_inhibition_scout.py` - `InhibitionScout` - inhibition field

**Responsibilities**: Each scout implements domain-specific exploration/deposition logic

---

### 12. `vdm_rt/core/cortex/maps/*.py` [~100-200 LOC each]
**Role**: Spatial field maps  
**Responsibilities**:
- Maintain N-dimensional fields (heat, trail, memory, excitation, inhibition)
- Deposit, diffuse, decay operations
- Query spatial distributions

**Key Classes**:
- `HeatMap`, `TrailMap`, `MemoryMap`, `ExcitationMap`, `InhibitionMap`

**Key Methods**:
- `deposit(idx, value)` - add to field
- `diffuse(alpha)` - spatial diffusion
- `decay(beta)` - temporal decay

---

### 13. `vdm_rt/core/proprioception/events.py` [~300 LOC]
**Role**: Event system (observations from core)  
**Responsibilities**:
- Define event types (VTTouchEvent, SpikeEvent, DeltaWEvent, EdgeOnEvent, BiasHintEvent)
- EventDrivenMetrics - aggregate events for telemetry
- Serialize events to JSONL

**Key Classes**:
- `BaseEvent`, `VTTouchEvent`, `SpikeEvent`, `DeltaWEvent`, `EdgeOnEvent`, `BiasHintEvent`
- `EventDrivenMetrics` - aggregator

**Dependencies**: `dataclasses`, JSON serialization

---

### 14. `vdm_rt/core/metrics.py` [~200 LOC]
**Role**: Network metrics computation  
**Responsibilities**:
- Compute graph metrics (degree, clustering, path lengths)
- StreamingZEMA - Z-score topology detector
- Persistent homology (TDA via ripser)

**Key Classes**:
- `StreamingZEMA` - Z-score moving average

**Key Functions**:
- `compute_metrics(connectome, ...)` - full metrics suite

**Dependencies**: `networkx`, `ripser`, `numpy`

---

### 15. `vdm_rt/core/neuroplasticity/*.py` [~100-200 LOC each]
**Role**: Weight update rules  
**Responsibilities**:
- GDSP (Gradient-Driven Structural Plasticity)
- RevGSP (Reverse Gradient Structural Plasticity)
- Hebbian, spike-timing-dependent plasticity (STDP) variants

**Key Functions**:
- `apply_gdsp(connectome, ...)` - weight updates
- `apply_revgsp(connectome, ...)` - reverse updates

---

### 16. `vdm_rt/core/memory/engram_io.py` [~200 LOC]
**Role**: Checkpoint persistence  
**Responsibilities**:
- Save/load connectome state (h5py, npz formats)
- Metadata (step, seed, N, k, domain)
- Provenance tracking

**Key Functions**:
- `save_engram(connectome, path, format='h5')` - persist
- `load_engram(path, connectome)` - restore

**Dependencies**: `h5py`, `numpy`

---

## I/O LAYER

### 17. `vdm_rt/io/ute.py` [~100 LOC]
**Role**: User Text Entry adapter  
**Responsibilities**:
- Read from stdin (optional) and inbox.jsonl
- Non-blocking message polling
- Return list of user messages

**Key Classes**:
- `UTE` - user input manager

**Key Methods**:
- `poll_messages()` - get new messages

---

### 18. `vdm_rt/io/utd.py` [~150 LOC]
**Role**: User Telemetry Display adapter  
**Responsibilities**:
- Write structured JSONL events (events.jsonl, macros.jsonl, thoughts.jsonl)
- Flush to disk
- Tail-friendly format

**Key Classes**:
- `UTD` - telemetry output manager

**Key Methods**:
- `log_event(event_dict)` - append to events.jsonl
- `log_macro(macro_dict)` - append to macros.jsonl

**Dependencies**: `io.logging.rolling_jsonl.RollingJsonlWriter`

---

### 19. `vdm_rt/io/cognition/stimulus.py` [~150 LOC]
**Role**: Text → connectome activation  
**Responsibilities**:
- Parse user text into symbols
- Map symbols to neuron groups (symbol → indices)
- Apply activation stimulus to connectome

**Key Functions**:
- `symbols_to_indices(text, lexicon, connectome, ...)` - symbol → activation

**Dependencies**: `core.text_utils`, `io.lexicon.store`

---

### 20. `vdm_rt/io/cognition/composer.py` [~200 LOC]
**Role**: Emergent text generation  
**Responsibilities**:
- Compose sentences from activated symbols
- Use phrase templates and lexicon
- Valence-based selection

**Key Functions**:
- `compose_say_text(connectome, lexicon, phrase_templates, ...)` - generate sentence

**Dependencies**: `io.lexicon.store`, `core.text_utils`

---

### 21. `vdm_rt/io/cognition/speaker.py` [~150 LOC]
**Role**: Speech gating logic  
**Responsibilities**:
- Decide if system should "speak" (emit text)
- Novelty scoring (IDF-based)
- Hysteresis, cooldown, Z-score thresholds

**Key Functions**:
- `should_speak(...)` - boolean decision
- `novelty_and_score(...)` - compute novelty

**Dependencies**: `io.lexicon.idf`

---

## FRONTEND

### 22. `vdm_rt/frontend/app.py` [~300 LOC]
**Role**: Dash app builder  
**Responsibilities**:
- Initialize Dash app
- Register all callbacks
- Assemble layout from components

**Key Functions**:
- `build_app(runs_root)` - return Dash app instance

**Dependencies**: `dash`, `frontend.components.layout`, `frontend.callbacks.*`

---

### 23. `vdm_rt/frontend/components/layout.py` [~400 LOC]
**Role**: Main dashboard layout  
**Responsibilities**:
- Build UI structure (workspace, runtime controls, charts, feed, chat, config, perf)
- File picker, graph tabs
- Responsive layout

**Key Functions**:
- `build_layout(runs_root)` - return Dash layout

**Dependencies**: `dash`, `frontend.components.*`

---

### 24. `vdm_rt/frontend/callbacks/charts.py` [~200 LOC]
**Role**: Chart update callbacks  
**Responsibilities**:
- Update Plotly charts (metrics, says, events time series)
- Poll events.jsonl via tail
- Aggregate data via `models.series.Series`

**Dependencies**: `plotly`, `frontend.models.series`, `frontend.utilities.tail`

---

### 25. `vdm_rt/frontend/services/process_manager.py` [~150 LOC]
**Role**: Subprocess lifecycle management  
**Responsibilities**:
- Start/stop Nexus subprocess
- Monitor process health
- Kill on demand

**Key Functions**:
- `start_process(profile_path)` - spawn subprocess
- `stop_process()` - terminate

**Dependencies**: `subprocess`, `psutil` (optional)

---

## PHYSICS HARNESSES

### 26. `vdm_rt/physics/pta_correlation_harness.py` [~300 LOC]
**Role**: Pulsar Timing Array correlation experiments  
**Responsibilities**:
- Simulate PTA correlations using VDM substrate
- Generate correlation curves
- Output to runs/

**Dependencies**: `core.*`, `numpy`, `matplotlib`

---

### 27. `vdm_rt/physics/sidm_curve_harness.py` [~250 LOC]
**Role**: Self-Interacting Dark Matter scattering curves  
**Responsibilities**:
- Simulate SIDM cross-sections
- Generate σ/m vs velocity plots

**Dependencies**: `core.*`, `numpy`, `matplotlib`

---

### 28. `vdm_rt/physics/memory_steering/memory_steering.py` [~400 LOC]
**Role**: Memory kernel steering experiments  
**Responsibilities**:
- Test memory-guided dynamics
- Plot memory field evolution

**Dependencies**: `core.memory`, `matplotlib`

---

## UTILITIES & INFRASTRUCTURE

### 29. `vdm_rt/utils/logging_setup.py` [~50 LOC]
**Role**: Centralized logger factory  
**Responsibilities**:
- `get_logger(name, jsonl_path)` - return structured logger
- JSON formatting

**Dependencies**: `logging`, `json`

---

### 30. `vdm_rt/cli/args.py` [~300 LOC]
**Role**: Argparse CLI definition  
**Responsibilities**:
- Define all Nexus CLI flags (~50 flags)
- Help text, defaults, type coercion

**Key Functions**:
- `make_parser()` - return ArgumentParser

---

### 31. `conftest.py` [~73 LOC]
**Role**: Pytest configuration  
**Responsibilities**:
- Add repo root to sys.path
- Alias `Prometheus_VDM.derivation.*` → `Derivation.*` for legacy imports
- Enable test discovery

---

## SUMMARY TABLE

| Module | LOC | Layer | Responsibility |
|--------|-----|-------|----------------|
| `run_nexus.py` | 99 | Entry | CLI entrypoint |
| `vdm_live.py` | 40 | Entry | Dashboard launcher |
| `nexus.py` | 600 | Application | Orchestrator façade |
| `runtime/loop` | 500 | Application | Main execution loop |
| `runtime/stepper.py` | 150 | Application | Single tick executor |
| `core/engine` | 800 | Domain | Core simulation kernel |
| `core/sparse_connectome.py` | 1,200 | Domain | Sparse graph backend |
| `core/cortex/void_walkers` | ~2,000 | Domain | Scout system |
| `core/cortex/maps` | ~1,000 | Domain | Spatial fields |
| `core/proprioception/events.py` | 300 | Domain | Event system |
| `core/metrics.py` | 200 | Domain | Network metrics |
| `core/neuroplasticity` | ~500 | Domain | Weight updates |
| `core/memory/engram_io.py` | 200 | Infrastructure | Checkpointing |
| `io/ute.py` | 100 | Infrastructure | User input |
| `io/utd.py` | 150 | Infrastructure | Telemetry output |
| `io/cognition` | ~500 | Infrastructure | Text processing |
| `frontend/app.py` | 300 | Presentation | Dash builder |
| `frontend/components` | ~2,000 | Presentation | UI components |
| `frontend/callbacks` | ~1,500 | Presentation | Interactivity |
| `frontend/services` | ~300 | Presentation | Subprocess mgmt |
| `physics/*` | ~2,000 | Research | Experimental harnesses |
| `utils/logging_setup.py` | 50 | Common | Logging factory |
| `cli/args.py` | 300 | Common | Argparse CLI |

**Total Core Runtime**: ~8,869 LOC (excluding tests, tools, derivations)

---

## LAYERING DISCIPLINE

**Dependency Direction**: Presentation → Application → Domain ← Infrastructure

**Acyclic**: Zero circular dependencies detected (validated via Tarjan's SCC algorithm)

**Separation of Concerns**:
- Domain (`core/`) is pure: no file I/O, no CLI parsing
- Infrastructure (`io/`, `data/`) adapts external systems to domain
- Application (`runtime/`, `nexus.py`) orchestrates domain + infrastructure
- Presentation (`frontend/`, `vdm_live.py`) consumes telemetry read-only

**Port/Adapter Boundaries**:
- `UTE`, `UTD` are ports (abstract input/output)
- `io/cognition/*` are adapters (text → connectome activation)
- `frontend/*` is external observer (read-only telemetry consumer)
