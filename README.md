# 🔐 JA4 Traffic Monitor

A cybersecurity tool for identifying applications from encrypted TLS traffic using JA4 fingerprinting.

---

## 🚀 Features

* 🔐 TLS traffic capture
* 🧠 JA4 fingerprint generation
* 📊 Application identification
* 🚨 Threat detection alerts
* 💻 Real-time dashboard visualization

---

## 🛠 Tech Stack

* Python (Scapy, Flask, Socket.IO)
* SQLite
* Chart.js
* Pandas

---

## 📥 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Tauseefkazmi02/ja4-traffic-monitor.git
cd ja4-traffic-monitor
```

---

### 2️⃣ Create Virtual Environment

#### 🐧 Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 🪟 Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

### 🔐 Start Packet Capture (Terminal 1)

#### Linux / macOS

```bash
sudo venv/bin/python backend/capture.py
```

#### Windows (Run as Administrator)

```bash
python backend/capture.py
```

---

### 🌐 Start Dashboard (Terminal 2)

```bash
cd backend
python app.py
```

---

### 🌍 Open in Browser

```
http://127.0.0.1:5000
```

---

## 📂 Project Structure

```
ja4-traffic-monitor/
│
├── backend/
│   ├── app.py              # Flask dashboard server
│   ├── capture.py          # Packet capture engine
│   ├── ja4_engine.py       # JA4 fingerprint logic
│   ├── database.py         # SQLite operations
│   ├── threat_detection.py # Alert system
│   └── fingerprint_db.csv  # Known fingerprints
│
├── frontend/
│   ├── templates/
│   │   └── dashboard.html
│   └── static/
│
├── requirements.txt
└── README.md
```

---

## ⚠️ Important Notes

* 🔑 Packet capture requires **admin/root privileges**
* 🌐 Cloud deployment only supports dashboard (not capture)
* 🔒 Works on **Windows, Linux, macOS**

---

## 🎯 Objective

To identify applications from encrypted network traffic **without decrypting data**, using JA4 fingerprinting and behavioral analysis.

---

## 👨‍💻 Author

**Tauseef Kazmi**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

