import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

DATA_PATH = "data/brent_crude_oil.csv"
SYMBOL = "BZ=F"

def fetch_data(symbol: str = SYMBOL):
    """Fetch past year's data for the given symbol."""
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        past_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
        print(f"Fetching data for {symbol} from {past_year} to {today}...")
        
        # Fetch data from yfinance
        data = yf.download(symbol, start=past_year, end=today)
        
        if data.empty:
            raise ValueError(f"No data returned for symbol {symbol}. Please check the symbol and date range.")
        
        # Clean and format the data
        data = data[['Close']].reset_index()
        data.rename(columns={"Date": "date", "Close": "price"}, inplace=True)
        
        # Save the data to CSV
        data.to_csv(DATA_PATH, index=False)
        print(f"Data saved to {DATA_PATH}")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_data()


