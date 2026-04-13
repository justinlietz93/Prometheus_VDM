"""
Validate the cubic spacetime discretization choices.

Runs matched pulse tests for:
- periodic 6-neighbor control
- open 6-neighbor control
- open metric-aware 26-neighbor stencil
- open metric-aware 26-neighbor stencil without calibration

Outputs machine-readable metrics and a concise markdown summary.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent

import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from run_sim import apply_stimulus, build_cubic_lattice
from vdm_runtime import Connectome
from vdm_runtime.void_equations import C_SIGNAL


PHASE_VAR_THRESHOLD = 1e-2
FIELD_DEPARTURE_THRESHOLD = 0.05
CONDENSED_BOND_THRESHOLD = 0.8


@dataclass(frozen=True)
class CaseSpec:
    name: str
    boundary: str
    stencil: str
    transport_calibration: str


def index_to_coord(index: int, shape: tuple[int, int, int]) -> tuple[int, int, int]:
    lx, ly, _ = shape
    z, rem = divmod(index, lx * ly)
    y, x = divmod(rem, lx)
    return x, y, z


def pulse_seed_centers(shape: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    lx, ly, lz = shape
    return [
        (lx // 4, ly // 2, lz // 2),
        (3 * lx // 4, ly // 2, lz // 2),
    ]


def distance_to_seed(
    index: int,
    shape: tuple[int, int, int],
    centers: list[tuple[int, int, int]],
    boundary: str,
) -> float:
    x, y, z = index_to_coord(index, shape)
    distances = []
    for cx, cy, cz in centers:
        dx = abs(x - cx)
        dy = abs(y - cy)
        dz = abs(z - cz)
        if boundary == "periodic":
            dx = min(dx, shape[0] - dx)
            dy = min(dy, shape[1] - dy)
            dz = min(dz, shape[2] - dz)
        distances.append(float(np.sqrt(dx * dx + dy * dy + dz * dz)))
    return min(distances) if distances else 0.0


def first_tick_where(values, predicate):
    for tick, value in enumerate(values):
        if predicate(value):
            return tick
    return None


def first_large_condensation_jump(condensed: list[int], initial_edges: int) -> tuple[int | None, int]:
    threshold = max(25, int(round(0.005 * initial_edges)))
    for tick in range(1, len(condensed)):
        if condensed[tick] - condensed[tick - 1] >= threshold:
            return tick, threshold
    return None, threshold


def fit_front_speed(
    radii: list[tuple[int, float]],
    front_fit_window: int = 20,
) -> float | None:
    times = []
    distances = []
    for tick, radius in radii:
        if tick <= 0 or tick > front_fit_window:
            continue
        if radius <= 0.0:
            continue
        times.append(float(tick))
        distances.append(float(radius))
    if len(times) < 2:
        return None
    slope, _intercept = np.polyfit(np.array(times), np.array(distances), 1)
    return float(slope)


def observation_front_speed(
    first_visit: np.ndarray,
    shape: tuple[int, int, int],
    boundary: str,
    front_fit_window: int = 20,
) -> float | None:
    centers = pulse_seed_centers(shape)
    radii = []
    for tick in range(1, front_fit_window + 1):
        nodes = np.flatnonzero(first_visit == tick)
        if nodes.size == 0:
            continue
        distances = [
            distance_to_seed(int(index), shape, centers, boundary) for index in nodes
        ]
        radii.append((tick, float(np.percentile(distances, 95))))
    return fit_front_speed(radii, front_fit_window=front_fit_window)


def morphology_metrics(
    phi: np.ndarray,
    shape: tuple[int, int, int],
    boundary: str,
) -> dict:
    positive = np.flatnonzero(phi > 0.9)
    negative = np.flatnonzero(phi < 0.1)
    interface = np.flatnonzero((phi > 0.35) & (phi < 0.65))

    def axis_touch(nodes: np.ndarray) -> dict:
        if nodes.size == 0:
            return {"x": False, "y": False, "z": False}
        coords = np.array([index_to_coord(int(i), shape) for i in nodes], dtype=np.int32)
        return {
            "x": bool(np.any(coords[:, 0] == 0) and np.any(coords[:, 0] == shape[0] - 1)),
            "y": bool(np.any(coords[:, 1] == 0) and np.any(coords[:, 1] == shape[1] - 1)),
            "z": bool(np.any(coords[:, 2] == 0) and np.any(coords[:, 2] == shape[2] - 1)),
        }

    def extent_fraction(nodes: np.ndarray) -> dict:
        if nodes.size == 0:
            return {"x": 0.0, "y": 0.0, "z": 0.0}
        coords = np.array([index_to_coord(int(i), shape) for i in nodes], dtype=np.int32)
        spans = coords.max(axis=0) - coords.min(axis=0) + 1
        return {
            "x": float(spans[0] / shape[0]),
            "y": float(spans[1] / shape[1]),
            "z": float(spans[2] / shape[2]),
        }

    interface_touch = axis_touch(interface)
    extent = extent_fraction(positive)
    return {
        "positive_nodes": int(positive.size),
        "negative_nodes": int(negative.size),
        "interface_nodes": int(interface.size),
        "positive_extent_fraction": extent,
        "positive_extent_anisotropy": float(max(extent.values()) - min(extent.values())),
        "interface_wrap_axes": interface_touch if boundary == "periodic" else {},
        "wrap_axes_count": int(sum(interface_touch.values())) if boundary == "periodic" else 0,
    }


def condensed_component_metrics(conn) -> dict:
    condensed_adj = [[] for _ in range(conn.N)]
    edge_count = 0
    for i in range(conn.N):
        for idx, nbr in enumerate(conn.adj[i]):
            j = int(nbr)
            if i >= j:
                continue
            if float(conn.psi_curr[i][idx]) <= CONDENSED_BOND_THRESHOLD:
                continue
            condensed_adj[i].append(j)
            condensed_adj[j].append(i)
            edge_count += 1

    component_sizes = []
    visited = np.zeros(conn.N, dtype=bool)
    for node in range(conn.N):
        if visited[node] or not condensed_adj[node]:
            continue
        stack = [node]
        visited[node] = True
        size = 0
        while stack:
            current = stack.pop()
            size += 1
            for nbr in condensed_adj[current]:
                if not visited[nbr]:
                    visited[nbr] = True
                    stack.append(nbr)
        component_sizes.append(size)

    component_sizes.sort(reverse=True)
    return {
        "condensed_edge_count": edge_count,
        "condensed_component_count": len(component_sizes),
        "largest_condensed_component_nodes": int(component_sizes[0]) if component_sizes else 0,
    }


def morphology_note(metrics: dict) -> str:
    notes = []
    anisotropy = metrics["morphology"]["positive_extent_anisotropy"]
    if metrics["morphology"]["wrap_axes_count"] > 0:
        notes.append(f"periodic wrap on {metrics['morphology']['wrap_axes_count']} axis/axes")
    if anisotropy >= 0.5:
        notes.append(f"strong axis bias ({anisotropy:.3f})")
    elif anisotropy >= 0.25:
        notes.append(f"moderate axis bias ({anisotropy:.3f})")
    else:
        notes.append(f"lower axis bias ({anisotropy:.3f})")
    components = metrics["condensed_components"]["condensed_component_count"]
    largest = metrics["condensed_components"]["largest_condensed_component_nodes"]
    if components == 0:
        notes.append("no condensed bond component")
    else:
        notes.append(f"{components} condensed component(s), largest={largest} nodes")
    return "; ".join(notes)


def run_case(case: CaseSpec, target_n: int, ticks: int, amp: float) -> dict:
    actual_n, lattice_def, lx, ly, lz = build_cubic_lattice(
        target_n,
        boundary=case.boundary,
        stencil=case.stencil,
        transport_calibration=case.transport_calibration,
    )
    shape = (lx, ly, lz)
    conn = Connectome(actual_n, lattice_def.edges, lattice_metadata=lattice_def.metadata)

    first_visit = np.full(actual_n, -1, dtype=np.int32)
    walkers = []
    phi_var = []
    condensed = []
    field_front_radii = []
    centers = pulse_seed_centers(shape)

    for tick in range(ticks):
        apply_stimulus(
            conn,
            "pulse",
            tick,
            actual_n,
            amp=amp,
            lattice_shape=shape,
            boundary=case.boundary,
        )
        result = conn.step(tick)

        newly_observed = (conn.last_visit >= 0) & (first_visit < 0)
        first_visit[newly_observed] = tick

        walkers.append(int(result["n_walkers"]))
        phi_var.append(float(result["phi_var"]))
        condensed.append(
            int(np.sum(np.concatenate(conn.psi_curr) > CONDENSED_BOND_THRESHOLD))
            if any(row.size for row in conn.psi_curr)
            else 0
        )
        disturbed = np.flatnonzero(np.abs(conn.phi_curr - 0.5) >= FIELD_DEPARTURE_THRESHOLD)
        if disturbed.size:
            distances = [
                distance_to_seed(int(index), shape, centers, case.boundary)
                for index in disturbed
            ]
            field_front_radii.append((tick, float(np.percentile(distances, 95))))

    front_speed = fit_front_speed(field_front_radii)
    observation_speed = observation_front_speed(first_visit, shape, case.boundary)
    first_walker_tick = first_tick_where(walkers, lambda value: value > 0)
    phi_var_rise_tick = first_tick_where(phi_var, lambda value: value >= PHASE_VAR_THRESHOLD)
    condensation_tick, condensation_threshold = first_large_condensation_jump(
        condensed,
        len(lattice_def.edges),
    )
    morphology = morphology_metrics(conn.phi_curr, shape, case.boundary)
    component_metrics = condensed_component_metrics(conn)

    result = {
        "name": case.name,
        "boundary": case.boundary,
        "stencil": case.stencil,
        "transport_calibration": case.transport_calibration,
        "transport_renormalization": float(lattice_def.metadata["transport_renormalization"]),
        "nodes": actual_n,
        "edges": len(lattice_def.edges),
        "shape": list(shape),
        "target_c_signal": float(C_SIGNAL),
        "field_front_speed": front_speed,
        "field_front_threshold": FIELD_DEPARTURE_THRESHOLD,
        "observation_front_speed_secondary": observation_speed,
        "first_walker_tick": first_walker_tick,
        "phi_var_rise_tick": phi_var_rise_tick,
        "phi_var_threshold": PHASE_VAR_THRESHOLD,
        "condensation_jump_tick": condensation_tick,
        "condensation_jump_threshold": condensation_threshold,
        "phase_separation_precedes_condensation": (
            phi_var_rise_tick is not None
            and condensation_tick is not None
            and phi_var_rise_tick < condensation_tick
        ),
        "final_phi_var": float(phi_var[-1]),
        "final_condensed_bonds": int(condensed[-1]),
        "max_walkers": int(max(walkers) if walkers else 0),
        "morphology": morphology,
        "condensed_components": component_metrics,
        "timeseries": {
            "walkers": walkers,
            "phi_var": phi_var,
            "condensed_bonds": condensed,
        },
        "lattice_metadata": lattice_def.metadata,
    }
    result["morphology_note"] = morphology_note(result)
    return result


def robust_effects(results: list[dict]) -> list[str]:
    effects = []
    if all(result["first_walker_tick"] == 1 for result in results):
        effects.append("walker ignition occurs immediately after the pulse in every measured case")
    if all(result["phase_separation_precedes_condensation"] for result in results):
        effects.append("field variance rise precedes the first large condensation jump in every measured case")
    return effects


def likely_artifacts(results: list[dict]) -> list[str]:
    artifacts = []
    periodic = next((result for result in results if result["name"] == "periodic6"), None)
    open6 = next((result for result in results if result["name"] == "open6"), None)
    open26 = next((result for result in results if result["name"] == "open26_calibrated"), None)
    if periodic and open6:
        if abs(periodic["final_phi_var"] - open6["final_phi_var"]) < 0.03:
            artifacts.append("periodic vs open boundary did not strongly separate final phi_var on this small pulse test")
    if open6 and open26:
        if open26["morphology"]["positive_extent_anisotropy"] < open6["morphology"]["positive_extent_anisotropy"]:
            artifacts.append("the weighted-26 experiment reduces axis anisotropy relative to open-6 in the final positive phase extent")
    return artifacts


def report_markdown(results: list[dict]) -> str:
    robust = robust_effects(results)
    artifacts = likely_artifacts(results)
    lookup = {result["name"]: result for result in results}
    lines = [
        "# Spacetime Discretization Comparison",
        "",
        "## Change log",
        "",
        "- Measurement only: expanded the comparison runner to use field-departure transport metrics, condensed-bond component summaries, and morphology notes.",
        "- Measurement only: added a structured markdown report and machine-readable comparison output for side-by-side lattice/boundary cases.",
        "",
        "## What changed in measurement/reporting",
        "",
        "- Primary transport metric is now field-front speed measured from `|phi - 0.5| >= 0.05`, rather than `last_visit`.",
        "- `last_visit` remains available only as the clearly secondary `observation_front_speed_secondary` diagnostic.",
        "- Reporting now includes first walker tick, first meaningful `phi_var` rise tick, first large condensation jump tick, final `phi_var`, final condensed bond count, condensed-component structure, and morphology notes.",
        "",
        "## Comparison table",
        "",
        "| case | first walker | phi_var rise | condensation jump | final phi_var | final condensed | field front speed | morphology notes |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        field_front = "n/a" if result["field_front_speed"] is None else f"{result['field_front_speed']:.4f}"
        walker = "n/a" if result["first_walker_tick"] is None else str(result["first_walker_tick"])
        phi_rise = "n/a" if result["phi_var_rise_tick"] is None else str(result["phi_var_rise_tick"])
        cond = "n/a" if result["condensation_jump_tick"] is None else str(result["condensation_jump_tick"])
        lines.append(
            f"| {result['name']} | {walker} | {phi_rise} | {cond} | "
            f"{result['final_phi_var']:.4f} | {result['final_condensed_bonds']} | "
            f"{field_front} | {result['morphology_note']} |"
        )

    lines.extend(["", "## Robust effects vs likely artifacts", ""])
    if robust:
        for effect in robust:
            lines.append(f"- Robust: {effect}")
    if artifacts:
        for effect in artifacts:
            lines.append(f"- Likely artifact-like or discretization-sensitive: {effect}")
    if not robust and not artifacts:
        lines.append("- The current small comparison does not cleanly separate robust behavior from lattice-specific behavior.")

    lines.extend(["", "## Calibration residual", ""])
    raw = lookup.get("open26_raw")
    cal = lookup.get("open26_calibrated")
    if raw and cal:
        field_raw = "n/a" if raw["field_front_speed"] is None else f"{raw['field_front_speed']:.4f}"
        field_cal = "n/a" if cal["field_front_speed"] is None else f"{cal['field_front_speed']:.4f}"
        residual = (
            "n/a"
            if cal["field_front_speed"] is None
            else f"{abs(cal['field_front_speed'] - cal['target_c_signal']):.4f}"
        )
        lines.append(
            f"- Raw weighted-26 renormalization: {raw['transport_renormalization']:.6f}; "
            f"calibrated weighted-26 renormalization: {cal['transport_renormalization']:.6f}."
        )
        lines.append(
            f"- Field-front speed shifts from {field_raw} to {field_cal}; "
            f"target `C_SIGNAL` is {cal['target_c_signal']:.4f}; residual mismatch after calibration is {residual}."
        )

    lines.extend(
        [
            "",
            "## What did NOT change in runtime physics semantics",
            "",
            "- Governing equations were not edited.",
            "- Superposition IC semantics were not edited.",
            "- Dynamic bond admissibility and dynamic bond creation semantics were not edited.",
            "- Active runtime defaults were not edited in this task.",
            "- No new normalization, clipping, gating, or heuristic smoothing was inserted into the runtime physics path.",
            "",
            "## Potential physics-semantic changes that were intentionally NOT implemented",
            "",
            "- No retuning of theory constants to chase front-speed agreement.",
            "- No change to dynamic walker-instantiated bond geometry semantics.",
            "- No change to runtime defaults to force one discretization into production.",
            "- No additional bond-admissibility filters or transport heuristics.",
            "",
            "## Recommendation",
            "",
        ]
    )
    open6 = lookup.get("open6")
    open26 = lookup.get("open26_calibrated")
    if open6 and open26 and open26["morphology"]["positive_extent_anisotropy"] < open6["morphology"]["positive_extent_anisotropy"]:
        lines.append("- promising but not canon-ready")
    else:
        lines.append("- needs better measurement first")

    lines.extend(
        [
            "",
            "## Final checklist",
            "",
            "- Governing equations changed? no",
            "- IC semantics changed? no",
            "- Dynamic bond semantics changed? no",
            "- Transport semantics in active runtime path changed? no",
            "- Defaults changed? no",
            "- New optional experimental modes added? no",
            "- Any heuristic/proxy inserted into physics path? no",
        ]
    )
    return "\n".join(lines) + "\n"


def markdown_summary(results: list[dict]) -> str:
    lookup = {result["name"]: result for result in results}
    lines = [
        "# Spacetime Discretization Validation",
        "",
        "## Tier 2: Transport sanity",
        "",
        "| case | boundary | stencil | renorm | front speed | first walkers | phi_var rise | condensation jump |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for result in results:
        front = "n/a" if result["field_front_speed"] is None else f"{result['field_front_speed']:.4f}"
        walkers = "n/a" if result["first_walker_tick"] is None else str(result["first_walker_tick"])
        phi_rise = "n/a" if result["phi_var_rise_tick"] is None else str(result["phi_var_rise_tick"])
        cond = "n/a" if result["condensation_jump_tick"] is None else str(result["condensation_jump_tick"])
        lines.append(
            f"| {result['name']} | {result['boundary']} | {result['stencil']} | "
            f"{result['transport_renormalization']:.6f} | {front} | {walkers} | {phi_rise} | {cond} |"
        )

    lines.extend(
        [
            "",
            "## Tier 3: Calibration",
            "",
        ]
    )
    raw = lookup.get("open26_raw")
    cal = lookup.get("open26_calibrated")
    if raw and cal:
        raw_front = "n/a" if raw["field_front_speed"] is None else f"{raw['field_front_speed']:.4f}"
        cal_front = "n/a" if cal["field_front_speed"] is None else f"{cal['field_front_speed']:.4f}"
        lines.append(
            f"Weighted-26 raw uses renormalization {raw['transport_renormalization']:.6f}; "
            f"calibrated uses {cal['transport_renormalization']:.6f}."
        )
        lines.append(
            f"Front speed shifts from {raw_front} to {cal_front}; "
            f"phi_var rise shifts from {raw['phi_var_rise_tick']} to {cal['phi_var_rise_tick']}."
        )
        if lookup.get("periodic6") and cal["field_front_speed"] is not None:
            target = lookup["periodic6"]["target_c_signal"]
            residual = abs(cal["field_front_speed"] - target)
            lines.append(
                f"Target C_SIGNAL is {target:.4f}; calibrated weighted-26 still carries "
                f"a residual front-speed mismatch of {residual:.4f} on this small test."
            )

    lines.extend(
        [
            "",
            "## Tier 4: Morphology and admissibility",
            "",
        ]
    )
    for result in results:
        morph = result["morphology"]
        lines.append(
            f"- {result['name']}: wrap_axes_count={morph['wrap_axes_count']}, "
            f"anisotropy={morph['positive_extent_anisotropy']:.3f}, "
            f"phase_before_condensation={result['phase_separation_precedes_condensation']}"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Validate cubic spacetime discretization.")
    parser.add_argument("--N", type=int, default=512, help="Target cubic node count")
    parser.add_argument("--ticks", type=int, default=120, help="Ticks per case")
    parser.add_argument("--amp", type=float, default=0.08, help="Pulse amplitude")
    parser.add_argument(
        "--out-dir",
        type=str,
        default=None,
        help="Output directory (default: analysis/spacetime_discretization/<timestamp>)",
    )
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "analysis" / "spacetime_discretization" / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    cases = [
        CaseSpec("periodic6", "periodic", "6", "legacy_face_6_low_k"),
        CaseSpec("open6", "open", "6", "legacy_face_6_low_k"),
        CaseSpec("open26_raw", "open", "26", "none"),
        CaseSpec("open26_calibrated", "open", "26", "legacy_face_6_low_k"),
    ]

    results = [run_case(case, target_n=args.N, ticks=args.ticks, amp=args.amp) for case in cases]

    comparison_path = out_dir / "comparison.json"
    comparison_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    summary_path = out_dir / "summary.md"
    summary_path.write_text(markdown_summary(results), encoding="utf-8")

    report_path = out_dir / "report.md"
    report_path.write_text(report_markdown(results), encoding="utf-8")

    print(f"Wrote {comparison_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {report_path}")


if __name__ == "__main__":
    main()
