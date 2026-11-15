import streamlit as st
from database import init_db
from product_service import add_product, get_all_products, delete_product

init_db()

st.title("📦 我的美妝庫存")
st.write("在這裡管理妳手邊所有的美妝與保養品。")

with st.form("product_form"):
    st.subheader("➕ 新增一筆美妝產品")
    name = st.text_input("產品名稱")
    category = st.selectbox("產品分類", ["保養品", "底妝", "彩妝", "香氛", "其他"])
    expiry_date = st.date_input("有效期限")
    notes = st.text_area("備註說明")
    
    submitted = st.form_submit_button("確認新增")
    if submitted and name:
        add_product(name, category, str(expiry_date), notes)
        st.success(f"成功新增產品：{name}！")
        st.rerun()

st.divider()
st.subheader("📋 目前的庫存清單")

products = get_all_products()

if not products:
    st.info("目前沒有任何美妝庫存，快去上方新增一個吧！")
else:
    for p in products:
        prod_id, name, category, expiry_date, notes = p
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.markdown(f"**{name}** (`{category}`)")
        with col2:
            st.text(f"期限: {expiry_date}")
        with col3:
            st.text(f"備註: {notes if notes else '無'}")
        with col4:
            if st.button("刪除", key=f"del_{prod_id}"):
                delete_product(prod_id)
                st.rerun()
        st.divider()
