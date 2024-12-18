from datetime import datetime
import pytz
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import os
import sys
import pandas as pd
from app.crud import fetch_data
from app.model import train_model
from app.volatility import calculate_volatility  # Import only the function

import uvicorn

# Ensure the app directory is in the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set timezone to Singapore Time (SGT)
SGT = pytz.timezone("Asia/Singapore")

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow all origins (you can adjust this as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Global variable to store the last update time
last_update_time = None

# Run initial setup: fetch data and train the model
try:
    print("Fetching initial data...")
    fetch_data()
    print("Training initial model...")
    train_model()
    last_update_time = datetime.now(SGT)  # Set initial update time
except Exception as e:
    print(f"Error during initial setup: {e}")


@app.get("/")
def read_root():
    """
    Root endpoint for API health check.
    """
    return {"message": "Welcome to the Brent Crude Oil Volatility Predictor API!"}


@app.get("/volatility")
def get_volatility(symbol: str = "BZ=F", window_size: int = 30):
    """
    Endpoint to calculate and return volatility for the given parameters.
    This now also predicts the next 7 days' volatility using a machine learning model.
    """
    try:
        # Generate the volatility plot and get the last volatility value
        plot_path, volatility_value = calculate_volatility(symbol=symbol, window_size=window_size)

        # Display the predicted volatility figure in the HTML
        image_url = f"/static/{plot_path}"  # Corrected path to the image
        html_content = f"""
        <html>
            <body>
                <h1>Next 7 Days Volatility: {volatility_value:.4f}</h1>
                <img src="{image_url}" alt="Volatility Plot">
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating volatility: {str(e)}")


@app.get("/last-update")
def get_last_update():
    """
    Endpoint to get the last update time.
    """
    if last_update_time:
        return {"last_update": last_update_time.strftime("%Y-%m-%d %H:%M:%S")}
    else:
        return {"last_update": "No updates have been made yet."}


@app.get("/api/brent-crude-data/")
async def get_brent_crude_data():
    """
    Exposes an endpoint for the frontend to get the historical Brent Crude data.
    """
    try:
        # Read the saved CSV data
        data = pd.read_csv("data/brent_crude_oil.csv")
        
        # Debug: Print raw data to check if it's being read correctly
        print("Raw data read from CSV:")
        print(data)

        # Clean the data: remove the extra "BZ=F" row in column 'Ticker' (if present)
        data = data.dropna(subset=["date", "price"])  # Drop rows where 'date' or 'price' are missing
        
        # Debug: Print data after removing missing values
        print("Data after dropping missing values:")
        print(data)

        # Convert the 'date' column to a datetime object (automatically detects the format)
        data['date'] = pd.to_datetime(data['date'], errors='coerce')

        # Debug: Print data after date conversion
        print("Data after date conversion:")
        print(data)

        # Drop rows where 'date' conversion failed (in case of invalid dates)
        data = data.dropna(subset=['date'])

        # Debug: Print data after dropping invalid dates
        print("Data after dropping invalid dates:")
        print(data)

        # Convert the date column to string for JSON serialization
        data['date'] = data['date'].dt.strftime('%Y-%m-%d')  # Format date as a string

        # Convert the cleaned data to a list of dictionaries for the JSON response
        data_dict = data[['date', 'price']].to_dict(orient="records")
        
        # Debug: Print the final data before returning it
        print("Final data to be returned as JSON:")
        print(data_dict)

        return JSONResponse(content={"status": "success", "data": data_dict})
    
    except Exception as e:
        return JSONResponse(content={"status": "failed", "error": str(e)})



# Ensure the app is listening on 0.0.0.0:8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)











