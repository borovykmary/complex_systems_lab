import numpy as np
import plotly.graph_objects as go


def oslo_model(L, T, initial_thresholds=None):
    z = np.zeros(L, dtype=int)
    thresholds = np.random.choice([1, 2], size=L) if initial_thresholds is None else initial_thresholds

    heights = []
    slopes = []
    avalanches = []

    for t in range(T):
        z[0] += 1
        avalanche_size = 0

        while np.any(z > thresholds):
            for i in range(L):
                if z[i] > thresholds[i]:
                    avalanche_size += 1
                    if i == 0:  # First site
                        z[i] -= 2
                        z[i + 1] += 1
                    elif i == L - 1:  # Last site
                        z[i] -= 2
                        z[i - 1] += 1
                    else:  # Middle sites
                        z[i] -= 2
                        z[i - 1] += 1
                        z[i + 1] += 1

                    thresholds[i] = np.random.choice([1, 2])

        heights.append(np.sum(z))
        slopes.append(z.copy())
        avalanches.append(avalanche_size)

    return heights, slopes, avalanches

# Task 2: Scaled Avalanche Sizes
def plot_scaled_avalanches(L, T):
    _, _, avalanches = oslo_model(L, T)
    s_max = max(avalanches)  # Find the largest avalanche size
    scaled_avalanches = [s / s_max for s in avalanches]  # Scale by the largest avalanche size

    # Plot scaled avalanche sizes over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(scaled_avalanches))), y=scaled_avalanches, mode='lines', name=f'L={L}'))
    fig.update_layout(title='Scaled Avalanche Size vs Time',
                      xaxis_title='Time step (Grain Additions)',
                      yaxis_title='Scaled Avalanche Size',
                      legend_title='System Size',
                      template='plotly_white')
    fig.show()


# Task 3: Avalanche Size Probability
def plot_avalanche_probability(system_sizes, T):
    fig = go.Figure()

    for L in system_sizes:
        _, _, avalanches = oslo_model(L, T)
        s_values, counts = np.unique(avalanches, return_counts=True)  # Find unique sizes and their counts
        probabilities = counts / np.sum(counts)  # Normalize to calculate probabilities

        fig.add_trace(go.Scatter(x=s_values, y=probabilities, mode='lines+markers', name=f'L={L}'))

    fig.update_layout(title='Avalanche Size Probability in Log-Log Scale',
                      xaxis_title='Avalanche Size',
                      yaxis_title='Probability',
                      legend_title='System Size',
                      xaxis_type='log',
                      yaxis_type='log',
                      template='plotly_white')
    fig.show()


L = 16
T = 1000
plot_scaled_avalanches(L, T)

system_sizes = [64, 128, 256]  # Different system sizes for Task 3
plot_avalanche_probability(system_sizes, T)

