import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def f(x):
    return x * (x - 1) * (x - 2)

x_values = np.linspace(0.01, 3, 400)
y_values = f(x_values)

plt.figure(figsize=(12, 6))
plt.plot(x_values, y_values, label='f(x) = x(x-1)(x-2)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Plot of f(x) = x(x-1)(x-2)')
plt.legend()
plt.grid(True)
plt.show()

def euler_method(x0, y, h, x):
    while x0 < x:
        y = y + h * f(y)
        x0 = x0 + h
    return y

fixed_points = [0, 1, 2]

# Initial conditions to observe the behavior of ( x(t) ) near the fixed points
initial_conditions = [0.1, 0.9, 1.9]

# Parameters for Euler's method
t_max = 10
time_steps = [0.01]

fig = go.Figure()

for dt in time_steps:
    for x0 in initial_conditions:
        t_values = np.arange(0, t_max, dt)
        x_values = [x0]
        for t in t_values[1:]:
            x_new = euler_method(t - dt, x_values[-1], dt, t)
            x_values.append(x_new)
        fig.add_trace(go.Scatter(x=t_values, y=x_values, mode='lines', name=f'x0 = {x0}, dt = {dt}'))

for fp in fixed_points:
    fig.add_trace(go.Scatter(x=[0, t_max], y=[fp, fp], mode='lines', line=dict(dash='dash'), name=f'Fixed point = {fp}'))

fig.update_layout(title='Stability Analysis of Fixed Points using Euler\'s Method', xaxis_title='t', yaxis_title='x')
fig.show()