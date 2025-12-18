# Exercise 1: Visualize f(x) = x³
# Write the function and its derivative
# Use visualize_derivative() from before
# Try points: x = -1, x = 0, x = 1

from day3_visualizing_derivatives import visualize_derivative


# Define the function f(x) = x^3
def f(x):
    return x**3

# Define the derivative f'(x) = 3x^2
def f_prime(x):
    return 3*x**2

# Visualize at different points
tangent_x = [-1, 0, 1]

for x in tangent_x:
    print(f"\n\nVisualizing f(x) = x³ at x = {x}")
    visualize_derivative(f, f_prime, x_range=(-2, 2), tangent_x=x)
    