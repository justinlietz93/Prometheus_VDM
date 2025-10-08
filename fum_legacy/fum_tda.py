# fum_tda.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from scipy.sparse import csc_matrix
from scipy.spatial.distance import pdist, squareform

# FUM Modules & External Libraries
from FUM_AdvancedMath.tda.compute_persistent_homology import compute_persistent_homology
from FUM_AdvancedMath.tda.calculate_tda_metrics import calculate_tda_metrics

class TDA_Module:
    """
    Acts as the FUM's sense of self-perception for its own internal structure.
    """
    def analyze_UKG_topology(self, W: csc_matrix) -> dict:
        """
        Performs TDA on the UKG to assess its topological health.
        """
        if W.nnz == 0:
            return {'component_count': W.shape[0], 'total_b1_persistence': 0.0}

        dense_W = W.toarray()
        
        if dense_W.shape[0] < 2:
            return {'component_count': dense_W.shape[0], 'total_b1_persistence': 0.0}
            
        # 1. Create the 1D condensed distance matrix (fast and memory-efficient).
        condensed_distances = pdist(dense_W, metric='euclidean')

        # 2. Convert 1D condensed matrix to 2D square matrix for the TDA tool.
        # This is the O(N^2) operation we only perform when "thinking" is needed.
        square_distances = squareform(condensed_distances)

        # 3. Call the TDA tool, explicitly telling it we're passing a distance matrix.
        persistence_result = compute_persistent_homology(
            square_distances, 
            max_dim=1,
            is_distance_matrix=True
        )
        
        tda_metrics = calculate_tda_metrics(persistence_result['dgms'])

        return tda_metrics