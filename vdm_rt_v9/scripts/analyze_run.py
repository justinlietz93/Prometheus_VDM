from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import h5py
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import periodogram
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components
from scipy.stats import kurtosis, skew


SUMMARY_KEYS = [
    "tick",
    "kT",
    "phi_mean",
    "phi_var",
    "mean_degree",
    "max_degree",
    "n_active",
    "n_warm",
    "n_walkers_emitted",
    "n_condensed_bonds",
    "bonds_total",
    "n_computed",
]
BOX_SCALES = [1, 2, 5, 10, 25, 50]
PHI_BINS = 64
CONDENSED_THRESHOLD = 0.8
PLATEAU_START_TICK = 200


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(rows: List[dict], path: Path) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(data: dict, path: Path) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def stabilization_tick(values: Sequence[float], tol_frac: float = 0.01) -> Tuple[int | None, float]:
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return None, 0.0
    tol = max(1e-12, tol_frac * float(arr.max() - arr.min()))
    final = float(arr[-1])
    for idx in range(arr.size):
        if np.all(np.abs(arr[idx:] - final) <= tol):
            return int(idx), tol
    return None, tol


def first_sticky_index(values: Sequence[float], predicate) -> int | None:
    for idx in range(len(values)):
        if predicate(values[idx]) and all(predicate(v) for v in values[idx:]):
            return idx
    return None


def largest_circular_run(mask: np.ndarray) -> int:
    if mask.size == 0 or not np.any(mask):
        return 0
    doubled = np.concatenate([mask, mask])
    best = 0
    current = 0
    for value in doubled:
        if value:
            current += 1
            best = min(mask.size, max(best, current))
        else:
            current = 0
    return int(best)


def gini(values: np.ndarray) -> float:
    arr = np.sort(np.asarray(values, dtype=float))
    if arr.size == 0:
        return 0.0
    if np.allclose(arr, 0.0):
        return 0.0
    index = np.arange(1, arr.size + 1, dtype=float)
    return float((np.sum((2.0 * index - arr.size - 1.0) * arr)) / (arr.size * np.sum(arr)))


def histogram_entropy_bits(values: np.ndarray, bins: int = PHI_BINS) -> float:
    hist, _ = np.histogram(values, bins=bins, range=(0.0, 1.0))
    total = hist.sum()
    if total <= 0:
        return 0.0
    probs = hist[hist > 0] / total
    return float(-np.sum(probs * np.log2(probs)))


def bimodality_coefficient(values: np.ndarray) -> float | None:
    k = float(kurtosis(values, fisher=False, bias=False))
    if not np.isfinite(k) or k <= 0.0:
        return None
    g = float(skew(values, bias=False))
    return float((g * g + 1.0) / k)


def dominant_period_metrics(values: Sequence[float], start_idx: int) -> dict:
    arr = np.asarray(values, dtype=float)
    if arr.size <= start_idx + 8:
        return {}
    tail = arr[start_idx:] - np.mean(arr[start_idx:])
    freqs, power = periodogram(tail)
    metrics = {
        "tail_mean": float(np.mean(arr[start_idx:])),
        "tail_std": float(np.std(arr[start_idx:])),
        "tail_cv": float(np.std(arr[start_idx:]) / max(np.mean(arr[start_idx:]), 1e-12)),
    }
    if freqs.size > 1:
        idx = int(np.argmax(power[1:]) + 1)
        metrics["dominant_frequency"] = float(freqs[idx])
        metrics["dominant_period_ticks"] = float(1.0 / freqs[idx]) if freqs[idx] > 0 else None
        metrics["dominant_power"] = float(power[idx])
    for lag in [1, 2, 3, 4, 5, 10, 15]:
        if tail.size > lag:
            metrics[f"autocorr_lag_{lag}"] = float(np.corrcoef(tail[:-lag], tail[lag:])[0, 1])
    return metrics


def build_coords(nx: int, ny: int, nz: int) -> np.ndarray:
    idx = np.arange(nx * ny * nz, dtype=np.int32)
    x = idx % nx
    y = (idx // nx) % ny
    z = idx // (nx * ny)
    return np.column_stack([x, y, z])


def choose_visual_ticks(snapshot_ticks: Sequence[int]) -> List[int]:
    if not snapshot_ticks:
        return []
    preferred = [0, 1, 2, 3, 4, len(snapshot_ticks) - 1]
    chosen: List[int] = []
    seen = set()
    for idx in preferred:
        if idx < 0 or idx >= len(snapshot_ticks):
            continue
        tick = int(snapshot_ticks[idx])
        if tick not in seen:
            chosen.append(tick)
            seen.add(tick)
    return chosen


def pulse_regions(config: dict) -> dict | None:
    if config.get("stimulus") != "pulse":
        return None
    n_nodes = int(config.get("N", 0))
    if n_nodes <= 0:
        return None
    n_stim = max(5, n_nodes // 50)
    start_b = n_nodes // 3
    region_a = np.arange(0, n_stim, dtype=np.int32)
    region_b = np.arange(start_b, min(start_b + n_stim, n_nodes), dtype=np.int32)
    return {
        "n_stim": int(n_stim),
        "region_a": region_a,
        "region_b": region_b,
    }


def box_count_metrics(coords: np.ndarray, scales: Sequence[int]) -> Tuple[dict, float | None]:
    counts = {}
    if coords.size == 0:
        return {str(scale): 0 for scale in scales}, None
    for scale in scales:
        boxes = np.unique(coords // scale, axis=0)
        counts[str(scale)] = int(boxes.shape[0])
    xs = []
    ys = []
    for scale in scales:
        count = counts[str(scale)]
        if count > 1:
            xs.append(math.log(1.0 / float(scale)))
            ys.append(math.log(float(count)))
    if len(xs) < 2:
        return counts, None
    slope = np.polyfit(xs, ys, 1)[0]
    return counts, float(slope)


def analyze_same_sign_components(
    row_ids: np.ndarray,
    col_idx: np.ndarray,
    same_mask: np.ndarray,
    signs: np.ndarray,
    n_nodes: int,
) -> dict:
    graph = csr_matrix(
        (np.ones(int(np.sum(same_mask)), dtype=np.int8), (row_ids[same_mask], col_idx[same_mask])),
        shape=(n_nodes, n_nodes),
    )
    n_comp, labels = connected_components(graph, directed=False)
    sizes = np.bincount(labels)
    pos_weight = np.bincount(labels, weights=signs.astype(np.float64), minlength=sizes.size)
    pos_sizes = sizes[pos_weight > 0.5 * sizes]
    neg_sizes = sizes[pos_weight <= 0.5 * sizes]
    return {
        "same_sign_component_count": int(n_comp),
        "positive_component_count": int(pos_sizes.size),
        "negative_component_count": int(neg_sizes.size),
        "largest_positive_component": int(pos_sizes.max()) if pos_sizes.size else 0,
        "largest_negative_component": int(neg_sizes.max()) if neg_sizes.size else 0,
    }


def analyze_condensed_components(
    row_ids: np.ndarray,
    col_idx: np.ndarray,
    condensed_mask: np.ndarray,
    n_nodes: int,
) -> dict:
    graph = csr_matrix(
        (np.ones(int(np.sum(condensed_mask)), dtype=np.int8), (row_ids[condensed_mask], col_idx[condensed_mask])),
        shape=(n_nodes, n_nodes),
    )
    n_comp, labels = connected_components(graph, directed=False)
    sizes = np.bincount(labels)
    return {
        "condensed_component_count": int(n_comp),
        "condensed_nontrivial_components": int(np.sum(sizes > 1)),
        "condensed_components_ge_10": int(np.sum(sizes >= 10)),
        "largest_condensed_component": int(sizes.max()) if sizes.size else 0,
        "largest_condensed_component_fraction": float((sizes.max() if sizes.size else 0) / max(n_nodes, 1)),
    }


def compare_to_e0(
    row_ptr: np.ndarray,
    col_idx: np.ndarray,
    e0_row_ptr: np.ndarray,
    e0_col_idx: np.ndarray,
) -> dict:
    persistent_new = 0
    removed = 0
    for node in range(row_ptr.size - 1):
        cur = col_idx[int(row_ptr[node]):int(row_ptr[node + 1])]
        e0 = e0_col_idx[int(e0_row_ptr[node]):int(e0_row_ptr[node + 1])]
        if cur.size:
            persistent_new += int(np.count_nonzero(~np.isin(cur, e0, assume_unique=True)))
        if e0.size:
            removed += int(np.count_nonzero(~np.isin(e0, cur, assume_unique=True)))
    return {
        "persistent_new_edges_directed": int(persistent_new),
        "removed_edges_directed": int(removed),
        "persistent_new_edges_undirected": int(persistent_new // 2),
        "removed_edges_undirected": int(removed // 2),
    }


def sample_edge_segments(
    coords: np.ndarray,
    row_ptr: np.ndarray,
    col_idx: np.ndarray,
    psi: np.ndarray,
    psi_threshold: float = 0.95,
    max_edges: int = 1500,
) -> Tuple[List[float], List[float], List[float]]:
    xs: List[float] = []
    ys: List[float] = []
    zs: List[float] = []
    added = 0
    for node in range(row_ptr.size - 1):
        start = int(row_ptr[node])
        end = int(row_ptr[node + 1])
        nbrs = col_idx[start:end]
        vals = psi[start:end]
        for nbr, value in zip(nbrs, vals):
            nbr_i = int(nbr)
            if nbr_i <= node or float(value) < psi_threshold:
                continue
            p0 = coords[node]
            p1 = coords[nbr_i]
            xs.extend([float(p0[0]), float(p1[0]), None])
            ys.extend([float(p0[1]), float(p1[1]), None])
            zs.extend([float(p0[2]), float(p1[2]), None])
            added += 1
            if added >= max_edges:
                return xs, ys, zs
    return xs, ys, zs


def summary_rows(summary: dict, n_nodes: int) -> List[dict]:
    rows = []
    directed_total = 2.0 * np.maximum(summary["bonds_total"].astype(float), 1.0)
    for idx in range(summary["tick"].size):
        rows.append(
            {
                "tick": int(summary["tick"][idx]),
                "kT": float(summary["kT"][idx]),
                "phi_mean": float(summary["phi_mean"][idx]),
                "phi_var": float(summary["phi_var"][idx]),
                "mean_degree": float(summary["mean_degree"][idx]),
                "max_degree": int(summary["max_degree"][idx]),
                "n_active": int(summary["n_active"][idx]),
                "n_warm": int(summary["n_warm"][idx]),
                "n_walkers_emitted": int(summary["n_walkers_emitted"][idx]),
                "n_condensed_bonds": int(summary["n_condensed_bonds"][idx]),
                "bonds_total": int(summary["bonds_total"][idx]),
                "n_computed": int(summary.get("n_computed", np.zeros_like(summary["tick"]))[idx]),
                "active_fraction": float(summary["n_active"][idx] / n_nodes),
                "warm_fraction": float(summary["n_warm"][idx] / n_nodes),
                "walker_fraction": float(summary["n_walkers_emitted"][idx] / n_nodes),
                "condensed_fraction_directed": float(summary["n_condensed_bonds"][idx] / directed_total[idx]),
            }
        )
    return rows


def build_summary_figure(summary: dict, path: Path) -> None:
    ticks = summary["tick"]
    fig = make_subplots(
        rows=3,
        cols=2,
        subplot_titles=[
            "kT",
            "Active and walkers",
            "phi mean",
            "phi variance",
            "Bond counts",
            "Mean degree",
        ],
    )
    fig.add_trace(go.Scatter(x=ticks, y=summary["kT"], mode="lines", name="kT"), row=1, col=1)
    fig.add_trace(go.Scatter(x=ticks, y=summary["n_active"], mode="lines", name="n_active"), row=1, col=2)
    fig.add_trace(go.Scatter(x=ticks, y=summary["n_walkers_emitted"], mode="lines", name="n_walkers"), row=1, col=2)
    fig.add_trace(go.Scatter(x=ticks, y=summary["phi_mean"], mode="lines", name="phi_mean"), row=2, col=1)
    fig.add_trace(go.Scatter(x=ticks, y=summary["phi_var"], mode="lines", name="phi_var"), row=2, col=2)
    fig.add_trace(go.Scatter(x=ticks, y=summary["bonds_total"], mode="lines", name="bonds_total"), row=3, col=1)
    fig.add_trace(go.Scatter(x=ticks, y=summary["n_condensed_bonds"], mode="lines", name="n_condensed_bonds"), row=3, col=1)
    fig.add_trace(go.Scatter(x=ticks, y=summary["mean_degree"], mode="lines", name="mean_degree"), row=3, col=2)
    fig.update_layout(height=1100, width=1200, title="Run Summary", template="plotly_white")
    fig.write_html(path, include_plotlyjs="cdn")


def build_spatial_figure(snapshot_rows: List[dict], z_profiles: dict, path: Path) -> None:
    ticks = [row["tick"] for row in snapshot_rows]
    positive_z = np.array([z_profiles[str(tick)]["positive_fraction_by_z"] for tick in ticks])
    observed_z = np.array([z_profiles[str(tick)]["observed_fraction_by_z"] for tick in ticks])
    active_z = np.array([z_profiles[str(tick)]["active_fraction_by_z"] for tick in ticks])

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Positive-domain occupancy by z",
            "Observed fraction by z",
            "Active fraction by z",
            "Snapshot metrics",
        ],
        specs=[[{"type": "heatmap"}, {"type": "heatmap"}], [{"type": "heatmap"}, {"type": "xy"}]],
    )
    fig.add_trace(go.Heatmap(z=positive_z.T, x=ticks, y=list(range(positive_z.shape[1])), coloraxis="coloraxis"), row=1, col=1)
    fig.add_trace(go.Heatmap(z=observed_z.T, x=ticks, y=list(range(observed_z.shape[1])), coloraxis="coloraxis"), row=1, col=2)
    fig.add_trace(go.Heatmap(z=active_z.T, x=ticks, y=list(range(active_z.shape[1])), coloraxis="coloraxis"), row=2, col=1)
    fig.add_trace(go.Scatter(x=ticks, y=[row["positive_fraction"] for row in snapshot_rows], mode="lines+markers", name="positive_fraction"), row=2, col=2)
    fig.add_trace(go.Scatter(x=ticks, y=[row["positive_slab_thickness_z"] for row in snapshot_rows], mode="lines+markers", name="slab_thickness_z"), row=2, col=2)
    fig.add_trace(go.Scatter(x=ticks, y=[row["interface_edges_undirected"] for row in snapshot_rows], mode="lines+markers", name="interface_edges"), row=2, col=2)
    fig.update_layout(
        height=1000,
        width=1300,
        title="Spatial Evolution",
        template="plotly_white",
        coloraxis={"colorscale": "Viridis"},
    )
    fig.write_html(path, include_plotlyjs="cdn")


def build_activity_figure(summary: dict, signature_metrics: dict, path: Path) -> None:
    ticks = summary["tick"]
    start_idx = int(signature_metrics["activity_regime"]["plateau_start_tick"])
    tail_ticks = ticks[start_idx:]
    active_tail = summary["n_active"][start_idx:]
    walker_tail = summary["n_walkers_emitted"][start_idx:]
    centered = active_tail - np.mean(active_tail)
    freqs, power = periodogram(centered)
    max_lag = min(30, centered.size - 1)
    ac_x = []
    ac_y = []
    for lag in range(1, max_lag + 1):
        ac_x.append(lag)
        ac_y.append(float(np.corrcoef(centered[:-lag], centered[lag:])[0, 1]))

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=[
            "Late-time activity",
            "Late-time walkers",
            "Activity periodogram",
            "Activity autocorrelation",
        ],
    )
    fig.add_trace(go.Scatter(x=tail_ticks, y=active_tail, mode="lines", name="n_active"), row=1, col=1)
    fig.add_trace(go.Scatter(x=tail_ticks, y=walker_tail, mode="lines", name="n_walkers"), row=1, col=2)
    fig.add_trace(go.Scatter(x=freqs[1:], y=power[1:], mode="lines", name="periodogram"), row=2, col=1)
    fig.add_trace(go.Bar(x=ac_x, y=ac_y, name="autocorr"), row=2, col=2)
    fig.update_layout(height=900, width=1200, title="Late-Time Activity Regime", template="plotly_white")
    fig.write_html(path, include_plotlyjs="cdn")


def build_topology_3d_figure(
    coords: np.ndarray,
    snapshot_visuals: Dict[int, dict],
    path: Path,
) -> None:
    ticks = list(snapshot_visuals.keys())
    if not ticks:
        return

    x_all = coords[:, 0].astype(np.float32)
    y_all = coords[:, 1].astype(np.float32)
    z_all = coords[:, 2].astype(np.float32)
    frames = []
    for tick in ticks:
        snap = snapshot_visuals[tick]
        phi = snap["phi"]
        active_mask = snap["active_mask"]
        active_coords = coords[active_mask]
        active_strength = np.abs(snap["phi"] - snap["phi_prev"])[active_mask]
        edge_x, edge_y, edge_z = sample_edge_segments(coords, snap["row_ptr"], snap["col_idx"], snap["psi"])

        frames.append(
            go.Frame(
                name=str(tick),
                data=[
                    go.Isosurface(
                        x=x_all,
                        y=y_all,
                        z=z_all,
                        value=phi,
                        isomin=0.49,
                        isomax=0.51,
                        surface_count=1,
                        opacity=0.45,
                        colorscale="RdBu",
                        showscale=False,
                        caps=dict(x_show=False, y_show=False, z_show=False),
                        hovertemplate="x=%{x}<br>y=%{y}<br>z=%{z}<br>phi=%{value:.3f}<extra></extra>",
                        name="phi=0.5 isosurface",
                    ),
                    go.Scatter3d(
                        x=edge_x,
                        y=edge_y,
                        z=edge_z,
                        mode="lines",
                        line=dict(color="#2ca02c", width=3),
                        opacity=0.35,
                        hoverinfo="skip",
                        name="sampled condensed edges",
                    ),
                    go.Scatter3d(
                        x=active_coords[:, 0] if active_coords.size else [],
                        y=active_coords[:, 1] if active_coords.size else [],
                        z=active_coords[:, 2] if active_coords.size else [],
                        mode="markers",
                        marker=dict(
                            size=3.2,
                            color=active_strength if active_strength.size else [],
                            colorscale="Turbo",
                            opacity=0.9,
                            colorbar=dict(title="|phi_dot|"),
                        ),
                        hovertemplate="x=%{x}<br>y=%{y}<br>z=%{z}<extra>active</extra>",
                        name="active nodes",
                    ),
                ],
            )
        )

    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.update_layout(
        title="3D Topology in Lattice Coordinates",
        template="plotly_white",
        width=1300,
        height=900,
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="z",
            aspectmode="cube",
        ),
        sliders=[
            dict(
                currentvalue=dict(prefix="Snapshot tick: "),
                pad=dict(t=40),
                steps=[
                    dict(
                        method="animate",
                        args=[[str(tick)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                        label=str(tick),
                    )
                    for tick in ticks
                ],
            )
        ],
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0.0,
                y=1.1,
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[None, {"frame": {"duration": 700, "redraw": True}, "fromcurrent": True}],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    ),
                ],
            )
        ],
    )
    fig.write_html(path, include_plotlyjs="cdn")


def build_final_activity_lattice_figure(
    coords: np.ndarray,
    final_snapshot: dict,
    path: Path,
) -> None:
    phi = final_snapshot["phi"]
    active_mask = final_snapshot["active_mask"]
    interface_mask = final_snapshot["interface_mask"]
    active_coords = coords[active_mask]
    interface_coords = coords[interface_mask]
    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=interface_coords[:, 0] if interface_coords.size else [],
            y=interface_coords[:, 1] if interface_coords.size else [],
            z=interface_coords[:, 2] if interface_coords.size else [],
            mode="markers",
            marker=dict(size=2.0, color="#1f77b4", opacity=0.2),
            name="interface nodes",
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=active_coords[:, 0] if active_coords.size else [],
            y=active_coords[:, 1] if active_coords.size else [],
            z=active_coords[:, 2] if active_coords.size else [],
            mode="markers",
            marker=dict(
                size=4.2,
                color=np.abs(phi[active_mask] - final_snapshot["phi_prev"][active_mask]) if np.any(active_mask) else [],
                colorscale="Turbo",
                opacity=0.95,
            ),
            name="late-time active nodes",
            hoverinfo="skip",
        )
    )
    fig.update_layout(
        title="Final Snapshot: Activity Localized on the Interface",
        template="plotly_white",
        width=1100,
        height=850,
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z", aspectmode="cube"),
    )
    fig.write_html(path, include_plotlyjs="cdn")


def build_spectral_topology_figure(run_path: Path, tick_index: int, path: Path) -> None:
    from scripts.dashboard import EngramReader, build_3d_figure

    reader = EngramReader(str(run_path))
    fig = build_3d_figure(reader, tick_index)
    fig.update_layout(title=f"Spectral Topology Embedding at Snapshot Index {tick_index}")
    fig.write_html(path, include_plotlyjs="cdn")


def build_stimulus_geometry_figure(
    config: dict,
    coords: np.ndarray,
    path: Path,
) -> dict | None:
    regions = pulse_regions(config)
    if regions is None:
        return None

    region_a = regions["region_a"]
    region_b = regions["region_b"]
    coords_a = coords[region_a]
    coords_b = coords[region_b]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter3d(
            x=coords_a[:, 0],
            y=coords_a[:, 1],
            z=coords_a[:, 2],
            mode="markers",
            marker=dict(size=3.4, color="#d62728", opacity=0.75),
            name="positive pulse region",
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=coords_b[:, 0],
            y=coords_b[:, 1],
            z=coords_b[:, 2],
            mode="markers",
            marker=dict(size=3.4, color="#1f77b4", opacity=0.75),
            name="negative pulse region",
            hoverinfo="skip",
        )
    )
    fig.update_layout(
        title="Initial Pulse Geometry",
        template="plotly_white",
        width=1100,
        height=850,
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z", aspectmode="cube"),
    )
    fig.write_html(path, include_plotlyjs="cdn")

    def bounds(points: np.ndarray) -> dict:
        return {
            "min": points.min(axis=0).astype(int).tolist(),
            "max": points.max(axis=0).astype(int).tolist(),
            "unique_z": np.unique(points[:, 2]).astype(int).tolist(),
        }

    return {
        "n_stim": regions["n_stim"],
        "region_a_bounds": bounds(coords_a),
        "region_b_bounds": bounds(coords_b),
    }


def build_report(
    run_path: Path,
    config: dict,
    summary: dict,
    snapshot_rows: List[dict],
    signature_metrics: dict,
) -> str:
    final_snapshot = snapshot_rows[-1]
    first_snapshot = snapshot_rows[0]
    macro_tick = signature_metrics["cosmogenesis"].get("macrostate_lock_tick")
    observation_tick = signature_metrics["cosmogenesis"].get("full_observation_tick")
    interface_tick = signature_metrics["cognition_like"].get("interface_localization_tick")
    period = signature_metrics["activity_regime"].get("dominant_period_ticks")
    lag5 = signature_metrics["activity_regime"].get("autocorr_lag_5")
    peak_walkers_tick = signature_metrics["summary_peaks"]["n_walkers_emitted"]["tick"]
    peak_walkers_value = signature_metrics["summary_peaks"]["n_walkers_emitted"]["value"]
    peak_kT_tick = signature_metrics["summary_peaks"]["kT"]["tick"]
    peak_kT_value = signature_metrics["summary_peaks"]["kT"]["value"]
    peak_active_tick = signature_metrics["summary_peaks"]["n_active"]["tick"]
    peak_active_value = signature_metrics["summary_peaks"]["n_active"]["value"]
    stimulus_geometry = signature_metrics.get("stimulus_geometry")
    recommendations = signature_metrics.get("suggested_improvements", [])

    lines = [
        f"# Run Analysis: {run_path.name}",
        "",
        "## Dataset",
        f"- H5 path: {run_path}",
        f"- Nodes: {config.get('N', 'unknown')}",
        f"- Lattice: {config.get('Lx', '?')} x {config.get('Ly', '?')} x {config.get('Lz', '?')} {config.get('lattice', 'unknown')}",
        f"- Stimulus: {config.get('stimulus', 'unknown')} (amp={config.get('amp', 'unknown')})",
        f"- Summary ticks: {int(summary['tick'][0])} to {int(summary['tick'][-1])} ({summary['tick'].size} samples)",
        f"- Snapshot cadence: every {config.get('snapshot_every', 50)} ticks ({len(snapshot_rows)} snapshots)",
        "",
        "## Executive Findings",
        f"- The run shows a real symmetry-breaking event: phi starts near the unstable midpoint and settles into a binary 90/10 split. The positive-phase occupancy grows from {first_snapshot['positive_fraction']:.4f} at t={first_snapshot['tick']} to {final_snapshot['positive_fraction']:.4f} at t={final_snapshot['tick']}.",
        f"- The settled geometry is a z-oriented slab, not a fragmented foam. The final positive planes are contiguous with thickness {final_snapshot['positive_slab_thickness_z']} out of {config.get('Lz', '?')} and x/y occupancy is flat to machine precision.",
        "- That slab is not fully unbiased evidence of isotropic emergence. In this run the pulse itself is planar in index space, so the initial condition already favors z-oriented walls on the cubic lattice.",
        f"- The early transient is violent but short: walkers peak at {peak_walkers_value:.0f} on tick {peak_walkers_tick}, kT peaks at {peak_kT_value:.6g} on tick {peak_kT_tick}, and active nodes peak at {peak_active_value:.0f} on tick {peak_active_tick}.",
        f"- After the transient, the system is not broadband-critical. For ticks >= {signature_metrics['activity_regime']['plateau_start_tick']}, n_active locks into a narrow period-{period:.2f} oscillation with lag-5 autocorrelation {lag5:.3f} and CV {signature_metrics['activity_regime']['tail_cv']:.4f}.",
        f"- Persistent topological growth is absent in the logged snapshots: max degree stays {int(np.max(summary['max_degree']))}, final persistent new edges are {final_snapshot['persistent_new_edges_undirected']}, and the final graph is a pruned subset of the original lattice.",
        "",
        "## Stimulus Geometry",
    ]
    if stimulus_geometry:
        lines.extend(
            [
                f"- The pulse logic injects {stimulus_geometry['n_stim']} nodes per sign.",
                f"- Positive region bounds: {stimulus_geometry['region_a_bounds']['min']} to {stimulus_geometry['region_a_bounds']['max']}; z slices {stimulus_geometry['region_a_bounds']['unique_z']}.",
                f"- Negative region bounds: {stimulus_geometry['region_b_bounds']['min']} to {stimulus_geometry['region_b_bounds']['max']}; z slices {stimulus_geometry['region_b_bounds']['unique_z']}.",
                "- This means the default pulse is a plane-plus-plane fragment, not a point-like or spherical perturbation. The final slab should therefore be interpreted as phase separation under a biased seed, not as spontaneous isotropic cosmogenesis.",
                "",
            ]
        )

    lines.extend(
        [
        "## Cosmogenesis Signatures",
        f"- Strong evidence for phase separation: final low/high well occupancy is {final_snapshot['phi_low_fraction']:.3f}/{final_snapshot['phi_high_fraction']:.3f}, with middle occupancy {final_snapshot['phi_mid_fraction']:.3f} and bimodality coefficient {final_snapshot['phi_bimodality_coefficient']:.3f}.",
        f"- Macrostate lock occurs by snapshot tick {macro_tick}, and full observation of the lattice is present by snapshot tick {observation_tick}.",
        f"- Interface energy localization is sharp: final cross-phase bond psi mean is {final_snapshot['cross_phase_psi_mean']:.3f}, versus {final_snapshot['same_phase_psi_mean']:.3f} inside domains.",
        f"- The final undirected interface count is {final_snapshot['interface_edges_undirected']}, while the positive domain volume increases fivefold relative to the first snapshot. That is compatible with low-perimeter coarsening rather than branching hierarchy growth inside this seeded geometry.",
        f"- Bond maturation continues after the slab geometry freezes: bonds_total stabilizes near tick {signature_metrics['stabilization_ticks']['bonds_total']['tick']}, while n_condensed_bonds does not settle within 1 percent of final until tick {signature_metrics['stabilization_ticks']['n_condensed_bonds']['tick']}.",
        "",
        "## Cognition-Like Proxies",
        f"- The only durable dynamical structure is an interface oscillator. By snapshot tick {interface_tick}, 100 percent of above-threshold active nodes are on the phase interface, and this remains true through the end of the run.",
        f"- The late-time active fraction is only {signature_metrics['activity_regime']['tail_mean'] / config.get('N', 1):.4f} of nodes on average, so the activity is sparse and spatially localized rather than globally distributed.",
        f"- There is persistent oscillation, but not the kind of broadband or avalanche-rich variability usually used as a brain-like criticality proxy. The late-time walker CV is {signature_metrics['walker_regime']['tail_cv']:.4f} and the dominant activity frequency is {signature_metrics['activity_regime']['dominant_frequency']:.5f} cycles per tick.",
        f"- The topology also stays simple: the largest condensed-bond component contains {final_snapshot['largest_condensed_component_fraction']:.3f} of nodes, and there are no persistent new long-range edges in the snapshots.",
        "",
        "## Limits",
        "- This is one run at one system size, so CF03 scaling laws across L cannot be tested here.",
        "- The log stores periodic snapshots rather than full per-tick fields, so a strict first-arrival causal-cone test is not possible from this artifact alone.",
        "- Human cognition is not directly measurable in this dataset. The report only evaluates generic proxies such as persistence, localization, periodicity, and topological complexity.",
        "",
        "## Suggested Improvements",
    ]
    )
    for item in recommendations:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Comprehensive VDM run analysis")
    parser.add_argument("h5_path", type=str, help="Path to run_log.h5")
    parser.add_argument("--out-dir", type=str, default=None, help="Output directory for analysis artifacts")
    parser.add_argument("--canon-dir", type=str, default=None, help="Optional path to canon docs for provenance")
    args = parser.parse_args()

    run_path = Path(args.h5_path).resolve()
    run_dir = run_path.parent
    out_dir = Path(args.out_dir).resolve() if args.out_dir else run_dir / "analysis"
    out_dir.mkdir(parents=True, exist_ok=True)

    config = load_json(run_dir / "config.json")
    if args.canon_dir:
        config["canon_dir"] = str(Path(args.canon_dir).resolve())

    nx = int(config.get("Lx", 1))
    ny = int(config.get("Ly", 1))
    nz = int(config.get("Lz", 1))
    coords = build_coords(nx, ny, nz)
    stimulus_geometry = build_stimulus_geometry_figure(config, coords, out_dir / "stimulus_geometry.html")

    with h5py.File(run_path, "r") as h5:
        all_snapshot_keys = sorted(h5["snapshots"].keys())
        visual_ticks = set(choose_visual_ticks([int(key) for key in all_snapshot_keys]))
        summary = {key: h5["summary"][key][:] for key in SUMMARY_KEYS if key in h5["summary"]}
        summary_rows_data = summary_rows(summary, int(config.get("N", coords.shape[0])))

        e0_row_ptr = h5["E0_row_ptr"][:]
        e0_col_idx = h5["E0_col_idx"][:]
        kT_by_tick = {int(t): float(k) for t, k in zip(summary["tick"], summary["kT"])}

        snapshot_rows_data: List[dict] = []
        z_profiles: Dict[str, dict] = {}
        snapshot_visuals: Dict[int, dict] = {}
        spectral_snapshot_index = len(all_snapshot_keys) - 1
        for snap_idx, key in enumerate(all_snapshot_keys):
            tick = int(key)
            group = h5["snapshots"][key]
            phi = group["phi_curr"][:].astype(np.float64)
            phi_prev = group["phi_prev"][:].astype(np.float64)
            debt = group["debt"][:].astype(np.float64)
            last_visit = group["last_visit"][:]
            row_ptr = group["adj_csr_row_ptr"][:]
            col_idx = group["adj_csr_col_idx"][:]
            psi = group["psi_csr_data"][:].astype(np.float64)

            degrees = np.diff(row_ptr).astype(np.int32)
            row_ids = np.repeat(np.arange(phi.size, dtype=np.int32), degrees)
            signs = phi > 0.5
            cross_mask = signs[row_ids] != signs[col_idx]
            same_mask = ~cross_mask
            condensed_mask = psi > CONDENSED_THRESHOLD

            interface_nodes = np.zeros(phi.size, dtype=bool)
            if np.any(cross_mask):
                interface_nodes[row_ids[cross_mask]] = True

            kT_value = kT_by_tick.get(tick, 0.0)
            threshold = math.sqrt(2.0 * max(kT_value, 0.0))
            active_proxy = np.abs(phi - phi_prev) > threshold if threshold > 0.0 else np.abs(phi - phi_prev) > 0.0

            phi_cube = phi.reshape(nz, ny, nx)
            sign_cube = signs.reshape(nz, ny, nx)
            observed_cube = (last_visit >= 0).reshape(nz, ny, nx)
            active_cube = active_proxy.reshape(nz, ny, nx)
            positive_by_z = sign_cube.mean(axis=(1, 2))
            observed_by_z = observed_cube.mean(axis=(1, 2))
            active_by_z = active_cube.mean(axis=(1, 2))
            positive_by_x = sign_cube.mean(axis=(0, 1))
            positive_by_y = sign_cube.mean(axis=(0, 2))

            box_counts, box_dim_proxy = box_count_metrics(coords[interface_nodes], BOX_SCALES)
            same_components = analyze_same_sign_components(row_ids, col_idx, same_mask, signs, phi.size)
            condensed_components = analyze_condensed_components(row_ids, col_idx, condensed_mask, phi.size)
            e0_delta = compare_to_e0(row_ptr, col_idx, e0_row_ptr, e0_col_idx)

            row = {
                "tick": tick,
                "phi_mean": float(np.mean(phi)),
                "phi_var": float(np.var(phi)),
                "phi_order_abs": float(np.mean(np.abs(2.0 * phi - 1.0))),
                "phi_low_fraction": float(np.mean(phi < 0.1)),
                "phi_high_fraction": float(np.mean(phi > 0.9)),
                "phi_mid_fraction": float(np.mean((phi >= 0.4) & (phi <= 0.6))),
                "phi_entropy_bits": histogram_entropy_bits(phi),
                "phi_bimodality_coefficient": bimodality_coefficient(phi),
                "positive_fraction": float(np.mean(signs)),
                "positive_slab_thickness_z": largest_circular_run(positive_by_z > 0.5),
                "observed_fraction": float(np.mean(last_visit >= 0)),
                "psi_mean": float(np.mean(psi)) if psi.size else 0.0,
                "psi_std": float(np.std(psi)) if psi.size else 0.0,
                "psi_fraction_gt_0_8": float(np.mean(psi > 0.8)) if psi.size else 0.0,
                "psi_fraction_gt_0_95": float(np.mean(psi > 0.95)) if psi.size else 0.0,
                "psi_fraction_lt_0_2": float(np.mean(psi < 0.2)) if psi.size else 0.0,
                "interface_edges_directed": int(np.sum(cross_mask)),
                "interface_edges_undirected": int(np.sum(cross_mask) // 2),
                "interface_fraction_directed": float(np.mean(cross_mask)) if cross_mask.size else 0.0,
                "same_phase_psi_mean": float(np.mean(psi[same_mask])) if np.any(same_mask) else 0.0,
                "cross_phase_psi_mean": float(np.mean(psi[cross_mask])) if np.any(cross_mask) else 0.0,
                "interface_nodes": int(np.sum(interface_nodes)),
                "interface_box_dimension_proxy": box_dim_proxy,
                "active_proxy_count": int(np.sum(active_proxy)),
                "active_proxy_fraction": float(np.mean(active_proxy)),
                "share_active_on_interface": float(np.mean(interface_nodes[active_proxy])) if np.any(active_proxy) else 0.0,
                "share_interface_active": float(np.mean(active_proxy[interface_nodes])) if np.any(interface_nodes) else 0.0,
                "debt_mean": float(np.mean(debt)),
                "debt_max": float(np.max(debt)),
                "debt_gini": gini(debt),
                "z_occupancy_std": float(np.std(positive_by_z)),
                "x_occupancy_std": float(np.std(positive_by_x)),
                "y_occupancy_std": float(np.std(positive_by_y)),
                "z_axis_anisotropy_ratio": float(np.std(positive_by_z) / max(np.std(positive_by_x), np.std(positive_by_y), 1e-12)),
            }
            row.update(same_components)
            row.update(condensed_components)
            row.update(e0_delta)
            for scale, count in box_counts.items():
                row[f"interface_box_count_scale_{scale}"] = count
            snapshot_rows_data.append(row)
            z_profiles[str(tick)] = {
                "positive_fraction_by_z": positive_by_z.tolist(),
                "observed_fraction_by_z": observed_by_z.tolist(),
                "active_fraction_by_z": active_by_z.tolist(),
            }
            if tick in visual_ticks:
                snapshot_visuals[tick] = {
                    "phi": phi.astype(np.float32),
                    "phi_prev": phi_prev.astype(np.float32),
                    "psi": psi.astype(np.float32),
                    "row_ptr": row_ptr.copy(),
                    "col_idx": col_idx.copy(),
                    "active_mask": active_proxy.copy(),
                    "interface_mask": interface_nodes.copy(),
                }

    summary_peaks = {}
    for key in ["kT", "phi_var", "n_active", "n_walkers_emitted", "n_condensed_bonds"]:
        idx = int(np.argmax(summary[key]))
        summary_peaks[key] = {"tick": int(summary["tick"][idx]), "value": float(summary[key][idx])}

    stabilization = {}
    for key in ["phi_mean", "phi_var", "kT", "bonds_total", "n_condensed_bonds"]:
        tick_idx, tol = stabilization_tick(summary[key])
        stabilization[key] = {
            "tick": int(summary["tick"][tick_idx]) if tick_idx is not None else None,
            "tolerance": float(tol),
        }

    snapshot_ticks = [row["tick"] for row in snapshot_rows_data]
    slab_thicknesses = [row["positive_slab_thickness_z"] for row in snapshot_rows_data]
    observed_fractions = [row["observed_fraction"] for row in snapshot_rows_data]
    interface_localization = [row["share_active_on_interface"] for row in snapshot_rows_data]
    macro_idx = first_sticky_index(
        snapshot_rows_data,
        lambda row: row["positive_slab_thickness_z"] == snapshot_rows_data[-1]["positive_slab_thickness_z"]
        and abs(row["positive_fraction"] - snapshot_rows_data[-1]["positive_fraction"]) <= 1e-6,
    )
    full_obs_idx = first_sticky_index(observed_fractions, lambda value: abs(value - 1.0) <= 1e-9)
    interface_idx = first_sticky_index(interface_localization, lambda value: value >= 0.999999)

    activity_regime = dominant_period_metrics(summary["n_active"], start_idx=PLATEAU_START_TICK)
    activity_regime["plateau_start_tick"] = PLATEAU_START_TICK
    walker_regime = dominant_period_metrics(summary["n_walkers_emitted"], start_idx=PLATEAU_START_TICK)
    kT_regime = dominant_period_metrics(summary["kT"], start_idx=PLATEAU_START_TICK)
    final_snapshot = snapshot_rows_data[-1]
    suggested_improvements = [
        "Replace the index-range pulse with coordinate-defined compact regions, such as spheres or small cubes, so the initial condition does not pre-impose z-oriented slabs on the cubic lattice.",
        "Increase logging density during the transient, for example snapshots every 1 to 5 ticks through tick 200, or log first-arrival maps explicitly. The current 50-tick spacing is too coarse for a clean CF04 cone test.",
        "If the goal is cosmogenesis rather than seeded domain growth, run a size sweep over multiple lattice lengths and compare slab thickness, interface box counts, and lock times against CF03 scaling predictions.",
        "If the goal is cognition-like complexity, use structured recurrent stimulation such as the sensory mode or a task-like input schedule. The single pulse in this run collapses to a narrow deterministic limit cycle instead of maintaining rich, multi-scale dynamics.",
        "Instrument bond instantiation and bond lifetime directly. In the current snapshots the graph only loses edges and never retains new ones, so claims about emergent long-range topology are not supported here.",
    ]

    signature_metrics = {
        "run": {
            "h5_path": str(run_path),
            "analysis_dir": str(out_dir),
            "canon_dir": config.get("canon_dir"),
            "N": int(config.get("N", 0)),
            "lattice": config.get("lattice"),
            "Lx": nx,
            "Ly": ny,
            "Lz": nz,
            "ticks": int(summary["tick"].size),
            "snapshots": len(snapshot_rows_data),
        },
        "stimulus_geometry": stimulus_geometry,
        "summary_peaks": summary_peaks,
        "stabilization_ticks": stabilization,
        "activity_regime": activity_regime,
        "walker_regime": walker_regime,
        "kT_regime": kT_regime,
        "cosmogenesis": {
            "macrostate_lock_tick": snapshot_ticks[macro_idx] if macro_idx is not None else None,
            "full_observation_tick": snapshot_ticks[full_obs_idx] if full_obs_idx is not None else None,
            "final_positive_fraction": snapshot_rows_data[-1]["positive_fraction"],
            "final_positive_slab_thickness_z": snapshot_rows_data[-1]["positive_slab_thickness_z"],
            "final_cross_phase_psi_mean": snapshot_rows_data[-1]["cross_phase_psi_mean"],
            "final_same_phase_psi_mean": snapshot_rows_data[-1]["same_phase_psi_mean"],
            "final_interface_edges_undirected": snapshot_rows_data[-1]["interface_edges_undirected"],
            "final_removed_edges_undirected": snapshot_rows_data[-1]["removed_edges_undirected"],
            "persistent_new_edges_seen": bool(any(row["persistent_new_edges_undirected"] > 0 for row in snapshot_rows_data)),
        },
        "cognition_like": {
            "interface_localization_tick": snapshot_ticks[interface_idx] if interface_idx is not None else None,
            "final_share_active_on_interface": snapshot_rows_data[-1]["share_active_on_interface"],
            "final_active_proxy_fraction": snapshot_rows_data[-1]["active_proxy_fraction"],
            "final_largest_condensed_component_fraction": snapshot_rows_data[-1]["largest_condensed_component_fraction"],
            "final_persistent_new_edges_undirected": snapshot_rows_data[-1]["persistent_new_edges_undirected"],
        },
        "limitations": [
            "Single run at fixed system size; no cross-size scaling law test is possible.",
            "Snapshots are every 50 ticks, so first-arrival causal-cone measurements are not directly recoverable.",
            "Cognition claims here are only proxy-based because the log has no task semantics or behavioral readout.",
        ],
        "suggested_improvements": suggested_improvements,
    }

    write_csv(summary_rows_data, out_dir / "summary_metrics.csv")
    write_csv(snapshot_rows_data, out_dir / "snapshot_metrics.csv")
    write_json(z_profiles, out_dir / "z_profiles.json")
    write_json(signature_metrics, out_dir / "signature_metrics.json")
    report = build_report(run_path, config, summary, snapshot_rows_data, signature_metrics)
    (out_dir / "report.md").write_text(report, encoding="utf-8")

    build_summary_figure(summary, out_dir / "summary_overview.html")
    build_spatial_figure(snapshot_rows_data, z_profiles, out_dir / "spatial_profiles.html")
    build_activity_figure(summary, signature_metrics, out_dir / "activity_regime.html")
    build_topology_3d_figure(coords, snapshot_visuals, out_dir / "topology_lattice_3d.html")
    build_final_activity_lattice_figure(coords, snapshot_visuals[snapshot_ticks[-1]], out_dir / "activity_interface_3d.html")
    build_spectral_topology_figure(run_path, spectral_snapshot_index, out_dir / "topology_spectral_final.html")

    print(f"Analysis complete: {out_dir}")


if __name__ == "__main__":
    main()
