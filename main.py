import os
import numpy as np
import pandas as pd
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

LAT, LON = 24.86, 67.01  # Karachi
URL = "https://archive-api.open-meteo.com/v1/archive"
VARS = "temperature_2m,relative_humidity_2m,surface_pressure,cloud_cover,wind_speed_10m"


def fetch_data():
    """Open-Meteo se 2024 ka hourly data laata hai."""
    r = requests.get(URL, params={
        "latitude": LAT, "longitude": LON,
        "start_date": "2024-01-01", "end_date": "2024-12-31",
        "hourly": VARS, "timezone": "auto",
    }, timeout=60)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df = df.sort_values("time").drop_duplicates("time").set_index("time")
    return df.interpolate().reset_index()  # missing values bharte hain


def make_features(df):
    """Target: agle ghante ka temperature. Sirf past values se features (no leakage)."""
    d = df.copy()
    T = d["temperature_2m"]
    for k in [1, 2, 3, 24]:
        d[f"lag_{k}"] = T.shift(k)
    d["roll_3"] = T.shift(1).rolling(3).mean()
    d["roll_24"] = T.shift(1).rolling(24).mean()
    hour = d["time"].dt.hour
    d["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    d["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    d["dow"] = d["time"].dt.dayofweek
    d["month"] = d["time"].dt.month
    d["target"] = T.shift(-1)  # agla ghanta
    return d.dropna().reset_index(drop=True)


def metrics(y_true, y_pred):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred),
    }


def main():
    df = fetch_data()
    d = make_features(df)

    # Time-based split: pehle 9 mahine train, aakhir ke 3 mahine test
    train = d[d["time"] < "2024-10-01"]
    test = d[d["time"] >= "2024-10-01"]

    feature_cols = [c for c in d.columns if c not in ["time", "target", "temperature_2m"]]
    X_train, y_train = train[feature_cols], train["target"]
    X_test, y_test = test[feature_cols], test["target"]

    results = {}

    # 1. Persistence: agla temperature = maujooda temperature
    results["Persistence"] = metrics(y_test, test["temperature_2m"])

    # 2. Linear Regression
    lr = LinearRegression().fit(X_train, y_train)
    results["Linear Regression"] = metrics(y_test, lr.predict(X_test))

    # 3. Random Forest
    rf = RandomForestRegressor(n_estimators=200, max_depth=12, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    results["Random Forest"] = metrics(y_test, rf.predict(X_test))

    table = pd.DataFrame(results).T.round(3)
    print(table)
    print("\nTest rows:", len(test), "| Train rows:", len(train))

    os.makedirs("results", exist_ok=True)
    table.to_csv("results/metrics.csv")


if __name__ == "__main__":
    main()
