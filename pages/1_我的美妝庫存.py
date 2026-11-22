import streamlit as st
from database import init_db
from product_service import add_product, get_all_products, update_product_status, delete_product

init_db()
st.title("📦 我的美妝庫存")


def add_product(
    name,
    category,
    brand=None,
    shade=None,
    purchase_date=None,
    opened_date=None,
    expiry_date=None,
    pao_months=None,
    reminder_days=30,
    price=None,
    notes=None
):
    with closing(get_connection()) as conn:
        with conn:
            cursor = conn.execute("""
                INSERT INTO products (
                    name, category, brand, shade,
                    purchase_date, opened_date, expiry_date,
                    pao_months, reminder_days, price, notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                name, category, brand, shade,
                purchase_date, opened_date, expiry_date,
                pao_months, reminder_days, price, notes
            ))
            return cursor.lastrowid


st.divider()
st.subheader("📋 使用中的產品清單")
products = get_all_products(status="using")

if not products:
    st.info("目前沒有使用中的產品，快去上方新增一個吧！")
else:
    for p in products:
        cols = st.columns([3, 2, 2, 1])
        with cols[0]:
            st.markdown(f"**{p['name']}**")
            if p['brand']:
                st.caption(f"品牌: {p['brand']} | 色號: {p['shade'] or '無'}")
        with cols[1]:
            st.text(f"類別: {p['category']}")
            st.text(f"到期日: {p['expiry_date'] or '未設定'}")
        with cols[2]:
            if st.button("標記為用完", key=f"finish_{p['product_id']}"):
                update_product_status(p['product_id'], "finished")
                st.rerun()
        with cols[3]:
            if st.button("刪除", key=f"del_{p['product_id']}"):
                delete_product(p['product_id'])
                st.rerun()
        st.divider()

purchase_date = st.date_input(
    "購買日期",
    value=None
)

opened_date = st.date_input(
    "開封日期",
    value=None
)

pao_months = st.number_input(
    "開封後使用期限（個月）",
    min_value=0,
    value=0
)

reminder_days = st.number_input(
    "到期前幾天提醒",
    min_value=0,
    value=30
)
