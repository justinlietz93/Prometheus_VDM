
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

class Visualizer:
    def __init__(self, run_dir: str):
        self.run_dir = run_dir

    def dashboard(self, history):
        os.makedirs(self.run_dir, exist_ok=True)
        fig, axs = plt.subplots(2, 2, figsize=(12, 9))
        t = [h['t'] for h in history]

        axs[0,0].plot(t, [h['active_synapses'] for h in history])
        axs[0,0].set_title('UKG Sparsity Over Time')
        axs[0,0].set_xlabel('Tick')
        axs[0,0].set_ylabel('Active Synapses')

        axs[0,1].plot(t, [h['avg_weight'] for h in history], marker='o', linestyle='-')
        axs[0,1].set_title('Average Synaptic Weight Over Time')
        axs[0,1].set_xlabel('Tick')
        axs[0,1].set_ylabel('Average Weight')

        axs[1,0].plot(t, [h['cohesion_components'] for h in history])
        axs[1,0].set_title('UKG Cohesion (Component Count)')
        axs[1,0].set_xlabel('Tick')
        axs[1,0].set_ylabel('Components')

        axs[1,1].plot(t, [h['complexity_cycles'] for h in history])
        axs[1,1].set_title('UKG Complexity (Cycles)')
        axs[1,1].set_xlabel('Tick')
        axs[1,1].set_ylabel('Cycles')

        fig.suptitle('FUM Performance Dashboard', fontsize=14)
        fig.tight_layout()
        # Overlay Control URL (Load Engram) if available
        try:
            import json as _json
            ctrl_url = None
            try:
                with open(os.path.join(self.run_dir, 'control.json'), 'r', encoding='utf-8') as _fh:
                    _ctrl = _json.load(_fh)
                    if isinstance(_ctrl, dict):
                        ctrl_url = _ctrl.get('url')
            except Exception:
                ctrl_url = None
            if ctrl_url:
                try:
                    import matplotlib.pyplot as _plt
                    _plt.subplots_adjust(bottom=0.16)
                except Exception:
                    pass
                fig.text(0.01, 0.01, f'Controls: {ctrl_url} — Load Engram', fontsize=9, color='#8b949e')
        except Exception:
            pass

        path = os.path.join(self.run_dir, 'dashboard.png')
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path

    def graph(self, G, fname='connectome.png'):
        os.makedirs(self.run_dir, exist_ok=True)
        fig = plt.figure(figsize=(8,8))
        pos = nx.spring_layout(G, seed=42, dim=2)
        nx.draw_networkx_nodes(G, pos, node_size=10)
        nx.draw_networkx_edges(G, pos, alpha=0.3)
        fig.suptitle('Foundational UKG Structure', fontsize=14)
        path = os.path.join(self.run_dir, fname)
        fig.savefig(path, dpi=150)
        plt.close(fig)
        return path
