
import argparse, os, json, csv, math, networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def load_edgelist(path):
    try:
        G = nx.read_edgelist(path, delimiter=",", data=(('w', float),), create_using=nx.Graph)
    except Exception:
        # try without weights
        G = nx.read_edgelist(path, delimiter=",", create_using=nx.Graph)
    return G

def ring_lattice_suspicion(G):
    N = G.number_of_nodes()
    degs = np.array([d for _,d in G.degree()])
    deg_var = float(np.var(degs))
    c = nx.average_clustering(G)
    try:
        a = nx.degree_assortativity_coefficient(G)
    except Exception:
        a = float('nan')
    # cycle basis size for undirected
    cycles = nx.cycle_basis(G)
    cycle_count = len(cycles)

    suspicion = (deg_var < 1.0) and (c < 0.2) and (cycle_count >= N*0.8)

    return {
        "N": N,
        "degree_variance": deg_var,
        "avg_clustering": c,
        "assortativity": a,
        "cycle_basis_count": cycle_count,
        "ring_lattice_suspicion": suspicion
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--edgelist', required=True, help='CSV edgelist src,dst[,w]')
    ap.add_argument('--out', default='outputs', help='output folder')
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    G = load_edgelist(args.edgelist)
    metrics = ring_lattice_suspicion(G)

    with open(os.path.join(args.out, 'connectome_metrics.json'), 'w') as f:
        json.dump(metrics, f, indent=2)

    # quick layout
    pos = nx.spring_layout(G, seed=42, k=None)
    plt.figure(figsize=(6,6))
    nx.draw_networkx_nodes(G, pos, node_size=10)
    nx.draw_networkx_edges(G, pos, alpha=0.15, width=0.5)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(os.path.join(args.out, 'connectome_layout.png'), dpi=180)

if __name__ == "__main__":
    main()
