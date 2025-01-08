import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.ndimage import label

def read_percolation_data(file_names):
    data = {}
    for file_name in file_names:
        L = int(file_name.split('_')[1][1:])
        data[L] = []
        with open(file_name, 'r') as file:
            for line in file:
                p, p_flow, smax = map(float, line.split())
                data[L].append((p, p_flow, smax))
    return data

def plot_percolation_data(data):
    # Plot p against p_flow for different L
    plt.figure(figsize=(12, 6))
    for L, values in data.items():
        p_values = [item[0] for item in values]
        p_flow_values = [item[1] for item in values]
        plt.plot(p_values, p_flow_values, label=f'L={L}')
    plt.xlabel('p')
    plt.ylabel('p_flow')
    plt.title('p vs p_flow for different L')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot smax as a function of p for different L
    plt.figure(figsize=(12, 6))
    for L, values in data.items():
        p_values = [item[0] for item in values]
        smax_values = [item[2] for item in values]
        plt.plot(p_values, smax_values, label=f'L={L}')
    plt.xlabel('p')
    plt.ylabel('smax')
    plt.title('smax as a function of p for different L')
    plt.legend()
    plt.grid(True)
    plt.show()

# Example usage:
file_names = ['Ave_L10_T1000.txt', 'Ave_L50_T1000.txt', 'Ave_L100_T1000.txt']
data = read_percolation_data(file_names)
plot_percolation_data(data)

def generate_lattice(L, p):
    return np.random.rand(L, L) < p

def burning_algorithm(lattice):
    L = len(lattice)
    label = np.copy(lattice).astype(int)
    t = 2

    # Label all occupied cells in the top line with the marker t=2
    for j in range(L):
        if lattice[0, j] == 1:
            label[0, j] = t

    while True:
        burning_cells = np.argwhere(label == t)
        if not burning_cells.size:
            break

        for x, y in burning_cells:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < L and 0 <= ny < L and label[nx, ny] == 1:
                    label[nx, ny] = t + 1

        if np.any(label[L-1, :] == t + 1):
            return label, t

        t += 1

    return label, t - 1


def hk_algorithm(lattice):
    labeled_lattice, num_features = label(lattice)
    cluster_sizes = np.bincount(labeled_lattice.ravel())[1:]  # Exclude background
    return labeled_lattice, cluster_sizes

def plot_lattice(lattice, title, cmap='copper'):
    plt.imshow(lattice, cmap=cmap, interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    for (i, j), val in np.ndenumerate(lattice):
        if val > 0:
            plt.text(j, i, f'{val}', ha='center', va='center', color='white')
    plt.show()

def visualize_configurations(file_name):
    L = int(file_name.split('_')[1][1:])
    p_values = []

    with open(file_name, 'r') as file:
        for line in file:
            p = float(line.split()[0])
            p_values.append(p)

    for p in p_values:
        lattice = generate_lattice(L, p)

        burned_lattice, shortest_path = burning_algorithm(lattice)
        plot_lattice(burned_lattice, f'Burning Algorithm for L={L}, p={p}, Shortest Path={shortest_path}', cmap='hot')

        hk_lattice, cluster_sizes = hk_algorithm(lattice)
        plot_lattice(hk_lattice, f'HK Algorithm for L={L}, p={p}', cmap='tab20')


# Example usage:
visualize_configurations('Ave_L10_T1000.txt')

def read_cluster_distribution(file_name):
    data = np.loadtxt(file_name)
    s = data[:, 0]
    n_s = data[:, 1]
    return s, n_s

def plot_cluster_distribution(file_names, pc=0.592746):
    plt.figure(figsize=(18, 6))

    # Subplot for p < pc
    plt.subplot(1, 3, 1)
    for file_name in file_names:
        p = float(file_name.split('_')[1][1:])
        if p < pc:
            s, n_s = read_cluster_distribution(file_name)
            plt.loglog(s, n_s, label=f'p={p:.2f}')
    plt.xlabel('Cluster size s')
    plt.ylabel('n(s, p, L)')
    plt.title(f'Cluster Distribution for p < {pc}')
    plt.legend()
    plt.grid(True, which="both", ls="--")

    # Subplot for p = pc
    plt.subplot(1, 3, 2)
    for file_name in file_names:
        p = float(file_name.split('_')[1][1:])
        if p == pc:
            s, n_s = read_cluster_distribution(file_name)
            plt.loglog(s, n_s, label=f'p={pc:.6f}')
    plt.xlabel('Cluster size s')
    plt.ylabel('n(s, p, L)')
    plt.title(f'Cluster Distribution for p = {pc}')
    plt.legend()
    plt.grid(True, which="both", ls="--")

    # Subplot for p > pc
    plt.subplot(1, 3, 3)
    for file_name in file_names:
        p = float(file_name.split('_')[1][1:])
        if p > pc:
            s, n_s = read_cluster_distribution(file_name)
            plt.loglog(s, n_s, label=f'p={p:.2f}')
    plt.xlabel('Cluster size s')
    plt.ylabel('n(s, p, L)')
    plt.title(f'Cluster Distribution for p > {pc}')
    plt.legend()
    plt.grid(True, which="both", ls="--")

    plt.tight_layout()
    plt.show()

# Example usage:
file_names = [
    'Dist_p0.20_L10_T1000.txt', 'Dist_p0.30_L10_T1000.txt', 'Dist_p0.40_L10_T1000.txt',
    'Dist_p0.50_L10_T1000.txt', 'Dist_p0.592746_L10_T1000.txt', 'Dist_p0.60_L10_T1000.txt',
    'Dist_p0.70_L10_T1000.txt', 'Dist_p0.80_L10_T1000.txt'
]
plot_cluster_distribution(file_names)