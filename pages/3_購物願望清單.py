import streamlit as st
from database import init_db
from wishlist_service import add_wishlist_item, get_wishlist

init_db()

st.title("🛍️ 購物願望清單")
st.write("記錄妳想要入手的美妝保養品，隨時掌握清單與價格！")

with st.form("wishlist_form"):
    st.subheader("➕ 新增心儀美妝")
    item_name = st.text_input("產品名稱")
    item_price = st.number_input("預估價格 (NT$)", min_value=0, value=500)
    item_store = st.text_input("購買通路 / 連結")
    
    submitted = st.form_submit_button("加入願望清單")
    if submitted and item_name:
        add_wishlist_item(item_name, item_price, item_store)
        st.success(f"成功將 「{item_name}」 加入願望清單！")
        st.rerun()

st.divider()
st.subheader("📋 目前的願望清單")

wishlist_items = get_wishlist()

if not wishlist_items:
    st.info("目前願望清單是空的，趕快在上方的表單新增妳想買的美妝品吧！")
else:
    for item in wishlist_items:
        item_id, name, price, store = item
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**{name}**")
            with col2:
                st.text(f"價格: NT$ {price}")
            with col3:
                st.text(f"通路: {store if store else '未填寫'}")
            st.divider()
