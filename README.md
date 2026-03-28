# AQI Logger

A Python script that fetches real-time Air Quality Index (AQI) data from the [World Air Quality Index (WAQI) API](https://aqicn.org/api/) and logs it into a PostgreSQL database.

## Features

- Fetches air quality data for a specific station from the WAQI API.
- Extracts key pollutant values: `pm25`, `pm10`, `no2`, `so2`, and `o3`.
- Records the data with a timestamp and station name.
- Connects and logs the data securely into a PostgreSQL Database.

## Prerequisites

- Python 3.x
- PostgreSQL Database
- A WAQI API Token (Get one at [aqicn.org/data-platform/token/](https://aqicn.org/data-platform/token/))

## Installation

1. Clone or download this repository.
2. It's recommended to create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory and add the following environment variables:

```ini
# WAQI API Settings
WAQI_TOKEN=your_waqi_api_token
WAQI_STATION=your_station_id_or_keyword

# PostgreSQL Database Settings
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

## Database Schema

Ensure your PostgreSQL database has a table named `aqi_logs` with the following structure:

```sql
CREATE TABLE aqi_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ,
    station VARCHAR(255),
    pm25 NUMERIC,
    pm10 NUMERIC,
    no2 NUMERIC,
    so2 NUMERIC,
    o3 NUMERIC
);
```

## Usage

Run the script to fetch the latest AQI data and log it to your database:

```bash
python script.py
```
