"""
VDM Metriplectic Klein-Gordon field equations.

The theory constants are split into:
- Category 1: free parameters of the action.
- Category 2: CF-derived quantities computed from category 1.

The lattice/stencil is part of the discrete spatial operator. Changing the
boundary condition or stencil changes transport and must therefore be tracked
explicitly, not treated as a rendering detail.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np


# Category 1: free parameters of the discrete action.
J_COUPLING: float = 0.0125
LAMBDA: float = 1.0
GAMMA_DAMP: float = 0.5
EPS_BOND: float = 200.0
LAMBDA_BOND: float = 1.0
BETA_DEBT: float = 0.1


# Category 2: CF-derived quantities.
A_LATTICE: float = 1.0
DT: float = 1.0

C_SQ = 2.0 * J_COUPLING * A_LATTICE**2
D_DIFF = C_SQ / GAMMA_DAMP
TAU = 1.0 / GAMMA_DAMP
C_SIGNAL = float(np.sqrt(D_DIFF / TAU))
TAU_BOND = EPS_BOND * DT**2


DEFAULT_WEIGHT_RULE = "inverse_r2"
DEFAULT_TRANSPORT_CALIBRATION = "legacy_face_6_low_k"
DEFAULT_DYNAMIC_BOND_GEOM_WEIGHT = 1.0


@dataclass(frozen=True)
class LatticeEdge:
    """One undirected substrate edge with geometric transport metadata."""

    u: int
    v: int
    geom_weight: float
    distance: float
    neighbor_class: str


@dataclass(frozen=True)
class LatticeDefinition:
    """Initial computational lattice plus metadata for transport calibration."""

    edges: List[LatticeEdge]
    metadata: Dict[str, object]

    def edge_pairs(self) -> List[Tuple[int, int]]:
        return [(edge.u, edge.v) for edge in self.edges]


def _canonical_stencil(stencil: str | int, ndim: int) -> str:
    text = str(stencil).strip().lower()
    if ndim == 3:
        aliases = {
            "6": "6",
            "face": "6",
            "18": "18",
            "edge": "18",
            "26": "26",
            "weighted26": "26",
            "26w": "26",
        }
    else:
        aliases = {
            "4": "4",
            "6": "4",
            "face": "4",
            "8": "8",
            "26": "8",
            "weighted8": "8",
        }
    if text not in aliases:
        raise ValueError(f"Unsupported {ndim}D stencil: {stencil}")
    return aliases[text]


def _stencil_offsets(ndim: int, stencil: str) -> List[Tuple[int, ...]]:
    offsets: List[Tuple[int, ...]] = []
    for delta in np.ndindex(*(3,) * ndim):
        offset = tuple(int(v) - 1 for v in delta)
        if all(v == 0 for v in offset):
            continue
        nnz = sum(1 for v in offset if v != 0)
        if stencil in {"4", "6"} and nnz != 1:
            continue
        if stencil in {"8", "18"} and nnz > 2:
            continue
        offsets.append(offset)
    return offsets


def _neighbor_class(offset: Iterable[int]) -> str:
    nnz = sum(1 for value in offset if value != 0)
    if nnz == 1:
        return "face"
    if nnz == 2:
        return "edge"
    if nnz == 3:
        return "corner"
    raise ValueError(f"Unsupported displacement: {tuple(offset)}")


def _offset_distance_sq(offset: Iterable[int]) -> float:
    return float(sum((A_LATTICE * float(value)) ** 2 for value in offset))


def _geometry_weight(offset: Iterable[int], weight_rule: str = DEFAULT_WEIGHT_RULE) -> float:
    if weight_rule != DEFAULT_WEIGHT_RULE:
        raise ValueError(f"Unsupported weight rule: {weight_rule}")
    return 1.0 / _offset_distance_sq(offset)


def _axis_second_moment(offsets: List[Tuple[int, ...]], weight_rule: str) -> float:
    tensor = np.zeros(len(offsets[0]), dtype=np.float64)
    for offset in offsets:
        disp = A_LATTICE * np.array(offset, dtype=np.float64)
        tensor += _geometry_weight(offset, weight_rule) * disp * disp
    return float(np.mean(tensor))


def _transport_renormalization(
    offsets: List[Tuple[int, ...]],
    ndim: int,
    weight_rule: str,
    calibration: str,
) -> Tuple[float, float, float]:
    actual = _axis_second_moment(offsets, weight_rule)
    reference_offsets = _stencil_offsets(ndim, "6" if ndim == 3 else "4")
    reference = _axis_second_moment(reference_offsets, DEFAULT_WEIGHT_RULE)
    if calibration == "none":
        return 1.0, actual, reference
    if calibration != DEFAULT_TRANSPORT_CALIBRATION:
        raise ValueError(f"Unsupported transport calibration: {calibration}")
    return reference / actual, actual, reference


def build_ring_lattice_spec(N: int, k: int = 3) -> LatticeDefinition:
    """k-nearest-neighbor ring computational lattice."""

    edge_map: Dict[Tuple[int, int], LatticeEdge] = {}
    for i in range(N):
        for offset in range(1, k + 1):
            j = (i + offset) % N
            u, v = (i, j) if i < j else (j, i)
            edge_map[(u, v)] = LatticeEdge(
                u=u,
                v=v,
                geom_weight=1.0 / float(offset * offset),
                distance=A_LATTICE * float(offset),
                neighbor_class="ring",
            )

    edge_list = [edge_map[key] for key in sorted(edge_map)]
    metadata = {
        "lattice_kind": "ring",
        "dimensions": [N, 1, 1],
        "boundary": "periodic",
        "stencil": f"ring_k{k}",
        "weight_rule": DEFAULT_WEIGHT_RULE,
        "weight_rule_expression": "w = 1 / r^2",
        "transport_calibration": "none",
        "transport_renormalization": 1.0,
        "neighbor_classes": {
            "ring": {
                "distance_min": float(A_LATTICE),
                "distance_max": float(A_LATTICE * k),
                "edge_count": len(edge_list),
            }
        },
        "dynamic_bond_geom_weight": DEFAULT_DYNAMIC_BOND_GEOM_WEIGHT,
        "dynamic_bond_geometry_mode": "unit_weight",
        "edge_count": len(edge_list),
    }
    return LatticeDefinition(edge_list, metadata)


def build_ring_lattice(N: int, k: int = 3) -> List[Tuple[int, int]]:
    return build_ring_lattice_spec(N, k).edge_pairs()


def build_grid_lattice_spec(
    Nx: int,
    Ny: int,
    Nz: int = 1,
    boundary: str = "periodic",
    stencil: str | int = "6",
    weight_rule: str = DEFAULT_WEIGHT_RULE,
    calibration: str = DEFAULT_TRANSPORT_CALIBRATION,
) -> LatticeDefinition:
    """
    Metric-aware 2D/3D grid. Node index: i = x + y*Nx + z*Nx*Ny.

    The returned transport renormalization keeps the low-k coefficient of the
    weighted stencil aligned with the legacy face-only control operator.
    """

    ndim = 3 if Nz > 1 else 2
    boundary = boundary.strip().lower()
    if boundary not in {"open", "periodic"}:
        raise ValueError(f"Unsupported boundary type: {boundary}")

    canonical_stencil = _canonical_stencil(stencil, ndim)
    offsets = _stencil_offsets(ndim, canonical_stencil)
    renorm, raw_moment, ref_moment = _transport_renormalization(
        offsets, ndim, weight_rule, calibration
    )

    def idx(x: int, y: int, z: int) -> int:
        return x + y * Nx + z * Nx * Ny

    def project(coord: int, limit: int) -> int | None:
        if boundary == "periodic":
            return coord % limit
        if 0 <= coord < limit:
            return coord
        return None

    edge_map: Dict[Tuple[int, int], LatticeEdge] = {}
    class_counts: Dict[str, int] = {}
    for z in range(Nz):
        for y in range(Ny):
            for x in range(Nx):
                i = idx(x, y, z)
                for offset in offsets:
                    dx = offset[0]
                    dy = offset[1]
                    dz = offset[2] if ndim == 3 else 0
                    x2 = project(x + dx, Nx)
                    y2 = project(y + dy, Ny)
                    z2 = project(z + dz, Nz)
                    if x2 is None or y2 is None or z2 is None:
                        continue
                    j = idx(x2, y2, z2)
                    if i == j:
                        continue
                    u, v = (i, j) if i < j else (j, i)
                    if (u, v) in edge_map:
                        continue
                    neighbor_class = _neighbor_class(offset)
                    edge_map[(u, v)] = LatticeEdge(
                        u=u,
                        v=v,
                        geom_weight=_geometry_weight(offset, weight_rule),
                        distance=float(np.sqrt(_offset_distance_sq(offset))),
                        neighbor_class=neighbor_class,
                    )
                    class_counts[neighbor_class] = class_counts.get(neighbor_class, 0) + 1

    edge_list = [edge_map[key] for key in sorted(edge_map)]
    class_metadata: Dict[str, Dict[str, float | int]] = {}
    class_weights: Dict[str, float] = {}
    for neighbor_class in sorted(class_counts):
        exemplar = next(edge for edge in edge_list if edge.neighbor_class == neighbor_class)
        class_metadata[neighbor_class] = {
            "distance": exemplar.distance,
            "geom_weight": exemplar.geom_weight,
            "edge_count": class_counts[neighbor_class],
        }
        class_weights[neighbor_class] = exemplar.geom_weight

    metadata = {
        "lattice_kind": "grid",
        "dimensions": [Nx, Ny, Nz],
        "boundary": boundary,
        "stencil": canonical_stencil,
        "weight_rule": weight_rule,
        "weight_rule_expression": "w = 1 / r^2",
        "class_weights": class_weights,
        "transport_calibration": calibration,
        "transport_renormalization": renorm,
        "transport_reference": "legacy_face_6_low_k",
        "raw_axis_second_moment": raw_moment,
        "reference_axis_second_moment": ref_moment,
        "neighbor_classes": class_metadata,
        "directed_offset_count": len(offsets),
        "edge_count": len(edge_list),
        "dynamic_bond_geom_weight": DEFAULT_DYNAMIC_BOND_GEOM_WEIGHT,
        "dynamic_bond_geometry_mode": "unit_weight",
    }
    return LatticeDefinition(edge_list, metadata)


def build_grid_lattice(
    Nx: int,
    Ny: int,
    Nz: int = 1,
    periodic: bool = True,
) -> List[Tuple[int, int]]:
    boundary = "periodic" if periodic else "open"
    return build_grid_lattice_spec(
        Nx,
        Ny,
        Nz,
        boundary=boundary,
        stencil="6",
        calibration="none",
    ).edge_pairs()


def bond_decoherence_floor(kT: float) -> float:
    """eta = sqrt(2 * kT / eps_bond)."""

    if kT <= 0.0:
        return 0.0
    return float(np.sqrt(2.0 * kT / EPS_BOND))


def bond_weighted_laplacian(
    phi: np.ndarray,
    adj_lists: List[np.ndarray],
    psi: List[np.ndarray],
    geom_weights: List[np.ndarray] | None = None,
    transport_renormalization: float = 1.0,
) -> np.ndarray:
    """(L_psi phi)_i = sum_j g_ij * psi_ij * (phi_j - phi_i)."""

    N = phi.shape[0]
    out = np.zeros(N, dtype=np.float64)
    for i in range(N):
        nbrs = adj_lists[i]
        if nbrs.size == 0:
            continue
        edge_weight = psi[i]
        if geom_weights is not None:
            edge_weight = edge_weight * geom_weights[i]
        out[i] = transport_renormalization * np.sum(edge_weight * (phi[nbrs] - phi[i]))
    return out


def node_potential_derivative(phi: np.ndarray, lam: float = LAMBDA) -> np.ndarray:
    """V'(phi) = 2 * lambda * phi * (1 - phi) * (1 - 2phi)."""

    return 2.0 * lam * phi * (1.0 - phi) * (1.0 - 2.0 * phi)


def node_potential(phi: np.ndarray, lam: float = LAMBDA) -> np.ndarray:
    """V(phi) = lambda * phi^2 * (1 - phi)^2."""

    return lam * phi**2 * (1.0 - phi) ** 2


def bond_potential_derivative(
    psi: np.ndarray,
    lam_bond: float = LAMBDA_BOND,
) -> np.ndarray:
    """U'(psi) = 2 * lambda_bond * psi * (1 - psi) * (1 - 2psi)."""

    return 2.0 * lam_bond * psi * (1.0 - psi) * (1.0 - 2.0 * psi)


def bond_gradient_source(phi_i: float, phi_j: np.ndarray) -> np.ndarray:
    """0.5 * (phi_j - phi_i)^2 from the action variation dS/dpsi."""

    return 0.5 * (phi_j - phi_i) ** 2


def get_constants() -> dict:
    """Theory constants for telemetry and checkpoints."""

    return {
        "J_COUPLING": J_COUPLING,
        "LAMBDA": LAMBDA,
        "GAMMA_DAMP": GAMMA_DAMP,
        "EPS_BOND": EPS_BOND,
        "LAMBDA_BOND": LAMBDA_BOND,
        "BETA_DEBT": BETA_DEBT,
        "A_LATTICE": A_LATTICE,
        "DT": DT,
        "TAU": TAU,
        "D_DIFF": D_DIFF,
        "C_SQ": C_SQ,
        "C_SIGNAL": C_SIGNAL,
        "TAU_BOND": TAU_BOND,
    }
