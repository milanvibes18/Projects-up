import requests

BASE = "http://127.0.0.1:5000"

# Test GET (should be [] initially)
r = requests.get(BASE + "/devices")
print("GET /devices ->", r.status_code, r.text)

# Test POST (add one device)
data = {"name": "TempSensor", "type": "sensor"}
r = requests.post(BASE + "/devices", json=data)
print("POST /devices ->", r.status_code, r.text)

# Test GET again (should now show the new device)
r = requests.get(BASE + "/devices")
print("GET /devices ->", r.status_code, r.text)
