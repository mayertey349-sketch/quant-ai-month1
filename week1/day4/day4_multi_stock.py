"""
Day 4: Multi-Stock Data Handler
Learning Pandas through financial data analysis

Goal: Build a class that handles multiple stocks at once
"""
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date

class MultiStockAnalyzer:
    """Analyze multiple stocks simultaneously
    """
    def __init__(self, tickers, start_date=None, end_date=None):
        """ If no start_date or end_date is provided, use first day of the current year and today's date.
            Initialize with a list of stock tickers.
        Parameters:
            tickers (list): A list of stock ticker symbols.
            start_date (date, str): The start date for data collection. Defaults to None.
            end_date (date, str): The end date for data collection. Defaults to None.
        """
        self.tickers = list(tickers)
        if start_date is None:
            start_date = date(date.today().year, 1, 1)
        if end_date is None:
            end_date = date.today()
        self.start_date = start_date
        self.end_date = end_date
        self.data = None
        self.returns = None
        
    def download_data(self):
        """Downloads data of all stocks
           Returns: DataFrames with columns for each stock
        """
        # Download data for multiple tickers at once
        data = yf.download(self.tickers, start=self.start_date, end=self.end_date, progress= False)
        if data is None or data.empty:
            print("Error: Failed to download data")
            exit(1)
            
        #Extract closing prices
        # If multiple tickers, this would create a DataFrame with columns for each
        self.data = data['Close'] 
        
        print(f"Downloaded {len(self.data)} days of data for {len(self.tickers)} stocks.")
        print(f"Columns: {list(self.data.columns)}")
        return self.data
    
    def calculate_returns(self):
        """Calculate Returns for all stocks
        """
        if self.data is None or self.data.empty:
            print("Error: No data available. Call download_data() first.")
            return None
        
        #ptc_change() , claculates percentage change for each column
        self.returns = self.data.pct_change()
        
        # Remove first row with NaN values from pct_change()
        self.returns = self.returns.dropna()
        return self.returns
    
    def summary_statistics(self):
        """
           Calculates summary stats for all stocks 
           Returns: DataFrame with stats for all stocks
        """
        if self.returns is None or self.returns.empty:
            print("Error: No returns data available. Call calculate_returns() first.")
            return None
        
        if self.returns is None or self.returns.empty:
            self.calculate_returns()
        
        #Create a Summary DataFrame
        summary = pd.DataFrame({
            'Mean Return': self.returns.mean(),
            'Volatility': self.returns.std(),
            'Min Return': self.returns.min(),
            'Max Return': self.returns.max(),
            'Annual Return': self.returns.mean() * 252,
            'Annual Volatility': self.returns.std() * np.sqrt(252)
        })           
        
        # Calculate Sharpe Ratio (Simplified, assuming risk-free rate = 0)
        summary['Sharpe Ratio'] = summary['Annual Return'] / summary['Annual Volatility']
        return summary
    
    def correlation_matrix(self):
        """
        Calculate correlation matrix between stocks.
        """
        if self.returns is None or self.returns.empty:
            print("Error: No returns data available. Call calculate_returns() first.")
            return None
        correlation = pd.DataFrame(self.returns).corr()
        return correlation

    def plot_normalized_prices(self):
        """
        Plot all stock prices normalized to 100.
        This shows relative performance.
        """
        if self.data is None or self.data.empty:
            print("Error: No data available. Call download_data() first.")
            return None
        
        # Normalize to 100 (start at 100 for all stocks)
        normalized = (self.data / self.data.iloc[0]) * 100
        
        plt.figure(figsize=(14, 7))
        
        for ticker in normalized.columns:
            plt.plot(normalized.index, normalized[ticker], 
                    label=ticker, linewidth=2)
        
        plt.axhline(y=100, color='black', linestyle='--', 
                   linewidth=1, alpha=0.3)
        plt.title('Normalized Stock Prices (Base = 100)', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Normalized Price', fontsize=12)
        plt.legend(loc='best')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        return plt
    
    def plot_correlation_heatmap(self):
        """
        Plot heatmap of correlations between stocks.
        """
        corr = self.correlation_matrix()
        
        if corr is None or corr.empty:
            print("Error: No correlation data available. Call calculate_returns() first.")
            return None
        
        plt.figure(figsize=(10, 8))
        
        # Create heatmap using matplotlib
        im = plt.imshow(corr, cmap='RdYlGn', aspect='auto', 
                       vmin=-1, vmax=1)
        
        # Add colorbar
        plt.colorbar(im, label='Correlation')
        
        # Set ticks and labels
        plt.xticks(range(len(corr.columns)), list(corr.columns), rotation=45)
        plt.yticks(range(len(corr.columns)), list(corr.columns))
        
        # Add correlation values as text
        for i in range(len(corr)):
            for j in range(len(corr)):
                text = plt.text(j, i, f'{corr.iloc[i, j]:.2f}',
                              ha="center", va="center", color="black")
        
        plt.title('Stock Correlation Matrix', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        return plt
    
    def best_and_worst(self):
        """
        Find best and worst performing stocks.
        """
        summary = self.summary_statistics()
        if summary is None or summary.empty:
            print("Error: No summary statistics available. Call summary_statistics() first.")
            return None
        
        if self.data is None or self.data.empty:
            print("Error: No data available. Call download_data() first.")
            return None
        
        # Sort by total return
        total_returns = (self.data.iloc[-1] / self.data.iloc[0] - 1) * 100
        
        best = total_returns.idxmax()
        worst = total_returns.idxmin()
        
        print("\n" + "="*60)
        print("BEST AND WORST PERFORMERS")
        print("="*60)
        print(f"\nBest: {best}")
        print(f"Total Return: {total_returns[best]:.2f}%")
        print(f"Sharpe Ratio: {summary.loc[best, 'Sharpe Ratio']:.3f}")
        
        print(f"\nWorst: {worst}")
        print(f"Total Return: {total_returns[worst]:.2f}%")
        print(f"Sharpe Ratio: {summary.loc[worst, 'Sharpe Ratio']:.3f}")
        print("="*60)
        
        return best, worst
    
    
# TEST YOUR CLASS
if __name__ == "__main__":
    # Create analyzer for tech stocks
    analyzer = MultiStockAnalyzer(
        tickers=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'],
        
    )
    
    # Download data
    analyzer.download_data()
    
    # Calculate returns
    analyzer.calculate_returns()
    
    # Print summary statistics
    print("\nSUMMARY STATISTICS:")
    print(analyzer.summary_statistics())
    
    # Print correlation matrix
    print("\nCORRELATION MATRIX:")
    print(analyzer.correlation_matrix())
    
    # Find best and worst
    analyzer.best_and_worst()
    
    # Plot normalized prices
    analyzer.plot_normalized_prices()
    plt.savefig('week1/day4/normalized_prices.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    # Plot correlation heatmap
    analyzer.plot_correlation_heatmap()
    plt.savefig('week1/day4/correlation_heatmap.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("\nGraphs saved to week1/day4/")