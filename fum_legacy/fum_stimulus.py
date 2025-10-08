# stimulus.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import random
import numpy as np

class StimulusGenerator:
    """
    Creates a library of diverse, information-rich stimuli to guide the
    FUM's initial self-organization (Phase 1: Random Seed Sprinkling).
    
    The stimuli are abstract and non-goal-oriented, representing the
    fundamental building blocks of logic, mathematics, and structure.
    """
    def __init__(self, num_vars=5):
        self.math_vars = [chr(ord('a') + i) for i in range(num_vars)]
        self.logic_vars = [chr(ord('P') + i) for i in range(num_vars)]
        self.math_ops = ['+', '-', '*']
        self.logic_ops = ['&', '|', '^'] # AND, OR, XOR

    def generate_math_expression(self, depth=2) -> str:
        """Generates a simple, nested mathematical expression as a string."""
        if depth == 0:
            return random.choice(self.math_vars)
        
        op = random.choice(self.math_ops)
        left = self.generate_math_expression(depth - 1)
        right = self.generate_math_expression(depth - 1)
        
        return f"({left} {op} {right})"

    def generate_logic_proposition(self, depth=2) -> str:
        """Generates a simple, nested logical proposition as a string."""
        if depth == 0:
            return random.choice(self.logic_vars)
            
        op = random.choice(self.logic_ops)
        left = self.generate_logic_proposition(depth - 1)
        right = self.generate_logic_proposition(depth - 1)
        
        return f"({left} {op} {right})"

    def generate_graph_structure(self, num_nodes=8) -> np.ndarray:
        """
        Generates a simple graph structure's adjacency matrix using NumPy.
        This is a pure, high-performance function.
        """
        adj_matrix = np.zeros((num_nodes, num_nodes), dtype=np.float32)
        graph_type = random.choice(['path', 'star', 'cycle', 'complete'])
        
        if graph_type == 'path':
            for i in range(num_nodes - 1):
                adj_matrix[i, i+1] = 1
                adj_matrix[i+1, i] = 1
        elif graph_type == 'star':
            center_node = 0
            for i in range(1, num_nodes):
                adj_matrix[center_node, i] = 1
                adj_matrix[i, center_node] = 1
        elif graph_type == 'cycle':
            for i in range(num_nodes):
                adj_matrix[i, (i + 1) % num_nodes] = 1
                adj_matrix[(i + 1) % num_nodes, i] = 1
        elif graph_type == 'complete':
            adj_matrix = np.ones((num_nodes, num_nodes), dtype=np.float32)
            np.fill_diagonal(adj_matrix, 0)
            
        return adj_matrix

    def get_random_stimulus(self) -> tuple[str, any]:
        """
        Returns a random stimulus from one of the categories.
        """
        stimulus_type = random.choice(['math', 'logic', 'graph'])
        
        if stimulus_type == 'math':
            return 'math', self.generate_math_expression()
        elif stimulus_type == 'logic':
            return 'logic', self.generate_logic_proposition()
        else: # graph
            return 'graph', self.generate_graph_structure()