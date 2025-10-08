# visualizer.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import imageio
from tqdm import tqdm
from scipy.sparse import csc_matrix

def plot_network_graph(W: csc_matrix, title: str, save_path: str):
    """
    Creates a visual representation of the network's UKG from a sparse matrix.
    
    NOTE: This is now the ONLY place in the entire FUM pipeline where we use
    the slow networkx conversion, and it is only for the final visualization.
    """
    plt.figure(figsize=(12, 12))
    
    # --- FIX: Updated to use the modern, correct function name ---
    graph = nx.from_scipy_sparse_array(W, create_using=nx.DiGraph)

    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx_nodes(graph, pos, node_color='skyblue', node_size=150, alpha=0.8)
    
    edges = graph.edges()
    weights = [graph[u][v].get('weight', 0.1) * 5 for u, v in edges]
    
    nx.draw_networkx_edges(graph, pos, edgelist=edges, width=weights, edge_color='gray', alpha=0.6)
    
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
    # This function is not used in the Phase 1 script, but we keep it for future experiments.
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