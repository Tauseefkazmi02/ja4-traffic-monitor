from collections import defaultdict
import time

# Track requests per IP
ip_time = defaultdict(list)

# Example blacklist
blacklist = ["192.168.1.100", "10.0.0.66"]

THRESHOLD = 20      # max requests
TIME_WINDOW = 10    # seconds


def detect_threat(src, ja4, app):
    alerts = []

    # 1️⃣ Unknown traffic
    if app == "Unknown":
        alerts.append("Unknown Application Traffic")

    # 2️⃣ Blacklisted IP
    if src in blacklist:
        alerts.append("Blacklisted IP Detected")

    # 3️⃣ Traffic spike detection
    now = time.time()
    ip_time[src].append(now)

    # keep only recent timestamps
    ip_time[src] = [t for t in ip_time[src] if now - t < TIME_WINDOW]

    if len(ip_time[src]) > THRESHOLD:
        alerts.append("High Traffic Spike (Possible DDoS)")

    return alerts
