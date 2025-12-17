"""
Day 2: Numerical Derivative Calculator
Verifies our calculus understanding through code
"""
def derivative(f,x,h=0.0001):
    """
    Calculate the numerical derivative of a function f at point x using the definition of derivative.
    
    Parameters:
    f : function
        The function for which to calculate the derivative.
    x : float
        The point at which to calculate the derivative.
    h : float, optional
        A small value to approximate the limit (default is 0.0001).
        
    Returns:
    float
        The numerical derivative of f at point x.
    """
    return (f(x + h) - f(x)) / h


# Test 1: f(x) = x²
# We know analytically: f'(x) = 2x
# So f'(3) should be 2(3) = 6

def f1(x):
    return x**2

numerical_result = derivative(f1,3)
analytical_result = 2*3

print(f"Test 1: f(x) =x² ")
print(f"Numerical f'(3) = {numerical_result:.6f}")
print(f"Analytical results = {analytical_result}")
print(f"Error: {abs(numerical_result - analytical_result):.8f}\n")


# Test 2: f(x) = x³
# Analytical: f'(x) = 3x²
# At x=2: f'(2) = 3(4) = 12

def f2(x):
    return x**3

numerical_result = derivative(f2,2)
analitical_result = 3*(2**2)

print(f"Test 2: f(x) =x³ ")
print(f"Numerical f'(2) = {numerical_result:.6f}")
print(f"Analytical results = {analytical_result}")
print(f"Error: {abs(numerical_result - analytical_result):.8f}\n")


# Test 3: Stock price example from earlier
# P(t) = 100 + 10t - 0.5t²
# P'(t) = 10 - t

def StockPrice(t):
    return 100 + 10*t + 0.5*t**2

print("Test 3: Stock Price P(t) = 100 + 10t - 0.5t²")
days = [0, 5, 10, 15]

for day in days:
    numerical_result= derivative(StockPrice,day)
    analitical_result = 10 - day
    print(f"Day {day}: Rate of change = {numerical_result:.4f}, analytical = {analitical_result}")
    

# Portfolio value: V(t) = 1000 + 200t - 5t²
# Code it, test at t = 10 and t = 20

def PortfolioValue(t):
    return 1000 + 200*t - 5*t**2

print("\nTest 4: Portfolio Value V(t) = 1000 + 200t - 5t²")
time = [10, 20]

for t in time:
    numerical_result = derivative(PortfolioValue,t)
    analytical_result = 200 - 10*t
    print(f"Time {t}: Rate of change = {numerical_result:.4f}, analytical = {analytical_result}")

