"""
Day 4: Complete Stock Comparison Tool
Synthesizing: OOP, NumPy, Pandas, Matplotlib, Calculus concepts
"""
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
class StockComparison:
    """Comparing two stocks across multiple dimensions.
    """
    def __init__(self, ticker1 , ticker2, start_date, end_date):
        self.ticker1 = ticker1
        self.ticker2 = ticker2
        
        if start_date is None:
            start_date = date(date.today().year,1,1)
        if end_date is None:
            end_date = date.today()
            
        self.start_date = start_date
        self.end_date = end_date
        self.data1 = None
        self.data2 = None
        self.returns1 = None
        self.returns2 = None
        
    def download_data(self):
        """Downloading Data for both stocks"""
        print(f"Downloading {self.ticker1} and {self.ticker2}...")
        self.data1 = yf.download(self.ticker1, start=self.start_date, end=self.end_date, progress=False)
        if self.data1 is None or self.data1.empty:
           raise ValueError(f"Failed to download data for {self.ticker1}")
             
        self.data2 = yf.download(self.ticker2, start=self.start_date, end=self.end_date, progress=False)
        if self.data2 is None or self.data2.empty:
            raise ValueError(f"Failed to download data for {self.ticker2}")
            
        self.returns1 = self.data1['Close'].pct_change().dropna()
        self.returns2 = self.data2['Close'].pct_change().dropna()
        
        print(f"Download Complete!")
        
    def calculate_max_drawdown(self, prices):
        """
        Calculate maximum drawdown (largest peak-to-trough decline).
        This uses calculus concepts - finding maximum decline.
        """
        # Calculate running maximum
        running_max = prices.expanding().max()
        
        # Calculate drawdown at each point
        drawdown = (prices - running_max) / running_max
        
        # Return maximum drawdown (most negative)
        return drawdown.min() * 100
      
      
    def compare_statistics(self):
        """Calculate and compare statistics."""
        if self.data1 is None or self.data1.empty:
            raise ValueError(f"Failed to download data for {self.ticker1}")
            
        if self.data2 is None or self.data2.empty:
           raise ValueError(f"Failed to download data for {self.ticker2}")
        
        if self.returns1 is None or self.returns1.empty:
            print("Error: No returns data available. Call calculate_returns() first.")
            return None
        
        if self.returns2 is None or self.returns2.empty:
            print("Error: No returns data available. Call calculate_returns() first.")
            return None
        
        stats = pd.DataFrame({
            self.ticker1: {
                'Total Return': (self.data1['Close'].iloc[-1] / self.data1['Close'].iloc[0] - 1) * 100,
                'Annual Return': self.returns1.mean() * 252 * 100,
                'Annual Volatility': self.returns1.std() * np.sqrt(252) * 100,
                'Sharpe Ratio': (self.returns1.mean() * 252) / (self.returns1.std() * np.sqrt(252)),
                'Max Drawdown': self.calculate_max_drawdown(self.data1['Close']),
                'Best Day': self.returns1.max() * 100,
                'Worst Day': self.returns1.min() * 100
            },
            self.ticker2: {
                'Total Return': (self.data2['Close'].iloc[-1] / 
                               self.data2['Close'].iloc[0] - 1) * 100,
                'Annual Return': self.returns2.mean() * 252 * 100,
                'Annual Volatility': self.returns2.std() * np.sqrt(252) * 100,
                'Sharpe Ratio': (self.returns2.mean() * 252) / 
                              (self.returns2.std() * np.sqrt(252)),
                'Max Drawdown': self.calculate_max_drawdown(self.data2['Close']),
                'Best Day': self.returns2.max() * 100,
                'Worst Day': self.returns2.min() * 100
            }
        }).T
        
        aligned = pd.concat([self.returns1, self.returns2], axis=1).dropna()

        # Calculate correlation
        correlation = aligned.corr().iloc[0, 1]
        
        print("\n" + "="*70)
        print("COMPARISON STATISTICS")
        print("="*70)
        print(stats.to_string())
        print(f"\nCorrelation: {correlation:.3f}")
        print("="*70)
        
        return stats, correlation
    
    
    def plot_comparison(self):
        """Create comprehensive comparison visualization."""
        if self.data1 is None or self.data1.empty:
           raise ValueError(f"Failed to download data for {self.ticker1}")
     
        if self.data2 is None or self.data2.empty:
           raise ValueError(f"Failed to download data for {self.ticker2}")
            
        if self.returns1 is None or self.returns1.empty:
            print("Error: No returns data available. Call calculate_returns() first.")
            return None
        
        if self.returns2 is None or self.returns2.empty:
            print("Error: No returns data available. Call calculate_returns() first.")
            return None
        
        aligned = pd.concat([self.returns1, self.returns2], axis=1).dropna()
        aligned.columns = [self.ticker1, self.ticker2]
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Plot 1: Normalized prices
        norm1 = (self.data1['Close'] / self.data1['Close'].iloc[0]) * 100
        norm2 = (self.data2['Close'] / self.data2['Close'].iloc[0]) * 100
        
        axes[0, 0].plot(norm1.index, norm1, label=self.ticker1, linewidth=2)
        axes[0, 0].plot(norm2.index, norm2, label=self.ticker2, linewidth=2)
        axes[0, 0].axhline(y=100, color='black', linestyle='--', alpha=0.3)
        axes[0, 0].set_title('Normalized Price Performance (Base = 100)',   fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Normalized Price')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Returns distribution
        axes[1, 0].scatter(aligned[self.ticker1] * 100, aligned[self.ticker2] * 100, alpha=0.5)
        axes[1, 0].set_title(f'Returns Correlation: {aligned.corr().iloc[0, 1]:.3f}', fontsize=12, fontweight='bold') 
        axes[1, 0].set_xlabel(f'{self.ticker1} Return (%)')
        axes[1, 0].set_ylabel(f'{self.ticker2} Return (%)') 
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 3: Scatter plot (correlation)
        
        axes[1, 0].scatter(self.returns1 * 100, self.returns2 * 100, alpha=0.5)
        axes[1, 0].set_title(f'Returns Correlation: {self.returns1.corr(self.returns2):.3f}', fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel(f'{self.ticker1} Return (%)')
        axes[1, 0].set_ylabel(f'{self.ticker2} Return (%)')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Add regression line
        z = np.polyfit(aligned.iloc[:,0], aligned.iloc[:,1], 1)
        p = np.poly1d(z)
        x_line = np.linspace(aligned.iloc[:,0].min(), aligned.iloc[:,0].max(), 100)
        axes[1, 0].plot(x_line * 100, p(x_line) * 100, "r--", linewidth=2)

        # Plot 4: Cumulative returns
        cumulative1 = (1 + self.returns1).cumprod() - 1
        cumulative2 = (1 + self.returns2).cumprod() - 1

        axes[1, 1].plot(cumulative1.index, cumulative1 * 100, label=self.ticker1, linewidth=2)
        axes[1, 1].plot(cumulative2.index, cumulative2 * 100, label=self.ticker2, linewidth=2)
        axes[1, 1].axhline(y=0, color='black', linestyle='--', alpha=0.3)
        axes[1, 1].set_title('Cumulative Returns', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Date')
        axes[1, 1].set_ylabel('Cumulative Return (%)')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('week1/day4/complete_comparison.png', dpi=150, bbox_inches='tight')
        plt.show()
        
        print("\nVisualization saved!")


# TEST THE COMPLETE SYSTEM
if __name__ == "__main__":
    # Compare Apple vs Microsoft
    comparison = StockComparison(
        ticker1='AAPL',
        ticker2='MSFT',
        start_date='2023-01-01',
        end_date='2024-01-01'
    )
    
    comparison.download_data()
    comparison.compare_statistics()
    comparison.plot_comparison()
    
    print("\n✅ Day 4 project complete!")
    print("You've now built a professional-grade comparison tool!")