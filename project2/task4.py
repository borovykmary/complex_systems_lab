import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define the original nonlinear system
def system(t, variables):
    x, y = variables
    dxdt = x * (3 - x - 2 * y)
    dydt = y * (2 - x - y)
    return [dxdt, dydt]

# Define the modified system (Lotka-Volterra)
def modified_system(t, variables):
    x, y = variables
    dxdt = x * (3 - x - y)  # Modify the equation for dx/dt
    dydt = y * (3 - x - y)  # Modify the equation for dy/dt
    return [dxdt, dydt]

# Define the initial conditions
x_values = np.linspace(0, 3, 20)
y_values = np.linspace(0, 3, 20)
X, Y = np.meshgrid(x_values, y_values)

# Compute vector field for the original system
U = X * (3 - X - 2 * Y)
V = Y * (2 - X - Y)

# phase portrait for the original system
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.quiver(X, Y, U, V, color="teal")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Phase Portrait of Original System")
plt.xlim(0, 3)
plt.ylim(0, 3)

# Compute vector field for the modified system
U_mod = X * (3 - X - Y)
V_mod = Y * (3 - X - Y)

# phase portrait for the modified system
plt.subplot(1, 2, 2)
plt.quiver(X, Y, U_mod, V_mod, color="orange")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Phase Portrait of Modified System (Stable Nonzero Population)")
plt.xlim(0, 3)
plt.ylim(0, 3)


plt.tight_layout()
plt.show()
