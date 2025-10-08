# fum_ehtp.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from scipy.sparse import csc_matrix
from scipy.sparse.csgraph import connected_components
from sklearn.cluster import SpectralClustering

# FUM Modules
from fum_tda import TDA_Module

class Introspection_Probe_Module:
    """
    Implements the Introspection Probe (aka EHTP).

    This is the FUM's primary method of introspection, providing a scalable
    way to analyze the health of the Emergent Connectome (UKG).

    A Note on Subquadratic Scaling:
    A core principle of the FUM is that no operation should scale quadratically
    with the total number of neurons (N). While this module may perform dense
    O(M^2) analysis (where M is a small, constant locus size), this is a
    controlled exception. The overall complexity remains subquadratic because M
    does not scale with N, ensuring performance at massive scales.
    """
    def __init__(self):
        self.tda = TDA_Module()

    def perform_introspection_probe_analysis(self, W: csc_matrix) -> dict:
        """
        Performs a hierarchical analysis of the UKG's structure.
        
        1. Checks for basic fragmentation using `connected_components`.
        2. If the graph is cohesive, proceeds to more complex analysis like
           TDA and functional clustering.
        """
        num_neurons = W.shape[0]
        if num_neurons < 2:
            return {'cohesion_cluster_count': 1, 'cluster_labels': np.array([0])}

        # --- Step 1: Fragmentation Check (The True Cohesion Score) ---
        # Use the correct, efficient tool to find the number of disconnected
        # components in the graph. This is our true measure of fragmentation.
        n_components, labels = connected_components(
            csgraph=W, directed=False, return_labels=True
        )
        
        metrics = {
            'cohesion_cluster_count': n_components,
            'cluster_labels': labels
        }

        # --- Step 2: Advanced Analysis (Only if the graph is healthy) ---
        # Only proceed to expensive calculations if the graph is not fragmented.
        if n_components == 1:
            # --- 2a: TDA for Cycle Complexity ---
            # Now that we know the graph is unified, we can analyze its
            # internal complexity (e.g., redundant loops).
            tda_metrics = self.tda.analyze_UKG_topology(W)
            metrics.update(tda_metrics)

            # --- 2b: Functional Clustering (Future-proofing) ---
            # This is where we would analyze the *communities* within the
            # single, healthy component. Placeholder for now.
            # metrics['functional_territories'] = self._find_functional_territories(W)
            
        return metrics