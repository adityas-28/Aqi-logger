import psycopg2
import os
from datetime import datetime
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()
print("Starting DB test...")

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    print("Connected to database")

    cur = conn.cursor()

    # Insert dummy row
    cur.execute("""
        INSERT INTO aqi_logs (timestamp, station, pm25, pm10, no2, so2, o3)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        datetime.now(),
        "IHBAS_TEST",
        100,
        150,
        40,
        10,
        25
    ))

    conn.commit()
    print("Dummy row inserted")

    # Verify insert
    cur.execute("SELECT * FROM aqi_logs ORDER BY id DESC LIMIT 1;")
    row = cur.fetchone()

    print("Latest row:", row)

    cur.close()
    conn.close()

except Exception as e:
    print("Error:", e)