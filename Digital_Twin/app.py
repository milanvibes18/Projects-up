import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# --- Always use the DB inside the project folder ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "digital_twin.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # return rows as dict-like objects
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/devices_view")
def devices_view():
    conn = get_db_connection()
    devices = conn.execute("SELECT * FROM devices").fetchall()
    conn.close()
    return render_template("devices_view.html", devices=devices)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/get_data")
def get_data():
    conn = get_db_connection()
    data = {}

    devices = conn.execute("SELECT id, name FROM devices").fetchall()

    for device in devices:
        readings = conn.execute("""
            SELECT timestamp, value
            FROM device_data
            WHERE device_id = ?
            ORDER BY id DESC
            LIMIT 20
        """, (device["id"],)).fetchall()

        # Convert rows to dict
        data[device["name"]] = [
            {"timestamp": r["timestamp"], "value": r["value"]} for r in readings
        ]

    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
