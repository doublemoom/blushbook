import sqlite3

DB_NAME = "blushbook.db"

def get_all_products():
    """取得所有美妝庫存產品"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, expiry_date, notes FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_product(name, category, expiry_date, notes=""):
    """新增一筆美妝產品"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category, expiry_date, notes) VALUES (?, ?, ?, ?)",
        (name, category, expiry_date, notes)
    )
    conn.commit()
    conn.close()

def delete_product(product_id):
    """刪除指定 ID 的產品"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
