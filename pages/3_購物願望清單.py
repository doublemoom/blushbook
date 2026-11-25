# --- 3. 購物願望清單 ---
import streamlit as st

from database import init_db
from product_service import add_product, get_all_products
from wishlist_service import (
    add_to_wishlist,
    compare_with_products,
    delete_from_wishlist,
    get_wishlist,
)

st.set_page_config(page_title="購物願望清單", page_icon="🛍️", layout="wide")
init_db()

# --- 3. 購物願望清單 ---
st.subheader("🛍️ 購物願望清單與相似產品比對")
with st.form("wish_form", clear_on_submit=True):
    w_name = st.text_input("產品名稱 *")
    w_brand = st.text_input("品牌")
    w_category = st.selectbox(
        "類別", ["底妝", "眼妝", "唇彩", "腮紅", "保養", "其他"], key="w_cat"
    )
    w_shade = st.text_input("色號或色系")
    w_price = st.number_input("參考價格 (NT$)", min_value=0, step=10, value=0)
    w_url = st.text_input("商品網址")
    w_notes = st.text_area("購買原因或備註")

    if st.form_submit_button("加入願望清單"):
        if not w_name.strip():
            st.error("請填寫產品名稱。")
        else:
            add_to_wishlist(
                name=w_name.strip(),
                brand=w_brand.strip() or None,
                category=w_category,
                shade=w_shade.strip() or None,
                price=int(w_price),
                product_url=w_url.strip() or None,
                notes=w_notes.strip() or None,
            )
            st.success("已加入願望清單！")
            st.rerun()

st.divider()

wishlist_items = get_wishlist()
all_products = get_all_products()

if not wishlist_items:
    st.info("願望清單目前是空的。")
else:
    for item in wishlist_items:
        cmp_result = compare_with_products(item, all_products)
        cols = st.columns([3, 2, 1])
        with cols[0]:
            st.markdown(f"**{item['name']}**（{item['brand'] or '未填寫品牌'}）")
            st.caption(
                f"類別：{item['category'] or '未填'}｜色號：{item['shade'] or '未填'}｜比對結果：**{cmp_result}**"
            )
            if item.get("product_url"):
                st.markdown(f"[商品網址]({item['product_url']})")
            if item.get("notes"):
                st.caption(f"備註：{item['notes']}")
        with cols[1]:
            st.write(f"參考價格：NT$ {item['price'] if item['price'] is not None else 0}")
        with cols[2]:
            if st.button("轉為庫存", key=f"to_inv_{item['wishlist_id']}"):
                add_product(
                    name=item["name"],
                    brand=item.get("brand"),
                    category=item.get("category") or "其他",
                    shade=item.get("shade"),
                    price=item.get("price"),
                    notes=item.get("notes"),
                )
                delete_from_wishlist(item["wishlist_id"])
                st.rerun()
            if st.button("刪除", key=f"del_w_{item['wishlist_id']}"):
                delete_from_wishlist(item["wishlist_id"])
                st.rerun()
        st.divider()

