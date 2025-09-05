import os, sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "digital_twin.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("📊 Devices:")
for row in c.execute("SELECT * FROM devices").fetchall():
    print(row)

print("\n📊 Last 5 readings:")
for row in c.execute("SELECT * FROM device_data ORDER BY id DESC LIMIT 5").fetchall():
    print(row)

conn.close()
