import requests


url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": 33.5992,
    "longitude": -7.6200,
    "daily": [
        "temperature_2m_max",
        "temperature_2m_min",
        "precipitation_sum",
        "precipitation_probability_max",
        "wind_speed_10m_max",
        "wind_gusts_10m_max",
        "weather_code"
    ],
    "timezone": "Africa/Casablanca"
}

response = requests.get(url, params=params, timeout=10)

response.raise_for_status()

data = response.json()

print(data)

