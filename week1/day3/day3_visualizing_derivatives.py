"""
Day 3: Visualizing Derivatives
Making calculus intuition visual

This code will show :
1. A function (the curve)
2. Its derivative (the slope at each point)
3. The tangent line at a specific point
"""
import numpy as np
import matplotlib.pyplot as plt

def visualize_derivative(f, f_prime, x_range, tangent_x):
    """
    Visualizes a function and its derivative, along with the tangent line at a specific point.
    
    Parameters:
    f : function
        The original function to visualize.
    f_prime : function
        The derivative of the function.
    x_range : tuple
        The range of x values to plot (min, max).
    tangent_x : float
        The x value at which to draw the tangent line.
    """
    # create x values
    x = np.linspace(x_range[0], x_range[1], 1000)
    
    # calc y values
    y = f(x)
    y_prime = f_prime(x)
    
    # calculate tangent line at tangent_x
    slope = f_prime(tangent_x)
    y_tangent = f(tangent_x)
    
    # Tangent line: y - y0 = m(x - x0)
    # Rearranged: y = m(x - x0) + y0
    tangent_line = slope *(x - tangent_x) + y_tangent
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Top plot: function and tangent line
    ax1.plot(x,y, 'b-', linewidth=2, label='f(x)')
    ax1.plot(x , tangent_line, 'r--', linewidth=2, label=f'Tangent Line at x={tangent_x}')
    ax1.plot(tangent_x, y_tangent, 'ro', markersize=10, label=f'Point ({tangent_x}, {y_tangent:.2f})')
    ax1.axhline(y=0, color='black', linewidth=0.5)
    ax1.axvline(x=0, color='black', linewidth=0.5)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=12)
    ax1.set_title(f'Function and Tangent Line\nSlope at x={tangent_x}: {slope:.3f}', fontsize=14)
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('f(x)', fontsize=12)
    
     # BOTTOM PLOT: Derivative function
    ax2.plot(x, y_prime, 'g-', linewidth=2, label="f'(x) (derivative)")
    ax2.plot(tangent_x, slope, 'ro', markersize=10, label=f"f'({tangent_x}) = {slope:.3f}")
    ax2.axhline(y=0, color='black', linewidth=0.5)
    ax2.axvline(x=0, color='black', linewidth=0.5)
    ax2.grid(True, alpha=0.3)
    ax2.legend(fontsize=12)
    ax2.set_title("Derivative Function (Rate of Change)", fontsize=14)
    ax2.set_xlabel('x', fontsize=12)
    ax2.set_ylabel("f'(x)", fontsize=12)
    
    plt.tight_layout()
    plt.show()
    
 # Print interpretation
    print("\n" + "="*60)
    print("INTERPRETATION")
    print("="*60)
    print(f"At x = {tangent_x}:")
    print(f"  • Function value: f({tangent_x}) = {y_tangent:.3f}")
    print(f"  • Slope (derivative): f'({tangent_x}) = {slope:.3f}")
    print(f"  • Meaning: The function is {'increasing' if slope > 0 else 'decreasing'}")
    print(f"            at a rate of {abs(slope):.3f} units per unit of x")
    print("="*60)

# EXAMPLE 1: f(x) = x²
print("EXAMPLE 1: f(x) = x²")
print("We know: f'(x) = 2x")

def f1(x):
    return x**2

def f1_prime(x):
    return 2*x

visualize_derivative(f1, f1_prime, x_range=(-3, 3), tangent_x=1)

# EXAMPLE 2: f(x) = x³ - 3x
print("\n\nEXAMPLE 2: f(x) = x³ - 3x")
print("We know: f'(x) = 3x² - 3")

def f2(x):
    return x**3 - 3*x

def f2_prime(x):
    return 3*x**2 - 3

visualize_derivative(f2, f2_prime, x_range=(-2, 2), tangent_x=0)

# FINANCIAL EXAMPLE: Stock price model
print("\n\nFINANCIAL EXAMPLE: Stock Price P(t) = 100 + 10t - 0.5t²")
print("This models a stock that initially rises, then slows down")
print("Derivative P'(t) = 10 - t tells us the rate of price change")

def stock_price(t):
    return 100 + 10*t - 0.5*t**2

def stock_price_rate(t):
    return 10 - t

visualize_derivative(stock_price, stock_price_rate, x_range=(0, 25), tangent_x=10)

print("\nNOTICE:")
print("• When derivative > 0: Price is rising")
print("• When derivative = 0: Price peaks (maximum)")
print("• When derivative < 0: Price is falling")
print("\nAt t=10 days, derivative = 0, so price is at maximum!")


