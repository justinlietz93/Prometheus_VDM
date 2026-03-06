"""
V8 Real-Time 3D Topology Dashboard
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

Standalone Plotly Dash app that replays v8 h5 engram data as a live
3D topology visualization — spectral embedding with φ-colored nodes,
activity glow, bond edges, and telemetry time series.

Usage:
    python -m vdm_rt.v8.dashboard [path/to/engram.h5]
"""

from __future__ import annotations

import sys
import os
import glob
import numpy as np
import h5py

from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html, Input, Output, State, callback_context, no_update

# ── Globals ──────────────────────────────────────────────────────────
DARK_BG = "#0d1117"
CARD_BG = "#161b22"
BORDER = "#30363d"
TEXT_FG = "#c9d1d9"
ACCENT = "#58a6ff"
GREEN = "#39d353"
ORANGE = "#f0883e"
RED = "#f85149"
PURPLE = "#a371f7"
CYAN = "#79c0ff"


# ── Data Loading ─────────────────────────────────────────────────────

class EngramReader:
    """Reads an h5 engram and caches spectral embeddings.
    
    Supports two H5 formats:
      Old (v8): ticks/{tick:08d}/ with full state per tick, summary from attrs
      New (v9): snapshots/{tick:08d}/ on schedule, summary/ group with arrays
    """

    def __init__(self, path: str):
        self.path = path
        self.f = h5py.File(path, "r")

        # Detect format: new has "snapshots", old has "ticks"
        if "snapshots" in self.f:
            self._data_group = "snapshots"
        elif "ticks" in self.f:
            self._data_group = "ticks"
        else:
            raise KeyError("H5 file has neither 'ticks' nor 'snapshots' group")

        self.tick_keys = sorted(self.f[self._data_group].keys())
        self.n_ticks = len(self.tick_keys)
        self.N = int(self.f["metadata"].attrs.get("N", 0))
        if self.N == 0 and self.n_ticks > 0:
            first = self.tick_keys[0]
            self.N = self.f[self._data_group][first]["phi_curr"].shape[0]

        # Cache
        self._embed_cache = {}
        self._summary = None

        # Map snapshot index → actual tick number (from key name)
        self.snapshot_ticks = np.array([int(k) for k in self.tick_keys])

    def load_summary(self):
        """Load per-tick summary arrays."""
        if self._summary is not None:
            return self._summary

        # New format: summary/ group has pre-computed arrays
        if "summary" in self.f:
            s = self.f["summary"]
            self._summary = {
                "ticks": s["tick"][:] if "tick" in s else np.arange(self.n_ticks),
                "kT": s["kT"][:] if "kT" in s else np.zeros(self.n_ticks),
                "phi_var": s["phi_var"][:] if "phi_var" in s else np.zeros(self.n_ticks),
                "mean_degree": s["mean_degree"][:] if "mean_degree" in s else np.zeros(self.n_ticks),
                "n_walkers": s["n_walkers_emitted"][:] if "n_walkers_emitted" in s else np.zeros(self.n_ticks),
                "n_active": s["n_active"][:] if "n_active" in s else np.zeros(self.n_ticks),
            }
            return self._summary

        # Old format: read from per-tick attrs
        ticks, kTs, phi_vars, mean_degrees, n_walkers_arr, n_active_arr = [], [], [], [], [], []
        for tk in self.tick_keys:
            grp = self.f[self._data_group][tk]
            attrs = grp.attrs
            ticks.append(int(attrs.get("tick", 0)))
            kTs.append(float(attrs.get("kT", 0)))
            phi_vars.append(float(attrs.get("phi_var", 0)))
            mean_degrees.append(float(attrs.get("mean_degree", 0)))
            n_walkers_arr.append(int(attrs.get("n_walkers_this_tick", 0)))
            n_active_arr.append(int(attrs.get("n_active", 0)))

        self._summary = {
            "ticks": np.array(ticks),
            "kT": np.array(kTs),
            "phi_var": np.array(phi_vars),
            "mean_degree": np.array(mean_degrees),
            "n_walkers": np.array(n_walkers_arr),
            "n_active": np.array(n_active_arr),
        }
        return self._summary

    def load_tick(self, tick_idx: int):
        """Load full data for a single tick (snapshot)."""
        tk = self.tick_keys[tick_idx]
        grp = self.f[self._data_group][tk]

        phi = grp["phi_curr"][:]
        phi_prev = grp["phi_prev"][:] if "phi_prev" in grp else phi
        N = phi.shape[0]

        row_ptr = grp["adj_csr_row_ptr"][:]
        col_idx = grp["adj_csr_col_idx"][:]
        psi_flat = grp["psi_csr_data"][:] if "psi_csr_data" in grp else np.array([])

        # Build CSR
        nnz = col_idx.shape[0]
        if nnz > 0 and psi_flat.size == nnz:
            adj_csr = csr_matrix((psi_flat, col_idx, row_ptr), shape=(N, N))
        else:
            data = np.ones(nnz, dtype=np.float32) if nnz > 0 else np.array([])
            adj_csr = csr_matrix((data, col_idx, row_ptr), shape=(N, N))

        phi_dot = phi - phi_prev
        kT = float(grp.attrs.get("kT", 1e-15))
        tick_num = int(grp.attrs.get("tick", tick_idx))

        return {
            "phi": phi,
            "phi_dot": phi_dot,
            "adj_csr": adj_csr,
            "psi_flat": psi_flat,
            "row_ptr": row_ptr,
            "col_idx": col_idx,
            "N": N,
            "kT": kT,
            "tick": tick_num,
        }

    def get_embedding(self, tick_idx: int):
        """Spectral embedding using ψ-weighted normalized Laplacian.
        
        L_norm = I - D^{-1/2} W D^{-1/2}
        W = ψ-weighted adjacency (E0 bonds have ψ≈0, contribute nothing).
        This is the v8 equivalent of v7's W[i]*W[j] > threshold filter.
        Eigenvectors 1,2,3 give x,y,z coordinates directly.
        K-means on eigenvectors for community coloring.
        """
        if tick_idx in self._embed_cache:
            return self._embed_cache[tick_idx]

        data = self.load_tick(tick_idx)
        row_ptr = data["row_ptr"]
        col_idx = data["col_idx"]
        psi_flat = data["psi_flat"]
        N = data["N"]

        # The physical graph ONLY consists of condensed bonds (ψ > threshold).
        # The E0 ring is merely the vacuum computational substrate.
        # We must explicitly remove structural edges where ψ is near 0.
        nnz = len(col_idx)
        if nnz > 0 and len(psi_flat) == nnz:
            # Mask identifying emergent physical bonds
            mask = psi_flat > 0.01
            filtered_cols = col_idx[mask]
            filtered_psi = psi_flat[mask]
            
            # Rebuild row_ptr for the filtered dataset
            new_row_ptr = np.zeros(N + 1, dtype=np.int32)
            edge_counts = np.add.reduceat(mask, row_ptr[:-1]) if len(row_ptr) > 1 else np.array([])
            if len(edge_counts) == N:
                new_row_ptr[1:] = np.cumsum(edge_counts)
                
            A = csr_matrix((filtered_psi, filtered_cols, new_row_ptr), shape=(N, N))
            # Symmetrize to ensure physical reciprocity in the embedding
            A = (A + A.T) / 2.0
        elif nnz > 0:
            ones = np.ones(nnz, dtype=np.float32)
            A = csr_matrix((ones, col_idx, row_ptr), shape=(N, N))
        else:
            A = csr_matrix((N, N), dtype=np.float32)

        degrees = np.array(A.sum(axis=1)).ravel()

        # Normalized Laplacian: L_norm = I - D^{-1/2} A D^{-1/2}
        d_inv_sqrt = np.zeros(N)
        mask = degrees > 0
        d_inv_sqrt[mask] = 1.0 / np.sqrt(degrees[mask])
        D_inv_sqrt = csr_matrix(
            (d_inv_sqrt, (np.arange(N), np.arange(N))), shape=(N, N)
        )
        L_norm = csr_matrix(np.eye(N)) - D_inv_sqrt @ A @ D_inv_sqrt

        n_components = min(7, N - 2)
        try:
            # Use 'SA' (Smallest Algebraic) instead of 'SM' (Smallest Magnitude).
            # For a normalized Laplacian, all eigenvalues should be >= 0 mathematically, 
            # but floating point error can yield small negative values.
            # 'SM' will pull large negative garbage if the matrix is slightly indefinite.
            vals, vecs = eigsh(L_norm.astype(np.float64), k=n_components, which="SA", tol=1e-5)
            # Hard floor eigenvalues to 0 to prevent downstream issues
            vals = np.maximum(vals, 0.0)
            order = np.argsort(vals)
            vals = vals[order]
            vecs = vecs[:, order]
        except Exception:
            vecs = np.random.RandomState(42).randn(N, n_components) * 0.01
            vals = np.zeros(n_components)

        # x, y, z from eigenvectors 1, 2, 3 (skip trivial ev0)
        x = vecs[:, 1] if vecs.shape[1] > 1 else np.zeros(N)
        y = vecs[:, 2] if vecs.shape[1] > 2 else np.zeros(N)
        z = vecs[:, 3] if vecs.shape[1] > 3 else np.zeros(N)

        # Community detection via k-means on eigenvectors (v7 approach)
        communities = np.zeros(N, dtype=int)
        try:
            from scipy.cluster.vq import kmeans2, whiten
            n_comm = min(8, N - 1)
            X = vecs[:, 1:n_comm+1].astype(np.float64)
            X_w = whiten(X)
            best_labels = None
            best_dist = np.inf
            for seed in range(5):
                try:
                    centroids, labels = kmeans2(X_w, n_comm, minit="++", seed=seed*42, iter=30)
                    dists = np.sum((X_w - centroids[labels])**2)
                    if dists < best_dist:
                        best_dist = dists
                        best_labels = labels
                except Exception:
                    continue
            if best_labels is not None:
                communities = best_labels
        except Exception:
            pass

        pos = np.column_stack([x, y, z])

        result = {
            "pos": pos,
            "communities": communities,
            "eigenvalues": vals,
        }
        self._embed_cache[tick_idx] = result
        return result


# ── Figure Builders ──────────────────────────────────────────────────

def build_3d_figure(reader: EngramReader, tick_idx: int):
    """Build the 3D spectral embedding figure for a given tick."""
    data = reader.load_tick(tick_idx)
    embed = reader.get_embedding(tick_idx)

    phi = data["phi"]
    phi_dot = data["phi_dot"]
    N = data["N"]
    kT = data["kT"]
    tick = data["tick"]

    # Coordinates from embedding
    pos = embed["pos"]
    x = pos[:, 0]
    y = pos[:, 1]
    z = pos[:, 2]

    communities = embed.get("communities", np.zeros(N, dtype=int))

    # Activity: |φ̇| normalized
    activity = np.abs(phi_dot)
    max_act = max(activity.max(), 1e-10)
    norm_act = activity / max_act

    # Node size: base + highly exaggerated activity glow
    sizes = 2 + 35 * (norm_act ** 1.5)

    # Community color palette (10 distinct colors)
    comm_colors = [
        "#58a6ff", "#f0883e", "#39d353", "#a371f7", "#f85149",
        "#79c0ff", "#e3b341", "#56d4dd", "#db61a2", "#7ee787",
    ]
    n_comms = int(communities.max()) + 1 if len(communities) > 0 else 1
    node_colors = [comm_colors[int(c) % len(comm_colors)] for c in communities]

    # Hover text
    hover = [
        f"Node {i}<br>φ={phi[i]:.3f}<br>|φ̇|={activity[i]:.4f}<br>Community {communities[i]}"
        for i in range(N)
    ]

    fig = go.Figure()

    # Draw edges (subsample for performance — max 2000 edges)
    row_ptr = data["row_ptr"]
    col_idx = data["col_idx"]
    psi_flat = data["psi_flat"]

    edge_x, edge_y, edge_z = [], [], []
    edge_count = 0
    max_edges = 2000

    for i in range(N):
        start = int(row_ptr[i])
        end = int(row_ptr[i + 1])
        for k in range(start, end):
            j = int(col_idx[k])
            if j <= i:
                continue  # avoid duplicate edges
            psi_val = float(psi_flat[k]) if k < len(psi_flat) else 0
            if psi_val < 0.001:
                continue  # skip near-vacuum bonds
            edge_x.extend([x[i], x[j], None])
            edge_y.extend([y[i], y[j], None])
            edge_z.extend([z[i], z[j], None])
            edge_count += 1
            if edge_count >= max_edges:
                break
        if edge_count >= max_edges:
            break

    if edge_x:
        fig.add_trace(go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode="lines",
            line=dict(color=CYAN, width=1, ),
            opacity=0.15,
            hoverinfo="skip",
            name="Bonds",
        ))

    # Draw nodes — community colored
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode="markers",
        marker=dict(
            size=sizes,
            color=node_colors,
            opacity=0.85,
            line=dict(width=0),
        ),
        text=hover,
        hoverinfo="text",
        name="Nodes",
    ))

    degrees = np.diff(row_ptr)
    mean_deg = float(degrees.mean()) if N > 0 else 0

    fig.update_layout(
        title=dict(
            text=f"t={tick}  ·  N={N}  ·  k̄={mean_deg:.1f}  ·  kT={kT:.2e}",
            font=dict(color=ACCENT, size=14),
        ),
        scene=dict(
            xaxis=dict(title="EV 2 (Fiedler)", showbackground=False,
                       color=TEXT_FG, gridcolor=BORDER),
            yaxis=dict(title="EV 3", showbackground=False,
                       color=TEXT_FG, gridcolor=BORDER),
            zaxis=dict(title="EV 4", showbackground=False,
                       color=TEXT_FG, gridcolor=BORDER),
            bgcolor=DARK_BG,
        ),
        paper_bgcolor=DARK_BG,
        plot_bgcolor=DARK_BG,
        font=dict(color=TEXT_FG),
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
        height=600,
    )

    return fig


def build_telemetry_figure(reader: EngramReader, current_tick_idx: int):
    """Build telemetry time series with cursor at current tick."""
    summary = reader.load_summary()
    ticks = summary["ticks"]

    fig = make_subplots(
        rows=3, cols=1, shared_xaxes=True,
        row_heights=[0.4, 0.3, 0.3],
        vertical_spacing=0.06,
        subplot_titles=["kT & Var(φ)", "Mean Degree", "Walkers & Active"],
    )

    # Row 1: kT and phi_var
    fig.add_trace(go.Scatter(
        x=ticks, y=summary["kT"], mode="lines",
        name="kT", line=dict(color=ORANGE, width=1.5),
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=ticks, y=summary["phi_var"], mode="lines",
        name="Var(φ)", line=dict(color=CYAN, width=1.5),
    ), row=1, col=1)

    # Row 2: mean degree
    fig.add_trace(go.Scatter(
        x=ticks, y=summary["mean_degree"], mode="lines",
        name="k̄", line=dict(color=GREEN, width=1.5),
    ), row=2, col=1)

    # Row 3: walkers and active
    fig.add_trace(go.Scatter(
        x=ticks, y=summary["n_walkers"], mode="lines",
        name="Walkers", line=dict(color=PURPLE, width=1.5),
    ), row=3, col=1)
    fig.add_trace(go.Scatter(
        x=ticks, y=summary["n_active"], mode="lines",
        name="Active", line=dict(color=RED, width=1.5),
    ), row=3, col=1)

    # Cursor line
    # Cursor line — map snapshot index to actual tick number
    if 0 <= current_tick_idx < len(reader.snapshot_ticks):
        cursor_tick = reader.snapshot_ticks[current_tick_idx]
        for row in [1, 2, 3]:
            fig.add_vline(
                x=cursor_tick, line_color=ACCENT, line_dash="dash",
                line_width=1, row=row, col=1,
            )

    fig.update_layout(
        paper_bgcolor=DARK_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT_FG, size=10),
        margin=dict(l=50, r=10, t=30, b=30),
        showlegend=True,
        legend=dict(
            orientation="h", x=0, y=1.15,
            font=dict(size=9),
        ),
        height=500,
    )

    for i in range(1, 4):
        fig.update_xaxes(gridcolor=BORDER, row=i, col=1)
        fig.update_yaxes(gridcolor=BORDER, row=i, col=1)

    fig.update_xaxes(title_text="Tick", row=3, col=1)

    return fig


# ── Dash App ─────────────────────────────────────────────────────────

def build_dashboard(h5_path: str):
    """Build and return the Dash app."""

    reader = EngramReader(h5_path)
    print(f"Loaded: {h5_path}")
    print(f"  Ticks: {reader.n_ticks}, N: {reader.N}")
    print("  Loading summaries...")
    reader.load_summary()
    print("  Ready.")

    app = Dash(__name__)
    app.title = "V8 Topology Dashboard"

    app.layout = html.Div([
        # Header
        html.Div([
            html.H2("V8 Topology Dashboard", style={
                "color": ACCENT, "margin": "0", "fontWeight": "600",
            }),
            html.Span(
                f"  {os.path.basename(h5_path)}  ·  {reader.n_ticks} ticks  ·  N={reader.N}",
                style={"color": TEXT_FG, "fontSize": "12px", "marginLeft": "16px"},
            ),
        ], style={
            "display": "flex", "alignItems": "center",
            "padding": "12px 20px", "borderBottom": f"1px solid {BORDER}",
        }),

        # Controls bar
        html.Div([
            html.Button("⏮", id="btn-start", n_clicks=0, style={
                "background": CARD_BG, "color": TEXT_FG, "border": f"1px solid {BORDER}",
                "borderRadius": "4px", "padding": "6px 12px", "cursor": "pointer",
                "fontSize": "16px",
            }),
            html.Button("◀", id="btn-prev", n_clicks=0, style={
                "background": CARD_BG, "color": TEXT_FG, "border": f"1px solid {BORDER}",
                "borderRadius": "4px", "padding": "6px 12px", "cursor": "pointer",
                "fontSize": "16px",
            }),
            html.Button("▶ Play", id="btn-play", n_clicks=0, style={
                "background": GREEN, "color": "#000", "border": "none",
                "borderRadius": "4px", "padding": "6px 16px", "cursor": "pointer",
                "fontWeight": "600", "fontSize": "13px",
            }),
            html.Button("▶", id="btn-next", n_clicks=0, style={
                "background": CARD_BG, "color": TEXT_FG, "border": f"1px solid {BORDER}",
                "borderRadius": "4px", "padding": "6px 12px", "cursor": "pointer",
                "fontSize": "16px",
            }),
            html.Button("⏭", id="btn-end", n_clicks=0, style={
                "background": CARD_BG, "color": TEXT_FG, "border": f"1px solid {BORDER}",
                "borderRadius": "4px", "padding": "6px 12px", "cursor": "pointer",
                "fontSize": "16px",
            }),

            html.Div([
                html.Label("Speed:", style={"color": TEXT_FG, "fontSize": "11px"}),
                dcc.Dropdown(
                    id="speed-select",
                    options=[
                        {"label": "100ms", "value": 100},
                        {"label": "200ms", "value": 200},
                        {"label": "500ms", "value": 500},
                        {"label": "1s", "value": 1000},
                    ],
                    value=200,
                    clearable=False,
                    style={"width": "90px", "fontSize": "12px"},
                ),
            ], style={"display": "flex", "alignItems": "center", "gap": "6px"}),

            dcc.Slider(
                id="tick-slider",
                min=0,
                max=reader.n_ticks - 1,
                step=1,
                value=0,
                marks={
                    i: str(int(reader.snapshot_ticks[i]))
                    for i in [0, reader.n_ticks - 1]
                },
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode="drag",
            ),
        ], style={
            "display": "flex", "alignItems": "center", "gap": "8px",
            "padding": "8px 20px", "borderBottom": f"1px solid {BORDER}",
            "flexWrap": "wrap",
        }),

        # Main content (2-column)
        html.Div([
            # Left: 3D topology
            html.Div([
                dcc.Graph(
                    id="graph-3d",
                    figure=build_3d_figure(reader, 0),
                    style={"height": "600px"},
                    config={"displayModeBar": True, "scrollZoom": True},
                ),
            ], style={"flex": "2", "minWidth": "500px"}),

            # Right: telemetry
            html.Div([
                dcc.Graph(
                    id="graph-telemetry",
                    figure=build_telemetry_figure(reader, 0),
                    style={"height": "500px"},
                ),
                # Tick info
                html.Div(id="tick-info", style={
                    "padding": "10px", "fontSize": "12px", "color": TEXT_FG,
                    "background": CARD_BG, "borderRadius": "6px",
                    "border": f"1px solid {BORDER}", "marginTop": "8px",
                }),
            ], style={"flex": "1", "minWidth": "350px"}),
        ], style={
            "display": "flex", "gap": "12px", "padding": "12px 20px",
            "flexWrap": "wrap",
        }),

        # Interval for auto-play
        dcc.Interval(id="play-interval", interval=200, n_intervals=0, disabled=True),

        # Stores
        dcc.Store(id="playing-state", data=False),

    ], style={
        "background": DARK_BG, "minHeight": "100vh", "fontFamily": "Inter, sans-serif",
    })

    # ── Callbacks ────────────────────────────────────────────────────

    @app.callback(
        Output("tick-slider", "value"),
        [
            Input("btn-start", "n_clicks"),
            Input("btn-prev", "n_clicks"),
            Input("btn-next", "n_clicks"),
            Input("btn-end", "n_clicks"),
            Input("play-interval", "n_intervals"),
        ],
        [State("tick-slider", "value")],
        prevent_initial_call=True,
    )
    def step_tick(n_start, n_prev, n_next, n_end, n_int, current):
        ctx = callback_context
        if not ctx.triggered:
            return no_update
        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger == "btn-start":
            return 0
        elif trigger == "btn-prev":
            return max(0, current - 1)
        elif trigger == "btn-next":
            return min(reader.n_ticks - 1, current + 1)
        elif trigger == "btn-end":
            return reader.n_ticks - 1
        elif trigger == "play-interval":
            new_val = current + 1
            if new_val >= reader.n_ticks:
                return 0  # loop
            return new_val
        return no_update

    @app.callback(
        [
            Output("play-interval", "disabled"),
            Output("btn-play", "children"),
            Output("btn-play", "style"),
        ],
        Input("btn-play", "n_clicks"),
        State("play-interval", "disabled"),
        prevent_initial_call=True,
    )
    def toggle_play(n_clicks, is_disabled):
        if is_disabled:
            style = {
                "background": RED, "color": "#fff", "border": "none",
                "borderRadius": "4px", "padding": "6px 16px", "cursor": "pointer",
                "fontWeight": "600", "fontSize": "13px",
            }
            return False, "⏸ Pause", style
        else:
            style = {
                "background": GREEN, "color": "#000", "border": "none",
                "borderRadius": "4px", "padding": "6px 16px", "cursor": "pointer",
                "fontWeight": "600", "fontSize": "13px",
            }
            return True, "▶ Play", style

    @app.callback(
        Output("play-interval", "interval"),
        Input("speed-select", "value"),
        prevent_initial_call=True,
    )
    def update_speed(speed):
        return speed

    @app.callback(
        [
            Output("graph-3d", "figure"),
            Output("graph-telemetry", "figure"),
            Output("tick-info", "children"),
        ],
        Input("tick-slider", "value"),
        prevent_initial_call=True,
    )
    def update_visuals(tick_idx):
        if tick_idx is None:
            return no_update, no_update, no_update

        tick_idx = int(tick_idx)
        fig_3d = build_3d_figure(reader, tick_idx)
        fig_telem = build_telemetry_figure(reader, tick_idx)

        data = reader.load_tick(tick_idx)
        degrees = np.diff(data["row_ptr"])
        psi = data["psi_flat"]
        nonzero_psi = psi[psi > 0] if psi.size > 0 else np.array([])

        info = html.Div([
            html.Strong(f"Tick {data['tick']}", style={"color": ACCENT}),
            html.Br(),
            f"kT = {data['kT']:.2e}",
            html.Br(),
            f"φ̄ = {float(np.mean(data['phi'])):.4f},  Var(φ) = {float(np.var(data['phi'])):.4f}",
            html.Br(),
            f"k̄ = {float(degrees.mean()):.1f},  max(k) = {int(degrees.max())}",
            html.Br(),
            f"ψ̄ = {float(nonzero_psi.mean()):.4f}" if nonzero_psi.size > 0 else "No active bonds",
            html.Br(),
            f"Active: {int(np.sum(np.abs(data['phi_dot']) > np.sqrt(2 * max(data['kT'], 1e-15))))} nodes",
        ])

        return fig_3d, fig_telem, info

    return app


# ── Entry Point ──────────────────────────────────────────────────────

def main():
    if len(sys.argv) > 1:
        h5_path = sys.argv[1]
    else:
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "v8_test_logs")
        candidates = sorted(glob.glob(os.path.join(base, "*", "run_log_gate8.h5")))
        if not candidates:
            candidates = sorted(glob.glob(os.path.join(base, "*", "*.h5")))
        if not candidates:
            print("No .h5 files found. Run verify.py first.")
            sys.exit(1)
        h5_path = candidates[-1]

    app = build_dashboard(h5_path)
    print(f"\n  Dashboard: http://127.0.0.1:8050\n")
    app.run(debug=False, port=8050)


if __name__ == "__main__":
    main()
