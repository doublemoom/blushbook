# database.py
import sqlite3
from pathlib import Path

# 設定資料庫檔案路徑
DB_PATH = Path(__file__).resolve().parent / "blushbook.db"

def get_connection():
    """建立並回傳 SQLite 資料庫連線，啟用 Row Factory 與外鍵約束"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """初始化資料庫，建立 products 與 wishlist 資料表"""
    with get_connection() as conn:
        # 1. 產品資料表 (products)[cite: 1, 6, 7]
        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT NOT NULL,
            shade TEXT,
            purchase_date TEXT,
            opened_date TEXT,
            expiry_date TEXT,
            pao_months INTEGER,
            reminder_days INTEGER NOT NULL DEFAULT 30,
            status TEXT NOT NULL DEFAULT 'using'
                CHECK (status IN ('using', 'finished', 'discarded')),
            price INTEGER,
            image_path TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # 2. 購物願望清單資料表 (wishlist)[cite: 2, 7, 8]
        # (已修正原 PDF 範例中的拼寫錯誤、句號誤用與缺少括號的問題)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS wishlist (
            wishlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT,
            category TEXT,
            shade TEXT,
            price INTEGER,
            product_url TEXT,
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """)

if __name__ == "__main__":
    init_db()
    print("資料表建立完成！")

# wishlist_service.py
from database import get_connection

def add_to_wishlist(name, brand="", category="", shade="", price=0, product_url="", notes=""):
    """新增一筆願望清單項目，使用參數佔位符以防範 SQL Injection[cite: 9]"""
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO wishlist (name, brand, category, shade, price, product_url, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, brand, category, shade, price, product_url, notes))

def get_wishlist():
    """取得所有願望清單項目，依照 wishlist_id 降冪排序（最新的在最上面）"""
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT * 
            FROM wishlist 
            ORDER BY wishlist_id DESC
        """).fetchall()
        return [dict(row) for row in rows]

def delete_from_wishlist(wishlist_id):
    """根據 wishlist_id 刪除指定的願望清單項目"""
    with get_connection() as conn:
        conn.execute("""
            DELETE FROM wishlist 
            WHERE wishlist_id = ?
        """, (wishlist_id,))

# pages/3_購物願望清單.py
import streamlit as st
from database import init_db
from wishlist_service import add_to_wishlist, get_wishlist, delete_from_wishlist

# 初始化資料庫
init_db()

st.title("🛍️ 購物願望清單")

# 新增表單區塊
with st.expander("➕ 新增願望清單項目"):
    with st.form("wish_form"):
        name = st.text_input("產品名稱 *")
        brand = st.text_input("品牌")
        category = st.selectbox("類別", ["底妝", "眼妝", "唇彩", "腮紅/修容", "保養品", "其他"])
        shade = st.text_input("色號")  # 補上符合企劃書規格的色號欄位[cite: 2]
        price = st.number_input("預估價格 (NT$)", min_value=0, value=0)
        product_url = st.text_input("商品網址")
        notes = st.text_area("備忘/心得")
        
        submitted = st.form_submit_button("加入願望清單")
        if submitted:
            if name.strip():
                add_to_wishlist(
                    name=name.strip(),
                    brand=brand.strip(),
                    category=category,
                    shade=shade.strip(),
                    price=price,
                    product_url=product_url.strip(),
                    notes=notes.strip()
                )
                st.success(f"成功加入願望清單：{name}！")
                st.rerun()
            else:
                st.error("請至少填寫產品名稱！")

st.divider()

# 顯示清單內容
items = get_wishlist()
if not items:
    st.info("願望清單目前是空的。")
else:
    for item in items:
        cols = st.columns([3, 2, 1])
        with cols[0]:
            shade_text = f" - 色號: {item['shade']}" if item['shade'] else ""
            st.markdown(f"**{item['name']}** ({item['brand'] or '無品牌'}{shade_text})")
            if item['notes']:
                st.caption(f"備註：{item['notes']}")
            if item['product_url']:
                st.markdown(f"[商品連結]({item['product_url']})")
        with cols[1]:
            st.text(f"預估價格: NT${item['price'] or 0}")
        with cols[2]:
            if st.button("刪除", key=f"del_wish_{item['wishlist_id']}"):
                delete_from_wishlist(item['wishlist_id'])
                st.rerun()
        st.divider()
