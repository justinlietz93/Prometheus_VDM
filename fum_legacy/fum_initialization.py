# fum_initialization.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from scipy.sparse import lil_matrix
from sklearn.neighbors import NearestNeighbors

def create_knn_graph(num_neurons: int, k: int, is_excitatory: np.ndarray, feature_dim: int = 16) -> lil_matrix:
    """
    Creates a k-Nearest Neighbors (k-NN) graph as a sparse matrix.
    This is a direct implementation of the subquadratic scaling principle.

    Instead of random connections, each neuron is connected only to its 'k'
    most similar neighbors, ensuring the network is both sparse and
    structurally intelligent from the start.

    Args:
        num_neurons (int): The total number of neurons in the network.
        k (int): The number of nearest neighbors to connect to.
        is_excitatory (np.ndarray): A boolean array indicating if a neuron is excitatory.
        feature_dim (int): The dimensionality of the feature space for neurons.

    Returns:
        lil_matrix: A sparse matrix representing the directed k-NN graph.
    """
    # 1. Assign a random feature vector to each neuron.
    # This represents a neuron's initial "functional preference".
    neural_features = np.random.rand(num_neurons, feature_dim)

    # 2. Use the highly optimized NearestNeighbors algorithm to find the k-NN for each neuron.
    # We add 1 to k because a neuron's closest neighbor is always itself.
    nn = NearestNeighbors(n_neighbors=k + 1, algorithm='auto').fit(neural_features)
    distances, indices = nn.kneighbors(neural_features)

    # 3. Create the sparse adjacency matrix.
    # lil_matrix is efficient for constructing sparse matrices element by element.
    W = lil_matrix((num_neurons, num_neurons), dtype=np.float32)
    
    # For each neuron, create a directed edge to its k nearest neighbors
    # (excluding itself, which is always at index 0).
    for i in range(num_neurons):
        for j in range(1, k + 1):
            neighbor_idx = indices[i, j]
            # Add a directed edge from the neuron to its neighbor
            # Set weight based on the type of the source neuron `i`
            if is_excitatory[i]:
                # Excitatory neurons have positive weights
                W[neighbor_idx, i] = np.random.uniform(0.0, 0.3)
            else:
                # Inhibitory neurons have negative weights
                W[neighbor_idx, i] = np.random.uniform(-0.3, 0.0)

    print(f"Initialized a k-NN graph with {W.nnz} synapses (k={k}).")
    return W