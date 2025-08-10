# analyze_graph.py
import networkx as nx
import numpy as np
import json

def analyze_ukg(adjacency_file):
    adj_matrix = np.load(adjacency_file)
    G = nx.from_numpy_array(adj_matrix, create_using=nx.DiGraph)
    
    if not nx.is_connected(G.to_undirected()):
        print("Graph is not connected. Analyzing the largest connected component.")
        largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
        G = G.subgraph(largest_cc)

    metrics = {
        "num_nodes": G.number_of_nodes(),
        "num_edges": G.number_of_edges(),
        "density": nx.density(G),
        "average_clustering_coefficient": nx.average_clustering(G),
        "degree_centrality_mean": np.mean(list(nx.degree_centrality(G).values())),
        "is_small_world": None
    }
    
    try:
        metrics["is_small_world"] = nx.is_small_world(G)
    except Exception as e:
        metrics["is_small_world"] = f"Could not compute: {e}"

    with open('graph_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

    print("Graph analysis complete. Metrics saved to graph_metrics.json")

if __name__ == "__main__":
    analyze_ukg('ukg_adjacency.npy') # Assumes you saved your graph