import streamlit as st
from database import init_db
from wishlist_service import add_to_wishlist, get_wishlist, delete_from_wishlist

init_db()
st.title("🛍️ 購物願望清單")

with st.expander("➕ 新增願望清單項目"):
    with st.form("wish_form"):
        name = st.text_input("產品名稱 *")
        brand = st.text_input("品牌")
        category = st.selectbox("類別", ["底妝", "眼妝", "唇彩", "腮紅/修容", "保養品", "其他"])
        shade = st.text_input("色號")
        price = st.number_input("預估價格 (NT$)", min_value=0, value=0)
        product_url = st.text_input("商品網址")
        notes = st.text_area("備忘/心得")

        submitted = st.form_submit_button("加入願望清單")
        if submitted:
            if name:
                add_to_wishlist(name=name, brand=brand, category=category, shade=shade, price=price, product_url=product_url, notes=notes)
                st.success(f"成功加入願望清單：{name}！")
                st.rerun()
            else:
                st.error("請至少填寫產品名稱！")

st.divider()
items = get_wishlist()
if not items:
    st.info("願望清單目前是空的。")
else:
    for item in items:
        cols = st.columns([3, 2, 1])
        with cols[0]:
            st.markdown(f"**{item['name']}** ({item['brand'] or '無品牌'})")
            if item['product_url']:
                st.markdown(f"[商品連結]({item['product_url']})")
        with cols[1]:
            st.text(f"預估價格: NT${item['price'] or 0}")
        with cols[2]:
            if st.button("刪除", key=f"del_wish_{item['wishlist_id']}"):
                delete_from_wishlist(item['wishlist_id'])
                st.rerun()
        st.divider()
