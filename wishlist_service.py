from contextlib import closing
from database import get_connection


def _norm(text):
    if not text:
        return ""
    return str(text).strip().lower()


def compare_with_products(wish_item, existing_products):
    w_name = _norm(wish_item.get("name"))
    w_brand = _norm(wish_item.get("brand"))
    w_cat = _norm(wish_item.get("category"))
    w_shade = _norm(wish_item.get("shade"))

    has_same_brand_cat_shade = False
    has_same_brand_cat_diff_shade = False

    for p in existing_products:
        p_name = _norm(p.get("name"))
        p_brand = _norm(p.get("brand"))
        p_cat = _norm(p.get("category"))
        p_shade = _norm(p.get("shade"))

        if w_name and p_name == w_name and w_brand and p_brand == w_brand:
            if not w_shade or not p_shade or p_shade == w_shade:
                return "可能重複"

        if w_brand and w_cat and p_brand == w_brand and p_cat == w_cat:
            if w_shade and p_shade and p_shade == w_shade:
                has_same_brand_cat_shade = True
            elif w_shade and p_shade and p_shade != w_shade:
                has_same_brand_cat_diff_shade = True

    if has_same_brand_cat_shade:
        return "可能重複"
    if has_same_brand_cat_diff_shade:
        return "同品牌同類別，請確認色系"
    if not w_brand and not w_cat:
        return "無法充分比對"
    return "無明顯重複"


def add_to_wishlist(
    name, brand=None, category=None, shade=None, price=None, product_url=None, notes=None
):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO wishlist (
                    name, brand, category, shade, price, product_url, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, brand, category, shade, price, product_url, notes),
            )
            return cursor.lastrowid


def get_wishlist():
    with closing(get_connection()) as conn:
        cursor = conn.execute("SELECT * FROM wishlist ORDER BY wishlist_id DESC")
        return [dict(row) for row in cursor.fetchall()]


def delete_from_wishlist(wishlist_id):
    with closing(get_connection()) as conn:
        with conn:
            conn.execute("DELETE FROM wishlist WHERE wishlist_id = ?", (wishlist_id,))
