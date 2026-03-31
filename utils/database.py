import sqlite3
import os

def save_to_db(records, db_path="data/osint.db"):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS osint_data (
            platform TEXT,
            user TEXT,
            timestamp TEXT,
            text TEXT,
            url TEXT,
            sentiment REAL
        )
    """)
    for r in records:
        cur.execute(
            "INSERT INTO osint_data VALUES (?, ?, ?, ?, ?, ?)",
            (r["platform"], r["user"], r["timestamp"], r["text"], r["url"], r.get("sentiment", 0.0))
        )
    conn.commit()
    conn.close()

def load_from_db(db_path="data/osint.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    # Ensure the table is created if this is the very first access
    cur.execute("""
        CREATE TABLE IF NOT EXISTS osint_data (
            platform TEXT,
            user TEXT,
            timestamp TEXT,
            text TEXT,
            url TEXT,
            sentiment REAL
        )
    """)
    cur.execute("SELECT platform, user, timestamp, text, sentiment, url FROM osint_data")
    rows = cur.fetchall()
    conn.close()
    return rows
