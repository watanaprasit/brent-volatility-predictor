import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
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
    data["lagged_volatility"] = data["volatility"].shift(1)
    data["price_change"] = data["price"].pct_change()
    data["moving_avg_7"] = data["price"].rolling(window=7).mean()
    data["moving_avg_30"] = data["price"].rolling(window=30).mean()
    data.dropna(inplace=True)  # Drop rows with NaN values after adding features

    # Prepare features and labels
    data["timestamp"] = pd.to_datetime(data["date"])
    data["day_of_year"] = data["timestamp"].dt.dayofyear
    features = ["day_of_year", "lagged_volatility", "price_change", "moving_avg_7", "moving_avg_30"]
    X = data[features].values
    y = data["volatility"].values

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, shuffle=False)

    # Train the model (choose Random Forest or XGBoost)
    print("Training model...")
    # Option 1: Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Option 2: XGBoost (Uncomment below to use XGBoost)
    # model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)

    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error on Test Set: {mse}")

    # Save the model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()



