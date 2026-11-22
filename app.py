import streamlit as st
from database import init_db
from product_service import get_all_products
from wishlist_service import get_wishlist

init_db()

st.set_page_config(page_title="BlushBook 美妝管理", page_icon="💄", layout="wide")

st.title("💄 BlushBook 美妝與保養品管理系統")
st.write("歡迎使用您的專屬美妝庫存與願望清單小幫手！請從左側選單切換不同功能頁面。")

col1, col2 = st.columns(2)
try:
    using_products = get_all_products(status="using")
    wishlist_items = get_wishlist()

    with col1:
        st.metric("目前使用中的產品數量", len(using_products))
    with col2:
        st.metric("願望清單收藏數量", len(wishlist_items))
except Exception as e:
    st.info("資料載入中...")

st.divider()
st.subheader("💡 系統功能簡介")
st.markdown("""
- **1_我的美妝庫存**: 管理手邊正在使用、已用完或丟棄的化妝品與保養品。
- **2_期限追蹤**: 檢查產品是否即將過期，避免放到過期浪費。
- **3_購物願望清單**: 記錄看到想買的美妝，防止衝動購物。
- **4_美妝收藏**: 查看其他收藏備忘。
""")
