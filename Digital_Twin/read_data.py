import sqlite3

# Connect to database
conn = sqlite3.connect("health_data.db")
c = conn.cursor()

# Query all stored readings
c.execute("SELECT * FROM health")
rows = c.fetchall()

print("📜 Heart Rate History:")
print("-" * 40)
for row in rows:
    timestamp, bpm = row
    status = "Low" if bpm < 50 else ("High" if bpm > 120 else "Normal")
    print(f"{timestamp} | {bpm} bpm | {status}")

conn.close()
