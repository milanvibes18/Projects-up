import sqlite3
import matplotlib.pyplot as plt

# Connect to database
conn = sqlite3.connect("health_data.db")
c = conn.cursor()

# Fetch all stored readings
c.execute("SELECT timestamp, heart_rate FROM health")
rows = c.fetchall()
conn.close()

# Separate into lists
timestamps = [row[0] for row in rows]
heart_rates = [row[1] for row in rows]

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(timestamps, heart_rates, marker="o", linestyle="-", label="Heart Rate (BPM)")

# Beautify the chart
plt.xlabel("Timestamp")
plt.ylabel("Heart Rate (BPM)")
plt.title("Heart Rate History")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()

# Show the plot
plt.show()
