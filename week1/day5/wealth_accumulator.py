"""
Day 5: Integration Applied to Wealth Accumulation
Daily returns → Cumulative wealth (this is integration!)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

class WealthAccumulator:
    """
    Calculate wealth accumulation from returns.
    Shows discrete vs continuous compounding.
    """
    
    def __init__(self, initial_capital):
        self.initial_capital = initial_capital
    
    def discrete_compounding(self, returns):
        """
        Discrete compounding: V(t+1) = V(t) x (1 + r(t))
        This is what actually happens in markets.
        """
        wealth = np.array([self.initial_capital])
        
        for r in returns:
            new_wealth = wealth[-1] * (1 + r)
            wealth= np.append(wealth,new_wealth)
            
        return wealth
    
    def continuous_compounding(self, returns):
        """
        Continuous compounding: V(t) = V(0) x exp(∫r(t)dt)
        This is the mathematical ideal (integration!).
        """
        # Convert returns to log returns
        log_returns = np.log(1 + returns)
        
        # Cumulative sum of log returns = integral
        cumulative_log_returns = np.cumsum(log_returns)
        
        # Wealth = initial × exp(cumulative log returns)
        wealth = self.initial_capital * np.exp(cumulative_log_returns)
        
        # Prepend initial capital
        wealth = np.insert(wealth, 0, self.initial_capital)
        
        return wealth
    
    def compare_methods(self, returns):
        """
        Compare discrete vs continuous compounding.
        """
        discrete = self.discrete_compounding(returns)
        continuous = self.continuous_compounding(returns)
        
        # Plot
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Plot 1: Both methods
        ax1.plot(discrete, 'b-', linewidth=2, label='Discrete Compounding (Reality)', alpha=0.7)
        ax1.plot(continuous, 'r--', linewidth=2, label='Continuous Compounding (Mathematical)', alpha=0.7)
        ax1.set_title('Wealth Accumulation: Discrete vs Continuous Compounding',  fontsize=14, fontweight='bold')
        ax1.set_xlabel('Days')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Difference between methods
        difference = discrete - continuous
        ax2.plot(difference, 'g-', linewidth=2)
        ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
        ax2.set_title('Difference Between Methods', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Days')
        ax2.set_ylabel('Difference ($)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('week1/day5/compounding_comparison.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("\n" + "="*70)
        print("COMPOUNDING COMPARISON")
        print("="*70)
        print(f"Initial Capital: ${self.initial_capital:,.2f}")
        print(f"\nAfter {len(returns)} days:")
        print(f"Discrete Compounding:   ${discrete[-1]:,.2f}")
        print(f"Continuous Compounding: ${continuous[-1]:,.2f}")
        print(f"Difference:             ${abs(discrete[-1] - continuous[-1]):,.2f}")
        print(f"Percentage Difference:  {abs(discrete[-1] - continuous[-1])/discrete[-1]*100:.4f}%")
        print("\nNotice: They're very close! For small returns, both methods similar.")
        print("="*70)


# EXAMPLE: Simulate trading for 1 year
print("SIMULATING 1 YEAR OF TRADING")
print("Scenario: Average 0.1% daily return with volatility")

np.random.seed(42)  # Reproducible results

# Generate returns: mean 0.1% per day, std dev 1.5%
num_days = 252  # Trading days in a year
mean_return = 0.001  # 0.1% per day
volatility = 0.015   # 1.5% daily volatility

returns = np.random.normal(mean_return, volatility, num_days)

# Calculate wealth accumulation
accumulator = WealthAccumulator(initial_capital=10000)
accumulator.compare_methods(returns)


# REAL MARKET DATA EXAMPLE
print("\n\nREAL MARKET DATA: Apple Stock (2023)")

# Download AAPL data
aapl = yf.download('AAPL', start='2023-01-01', end='2024-01-01', progress=False)

if aapl is None:
   raise ValueError(f"Failed to download data for AAPL")

aapl_returns = aapl['Close'].pct_change().dropna().values

# If you invested $10,000 in AAPL on Jan 1, 2023:
accumulator_aapl = WealthAccumulator(initial_capital=10000)
accumulator_aapl.compare_methods(aapl_returns)


# THE INTEGRATION CONNECTION
print("\n" + "="*70)
print("THE INTEGRATION CONNECTION")
print("="*70)
print("Daily returns r(t) are like the DERIVATIVE of wealth")
print("  → Returns tell you the RATE OF CHANGE of wealth")
print()
print("Cumulative wealth W(t) is the INTEGRAL of returns")
print("  → Wealth = ∫ r(t) dt (in continuous case)")
print("  → Wealth = ∏ (1 + r(t)) (in discrete case)")
print()
print("This is the Fundamental Theorem of Calculus in finance!")
print("  → Derivatives and integrals are inverse operations")
print("  → Rate of change ↔ Accumulation")
print("  → Returns ↔ Wealth")
print("="*70)


# ADVANCED: Calculate average return needed to reach goal
def calculate_required_return(initial, target, num_days):
    """
    If you want to grow from initial to target in num_days,
    what average daily return do you need?
    
    This is an integration problem solved backwards!
    """
    # Target = Initial × (1 + r)^days
    # Solving for r:
    required_return = (target / initial) ** (1 / num_days) - 1
    
    print("\n" + "="*70)
    print("GOAL PLANNING (Integration Backwards)")
    print("="*70)
    print(f"Initial capital: ${initial:,.2f}")
    print(f"Target wealth:   ${target:,.2f}")
    print(f"Time horizon:    {num_days} days")
    print(f"\nRequired average daily return: {required_return*100:.4f}%")
    print(f"Annualized return needed:      {(1 + required_return)**252 - 1:.2%}")
    print("="*70)

# Example: Turn $10,000 into $1,000,000 in 10 years
calculate_required_return(
    initial=10000,
    target=1000000,
    num_days=252 * 10  # 10 years of trading
)

# Your billionaire goal
calculate_required_return(
    initial=10000,
    target=1000000000,  # $1 billion
    num_days=252 * 20   # 20 years
)