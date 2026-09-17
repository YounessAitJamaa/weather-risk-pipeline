from pathlib import Path
import pandas as pd


# Load Silver data

BASE_DIR = Path(__file__).resolve().parent.parent

SILVER_PATH = BASE_DIR / "data" /"silver"

df = pd.read_csv(SILVER_PATH / "weather_clean.csv")

df['date'] = pd.to_datetime(df['date'])


# Weather categorization

def categorize_precipitation(value):
    if value == 0:
        return "None"
    elif value <= 5:
        return "Light"
    elif value <= 15:
        return "Moderate"
    elif value <= 30:
        return "Heavy"
    else:
        return "Extreme"


def categorize_heat(value):
    if value <= 30:
        return "Normal"
    elif value <= 40:
        return "Hot"
    else:
        return "Extreme Heat"


def categorize_cold(value):
    if value >= 10:
        return "Normal"
    elif value >= 5:
        return "Cold"
    else:
        return "Extreme Cold"


def categorize_wind(value):
    if value < 20:
        return "Calm"
    elif value <= 40:
        return "Moderate"
    elif value <= 60:
        return "Strong"
    elif value <= 80:
        return "Very Strong"
    else:
        return "Extreme"


df["precipitation_category"] = df["precipitation"].apply(categorize_precipitation)
df["heat_category"] = df["temp_max"].apply(categorize_heat)
df["cold_category"] = df["temp_min"].apply(categorize_cold)
df["wind_category"] = df["wind_speed"].apply(categorize_wind)


# Rain risk

def rain_risk(precipitation, precipitation_probability):

    rain_risk = 0

    if precipitation == 0:
        rain_risk = 0

    elif precipitation <= 5:
        rain_risk =  25

    elif precipitation <= 15:
        rain_risk =  50

    elif precipitation <= 30:
        rain_risk =  75

    else:
        rain_risk =  100

    if precipitation_probability < 30:
        rain_risk *= 1.00
    elif precipitation_probability <= 60:
        rain_risk *= 1.10
    elif precipitation_probability <= 80:
        rain_risk *= 1.20
    else:
        rain_risk *= 1.30

    return round(min(rain_risk, 100))


def calculate_rain_risk(row):
    return rain_risk(
        row["precipitation"],
        row["precipitation_probability"]
    )


# Wind and gust risk

def wind_risk(wind_speed):

    wind_risk = 0
    if wind_speed <= 20:
        wind_risk = 0
    elif wind_speed <= 40:
        wind_risk = 25
    elif wind_speed <= 60:
        wind_risk = 50
    elif wind_speed <= 80:
        wind_risk = 75
    else:
        wind_risk = 100

    return wind_risk

def gust_risk(wind_gusts):

    gust_risk = 0
    if wind_gusts <= 30:
        gust_risk = 0
    elif wind_gusts <= 50:
        gust_risk = 25
    elif wind_gusts <= 70:
        gust_risk = 50
    elif wind_gusts <= 90:
        gust_risk = 75
    else:
        gust_risk = 100

    return gust_risk


df["rain_risk"] = df.apply(calculate_rain_risk, axis=1)
df["wind_risk"] = df["wind_speed"].apply(wind_risk)
df["gust_risk"] = df["wind_gusts"].apply(gust_risk)


# Temperature risk

def heat_risk(temp_max):

    if temp_max <= 30:
        return 0

    elif temp_max <= 35:
        return 25

    elif temp_max <= 40:
        return 50

    elif temp_max <= 45:
        return 75

    else:
        return 100

def cold_risk(temp_min):

    if temp_min >= 10:
        return 0

    elif temp_min >= 5:
        return 25

    elif temp_min >= 0:
        return 50

    elif temp_min >= -5:
        return 75

    else:
        return 100


def calculate_temp_risk(row):

    cold = cold_risk(row["temp_min"])
    heat = heat_risk(row["temp_max"])

    return max(cold, heat)


df["temperature_risk"] = df.apply(calculate_temp_risk, axis=1)

# Weather code risk

weather_risk_map = {
    0: 0,

    1: 10,
    2: 10,
    3: 10,

    45: 20,
    48: 20,

    51: 40,
    53: 40,
    55: 40,

    56: 60,
    57: 60,

    61: 40,
    63: 60,
    65: 80,

    66: 80,
    67: 80,

    71: 80,
    73: 80,
    75: 80,
    77: 80,

    80: 40,
    81: 60,
    82: 80,

    85: 80,
    86: 80,

    95: 100,
    96: 100,
    99: 100
}


def weather_code_risk(weather_code):
    return weather_risk_map.get(weather_code, 0)


df["weather_code_risk"] = df["weather_code"].apply(weather_code_risk)


# Calculate overall risk score

df["risk_score"] = (
    df["rain_risk"] * 0.30
    + df["wind_risk"] * 0.25
    + df["gust_risk"] * 0.20
    + df["temperature_risk"] * 0.15
    + df["weather_code_risk"] * 0.10
)

df["risk_score"] = df["risk_score"].round(2)


# Risk classification

def categorize_risk(risk_score):
    if risk_score <= 20:
        return "Low"

    elif risk_score <= 40:
        return "Moderate"

    elif risk_score <= 60:
        return "High"

    elif risk_score <= 80:
        return "Very High"

    else:
        return "Critical"

df["risk_category"] = df["risk_score"].apply(categorize_risk)


# Save Gold dataset

GOLD_PATH = BASE_DIR / "data" /"gold"

GOLD_PATH.mkdir(parents=True, exist_ok=True)

df.to_csv(GOLD_PATH / "weather_risk.csv", index=False)

print("Gold dataset created successfully.")