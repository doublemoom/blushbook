from database import get_connection
from contextlib import closing

def add_product(name, category, brand=None, shade=None, purchase_date=None, opened_date=None, expiry_date=None, pao_months=None, price=None, notes=None):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute("""
                INSERT INTO products (name, category, brand, shade, purchase_date, opened_date, expiry_date, pao_months, price, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, category, brand, shade, purchase_date, opened_date, expiry_date, pao_months, price, notes))
            return cursor.lastrowid

def get_all_products(status="using"):
    with closing(get_connection()) as conn:
        cursor = conn.execute("SELECT * FROM products WHERE status = ? ORDER BY created_at DESC", (status,))
        return [dict(row) for row in cursor.fetchall()]

def update_product_status(product_id, new_status):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("UPDATE products SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE product_id = ?", (new_status, product_id))

def delete_product(product_id):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
