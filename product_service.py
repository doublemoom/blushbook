import sqlite3

DB_NAME = "blushbook.db"

def get_all_products(status=None):
    """取得所有美妝庫存產品（支援狀態篩選，若無則回傳全部）"""
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

def delete_product(product_id):
    """根據 ID 刪除產品"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
