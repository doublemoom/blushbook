i# --- 4. 產品狀態紀錄 ---
import streamlit as st

from database import init_db
from product_service import get_all_products, update_product_status

st.set_page_config(page_title="美妝收藏", page_icon="✨", layout="wide")
init_db()

# --- 4. 產品狀態紀錄 ---
st.subheader("✨ 已用完與已丟棄產品")
finished_list = get_all_products(status="finished")
discarded_list = get_all_products(status="discarded")

st.markdown("### 已用完（finished）")
if not finished_list:
    st.info("尚無已用完產品。")
for p in finished_list:
    c1, c2 = st.columns([4, 1])
    c1.write(f"- **{p['name']}**（{p['brand'] or '未填寫'}｜色號：{p['shade'] or '無'}）")
    if c2.button("改回使用中", key=f"re_fin_{p['product_id']}"):
        update_product_status(p["product_id"], "using")
        st.rerun()

st.divider()
st.markdown("### 已丟棄（discarded）")
if not discarded_list:
    st.info("尚無已丟棄產品。")
for p in discarded_list:
    c1, c2 = st.columns([4, 1])
    c1.write(f"- **{p['name']}**（{p['brand'] or '未填寫'}｜備註：{p['notes'] or '無'}）")
    if c2.button("改回使用中", key=f"re_dis_{p['product_id']}"):
        update_product_status(p["product_id"], "using")
        st.rerun()
