import os
import sqlite3
import time
import random
from datetime import datetime

# --- IMPORTANT: Hardcode the absolute path to your project directory ---
# This ensures all scripts (app.py, input_data.py, check_db.py)
# always use the exact same database file.
PROJECT_DIR = r"C:\Users\Oindrieel\Desktop\project file\Projects-up\Digital_Twin"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "digital_twin.db")


def setup_database():
    """Initializes the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create 'devices' table (using a cleaner schema)
    c.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL, model TEXT, location TEXT, firmware TEXT
    )""")
    # Create 'device_data' table
    c.execute("""
    CREATE TABLE IF NOT EXISTS device_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT, device_id INTEGER,
        timestamp TEXT NOT NULL, value REAL NOT NULL,
        FOREIGN KEY (device_id) REFERENCES devices(id)
    )""")
    # Insert initial device metadata
    devices = [
        ("Heart Rate Sensor", "Health", "MAX30102", "ICU Room 1", "v1.2"),
        ("Temp Sensor", "Environment", "DHT22", "ICU Room 1", "v2.3")
    ]
    c.executemany("INSERT OR IGNORE INTO devices (name, type, model, location, firmware) VALUES (?, ?, ?, ?, ?)",
                  devices)
    conn.commit()
    conn.close()
    print("[INFO] Database setup is complete.")


# --- Main Execution ---
setup_database()  # Run setup once at the start

# Get the device IDs
conn = sqlite3.connect(DB_PATH)
heart_id = conn.execute("SELECT id FROM devices WHERE name = 'Heart Rate Sensor'").fetchone()[0]
temp_id = conn.execute("SELECT id FROM devices WHERE name = 'Temp Sensor'").fetchone()[0]
conn.close()

print(f"📌 Using device IDs → Heart Rate: {heart_id}, Temp: {temp_id}")
print("🚀 Starting data generator... Press CTRL+C to stop.")

# --- Main Loop ---
while True:
    try:
        # --- Connection is managed inside the loop for robustness ---
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Use the JavaScript-friendly ISO 8601 timestamp format
        now_iso = datetime.now().isoformat(timespec="seconds")

        # Insert Data
        heart_rate = random.randint(55, 125)
        c.execute("INSERT INTO device_data (device_id, timestamp, value) VALUES (?, ?, ?)",
                  (heart_id, now_iso, heart_rate))
        temp_value = round(random.uniform(30.0, 35.5), 2)
        c.execute("INSERT INTO device_data (device_id, timestamp, value) VALUES (?, ?, ?)",
                  (temp_id, now_iso, temp_value))
        conn.commit()

        # Self-Verification Step to confirm data is being saved
        count = c.execute("SELECT COUNT(*) FROM device_data").fetchone()[0]
        print(f"✅ Inserted Data | Total Readings in DB: {count} | Latest Temp: {temp_value} °C")

    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
    finally:
        if conn:
            conn.close()  # Ensure connection is always closed

    time.sleep(3)

