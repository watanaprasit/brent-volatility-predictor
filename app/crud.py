import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

DATA_PATH = "data/brent_crude_oil.csv"
SYMBOL = "BZ=F"

def fetch_data():
    """Fetch past year's Brent Crude Oil data."""
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    today = datetime.today().strftime('%Y-%m-%d')
    past_year = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    data = yf.download(SYMBOL, start=past_year, end=today)
    data = data[['Close']].reset_index()
    data.rename(columns={"Date": "date", "Close": "price"}, inplace=True)
    data.to_csv(DATA_PATH, index=False)
    print(f"Data saved to {DATA_PATH}")

if __name__ == "__main__":
    fetch_data()

