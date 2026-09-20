from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

# Load gold data

BASE_DIR = Path(__file__).resolve().parent.parent

GOLD_PATH = BASE_DIR / "data" / "gold" / "weather_risk.csv"

df = pd.read_csv(GOLD_PATH)


# Load cities csv

BRONZ_PATH = BASE_DIR / "data" / "bronze" / "cities.csv"

cities_df = pd.read_csv(BRONZ_PATH)

cities_df = cities_df[["city", "lat", "lng"]].copy()



# connect to PostgreSQL

DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/weather_risk"

engine = create_engine(DATABASE_URL)

# Clear old data

with engine.begin() as connection:
    connection.execute(
        text("TRUNCATE TABLE weather_risk, cities RESTART IDENTITY")
    )

print("Old data cleared")


# Load cities first

cities_df.to_sql(
    "cities",
    engine,
    if_exists="append",
    index=False
)

print("Cities loaded successfully.")


# Get city IDs from PostgreSQL

with engine.connect() as connection:
    db_cities = pd.read_sql(
        text("SELECT city_id, city FROM cities"),
        connection
    )


# Add city_id to weather data

df = df.merge(
    db_cities,
    on="city",
    how="left"
)

# Remove duplicated city information

df = df.drop(columns=["city", "lat", "lng"])


df = df[
    [
        "city_id",
        "date",
        "temp_max",
        "temp_min",
        "precipitation",
        "precipitation_probability",
        "wind_speed",
        "wind_gusts",
        "weather_code",
        "precipitation_category",
        "heat_category",
        "cold_category",
        "wind_category",
        "rain_risk",
        "wind_risk",
        "gust_risk",
        "temperature_risk",
        "weather_code_risk",
        "risk_score",
        "risk_category"
    ]
]

df.to_sql(
    "weather_risk",
    engine,
    if_exists="append",
    index=False
)

print("Weather risk data loaded successfully.")