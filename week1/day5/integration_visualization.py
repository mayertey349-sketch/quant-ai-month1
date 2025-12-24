"""
Day 5: Visualizing Integration
Understanding integration through visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def visualize_integration(f, a, b, n=50):
    """
    Visualize integration as area under curve.
    
    Parameters:
    f: Function to integrate
    a: Lower bound
    b: Upper bound
    n: Number of rectangles for Riemann sum
    """
    
    # Create smooth curve
    x_smooth = np.linspace(a, b, 1000)
    y_smooth = np.array([f(x) for x in x_smooth])
    
    # Create rectangles for visualization
    x_rect = np.linspace(a, b, n+1)
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 14))
    
    # PLOT 1: Function with area shaded
    ax1.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x)')
    ax1.fill_between(x_smooth, 0, y_smooth, alpha=0.3, color='blue')
    ax1.axhline(y=0, color='black', linewidth=0.5)
    ax1.axvline(x=0, color='black', linewidth=0.5)
    ax1.set_title('Integration as Area Under Curve', fontsize=14, fontweight='bold')
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # PLOT 2: Riemann sum (rectangles approximating area)
    ax2.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x)')
    
    # Draw rectangles (midpoint method)
    dx = (b - a) / n
    total_area = 0
    for i in range(n):
        x_mid = a + (i + 0.5) * dx
        height = f(x_mid)
        total_area += height * dx
        
        rect = Rectangle((a + i*dx, 0), dx, height, fill=False, edgecolor='red', linewidth=1.5)
        ax2.add_patch(rect)
    
    ax2.axhline(y=0, color='black', linewidth=0.5)
    ax2.set_title(f'Riemann Sum Approximation (n={n} rectangles)\nArea ≈ {total_area:.4f}', fontsize=14, fontweight='bold')
    ax2.set_xlabel('x')
    ax2.set_ylabel('f(x)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # PLOT 3: Convergence (more rectangles = better approximation)
    rectangle_counts = [5, 10, 20, 50, 100, 500, 1000]
    approximations = []
    
    for num_rects in rectangle_counts:
        dx = (b - a) / num_rects
        area = sum(f(a + (i + 0.5) * dx) * dx for i in range(num_rects))
        approximations.append(area)
    
    ax3.plot(rectangle_counts, approximations, 'ro-', linewidth=2, markersize=8)
    ax3.axhline(y=approximations[-1], color='green', linestyle='--', linewidth=2, label=f'True value ≈ {approximations[-1]:.6f}')
    ax3.set_title('Convergence: More Rectangles → Better Approximation', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Number of Rectangles')
    ax3.set_ylabel('Approximated Area')
    ax3.set_xscale('log')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('week1/day5/integration_visualization.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*60)
    print("INTEGRATION INTERPRETATION")
    print("="*60)
    print(f"Function: f(x)")
    print(f"Interval: [{a}, {b}]")
    print(f"Approximate area (using {n} rectangles): {total_area:.6f}")
    print(f"\nAs we use more rectangles, approximation improves:")
    print(f"  5 rectangles:    {approximations[0]:.6f}")
    print(f"  50 rectangles:   {approximations[3]:.6f}")
    print(f"  1000 rectangles: {approximations[6]:.6f}")
    print("\nThis is what integration calculates: the EXACT area")
    print("="*60)


# EXAMPLE 1: f(x) = x²
print("EXAMPLE 1: Integrating f(x) = x² from 0 to 1")
print("We know the exact answer: ∫₀¹ x² dx = 1/3 = 0.33333...")

def f1(x):
    return x**2

visualize_integration(f1, 0, 1, n=20)


# EXAMPLE 2: f(x) = sin(x)
print("\n\nEXAMPLE 2: Integrating f(x) = sin(x) from 0 to π")
print("We know the exact answer: ∫₀ᵖⁱ sin(x) dx = 2")

def f2(x):
    return np.sin(x)

visualize_integration(f2, 0, np.pi, n=20)


# FINANCIAL EXAMPLE: Daily returns
print("\n\nFINANCIAL EXAMPLE: Cumulative return as integral")
print("If you have daily returns r(t), cumulative return is the integral!")

def daily_return(t):
    """
    Simulated daily return function.
    In reality, this would be actual market data.
    """
    return 0.001 + 0.0005 * np.sin(t / 10)  # Average 0.1% per day with fluctuation

visualize_integration(daily_return, 0, 252, n=50)
print("\nInterpretation: The area under the daily return curve")
print("is the TOTAL return over the year!")