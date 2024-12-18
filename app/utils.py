# import pandas as pd
# import numpy as np
# import yfinance as yf

# def calculate_volatility(symbol: str, start_date: str, end_date: str, window_size: int = 30):
#     """
#     Calculate rolling annualized historical volatility for a given symbol.
#     """
#     # Fetch historical data
#     data = yf.download(symbol, start=start_date, end=end_date)
    
#     # Check if data is empty
#     if data.empty:
#         raise ValueError(f"No data found for symbol {symbol} in the given date range.")
    
#     # Calculate daily returns
#     data['Log_Returns'] = np.log(data['Close'] / data['Close'].shift(1))
    
#     # Calculate rolling standard deviation (volatility)
#     data['Rolling_Std'] = data['Log_Returns'].rolling(window_size).std()
    
#     # Annualize the volatility
#     data['Annualized_Volatility'] = data['Rolling_Std'] * np.sqrt(252)
    
#     # Return as a dictionary of dates and volatility values
#     return data['Annualized_Volatility'].dropna().to_dict()
