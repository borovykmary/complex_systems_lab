import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import eig, det

# Define matrices
matrices = {
    'a': np.array([[-2, 1], [0, 2]]),
    'b': np.array([[3, -4], [2, -1]]),
    'c': np.array([[-3, -2], [-1, -3]]),
    'd': np.array([[2, 0], [0, 2]])
}


def plot_phase_portrait(A, title, t_max=10, dt=0.01, grid_size=6):
    # Set up a grid of initial conditions
    x_vals = np.linspace(-5, 5, grid_size)
    y_vals = np.linspace(-5, 5, grid_size)

    max_val = 1e3

    initial_conditions = [(x, y) for x in x_vals for y in y_vals]

    plt.figure(figsize=(12, 6))
    plt.title(f"Phase Portrait for {title}")
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    # For each initial condition, compute the trajectory
    for (x0, y0) in initial_conditions:
        trajectory = []
        x = np.array([x0, y0])
        for _ in np.arange(0, t_max, dt):
            if np.any(np.abs(x) > max_val):
                break
            trajectory.append(x)
            x = x + dt * A @ x  # Euler method: x_{n+1} = x_n + dt * (A @ x_n)

        # Convert trajectory to x1 and x2 for plotting
        trajectory = np.array(trajectory)
        plt.plot(trajectory[:, 0], trajectory[:, 1], 'b-', linewidth=0.5)

    plt.grid()
    plt.show()


def analyze_matrix(A, label):
    trace_A = np.trace(A)
    det_A = det(A)

    eigenvalues = eig(A)[0]

    # Classify based on trace and determinant
    if det_A < 0:
        behavior = "Saddle Point"
    elif trace_A ** 2 > 4 * det_A:
        behavior = "Node"
    elif trace_A ** 2 < 4 * det_A:
        behavior = "Spiral"
    else:
        behavior = "Center"

    # Print analysis
    print(f"Matrix {label}:")
    print(f"A =\n{A}")
    print(f"Trace = {trace_A}, Determinant = {det_A}")
    print(f"Eigenvalues: {eigenvalues}")
    print(f"Behavior: {behavior}")
    print()


# Run analysis and plot for each matrix
for label, A in matrices.items():
    analyze_matrix(A, label)
    plot_phase_portrait(A, f"Matrix {label}")
