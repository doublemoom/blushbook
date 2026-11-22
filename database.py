import sqlite3
from pathlib import Path

try:
    DB_PATH = Path(__file__).resolve().parent / "blushbook.db"
except NameError:
    DB_PATH = Path("blushbook.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brand TEXT,
                category TEXT NOT NULL,
                shade TEXT,
                purchase_date TEXT,
                opened_date TEXT,
                expiry_date TEXT,
                pao_months INTEGER,
                reminder_days INTEGER NOT NULL DEFAULT 30,
                status TEXT NOT NULL DEFAULT 'using'
                    CHECK (status IN ('using', 'finished', 'discarded')),
                price INTEGER,
                image_path TEXT,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wishlist (
                wishlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                brand TEXT,
                category TEXT,
                shade TEXT,
                price INTEGER,
                product_url TEXT,
                notes TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        setting_key TEXT PRIMARY KEY,
        setting_value TEXT
    )
""")

if __name__ == "__main__":
    init_db()
