# Exercise 3: Your own function
# Pick any polynomial (like x⁴ - 2x² + 1)
# Calculate its derivative
# Visualize it using visualize_derivative()
from day3_visualizing_derivatives import visualize_derivative

# Defining my polynomial function: f(x) = x⁴ - 2x² + 1
def f(x):
    return x**4 - 2*x**2 +1

# Defining its derivative: f'(x) = 4x³ - 4x
def f_prime(x):
    return 4*x**3 - 4*x

# Visualize the function and its derivative at a specific point
tangent_x = 1  # You can change this value to visualize at different points
print(f"\n\nVisualizing f(x) = x⁴ - 2x² + 1 at x = {tangent_x}")
visualize_derivative(f, f_prime, x_range=(-3, 3), tangent_x=tangent_x)
