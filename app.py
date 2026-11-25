from datetime import date

import streamlit as st

from database import init_db
from expiry_service import get_expiry_status
from product_service import get_all_products
from wishlist_service import get_wishlist

st.set_page_config(
    page_title="BlushBook | 我的美妝手帳",
    page_icon="💄",
    layout="wide",
)
init_db()

st.title("💄 BlushBook | 我的美妝手帳")
st.caption("記錄你的美妝，管理你的收藏。")

using_products = get_all_products(status="using")
wishlist_items = get_wishlist()

expiring_or_expired_count = 0
for p in using_products:
    info = get_expiry_status(
        today=date.today(),
        expiry_date=p.get("expiry_date"),
        opened_date=p.get("opened_date"),
        pao_months=p.get("pao_months"),
        reminder_days=p.get("reminder_days") or 30,
    )
    if info["status"] in ("即將到期", "已超過記錄期限"):
        expiring_or_expired_count += 1

m1, m2, m3 = st.columns(3)
m1.metric("使用中產品", len(using_products))
m2.metric("需留意期限（使用中）", expiring_or_expired_count)
m3.metric("願望清單", len(wishlist_items))

st.divider()

nav_cols = st.columns(4)
with nav_cols[0]:
    st.page_link("pages/1_我的美妝庫存.py", label="我的美妝庫存", icon="📦")
with nav_cols[1]:
    st.page_link("pages/2_期限追蹤.py", label="期限追蹤", icon="⏳")
with nav_cols[2]:
    st.page_link("pages/3_購物願望清單.py", label="購物願望清單", icon="🛍️")
with nav_cols[3]:
    st.page_link("pages/4_美妝收藏.py", label="美妝收藏", icon="✨")
