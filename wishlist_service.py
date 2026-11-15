import sqlite3

DB_NAME = "blushbook.db"

def get_wishlist():
    """取得所有願望清單項目"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            store TEXT
        )
    ''')
    cursor.execute("SELECT id, name, price, store FROM wishlist")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_wishlist_item(name, price, store):
    """新增一筆願望清單項目"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            store TEXT
        )
    ''')
    cursor.execute(
        "INSERT INTO wishlist (name, price, store) VALUES (?, ?, ?)",
        (name, price, store)
    )
    conn.commit()
    conn.close()
