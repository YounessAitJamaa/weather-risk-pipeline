from pathlib import Path
import json
import pandas as pd


# stock the path of the base directorie
BASE_DIR = Path(__file__).resolve().parent.parent

# the path of the weather folder
weather_path = BASE_DIR/"data"/"bronze"/"weather"

# stock all the json files inside weather
weather_files = weather_path.glob("*.json")

# path to the cities.csv file
csv_path = BASE_DIR/"data"/"bronze"/"cities.csv"

# Read the cities CSV file
cities_df = pd.read_csv(csv_path)

cities_df = cities_df[["city", "lat", "lng"]]

all_data = []


for weather_file in weather_files:

    # read the json file
    with open(weather_file, 'r') as f:
        data = json.load(f)

    # stock only the daily data 
    daily = data['daily']

    # make a dataframe from the daily 
    df = pd.DataFrame(daily)


    # add a column into the dataframe named city
    df.insert(0, "city", weather_file.stem)

    # renaming the columns where we can undestand 
    df = df.rename(columns={
        "time": "date",
        "temperature_2m_max": "temp_max",
        "temperature_2m_min": "temp_min",
        "precipitation_sum": "precipitation",
        "precipitation_probability_max": "precipitation_probability",
        "wind_speed_10m_max": "wind_speed",
        "wind_gusts_10m_max": "wind_gusts",
        "weather_code": "weather_code"
    })

    # change the type of date columns
    df['date'] = pd.to_datetime(arg=df['date'])

    # merge the two dataframes
    df = pd.merge(df, cities_df, on="city", how="left")

    all_data.append(df)


silver_df = pd.concat(all_data)

print(silver_df)
# print(silver_df.shape)

# print(silver_df.isna().sum())
# print(silver_df["city"].nunique())
# print(silver_df.duplicated(subset=["city", "date"]).sum())


silver_path = BASE_DIR / "data"/ "silver" / "weather_clean.csv"


silver_df.to_csv(silver_path, index = False)

