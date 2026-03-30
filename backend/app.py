from flask import Flask, render_template
from flask_socketio import SocketIO
from database import get_logs, get_alerts

# 🔥 NEW IMPORTS (for real-time updates)
import threading
import time

# ✅ IMPORTANT FIX (frontend path)
app = Flask(__name__,
            template_folder="../frontend/templates",
            static_folder="../frontend/static")

socketio = SocketIO(app)


@app.route("/")
def index():
    logs = get_logs()
    alerts = get_alerts()  # 🚨 alerts also

    return render_template("dashboard.html",
                           logs=logs,
                           alerts=alerts)


# 🔥 SOCKET CONNECTION
@socketio.on("connect")
def handle_connect():
    print("Client connected")


# 🔥 REAL-TIME UPDATE FUNCTION (NEW)
def send_updates():
    while True:
        try:
            logs = get_logs()
            alerts = get_alerts()

            socketio.emit("update_data", {
                "logs": logs,
                "alerts": alerts
            })

            time.sleep(5)  # update every 5 seconds

        except Exception as e:
            print("Update Error:", e)


# 🚀 START SERVER
if __name__ == "__main__":

    # 🔥 Start background thread
    thread = threading.Thread(target=send_updates)
    thread.daemon = True
    thread.start()

    socketio.run(app, debug=True)
