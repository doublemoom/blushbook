import streamlit as st
from database import init_db
from product_service import get_all_products

init_db()

st.title("⏳ 期限與提醒追蹤")
st.write("在這裡追蹤妳所有美妝保養品的效期狀況，避免放到過期浪費！")

products = get_all_products()

if not products:
    st.info("目前沒有任何美妝品庫存，請先至「我的美妝庫存」頁面新增產品！")
else:
    st.subheader("📋 產品效期總覽")
    for p in products:
        prod_id, name, category, expiry_date, notes = p
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**{name}** (`{category}`)")
            with col2:
                st.text(f"有效期限: {expiry_date}")
            with col3:
                st.markdown("<span style='color:green'>**正常使用中**</span>", unsafe_allow_html=True)
            st.divider()
