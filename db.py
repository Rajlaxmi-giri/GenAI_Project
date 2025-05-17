import sqlite3
from datetime import datetime

DB_FILE = "db.sqlite"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        user_query TEXT,
        response TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

def log_interaction(log_type: str, user_query: str, response: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO logs (type, user_query, response, timestamp)
    VALUES (?, ?, ?, ?)
    """, (log_type, user_query, response, datetime.now().isoformat()))

    conn.commit()
    conn.close()

def get_recent_logs(log_type: str = None, limit: int = 10):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT user_query, response, timestamp FROM logs"
    if log_type:
        query += " WHERE type = ? ORDER BY timestamp DESC LIMIT ?"
        cursor.execute(query, (log_type, limit))
    else:
        query += " ORDER BY timestamp DESC LIMIT ?"
        cursor.execute(query, (limit,))

    logs = cursor.fetchall()
    conn.close()
    return logs

#Run once to initialize
#init_db()
