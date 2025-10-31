"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a proprietary license. Use requires written
permission from Justin K. Lietz. See LICENSE file for full terms.

Knowledge Graph Generation - Knowledge Graph TDA Validation
"""


import numpy as np
import scipy.sparse as sp
import networkx as nx
import os
import pickle
import time
from datetime import datetime

# Configuration
NUM_SNAPSHOTS = 10
NUM_NEURONS = 100  # Use a smaller size for faster testing
SNAPSHOT_DIR = "data/kg_snapshots/"
SPARSITY = 0.05  # 5% connectivity (sparse)
WEIGHT_RANGE = (-1.0, 1.0)

# Create directory if it doesn't exist
os.makedirs(SNAPSHOT_DIR, exist_ok=True)


def generate_random_graph(n, sparsity, weight_range, fragmentation=0):
    """
    Generate a random graph with sparse weights.
    Fragmentation controls how disconnected the graph is (0 = fully connected, 1 = maximally fragmented)
    """
    # Create a random sparse matrix
    nnz = int(n * n * sparsity)  # Number of non-zero elements
    rows = np.random.randint(0, n, nnz)
    cols = np.random.randint(0, n, nnz)
    weights = np.random.uniform(weight_range[0], weight_range[1], nnz)
    
    # Create sparse matrix
    w_ij = sp.csr_matrix((weights, (rows, cols)), shape=(n, n))
    
    # If fragmentation is requested, split into components
    if fragmentation > 0:
        # Convert to networkx graph for easier manipulation
        G = nx.from_scipy_sparse_array(abs(w_ij))
        
        # Calculate how many components to create based on fragmentation level
        # Higher fragmentation = more components
        num_components = max(2, int(n * fragmentation * 0.1))  # At most 10% of nodes as components
        
        # Create isolated components by removing edges
        if len(G.edges) > 0 and num_components > 1:
            # Get largest connected component
            largest_cc = max(nx.connected_components(G), key=len)
            G_largest = G.subgraph(largest_cc).copy()
            
            # We'll make smaller components by splitting the largest one
            # Calculate how many nodes per component
            nodes_per_component = len(largest_cc) // num_components
            
            # For each component, select and isolate nodes
            for i in range(1, num_components):
                # Select random nodes from largest component
                if len(G_largest.nodes) >= nodes_per_component:
                    nodes_to_isolate = list(G_largest.nodes)[:nodes_per_component]
                    
                    # Remove all edges between these nodes and the rest
                    for u in nodes_to_isolate:
                        neighbors = list(G_largest.neighbors(u))
                        for v in neighbors:
                            if v not in nodes_to_isolate:
                                G.remove_edge(u, v)
                
                    # Update largest component
                    G_largest.remove_nodes_from(nodes_to_isolate)
            
            # Convert back to sparse matrix
            w_ij = nx.to_scipy_sparse_array(G)
            
            # Restore original weights (sign and magnitude)
            orig_rows, orig_cols = w_ij.nonzero()
            if len(orig_rows) > 0:
                new_weights = np.random.uniform(weight_range[0], weight_range[1], len(orig_rows))
                w_ij = sp.csr_matrix((new_weights, (orig_rows, orig_cols)), shape=(n, n))
    
    return w_ij


def generate_small_world_graph(n, k, p, weight_range, fragmentation=0):
    """
    Generate a small-world graph with the Watts-Strogatz model.
    Fragmentation controls how disconnected the graph is.
    """
    G = nx.watts_strogatz_graph(n, k, p)
    
    # Apply fragmentation if requested
    if fragmentation > 0:
        # Calculate number of components to create
        num_components = max(2, int(n * fragmentation * 0.1))
        
        # Create isolated components by removing edges
        if len(G.edges) > 0 and num_components > 1:
            # Get nodes
            nodes = list(G.nodes)
            
            # Calculate nodes per component
            nodes_per_component = n // num_components
            
            # For each component, isolate nodes
            for i in range(1, num_components):
                start_idx = i * nodes_per_component
                end_idx = min((i + 1) * nodes_per_component, n)
                component_nodes = nodes[start_idx:end_idx]
                
                # Remove edges between this component and others
                for u in component_nodes:
                    neighbors = list(G.neighbors(u))
                    for v in neighbors:
                        if v not in component_nodes:
                            G.remove_edge(u, v)
    
    # Convert to sparse matrix and assign random weights
    adj = nx.adjacency_matrix(G)
    rows, cols = adj.nonzero()
    
    if len(rows) > 0:
        weights = np.random.uniform(weight_range[0], weight_range[1], len(rows))
        w_ij = sp.csr_matrix((weights, (rows, cols)), shape=(n, n))
    else:
        w_ij = sp.csr_matrix((n, n))
    
    return w_ij


def generate_scale_free_graph(n, weight_range, fragmentation=0):
    """
    Generate a scale-free (preferential attachment) graph.
    Fragmentation controls how disconnected the graph is.
    """
    # Need at least m=1 edge per new node for Barabasi-Albert
    G = nx.barabasi_albert_graph(n, m=1)
    
    # Apply fragmentation if requested
    if fragmentation > 0:
        # Calculate number of components to create
        num_components = max(2, int(n * fragmentation * 0.1))
        
        # Create isolated components by removing edges
        if len(G.edges) > 0 and num_components > 1:
            # Remove strategic edges to create components
            # Start with the highest degree nodes as they're most connected
            degrees = dict(G.degree())
            nodes_sorted = sorted(degrees.keys(), key=lambda x: degrees[x], reverse=True)
            
            # We'll remove edges connecting to highest degree nodes
            for i in range(min(num_components-1, len(nodes_sorted)//2)):
                node = nodes_sorted[i]
                # Remove about half the edges
                neighbors = list(G.neighbors(node))
                edges_to_remove = neighbors[:len(neighbors)//2]
                for neighbor in edges_to_remove:
                    if G.has_edge(node, neighbor):
                        G.remove_edge(node, neighbor)
    
    # Convert to sparse matrix and assign random weights
    adj = nx.adjacency_matrix(G)
    rows, cols = adj.nonzero()
    
    if len(rows) > 0:
        weights = np.random.uniform(weight_range[0], weight_range[1], len(rows))
        w_ij = sp.csr_matrix((weights, (rows, cols)), shape=(n, n))
    else:
        w_ij = sp.csr_matrix((n, n))
    
    return w_ij


def calculate_efficiency_score(w_ij):
    """
    Calculate an efficiency score for the graph.
    For our simulation, efficiency will be inversely related to cycle structure:
    - More cycles → Lower efficiency (higher processing overhead)
    """
    # Convert to undirected graph for cycle analysis
    abs_weights = np.abs(w_ij.data) if w_ij.nnz > 0 else []
    threshold = 0.1
    mask = abs_weights >= threshold if len(abs_weights) > 0 else []
    
    if len(mask) == 0 or np.sum(mask) == 0:
        return 0.8  # Default for empty graph
        
    rows, cols = w_ij.nonzero()
    filtered_rows = rows[mask] if len(mask) > 0 else []
    filtered_cols = cols[mask] if len(mask) > 0 else []
    
    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(w_ij.shape[0]))
    edges = zip(filtered_rows, filtered_cols)
    G.add_edges_from(edges)
    
    # Get largest connected component if graph is disconnected
    if not nx.is_connected(G):
        connected_components = list(nx.connected_components(G))
        if connected_components:
            largest_cc = max(connected_components, key=len)
            G = G.subgraph(largest_cc).copy()
    
    # Estimate number of cycles using graph measures
    # More edges relative to nodes indicates more cycles
    n = G.number_of_nodes()
    m = G.number_of_edges()
    
    if n <= 1:
        return 0.8  # Default for tiny graph
    
    # Calculate efficiency: inverse of cycle density estimate
    # The closer to a tree (minimal cycles), the higher the efficiency
    cycle_density = (m - (n - 1)) / (n * (n - 1) / 2) if n > 1 else 0
    efficiency = 1.0 - cycle_density
    
    # Scale to [0.2, 0.9] range
    return 0.2 + 0.7 * efficiency


def calculate_pathology_score(w_ij):
    """
    Calculate a pathology score for the graph.
    For our simulation, pathology will be related to disconnectedness:
    - More separate components → Higher pathology (fragmentation)
    """
    # Convert to undirected graph for component analysis
    if w_ij.nnz == 0:
        return 0.7  # Default for empty graph
        
    abs_weights = np.abs(w_ij.data)
    threshold = 0.1
    mask = abs_weights >= threshold
    
    if np.sum(mask) == 0:
        return 0.7  # Default for effectively empty graph
        
    rows, cols = w_ij.nonzero()
    filtered_rows = rows[mask]
    filtered_cols = cols[mask]
    
    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(w_ij.shape[0]))
    edges = zip(filtered_rows, filtered_cols)
    G.add_edges_from(edges)
    
    # Count connected components
    num_components = nx.number_connected_components(G)
    
    # Calculate pathology: related to component count
    # More components = higher pathology
    pathology = min(0.9, (num_components / w_ij.shape[0]) * 5)
    
    # Scale to [0.1, 0.9] range
    return max(0.1, pathology)


def generate_snapshots():
    """Generate a series of KG snapshots with varying characteristics."""
    print(f"Generating {NUM_SNAPSHOTS} KG snapshots...")
    start_time = time.time()
    
    for i in range(NUM_SNAPSHOTS):
        # Generate a graph with varying properties
        graph_type = i % 3  # Alternate between graph types
        n = NUM_NEURONS
        
        # Introduce fragmentation in the second half of snapshots
        # This increases pathology scores by creating disconnected components
        fragmentation = 0 if i < NUM_SNAPSHOTS // 2 else ((i - NUM_SNAPSHOTS // 2) / (NUM_SNAPSHOTS // 2)) * 0.5
        
        if graph_type == 0:
            # Random graph with varying sparsity
            sparsity = SPARSITY * (1 + 0.5 * np.sin(i * 0.8))
            w_ij = generate_random_graph(n, sparsity, WEIGHT_RANGE, fragmentation)
            graph_name = "random"
            
        elif graph_type == 1:
            # Small-world graph with varying rewiring probability
            k = 4  # Each node connects to k nearest neighbors
            p = 0.1 * (1 + np.sin(i * 0.5))  # Rewiring probability varies
            w_ij = generate_small_world_graph(n, k, p, WEIGHT_RANGE, fragmentation)
            graph_name = "small_world"
            
        else:  # graph_type == 2
            # Scale-free graph
            w_ij = generate_scale_free_graph(n, WEIGHT_RANGE, fragmentation)
            graph_name = "scale_free"
        
        # Calculate metrics
        efficiency_score = calculate_efficiency_score(w_ij)
        pathology_score = calculate_pathology_score(w_ij)
        
        # Create snapshot data
        snapshot_data = {
            'w_ij': w_ij,
            'efficiency_score': efficiency_score,
            'pathology_score': pathology_score,
            'timestamp': datetime.now().timestamp(),
            'graph_type': graph_name,
            'neurons': n,
            'fragmentation': fragmentation
        }
        
        # Save snapshot
        filename = f"snapshot_{i:02d}.pkl"
        filepath = os.path.join(SNAPSHOT_DIR, filename)
        with open(filepath, 'wb') as f:
            pickle.dump(snapshot_data, f)
        
        print(f"Generated snapshot {i+1}/{NUM_SNAPSHOTS}: {graph_name}, efficiency={efficiency_score:.4f}, pathology={pathology_score:.4f}, fragmentation={fragmentation:.2f}")
    
    elapsed_time = time.time() - start_time
    print(f"Snapshot generation completed in {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    generate_snapshots()
    print(f"KG snapshots saved to {SNAPSHOT_DIR}")
