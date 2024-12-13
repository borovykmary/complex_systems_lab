import numpy as np
import random
from scipy.ndimage import label

def load_parameters(file_name):
    with open(file_name, 'r') as f:
        params = {}
        for line in f:
            line = line.strip()  # Remove extra spaces or newlines
            if not line or '%' not in line:  # Skip empty or invalid lines
                print(f"Skipping invalid line: {line}")
                continue
            try:
                key, comment = line.split('%')
                params[comment.strip()] = float(key.strip())
            except ValueError as e:
                print(f"Error parsing line '{line}': {e}")
    return params

def initialize_lattice(L, p):
    return (np.random.rand(L, L) < p).astype(int)

def check_connectivity(lattice):
    L = lattice.shape[0]
    visited = np.zeros_like(lattice, dtype=bool)

    # Start burning from all occupied sites in the top row
    burn_stack = [(0, col) for col in range(L) if lattice[0, col] == 1]

    while burn_stack:
        x, y = burn_stack.pop()

        if visited[x, y]:
            continue

        visited[x, y] = True

        # Check if we reached the bottom row
        if x == L - 1:
            return True

        # Add neighbors to the burn stack
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < L and 0 <= ny < L and lattice[nx, ny] == 1 and not visited[nx, ny]:
                burn_stack.append((nx, ny))

    return False


def hoshen_kopelman(lattice):
    labeled_lattice, num_features = label(lattice)
    cluster_sizes = np.bincount(labeled_lattice.ravel())[1:]  # Exclude background
    return cluster_sizes


def monte_carlo(L, T, p_range):
    p_min, p_max, dp = p_range
    probabilities = []
    max_cluster_sizes = []
    cluster_distributions = {}

    p_values = np.arange(p_min, p_max + dp, dp)

    for p in p_values:
        flow_count = 0
        max_sizes = []
        cluster_size_distribution = []

        for _ in range(int(T)):
            lattice = initialize_lattice(L, p)

            # Check connectivity
            if check_connectivity(lattice):
                flow_count += 1

            # Calculate maximum cluster size
            cluster_sizes = hoshen_kopelman(lattice)
            if cluster_sizes.size > 0:
                max_sizes.append(cluster_sizes.max())

            cluster_size_distribution.extend(cluster_sizes)

        probabilities.append(flow_count / T)
        max_cluster_sizes.append(np.mean(max_sizes) if max_sizes else 0)
        cluster_distributions[p] = np.bincount(cluster_size_distribution)

    return p_values, probabilities, max_cluster_sizes, cluster_distributions


def save_results(p_values, probabilities, max_cluster_sizes, cluster_distributions, L, T):

    with open(f"Ave_L{L}_T{T}.txt", 'w') as f:
        for p, P_flow, s_max in zip(p_values, probabilities, max_cluster_sizes):
            f.write(f"{p:.2f}  {P_flow:.2f}  {s_max:.2f}\n")


    for p, distribution in cluster_distributions.items():
        with open(f"Dist_p{p:.2f}_L{L}_T{T}.txt", 'w') as f:
            for size, count in enumerate(distribution):
                f.write(f"{size}  {count}\n")


def main():
    params = load_parameters("perc_ini.txt")
    L = int(params["L"])
    T = int(params["T"])
    p_min = params["p0"]
    p_max = params["pk"]
    dp = params["dp"]

    p_values, probabilities, max_cluster_sizes, cluster_distributions = monte_carlo(
        L, T, (p_min, p_max, dp)
    )

    save_results(p_values, probabilities, max_cluster_sizes, cluster_distributions, L, T)

if __name__ == "__main__":
    main()
