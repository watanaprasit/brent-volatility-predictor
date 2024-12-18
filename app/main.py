import sys
import os
from fastapi import FastAPI, HTTPException
from app.crud import fetch_data
from app.model import train_model
from app.volatility import calculate_volatility  # Importing the calculate_volatility function
from fastapi.middleware.cors import CORSMiddleware

# Ensure the app directory is in the module search path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# Allow all origins (you can adjust this as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Run initial setup: fetch data and train the model
try:
    print("Fetching initial data...")
    fetch_data()
    print("Training initial model...")
    train_model()
except Exception as e:
    print(f"Error during initial setup: {e}")


@app.get("/")
def read_root():
    """
    Root endpoint for API health check.
    """
    return {"message": "Welcome to the Brent Crude Oil Volatility Predictor API!"}


@app.get("/volatility")
def get_volatility(symbol: str, start_date: str, end_date: str, window_size: int = 30):
    """
    Endpoint to calculate and return volatility for the given parameters.
    """
    try:
        # Calculate the volatility
        volatility_data = calculate_volatility(symbol, start_date, end_date, window_size)
        return {"success": True, "data": volatility_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating volatility: {str(e)}")



