# Exercise 2: Profit function
# A company's profit is P(x) = -x² + 20x - 50
# where x is units sold (in thousands)
# Derivative: P'(x) = -2x + 20
# Find: At what x is profit maximized? (where derivative = 0)
from day3_visualizing_derivatives import visualize_derivative
# Define the profit function P(x)
def Profit(x):
    return -x**2 + 20*x - 50

# Define the derivative P'(x)
def Profit_prime(x):
    return -2*x + 20

# Solve for maximum: -2x + 20 = 0 → x = 10
x_max = 10
max_profit = Profit(x_max)

print(f"Profit is maximized at x = {x_max} thousand units")
print(f"Maximum profit: P({x_max}) = ${max_profit} thousand")

# Visualize the profit function and its derivative
print(f"\nVisualizing Profit function P(x)")
visualize_derivative(Profit, Profit_prime, x_range=(0, 20), tangent_x=x_max)
