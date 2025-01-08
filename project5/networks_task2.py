import networkx as nx
import plotly.graph_objects as go
import numpy as np
from networks_task1 import read_file, visualize_network

def calculate_degree_distribution(G):
    degrees = [G.degree(n) for n in G.nodes()]
    degree_count = np.bincount(degrees)
    k = np.arange(len(degree_count))
    P_k = degree_count / sum(degree_count)
    avg_degree = np.mean(degrees)
    return k, P_k, avg_degree

def calculate_clustering_coefficients(G):
    clustering_coeffs = nx.clustering(G).values()
    avg_clustering_coeff = np.mean(list(clustering_coeffs))
    return clustering_coeffs, avg_clustering_coeff

def calculate_shortest_paths(G):
    path_lengths = dict(nx.all_pairs_shortest_path_length(G))
    all_lengths = [length for target_dict in path_lengths.values() for length in target_dict.values()]
    diameter = max(all_lengths)
    avg_path_length = np.mean(all_lengths)
    return all_lengths, diameter, avg_path_length

def main():
    edges = read_file('facebook_combined.txt')
    G = nx.Graph()
    G.add_edges_from(edges)

    # (a) Degree distribution and average degree
    k, P_k, avg_degree = calculate_degree_distribution(G)
    print(f'Average Degree: {avg_degree}')

    # (b) Clustering coefficients and average clustering coefficient
    clustering_coeffs, avg_clustering_coeff = calculate_clustering_coefficients(G)
    print(f'Average Clustering Coefficient: {avg_clustering_coeff}')

    # (c) Shortest paths, diameter, and average path length
    all_lengths, diameter, avg_path_length = calculate_shortest_paths(G)
    print(f'Diameter: {diameter}')
    print(f'Average Path Length: {avg_path_length}')

    visualize_network(G)

if __name__ == "__main__":
    main()