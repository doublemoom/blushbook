from database import get_connection
from contextlib import closing

def add_to_wishlist(name, brand=None, category=None, shade=None, price=None, product_url=None, notes=None):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute("""
                INSERT INTO wishlist (name, brand, category, shade, price, product_url, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, brand, category, shade, price, product_url, notes))
            return cursor.lastrowid

def get_wishlist():
    with closing(get_connection()) as conn:
        cursor = conn.execute("SELECT * FROM wishlist ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

def delete_from_wishlist(wishlist_id):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("DELETE FROM wishlist WHERE wishlist_id = ?", (wishlist_id,))
