from datetime import date, datetime
import streamlit as st
from database import init_db
from expiry_service import get_expiry_status
from product_service import (
    add_product,
    delete_product,
    get_all_products,
    update_product,
    update_product_status,
)
from wishlist_service import (
    add_to_wishlist,
    compare_with_products,
    delete_from_wishlist,
    get_wishlist,
)

init_db()
st.set_page_config(
    page_title="BlushBook | 我的美妝手帳",
    page_icon="💄",
    layout="wide",
)


def _to_date_or_none(val):
    if not val:
        return None
    try:
        return datetime.strptime(str(val)[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def _to_str_or_none(d):
    return d.isoformat() if d else None


ADD_DEFAULTS = {
    "add_name": "",
    "add_brand": "",
    "add_category": "底妝",
    "add_shade": "",
    "add_price": 0,
    "add_know_purchase": False,
    "add_purchase_date": None,
    "add_know_opened": False,
    "add_opened_date": None,
    "add_know_expiry": False,
    "add_expiry_date": None,
    "add_pao_months": 0,
    "add_reminder_days": 30,
    "add_notes": "",
}


def _handle_add_product():
    raw_name = (st.session_state.get("add_name") or "").strip()
    if not raw_name:
        st.session_state["add_feedback"] = ("error", "請填寫產品名稱。")
        return

    add_product(
        name=raw_name,
        brand=(st.session_state.get("add_brand") or "").strip() or None,
        category=st.session_state.get("add_category") or "其他",
        shade=(st.session_state.get("add_shade") or "").strip() or None,
        purchase_date=(
            _to_str_or_none(st.session_state.get("add_purchase_date"))
            if st.session_state.get("add_know_purchase")
            else None
        ),
        opened_date=(
            _to_str_or_none(st.session_state.get("add_opened_date"))
            if st.session_state.get("add_know_opened")
            else None
        ),
        expiry_date=(
            _to_str_or_none(st.session_state.get("add_expiry_date"))
            if st.session_state.get("add_know_expiry")
            else None
        ),
        pao_months=(
            int(st.session_state.get("add_pao_months") or 0)
            if int(st.session_state.get("add_pao_months") or 0) > 0
            else None
        ),
        reminder_days=int(st.session_state.get("add_reminder_days") or 30),
        price=int(st.session_state.get("add_price") or 0),
        notes=(st.session_state.get("add_notes") or "").strip() or None,
    )

    for k, v in ADD_DEFAULTS.items():
        st.session_state[k] = v
    st.session_state["add_feedback"] = ("success", "產品已新增！")


st.title("💄 BlushBook | 我的美妝手帳")
st.caption("記錄你的美妝，管理你的收藏。")

using_products = get_all_products(status="using")
all_products = get_all_products()
wishlist_items = get_wishlist()

expiring_or_expired_count = 0
for p in using_products:
    info = get_expiry_status(
        today=date.today(),
        expiry_date=p.get("expiry_date"),
        opened_date=p.get("opened_date"),
        pao_months=p.get("pao_months"),
        reminder_days=p.get("reminder_days") or 30,
    )
    if info["status"] in ("即將到期", "已超過記錄期限"):
        expiring_or_expired_count += 1

m1, m2, m3 = st.columns(3)
m1.metric("使用中產品", len(using_products))
m2.metric("需留意期限（使用中）", expiring_or_expired_count)
m3.metric("願望清單", len(wishlist_items))

tab1, tab2, tab3, tab4 = st.tabs(
    ["📦 我的美妝庫存", "⏳ 期限追蹤", "🛍️ 購物願望清單", "✨ 產品狀態紀錄"]
)
