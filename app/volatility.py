import pandas as pd
import yfinance as yf
import matplotlib
import os
from datetime import timedelta
import matplotlib.pyplot as plt
matplotlib.use('Agg')  # Use the Agg backend, which does not require a display

def calculate_volatility(symbol: str, window_size: int = 30):
    """
    Fetches historical data for the given symbol and calculates the volatility
    over a rolling window of the past year until the day before the current date.
    Also returns an estimated volatility for the next 7 days.
    
    Args:
    - symbol: The ticker symbol (default is 'BZ=F' for Brent Crude Oil).
    - window_size: The rolling window size for volatility calculation (default is 30).
    
    Returns:
    - The relative URL to the saved plot image.
    - Estimated volatility for the next 7 days.
    """
    # Calculate the date range: the last 365 days until yesterday
    end_date = pd.to_datetime("today") - timedelta(days=1)
    start_date = end_date - timedelta(days=365)
    
    # Ensure start_date and end_date are in correct format (string for yfinance)
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    
    # Fetch historical data
    data = yf.download(symbol, start=start_date, end=end_date)
    
    if data.empty:
        raise ValueError(f"No data found for symbol {symbol} in the given date range.")
    
    # Calculate daily returns
    data['daily_return'] = data['Close'].pct_change()

    # Calculate rolling volatility (standard deviation of daily returns)
    data['volatility'] = data['daily_return'].rolling(window=window_size).std()

    # Use the last computed volatility as the "estimated" next 7 days volatility
    last_volatility = data['volatility'].dropna().iloc[-1]  # Get the most recent volatility value

    # Plot the volatility
    plt.figure(figsize=(10, 6))
    plt.plot(data['volatility'], label=f'{symbol} Volatility ({window_size}-day rolling)')
    plt.title(f'Volatility of {symbol} from {start_date} to {end_date}')
    plt.xlabel('Date')
    plt.ylabel('Volatility')
    plt.legend()
    plt.grid(True)

    # Save the plot to a 'static/images' directory
    image_dir = "static/images"
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # Constructing the file path and saving the plot
    plot_filename = f'volatility_{symbol}_{start_date}_to_{end_date}.png'
    plot_path = os.path.join(image_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()

    # Return the relative path for use in the API response
    return f"images/{plot_filename}", last_volatility  # Include last volatility value







