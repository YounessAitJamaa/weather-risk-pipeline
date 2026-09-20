import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres@localhost/weather_risk"
engine = create_engine(DATABASE_URL)

st.title("Weather Risk Dashboard")

# get the cities and dates for filter
with engine.connect() as connection:
    result = connection.execute(
        text("""
            SELECT city
            FROM cities
            ORDER BY city
        """)
    )
    cities = [row[0] for row in result.fetchall()]

    result = connection.execute(
        text("""
            SELECT DISTINCT date
            FROM weather_risk
            ORDER BY date
        """)
    )
    dates = [row[0] for row in result.fetchall()]

# filter by city
selected_city = st.selectbox(
    "Select a city",
    ["All cities"] + cities
)

# filter by date
selected_date = st.selectbox(
    "Select a date",
    ["All dates"] + dates
)

# filter by period
selected_period = st.date_input(
    "Select a period",
    value=(min(dates), max(dates))
)

period_start = selected_period[0]
period_end = selected_period[1]

# filter by risk level
risk_levels = [
    "All risk levels",
    "Low",
    "Moderate",
    "High",
    "Extreme"
]

selected_risk_level = st.selectbox(
    "Select a risk level",
    risk_levels
)


if selected_city == "All cities" and selected_date == "All dates":
    city_filter = "WHERE wr.date BETWEEN :period_start AND :period_end"
    city_params = {
        "period_start": period_start,
        "period_end": period_end
    }

elif selected_city != "All cities" and selected_date == "All dates":
    city_filter = """
        WHERE c.city = :city
        AND wr.date BETWEEN :period_start AND :period_end
    """
    city_params = {
        "city": selected_city,
        "period_start": period_start,
        "period_end": period_end
    }

elif selected_city == "All cities" and selected_date != "All dates":
    city_filter = "WHERE wr.date = :date"
    city_params = {
        "date": selected_date
    }

else:
    city_filter = """
        WHERE c.city = :city
        AND wr.date = :date
    """
    city_params = {
        "city": selected_city,
        "date": selected_date
    }


if selected_risk_level != "All risk levels":
    if city_filter == "":
        city_filter = "WHERE wr.risk_category = :risk_level"
    else:
        city_filter += " AND wr.risk_category = :risk_level"

    city_params["risk_level"] = selected_risk_level

with engine.connect() as connection:

    # KPI 1 - Number of cities
    result = connection.execute(
        text("""
            SELECT COUNT(DISTINCT c.city)
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter),
        city_params
    )
    number_of_cities = result.scalar()

    # KPI 2 - Maximum temperature
    result = connection.execute(
        text("""
            SELECT MAX(wr.temp_max)
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter),
        city_params
    )
    maximum_temperature = result.scalar()

    # KPI 3 - Maximum precipitation
    result = connection.execute(
        text("""
            SELECT MAX(wr.precipitation)
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter),
        city_params
    )
    maximum_precipitation = result.scalar()

    # KPI 4 - Number of risky periods
    if selected_city == "All cities" and selected_date == "All dates":
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM weather_risk wr
                WHERE wr.risk_score > 20
            """)
        )

    elif selected_city != "All cities" and selected_date == "All dates":
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM weather_risk wr
                JOIN cities c
                    ON wr.city_id = c.city_id
                WHERE c.city = :city
                AND wr.risk_score > 20
            """),
            city_params
        )

    elif selected_city == "All cities" and selected_date != "All dates":
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM weather_risk wr
                WHERE wr.date = :date
                AND wr.risk_score > 20
            """),
            city_params
        )

    else:
        result = connection.execute(
            text("""
                SELECT COUNT(*)
                FROM weather_risk wr
                JOIN cities c
                    ON wr.city_id = c.city_id
                WHERE c.city = :city
                AND wr.date = :date
                AND wr.risk_score > 20
            """),
            city_params
        )

    number_of_risky_periods = result.scalar()

    # KPI 5 - City presenting the highest risk
    result = connection.execute(
        text("""
            SELECT c.city
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter + """
            ORDER BY wr.risk_score DESC
            LIMIT 1
        """),
        city_params
    )
    highest_risk_city = result.scalar()

    # Risk distribution
    result = connection.execute(
        text("""
            SELECT
                wr.risk_category,
                COUNT(*)
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter + """
            GROUP BY wr.risk_category
            ORDER BY COUNT(*) DESC
        """),
        city_params
    )

    risk_distribution = result.fetchall()
    risk_categories = [row[0] for row in risk_distribution]
    risk_counts = [row[1] for row in risk_distribution]

    # Top 10 risky city/date records
    result = connection.execute(
        text("""
            SELECT
                c.city,
                wr.date,
                wr.risk_score,
                wr.risk_category
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter + """
            ORDER BY wr.risk_score DESC
            LIMIT 10
        """),
        city_params
    )

    top_risky_records = result.fetchall()

    # Daily risk trend
    result = connection.execute(
        text("""
            SELECT
                wr.date,
                ROUND(AVG(wr.risk_score)::numeric, 2) AS average_risk
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter + """
            GROUP BY wr.date
            ORDER BY wr.date
        """),
        city_params
    )

    daily_risk = result.fetchall()

    # Risk causes
    result = connection.execute(
        text("""
            SELECT
                ROUND(AVG(wr.rain_risk)::numeric, 2),
                ROUND(AVG(wr.wind_risk)::numeric, 2),
                ROUND(AVG(wr.gust_risk)::numeric, 2),
                ROUND(AVG(wr.temperature_risk)::numeric, 2),
                ROUND(AVG(wr.weather_code_risk)::numeric, 2)
            FROM weather_risk wr
            JOIN cities c
                ON wr.city_id = c.city_id
        """ + city_filter),
        city_params
    )

    risk_causes = result.fetchone()

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Cities", number_of_cities)

with col2:
    st.metric("Max Temperature", maximum_temperature)

with col3:
    st.metric("Max Precipitation", maximum_precipitation)

with col4:
    st.metric("Risky Periods", number_of_risky_periods)

with col5:
    st.metric("Highest-Risk City", highest_risk_city)

# Risk Distribution
st.subheader("Risk Distribution")

risk_chart = pd.DataFrame(
    {"Counts": risk_counts},
    index=risk_categories
)

st.bar_chart(risk_chart)

# Top 10 Risky City/Date Records
st.subheader("Top 10 Risky City/Date Records")

risky_records_df = pd.DataFrame(
    top_risky_records,
    columns=[
        "City",
        "Date",
        "Risk Score",
        "Risk Category"
    ]
)

st.dataframe(risky_records_df)

# Daily Risk Trend
st.subheader("Daily Risk Trend")

daily_risk_df = pd.DataFrame(
    daily_risk,
    columns=[
        "Date",
        "Average Risk"
    ]
)

daily_risk_df["Date"] = pd.to_datetime(
    daily_risk_df["Date"]
)

daily_risk_df["Average Risk"] = pd.to_numeric(
    daily_risk_df["Average Risk"]
)

st.line_chart(
    daily_risk_df,
    x="Date",
    y="Average Risk"
)

# Risk causes
risk_causes_df = pd.DataFrame(
    {
        "Cause": [
            "Rain",
            "Wind",
            "Wind Gusts",
            "Temperature",
            "Weather Code"
        ],
        "Average Risk": [
            risk_causes[0],
            risk_causes[1],
            risk_causes[2],
            risk_causes[3],
            risk_causes[4]
        ]
    }
)

risk_causes_df["Average Risk"] = pd.to_numeric(
    risk_causes_df["Average Risk"]
)

st.subheader("Risk Causes")

st.bar_chart(
    risk_causes_df,
    x="Cause",
    y="Average Risk"
)