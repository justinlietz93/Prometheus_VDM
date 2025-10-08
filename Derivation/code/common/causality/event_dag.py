"""
Event DAG construction and minimal analyses (acyclicity, transitive reduction).

Goals
- Pure-Python, bounded algorithms suited for CI hygiene and small/medium analyses.
- Caller provides events with (id, t, ...). Edges can be provided explicitly or inferred
  with a simple precedence rule under a time tolerance.

Definitions
- Event: a hashable id and a timestamp float t.
- Edge inference (optional): u -> v if t_v - t_u >= 0 and within a caller-specified window
  or follows a supplied adjacency rule. By default we infer no edges unless asked, so this
  module is safe to import without side effects.

Notes
- For large graphs, prefer providing edges; transitive reduction is bounded by a max edge cap.
- We avoid third-party graph libs to stay dependency-minimal.
"""
from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Set


Event = Tuple[str, float]
Edge = Tuple[str, str]


def build_event_dag(
    events: Sequence[Event],
    edges: Optional[Iterable[Edge]] = None,
    *,
    infer_by_time: bool = False,
    max_successors: int = 0,
    time_tolerance: float = 0.0,
) -> Tuple[Dict[str, float], Dict[str, Set[str]]]:
    """
    Build an event DAG adjacency from events and optional edges.

    Args
    - events: sequence of (id, t)
    - edges: optional iterable of (u, v) pairs; assumed to be candidate precedence edges
    - infer_by_time: when True, infer edges by time ordering within same-timestamp tolerance
    - max_successors: cap the number of successors added per node during inference (0 disables)
    - time_tolerance: allow small negative/zero lags |Δt| <= tol to count as zero-lag

    Returns: (times, adj) where
    - times: {id -> t}
    - adj: {u -> set(v)} (may include zero-lag edges when within tolerance)

    Note: acyclicity is not guaranteed; call is_acyclic to verify.
    """
    times: Dict[str, float] = {}
    for eid, t in events:
        # Skip malformed entries deterministically
        if eid is None:
            continue
        ts = None
        # Convert t to float if possible
        if isinstance(t, (int, float)):
            ts = float(t)
        else:
            try:
                ts = float(t)  # type: ignore
            except Exception:
                ts = None
        if ts is None or not (ts == ts):  # NaN guard
            continue
        times[str(eid)] = float(ts)

    adj: Dict[str, Set[str]] = {eid: set() for eid in times.keys()}

    if edges is not None:
        for u, v in edges:
            us = str(u); vs = str(v)
            if us in adj and vs in adj:
                adj[us].add(vs)

    if infer_by_time:
        # O(N log N + N * k) best effort: only wire minimal forward links by timestamp bins
        # We sort events by time; for ties within tolerance, optionally connect as zero-lag
        items = sorted(times.items(), key=lambda kv: kv[1])
        n = len(items)
        for i in range(n):
            ui, ti = items[i]
            succ = 0
            # Greedy forward links with increasing time; cap successors
            for j in range(i + 1, n):
                vj, tj = items[j]
                dt = tj - ti
                if dt < -abs(time_tolerance):
                    # future clock skew beyond tolerance → skip
                    continue
                # within tolerance: treat as zero-lag precedence (optional edge)
                if dt < abs(time_tolerance):
                    adj[ui].add(vj)
                    succ += 1
                else:
                    adj[ui].add(vj)
                    succ += 1
                if max_successors > 0 and succ >= max_successors:
                    break

    return times, adj


def is_acyclic(adj: Dict[str, Set[str]]) -> bool:
    """
    Return True if adjacency adj is acyclic (DAG), False otherwise.
    Uses Kahn's algorithm (iterative) to avoid recursion depth issues. O(V + E).
    """
    # Build indegree map
    indeg: Dict[str, int] = {u: 0 for u in adj.keys()}
    for u, vs in adj.items():
        for v in vs:
            if v not in indeg:
                indeg[v] = 0
            indeg[v] += 1

    # Initialize queue with zero‑indegree nodes
    from collections import deque
    q = deque([u for u, d in indeg.items() if d == 0])
    visited = 0

    # Copy adjacency to avoid mutating caller data
    local_adj: Dict[str, Set[str]] = {u: set(vs) for u, vs in adj.items()}

    while q:
        u = q.popleft()
        visited += 1
        for v in list(local_adj.get(u, ())):  # type: ignore
            indeg[v] -= 1
            # remove edge u->v from local view
            try:
                local_adj[u].remove(v)
            except KeyError:
                pass
            if indeg[v] == 0:
                q.append(v)

    # If all nodes were visited via zero‑indegree pops, graph is acyclic
    return visited == len(indeg)


def transitive_reduction(
    adj: Dict[str, Set[str]],
    *,
    max_edges: int = 200_000,
) -> Dict[str, Set[str]]:
    """
    Compute a transitive reduction (TR) approximation by removing edges u->v that
    are redundant via another path u -> ... -> v.

    Exact TR on arbitrary DAGs can be expensive; this routine caps work by a
    global edge budget. If the budget is exceeded, returns a best-effort reduction.

    Returns a new adjacency dict.
    """
    # Copy adjacency
    red: Dict[str, Set[str]] = {u: set(vs) for u, vs in adj.items()}

    # Early exit if graph is small
    total_e = sum(len(vs) for vs in red.values())
    if total_e == 0:
        return red

    # For each (u, v), see if there is an alternate path u -> w -> ... -> v
    processed = 0
    for u, vs in list(red.items()):
        if not vs:
            continue
        # union of successors of successors (limited expansion)
        # we use a bounded BFS from each successor to detect reachability back to v
        for v in list(vs):
            if processed >= max_edges:
                return red
            processed += 1
            # bounded reachability from neighbors of u excluding direct edge to v
            frontier = list(red[u] - {v})
            seen: Set[str] = set(frontier)
            found = False
            # breadth-first up to a reasonable depth cap to avoid worst-case blowup
            depth = 0
            DEPTH_CAP = 32
            while frontier and depth < DEPTH_CAP and processed < max_edges:
                depth += 1
                nxt: List[str] = []
                for w in frontier:
                    processed += 1
                    if w == v:
                        found = True
                        break
                    for z in red.get(w, ()):  # type: ignore
                        if z not in seen:
                            seen.add(z)
                            nxt.append(z)
                if found:
                    break
                frontier = nxt
            if found:
                # remove redundant edge
                try:
                    red[u].remove(v)
                except KeyError:
                    pass
    return red
