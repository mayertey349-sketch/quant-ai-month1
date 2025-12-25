"""
Day 3: Calculus Applied to Real Stock Data
Connecting derivatives to actual market behavior
"""
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Download Historical Apple Stock data
print(f"Downloading AAPL data...")
aapl = yf.download('AAPL', start='2023-01-01', end='2024-01-01', progress=False)
if aapl is None or aapl.empty:
    print("Error: Failed to download data")
    exit(1)

#Calculate the returns(descrete derivative)
aapl['Returns'] = aapl['Close'].pct_change()

#Calculate Moving Average (smoothed price)
aapl['MA_50'] = aapl['Close'].rolling(window=50).mean()

# Visualize
fig , axes = plt.subplots(3,1, figsize=(14,12))

# Plot1 Price over time
axes[0].plot(aapl.index, aapl['Close'] , label='AAPL Price' , color='blue' , linewidth=1.5)
axes[0].plot(aapl.index, aapl['MA_50'], label='50-Day MA', color='red', linewidth=2)
axes[0].set_title('AAPL Stock Price - 2023', fontsize=14 , fontweight='bold')
axes[0].set_ylabel('Price (USD)', fontsize=12)
axes[0].legend()
axes[0].grid(True , alpha=0.3)

# Plot2 : Daily Returns (This is like the derivative)
axes[1].plot(aapl.index, aapl['Returns'], label='Daily Returns', color='green', alpha=0.7)
axes[1].axhline(y=0, color='black', linestyle='--', linewidth=1)
axes[1].fill_between(aapl.index, aapl['Returns'], 0, where=(aapl['Returns'] > 0), color='green', alpha=0.3)
axes[1].fill_between(aapl.index, aapl['Returns'], 0, where=(aapl['Returns'] < 0), color='red', alpha=0.3)
axes[1].set_title('Daily Returns of AAPL Stocks, (Discrete Derivative of Price)', fontsize=14 , fontweight='bold')
axes[1].set_ylabel('Returns', fontsize=12)
axes[1].legend()
axes[1].grid(True , alpha=0.3)

# Plot3 : Comulative Returns (Integral of Returns)
cumulative_returns = (1 +aapl['Returns']).cumprod() - 1
axes[2].plot(aapl.index, cumulative_returns, label='Cumulative Returns', color='purple', linewidth=2)
axes[2].axhline(y=0, color='black', linestyle='--', linewidth=1)
axes[2].fill_between(aapl.index, cumulative_returns, 0, color='purple', alpha=0.3)
axes[2].set_title('Cumulative Returns of AAPL Stocks (Integral of Daily Returns)', fontsize=14 , fontweight='bold')
axes[2].set_ylabel('Cumulative Returns', fontsize=12)
axes[2].set_xlabel('Date', fontsize=12)
axes[2].legend()
axes[2].grid(True , alpha=0.3)

plt.tight_layout()
plt.savefig(r'week1\day3\day3_aapl_stock_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("Plot saved as 'week1/day3/day3_aapl_stock_analysis.png'")

# Statistics
print("\n" + "="*60)
print("AAPL STATISTICS - 2023")
print("="*60)
print(f"Starting Price: ${aapl['Close'].iloc[0]:.2f}")
print(f"Ending Price: ${aapl['Close'].iloc[-1]:.2f}")
print(f"Total Return: {(aapl['Close'].iloc[-1]/aapl['Close'].iloc[0] - 1)*100:.2f}%")
print()
print(f"Average Daily Return: {aapl['Returns'].mean():.4f} ({aapl['Returns'].mean()*100:.2f}%)")
print(f"Daily Volatility: {aapl['Returns'].std():.4f} ({aapl['Returns'].std()*100:.2f}%)")
print()
print(f"Annualized Return: {aapl['Returns'].mean()*252*100:.2f}%")
print(f"Annualized Volatility: {aapl['Returns'].std()*np.sqrt(252)*100:.2f}%")
print()
print(f"Best Day: {aapl['Returns'].max()*100:.2f}%")
print(f"Worst Day: {aapl['Returns'].min()*100:.2f}%")
print("="*60)

# THE CALCULUS CONNECTION
print("\n" + "="*60)
print("THE CALCULUS CONNECTION")
print("="*60)
print("PRICE → RETURNS is like taking a DERIVATIVE")
print("  • Price = position")
print("  • Returns = velocity (rate of change of position)")
print()
print("RETURNS → CUMULATIVE RETURNS is like taking an INTEGRAL")
print("  • Daily returns = velocity at each moment")
print("  • Cumulative return = total distance traveled")
print()
print("This is the Fundamental Theorem of Calculus in action!")
print("  Differentiation and integration are inverse operations")
print("="*60)
