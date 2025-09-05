import os
import sqlite3
import time
import random
from datetime import datetime

# --- Always use the DB inside the project folder ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "digital_twin.db")

# Connect to the database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create tables if not exists (with metadata)
c.execute("""
CREATE TABLE IF NOT EXISTS devices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    model TEXT,
    location TEXT,
    timezone TEXT DEFAULT 'UTC',
    firmware TEXT,
    sampling_rate INTEGER
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS device_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER,
    timestamp TEXT,
    value REAL,
    FOREIGN KEY (device_id) REFERENCES devices(id)
)
""")

# Insert devices if not already present (with metadata)
devices = [
    ("Heart Rate Sensor", "health", "MAX30102", "ICU Room 1", "UTC", "v1.0", 3),
    ("Temp Sensor", "environment", "DHT22", "ICU Room 1", "UTC", "v2.1", 5)
]

c.executemany("""
INSERT OR IGNORE INTO devices (name, type, model, location, timezone, firmware, sampling_rate)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", devices)
conn.commit()

# --- Fetch actual device IDs dynamically ---
c.execute("SELECT id FROM devices WHERE name = 'Heart Rate Sensor'")
heart_id = c.fetchone()[0]

c.execute("SELECT id FROM devices WHERE name = 'Temp Sensor'")
temp_id = c.fetchone()[0]

print(f"📌 Using device IDs → Heart Rate: {heart_id}, Temp: {temp_id}")
print("🚀 Starting fake data generator... (Press CTRL+C to stop)")

while True:
    now = datetime.now().isoformat(sep=" ", timespec="seconds")

    # Fake Heart Rate
    heart_rate = random.randint(48, 130)
    c.execute("INSERT INTO device_data (device_id, timestamp, value) VALUES (?, ?, ?)",
              (heart_id, now, heart_rate))

    # Fake Temperature
    temp_value = round(random.uniform(28, 36), 2)
    c.execute("INSERT INTO device_data (device_id, timestamp, value) VALUES (?, ?, ?)",
              (temp_id, now, temp_value))

    conn.commit()

    print(f"Inserted → Heart Rate: {heart_rate} BPM | Temp: {temp_value} °C at {now}")

    # Keep only latest 100 readings per device
    for device_id in [heart_id, temp_id]:
        c.execute(f"""
            DELETE FROM device_data 
            WHERE id NOT IN (
                SELECT id FROM device_data WHERE device_id = {device_id} 
                ORDER BY id DESC LIMIT 100
            )
        """)
        conn.commit()

    time.sleep(3)  # wait 3 seconds
