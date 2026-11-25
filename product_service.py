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

st.set_page_config(page_title="我的美妝庫存", page_icon="💄", layout="wide")
init_db()

ADD_DEFAULTS = {
    "add_name": "",
    "add_brand": "",
    "add_category": "底妝",
    "add_shade": "",
    "add_price": 0,
    "add_know_purchase": False,
    "add_purchase_date": date.today(),
    "add_know_opened": False,
    "add_opened_date": date.today(),
    "add_know_expiry": False,
    "add_expiry_date": date.today(),
    "add_pao_months": 0,
    "add_reminder_days": 30,
    "add_notes": "",
}


def _to_date_or_none(val):
    if val is None or val == "":
        return None
    if isinstance(val, date):
        return val
    try:
        return datetime.fromisoformat(str(val)).date()
    except ValueError:
        return None


def _to_str_or_none(val):
    if val is None or val == "":
        return None
    if isinstance(val, date):
        return val.isoformat()
    return str(val)


def _handle_add_product():
    name = (st.session_state.get("add_name") or "").strip()
    if not name:
        st.session_state["add_feedback"] = ("error", "請輸入產品名稱（* 為必填）。")
        return

    know_purchase = st.session_state.get("add_know_purchase", False)
    know_opened = st.session_state.get("add_know_opened", False)
    know_expiry = st.session_state.get("add_know_expiry", False)
    pao_months = int(st.session_state.get("add_pao_months") or 0)

    add_product(
        name=name,
        brand=(st.session_state.get("add_brand") or "").strip() or None,
        category=st.session_state.get("add_category") or "其他",
        shade=(st.session_state.get("add_shade") or "").strip() or None,
        purchase_date=_to_str_or_none(st.session_state.get("add_purchase_date")) if know_purchase else None,
        opened_date=_to_str_or_none(st.session_state.get("add_opened_date")) if know_opened else None,
        expiry_date=_to_str_or_none(st.session_state.get("add_expiry_date")) if know_expiry else None,
        pao_months=pao_months if pao_months > 0 else None,
        reminder_days=int(st.session_state.get("add_reminder_days") or 30),
        price=int(st.session_state.get("add_price") or 0),
        notes=(st.session_state.get("add_notes") or "").strip() or None,
    )

    for k, v in ADD_DEFAULTS.items():
        st.session_state[k] = v
    st.session_state["add_feedback"] = ("success", f"已新增產品：{name}")


# --- 1. 我的美妝庫存 ---
st.subheader("➕ 新增美妝產品")

for k, v in ADD_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

c1, c2 = st.columns(2)
with c1:
    st.text_input("產品名稱 *", key="add_name")
    st.text_input("品牌", key="add_brand")
    st.selectbox(
        "產品類別",
        ["底妝", "眼妝", "唇彩", "腮紅", "保養", "其他"],
        key="add_category",
    )
    st.text_input("色號/色系", key="add_shade")
    st.number_input("購買價格 (NT$)", min_value=0, step=10, key="add_price")
with c2:
    know_purchase = st.checkbox("已知購買日期", key="add_know_purchase")
    st.date_input("購買日期", disabled=not know_purchase, key="add_purchase_date")

    know_opened = st.checkbox("已知開封日期", key="add_know_opened")
    st.date_input("開封日期", disabled=not know_opened, key="add_opened_date")

    know_expiry = st.checkbox("已知標示有效期限", key="add_know_expiry")
    st.date_input("有效期限", disabled=not know_expiry, key="add_expiry_date")

    st.number_input(
        "開封後建議使用月數 (PAO，0 表示無)",
        min_value=0,
        max_value=120,
        key="add_pao_months",
    )
    st.number_input(
        "提前幾天提醒",
        min_value=1,
        max_value=365,
        key="add_reminder_days",
    )

st.text_area("備註", key="add_notes")

st.button("新增產品", type="primary", on_click=_handle_add_product)

feedback = st.session_state.pop("add_feedback", None)
if feedback:
    level, msg = feedback
    if level == "error":
        st.error(msg)
    else:
        st.success(msg)

st.divider()
st.subheader("📋 使用中的產品")
keyword = st.text_input("搜尋產品名稱、品牌或色號", key="search_using").strip().lower()

using_products = get_all_products("using")

filtered_using = [
    p
    for p in using_products
    if not keyword
    or keyword in (p.get("name") or "").lower()
    or keyword in (p.get("brand") or "").lower()
    or keyword in (p.get("shade") or "").lower()
]

if not filtered_using:
    st.info("目前沒有符合條件的使用中產品。")
else:
    for p in filtered_using:
        pid = p["product_id"]
        exp_info = get_expiry_status(
            today=date.today(),
            expiry_date=p.get("expiry_date"),
            opened_date=p.get("opened_date"),
            pao_months=p.get("pao_months"),
            reminder_days=p.get("reminder_days") or 30,
        )
        cols = st.columns([3, 2, 2])
        with cols[0]:
            st.markdown(f"**{p['name']}**（編號 #{pid}）")
            st.caption(
                f"品牌：{p['brand'] or '未填寫'}｜類別：{p['category']}｜色號：{p['shade'] or '未填寫'}"
            )
            if p.get("notes"):
                st.caption(f"備註：{p['notes']}")
        with cols[1]:
            st.write(f"期限狀態：**{exp_info['status']}**")
            if exp_info["check_date"]:
                st.caption(
                    f"依據日期：{exp_info['check_date']}（剩餘 {exp_info['days_remaining']} 天）"
                )
            st.caption(f"價格：NT$ {p['price'] if p['price'] is not None else 0}")
        with cols[2]:
            b1, b2, b3 = st.columns(3)
            if b1.button("用完", key=f"fin_{pid}"):
                update_product_status(pid, "finished")
                st.rerun()
            if b2.button("丟棄", key=f"dis_{pid}"):
                update_product_status(pid, "discarded")
                st.rerun()
            if b3.button("刪除", key=f"del_{pid}"):
                delete_product(pid)
                st.rerun()

        with st.expander("✏️ 編輯此產品"):
            with st.form(f"edit_form_{pid}"):
                e_name = st.text_input("產品名稱 *", value=p["name"], key=f"ename_{pid}")
                e_brand = st.text_input("品牌", value=p.get("brand") or "", key=f"ebrand_{pid}")
                cat_options = ["底妝", "眼妝", "唇彩", "腮紅", "保養", "其他"]
                cat_idx = cat_options.index(p["category"]) if p["category"] in cat_options else 5
                e_cat = st.selectbox("產品類別", cat_options, index=cat_idx, key=f"ecat_{pid}")
                e_shade = st.text_input("色號/色系", value=p.get("shade") or "", key=f"eshade_{pid}")
                e_price = st.number_input(
                    "購買價格 (NT$)", min_value=0, step=10, value=int(p.get("price") or 0), key=f"eprice_{pid}"
                )
                e_p_date = st.date_input(
                    "購買日期", value=_to_date_or_none(p.get("purchase_date")), key=f"epdate_{pid}"
                )
                e_o_date = st.date_input(
                    "開封日期", value=_to_date_or_none(p.get("opened_date")), key=f"eodate_{pid}"
                )
                e_e_date = st.date_input(
                    "有效期限", value=_to_date_or_none(p.get("expiry_date")), key=f"eedate_{pid}"
                )
                e_pao = st.number_input(
                    "開封後建議使用月數 (PAO)",
                    min_value=0,
                    max_value=120,
                    value=int(p.get("pao_months") or 0),
                    key=f"epao_{pid}",
                )
                e_rem = st.number_input(
                    "提前幾天提醒",
                    min_value=1,
                    max_value=365,
                    value=int(p.get("reminder_days") or 30),
                    key=f"erem_{pid}",
                )
                e_notes = st.text_area("備註", value=p.get("notes") or "", key=f"enotes_{pid}")

                if st.form_submit_button("儲存修改"):
                    if not e_name.strip():
                        st.error("產品名稱不能為空。")
                    else:
                        update_product(
                            product_id=pid,
                            name=e_name.strip(),
                            brand=e_brand.strip() or None,
                            category=e_cat,
                            shade=e_shade.strip() or None,
                            purchase_date=_to_str_or_none(e_p_date),
                            opened_date=_to_str_or_none(e_o_date),
                            expiry_date=_to_str_or_none(e_e_date),
                            pao_months=int(e_pao) if e_pao > 0 else None,
                            reminder_days=int(e_rem),
                            price=int(e_price),
                            notes=e_notes.strip() or None,
                        )
                        st.success("已更新產品資料！")
                        st.rerun()
        st.divider()
