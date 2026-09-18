CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    lat DOUBLE PRECISION NOT NULL,
    lng DOUBLE PRECISION NOT NULL
);

CREATE TABLE weather_risk (
    city_id INTEGER NOT NULL REFERENCES cities(city_id),
    date DATE NOT NULL,
    temp_max DOUBLE PRECISION,
    temp_min DOUBLE PRECISION,
    precipitation DOUBLE PRECISION,
    precipitation_probability INTEGER,
    wind_speed DOUBLE PRECISION,
    wind_gusts DOUBLE PRECISION,
    weather_code INTEGER,
    precipitation_category VARCHAR(30),
    heat_category VARCHAR(30),
    cold_category VARCHAR(30),
    wind_category VARCHAR(30),
    rain_risk INTEGER,
    wind_risk INTEGER,
    gust_risk INTEGER,
    temperature_risk INTEGER,
    weather_code_risk INTEGER,
    risk_score DOUBLE PRECISION,
    risk_category VARCHAR(30),
    PRIMARY KEY (city_id, date)
);

ALTER TABLE cities
ADD CONSTRAINT cities_city_unique UNIQUE (city);