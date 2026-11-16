from database import init_db, get_connection

init_db()

with get_connection() as conn:
    conn.execute("""
        INSERT INTO products (name, category, brand, shade)
        VALUES (?, ?, ?, ?)
    """, ("測試眼影盤", "眼妝", "Test Brand", "01"))

    rows = conn.execute(
        "SELECT product_id, name, category FROM products"
    ).fetchall()

    for row in rows:
        print(dict(row))
