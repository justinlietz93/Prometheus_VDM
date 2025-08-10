# announce.py
"""
Event schema for the void-walker announcement bus (Active Domain Cartography input).

Blueprint alignment:
- Use void equations for traversal/measuring: walkers traverse using your RE-VGSP/GDSP deltas
  and publish compact observations only (no W dumps).
- ADC consumes only these observations to maintain territories/boundaries incrementally.
- This keeps introspection cost proportional to the number of announcements, not to N.

Kinds:
- "region_stat": aggregate stats for a small visited set (mean/var over W, mean coupling S_ij)
- "boundary_probe": evidence of a low-coupling cut between neighborhoods (candidate boundary)
- "cycle_hit": a loop was closed during a walk (B1 proxy event)
- "novel_frontier": sustained novelty ridge / new subdomain frontier

Notes:
- All floats are plain Python floats to keep JSON-friendly if logged.
- nodes is small (sampled IDs visited during the walk). Keep it compact (<= ~64).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict, Any


@dataclass
class Observation:
    tick: int
    kind: str  # "region_stat" | "boundary_probe" | "cycle_hit" | "novel_frontier"
    # Small, representative subset of node ids touched during the walk or boundary sample
    nodes: List[int] = field(default_factory=list)

    # Optional centroid in an embedding space if available (not required)
    centroid: Optional[Tuple[float, float, float]] = None

    # Aggregate stats over the local visited set
    w_mean: float = 0.0
    w_var: float = 0.0
    s_mean: float = 0.0  # mean positive coupling encountered during the walk

    # Boundary-specific signal (strength of cut across a small boundary sample)
    cut_strength: float = 0.0

    # Cycle-specific fields
    loop_len: int = 0
    loop_gain: float = 0.0  # accumulated positive transition weights along the loop

    # Coverage bin for ADC scheduling and map updates (e.g., int(vt_coverage*10))
    coverage_id: int = 0

    # Optional hint from the domain/cartographer
    domain_hint: str = ""

    # Extra metadata bag for future-proofing (small; JSON-serializable only)
    meta: Dict[str, Any] = field(default_factory=dict)


def validate_observation(o: Observation) -> bool:
    """Light sanity checks to avoid corrupting the bus/ADC with malformed events."""
    if not isinstance(o.tick, int) or o.tick < 0:
        return False
    if o.kind not in ("region_stat", "boundary_probe", "cycle_hit", "novel_frontier"):
        return False
    if not isinstance(o.nodes, list):
        return False
    # keep nodes tiny to avoid large payloads by accident
    if len(o.nodes) > 256:
        return False
    return True