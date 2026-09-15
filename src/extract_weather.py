from pathlib import Path
import pandas as pd
import requests
import json


BASE_DIR = Path(__file__).resolve().parent.parent


API_URL = "https://api.open-meteo.com/v1/forecast"

def get_meteo(city, latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "wind_gusts_10m_max",
            "weather_code"
        ],
        "timezone": "Africa/Casablanca",
        "forecast_days" : 7
    }

    response = requests.get(API_URL, params=params, timeout=10)

    response.raise_for_status()

    data = response.json()

    save_files_path = BASE_DIR/"data"/"bronze"/"weather"

    with open(save_files_path / f"{city}.json", "w") as f:
        json.dump(data, f)

    return data    


csv_path = BASE_DIR/"data"/"bronze"/"cities.csv"


df = pd.read_csv(csv_path)

for index, row in df.iterrows(): 
    try:
        get_meteo(row["city"], row["lat"], row["lng"])
    except requests.RequestException as e:
        print(f"Error for {row['city']} : ", e)