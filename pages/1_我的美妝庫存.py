import streamlit as st
from database import init_db
from product_service import add_product, get_all_products, update_product_status, delete_product

init_db()
st.title("📦 我的美妝庫存")

with st.expander("➕ 新增一筆美妝產品"):
    with st.form("add_product_form"):
        name = st.text_input("產品名稱 *")
        brand = st.text_input("品牌")
        category = st.selectbox("類別", ["底妝", "眼妝", "唇彩", "腮紅/修容", "保養品", "其他"])
        shade = st.text_input("色號/規格")
        price = st.number_input("價格 (NT$)", min_value=0, value=0)
        expiry_date = st.date_input("有效期限", value=None)
        notes = st.text_area("備忘筆記")
        
        submitted = st.form_submit_button("確認新增")
        if submitted:
            if name:
                exp_str = expiry_date.strftime("%Y-%m-%d") if expiry_date else None
                add_product(name=name, category=category, brand=brand, shade=shade, expiry_date=exp_str, price=price, notes=notes)
                st.success(f"成功新增產品：{name}！")
                st.rerun()
            else:
                st.error("請至少填寫產品名稱！")

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
