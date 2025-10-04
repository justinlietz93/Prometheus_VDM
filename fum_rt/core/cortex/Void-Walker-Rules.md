# Technical Summary Report

**Generated on:** October 4, 2025 at 2:23 AM CDT

---

### Architecture
*   Do not perform global scans.
*   Do not perform dense conversions.
*   Do not directly access raw weight arrays.
*   Do not directly access external graph libraries.
*   Operate only on local neighbor reads provided by the active graph.
*   Emit only small, foldable events.
*   The `bus` parameter must not be used for writes by read-only scouts.
*   Do not perform I/O operations in `BaseDecayMap`.
*   Do not perform logging in `BaseDecayMap`.
*   The `fum_rt.core.cortex.void_walkers.base_decay_map` module must perform event-driven folding only.
*   The `fum_rt.core.cortex.void_walkers.base_decay_map` module must maintain a bounded working set via `keep_max`.
*   The `fum_rt.core.cortex.void_walkers.base_decay_map` module must implement sample-based pruning for the working set.
*   The `fum_rt.core.cortex.void_walkers.base_decay_map` module must ensure snapshot operations are cheap and bounded by `head_k`/`keep_max`.
*   The `fum_rt.core.cortex.void_walkers.base_decay_map` module must ensure `fold` operations are O(#events) time per tick.
*   The `frontier_scout.py` module must serve as a shim for naming conventions.
*   Use the `void_frontier_scout.py` module for the actual class implementation of `FrontierScout`.
*   `HeatMap` must fold events only.
*   `HeatMap` must never scan global structures.
*   The single source of truth for the slow memory field must reside outside the `maps/` directory.
*   `MemoryMap` must act as a thin view/adapter when a `field` is provided.
*   If no `field` is provided, `MemoryMap` must operate as a bounded reducer proxy.
*   When operating as a reducer proxy, `MemoryMap` must only retain a small working set (no full-N vector).
*   `MemoryMap` must not perform global scans.
*   `MemoryMap` must maintain a bounded working set only when in reducer-proxy mode.
*   The `runner` module must be stateless.
*   The `runner` module must be a per-tick scout executor.
*   The `runner` module must not use schedulers.
*   `run_scouts_once` must not perform writes.
*   `run_scouts_once` must not use timers.
*   `run_scouts_once` must not manage cadence.
*   `run_scouts_once` must not use background threads.
*   `run_scouts_once` must be a pure function.
*   `run_scouts_once` must be called exactly once per tick.
*   The `scouts` module must act as a thin aggregator re-exporting scout classes and maps.
*   The `scouts` module must preserve legacy import paths.
*   The `scouts` module must enforce void-faithful, read-only traversal.
*   Scouts must not perform global scans.
*   Scouts must only use local neighbor reads.
*   Scouts must operate within bounded TTL/budgets.
*   Scouts must not mutate the connectome (read-only).
*   Scouts must not perform scans.
*   Scouts must not use schedulers.
*   `TrailMap` must not perform scans.
*   `TrailMap` must use a bounded working set via `BaseDecayMap.keep_max`.
*   `TrailMap.fold` must only use provided events.
*   `TrailMap.fold` must not perform adjacency or weight scans.
*   Updates in `TrailMap.fold` must be strictly local to nodes appearing in events.
*   `ColdScout` must not scan global structures.
*   `ColdScout` must use local neighbor reads.
*   `ColdScout` must operate within bounded TTL/budgets.
*   `CycleHunterScout` must be purely local.
*   `CycleHunterScout` must only read neighbor lists.
*   `CycleHunterScout` must not perform global scans or dense conversions.
*   `CycleHunterScout` must not use schedulers.
*   `CycleHunterScout` must execute once per tick under the runner.
*   `CycleHunterScout` must operate within bounded budgets for visits, edges, and TTL.
*   `CycleHunterScout` must not perform writes.
*   `CycleHunterScout` must emit events only.
*   `ExcitationScout` must not perform global scans.
*   `ExcitationScout` must not scan global structures.
*   `ExcitationScout` must use local neighbor reads.
*   `ExcitationScout` must operate within bounded TTL/budgets.
*   `FrontierScout` must use purely local heuristics.
*   `FrontierScout` must not perform scans.
*   `FrontierScout` must not use schedulers.
*   TTL and budgets must enforce bounds for `FrontierScout`.
*   `FrontierScout` must not perform writes.
*   `FrontierScout` must emit events only.
*   The `HeatScout.step` method must contain an inline copy of `BaseScout.step` logic to facilitate map-aware neighbor choice.
*   `HeatScout` must not perform writes.
*   `HeatScout` must not perform scans.
*   `InhibitionScout` must not perform global scans.
*   `InhibitionScout` must not scan global structures.
*   `InhibitionScout` must use local neighbor reads.
*   `InhibitionScout` must operate within bounded TTL/budgets.
*   `MemoryRayScout` must not perform writes.
*   `MemoryRayScout` must not perform scans.
*   `MemoryRayScout` must not perform global scans or dense conversions.
*   `MemoryRayScout` must only operate on neighbors.
*   `MemoryRayScout` must not use schedulers.
*   `MemoryRayScout` must be TTL/budget bounded.
*   `MemoryRayScout` must emit compact events only.
*   `VoidRayScout` must not perform global scans or dense conversions.
*   `VoidRayScout` must operate only on local neighbor lists.
*   `VoidRayScout` must operate only on small map snapshots.
*   `VoidRayScout` must not use schedulers.
*   `VoidRayScout` must be TTL/budget bounded.
*   `VoidRayScout` must emit compact events only.
*   `SentinelScout` must perform local reads only (neighbors of the current node).
*   `SentinelScout` must not perform scans.
*   `SentinelScout` must not perform writes.

### API Contract
*   The `BaseScout.step` method must return a `list[BaseEvent]`.
*   The `connectome` object passed to `BaseScout.step` must expose `N` (node count).
*   The `connectome` object passed to `BaseScout.step` must expose either `neighbors`, `get_neighbors` methods, or an `adj` mapping for neighbor access.
*   Read-only scouts must emit events by returning them, not by writing to the bus.
*   Subclasses of `BaseScout` may override `_priority_set`.
*   `BaseScout._priority_set` must return a bounded set of node indices.
*   Subclasses of `BaseDecayMap` must implement the `fold(events, tick)` method.
*   Subclasses of `BaseDecayMap` must call `add(node, tick, inc)` within their `fold` implementation.
*   The `BaseDecayMap.fold` method must raise `NotImplementedError` in the base class.
*   The `BaseDecayMap.snapshot` method must return `head` as the top-k [node, score] pairs, bounded by `head_k`.
*   The `BaseDecayMap.snapshot` method must return "p95", "p99", "max", and "count" summaries.
*   `ColdMap` must expose a `touch(node: int, tick: int)` method.
*   `ColdMap` must expose a `snapshot(tick: int, head_n: int = 16)` method returning a dictionary with specified fields.
*   `ColdMap.snapshot` must return a dictionary with "cold_head", "cold_p95", "cold_p99", and "cold_max" keys.
*   `ExcitationMap.snapshot` must return a dictionary with "exc_head", "exc_p95", "exc_p99", "exc_max", and "exc_count" keys.
*   `HeatMap.snapshot` must return a dictionary with "heat_head", "heat_p95", "heat_p99", "heat_max", and "heat_count" keys.
*   `InhibitionMap.snapshot` must return a dictionary with "inh_head", "inh_p95", "inh_p99", "inh_max", and "inh_count" keys.
*   The `MemoryMap.snapshot` method must return a dictionary with "memory_head", "memory_p95", "memory_p99", "memory_max", "memory_count", and "memory_dict" keys.
*   `run_scouts_once` must accept optional `seeds` and `map_heads`.
*   The facade (scouts.py) must expose `VoidColdScoutWalker` (aliasing `ColdScout`), `HeatScout`, `ExcitationScout`, `InhibitionScout`, `VoidRayScout`, `MemoryRayScout`, `FrontierScout`, `CycleHunterScout`, `SentinelScout`, `ColdMap`, `BaseScout`, `GDSPActuator`, and `RevGSP`.
*   `TrailMap.snapshot` must include "trail_head" and "trail_dict" keys.
*   `TrailMap.snapshot` must export a bounded snapshot including both the head list and the working-set dictionary.
*   The `trail_dict` in `TrailMap.snapshot` must be bounded by `keep_max`.

### Behavior
*   If the connectome has 0 or fewer nodes, the `BaseScout.step` method must return an empty event list.
*   `BaseScout._pick_neighbor` must prioritize neighbors from the `priority` set if available.
*   If no priority neighbors are available, `BaseScout._pick_neighbor` must choose a random neighbor (blue-noise hop).
*   The `BaseDecayMap._prune` method must be called if the number of tracked values exceeds `keep_max`.
*   `BaseDecayMap._prune` must drop the smallest entries from the working set.
*   The `ColdMap` coldness score must be calculated as `1 - 2^(-age / half_life_ticks)`.
*   The `ColdMap` coldness score must be monotonic in idle time.
*   The `ColdMap` coldness score must be bounded in [0,1).
*   The `ColdMap._prune` method must be called if the number of tracked `_last_seen` entries exceeds `keep_max`.
*   `ColdMap._prune` must reduce the tracked set to `keep_max` entries.
*   `ColdMap._prune` must preferentially drop the most recently seen nodes.
*   `ExcitationMap` must track excitatory-only activity.
*   `ExcitationMap` must filter `SpikeEvent` by `sign > 0`.
*   `ExcitationMap` must filter `DeltaWEvent` by `dw > 0`.
*   When processing `SpikeEvent`s, `ExcitationMap` must only consider events where `sign` is greater than 0.
*   When processing `DeltaWEvent`s, `ExcitationMap` must only consider events where `dw` is greater than 0.0.
*   `HeatMap` must track recency-weighted activity with a short half-life.
*   `HeatMap` must increment on `VTTouchEvent`s.
*   `HeatMap` must increment on any `SpikeEvent`.
*   `HeatMap` must increment on any `DeltaWEvent`.
*   When processing `VTTouchEvent`s, `HeatMap` must add `vt_touch_gain * w` to the node.
*   When processing `SpikeEvent`s, `HeatMap` must add `spike_gain * amp` to the node.
*   When processing `DeltaWEvent`s, `HeatMap` must add `dW_gain * |dw|` to the node.
*   `InhibitionMap` must track inhibitory-only activity.
*   `InhibitionMap` must filter `SpikeEvent` by `sign < 0`.
*   `InhibitionMap` must filter `DeltaWEvent` by `dw < 0`.
*   When processing `SpikeEvent`s, `InhibitionMap` must only consider events where `sign` is less than 0.
*   When processing `DeltaWEvent`s, `InhibitionMap` must only consider events where `dw` is less than 0.0.
*   If a `MemoryMap.field` is attached, the `fold()` method must be a no-op.
*   If a `MemoryMap.field` is attached, the view must delegate snapshot operations to the field's snapshot.
*   When capping the dictionary size from a field snapshot, `MemoryMap._snapshot_from_field` must do so deterministically by highest values.
*   If `MemoryMap.self.field` is not `None`, the `MemoryMap.fold` method must immediately return.
*   If the `MemoryMap` proxy-mode working set `_m` exceeds `keep_max`, `_prune` must be called.
*   `MemoryMap._prune` for proxy-mode must drop a sampled set of the smallest entries.
*   `MemoryMap.snapshot` must cap the `memory_dict` size to `self.dict_cap`.
*   `run_scouts_once` must run a bounded list of read-only scouts.
*   `run_scouts_once` must execute scouts exactly once per tick.
*   `run_scouts_once` must enforce a microsecond time budget across all scouts.
*   Drop-oldest behavior for events must be handled by the downstream bus implementation when `publish_many` is used.
*   `run_scouts_once` must rotate the starting scout by tick (round-robin) to ensure fairness and avoid starvation.
*   `run_scouts_once` must implement a global time guard, stopping scout execution if the `max_us` budget is exceeded.
*   `run_scouts_once` must implement a best-effort per-scout time guard.
*   If `bus` is provided and has `publish_many`, `bus.publish_many(evs)` must be invoked exactly once at the end.
*   If `bus` does not have `publish_many`, `bus.publish(e)` must be called for each event, with a bounded fallback mechanism.
*   `TrailMap` must be a short half-life trail/repulsion map.
*   `TrailMap` must be updated only by events.
*   `TrailMap` must be event-driven only.
*   `TrailMap` must fold `vt_touch` and `edge_on` events.
*   `TrailMap` is intended as a light repulsion field.
*   When processing `VTTouchEvent`s, `TrailMap` must add `vt_touch_gain * w` to the node.
*   When processing `EdgeOnEvent`s, `TrailMap` must add `edge_gain` to both `u` and `v` nodes if they are non-negative.
*   When processing `SpikeEvent`s, `TrailMap` must add `spike_gain * amp` to the node.
*   When processing `DeltaWEvent`s, `TrailMap` must add `dW_gain * |dw|` to the node.
*   `ColdScout` must prefer neighbors whose node IDs appear in the `ColdMap`'s "cold_head" snapshot.
*   `ColdScout._priority_set` must prioritize nodes from "cold_head" with a `cap` based on `budget_visits`.
*   `CycleHunterScout` must seek short cycles (3-6 hops).
*   `CycleHunterScout` must use a TTL-limited walk.
*   `CycleHunterScout` must use a tiny path window.
*   `CycleHunterScout` must maintain a small deque of the recent path.
*   `CycleHunterScout` must prefer stepping to a neighbor already in the recent path window.
*   If no preferred neighbor is found, `CycleHunterScout` must hop randomly (blue-noise) among neighbors.
*   `CycleHunterScout._priority_set` must return an empty set.
*   `ExcitationScout` must map excitatory corridors.
*   `ExcitationScout` must feed `ExcitationMap` strictly via events.
*   `ExcitationScout` must seed from `ExcitationMap.exc_head`.
*   During a walk, `ExcitationScout` must emit a `VTTouchEvent` per visit.
*   During a walk, `ExcitationScout` must synthesize `SpikeEvent(node, amp, sign=+1)` with bounded amplitude in [0,1].
*   `_head_lookup` must normalize scores by dividing by the maximum score over the truncated head.
*   `_head_lookup` must return an empty dictionary if the head is empty.
*   `ExcitationScout._priority_set` must prefer `ExcitationMap` head indices.
*   `SpikeEvent` amplitude emitted by `ExcitationScout` must be within [0,1].
*   If excitation is not found, default `SpikeEvent` amplitude from `ExcitationScout` to 0.5.
*   `FrontierScout` must skim component boundaries and likely bridge frontiers.
*   `FrontierScout._priority_set` must prioritize coldest tiles as starting seeds.
*   `FrontierScout._deg` must return the integer length of the neighbor list.
*   `FrontierScout._pick_neighbor_scored` must use a Softmax choice mechanism.
*   `HeatScout` must perform local-only neighbor selection.
*   `HeatScout` must use a softmax over map signals for neighbor selection.
*   `HeatScout` must support trail repulsion.
*   `HeatScout` must support optional memory steering.
*   `HeatScout.theta_mem` must control attraction or repulsion to memory.
*   `HeatScout.rho_trail` must repel recently traversed/hot nodes.
*   `HeatScout.gamma_heat` must bias toward heat fronts.
*   If map dictionaries are absent, `HeatScout` must fall back to priority head nodes.
*   If priority head nodes are also absent, `HeatScout` must fall back to a blue-noise hop.
*   The priority seed set must be used for initial pool bias via `HeatScout._priority_set()`.
*   `HeatScout._head_to_dict` must handle `head` being an already-formed dictionary.
*   If Softmax denominator Z is zero or negative, `_softmax_choice` must fallback to a uniform random choice among candidates.
*   `HeatScout._priority_set` must prefer `HeatMap` head indices for seeds.
*   `HeatScout._pick_neighbor_scored` must use `heat_dict` as a fallback for `trail_dict` if `trail_dict` is absent.
*   `InhibitionScout` must map inhibitory ridges.
*   `InhibitionScout` must feed `InhibitionMap` strictly via events.
*   `InhibitionScout` must seed from `InhibitionMap.inh_head`.
*   During a walk, `InhibitionScout` must emit a `VTTouchEvent` per visit.
*   During a walk, `InhibitionScout` must synthesize `SpikeEvent(node, amp, sign=-1)` with bounded amplitude in [0,1].
*   `InhibitionScout._priority_set` must prefer `InhibitionMap` head indices.
*   `SpikeEvent` amplitude emitted by `InhibitionScout` must be within [0,1].
*   If inhibition is not found, default `SpikeEvent` amplitude from `InhibitionScout` to 0.5.
*   `MemoryRayScout` must implement refractive-index steering using a slow memory field.
*   `MemoryRayScout` must fall back to `HeatMap` head/dict when memory is absent.
*   `MemoryRayScout._head_to_set` must accept multiple keys for head extraction.
*   `MemoryRayScout._dict_from_maps` must accept dict snapshots directly.
*   `MemoryRayScout._dict_from_maps` must minimally adapt if a head list is mistakenly passed.
*   `MemoryRayScout._priority_set` must prioritize "memory_head".
*   `MemoryRayScout._priority_set` must fall back to "heat_head" if "memory_head" is not available.
*   `MemoryRayScout._pick_neighbor_scored` must prioritize `memory_dict`.
*   `MemoryRayScout._pick_neighbor_scored` must fall back to `heat_dict` as a slow proxy if `memory_dict` is not available.
*   `VoidRayScout` must implement physics-aware routing.
*   `VoidRayScout` must prefer neighbors with favorable local change in a fast field φ.
*   If Softmax denominator Z is zero or negative, `_softmax_choice` in `VoidRayScout` must fallback to picking the first candidate.
*   `VoidRayScout._priority_set` must prefer `HeatMap` head for initial seeds.
*   If `connectome.phi` is `None`, `VoidRayScout._phi` must return 0.0.
*   `SentinelScout` must act as a blue-noise reseeder/de-trample walker.
*   `SentinelScout` must prevent path lock-in by sampling uniformly across space.
*   `SentinelScout` must announce coverage.
*   `SentinelScout` must use `budget["seeds"]` when provided.
*   If `budget["seeds"]` is not provided, `SentinelScout` must use uniform random nodes as seeds.
*   `SentinelScout` TTL must be kept minimal (default 1).
*   `SentinelScout` TTL must be minimal to avoid trampling.
*   `SentinelScout` TTL must be minimal to keep cost bounded.
*   The `SentinelScout.ttl` must be enforced as 1 to ensure single-step walks.
*   `SentinelScout._priority_set` must prefer low-visit or cold heads when available.

### Event Handling
*   Returned events from `BaseScout.step` must use only `VTTouchEvent` or `EdgeOnEvent`.
*   Subclasses of `BaseScout` may add `SpikeEvent`s.
*   Scouts in `runner.py` must emit only foldable events (`vt_touch`, `edge_on`, optional `spike`/`delta_w`).
*   Scouts (via `scouts.py` facade) must emit only foldable events: `vt_touch`, `edge_on`, and (optionally) `spike(+/-)`.
*   `ColdScout` must emit only `VTTouchEvent` and `EdgeOnEvent` events.
*   `CycleHunterScout` must emit `VTTouchEvent` and `EdgeOnEvent` events.
*   `FrontierScout` must emit `VTTouchEvent` and `EdgeOnEvent` only.
*   `HeatScout` must emit `VTTouchEvent` and `EdgeOnEvent` events.
*   `MemoryRayScout` must emit `VTTouchEvent` and `EdgeOnEvent` events.
*   `VoidRayScout` must emit `VTTouchEvent` and `EdgeOnEvent` events.
*   `SentinelScout` must emit `VTTouchEvent` for coverage.
*   `SentinelScout` must emit opportunistic `EdgeOnEvent` (one hop) when neighbors exist.

### Parameter Constraints
*   `BaseScout.__init__` `budget_visits` must be an integer, default 16.
*   `BaseScout.__init__` `budget_edges` must be an integer, default 8.
*   `BaseScout.__init__` `ttl` must be an integer, default 64.
*   `BaseScout.__init__` `seed` must be an integer, default 0.
*   `BaseScout.budget_visits` must be non-negative.
*   `BaseScout.budget_edges` must be non-negative.
*   `BaseScout.ttl` must be at least 1.
*   The effective `BaseScout.step` `budget_visits` must be between 0 and N (inclusive).
*   The effective `BaseScout.step` `budget_edges` must be non-negative.
*   The effective `BaseScout.step` `ttl` must be at least 1.
*   Seed nodes for `BaseScout.step` must be valid node indices (non-negative and less than N).
*   `BaseDecayMap.__init__` `head_k` must be an integer, default 256.
*   `BaseDecayMap.__init__` `half_life_ticks` must be an integer, default 200.
*   `BaseDecayMap.__init__` `keep_max` must be an integer or None, default None.
*   `BaseDecayMap.__init__` `seed` must be an integer, default 0.
*   `BaseDecayMap.head_k` must be at least 8.
*   `BaseDecayMap.half_life` must be at least 1.
*   `BaseDecayMap.keep_max` must be at least `head_k`.
*   Nodes added to `BaseDecayMap.add` must be non-negative.
*   `BaseDecayMap.snapshot` `head_n` parameter defaults to 16.
*   `BaseDecayMap.snapshot` `head_n` must be at least 1 and at most `self.head_k`.
*   Node IDs passed to `ColdMap.touch` must be non-negative integers.
*   `ColdMap.snapshot` `head_n` parameter must be at least 1 and at most `self.head_k`.
*   `ExcitationMap.__init__` `spike_gain` must be a float, default 1.0.
*   `ExcitationMap.__init__` `dW_gain` must be a float, default 0.5.
*   `HeatMap.__init__` `vt_touch_gain` must be a float, default 0.25.
*   `HeatMap.__init__` `spike_gain` must be a float, default 1.0.
*   `HeatMap.__init__` `dW_gain` must be a float, default 0.5.
*   `InhibitionMap.__init__` `spike_gain` must be a float, default 1.0.
*   `InhibitionMap.__init__` `dW_gain` must be a float, default 0.5.
*   `MemoryMap.__init__` `head_k` must be an integer, default 256.
*   `MemoryMap.__init__` `dict_cap` must be an integer, default 2048.
*   `MemoryMap.__init__` `keep_max` must be an integer or None, default None.
*   `MemoryMap.__init__` `seed` must be an integer, default 0.
*   `MemoryMap.__init__` `gamma` must be a float, default 0.05.
*   `MemoryMap.__init__` `delta` must be a float, default 0.01.
*   `MemoryMap.__init__` `kappa` must be a float, default 0.10.
*   `MemoryMap.__init__` `touch_gain` must be a float, default 1.0.
*   `MemoryMap.__init__` `spike_gain` must be a float, default 0.20.
*   `MemoryMap.__init__` `dW_gain` must be a float, default 0.10.
*   `MemoryMap.head_k` must be at least 8.
*   `MemoryMap.dict_cap` must be at least 8.
*   `MemoryMap.keep_max` must be at least `head_k`.
*   `MemoryMap.gamma` must be non-negative.
*   `MemoryMap.delta` must be between 0.0 and 1.0 (inclusive).
*   `MemoryMap.kappa` must be non-negative.
*   `MemoryMap.touch_gain` must be non-negative.
*   `MemoryMap.spike_gain` must be non-negative.
*   `MemoryMap.dW_gain` must be non-negative.
*   Nodes processed in `MemoryMap` proxy-mode `fold` must be non-negative.
*   `run_scouts_once` `max_us` parameter defaults to 2000.
*   `run_scouts_once` `max_us` must be non-negative.
*   `TrailMap.__init__` `half_life_ticks` defaults to 50.
*   `TrailMap.__init__` `vt_touch_gain` defaults to 0.15.
*   `TrailMap.__init__` `edge_gain` defaults to 0.05.
*   `TrailMap.__init__` `spike_gain` defaults to 0.05.
*   `TrailMap.__init__` `dW_gain` defaults to 0.02.
*   `_extract_head_nodes` (used by ColdScout) `cap` parameter defaults to 512.
*   Extracted node IDs from head lists by `_extract_head_nodes` must be non-negative.
*   `CycleHunterScout.__init__` `window` must be an integer, default 5.
*   `CycleHunterScout.window` must be at least 2.
*   Seed nodes for `CycleHunterScout.step` must be valid node indices (non-negative and less than N).
*   `_head_lookup` (used by ExcitationScout) `cap` parameter defaults to 512.
*   Nodes extracted by `_head_lookup` must be non-negative.
*   `_extract_head_nodes` (used by ExcitationScout) `cap` parameter defaults to 512.
*   Nodes extracted by `_extract_head_nodes` must be non-negative.
*   `_head_to_dict` (used by FrontierScout) `cap` parameter defaults to 1024.
*   Nodes extracted by `_head_to_dict` must be non-negative.
*   `FrontierScout.__init__` `w_cold` must be a float, default 1.0.
*   `FrontierScout.__init__` `w_heat` must be a float, default 0.5.
*   `FrontierScout.__init__` `w_shn` must be a float, default 0.25.
*   `FrontierScout.__init__` `w_deg` must be a float, default 0.5.
*   `FrontierScout.__init__` `tau` must be a float, default 1.0.
*   `FrontierScout.w_cold` must be non-negative.
*   `FrontierScout.w_heat` must be non-negative.
*   `FrontierScout.w_shn` must be non-negative.
*   `FrontierScout.w_deg` must be non-negative.
*   `FrontierScout.tau` must be at least 1e-6.
*   The `FrontierScout._priority_set` `cap` for "cold_head" must be at least 64 and `budget_visits * 8`.
*   `FrontierScout._shared_neighbors` `cap` parameter defaults to 128.
*   `_head_to_set` (used by HeatScout) `cap` parameter defaults to 512.
*   Nodes extracted by `_head_to_set` must be non-negative.
*   `_head_to_dict` (used by HeatScout) `cap` parameter defaults to 2048.
*   Nodes extracted by `_head_to_dict` must be non-negative.
*   `HeatScout.__init__` `theta_mem` must be a float, default 0.0.
*   `HeatScout.__init__` `rho_trail` must be a float, default 0.0.
*   `HeatScout.__init__` `gamma_heat` must be a float, default 1.0.
*   `HeatScout.__init__` `tau` must be a float, default 1.0.
*   `HeatScout.rho_trail` must be non-negative.
*   `HeatScout.gamma_heat` must be non-negative.
*   `HeatScout.tau` must be at least 1e-6.
*   Seed nodes for `HeatScout.step` must be valid node indices (non-negative and less than N).
*   `_head_lookup` (used by InhibitionScout) `cap` parameter defaults to 512.
*   Nodes extracted by `_head_lookup` must be non-negative.
*   `_extract_head_nodes` (used by InhibitionScout) `cap` parameter defaults to 512.
*   Nodes extracted by `_extract_head_nodes` must be non-negative.
*   `_head_to_set` (used by MemoryRayScout) `cap` parameter defaults to 512.
*   Nodes extracted by `_head_to_set` must be non-negative.
*   Nodes extracted by `_dict_from_maps` must be non-negative.
*   `MemoryRayScout.__init__` `theta_mem` must be a float, default 0.8.
*   `MemoryRayScout.__init__` `tau` must be a float, default 1.0.
*   `MemoryRayScout.tau` must be at least 1e-6.
*   Seed nodes for `MemoryRayScout.step` must be valid node indices (non-negative and less than N).
*   `_head_to_set` (used by VoidRayScout) `cap` parameter defaults to 512.
*   Nodes extracted by `_head_to_set` must be non-negative.
*   `VoidRayScout.__init__` `lambda_phi` must be a float, default 1.0.
*   `VoidRayScout.__init__` `theta_mem` must be a float, default 0.0.
*   `VoidRayScout.__init__` `tau` must be a float, default 1.0.
*   `VoidRayScout.tau` must be at least 1e-6.
*   The `VoidRayScout._priority_set` `cap` for "heat_head" must be at least 64 and `budget_visits * 8`.
*   Seed nodes for `VoidRayScout.step` must be valid node indices (non-negative and less than N).
*   `SentinelScout.__init__` `ttl` defaults to 1.
*   The effective `SentinelScout.step` `ttl` must be capped to 1.
*   The `SentinelScout._priority_set` `cap` for "visit_head" or "cold_head" must be at least 64 and `budget_visits * 8`.
*   Seed nodes for `SentinelScout.step` must be valid node indices (non-negative and less than N).

### Performance
*   `BaseDecayMap._prune` must avoid full O(N) sorts.
*   `ColdMap._prune` must use sampling to avoid O(N) passes.
*   `FrontierScout._shared_neighbors` must bound its cost by only checking up to `cap` neighbors of `v`.

### Syntax
*   `BaseScout` must define `__slots__` with "budget_visits", "budget_edges", "ttl", and "rng".
*   `BaseDecayMap` must define `__slots__` with "head_k", "half_life", "keep_max", "rng", "_val", and "_last_tick".
*   `ColdMap` must define `__slots__` with "head_k", "half_life", "keep_max", "rng", and "_last_seen".
*   `ExcitationMap` must define `__slots__` with "spike_gain" and "dW_gain".
*   `HeatMap` must define `__slots__` with "vt_touch_gain", "spike_gain", and "dW_gain".
*   `InhibitionMap` must define `__slots__` with "spike_gain" and "dW_gain".
*   `MemoryMap` must define `__slots__` with "field", "head_k", "dict_cap", "keep_max", "rng", "_m", "_last_tick", "gamma", "delta", "kappa", "touch_gain", "spike_gain", and "dW_gain".
*   `TrailMap` must define `__slots__` with "vt_touch_gain", "edge_gain", "spike_gain", and "dW_gain".
*   `ColdScout` must define `__slots__` as empty.
*   `CycleHunterScout` must define `__slots__` with "window".
*   `ExcitationScout` must define `__slots__` as empty.
*   `FrontierScout` must define `__slots__` with "w_cold", "w_heat", "w_shn", "w_deg", and "tau".
*   `HeatScout` must define `__slots__` with "theta_mem", "rho_trail", "gamma_heat", and "tau".
*   `InhibitionScout` must define `__slots__` as empty.
*   `MemoryRayScout` must define `__slots__` with "theta_mem" and "tau".
*   `VoidRayScout` must define `__slots__` with "lambda_phi", "theta_mem", and "tau".
*   `SentinelScout` must define `__slots__` as empty.

### Type Requirement
*   `ExcitationMap.spike_gain` must be convertible to float.
*   `ExcitationMap.dW_gain` must be convertible to float.
*   `HeatMap.vt_touch_gain` must be convertible to float.
*   `HeatMap.spike_gain` must be convertible to float.
*   `HeatMap.dW_gain` must be convertible to float.
*   `InhibitionMap.spike_gain` must be convertible to float.
*   `InhibitionMap.dW_gain` must be convertible to float.
*   `TrailMap.vt_touch_gain` must be convertible to float.
*   `TrailMap.edge_gain` must be convertible to float.
*   `TrailMap.spike_gain` must be convertible to float.
*   `TrailMap.dW_gain` must be convertible to float.

### Algorithm
*   The `FrontierScout._pick_neighbor_scored` (Softmax fallback) random choice must use a deterministic-ish hashing for reproducibility in its randomness.
*   `HeatScout` local selection must use `logit_j = (self.theta_mem * m_j) - (self.rho_trail * htrail_j) + (self.gamma_heat * h_j)` divided by `self.tau`.
*   `MemoryRayScout` local selection must follow `P(i→j) ∝ exp(Theta * m[j])` with temperature `tau` (Boltzmann choice).
*   If Softmax denominator Z is zero or negative, `_softmax_choice` (used by `HeatScout`, `MemoryRayScout`) must fallback to a uniform random choice among candidates.
*   `VoidRayScout` local scoring must follow `s_j = lambda_phi * (φ[j] - φ[i]) + theta_mem * m[j]`.
*   `VoidRayScout` local scoring must not perform scans.
*   `VoidRayScout` must use a temperatured choice via softmax over neighbors.
*   `VoidRayScout` must perform strictly local reads.
*   The `VoidRayScout._softmax_choice` (Softmax fallback) random choice must use a deterministic-ish hashing for reproducibility in its randomness.

### Purpose
*   `TrailMap` is intended as a light repulsion field.
*   `FrontierScout` must skim component boundaries and likely bridge frontiers.
*   `SentinelScout` must act as a blue-noise reseeder/de-trample walker.
*   `SentinelScout` must prevent path lock-in by sampling uniformly across space.
*   `SentinelScout` must announce coverage.

### Duty
*   `ExcitationScout` must map excitatory corridors.
*   `ExcitationScout` must feed `ExcitationMap` strictly via events.
*   `InhibitionScout` must map inhibitory ridges.
*   `InhibitionScout` must feed `InhibitionMap` strictly via events.

## Key Highlights

* All modules and scouts must operate strictly locally, avoiding global scans, dense conversions, and direct access to raw weight arrays or external graph libraries to ensure bounded and efficient computation.
* Maps and scouts are required to maintain bounded working sets and adhere to strict resource limits, including `head_k`, `keep_max`, TTLs, and per-tick time budgets, with explicit pruning strategies to manage memory.
* The system architecture is primarily event-driven, with scouts emitting small, foldable events and maps processing these events to update their state, fostering decoupled and reactive information flow.
* Scouts are strictly read-only entities, must not mutate the connectome, and are designed to communicate results solely by emitting events, thereby preserving the integrity of the underlying graph structure.
* The `runner` module, particularly `run_scouts_once`, functions as a stateless, per-tick executor that meticulously manages scout execution within strict microsecond time budgets, ensures fairness via round-robin rotation, and is responsible for publishing all collected events.
* Various specialized maps, including `ColdMap`, `HeatMap`, `ExcitationMap`, `InhibitionMap`, `MemoryMap`, and `TrailMap`, are designed to track and expose distinct localized activity patterns such as coldness, recency, excitation, inhibition, memory, and repulsion.
* Scouts like `CycleHunterScout`, `FrontierScout`, `HeatScout`, and `MemoryRayScout` utilize sophisticated, local-only heuristics and map-driven priority sets to intelligently guide their traversals and neighbor selection within the graph.

## Next Steps & Suggestions

* Evaluate the scalability and performance of `BaseDecayMap` pruning mechanisms and `keep_max` thresholds under varying graph sizes and event loads to ensure bounded resource consumption.
* Conduct empirical studies to quantify the effectiveness of specific scout heuristics (e.g., `FrontierScout` for boundaries, `CycleHunterScout` for short cycles, `MemoryRayScout` for memory steering) in achieving their stated exploration goals across diverse graph topologies.
* Develop a systematic framework for tuning the numerous behavioral parameters (e.g., gain values, `half_life_ticks`, `tau`, `theta_mem`) to optimize for desired system outcomes, such as exploration efficiency or map accuracy.
* Investigate the robustness and consistency of the entire event propagation pipeline, from scout emission and `run_scouts_once` execution (including time budgets and fairness) to event bus handling and map folding, particularly concerning the single source of truth for the 'slow memory field'.
