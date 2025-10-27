"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles.

Commercial use of proprietary VDM code requires written permission from Justin K. Lietz.
See LICENSE file for full terms.
"""
import pytest

from fum_rt.core.proprioception.territory import TerritoryUF


class Obs:
    """Minimal Observation-like stub with kind and fields used by TerritoryUF.fold()."""
    def __init__(self, kind: str, **kwargs):
        self.kind = kind
        for k, v in (kwargs or {}).items():
            setattr(self, k, v)


def test_union_and_components_with_cycle_hit_and_edge_on():
    uf = TerritoryUF(head_k=8)

    # Two observations that should union (0,1) and (1,2) into a single component
    obs = [
        Obs("cycle_hit", nodes=[0, 1, 9]),
        Obs("edge_on", u=1, v=2),
    ]
    uf.fold(obs)

    # All three nodes should share the same root; components_count should be 1
    # Components count approximates roots; with only one merged, we expect 1.
    assert uf.components_count() == 1
    # Heads should include members of that component, bounded by head_k
    head_any = set(uf.sample_any(8))
    assert {0, 1, 2}.issubset(head_any)


def test_sample_indices_and_any_are_bounded_and_stable():
    uf = TerritoryUF(head_k=4)

    # Create three disjoint edges => components: (0,1), (2,3), (4,5)
    uf.fold([
        Obs("edge_on", u=0, v=1),
        Obs("edge_on", u=2, v=3),
        Obs("edge_on", u=4, v=5),
    ])

    # Each sample should be bounded by k
    s1 = uf.sample_indices(0, 10)
    s2 = uf.sample_any(10)
    assert len(s1) <= 4  # head_k bound
    assert len(s2) <= 10  # request bound
    # Heads should be unique-index lists (no duplicates)
    assert len(s1) == len(set(s1))
    assert len(s2) == len(set(s2))

    # Asking for k=0 returns empty lists
    assert uf.sample_indices(0, 0) == []
    assert uf.sample_any(0) == []


def test_edge_off_marks_dirty_but_does_not_crash_fold():
    uf = TerritoryUF(head_k=4)
    uf.fold([Obs("edge_off", u=10, v=11)])
    # No exceptions, and components can be computed
    _ = uf.components_count()