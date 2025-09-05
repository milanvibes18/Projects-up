import sqlite3
from datetime import datetime, timedelta
import random

conn = sqlite3.connect("digital_twin.db")
c = conn.cursor()

# Create tables
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
    FOREIGN KEY (device_id) REFERENCES devices (id)
)
""")

# Insert dummy devices (with metadata)
devices = [
    ("Heart Rate Sensor", "health", "MAX30102", "ICU Room 1", "UTC", "v1.0", 3),
    ("Temp Sensor", "environment", "DHT22", "ICU Room 1", "UTC", "v2.1", 5)
]
c.executemany("""
INSERT INTO devices (name, type, model, location, timezone, firmware, sampling_rate)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", devices)

# Insert dummy data for each device
now = datetime.now()
for device_id in range(1, 3):
    for i in range(10):
        ts = (now - timedelta(minutes=i)).isoformat()
        value = random.uniform(60, 100) if device_id == 1 else random.uniform(20, 35)
        c.execute("INSERT INTO device_data (device_id, timestamp, value) VALUES (?, ?, ?)",
                  (device_id, ts, value))

conn.commit()
conn.close()
print("✅ Database initialized with dummy data + metadata.")
