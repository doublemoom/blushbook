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


def _submit_wishlist():
    name_val = (st.session_state.get("w_name") or "").strip()
    if not name_val:
        st.session_state["wish_feedback"] = ("error", "請填寫產品名稱。")
        return

    add_to_wishlist(
        name=name_val,
        brand=(st.session_state.get("w_brand") or "").strip() or None,
        category=st.session_state.get("w_cat") or "其他",
        shade=(st.session_state.get("w_shade") or "").strip() or None,
        price=int(st.session_state.get("w_price") or 0),
        product_url=(st.session_state.get("w_url") or "").strip() or None,
        notes=(st.session_state.get("w_notes") or "").strip() or None,
    )
    st.session_state["w_name"] = ""
    st.session_state["w_brand"] = ""
    st.session_state["w_cat"] = "底妝"
    st.session_state["w_shade"] = ""
    st.session_state["w_price"] = 0
    st.session_state["w_url"] = ""
    st.session_state["w_notes"] = ""
    st.session_state["wish_feedback"] = ("success", "已加入願望清單！")


# --- 3. 購物願望清單 ---
st.subheader("🛍️ 購物願望清單與相似產品比對")

st.text_input("產品名稱 *", key="w_name")
st.text_input("品牌", key="w_brand")
st.selectbox(
    "類別", ["底妝", "眼妝", "唇彩", "腮紅", "保養", "其他"], key="w_cat"
)
st.text_input("色號或色系", key="w_shade")
st.number_input("參考價格 (NT$)", min_value=0, step=10, value=0, key="w_price")
st.text_input("商品網址", key="w_url")
st.text_area("購買原因或備註", key="w_notes")

st.button("加入願望清單", type="primary", on_click=_submit_wishlist)

feedback = st.session_state.pop("wish_feedback", None)
if feedback:
    kind, msg = feedback
    if kind == "error":
        st.error(msg)
    else:
        st.success(msg)

st.divider()

wishlist_items = get_wishlist()
all_products = get_all_products()

keyword = st.text_input(
    "搜尋願望清單（產品名稱、品牌或色號）",
    key="search_wishlist",
).strip().lower()

filtered_items = [
    item
    for item in wishlist_items
    if not keyword
    or keyword in (item.get("name") or "").lower()
    or keyword in (item.get("brand") or "").lower()
    or keyword in (item.get("shade") or "").lower()
]

if not filtered_items:
    st.info("目前沒有符合條件的願望清單項目。")
else:
    for item in filtered_items:
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
