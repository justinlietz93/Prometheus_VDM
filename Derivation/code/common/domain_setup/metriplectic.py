"""
Metriplectic domain setup helpers.

This module provides light-weight normalization and bookkeeping for the
shared parameter set used by the metriplectic instruments suite
(e.g. meters-EBN cone-speed / Lyapunov / degeneracy meters).

It is intentionally minimal: it does not implement any physics, only
parses and normalizes configuration dictionaries so runners and meters
can share a consistent view of:

- Grid size N
- Time step dt
- Klein–Gordon branch parameters (c, m)
- Reaction–diffusion parameters (D, r, lambda)
- Stability/control parameters (CFL, BCs, precision)
- RNG seeds

Canonical parameter semantics, units, and ranges are defined by:
- Derivation/Metriplectic/Metriplectic_Instruments/T2_PROPOSAL_Metriplectic_Instruments_v1.md
- Derivation/z.CANONICAL_Units_Normalization/00_UNITS_NORMALIZATION.md
No thresholds or units are duplicated here.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping, MutableMapping, Dict, Optional, List


_EXPECTED_KEYS = (
    "N",
    "dt",
    "c",
    "m",
    "D",
    "r",
    "lambda",
    "CFL",
    "BCs",
    "precision",
    "seeds",
)


@dataclass
class MetriplecticParams:
    """Normalized metriplectic configuration (shape only, no physics)."""

    N: Optional[int] = None
    dt: Optional[float] = None
    c: Optional[float] = None
    m: Optional[float] = None
    D: Optional[float] = None
    r: Optional[float] = None
    lambda_: Optional[float] = None
    CFL: Optional[float] = None
    BCs: Optional[str] = None
    precision: Optional[str] = None
    seeds: List[int] | None = None
    extra: Dict[str, Any] | None = None


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    return str(value)


def _to_int_list(value: Any) -> List[int] | None:
    if value is None:
        return None
    if isinstance(value, (list, tuple)):
        out: List[int] = []
        for v in value:
            try:
                out.append(int(v))
            except (TypeError, ValueError):
                continue
        return out or None
    try:
        return [int(value)]
    except (TypeError, ValueError):
        return None


def normalize_params(raw: Mapping[str, Any]) -> MetriplecticParams:
    """
    Normalize a raw parameters mapping into a MetriplecticParams instance.

    This is a *shape* normalizer only:

    - It does not enforce ranges or units.
    - It does not fill in proposal-default numeric values, except for neutral
      baselines needed to keep preregistration skeletons runnable (e.g.
      defaulting ``c = 1.0`` when it is omitted).
    - It records any keys not part of the shared meters-EBN parameter set
      in the ``extra`` field so that meter-specific options are preserved.

    Callers should enforce proposal- and schema-level constraints separately.
    """
    data: MutableMapping[str, Any] = dict(raw)

    N = _to_int(data.get("N"))
    dt = _to_float(data.get("dt"))
    # For preregistration skeletons we allow ``c`` to be omitted and fall back
    # to a neutral baseline c = 1.0 so that instruments do not crash on
    # shape-only specs. Gate semantics remain defined exclusively in the
    # metriplectic validation helpers and canonical docs.
    raw_c = data.get("c", 1.0)
    c = _to_float(raw_c)
    m = _to_float(data.get("m"))
    D = _to_float(data.get("D"))
    r = _to_float(data.get("r"))
    lambda_ = _to_float(data.get("lambda"))
    CFL = _to_float(data.get("CFL"))
    BCs = _to_str(data.get("BCs"))
    precision = _to_str(data.get("precision"))
    seeds = _to_int_list(data.get("seeds"))

    extra_keys = {k for k in data.keys() if k not in _EXPECTED_KEYS}
    extra: Dict[str, Any] | None = None
    if extra_keys:
        extra = {k: data[k] for k in sorted(extra_keys)}

    return MetriplecticParams(
        N=N,
        dt=dt,
        c=c,
        m=m,
        D=D,
        r=r,
        lambda_=lambda_,
        CFL=CFL,
        BCs=BCs,
        precision=precision,
        seeds=seeds,
        extra=extra,
    )


def params_as_dict(params: MetriplecticParams) -> Dict[str, Any]:
    """
    Convert a MetriplecticParams instance to a JSON-serializable dict.

    The field ``lambda_`` is exposed as ``"lambda"`` to match spec keys.
    """
    d = asdict(params)
    # Rename lambda_ back to lambda for JSON/metrics
    d["lambda"] = d.pop("lambda_", None)
    return d


__all__ = ["MetriplecticParams", "normalize_params", "params_as_dict"]