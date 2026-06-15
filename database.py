import sqlite3
from config import DATABASE

def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        risk INTEGER,
        result TEXT,
        email TEXT
    )
    """)
    conn.close()