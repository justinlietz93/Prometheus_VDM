# fum_analysis.py
"""
Copyright © 2025 Justin K. Lietz, Neuroca, Inc. All Rights Reserved.

This research is protected under a dual-license to foster open academic
research while ensuring commercial applications are aligned with the project's ethical principles. Commercial use requires written permission from Justin K. Lietz. 
See LICENSE file for full terms.
"""
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.sparse import csc_matrix
import networkx as nx

# FUM Modules
from fum_ehtp import Introspection_Probe_Module #<-- Using the official EHTP module

class FUM_Analysis:
    """
    The FUM's definitive control panel for analysis and visualization.
    """
    def __init__(self, results_dir: str, run_id: str):
        self.results_dir = results_dir
        self.run_id = run_id
        self.ehtp = Introspection_Probe_Module()
        self.episode_data = []

    def record_episode_data(self, episode_num, W, introspection_probe_metrics):
        """Records the key metrics at the end of an episode."""
        self.episode_data.append({
            'episode_num': episode_num,
            'sparsity': W.nnz,
            'avg_weight': np.mean(W.data) if W.nnz > 0 else 0,
            'introspection_probe_metrics': introspection_probe_metrics
        })

    def analyze_UKG(self, W: csc_matrix) -> dict:
        """
        Runs the full EHTP analysis on the UKG.
        """
        return self.ehtp.perform_introspection_probe_analysis(W)

    def create_dashboard(self):
        """
        Generates the final, multi-panel dashboard visualizing the run.
        """
        if not self.episode_data: return

        fig, axs = plt.subplots(2, 2, figsize=(20, 15))
        fig.suptitle(f'FUM Performance Dashboard - Run: {self.run_id}', fontsize=24, weight='bold')
        plt.style.use('dark_background')

        episodes = [e['episode_num'] for e in self.episode_data]

        # Panel 1: Sparsity
        ax1 = axs[0, 0]
        sparsity = [e['sparsity'] for e in self.episode_data]
        ax1.plot(episodes, sparsity, 'o-', color='lime', label='Active Synapses')
        ax1.set_title('UKG Sparsity Over Time', fontsize=16)
        ax1.set_xlabel('Stimulus Block', fontsize=12)
        ax1.set_ylabel('Number of Synapses', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.2)

        # Panel 2: Average Weight
        ax2 = axs[0, 1]
        avg_weight = [e['avg_weight'] for e in self.episode_data]
        ax2.plot(episodes, avg_weight, 'o-', color='orange', label='Average Weight')
        ax2.set_title('Average Synaptic Weight Over Time', fontsize=16)
        ax2.set_xlabel('Stimulus Block', fontsize=12)
        ax2.set_ylabel('Average Weight', fontsize=12)
        ax2.legend()
        ax2.grid(True, alpha=0.2)
        
        # Panel 3 & 4: EHTP Metrics
        ax3 = axs[1, 0]
        cohesion = [e['introspection_probe_metrics'].get('cohesion_cluster_count', 1) for e in self.episode_data]
        ax3.plot(episodes, cohesion, 'o-', color='red', label='Cohesion (Cluster Count)')
        ax3.set_title('UKG Cohesion', fontsize=16)
        ax3.set_xlabel('Stimulus Block', fontsize=12)
        ax3.set_ylabel('Cluster Count', fontsize=12)
        ax3.legend()
        ax3.grid(True, alpha=0.2)
        
        ax4 = axs[1, 1]
        complexity = [e['introspection_probe_metrics'].get('total_b1_persistence', 0) for e in self.episode_data]
        ax4.plot(episodes, complexity, 'o-', color='yellow', label='Complexity (B1 Persistence)')
        ax4.set_title('UKG Complexity', fontsize=16)
        ax4.set_xlabel('Stimulus Block', fontsize=12)
        ax4.set_ylabel('Total B1 Persistence', fontsize=12)
        ax4.legend()
        ax4.grid(True, alpha=0.2)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        save_path = os.path.join(self.results_dir, "02_FUM_Demo_dashboard.png")
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"Saved metrics dashboard to '{save_path}'")