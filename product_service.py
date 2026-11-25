from contextlib import closing
from database import get_connection


def add_product(
    name,
    category="其他",
    brand=None,
    shade=None,
    purchase_date=None,
    opened_date=None,
    expiry_date=None,
    pao_months=None,
    reminder_days=30,
    price=None,
    notes=None,
):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO products (
                    name, brand, category, shade,
                    purchase_date, opened_date, expiry_date,
                    pao_months, reminder_days, price, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    brand,
                    category,
                    shade,
                    purchase_date,
                    opened_date,
                    expiry_date,
                    pao_months,
                    reminder_days,
                    price,
                    notes,
                ),
            )
            return cursor.lastrowid


def get_all_products(status=None):
    with closing(get_connection()) as conn:
        if status:
            cursor = conn.execute(
                "SELECT * FROM products WHERE status = ? ORDER BY product_id DESC",
                (status,),
            )
        else:
            cursor = conn.execute("SELECT * FROM products ORDER BY product_id DESC")
        return [dict(row) for row in cursor.fetchall()]


def update_product(
    product_id,
    name,
    brand=None,
    category="其他",
    shade=None,
    purchase_date=None,
    opened_date=None,
    expiry_date=None,
    pao_months=None,
    reminder_days=30,
    price=None,
    notes=None,
):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute(
                """
                UPDATE products
                SET name = ?,
                    brand = ?,
                    category = ?,
                    shade = ?,
                    purchase_date = ?,
                    opened_date = ?,
                    expiry_date = ?,
                    pao_months = ?,
                    reminder_days = ?,
                    price = ?,
                    notes = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE product_id = ?
                """,
                (
                    name,
                    brand,
                    category,
                    shade,
                    purchase_date,
                    opened_date,
                    expiry_date,
                    pao_months,
                    reminder_days,
                    price,
                    notes,
                    product_id,
                ),
            )


def update_product_status(product_id, new_status):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute(
                """
                UPDATE products
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE product_id = ?
                """,
                (new_status, product_id),
            )


def delete_product(product_id):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
