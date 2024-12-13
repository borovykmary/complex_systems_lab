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
    label = np.zeros_like(lattice, dtype=int)
    current_label = 1

    def burn(x, y, step):
        if x < 0 or x >= L or y < 0 or y >= L or lattice[x, y] == 0 or label[x, y] != 0:
            return
        label[x, y] = step
        burn(x+1, y, step+1)
        burn(x-1, y, step+1)
        burn(x, y+1, step+1)
        burn(x, y-1, step+1)

    for i in range(L):
        for j in range(L):
            if lattice[i, j] == 1 and label[i, j] == 0:
                burn(i, j, current_label)
                current_label += 1

    return label

def hk_algorithm(lattice):
    labeled_lattice, num_features = label(lattice)
    cluster_sizes = np.bincount(labeled_lattice.ravel())[1:]  # Exclude background
    return labeled_lattice

def plot_lattice(lattice, title, cmap='hot'):
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

        burned_lattice = burning_algorithm(lattice)
        plot_lattice(burned_lattice, f'Burning Algorithm for L={L}, p={p}', cmap='hot')

        hk_lattice = hk_algorithm(lattice)
        plot_lattice(hk_lattice, f'HK Algorithm for L={L}, p={p}', cmap='tab20')

# Example usage:
visualize_configurations('Ave_L10_T1000.txt')