import sqlite3

DB_NAME = "blushbook.db"

def init_db():
    """初始化資料庫與所有必要的資料表"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 產品庫存表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            expiry_date TEXT,
            notes TEXT
        )
    ''')
    
    # 購物願望清單表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wishlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL,
            store TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
