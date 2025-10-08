# visualizer.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.
"""
import matplotlib.pyplot as plt
import numpy as np
import imageio
from tqdm import tqdm
import plotly.graph_objects as go
import scipy.sparse
import os
from Void_Equations import delta_re_vgsp, delta_gdsp # Import the void dynamics

def void_driven_layout(W, iterations=50, dim=3):
    """
    Computes a node layout using void dynamics for attraction and repulsion.
    This creates a more organic, biologically plausible layout than random placement.
    Handles both dense and sparse matrices.

    Improvements:
    - O(E) attraction accumulation using numpy.add.at (no NxN tensor)
    - Adaptive, sub-sampled repulsion for large N to avoid O(N^2) blowups
    - Step clipping for stability
    """
    num_nodes = W.shape[0]
    pos = np.random.rand(num_nodes, dim)

    # Extract edges and weights from sparse or dense adjacency
    if scipy.sparse.issparse(W):
        rows, cols = W.nonzero()
        weights = W.data
    else:
        rows, cols = np.where(W > 0)
        weights = W[rows, cols]

    rows = np.asarray(rows, dtype=np.int64)
    cols = np.asarray(cols, dtype=np.int64)
    weights = np.asarray(weights, dtype=float)

    for t_idx in range(iterations):
        # Repulsion (adaptive) — base global void pressure
        if num_nodes <= 800:
            delta = pos[:, np.newaxis, :] - pos[np.newaxis, :, :]
            distance = np.linalg.norm(delta, axis=-1) + 1e-9
            repulsive_force = (1.0 / distance) * (1.0 - (1.0 / distance))
            repulsion = np.sum(delta * (repulsive_force / distance)[..., np.newaxis], axis=1)
        else:
            # Subsample for approximate repulsion, re-scale to keep magnitude consistent
            P = min(400, num_nodes)
            idx = np.random.choice(num_nodes, P, replace=False)
            delta_s = pos[:, np.newaxis, :] - pos[idx][np.newaxis, :, :]
            distance_s = np.linalg.norm(delta_s, axis=-1) + 1e-9
            repulsive_force_s = (1.0 / distance_s) * (1.0 - (1.0 / distance_s))
            repulsion = np.sum(delta_s * (repulsive_force_s / distance_s)[..., np.newaxis], axis=1) * (num_nodes / P)

        # Attraction/Repulsion along existing edges (i -> j), governed by Void Dynamics
        attraction = np.zeros_like(pos)
        vec_ij = pos[cols] - pos[rows]  # direction from i to j
        signs = np.sign(weights).astype(float)  # excitatory(+)/inhibitory(-)

        # Time-dynamic void equations
        try:
            gdsp = delta_gdsp(weights, t_idx, use_time_dynamics=True)  # structural pull/closure
        except Exception:
            gdsp = np.array([delta_gdsp(w, t_idx, use_time_dynamics=True) for w in weights], dtype=float)
        try:
            re_vgsp = delta_re_vgsp(np.abs(weights), t_idx, use_time_dynamics=True)  # resonance modulation
        except Exception:
            re_vgsp = np.array([delta_re_vgsp(abs(w), t_idx, use_time_dynamics=True) for w in weights], dtype=float)

        # Normalize absolute synaptic strength and combine with void signals
        abs_w = np.abs(weights).astype(float)
        if abs_w.size and abs_w.max() > 0:
            abs_w = abs_w / (abs_w.max() + 1e-12)

        # Effective magnitude: strong edges + dynamic modulation
        fmag = abs_w * (1.0 + np.abs(gdsp)) * (1.0 + 0.5 * np.abs(re_vgsp))

        # Direction: excitatory pulls together (+), inhibitory pushes apart (-)
        vec_dir = vec_ij * signs[:, np.newaxis]
        forces = vec_dir * fmag[:, np.newaxis]
        np.add.at(attraction, rows, forces)

        # Global repulsion modulation from RE-VGSP (prevents collapse, encourages differentiation)
        repulsion *= (1.0 + 0.1 * float(np.mean(np.abs(re_vgsp)))) if re_vgsp.size else 1.0

        # Update positions with clipping + annealed step size
        update = repulsion + attraction
        norms = np.linalg.norm(update, axis=1) + 1e-12
        cap = np.percentile(norms, 95)
        scale = np.minimum(1.0, cap / norms)
        step = 0.03 * (0.95 ** t_idx)  # anneal for stability
        pos += step * (update * scale[:, np.newaxis])

    # Normalize positions to [0, 1]^dim
    pos -= pos.min(axis=0)
    span = pos.max(axis=0) - pos.min(axis=0) + 1e-9
    pos /= span

    return {i: pos[i] for i in range(num_nodes)}

def void_traverse_graph(W, iterations=100):
    """
    Traverse the entire connectome via the Void Equations and accumulate per-node potentials.
    Returns a dict with:
      - 'node_potential': ndarray (N,) accumulated resonance/closure magnitude per node
      - 'edge_flux': ndarray (M,) final per-edge flux (|delta_re| + |delta_gd|)*|w|
      - 'rows','cols': edge index mapping for 'edge_flux'
    This can be consumed by the SelfImprovementEngine to guide learning.
    """
    import numpy as _np
    import scipy.sparse as _sp

    N = int(W.shape[0])
    if _sp.issparse(W):
        rows, cols = W.nonzero()
        weights = _np.asarray(W.data, dtype=float)
    else:
        Wd = _np.asarray(W)
        rows, cols = _np.where(Wd != 0)
        weights = _np.asarray(Wd[rows, cols], dtype=float)

    node_potential = _np.zeros(N, dtype=float)
    edge_flux = _np.zeros_like(weights, dtype=float)

    for t in range(int(iterations)):
        try:
            re = delta_re_vgsp(_np.abs(weights), t, use_time_dynamics=True)
        except Exception:
            re = _np.array([delta_re_vgsp(abs(w), t, use_time_dynamics=True) for w in weights], dtype=float)
        try:
            gd = delta_gdsp(weights, t, use_time_dynamics=True)
        except Exception:
            gd = _np.array([delta_gdsp(w, t, use_time_dynamics=True) for w in weights], dtype=float)

        flux = (_np.abs(re) + _np.abs(gd)) * _np.maximum(1e-12, _np.abs(weights))
        edge_flux = flux  # keep last (or could accumulate with +=)

        # Deposit flux to target nodes (incoming) and a small portion to source
        _np.add.at(node_potential, cols, flux)
        _np.add.at(node_potential, rows, 0.25 * flux)

    return {
        "node_potential": node_potential,
        "edge_flux": edge_flux,
        "rows": rows,
        "cols": cols,
    }

def plot_network_graph(W, t, title: str, save_path: str, pos: dict, threshold=0.0, node_strength_mode: str = "inout"):
    """
    Creates a 2D visual representation of the FUM's connectome using a pre-calculated layout.
    Renders all connections above a minimal threshold, with transparency based on weight.
    """
    if scipy.sparse.issparse(W):
        W_dense = W.toarray()
    else:
        W_dense = W

    if hasattr(W_dense, 'cpu'):
        W_dense = W_dense.cpu().numpy()
        
    num_nodes = W_dense.shape[0]
    if not pos:
        pos = {i: np.random.rand(2) for i in range(num_nodes)}

    plt.figure(figsize=(12, 12))
    ax = plt.gca()
    
    node_coords = np.array(list(pos.values()))
    # --- Node coloring by synaptic strength (dark blue = strong, light blue = weak) ---
    absW = np.abs(W_dense)
    in_strength = absW.sum(axis=0)
    out_strength = absW.sum(axis=1)
    mode = str(node_strength_mode).lower()
    if mode == "in":
        strengths = in_strength
    elif mode == "out":
        strengths = out_strength
    else:
        strengths = in_strength + out_strength  # default: total in+out strength
    strengths = np.asarray(strengths, dtype=float)
    cmap = plt.get_cmap('Blues')  # light->dark; high (strong) appears darker
    vmin = float(np.min(strengths))
    vmax = float(np.max(strengths)) if np.max(strengths) > vmin else vmin + 1e-9
    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    node_colors = cmap(norm(strengths))
    ax.scatter(node_coords[:, 0], node_coords[:, 1], s=150, color=node_colors, alpha=0.9, zorder=2, edgecolors='white', linewidth=0.5)

    # Correctly handle sparse or dense matrix for edges
    if scipy.sparse.issparse(W):
        rows, cols = W.nonzero()
        weights = W.data
    else:
        rows, cols = np.where(W_dense > threshold)
        weights = W_dense[rows, cols]
        
    valid_weights = weights[weights > 0]
    if len(valid_weights) > 0:
        edge_norm = plt.Normalize(vmin=valid_weights.min(), vmax=valid_weights.max())
    else:
        edge_norm = plt.Normalize(vmin=0, vmax=1) # Fallback

    for i, j, weight in zip(rows, cols, weights):
        if weight <= threshold:
             continue
        edge_color = cmap(edge_norm(weight))
        alpha = max(0.1, min(1.0, weight*2))
        linewidth = max(0.5, weight*3)
        ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]], color=edge_color, alpha=alpha, linewidth=linewidth, zorder=1)
    
    plt.title(title, fontsize=20, color='white')
    plt.axis('off')
    plt.tight_layout()
    fig = plt.gcf()
    fig.set_facecolor('black')
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"Saved network graph to '{save_path}'")

def plot_spike_raster(spike_times: list, title: str, save_path: str):
    """
    Creates and saves a spike raster plot.
    """
    plt.figure(figsize=(12, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    plt.eventplot(spike_times, colors='cyan', linelengths=0.75)
    
    plt.title(title, fontsize=20, color='white')
    plt.xlabel("Time (Global Steps)", fontsize=14, color='white')
    plt.ylabel("Computational Unit (CU) ID", fontsize=14, color='white')
    
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, facecolor='black')
    plt.close()
    print(f"Saved spike raster plot to '{save_path}'")

def create_maze_animation(maze_layout: np.ndarray, goal_pos: tuple, path: list, title: str, save_path: str):
    """
    Creates an animated GIF of the agent's path through a maze.
    This function is for specific experiments and is not part of the core FUM.
    """
    if not path:
        print("Warning: Cannot create animation for an empty path.")
        return
        
    frames = []
    for i in tqdm(range(len(path)), desc="Generating Animation Frames"):
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='black')
        ax.set_facecolor('black')
        
        ax.imshow(maze_layout, cmap='Greys', interpolation='nearest')
        
        goal_patch = plt.Rectangle((goal_pos[1] - 0.5, goal_pos[0] - 0.5), 1, 1, color='gold', alpha=0.9)
        ax.add_patch(goal_patch)

        if i > 0:
            path_arr = np.array(path[:i+1])
            ax.plot(path_arr[:, 1], path_arr[:, 0], color='cyan', linewidth=2.5, alpha=0.7)

        agent_patch = plt.Circle((path[i][1], path[i][0]), radius=0.3, color='red')
        ax.add_patch(agent_patch)

        ax.set_title(f"{title}\nStep: {i+1}/{len(path)}", fontsize=16, color='white')
        ax.set_xticks([])
        ax.set_yticks([])
        
        fig.canvas.draw()
        frame = np.array(fig.canvas.renderer.buffer_rgba())
        frames.append(frame)
        plt.close(fig)

    imageio.mimsave(save_path, frames, fps=max(10, len(path)//10))
    print(f"Saved animation to '{save_path}'")

def plot_3d_network_graph(
    W,
    t,
    title: str,
    save_path: str,
    pos: dict,
    threshold=0.0,
    edge_bins: int = 4,
    edge_style: str = "gray",          # "gray" for classic brain look, "blues" for weight-binned blues
    save_png: bool = True,             # also write a static PNG via kaleido
    camera: dict | None = None,        # optional plotly camera dict
    node_size: int = 7,
    node_opacity: float = 0.9
):
    """
    Creates an interactive 3D visual representation of the FUM's connectome using Plotly.
    Upgrades:
    - Consolidates edges into a small number of traces (binned by weight) for faster rendering.
    - Optional classic brain styling: light-blue nodes with soft gray edges.
    - Saves BOTH an interactive HTML and a high-res PNG (requires 'kaleido').
    """
    # Ensure a dense array for node metrics only; edges are drawn from original W
    if scipy.sparse.issparse(W):
        W_dense = W.toarray()
    else:
        W_dense = W

    if hasattr(W_dense, 'cpu'):
        W_dense = W_dense.cpu().numpy()

    num_nodes = W_dense.shape[0]
    if not pos:
        pos = {i: np.random.rand(3) for i in range(num_nodes)}

    # --- Nodes (colored by incoming strength) ---
    node_coords = np.array(list(pos.values()))
    # Node color encodes synaptic strength (dark=strong, light=weak)
    absW = np.abs(W_dense)
    in_strength = absW.sum(axis=0)
    out_strength = absW.sum(axis=1)
    strengths = (in_strength + out_strength).astype(float)
    vmin = float(np.min(strengths))
    vmax = float(np.max(strengths)) if np.max(strengths) > vmin else vmin + 1e-9
    node_trace = go.Scatter3d(
        x=node_coords[:, 0], y=node_coords[:, 1], z=node_coords[:, 2],
        mode='markers',
        marker=dict(
            size=int(node_size),
            color=strengths,
            colorscale='Blues',
            cmin=vmin,
            cmax=vmax,
            showscale=True,
            colorbar=dict(title='Synapse Strength'),
            opacity=float(node_opacity),
        ),
        hoverinfo='text',
        text=[f'Neuron {i}<br>Syn Strength: {strengths[i]:.2f}' for i in range(num_nodes)],
    )

    # --- Edges: build in a handful of weight bins for speed ---
    if scipy.sparse.issparse(W):
        rows, cols = W.nonzero()
        weights = np.asarray(W.data, dtype=float)
    else:
        rows, cols = np.where(W_dense > threshold)
        weights = np.asarray(W_dense[rows, cols], dtype=float)

    # Filter by threshold
    mask = weights > float(threshold)
    rows, cols, weights = rows[mask], cols[mask], weights[mask]

    edge_traces = []
    if len(weights) > 0:
        # Compute bin edges (quantiles); fall back to single-bin if all weights equal
        try:
            qs = np.linspace(0.0, 1.0, num=max(2, edge_bins + 1))
            bin_edges = np.quantile(weights, qs)
            # Ensure strictly increasing (handle degenerate distributions)
            bin_edges = np.unique(bin_edges)
        except Exception:
            bin_edges = np.array([weights.min(), weights.max()])

        # If degenerate, just one bin
        if bin_edges.size <= 1:
            bin_edges = np.array([float(weights.min()), float(weights.max() + 1e-9)])

        # Edge color palette
        if str(edge_style).lower() == "gray":
            # Classic brain style: soft gray edges with increasing opacity
            palette = [
                'rgba(170, 170, 170, 0.22)',
                'rgba(170, 170, 170, 0.30)',
                'rgba(170, 170, 170, 0.40)',
                'rgba(170, 170, 170, 0.52)',
                'rgba(170, 170, 170, 0.65)',
            ]
        else:
            # Pastel blues (light to brighter)
            palette = [
                'rgba(135, 206, 235, 0.35)',  # light skyblue
                'rgba(100, 149, 237, 0.5)',   # cornflower
                'rgba(65, 105, 225, 0.65)',   # royalblue
                'rgba(30, 144, 255, 0.8)',    # dodgerblue
                'rgba(0, 191, 255, 0.9)',     # deepskyblue
            ]

        # Build one trace per bin with None-separated line segments
        for b in range(bin_edges.size - 1):
            lo, hi = bin_edges[b], bin_edges[b + 1]
            # Include the upper edge for the last bin
            in_bin = (weights >= lo) & (weights <= hi if b == bin_edges.size - 2 else weights < hi)
            if not np.any(in_bin):
                continue
            r_b = rows[in_bin]
            c_b = cols[in_bin]

            edge_x, edge_y, edge_z = [], [], []
            for i, j in zip(r_b, c_b):
                edge_x.extend([pos[i][0], pos[j][0], None])
                edge_y.extend([pos[i][1], pos[j][1], None])
                edge_z.extend([pos[i][2], pos[j][2], None])

            color = palette[min(b, len(palette) - 1)]
            width = max(1.0, 1.0 + 0.6 * (b + 1))
            edge_traces.append(
                go.Scatter3d(
                    x=edge_x, y=edge_y, z=edge_z,
                    mode='lines',
                    line=dict(color=color, width=width),
                    hoverinfo='none',
                    showlegend=False,
                )
            )

    # --- Compose figure ---
    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, color='white')),
        showlegend=False,
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
            bgcolor='black',
        ),
        margin=dict(l=0, r=0, b=0, t=40),
        paper_bgcolor='black',
        font_color='white',
    )
    # Set a pleasant default camera if none provided
    if camera is None:
        camera = dict(eye=dict(x=1.6, y=1.6, z=0.9))
    fig.update_layout(scene_camera=camera)

    # Save as interactive HTML
    html_save_path = save_path.replace('.png', '.html')
    fig.write_html(html_save_path)
    print(f"Saved interactive 3D network graph to '{html_save_path}'")

    # Optionally save a high-res PNG using kaleido
    if save_png and save_path.lower().endswith(".png"):
        try:
            # Width/height chosen for publication-quality output
            fig.write_image(save_path, format="png", width=1920, height=1200, scale=2)
            print(f"Saved static 3D network graph PNG to '{save_path}'")
        except Exception as e:
            print(f"[WARN] Could not save PNG to '{save_path}'. Install 'kaleido' to enable static image export. Error: {e}")

def export_connectome_json(W, pos, path, threshold=0.0):
    """
    Export adjacency and node positions to a JSON schema for front-end visualization.

    - Handles scipy.sparse and dense matrices
    - Accepts pos as a dict {node_id: [x,y,(z)?]} or ndarray shape (N, D)
    - Applies a weight threshold (exclusive) to filter edges

    JSON schema (FUM.connectome.v1):
    {
      "schema": "FUM.connectome.v1",
      "directed": true,
      "num_nodes": N,
      "num_edges": M,
      "threshold": float,
      "nodes": [{ "id": int, "pos": [x,y,(z)?] }, ...],
      "edges": [{ "source": int, "target": int, "weight": float }, ...]
    }
    """
    import json
    import numpy as _np
    import scipy.sparse as _sp

    num_nodes = int(W.shape[0])

    # Build nodes with positions
    nodes = []
    if isinstance(pos, dict):
        for i in range(num_nodes):
            coords = pos.get(i)
            if coords is None:
                coords = _np.random.rand(2)
            coords = _np.asarray(coords).tolist()
            nodes.append({"id": i, "pos": coords})
    else:
        pos_arr = _np.asarray(pos)
        for i in range(num_nodes):
            coords = pos_arr[i].tolist()
            nodes.append({"id": i, "pos": coords})

    # Extract edges
    if _sp.issparse(W):
        rows, cols = W.nonzero()
        weights = W.data
    else:
        W_dense = _np.asarray(W)
        rows, cols = _np.where(W_dense > threshold)
        weights = W_dense[rows, cols]

    edges = []
    for i, j, w in zip(rows, cols, weights):
        if w <= threshold:
            continue
        edges.append({"source": int(i), "target": int(j), "weight": float(w)})

    payload = {
        "schema": "FUM.connectome.v1",
        "directed": True,
        "num_nodes": num_nodes,
        "num_edges": len(edges),
        "threshold": float(threshold),
        "nodes": nodes,
        "edges": edges,
    }

    with open(path, "w") as f:
        json.dump(payload, f)

    print(f"Saved connectome JSON to '{path}'")


def export_connectome_npz(W, path):
    """
    Persist the connectome to NPZ (CSR) for exact reconstruction later.
    """
    import scipy.sparse as _sp
    from scipy.sparse import csr_matrix as _csr

    W_csr = W if _sp.issparse(W) else _csr(W)
    _sp.save_npz(path, W_csr)
    print(f"Saved connectome NPZ to '{path}'")