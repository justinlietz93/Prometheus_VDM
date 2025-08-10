# fum_data_curation.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import numpy as np
from collections import Counter
from scipy import stats # <-- NEW
import math

class DataCuration:
    """
    Analyzes a generated dataset of stimuli to ensure it meets benchmarks
    for coverage, diversity, and complexity. This validation happens before
    the dataset is presented to the FUM instance.
    """

    def _calculate_entropy(self, frequencies: dict) -> float:
        """Calculates Shannon entropy for a distribution."""
        total_items = sum(frequencies.values())
        if total_items == 0:
            return 0.0
        
        entropy = 0.0
        for count in frequencies.values():
            probability = count / total_items
            if probability > 0:
                entropy -= probability * math.log2(probability)
        return entropy

    def _analyze_string_stimulus(self, content: str):
        """Extracts operators and depth from a math/logic expression."""
        operators = Counter(char for char in content if char in ['+', '-', '*', '&', '|', '^'])
        # A simple proxy for depth is the number of opening parentheses
        depth = content.count('(')
        return operators, depth

    def _analyze_graph_stimulus(self, adj_matrix: np.ndarray):
        """Calculates density for a graph's adjacency matrix."""
        num_nodes = adj_matrix.shape[0]
        if num_nodes == 0:
            return 0.0
        num_edges = np.sum(adj_matrix) / 2 # Each edge is counted twice
        
        # For a simple graph, max edges is n*(n-1)/2
        max_edges = (num_nodes * (num_nodes - 1)) / 2
        if max_edges == 0:
            return 0.0 # Avoid division by zero for single-node graphs
            
        density = num_edges / max_edges
        return density

    def analyze_dataset(self, dataset: list[tuple[str, any]]):
        """
        Performs a full analysis of the provided list of stimuli.

        Args:
            dataset: A list of tuples, where each is (stimulus_type, stimulus_content).

        Returns:
            A dictionary of metrics.
        """
        if not dataset:
            return {"error": "Dataset is empty"}

        type_counts = Counter(item[0] for item in dataset)
        
        all_operators = Counter()
        total_depth = 0
        num_string_stimuli = 0
        
        total_density = 0.0
        num_graph_stimuli = 0

        for stim_type, content in dataset:
            if stim_type in ['math', 'logic']:
                operators, depth = self._analyze_string_stimulus(content)
                all_operators.update(operators)
                total_depth += depth
                num_string_stimuli += 1
            elif stim_type == 'graph':
                density = self._analyze_graph_stimulus(content)
                total_density += density
                num_graph_stimuli += 1

        # --- Calculate Final Metrics ---
        # Coverage & Diversity
        type_diversity = self._calculate_entropy(type_counts)
        operator_diversity = self._calculate_entropy(all_operators)
        
        # Complexity
        avg_depth = total_depth / num_string_stimuli if num_string_stimuli > 0 else 0
        avg_density = total_density / num_graph_stimuli if num_graph_stimuli > 0 else 0

        metrics = {
            "Total Stimuli": len(dataset),
            "Stimulus Type Distribution": dict(type_counts),
            "Type Diversity (Entropy)": f"{type_diversity:.4f}",
            "Operator Distribution": dict(all_operators),
            "Operator Diversity (Entropy)": f"{operator_diversity:.4f}",
            "Avg. Expression Depth": f"{avg_depth:.2f}",
            "Avg. Graph Density": f"{avg_density:.4f}",
        }
        
        # --- Bias Mitigation Checks ---
        # 1. Check for uniformity in stimulus types
        expected_type_count = len(dataset) / len(type_counts)
        type_chi2, type_p_value = stats.chisquare(f_obs=list(type_counts.values()), f_exp=[expected_type_count] * len(type_counts))
        
        # 2. Check for uniformity in operators
        expected_op_count = sum(all_operators.values()) / len(all_operators)
        op_chi2, op_p_value = stats.chisquare(f_obs=list(all_operators.values()), f_exp=[expected_op_count] * len(all_operators))

        bias_metrics = {
            "Stimulus Type Chi-Squared": f"{type_chi2:.2f}",
            "Stimulus Type p-value": f"{type_p_value:.3f}",
            "Operator Chi-Squared": f"{op_chi2:.2f}",
            "Operator p-value": f"{op_p_value:.3f}",
            "Bias Assessment": "PASS" if type_p_value > 0.05 and op_p_value > 0.05 else "FAIL"
        }
        metrics.update(bias_metrics)

        return metrics