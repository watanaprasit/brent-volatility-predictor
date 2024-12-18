import pandas as pd
import yfinance as yf
import matplotlib
matplotlib.use('Agg')  # Use the Agg backend, which does not require a display

import matplotlib.pyplot as plt


import matplotlib.pyplot as plt

def calculate_volatility(symbol: str, start_date: str, end_date: str, window_size: int = 30):
    """
    Fetches historical data for the given symbol and calculates the volatility
    over a rolling window.
    
    Args:
    - symbol: The ticker symbol (e.g., 'CL=F' for Brent Crude Oil).
    - start_date: The start date for historical data (e.g., '2023-01-01').
    - end_date: The end date for historical data (e.g., '2023-12-31').
    - window_size: The rolling window size for volatility calculation (default is 30).
    
    Returns:
    - A plot of the calculated volatility.
    """
    # Fetch historical data
    data = yf.download(symbol, start=start_date, end=end_date)
    
    if data.empty:
        raise ValueError(f"No data found for symbol {symbol} in the given date range.")
    
    # Calculate daily returns
    data['daily_return'] = data['Close'].pct_change()

    # Calculate rolling volatility (standard deviation of daily returns)
    data['volatility'] = data['daily_return'].rolling(window=window_size).std()

    # Plot the volatility
    plt.figure(figsize=(10, 6))
    plt.plot(data['volatility'], label=f'{symbol} Volatility ({window_size}-day rolling)')
    plt.title(f'Volatility of {symbol} from {start_date} to {end_date}')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()
    plt.grid(True)

    # Save the plot to a file and return the file path
    plot_path = f'volatility_{symbol}_{start_date}_to_{end_date}.png'
    plt.savefig(plot_path)
    plt.close()

    return plot_path
