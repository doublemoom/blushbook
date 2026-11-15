import streamlit as st
from database import init_db
from product_service import get_all_products
from expiry_service import calculate_expiry_status

init_db()

st.title("⏳ 期限與提醒追蹤")
st.write("在這裡追蹤你所有美妝保養品的效期狀況，避免放到過期浪費！")

# 取得所有產品
products = get_all_products()

if not products:
    st.info("目前沒有任何美妝品庫存，請先至「我的美妝庫存」頁面新增產品！")
else:
    # 建立一個列表來存放狀態
    expired_count = 0
    warning_count = 0
    normal_count = 0

    st.subheader("📋 產品效期總覽")

    for p in products:
        # p 的結構假設為: (id, name, category, expiry_date, ...) 
        # 根據實際資料庫欄位調整索引，這裡假設 expiry_date 在索引 3 或對應欄位
        # 如果是用 dict 或是 tuple，我們做安全防護：
        try:
            prod_id = p[0]
            name = p[1]
            category = p[2] if len(p) > 2 else "未分類"
            expiry_date = p[3] if len(p) > 3 else "未知"
        except Exception:
            name = str(p)
            expiry_date = "未知"

        status_info = calculate_expiry_status(expiry_date)
        
        # 顯示每一筆產品的效期卡片
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"**{name}** (`{category}`)")
            with col2:
                st.text(f"有效期限: {expiry_date}")
            with col3:
                st.markdown(f"<span style='color:{status_info['color']}'>**{status_info['status']}**</span>", unsafe_allow_html=True)
            st.divider()
