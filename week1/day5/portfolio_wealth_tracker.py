"""
Day 5 Capstone: Complete Wealth Accumulation Tracker
Combines: OOP, NumPy, Pandas, Integration, Visualization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
from datetime import datetime

class PortfolioWealthTracker:
    """
    Track wealth accumulation for a portfolio over time.
    Uses integration concepts to calculate cumulative returns.
    """
    
    def __init__(self, tickers, weights, initial_capital, start_date= None, end_date=None):
        """
        Parameters:
        tickers (list): Stock symbols
        weights (list): Portfolio weights (must sum to 1)
        initial_capital (float): Starting amount
        start_date (str): 'YYYY-MM-DD'
        end_date (str): 'YYYY-MM-DD'
        """
        self.tickers = list(tickers)
        self.weights = np.array(weights)
        self.initial_capital = initial_capital
        if start_date is None:
            start_date = date(date.today().year, 1, 1)
        if end_date is None:
            end_date = date.today()
        self.start_date = start_date
        self.end_date = end_date
        
        # Validate weights
        assert np.isclose(self.weights.sum(), 1.0), "Weights must sum to 1"
        
        self.data = None
        self.returns = None
        self.portfolio_returns = None
        self.wealth_history = None
    
    def download_data(self):
        """Download price data for all stocks."""
        print(f"Downloading data for {len(self.tickers)} stocks...")
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date, progress=False)
        if data is None or data.empty:
           raise ValueError(f"Failed to download data for {self.tickers}")
       
        #Extract closing prices
        # If multiple tickers, this would create a DataFrame with columns for each
        self.data = data['Close']
        
        print(f"Downloaded {len(self.data)} days of data")
        return self.data
    
    def calculate_portfolio_returns(self):
        """Calculate portfolio returns (weighted average of stock returns)."""
        if self.data is None or self.data.empty:
            raise ValueError(f"Failed to download data for {self.tickers}") 
        
        # Individual stock returns
        self.returns = self.data.pct_change().dropna()
        
        # Portfolio returns = weighted sum
        self.portfolio_returns = np.dot(self.returns,self.weights)
       
        return self.portfolio_returns
    
    def calculate_wealth_history(self):
        """
        Calculate wealth over time.
        This is the INTEGRAL of returns!
        """
        if self.data is None or self.data.empty:
            raise ValueError(f"Failed to download data for {self.tickers}")
         
        if self.portfolio_returns is None or self.portfolio_returns.empty:
            raise ValueError(f"Failed to download data for {self.tickers}") 
        
        # Discrete compounding: W(t) = W(0) × ∏(1 + r(t))
        wealth = np.array([self.initial_capital])
        
        for r in self.portfolio_returns:
            new_wealth = wealth[-1] * (1 + r)
            wealth = np.append(wealth, new_wealth)
        
        # Create DataFrame
        dates = [self.data.index[0]] + list(self.portfolio_returns.index)
        
        self.wealth_history = pd.DataFrame({
            'Date': dates,
            'Wealth': wealth
        }).set_index('Date')
        
        return self.wealth_history
    
    def calculate_metrics(self):
        """Calculate performance metrics."""
        if self.portfolio_returns is None:
            raise ValueError(f"Failed to download data for {self.tickers}")
        
        if self.wealth_history is None or self.wealth_history.empty:
            raise ValueError(f"Failed to download data for {self.tickers}")
        
        final_wealth = self.wealth_history['Wealth'].iloc[-1]
        total_return = (final_wealth / self.initial_capital - 1) * 100
        
        # Calculate annual metrics
        num_days = len(self.portfolio_returns)
        num_years = num_days / 252
        
        annual_return = (final_wealth / self.initial_capital) ** (1/num_years) - 1
        annual_volatility = self.portfolio_returns.std() * np.sqrt(252)
        sharpe_ratio = annual_return / annual_volatility if annual_volatility > 0 else 0
        
        # Maximum drawdown
        cumulative_max = self.wealth_history['Wealth'].expanding().max()
        drawdown = (self.wealth_history['Wealth'] - cumulative_max) / cumulative_max
        max_drawdown = drawdown.min()
        
        metrics = {
            'Initial Capital': self.initial_capital,
            'Final Wealth': final_wealth,
            'Total Return': total_return,
            'Annual Return': annual_return * 100,
            'Annual Volatility': annual_volatility * 100,
            'Sharpe Ratio': sharpe_ratio,
            'Max Drawdown': max_drawdown * 100,
            'Best Day': self.portfolio_returns.max() * 100,
            'Worst Day': self.portfolio_returns.min() * 100,
            'Days Traded': num_days
        }
        
        return metrics
    
    def plot_wealth_accumulation(self):
        """
        Visualize wealth accumulation over time.
        This is visualizing the INTEGRAL of returns.
        """
        if self.wealth_history is None:
            raise ValueError(f"Failed to download data for {self.tickers}")
        
        if self.portfolio_returns is None:
            raise ValueError(f"Failed to download data for {self.tickers}")
        
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # PLOT 1: Wealth over time
        axes[0].plot(self.wealth_history.index, self.wealth_history['Wealth'], 'b-', linewidth=2)
        axes[0].axhline(y=self.initial_capital, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Initial Capital')
        axes[0].fill_between(self.wealth_history.index,  self.initial_capital, self.wealth_history['Wealth'], where=(self.wealth_history['Wealth'] >= self.initial_capital),color='green', alpha=0.3, label='Profit')
        axes[0].fill_between(self.wealth_history.index, self.initial_capital, self.wealth_history['Wealth'], where=(self.wealth_history['Wealth'] < self.initial_capital),color='red', alpha=0.3, label='Loss')
        axes[0].set_title('Portfolio Wealth Over Time (Integration of Returns)', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Wealth ($)', fontsize=12)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # PLOT 2: Daily returns (this is like the derivative)
        axes[1].plot(self.portfolio_returns.index, self.portfolio_returns * 100,  'g-', linewidth=1, alpha=0.7)
        axes[1].axhline(y=0, color='black', linestyle='--', linewidth=1)
        axes[1].fill_between(self.portfolio_returns.index, 0, self.portfolio_returns * 100, where=(self.portfolio_returns > 0), color='green', alpha=0.3)
        axes[1].fill_between(self.portfolio_returns.index, 0, self.portfolio_returns * 100, where=(self.portfolio_returns < 0), color='red', alpha=0.3)
        axes[1].set_title('Daily Portfolio Returns (Derivative of Wealth)', fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Return (%)', fontsize=12)
        axes[1].grid(True, alpha=0.3)
        
        # PLOT 3: Drawdown
        cumulative_max = self.wealth_history['Wealth'].expanding().max()
        drawdown = (self.wealth_history['Wealth'] - cumulative_max) / cumulative_max * 100
        
        axes[2].fill_between(drawdown.index, 0, drawdown, color='red', alpha=0.5)
        axes[2].plot(drawdown.index, drawdown, 'r-', linewidth=1)
        axes[2].set_title('Portfolio Drawdown (Peak-to-Trough Decline)',  fontsize=14, fontweight='bold')
        axes[2].set_xlabel('Date', fontsize=12)
        axes[2].set_ylabel('Drawdown (%)', fontsize=12)
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('week1/day5/portfolio_wealth_tracker.png', dpi=150, bbox_inches='tight')
        plt.show()
    
    def generate_report(self):
        """Generate comprehensive performance report."""
        metrics = self.calculate_metrics()
        
        print("\n" + "="*70)
        print("PORTFOLIO PERFORMANCE REPORT")
        print("="*70)
        print(f"\nPortfolio Composition:")
        for ticker, weight in zip(self.tickers, self.weights):
            print(f"  {ticker}: {weight*100:.1f}%")
        
        print(f"\nPeriod: {self.start_date} to {self.end_date}")
        print(f"Days Traded: {metrics['Days Traded']}")
        
        print(f"\n{'Wealth Accumulation:':<30}")
        print(f"  {'Initial Capital:':<28} ${metrics['Initial Capital']:>12,.2f}")
        print(f"  {'Final Wealth:':<28} ${metrics['Final Wealth']:>12,.2f}")
        print(f"  {'Total Return:':<28} {metrics['Total Return']:>11.2f}%")
        
        print(f"\n{'Risk-Adjusted Performance:':<30}")
        print(f"  {'Annual Return:':<28} {metrics['Annual Return']:>11.2f}%")
        print(f"  {'Annual Volatility:':<28} {metrics['Annual Volatility']:>11.2f}%")
        print(f"  {'Sharpe Ratio:':<28} {metrics['Sharpe Ratio']:>12.3f}")
        
        print(f"\n{'Risk Metrics:':<30}")
        print(f"  {'Max Drawdown:':<28} {metrics['Max Drawdown']:>11.2f}%")
        print(f"  {'Best Day:':<28} {metrics['Best Day']:>11.2f}%")
        print(f"  {'Worst Day:':<28} {metrics['Worst Day']:>11.2f}%")
        
        print("\n" + "="*70)
        print("THE INTEGRATION CONNECTION:")
        print("="*70)
        print("1. Daily Returns = Derivative of Wealth")
        print("   → Tells you: How fast is wealth changing?")
        print()
        print("2. Cumulative Wealth = Integral of Returns")
        print("   → Tells you: What's the total accumulation?")
        print()
        print("3. Fundamental Theorem of Calculus:")
        print("   → Final Wealth - Initial Wealth = ∫(returns) dt")
        print("   → Integration accumulates all the daily changes")
        print("="*70)


# EXAMPLE 1: Tech Portfolio (2023)
print("="*70)
print("EXAMPLE 1: TECH PORTFOLIO")
print("="*70)

tech_portfolio = PortfolioWealthTracker(
    tickers=['AAPL', 'MSFT', 'GOOGL', 'AMZN'],
    weights=[0.25, 0.25, 0.25, 0.25],
    initial_capital=10000,
    
)

tech_portfolio.download_data()
tech_portfolio.calculate_wealth_history()
tech_portfolio.plot_wealth_accumulation()
tech_portfolio.generate_report()


# EXAMPLE 2: Your future portfolio (simulate)
print("\n\n" + "="*70)
print("EXAMPLE 2: YOUR 4-YEAR UNIVERSITY PLAN (SIMULATED)")
print("="*70)
print("Scenario: You start with $2,000 and add $200/month")
print("Target: 25% annual return")

def simulate_contributions():
    """
    Simulate wealth accumulation with:
    - Monthly contributions
    - Target annual return
    """
    
    initial_capital = 2000
    monthly_contribution = 200
    annual_return = 0.25  # 25%
    daily_return = (1 + annual_return) ** (1/252) - 1  # Convert to daily
    
    num_days = 252 * 4  # 4 years
    wealth = [initial_capital]
    contributions = [0]
    
    for day in range(num_days):
        # Add contribution at start of each month (every ~21 trading days)
        if day % 21 == 0 and day > 0:
            contribution = monthly_contribution
        else:
            contribution = 0
        
        # Grow previous wealth + add contribution
        new_wealth = wealth[-1] * (1 + daily_return) + contribution
        wealth.append(new_wealth)
        contributions.append(contributions[-1] + contribution)
    
    # Plot
    days = np.arange(len(wealth))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Wealth accumulation
    ax1.plot(days, wealth, 'b-', linewidth=2, label='Total Wealth')
    ax1.plot(days, contributions, 'g--', linewidth=2, label='Total Contributed')
    ax1.fill_between(days, contributions, wealth, alpha=0.3, color='gold', label='Investment Gains')
    ax1.set_title('Your 4-Year Wealth Accumulation Plan',  fontsize=14, fontweight='bold')
    ax1.set_xlabel('Days')
    ax1.set_ylabel('Amount ($)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Year-by-year breakdown
    years = [0, 252, 504, 756, 1008]
    year_wealth = [wealth[i] for i in years]
    year_labels = ['Start', 'Year 1', 'Year 2', 'Year 3', 'Year 4']
    
    ax2.bar(year_labels, year_wealth, color='steelblue', alpha=0.7, edgecolor='black')
    for i, (label, value) in enumerate(zip(year_labels, year_wealth)):
        ax2.text(i, value + 500, f'${value:,.0f}',  ha='center', fontsize=11, fontweight='bold')
    ax2.set_title('Wealth by Year', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Wealth ($)')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('week1/day5/university_wealth_plan.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*70)
    print("4-YEAR PROJECTION")
    print("="*70)
    print(f"Initial Capital:        ${initial_capital:>10,.2f}")
    print(f"Monthly Contribution:   ${monthly_contribution:>10,.2f}")
    print(f"Total Contributed:      ${contributions[-1]:>10,.2f}")
    print(f"Target Annual Return:   {annual_return*100:>10.1f}%")
    print()
    print(f"Final Wealth:           ${wealth[-1]:>10,.2f}")
    print(f"Investment Gains:       ${wealth[-1] - initial_capital - contributions[-1]:>10,.2f}")
    print(f"Total Return:           {(wealth[-1]/initial_capital - 1)*100:>10.1f}%")
    print()
    print("By graduation, you'll have:")
    print(f"  - Working trading system")
    print(f"  - 4-year track record")
    print(f"  - ${wealth[-1]:,.0f} to scale with")
    print("="*70)

simulate_contributions()


# EXAMPLE 3: Path to billionaire (math check)
print("\n\n" + "="*70)
print("EXAMPLE 3: THE BILLIONAIRE MATH")
print("="*70)

def billionaire_calculator(initial, annual_return, target=1e9):
    """
    Calculate how long to reach billionaire status.
    
    Formula: target = initial x (1 + r)^years
    Solving: years = log(target/initial) / log(1 + r)
    """
    
    years = np.log(target / initial) / np.log(1 + annual_return)
    
    print(f"Starting Capital:     ${initial:>15,.2f}")
    print(f"Target:               ${target:>15,.2f}")
    print(f"Annual Return:        {annual_return*100:>14.1f}%")
    print(f"\nYears Required:       {years:>15.1f} years")
    print(f"Age when achieved:    {20 + years:>15.1f} years old")
    
    # Show year-by-year
    print(f"\nYear-by-Year Projection:")
    wealth = initial
    for year in [5, 10, 15, 20, 25, 30]:
        if year <= years:
            wealth = initial * (1 + annual_return) ** year
            print(f"  Year {year:>2}: ${wealth:>20,.2f} (Age {20+year})")
    
    return years

print("\nScenario 1: Conservative (20% annual)")
billionaire_calculator(initial=10000, annual_return=0.20)

print("\n" + "-"*70)
print("\nScenario 2: Optimistic (30% annual)")
billionaire_calculator(initial=10000, annual_return=0.30)

print("\n" + "-"*70)
print("\nScenario 3: Elite (40% annual, like Renaissance)")
billionaire_calculator(initial=10000, annual_return=0.40)

print("\n" + "="*70)
print("KEY INSIGHT:")
print("Even at 40% annual returns (Renaissance-level), it takes ~30 years")
print("from $10K to $1B. This is why starting NOW at age 20 matters.")
print("Every year of head start = millions in final wealth.")
print("="*70)
