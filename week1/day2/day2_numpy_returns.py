"""
Day 2: Stock Returns with NumPy
Practicing array operations with financial data
"""
import numpy as np 

# Stock prices over 10 days
prices = np.array([100, 102, 101, 105, 103, 107, 106, 110, 108, 112])
print(f"Stock Prices over 10 days:", prices)

#calculate daily returns
# daily return = (current_price - previous_price) / previous_price
daily_returns = (prices[1:] - prices[:-1]) / prices[:-1]
print(f"Daily Returns:", daily_returns)

#Calculate Statistics
mean_returns = np.mean(daily_returns)
std_returns = np.std(daily_returns)
min_return = np.min(daily_returns)
max_returns = np.max(daily_returns)

print(f"Statistics of Daily Returns:")
print(f"Mean Return: {mean_returns:.4f} ({mean_returns*100:.2f}%)")
print(f"Standard Deviation: {std_returns:.4f} ({std_returns*100:.2f}%)")
print(f"Minimum Return: {min_return:.4f} ({min_return*100:.2f}%)")
print(f"Maximum Return: {max_returns:.4f} ({max_returns*100:.2f}%)")


#Annualized Return and Volatility
trading_days = 252  # Typical number of trading days in a year
annual_return = mean_returns * trading_days
annual_volatility = std_returns * np.sqrt(trading_days)

print(f"Annualized return:")
print(f"Expected Annual Return: {annual_return:.2%} ")
print(f"Annual Volatility: {annual_volatility:.2%} ")

# Sharpe Ratio (simplified, assuming risk-free rate = 0)
sharpe_ratio = annual_return / annual_volatility
print(f"Sharpe Ratio: {sharpe_ratio:.3f} ")

# Portfolio with 4 stocks
print("="*50)
print("PORTFOLIO CALCULATION")
print("="*50)

# Returns for 4 stocks
stock1_returns = np.array([0.02, 0.01, 0.03, -0.01, 0.02])
stock2_returns = np.array([0.01, 0.02, 0.01, 0.02, 0.01])
stock3_returns = np.array([0.03, -0.01, 0.02, 0.01, 0.03])
stock4_returns = np.array([-0.01, 0.03, 0.01, 0.02, -0.02])

# Portfolio weights
weights = np.array([0.25, 0.25, 0.25, 0.25]) # Equal weights for 4 stocks

print(f"Weights of the portfolio: {weights}")
print(f"Weights sum to: {np.sum(weights)}")

# Calculate portfolio return for each period
# For each day, weighted sum of returns
portfolio_returns = (
    weights[0] * stock1_returns +
    weights[1] * stock2_returns +
    weights[2] * stock3_returns +
    weights[3] * stock4_returns
)

print(f"Portfolio Returns: {portfolio_returns}")

# Portfolio statistics
portfolio_mean_r = np.mean(portfolio_returns)
portfoli0_volatility = np.std(portfolio_returns)

print(f"Portfolio Mean Return: {portfolio_mean_r:.4f} ")
print(f"Portfolio Volatility: {portfoli0_volatility:.4f} ")
