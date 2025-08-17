from __future__ import annotations

"""
fum_rt.tests.core.test_active_graph_regression

Regression tests for active-graph lower-bound component counting and dirty-flag/audit behavior
in SparseConnectome._maybe_audit_frag (void-faithful, streaming over ACTIVE edges only).

Covers:
- components_lb reflects the number of components in the ACTIVE subgraph
- After removing bridges (splitting the graph), components_lb increases
- After adding a bridge across components, components_lb decreases to 1
- Dirty flag persists when audit budget is exhausted; is cleared only when audit completes
"""

import numpy as np

from fum_rt.core.sparse_connectome import SparseConnectome


def _np_adj_from_sets(N: int, groups: list[list[int]]) -> list[np.ndarray]:
    """
    Build adjacency as undirected clique for each group in groups, disjoint between groups.
    Returns list of numpy int32 arrays per node.
    """
    adj_sets = [set() for _ in range(N)]
    for g in groups:
        gset = set(int(x) for x in g)
        for i in gset:
            for j in gset:
                if i != j:
                    adj_sets[i].add(j)
    return [np.fromiter(sorted(s), dtype=np.int32) if s else np.zeros(0, dtype=np.int32) for s in adj_sets]


def test_active_graph_components_audit_transitions() -> None:
    N = 5
    sc = SparseConnectome(N=N, k=0, seed=0, threshold=0.15, lambda_omega=0.1, candidates=1)
    # Uniform W so that all listed edges are ACTIVE (> threshold)
    sc.W = np.ones(N, dtype=np.float32)

    # Stage 1: fully connected graph -> components_lb == 1
    sc.adj = _np_adj_from_sets(N, [list(range(N))])
    sc._maybe_audit_frag(budget_edges=1_000_000)
    assert int(getattr(sc, "_frag_components_lb", N)) == 1

    # Stage 2: split into two components {0,1} and {2,3,4}
    sc.adj = _np_adj_from_sets(N, [[0, 1], [2, 3, 4]])
    sc._maybe_audit_frag(budget_edges=1_000_000)
    assert int(getattr(sc, "_frag_components_lb", 0)) == 2

    # Stage 3: add a single bridge across the components (1-2)
    adj_sets = [set(a.tolist()) for a in sc.adj]
    adj_sets[1].add(2)
    adj_sets[2].add(1)
    sc.adj = [np.fromiter(sorted(s), dtype=np.int32) if s else np.zeros(0, dtype=np.int32) for s in adj_sets]
    sc._maybe_audit_frag(budget_edges=1_000_000)
    assert int(getattr(sc, "_frag_components_lb", N)) == 1


def test_dirty_flag_persists_when_budget_exhausted() -> None:
    """
    When the audit budget is exhausted, _frag_dirty_since should remain non-None.
    """
    N = 8
    sc = SparseConnectome(N=N, k=0, seed=0, threshold=0.15, lambda_omega=0.1, candidates=1)
    sc.W = np.ones(N, dtype=np.float32)

    # Build a graph with enough edges to exceed the small budget
    sc.adj = _np_adj_from_sets(N, [[0, 1, 2, 3], [4, 5, 6, 7]])
    # Mark as dirty beforehand
    sc._frag_dirty_since = 1234
    # Use a very small budget (1 edge), which should not clear the dirty flag
    sc._maybe_audit_frag(budget_edges=1)
    assert getattr(sc, "_frag_dirty_since", None) is not None, "Dirty flag should persist when budget is exhausted"

    # Now audit with a large budget to allow completion; flag should clear
    sc._maybe_audit_frag(budget_edges=1_000_000)
    assert getattr(sc, "_frag_dirty_since", None) is None, "Dirty flag should clear when audit completes within budget"