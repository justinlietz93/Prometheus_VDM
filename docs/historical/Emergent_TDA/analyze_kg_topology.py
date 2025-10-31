"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a proprietary license. Use requires written
permission from Justin K. Lietz. See LICENSE file for full terms.

Knowledge Graph Topology Analysis - Knowledge Graph TDA Validation
"""

import numpy as np
import scipy.sparse as sp
from scipy.stats import pearsonr
from ripser import ripser
import networkx as nx # Using networkx for shortest paths initially
import time
import glob
import os
import pickle # Assuming snapshots might be pickled dicts

# --- Configuration ---
# Threshold for edge weights to consider for graph construction
WEIGHT_THRESHOLD = 0.1
# Maximum dimension for homology calculation
MAX_DIM_HOMOLOGY = 2
# Directory containing snapshot files
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "../data/kg_snapshots/")
# File pattern for snapshots
SNAPSHOT_PATTERN = "snapshot_*.pkl" # Placeholder

# --- Helper Functions ---

def load_snapshot(filepath):
    """Loads KG snapshot data from a file."""
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        # Expected keys: 'w_ij' (sparse matrix), 'efficiency_score', 'pathology_score', 'timestamp'
        if not all(k in data for k in ['w_ij', 'efficiency_score', 'pathology_score']):
            print(f"Warning: Snapshot {filepath} missing required keys.")
            return None
        return data
    except Exception as e:
        print(f"Error loading snapshot {filepath}: {e}")
        return None

def create_graph(w_ij, threshold):
    """Creates a NetworkX graph from a sparse weight matrix, thresholded."""
    if not sp.issparse(w_ij):
        w_ij = sp.csr_matrix(w_ij)

    # Apply threshold and ensure symmetry for undirected graph
    w_abs = np.abs(w_ij.data)
    mask = w_abs >= threshold
    rows, cols = w_ij.nonzero()
    filtered_rows = rows[mask]
    filtered_cols = cols[mask]

    # Create undirected graph using NetworkX
    # Note: Using NetworkX for shortest paths, might be slow for large graphs
    G = nx.Graph()
    num_neurons = w_ij.shape[0]
    G.add_nodes_from(range(num_neurons))
    edges = zip(filtered_rows, filtered_cols)
    G.add_edges_from(edges)

    # Keep only the largest connected component for simplicity?
    # Or compute distance matrix on the full graph?
    # For now, use the full graph, but note this assumption.
    # If graph is disconnected, ripser might behave unexpectedly or require handling.
    if G.number_of_nodes() > 0 and not nx.is_connected(G):
         print("Warning: Graph is disconnected. Using the largest connected component.")
         largest_cc_nodes = max(nx.connected_components(G), key=len)
         G = G.subgraph(largest_cc_nodes).copy() # Create a copy to avoid modifying the original graph view


    return G

def compute_distance_matrix(graph):
    """Computes the all-pairs shortest path distance matrix."""
    # This is computationally expensive O(N*(N+E)) or worse.
    # Consider alternatives for large graphs (e.g., landmark MDS, approx_shortest_path)
    # or libraries that compute homology directly on graphs.
    start_time = time.time()
    num_nodes = graph.number_of_nodes()
    if num_nodes == 0:
        print("Graph has no nodes, cannot compute distance matrix.")
        return None
    print(f"Computing distance matrix for {num_nodes} nodes...")
    # Use floyd_warshall_numpy for dense matrix output expected by ripser
    # Note: Requires significant memory O(N^2)
    try:
        # Ensure nodes are integers starting from 0 for matrix indexing
        node_list = sorted(list(graph.nodes()))
        mapping = {node: i for i, node in enumerate(node_list)}
        graph_relabeled = nx.relabel_nodes(graph, mapping) # Use the mapping
        # Use nodelist parameter to ensure matrix order matches node_list
        dist_matrix = nx.floyd_warshall_numpy(graph_relabeled, nodelist=sorted(graph_relabeled.nodes()))
        # Handle infinite distances (disconnected components, though we try to use largest CC)
        # Replace inf with a value larger than the max finite distance
        if np.any(np.isinf(dist_matrix)):
            finite_distances = dist_matrix[np.isfinite(dist_matrix)]
            if len(finite_distances) > 0:
                 inf_val = np.max(finite_distances) + 1
            else: # Graph was completely disconnected originally, or only one node
                 inf_val = 1 # Assign a default distance if no finite paths exist
            dist_matrix[np.isinf(dist_matrix)] = inf_val


        print(f"Distance matrix computed in {time.time() - start_time:.2f}s")
        return dist_matrix
    except Exception as e:
        # Catch potential memory errors or other issues
        print(f"Error computing distance matrix: {e}")
        return None


def compute_persistence(dist_matrix, maxdim):
    """Computes persistent homology using ripser."""
    if dist_matrix is None:
        return None
    start_time = time.time()
    print(f"Computing persistence (maxdim={maxdim})...")
    try:
        # Use distance_matrix=True
        # Add coeff=2 if prime field coefficients are needed (usually not for basic persistence)
        result = ripser(dist_matrix, maxdim=maxdim, distance_matrix=True)
        diagrams = result['dgms']
        print(f"Persistence computed in {time.time() - start_time:.2f}s")
        return diagrams
    except Exception as e:
        print(f"Error computing persistence: {e}")
        return None

def calculate_m1(pd1):
    """Calculates Total B1 Persistence (Sum of lifetimes for 1-cycles)."""
    if pd1 is None or len(pd1) == 0:
        return 0.0
    # Handle infinite persistence - replace inf with a large value?
    # Ripser typically returns max filtration value used if finite.
    # If ripser can return inf, need to handle it. Let's assume finite for now.
    persistence = pd1[:, 1] - pd1[:, 0]
    # Ensure no negative persistence due to potential floating point issues
    persistence = np.maximum(persistence, 0)
    return np.sum(persistence)

def calculate_m2(pd0):
    """Calculates Persistent B0 Count (Number of components never merging)."""
    if pd0 is None or len(pd0) == 0:
        return 0
    # In ripser, infinite death time indicates component never merges.
    # Check for np.inf. Ripser might cap infinite values at max filtration radius.
    # Let's assume np.inf is possible or check library docs.
    # If ripser caps at max radius, this definition needs refinement.
    # For now, assume np.inf is the indicator.
    infinite_count = np.sum(np.isinf(pd0[:, 1]))
    # If only one component exists and persists infinitely (common), count is 1.
    return infinite_count

def calculate_component_count(w_ij, threshold=0.1):
    """
    Calculate the number of connected components in the original graph 
    before extracting largest connected component.
    This gives a better measure of fragmentation for pathology correlation.
    """
    if w_ij.nnz == 0:
        return 1  # Default for empty graph
        
    # Apply threshold to weights
    abs_weights = np.abs(w_ij.data)
    mask = abs_weights >= threshold
    
    if np.sum(mask) == 0:
        return 1  # Default for effectively empty graph
        
    rows, cols = w_ij.nonzero()
    filtered_rows = rows[mask]
    filtered_cols = cols[mask]
    
    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(w_ij.shape[0]))  # Ensure all nodes are added
    edges = zip(filtered_rows, filtered_cols)
    G.add_edges_from(edges)
    
    # Count connected components
    return nx.number_connected_components(G)

# --- Main Analysis ---

def run_analysis(snapshot_dir, pattern, weight_threshold, maxdim):
    """Loads snapshots, computes TDA metrics, and performs correlation analysis."""
    snapshot_files = sorted(glob.glob(os.path.join(snapshot_dir, pattern)))
    print(f"Found {len(snapshot_files)} snapshot files.")

    if not snapshot_files:
        print(f"No snapshot files found matching pattern {repr(pattern)} in directory {repr(snapshot_dir)}")
        return None, None # Indicate no analysis performed

    results = []
    computation_times = {'load': [], 'graph': [], 'distance': [], 'persistence': [], 'metrics': []}

    for i, fpath in enumerate(snapshot_files):
        # Convert absolute path to relative for GitHub compatibility
        relative_path = os.path.relpath(fpath)
        print(f"\nProcessing snapshot {i+1}/{len(snapshot_files)}: {relative_path}")

        # 1. Load Data
        start_load = time.time()
        snapshot_data = load_snapshot(fpath)
        computation_times['load'].append(time.time() - start_load)
        if snapshot_data is None:
            continue
        w_ij = snapshot_data['w_ij']
        efficiency = snapshot_data['efficiency_score']
        pathology = snapshot_data['pathology_score']
        timestamp = snapshot_data.get('timestamp', i) # Use index if no timestamp


        # 2. Create Graph
        start_graph = time.time()
        graph = create_graph(w_ij, weight_threshold)
        computation_times['graph'].append(time.time() - start_graph)
        if graph is None or graph.number_of_nodes() == 0:
            print("Skipping snapshot due to empty or invalid graph.")
            continue
        num_nodes_processed = graph.number_of_nodes() # Nodes after taking largest CC if disconnected
        num_edges_processed = graph.number_of_edges()
        print(f"Graph created/processed: {num_nodes_processed} nodes, {num_edges_processed} edges")


        # 3. Compute Distance Matrix (Bottleneck)
        start_dist = time.time()
        dist_matrix = compute_distance_matrix(graph)
        comp_time_dist = time.time() - start_dist
        computation_times['distance'].append(comp_time_dist)
        if dist_matrix is None:
             print(f"Skipping snapshot due to distance matrix error (Time: {comp_time_dist:.2f}s).")
             continue

        # 4. Compute Persistence
        start_pers = time.time()
        diagrams = compute_persistence(dist_matrix, maxdim)
        comp_time_pers = time.time() - start_pers
        computation_times['persistence'].append(comp_time_pers)
        if diagrams is None:
            print(f"Skipping snapshot due to persistence computation error (Time: {comp_time_pers:.2f}s).")
            continue

        # 5. Calculate Metrics
        start_metrics = time.time()
        # Ensure diagrams list has expected length based on maxdim
        pd0 = diagrams[0] if len(diagrams) > 0 else np.empty((0, 2))
        pd1 = diagrams[1] if len(diagrams) > 1 else np.empty((0, 2))
        # pd2 = diagrams[2] if maxdim >= 2 and len(diagrams) > 2 else np.empty((0, 2)) # If needed later

        m1 = calculate_m1(pd1)
        m2 = calculate_m2(pd0)
        
        # Calculate component count from original matrix (before largest CC extraction)
        component_count = calculate_component_count(w_ij, threshold=weight_threshold)
        
        computation_times['metrics'].append(time.time() - start_metrics)

        results.append({
            'timestamp': timestamp,
            'm1_total_b1_persistence': m1,
            'm2_persistent_b0_count': m2,
            'component_count': component_count,
            'efficiency_score': efficiency,
            'pathology_score': pathology,
            'nodes': num_nodes_processed,
            'edges': num_edges_processed,
            'time_distance_matrix': comp_time_dist,
            'time_persistence': comp_time_pers,
        })
        print(f"Metrics: M1={m1:.2f}, M2={m2}, Components={component_count}")

    if not results:
        print("No results generated. Cannot perform correlation analysis.")
        return None, None # Indicate no analysis performed

    # --- Correlation Analysis ---
    m1_values = np.array([r['m1_total_b1_persistence'] for r in results])
    m2_values = np.array([r['m2_persistent_b0_count'] for r in results])
    component_values = np.array([r['component_count'] for r in results])
    efficiency_values = np.array([r['efficiency_score'] for r in results])
    pathology_values = np.array([r['pathology_score'] for r in results])

    analysis_summary = {}

    print("\n--- Correlation Results ---")

    if len(m1_values) > 1 and len(efficiency_values) > 1 and np.std(m1_values) > 0 and np.std(efficiency_values) > 0:
        try:
            corr_m1_eff, p_m1_eff = pearsonr(m1_values, efficiency_values)
            print(f"Correlation(M1_TotalB1Persistence, EfficiencyScore): r={corr_m1_eff:.4f}, p={p_m1_eff:.4g}")
            analysis_summary['corr_m1_eff'] = {'r': corr_m1_eff, 'p': p_m1_eff}
        except ValueError as e:
            print(f"Could not calculate M1 vs Efficiency correlation: {e}")
            analysis_summary['corr_m1_eff'] = {'r': np.nan, 'p': np.nan}
    else:
        print("Not enough valid data points or zero variance to calculate M1 vs Efficiency correlation.")
        analysis_summary['corr_m1_eff'] = {'r': np.nan, 'p': np.nan}


    if len(m2_values) > 1 and len(pathology_values) > 1 and np.std(m2_values) > 0 and np.std(pathology_values) > 0:
         try:
            corr_m2_path, p_m2_path = pearsonr(m2_values, pathology_values)
            print(f"Correlation(M2_PersistentB0Count, PathologyScore): r={corr_m2_path:.4f}, p={p_m2_path:.4g}")
            analysis_summary['corr_m2_path'] = {'r': corr_m2_path, 'p': p_m2_path}
         except ValueError as e:
            print(f"Could not calculate M2 vs Pathology correlation: {e}")
            analysis_summary['corr_m2_path'] = {'r': np.nan, 'p': np.nan}
    else:
        print("Not enough valid data points or zero variance to calculate M2 vs Pathology correlation.")
        analysis_summary['corr_m2_path'] = {'r': np.nan, 'p': np.nan}
        
    # Calculate correlation between component count and pathology score
    if len(component_values) > 1 and len(pathology_values) > 1 and np.std(component_values) > 0 and np.std(pathology_values) > 0:
         try:
            corr_comp_path, p_comp_path = pearsonr(component_values, pathology_values)
            print(f"Correlation(ComponentCount, PathologyScore): r={corr_comp_path:.4f}, p={p_comp_path:.4g}")
            analysis_summary['corr_comp_path'] = {'r': corr_comp_path, 'p': p_comp_path}
         except ValueError as e:
            print(f"Could not calculate ComponentCount vs Pathology correlation: {e}")
            analysis_summary['corr_comp_path'] = {'r': np.nan, 'p': np.nan}
    else:
        print("Not enough valid data points or zero variance to calculate ComponentCount vs Pathology correlation.")
        analysis_summary['corr_comp_path'] = {'r': np.nan, 'p': np.nan}
        
    # Calculate correlation between component count and pathology score
    if len(component_values) > 1 and len(pathology_values) > 1 and np.std(component_values) > 0 and np.std(pathology_values) > 0:
         try:
            corr_comp_path, p_comp_path = pearsonr(component_values, pathology_values)
            print(f"Correlation(ComponentCount, PathologyScore): r={corr_comp_path:.4f}, p={p_comp_path:.4g}")
            analysis_summary['corr_comp_path'] = {'r': corr_comp_path, 'p': p_comp_path}
         except ValueError as e:
            print(f"Could not calculate ComponentCount vs Pathology correlation: {e}")
            analysis_summary['corr_comp_path'] = {'r': np.nan, 'p': np.nan}
    else:
        print("Not enough valid data points or zero variance to calculate ComponentCount vs Pathology correlation.")
        analysis_summary['corr_comp_path'] = {'r': np.nan, 'p': np.nan}


    print("\n--- Computation Time Summary (average seconds) ---")
    avg_times = {}
    for key, times in computation_times.items():
        if times:
            avg_time = np.mean(times)
            print(f"{key}: {avg_time:.4f}")
            avg_times[f"avg_time_{key}"] = avg_time
    analysis_summary['avg_times'] = avg_times


    # TODO: Save detailed results (results list) and analysis_summary
    # Example:
    # with open('tda_analysis_results.pkl', 'wb') as f:
    #     pickle.dump({'results': results, 'summary': analysis_summary}, f)

    return results, analysis_summary

if __name__ == "__main__":
    # Example usage:
    # Assumes snapshot files exist in SNAPSHOT_DIR
    # Need to create dummy data or point to real data for execution
    print(f"Starting TDA analysis on snapshots in {repr(SNAPSHOT_DIR)}...")
    results_data, summary_data = run_analysis(
        snapshot_dir=SNAPSHOT_DIR,
        pattern=SNAPSHOT_PATTERN,
        weight_threshold=WEIGHT_THRESHOLD,
        maxdim=MAX_DIM_HOMOLOGY
    )
    if summary_data:
        print("\nAnalysis Summary:")
        print(summary_data)
    else:
        print("\nAnalysis could not be completed.")
