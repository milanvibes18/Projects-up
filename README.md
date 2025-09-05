# 🧑‍⚕️ AI-Powered Digital Twin Assistant

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python\&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-orange?logo=flask\&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-3.42.0-lightgrey?logo=sqlite\&logoColor=white)](https://www.sqlite.org/)

---

## 📌 Project Overview

An **AI-powered Digital Twin** for **personalized health and lifestyle assistance**.
It collects health and activity data (currently simulated, later via Arduino IoT sensors) and provides:

* 🩺 Real-time monitoring
* ⚠️ Anomaly detection
* 📊 Interactive visual dashboards

---

## ✅ Current Progress (Phase 1 Completed)

* **Database (SQLite):** Timestamped health data storage
* **AI Rules:** Detect abnormal heart rates (Low <50, High >120)
* **Flask Backend:**

  * `/get_data` → Full history (JSON)
  * `/latest` → Latest reading + status (JSON)
  * `/dashboard` → HTML dashboard with table + auto-updating chart
* **Frontend (Dashboard):**

  * Real-time table of values
  * Live graph (Chart.js) auto-refreshing every 5s
* **Fake Data Generator:** Simulates continuous heart rate readings

---

## 🚀 Next Steps (Planned)

* **Integrate Arduino/ESP32 + Sensors:**

  * MAX30102 → Pulse & SpO₂
  * MPU6050 → Steps & Activity
  * LDR → Sleep environment monitoring
* **Extend AI Analysis:** Sleep pattern analysis & daily activity detection
* **Privacy-first storage** & optional cloud sync
* **Mobile-friendly dashboard**

---

## 🛠️ Tech Stack

| Component    | Technology                                                     |
| ------------ | -------------------------------------------------------------- |
| **Hardware** | Arduino Uno / ESP32, IoT sensors                               |
| **Backend**  | Flask (Python)                                                 |
| **Database** | SQLite                                                         |
| **Frontend** | HTML, CSS, Chart.js                                            |
| **AI/ML**    | Rule-based logic (current), TensorFlow / Scikit-learn (future) |

---

## 📂 Project Structure

```
digital-twin-project/
│
├── app.py             # Flask API + dashboard routes
├── insert_data.py     # Fake data generator (simulates Arduino sensor input)
├── health_data.db     # SQLite database (auto-created)
└── templates/
    └── dashboard.html # Dashboard (table + live graph)
```

---

## 📸 Screenshots (Optional)

![Dashboard Screenshot](path/to/your/dashboard_screenshot.png)
![Chart Screenshot](path/to/your/chart_screenshot.png)

---

## ⚡ How to Run

1. **Clone the repo:**

```bash
git clone https://github.com/<your-username>/projects.git
cd projects/digital-twin-project
```

2. **Install dependencies:**

```bash
pip install flask matplotlib
```

3. **Run the fake data generator (in one terminal):**

```bash
python insert_data.py
```

4. **Run the Flask app (in another terminal):**

```bash
python app.py
```

5. **Open in browser:**

* `http://127.0.0.1:5000/get_data` → JSON history
* `http://127.0.0.1:5000/latest` → Latest reading + status
* `http://127.0.0.1:5000/dashboard` → Dashboard with table + live chart

---

## 👨‍💻 Author

**Name:** Milan
**Degree:** B.Tech CSE (2024–2028)
**Focus Areas:** IoT, Blockchain, Cybersecurity

---

✅ **Optional Enhancements for GitHub:**

* Add a GIF showing live dashboard updates
* Include a `requirements.txt` for easy dependency installation
* Add badges for GitHub license, issues, or stars if relevant

