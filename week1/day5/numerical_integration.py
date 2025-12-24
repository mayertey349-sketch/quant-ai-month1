"""
Day 5: Numerical Integration Methods
Building tools to integrate any function
"""

import numpy as np
import matplotlib.pyplot as plt

class NumericalIntegrator:
    """
    A toolkit for numerical integration.
    Implements multiple methods with increasing accuracy.
    """
    
    def __init__(self, f, a, b):
        """
        Parameters:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        """
        self.f = f
        self.a = a
        self.b = b
    
    def riemann_left(self, n=1000):
        """
        Left Riemann sum: use left endpoint of each rectangle.
        """
        dx = (self.b - self.a) / n
        x_points = np.linspace(self.a, self.b - dx, n)
        total = sum(self.f(x) * dx for x in x_points)
        return total
    
    def riemann_right(self, n=1000):
        """
        Right Riemann sum: use right endpoint of each rectangle.
        """
        dx = (self.b - self.a) / n
        x_points = np.linspace(self.a + dx, self.b, n)
        total = sum(self.f(x) * dx for x in x_points)
        return total
    
    def riemann_midpoint(self, n=1000):
        """
        Midpoint Riemann sum: use midpoint of each rectangle.
        More accurate than left/right.
        """
        dx = (self.b - self.a) / n
        x_points = np.linspace(self.a + dx/2, self.b - dx/2, n)
        total = sum(self.f(x) * dx for x in x_points)
        return total
    
    def trapezoidal(self, n=1000):
        """
        Trapezoidal rule: approximate with trapezoids instead of rectangles.
        Formula: (b-a) * [f(a) + 2*f(x₁) + 2*f(x₂) + ... + f(b)] / (2n)
        """
        x = np.linspace(self.a, self.b, n+1)
        y = np.array([self.f(xi) for xi in x])
        dx = (self.b - self.a) / n
        
        # Trapezoidal: first + last + 2*(everything in between)
        total = (y[0] + y[-1] + 2 * np.sum(y[1:-1])) * dx / 2
        return total
    
    def simpsons(self, n=1000):
        """
        Simpson's rule: approximate with parabolas.
        Most accurate of the simple methods.
        Note: n must be even
        """
        if n % 2 == 1:
            n += 1  # Make it even
        
        x = np.linspace(self.a, self.b, n+1)
        y = np.array([self.f(xi) for xi in x])
        dx = (self.b - self.a) / n
        
        # Simpson's: f(x₀) + 4*f(x₁) + 2*f(x₂) + 4*f(x₃) + ... + f(xₙ)
        total = (y[0] + y[-1] +  4 * np.sum(y[1:-1:2]) + 2 * np.sum(y[2:-2:2])) * dx / 3  
        return total
    
    def compare_methods(self, true_value=None, n=1000):
        """
        Compare all methods and show accuracy.
        """
        left = self.riemann_left(n)
        right = self.riemann_right(n)
        midpoint = self.riemann_midpoint(n)
        trap = self.trapezoidal(n)
        simp = self.simpsons(n)
        
        print("\n" + "="*70)
        print(f"COMPARING INTEGRATION METHODS (n={n})")
        print("="*70)
        print(f"Left Riemann:     {left:.10f}")
        print(f"Right Riemann:    {right:.10f}")
        print(f"Midpoint Riemann: {midpoint:.10f}")
        print(f"Trapezoidal:      {trap:.10f}")
        print(f"Simpson's:        {simp:.10f}")
        
        if true_value is not None:
            print(f"\nTrue Value:       {true_value:.10f}")
            print("\nErrors:")
            print(f"Left:     {abs(left - true_value):.10e}")
            print(f"Right:    {abs(right - true_value):.10e}")
            print(f"Midpoint: {abs(midpoint - true_value):.10e}")
            print(f"Trapezoid: {abs(trap - true_value):.10e}")
            print(f"Simpson's: {abs(simp - true_value):.10e}")
            print("\nNotice: Simpson's is usually most accurate!")
        print("="*70)
        
        return {
            'left': left,
            'right': right,
            'midpoint': midpoint,
            'trapezoidal': trap,
            'simpsons': simp
        }


# TEST 1: ∫₀¹ x² dx = 1/3
print("TEST 1: ∫₀¹ x² dx")
print("Known exact value: 1/3 = 0.333333...")

def f1(x):
    return x**2

integrator1 = NumericalIntegrator(f1, 0, 1)
results1 = integrator1.compare_methods(true_value=1/3, n=100)


# TEST 2: ∫₀² (2x + 1) dx = 6
print("\n\nTEST 2: ∫₀² (2x + 1) dx")
print("Known exact value: [x² + x]₀² = 4 + 2 = 6")

def f2(x):
    return 2*x + 1

integrator2 = NumericalIntegrator(f2, 0, 2)
results2 = integrator2.compare_methods(true_value=6, n=100)


# TEST 3: ∫₀ᵖⁱ sin(x) dx = 2
print("\n\nTEST 3: ∫₀ᵖⁱ sin(x) dx")
print("Known exact value: [-cos(x)]₀ᵖⁱ = -cos(π) + cos(0) = 1 + 1 = 2")

def f3(x):
    return np.sin(x)

integrator3 = NumericalIntegrator(f3, 0, np.pi)
results3 = integrator3.compare_methods(true_value=2, n=100)


# VERIFY: All methods converge as n increases
print("\n\nCONVERGENCE TEST: How does accuracy improve with more points?")

def test_convergence():
    """Test how error decreases as n increases."""
    
    f = lambda x: x**2
    true_value = 1/3
    
    n_values = [10, 50, 100, 500, 1000, 5000]
    errors_trap = []
    errors_simp = []
    
    for n in n_values:
        integrator = NumericalIntegrator(f, 0, 1)
        trap = integrator.trapezoidal(n)
        simp = integrator.simpsons(n)
        
        errors_trap.append(abs(trap - true_value))
        errors_simp.append(abs(simp - true_value))
    
    # Plot convergence
    plt.figure(figsize=(12, 6))
    plt.plot(n_values, errors_trap, 'bo-', linewidth=2, markersize=8, label='Trapezoidal')
    plt.plot(n_values, errors_simp, 'ro-', linewidth=2, markersize=8, label="Simpson's")
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Number of Points (n)', fontsize=12)
    plt.ylabel('Absolute Error (log scale)', fontsize=12)
    plt.title('Integration Error vs Number of Points\n(More points = Better accuracy)', 
             fontsize=14, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('week1/day5/convergence_test.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("Notice: Error decreases as n increases (downward slope)")
    print("Simpson's method is more accurate (lower on graph)")

test_convergence()