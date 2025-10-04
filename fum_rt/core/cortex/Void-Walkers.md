# Technical Summary Report

**Generated on:** October 4, 2025 at 2:10 AM CDT

---

### Identified Components

*   **`BaseScout` (Class):** An abstract base class for "void-faithful, read-only scouts." It provides common functionality for interacting with a `connectome` (graph structure) and managing exploration budgets. It defines the core `step` contract.
*   **`BaseDecayMap` (Class):** An abstract base class for bounded, exponentially decaying accumulators. It manages per-node scores (`_val`) and last update times (`_last_tick`), handling decay and pruning. It defines the `fold` and `snapshot` contracts.
*   **`ColdMap` (Class):** A concrete implementation of a "coldness tracker" that records the last seen `tick` for each node and calculates a coldness score based on idle time. It's used for telemetry and read-only purposes.
*   **`ExcitationMap` (Class):** A concrete `BaseDecayMap` subclass that accumulates positive `SpikeEvent`s and positive `DeltaWEvent`s to track excitatory activity.
*   **`HeatMap` (Class):** A concrete `BaseDecayMap` subclass that accumulates `VTTouchEvent`s, `SpikeEvent`s, and `DeltaWEvent`s (absolute `dw`) to track general recency-weighted activity.
*   **`InhibitionMap` (Class):** A concrete `BaseDecayMap` subclass that accumulates negative `SpikeEvent`s and negative `DeltaWEvent`s (absolute `dw`) to track inhibitory activity.
*   **`MemoryMap` (Class):** A flexible map that can act as a view/adapter over an external "MemoryField" or as a self-contained, bounded reducer (proxy mode) that folds various events (`VTTouchEvent`, `EdgeOnEvent`, `SpikeEvent`, `DeltaWEvent`) to update an internal memory-like value.
*   **`TrailMap` (Class):** A concrete `BaseDecayMap` subclass used as a short-half-life repulsion map, accumulating `VTTouchEvent`s, `EdgeOnEvent`s, `SpikeEvent`s, and `DeltaWEvent`s to track recent traversal footprints.
*   **`ColdScout` / `VoidColdScoutWalker` (Class):** A `BaseScout` subclass that prioritizes exploring nodes identified as "cold" by a `ColdMap` snapshot.
*   **`CycleHunterScout` (Class):** A `BaseScout` subclass that performs walks to seek short cycles, prioritizing neighbors already in its recent path history.
*   **`ExcitationScout` (Class):** A `BaseScout` subclass that prioritizes nodes with high excitatory scores and emits `SpikeEvent`s with positive `sign` and an amplitude based on local excitation.
*   **`FrontierScout` (Class):** A `BaseScout` subclass that explores graph frontiers and bridge-like structures, using a scoring heuristic based on coldness, heat, shared neighbors, and degree differences.
*   **`HeatScout` (Class):** A `BaseScout` subclass that routes based on a softmax choice over neighbors, considering memory values, trail repulsion, and heat scores.
*   **`InhibitionScout` (Class):** A `BaseScout` subclass that prioritizes nodes with high inhibitory scores and emits `SpikeEvent`s with negative `sign` and an amplitude based on local inhibition.
*   **`MemoryRayScout` (Class):** A `BaseScout` subclass that steers its walk using a "refractive-index" like mechanism, prioritizing neighbors with higher memory values, with fallback to heat if memory is unavailable.
*   **`VoidRayScout` (Class):** A `BaseScout` subclass that routes based on local gradients of an external `phi` field (if provided by `connectome`) combined with memory values.
*   **`SentinelScout` (Class):** A `BaseScout` subclass designed for blue-noise reseeding and de-trampling, performing minimal-TTL (typically 1 hop) walks to ensure broad coverage, potentially biased by "visit" or "cold" maps.
*   **`run_scouts_once` (Function):** A utility function responsible for executing a given sequence of scout objects within a time budget for a single tick.
*   **`fum_rt.core.proprioception.events` (Module/Events):** Contains `BaseEvent`, `VTTouchEvent` (node visit), `EdgeOnEvent` (edge traversal), `SpikeEvent` (node activity with sign/amplitude), and `DeltaWEvent` (weight change event). These are the primary data units emitted by scouts and processed by maps.
*   **`connectome` (Implicit Interface):** An object passed to scouts, exposing methods/attributes like `N` (number of nodes), `neighbors(u)` or `get_neighbors(u)` (list of neighbors for node `u`), `adj` (adjacency mapping), and potentially `phi` (scalar field).
*   **`bus` (Implicit Interface):** An optional object passed to `run_scouts_once` that, if present, is used to publish collected events (e.g., via `publish_many`).
*   **`scouts.py` (Facade Module):** A module that re-exports various scout and map classes, providing a centralized import path and preserving legacy compatibility.

### Observed Interactions & Data Flow

1.  **System Orchestration (`run_scouts_once`):**
    *   The `run_scouts_once` function is called per tick with a `connectome`, a list of `scouts`, a `maps` dictionary, a `budget`, an optional `bus`, and a `max_us` time limit.
    *   It determines the starting scout for fairness (round-robin by tick).
    *   It iterates through the `scouts`, calling each `scout.step()` method. It enforces a global time budget (`max_us`) and a soft per-scout budget (`per_us`).
    *   All `BaseEvent`s returned by `scout.step()` calls are aggregated into a single list.
    *   If a `bus` is provided and events were generated, `bus.publish_many(events)` is called (or `bus.publish(e)` for each event as a fallback).

2.  **Scout Execution (`BaseScout.step` and subclasses):**
    *   `scout.step()` receives a `connectome`, `bus` (ignored by scouts as they are read-only), `maps` (for contextual routing), and a `budget`.
    *   Scouts (via `BaseScout` helpers) query the `connectome` for graph size (`_get_N`) and neighbors of a given node (`_neighbors`). This is strictly local and read-only.
    *   Scouts consult the `maps` dictionary (e.g., `maps["heat_head"]`, `maps["cold_head"]`, `maps["memory_dict"]`) to derive priority sets (`_priority_set`) or scores (`_pick_neighbor_scored`) for guiding their walks. Helper functions (`_extract_head_nodes`, `_head_lookup`, `_head_to_dict`, `_head_to_set`, `_dict_from_maps`) facilitate parsing these map snapshots.
    *   During their bounded walks (controlled by `budget_visits`, `budget_edges`, `ttl`), scouts generate `BaseEvent`s:
        *   `VTTouchEvent`: emitted for each node visited.
        *   `EdgeOnEvent`: emitted for each edge traversed.
        *   `SpikeEvent` (e.g., by `ExcitationScout`, `InhibitionScout`): for specific activity.
    *   These events are returned as a `List[BaseEvent]` from `scout.step()`.

3.  **Map Updates (`BaseDecayMap.fold` and subclasses):**
    *   Maps (e.g., `HeatMap`, `ExcitationMap`, `InhibitionMap`, `TrailMap`) expose a `fold(events, tick)` method.
    *   An external orchestrator (not shown in this segment, but implied by the `fold` contract) would pass the collected events from `run_scouts_once` to the relevant maps.
    *   The `fold` method iterates through the `events`, filters them by `kind` and other attributes (e.g., `sign`, `dw` value), and calls `self.add(node, tick, increment)` to update its internal score for specific nodes.
    *   `ColdMap` uses a `touch(node, tick)` method instead of `fold` for its specific update logic.
    *   `MemoryMap` in proxy mode also implements `fold` to update its internal `_m` dictionary based on events. If it has an external `field`, `fold` becomes a no-op.

4.  **Map State and Snapshots (`BaseDecayMap.snapshot`):**
    *   All maps maintain internal state (`_val`, `_last_tick` for `BaseDecayMap` and its subclasses; `_last_seen` for `ColdMap`).
    *   Map state is subject to exponential decay (`_decay_to`) based on `half_life_ticks` and `tick` progression.
    *   Maps enforce bounded working sets (`keep_max`) by pruning (`_prune`) the smallest or oldest entries to limit memory usage.
    *   Maps provide `snapshot()` methods that return a `dict` containing summarized data:
        *   `head`: top-k nodes by score/coldness.
        *   `p95`, `p99`, `max`, `count`: percentile and max summaries.
        *   `_dict` (for `TrailMap`, `MemoryMap`): a bounded dictionary of node scores.
    *   These snapshot dictionaries are then passed to scouts via the `maps` parameter in `run_scouts_once`, completing a feedback loop.

### Inferred Design Rationale

1.  **"Void-faithful, Read-Only" Principle:** This is a fundamental constraint explicitly stated and enforced throughout the documentation. Scouts are strictly read-only, never modifying the `connectome` or directly altering global state. This promotes:
    *   **Loose Coupling:** Scouts are independent and don't create side effects, making them easier to test, reason about, and potentially run in parallel.
    *   **Determinism & Reproducibility:** By separating observation (scouts) from action/state change (maps, external systems via bus), the system's behavior can be more predictable.
    *   **Scalability:** Avoiding global scans and direct writes simplifies concurrent execution and distributed processing.

2.  **Event-Driven Architecture:** The system heavily relies on `BaseEvent`s (e.g., `VTTouchEvent`, `EdgeOnEvent`, `SpikeEvent`). Scouts emit events, and maps "fold" events. This pattern:
    *   **Decouples Components:** Producers (scouts) and consumers (maps, bus) of events don't need direct knowledge of each other.
    *   **Flexibility:** New event types or new event consumers can be added without modifying existing scouts.
    *   **Asynchronous Processing:** Events can be queued and processed asynchronously, which is useful for real-time systems.

3.  **Bounded Computation & Memory Footprint:**
    *   **Scouts:** Use `budget_visits`, `budget_edges`, `ttl` (Time-To-Live) to limit walk depth and resource consumption per tick. They perform only local neighbor reads.
    *   **Maps:** Implement `head_k`, `keep_max`, `half_life` for bounded storage and exponential decay. They avoid global scans by only processing events and pruning old/small entries.
    *   **Rationale:** This design is crucial for real-time systems or very large graphs, preventing performance degradation and excessive memory usage. It ensures the system remains responsive and predictable under high load.

4.  **Specialization and Modular Extension:**
    *   `BaseScout` and `BaseDecayMap` provide common interfaces and shared logic, allowing for easy creation of new, specialized scout strategies and map types. Each scout/map focuses on a single responsibility (e.g., `HeatScout` follows heat, `ColdScout` seeks cold).
    *   **Rationale:** Promotes code reuse, maintainability, and extensibility. New heuristics or state-tracking mechanisms can be integrated without modifying core components.

5.  **Abstraction of `Connectome` and `Maps` Data:**
    *   `BaseScout` abstracts how it queries graph neighbors (`_neighbors`) supporting multiple `connectome` interfaces (methods, dicts).
    *   Scouts interact with map data through a generic `maps` dictionary containing "snapshots" (head lists, summary stats, bounded dicts) rather than direct access to map objects. Helper functions manage extracting relevant data from these snapshots.
    *   **Rationale:** Decouples scouts from specific `connectome` and `map` implementations, allowing for flexible underlying data structures and preventing tight dependencies.

6.  **Real-time Performance and Fairness:**
    *   `run_scouts_once` includes a microsecond time budget (`max_us`) and round-robin scout scheduling.
    *   **Rationale:** Essential for a real-time system (`fum_rt`) to ensure predictable execution times and prevent any single scout from monopolizing resources or starving others.

7.  **Robustness (Extensive Error Handling):**
    *   Numerous `try-except` blocks around type conversions, dictionary accesses, and attribute lookups.
    *   **Rationale:** Makes the system resilient to malformed input data, incomplete `maps` dictionaries, or unexpected `connectome` object behavior, leading to graceful degradation rather than crashes.

### Operational Snippets

1.  **Initializing a scout:**
    ```python
    from fum_rt.core.cortex.void_walkers.void_heat_scout import HeatScout
    scout = HeatScout(budget_visits=32, half_life_ticks=100, seed=42)
    ```

2.  **Initializing a map:**
    ```python
    from fum_rt.core.cortex.maps.heatmap import HeatMap
    heatmap = HeatMap(half_life_ticks=200, vt_touch_gain=0.25)
    ```

3.  **Executing scouts for a tick:**
    ```python
    from fum_rt.core.cortex.void_walkers.runner import run_scouts_once
    from fum_rt.core.proprioception.events import BaseEvent
    # Assume 'my_connectome', 'my_scouts_list', 'current_maps_snapshot', 'my_bus_instance' are defined
    # and 'current_tick' is an integer
    
    budget = {"visits": 100, "edges": 50, "ttl": 10, "tick": current_tick, "seeds": [1, 5, 10]}
    
    emitted_events: List[BaseEvent] = run_scouts_once(
        connectome=my_connectome,
        scouts=my_scouts_list,
        maps=current_maps_snapshot,
        budget=budget,
        bus=my_bus_instance,
        max_us=5000 # 5 milliseconds total budget
    )
    # The bus would have published the events, or they are returned if no bus.
    ```

4.  **Map folding events:**
    ```python
    # Assume 'heatmap' is an instance of HeatMap and 'emitted_events' is a list of events from scouts
    current_tick = 123
    heatmap.fold(emitted_events, current_tick)
    ```

5.  **Generating a map snapshot:**
    ```python
    # After folding events, get a snapshot
    heatmap_snapshot = heatmap.snapshot()
    # Example output (simplified):
    # {
    #     "heat_head": [[12, 0.85], [34, 0.72]],
    #     "heat_p95": 0.6,
    #     "heat_p99": 0.9,
    #     "heat_max": 1.0,
    #     "heat_count": 500
    # }
    ```
    This `heatmap_snapshot` (and similar snapshots from other maps) would then be aggregated into the `maps` dictionary passed to `run_scouts_once` in a subsequent tick.

## Key Highlights

* The system is built on a "void-faithful, read-only" principle, with `BaseScout` abstracting graph exploration and `BaseDecayMap` managing dynamic, decaying graph state in a feedback loop.
* Scouts are strictly read-only, never modifying the `connectome` or global state directly, which ensures loose coupling, determinism, and scalability.
* An event-driven architecture, using `BaseEvent`s like `VTTouchEvent` and `SpikeEvent`, decouples scouts (event producers) from maps and other consumers for flexibility and asynchronous processing.
* Both scouts and maps incorporate bounded computation and memory management, utilizing walk budgets, exponential decay, and pruning to ensure real-time performance and prevent resource exhaustion on large graphs.
* The architecture promotes modularity and extensibility through abstract base classes, allowing for the easy creation and integration of specialized scout strategies and map types.
* The `run_scouts_once` function centrally orchestrates scout execution, enforcing per-tick time budgets and using round-robin scheduling to ensure fairness and predictable real-time operation.
* Scouts derive their exploration strategies by consulting dynamic `maps` snapshots, which are in turn updated by events emitted during scout walks, forming a continuous feedback mechanism.
