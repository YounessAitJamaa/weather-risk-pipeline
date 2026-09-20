# Weather Risk Pipeline

## Description

Weather Risk Pipeline is a data engineering project that analyzes weather forecasts for Moroccan cities and identifies periods that may create risks for delivery and logistics operations.

The pipeline collects weather data from Open-Meteo, cleans and transforms it, calculates a weather risk score, stores the results in PostgreSQL, and provides a Streamlit dashboard for analysis.

## Business Problem

Bad weather conditions such as heavy precipitation, strong winds, extreme temperatures, or severe weather conditions can affect delivery operations.

The project answers the following business question:

> **Quelles villes et quelles périodes présentent le plus grand risque météorologique dans les prochains jours ?**

The results help identify risky cities and periods and support delivery planning.

## Objectives

* Collect weather forecasts for Moroccan cities.
* Clean and standardize the data.
* Calculate weather risk indicators.
* Generate a risk score from 0 to 100.
* Store the results in PostgreSQL.
* Analyze the data with SQL.
* Visualize the results with Streamlit.
* Automate the pipeline with Apache Airflow.
* Run the services with Docker Compose.

## Architecture

The project follows a **Bronze → Silver → Gold** architecture.

```text
SimpleMaps + Open-Meteo
          │
          ▼
       Bronze
     Raw data
          │
          ▼
       Silver
   Cleaned data
          │
          ▼
        Gold
   Risk features
          │
          ▼
     PostgreSQL
       │     │
       ▼     ▼
      SQL  Streamlit
   Analysis Dashboard

      Apache Airflow
      orchestrates
     the pipeline
```

### Bronze

Stores the raw source data without modification.

* Moroccan cities and coordinates.
* Raw Open-Meteo weather responses.

### Silver

Cleans and prepares the data.

* Standardize data types and dates.
* Check missing values and duplicates.
* Combine city and weather data.
* Produce a clean weather dataset.

### Gold

Creates business-ready risk data.

* Weather categories.
* Individual risk indicators.
* Global risk score.
* Risk category.
* PostgreSQL-ready data.

## Technologies

| Technology     | Purpose                          |
| -------------- | -------------------------------- |
| Python         | Data pipeline                    |
| Pandas         | Data cleaning and transformation |
| Open-Meteo API | Weather forecasts                |
| SimpleMaps     | Moroccan cities and coordinates  |
| PostgreSQL     | Data storage                     |
| SQL            | Business analysis                |
| Streamlit      | Interactive dashboard            |
| Apache Airflow | Pipeline orchestration           |
| Docker Compose | Containerization                 |
| Git / GitHub   | Version control                  |

## Project Structure

```text
weather-risk-pipeline/
│
├── airflow/
│   └── dags/
│       └── weather_risk_dag.py
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── bronze/
│   │   ├── cities.csv
│   │   └── weather/*.json
│   ├── silver/
│   │   └── weather_clean.csv
│   └── gold/
│       └── weather_risk.csv
│
├── sql/
│   ├── schema.sql
│   └── analysis.sql
│
├── src/
│   ├── check_cities.py
│   ├── test_open_meteo.py
│   ├── extract_weather.py
│   ├── transform.py
│   ├── gold.py
│   └── load.py
│
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Pipeline

The pipeline consists of four main stages:

```text
Extract → Transform → Gold → Load
```

* **Extract:** Collect Moroccan cities and weather forecasts from Open-Meteo.
* **Transform:** Clean, standardize and validate the collected data.
* **Gold:** Calculate weather risk indicators and the global risk score.
* **Load:** Store the final data in PostgreSQL.

Apache Airflow orchestrates these stages automatically on a daily schedule with retries.

## Risk Score

The project calculates a weather risk score from **0 to 100** using five factors:

| Risk Factor        | Weight |
| ------------------ | -----: |
| Precipitation      |    30% |
| Wind speed         |    25% |
| Wind gusts         |    20% |
| Temperature        |    15% |
| Weather conditions |    10% |

The weighted factors are combined to produce the final risk score.

The score is classified into categories such as:

* Low
* Moderate
* High
* Extreme

## Dashboard

The Streamlit dashboard provides an interactive analysis of weather risks.

It includes:

* Number of cities
* Maximum temperature
* Maximum precipitation
* Number of risky periods
* Highest-risk city
* Risk distribution
* Daily risk evolution
* Filters by city, date, period and risk level

The dashboard answers:

> **Où et quand faut-il être particulièrement vigilant dans les prochains jours ?**

## SQL Analysis

The project contains SQL queries for analyzing the weather risk data stored in PostgreSQL.

The analysis includes:

* Risk distribution
* Highest-risk cities and dates
* Average risk by city
* Risk evolution
* Precipitation risk
* Wind risk
* Temperature risk
* Weather-condition risk

SQL files:

```text
sql/schema.sql
sql/analysis.sql
```

## Installation

### Clone the repository

```bash
git clone git@github.com:YounessAitJamaa/weather-risk-pipeline.git
cd weather-risk-pipeline
```

### Start the services

```bash
docker compose up -d
```

Docker Compose starts:

* **PostgreSQL** — database
* **Apache Airflow** — pipeline orchestration
* **Streamlit** — dashboard

### Access the applications

* **Airflow:** http://localhost:8081
* **Streamlit:** http://localhost:8501
* **PostgreSQL:** `localhost:5433`

The Airflow DAG is scheduled to run daily:

```text
Extract → Transform → Gold → Load
```

## Results

The pipeline processes weather forecasts for **120 Moroccan cities** over a **7-day forecast period**.

The final system provides:

* Clean and validated weather data.
* A risk score from 0 to 100 for each city and date.
* Risk categories for easier interpretation.
* PostgreSQL storage.
* SQL business analysis.
* An interactive Streamlit dashboard.
* Automated execution with Apache Airflow.

The project helps identify **where and when weather conditions may affect delivery operations**.
