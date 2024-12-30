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
from datetime import timedelta
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
    Exposes an endpoint for the frontend to get the latest Brent Crude data and data for the past 7 days.
    """
    try:
        # Read the CSV data
        data = pd.read_csv("data/brent_crude_oil.csv")
        
        # Debug: Print raw data to check if it's being read correctly
        print("Raw data read from CSV:")
        print(data)

        # Extract all columns that match the pattern for dates and prices
        date_columns = [col for col in data.columns if 'date' in col]
        price_columns = [col for col in data.columns if 'price' in col]

        # Ensure equal numbers of date and price columns
        if len(date_columns) != len(price_columns):
            raise ValueError("Mismatch between date and price columns.")

        # Flatten the data into a single DataFrame
        combined_data = pd.DataFrame()
        for date_col, price_col in zip(date_columns, price_columns):
            temp_data = data[[date_col, price_col]].rename(
                columns={date_col: "date", price_col: "price"}
            )
            combined_data = pd.concat([combined_data, temp_data])

        # Drop rows with missing data and convert the date column
        combined_data = combined_data.dropna(subset=["date", "price"])
        combined_data["date"] = pd.to_datetime(combined_data["date"], errors="coerce")
        combined_data = combined_data.dropna(subset=["date"])

        # Sort by date
        combined_data = combined_data.sort_values(by="date", ascending=True)

        # Get the latest entry
        latest_entry = combined_data.iloc[-1]
        latest_date = latest_entry["date"]

        # Filter the past 7 days of data
        past_week_data = combined_data[
            (combined_data["date"] > (latest_date - timedelta(days=7))) & 
            (combined_data["date"] <= latest_date)
        ]

        # Format the past week data
        past_week_list = past_week_data.assign(
            date=past_week_data["date"].dt.strftime("%Y-%m-%d")
        )[["date", "price"]].to_dict(orient="records")

        # Prepare the final response
        response_data = {
            "latest": {
                "date": latest_entry["date"].strftime("%Y-%m-%d"),
                "price": latest_entry["price"],
            },
            "past_7_days": past_week_list,
        }

        # Debug: Print the response data
        print("Response data to be returned as JSON:")
        print(response_data)

        return JSONResponse(content={"status": "success", "data": response_data})
    
    except Exception as e:
        return JSONResponse(content={"status": "failed", "error": str(e)})





# Ensure the app is listening on 0.0.0.0:8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)











