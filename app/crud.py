import os
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

DATA_PATH = "data/brent_crude_oil.csv"
SYMBOL = "BZ=F"

def fetch_data(symbol: str = SYMBOL):
    """Fetch past year's data for the given symbol and update the CSV."""
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

        # Check if the CSV exists
        if os.path.exists(DATA_PATH):
            # Read the existing data
            existing_data = pd.read_csv(DATA_PATH)
            
            # Check for duplicates, only append if the new data is not already in the CSV
            new_data = data[~data['date'].isin(existing_data['date'])]
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            # If the file doesn't exist, use the fetched data
            combined_data = data
        
        # Save the updated data to CSV
        combined_data.to_csv(DATA_PATH, index=False)
        print(f"Data saved to {DATA_PATH}")
    
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_data()

















