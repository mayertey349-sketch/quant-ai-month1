"""
Day 4: Chain Rule Practice
"""
import numpy as np
import matplotlib.pyplot as plt

def numerical_derivative(f, x, h=1e-7):
    """Calculate derivative numerically."""
    return (f(x + h) - f(x)) / h

# Problem 1: f(x) = (x² + 1)³
# let u = x² + 1, then f(x) = u³
# Chain rule : f'(x) = 3u² * du/dx = 3(x² + 1)² * 2x = 6x(x² + 1)²

def f1(x):
    return (x**2 + 1)**3

def f1_derivative(x):
    """Derivative using chain rule."""
    return 3 * (x**2 + 1)**2 * (2*x)

# Test at x = 2
x_test = 2
numerical = numerical_derivative(f1, x_test)
analytical = f1_derivative(x_test)

print(f"Problem 1: f(x) = (x² + 1)³")
print(f"At x = {x_test}:")
print(f"Numerical Derivative: {numerical:.6f}")
print(f"Analytical Derivative: {analytical:.6f}")
print(f"Match : {abs(numerical - analytical) < 0.0001}\n")

# Problem 2: f(x) = (2x + 3)⁵
# let u = 2x + 3 , then f(x) = u⁵
# Chain rule : f'(x) = 5u**4 * du/dx = 5(2x + 3)**4 * (2)

def f2(x):
    return (2*x + 3)**5

def f2_derivative(x):
   """Derivative using chain rule."""
   return 5 * (2*x + 3)**4 * (2) 

# Test at x = 2 
x = 2
numerical2 = numerical_derivative(f2,x)
analytical2 = f2_derivative(x)

print(f" Problem 2: f(x) = (2x + 3)⁵")
print(f"At x = {x}")
print(f"Numerical derivative : {numerical2:.6f}")
print(f"Analytical derivative : {analytical2:.6f}")
print(f"Match : {abs(numerical2 - analytical2 )< 0.0001}\n ")

# Problem 3 : Financial Application
# Stock price follows : P(x) = (100 + 5t)**2

def stock_price(t):
    return  (100 + 5 *t)**2

def Stock_derivative (t):
    return 2 * (100 + 5*t) * (5)

#Verifying the answers
print(f" Problem 3 :Stock Price P(t) = (100 + 5t)²")
days = [0, 5, 10]

for day in days:
    numerical= numerical_derivative(stock_price,day)
    analytical = Stock_derivative(day)
    print(f"Day {day}: Rate = {numerical:.2f} (analytical: {analytical:.2f})")
    
    
"""
Day 4: Chain Rule Applied to Compounded Returns
"""

# When reurns compound , we have nested functions
# If R₁, R₂, R₃ are returns, final value is:
# V = V₀ × (1 + R₁) × (1 + R₂) × (1 + R₃)

# The rate of change involves the chain rule!
def compounded_value(initial,returns):
    """
    Calculate final value after compounding returns.
    
    Parameters:
    initial: Initial investment
    returns: List of returns (as decimals, e.g., 0.05 for 5%)
    """
    value = initial
    for r in returns:
        value = value * (1 + r)
    return value

# Example $1000 initial investment
initial = 1000
daily_returns = [0.01, -0.005, 0.02, 0.015, -0.01]

final_value = compounded_value(initial,daily_returns)
total_return = (final_value / initial - 1) * 100

print("="*60)
print("COMPOUNDED RETURNS ANALYSIS")
print("="*60)
print(f"Initial Investment: ${initial}")
print(f"Daily Returns: {[f'{r*100:.1f}%' for r in daily_returns]}")
print(f"Final Value: ${final_value:.2f}")
print(f"Total Return: {total_return:.2f}%")
print("="*60)

# Now let's see how sensitive final value is to FIRST day's return
# This is a chain rule problem!

def sensitivity_analysis():
    """
    How does changing first day's return affect final value?
    This is the derivative (rate of change).
    """
    
    # Keep other days fixed
    fixed_returns = [-0.005, 0.02, 0.015, -0.01]
    
    # Vary first day's return
    first_day_returns = np.linspace(-0.05, 0.05, 100)
    final_values = []
    
    for r1 in first_day_returns:
        returns = [r1] + fixed_returns
        final = compounded_value(initial, returns)
        final_values.append(final)
    
    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(first_day_returns * 100, final_values, linewidth=2)
    plt.axvline(x=0, color='red', linestyle='--', alpha=0.5)
    plt.axhline(y=initial, color='red', linestyle='--', alpha=0.5)
    plt.xlabel('First Day Return (%)', fontsize=12)
    plt.ylabel('Final Portfolio Value ($)', fontsize=12)
    plt.title('Sensitivity of Final Value to First Day Return\n(Chain Rule in Action)', 
             fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('week1/day4/return_sensitivity.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Calculate numerical derivative at r1 = 1%
    r1_test = 0.01
    returns_base = [r1_test] + fixed_returns
    returns_plus = [r1_test + 0.0001] + fixed_returns
    
    value_base = compounded_value(initial, returns_base)
    value_plus = compounded_value(initial, returns_plus)
    
    sensitivity = (value_plus - value_base) / 0.0001
    
    print(f"\nSENSITIVITY ANALYSIS")
    print(f"At first day return = {r1_test*100}%:")
    print(f"A 1% increase in first day return changes final value by ${sensitivity:.2f}")
    print("\nThis is the derivative of final value with respect to first day return!")
    print("(Calculated using chain rule internally)")

sensitivity_analysis()

    