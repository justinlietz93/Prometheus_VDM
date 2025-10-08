# fum_structural_homeostasis.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from scipy.sparse import csc_matrix, lil_matrix

def perform_structural_homeostasis(W: csc_matrix, ccc_metrics: dict) -> csc_matrix:
    """
    Performs Structural Homeostasis on the Emergent Connectome (UKG).
    
    This is a purpose-driven, self-regulating process that uses TDA metrics
    (Cohesion and Complexity) to maintain the network's topological health,
    ensuring the FUM remains in a stable and efficient state.

    Args:
        W (csc_matrix): The current sparse weight matrix representing the UKG.
        ccc_metrics (dict): A dictionary of metrics from the CCC_Module.

    Returns:
        csc_matrix: The modified, healthier weight matrix.
    """
    num_neurons = W.shape[0]
    
    # To avoid performance warnings, all structural modifications (pruning and
    # growth) are performed on a `lil_matrix`, which is efficient for
    # changing sparsity structure.
    W_lil = W.tolil()
    
    # --- 1. Pruning (Complexity Homeostasis) ---
    pruning_threshold = 0.05
    rows_cols = W_lil.rows
    data_rows = W_lil.data
    for i in range(num_neurons):
        to_prune_indices = [
            idx for idx, weight in enumerate(data_rows[i])
            if abs(weight) < pruning_threshold
        ]
        for idx in sorted(to_prune_indices, reverse=True):
            del rows_cols[i][idx]
            del data_rows[i][idx]

    # --- 2. Growth (Cohesion Homeostasis) ---
    component_count = ccc_metrics.get('cohesion_cluster_count', 1)
    if isinstance(component_count, np.integer):
        component_count = component_count.item()

    if component_count > 1 and 'cluster_labels' in ccc_metrics:
        # A "pathological" state of low cohesion has been detected. The system
        # implements the documented strategy of "biasing plasticity towards
        # growing connections" to heal the fragmentation.
        labels = ccc_metrics['cluster_labels']
        unique_labels = np.unique(labels)
        
        # To make the healing effective, we create a "bundle" of new connections
        # to ensure the clustering algorithm recognizes the new bridge.
        BUNDLE_SIZE = 3
        
        # We'll build one bridge for each excess cluster to encourage fusion.
        num_bridges_to_build = component_count - 1

        for _ in range(num_bridges_to_build):
            # Choose two different territories to bridge
            cluster_a, cluster_b = np.random.choice(unique_labels, 2, replace=False)
            
            indices_a = np.where(labels == cluster_a)[0]
            indices_b = np.where(labels == cluster_b)[0]
            
            if len(indices_a) > 0 and len(indices_b) > 0:
                # Create a bundle of connections between the two territories
                for _ in range(BUNDLE_SIZE):
                    neuron_u = np.random.choice(indices_a)
                    neuron_v = np.random.choice(indices_b)
                    if neuron_u != neuron_v and W_lil[neuron_u, neuron_v] == 0:
                        W_lil[neuron_u, neuron_v] = np.random.uniform(0.05, 0.1)
    
    # Convert back to csc_matrix once at the end for efficient calculations
    W_csc = W_lil.tocsc()
    W_csc.prune()
    return W_csc