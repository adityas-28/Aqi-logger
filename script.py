import psycopg2
import os
import requests
from datetime import datetime
import dotenv

dotenv.load_dotenv()

print("Starting WAQI logger...")

TOKEN = os.getenv("WAQI_TOKEN")
station_id= os.getenv("WAQI_STATION")

URL = f"https://api.waqi.info/feed/@{station_id}/?token={TOKEN}"

try:
    response = requests.get(URL)
    result = response.json()

    data = result["data"]

    iaqi = data.get("iaqi", {})

    pm25 = iaqi.get("pm25", {}).get("v")
    pm10 = iaqi.get("pm10", {}).get("v")
    no2  = iaqi.get("no2", {}).get("v")
    so2  = iaqi.get("so2", {}).get("v")
    o3   = iaqi.get("o3", {}).get("v")
    co  = iaqi.get("co", {}).get("v")
    temperature = iaqi.get("t", {}).get("v")
    humidity    = iaqi.get("h", {}).get("v")
    aqi = data.get("aqi")

    timestamp = datetime.fromisoformat(data["time"]["iso"])
    station = data["city"]["name"]

    print("Extracted:", pm25, pm10, no2, so2, o3)

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    cur = conn.cursor()

    # 🔹 Insert
    cur.execute("""
    INSERT INTO aqi_logs 
    (timestamp, station, pm25, pm10, no2, so2, o3, co, temperature, humidity, aqi)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    timestamp,
    station,
    pm25,
    pm10,
    no2,
    so2,
    o3,
    co,
    temperature,
    humidity,
    aqi
))

    conn.commit()

    print("Data inserted successfully")

    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)