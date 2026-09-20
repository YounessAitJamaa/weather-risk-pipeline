import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


DATABASE_URL = "postgresql://postgres@localhost/weather_risk"

engine = create_engine(DATABASE_URL)

st.title("Weather Risk Dashboard")


with engine.connect() as connection:
    result = connection.execute(
        text("SELECT COUNT(*) FROM cities")
    )

    number_of_cities = result.scalar()

    result = connection.execute(
        text("SELECT COUNT(DISTINCT date) FROM weather_risk")
    )

    number_of_forecast_days = result.scalar()

    result = connection.execute(
            text("SELECT COUNT(*) FROM weather_risk WHERE risk_score > 20")
    )

    number_of_risky_records = result.scalar()

    result = connection.execute(
            text("SELECT MAX(risk_score) FROM weather_risk")
    )

    highest_risk = result.scalar()

    result = connection.execute(
                text("SELECT risk_category, COUNT(*) FROM weather_risk GROUP BY risk_category;")
    )
    
    risk_distribution = result.fetchall()
    risk_categories = [row[0] for row in risk_distribution]
    risk_counts = [row[1] for row in risk_distribution]


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
            ORDER BY wr.risk_score DESC
            LIMIT 10
        """)
    )

    top_risky_records = result.fetchall()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Cities", number_of_cities)

with col2:
    st.metric("Forecast Days", number_of_forecast_days)

with col3:
    st.metric("Risky Records", number_of_risky_records)

with col4:
    st.metric("Highest Risk", highest_risk)

st.subheader("Risk Distribution")


risk_chart = pd.DataFrame(
    {"Counts" : risk_counts},
    index=risk_categories
)

st.bar_chart(risk_chart)

st.subheader("Top 10 Risky City/Date Records")

risky_records_df = pd.DataFrame(
    top_risky_records,
    columns=["City", "Date", "Risk Score", "Risk Category"]
)

st.dataframe(risky_records_df)