import numpy as np
import matplotlib.pyplot as plt

# Define the system of first-order equations for x'' + x = 0
def f1(x, y):
    return -x

# Define the system of first-order equations for x'' + sin(x) = 0
def f2(x, y):
    return -np.sin(x)

# Define the system of first-order equations for x'' = -x + x^3
def f3(x, y):
    return -x + x**3

# Define the system of first-order equations for x'' = x - x^3
def f4(x, y):
    return x - x**3

def midpoint_method(f, x0, y0, t_max, h):
    t_values = np.arange(0, t_max, h)
    x_values = [x0]
    y_values = [y0]

    for _ in t_values[:-1]:
        x_n = x_values[-1]
        y_n = y_values[-1]

        k1_x = h * y_n
        k1_y = h * f(x_n, y_n)

        x_mid = x_n + 0.5 * k1_x
        y_mid = y_n + 0.5 * k1_y

        k2_x = h * y_mid
        k2_y = h * f(x_mid, y_mid)

        x_next = x_n + k2_x
        y_next = y_n + k2_y

        if abs(x_next) > 1e2 or abs(y_next) > 1e2:
            break

        x_values.append(x_next)
        y_values.append(y_next)

    return t_values[:len(x_values)], x_values, y_values

# Initial conditions
initial_conditions = [
    (0.5, 0), (0.2, 0.5), (0.3, 0.1), (0.1, 0.3),
    (0.4, 0.2), (0.6, 0.1), (0.1, 0.6), (0.7, 0.3),
    (0.3, 0.4), (0.2, 0.2), (0.5, 0.5), (0.6, 0.6),
    (0.7, 0.7), (0.8, 0.8), (0.9, 0.9), (1.0, 1.0)
]

# Parameters
t_max = 10
h = 0.001
plt.style.use('seaborn-v0_8-deep')

# Plot phase portraits for each initial condition for x'' + x = 0
plt.figure(figsize=(12, 6))
for x0, y0 in initial_conditions:
    t_values, x_values, y_values = midpoint_method(f1, x0, y0, t_max, h)
    plt.plot(x_values, y_values, label=f'Initial: x0={x0}, y0={y0} (x\'\' + x = 0)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Phase Portraits using Midpoint Method for x\'\' + x = 0')
plt.legend()
plt.grid(True)
plt.show()

# Plot phase portraits for each initial condition for x'' + sin(x) = 0
plt.figure(figsize=(12, 6))
for x0, y0 in initial_conditions:
    t_values, x_values, y_values = midpoint_method(f2, x0, y0, t_max, h)
    plt.plot(x_values, y_values, label=f'Initial: x0={x0}, y0={y0} (x\'\' + sin(x) = 0)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Phase Portraits using Midpoint Method for x\'\' + sin(x) = 0')
plt.legend()
plt.grid(True)
plt.show()

# Plot phase portraits for each initial condition for x'' = -x + x^3
plt.figure(figsize=(12, 6))
for x0, y0 in initial_conditions:
    t_values, x_values, y_values = midpoint_method(f3, x0, y0, t_max, h)
    plt.plot(x_values, y_values, label=f'Initial: x0={x0}, y0={y0} (x\'\' = -x + x^3)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Phase Portraits using Midpoint Method for x\'\' = -x + x^3')
plt.legend()
plt.grid(True)
plt.show()

# Plot phase portraits for each initial condition for x'' = x - x^3
plt.figure(figsize=(12, 6))
for x0, y0 in initial_conditions:
    t_values, x_values, y_values = midpoint_method(f4, x0, y0, t_max, h)
    plt.plot(x_values, y_values, label=f'Initial: x0={x0}, y0={y0} (x\'\' = x - x^3)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Phase Portraits using Midpoint Method for x\'\' = x - x^3')
plt.legend()
plt.grid(True)
plt.show()
