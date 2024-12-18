import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

DATA_PATH = "data/brent_crude_oil.csv"
MODEL_PATH = "models/volatility_model.pkl"

def train_model():
    """Train a model on historical Brent Crude Oil volatility."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Please fetch data first.")

    # Load and clean data
    data = pd.read_csv(DATA_PATH)
    data["price"] = pd.to_numeric(data["price"], errors="coerce")  # Convert to numeric, set invalid to NaN
    data.dropna(subset=["price"], inplace=True)  # Drop rows with NaN prices

    # Calculate volatility
    data["volatility"] = data["price"].pct_change().rolling(window=30).std()
    data.dropna(subset=["volatility"], inplace=True)  # Drop rows with NaN volatility

    # Prepare features and labels
    data["timestamp"] = pd.to_datetime(data["date"])
    data["day_of_year"] = data["timestamp"].dt.dayofyear
    X = data[["day_of_year"]].values
    y = data["volatility"].values

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Save the model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()


