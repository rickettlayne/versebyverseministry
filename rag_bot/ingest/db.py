import sqlite3
from contextlib import contextmanager
from datetime import datetime

from .config import SQLITE_PATH

@contextmanager
def get_conn():
    conn = sqlite3.connect(SQLITE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE,
                checksum TEXT,
                last_processed_at TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ingest_log (
                id INTEGER PRIMARY KEY,
                url TEXT,
                event TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()

def log_event(url: str, event: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO ingest_log (url, event, timestamp) VALUES (?, ?, ?)",
            (url, event, datetime.utcnow().isoformat())
        )
        conn.commit()

def get_document(url: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, url, checksum, last_processed_at FROM documents WHERE url = ?", (url,))
        row = cur.fetchone()
        return row

def upsert_document(url: str, checksum: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO documents (url, checksum, last_processed_at)
            VALUES (?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                checksum = excluded.checksum,
                last_processed_at = excluded.last_processed_at
        """, (url, checksum, datetime.utcnow().isoformat()))
        conn.commit()

def clear_all():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM documents")
        cur.execute("DELETE FROM ingest_log")
        conn.commit()
