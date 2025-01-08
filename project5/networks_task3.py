import networkx as nx
from networks_task2 import (
    calculate_degree_distribution,
    calculate_clustering_coefficients,
    calculate_shortest_paths
)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random


def erdos_renyi_graph_manual(N, p):
    G = nx.Graph()
    G.add_nodes_from(range(N))
    for i in range(N):
        for j in range(i + 1, N):
            if random.random() < p:
                G.add_edge(i, j)
    return G

def plot_degree_distributions(graphs, names):
    fig = make_subplots(rows=1, cols=len(graphs), subplot_titles=names)

    for col, (G, name) in enumerate(zip(graphs, names), start=1):
        k, P_k, _ = calculate_degree_distribution(G)
        fig.add_trace(
            go.Bar(x=k, y=P_k, name=f"Degree Distribution ({name})"),
            row=1, col=col
        )

    fig.update_layout(
        title_text="Degree Distributions",
        height=400,
        showlegend=False
    )
    fig.show()


def plot_clustering_coefficients(graphs, names):
    fig = make_subplots(rows=1, cols=len(graphs), subplot_titles=names)

    for col, (G, name) in enumerate(zip(graphs, names), start=1):
        clustering_coeffs, _ = calculate_clustering_coefficients(G)
        fig.add_trace(
            go.Histogram(
                x=list(clustering_coeffs),
                nbinsx=30,
                name=f"Clustering ({name})",
            ),
            row=1, col=col
        )

    fig.update_layout(
        title_text="Clustering Coefficients",
        height=400,
        showlegend=False
    )
    fig.show()


def plot_shortest_paths(graphs, names):
    fig = make_subplots(rows=1, cols=len(graphs), subplot_titles=names)

    for col, (G, name) in enumerate(zip(graphs, names), start=1):
        all_lengths, diameter, avg_path_length = calculate_shortest_paths(G)
        fig.add_trace(
            go.Histogram(
                x=all_lengths,
                nbinsx=30,
                name=f"Shortest Paths ({name})"
            ),
            row=1, col=col
        )
        fig.add_annotation(
            x=0.5, y=1.1,
            xref=f"x{col}", yref=f"y{col}",
            text=f"Diameter: {diameter}<br>Avg Path Length: {avg_path_length:.2f}",
            showarrow=False,
            align="center"
        )

    fig.update_layout(
        title_text="Shortest Paths",
        height=400,
        showlegend=False
    )
    fig.show()


def main():
    N = 100  # Number of nodes
    L = 200  # Number of edges (for G(N, L))
    p = 0.1  # Edge probability (for G(N, p))
    k = 4  # Number of neighbors (for WS(N, k, β))
    beta = 0.2  # Rewiring probability (for WS(N, k, β))

    # Create graphs
    G_NL = nx.gnm_random_graph(N, L)  # Erdős-Rényi G(N, L)
    G_Np = erdos_renyi_graph_manual(N, p)  # Erdős-Rényi-Gilbert G(N, p)
    G_WS = nx.watts_strogatz_graph(N, k, beta)  # Watts-Strogatz WS(N, k, β)

    # Graph names
    names = ["G(N, L)", "G(N, p)", "WS(N, k, β)"]

    # Plot each property separately
    plot_degree_distributions([G_NL, G_Np, G_WS], names)
    plot_clustering_coefficients([G_NL, G_Np, G_WS], names)
    plot_shortest_paths([G_NL, G_Np, G_WS], names)



if __name__ == "__main__":
    main()
