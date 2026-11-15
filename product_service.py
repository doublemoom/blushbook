import sqlite3

DB_NAME = "blushbook.db"

def get_all_products():
    """取得所有美妝庫存產品"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            expiry_date TEXT,
            notes TEXT
        )
    ''')
    cursor.execute("SELECT id, name, category, expiry_date, notes FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_product(name, category, expiry_date, notes=""):
    """新增一筆美妝產品到資料庫"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            expiry_date TEXT,
            notes TEXT
        )
    ''')
    cursor.execute(
        "INSERT INTO products (name, category, expiry_date, notes) VALUES (?, ?, ?, ?)",
        (name, category, expiry_date, notes)
    )
    conn.commit()
    conn.close()

def update_product_status(product_id, status):
    """預留的狀態更新函數（防範導入錯誤）"""
    pass
