from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Literal, Tuple


@dataclass
class PlotSpec:
    domain: str
    name: str
    tag: Optional[str] = None
    title: Optional[str] = None
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    cmap: str = "viridis"
    style: Literal["light", "dark"] = "light"
    logx: bool = False
    logy: bool = False
    dpi: int = 160
    size: Tuple[float, float] = (6.4, 4.0)
    legend: bool = True
    tight: bool = True

    # Arbitrary metadata (serialized to sidecar)
    meta: dict = field(default_factory=dict)
