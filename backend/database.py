import sqlite3
from datetime import datetime

DB = "traffic.db"

# =======================
# 📦 LOG TABLE
# =======================

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        src TEXT,
        dst TEXT,
        ja4 TEXT,
        app TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_log(src, dst, ja4, app):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO logs (time, src, dst, ja4, app)
    VALUES (?, ?, ?, ?, ?)
    """, (datetime.now(), src, dst, ja4, app))

    conn.commit()
    conn.close()


def get_logs():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 50")
    data = cur.fetchall()

    conn.close()
    return data


# =======================
# 🚨 ALERT TABLE
# =======================

def init_alert_table():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        src TEXT,
        dst TEXT,
        alert TEXT
    )
    """)

    conn.commit()
    conn.close()


def insert_alert(src, dst, alert):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO alerts (time, src, dst, alert)
    VALUES (?, ?, ?, ?)
    """, (datetime.now(), src, dst, alert))

    conn.commit()
    conn.close()


def get_alerts():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT 20")
    data = cur.fetchall()

    conn.close()
    return data
