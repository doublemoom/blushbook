# --- 2. 期限追蹤 ---
from datetime import date
import streamlit as st

from database import init_db
from expiry_service import get_expiry_status
from product_service import get_all_products

st.set_page_config(page_title="期限追蹤", page_icon="⏳", layout="wide")
init_db()

# --- 2. 期限追蹤 ---
st.subheader("⏳ 期限與提醒追蹤")
st.caption("依據標示有效期限與「開封日期 + PAO 月數」中最早的日期，由系統每日重新計算。")
status_filter = st.selectbox(
    "篩選期限狀態",
    ["全部", "即將到期", "已超過記錄期限", "期限內", "待確認"],
)

using_products = get_all_products("using")

if not using_products:
    st.info("目前沒有使用中的產品可供追蹤。")
else:
    for p in using_products:
        info = get_expiry_status(
            today=date.today(),
            expiry_date=p.get("expiry_date"),
            opened_date=p.get("opened_date"),
            pao_months=p.get("pao_months"),
            reminder_days=p.get("reminder_days") or 30,
        )
        if status_filter != "全部" and info["status"] != status_filter:
            continue

        badge_map = {
            "已超過記錄期限": "🔴",
            "即將到期": "🟡",
            "期限內": "🟢",
            "待確認": "⚪",
        }
        icon = badge_map.get(info["status"], "⚪")

        with st.expander(f"{icon} {p['name']} — {info['status']}"):
            st.write(
                f"**品牌 / 類別 / 色號：** {p['brand'] or '未填寫'} / {p['category']} / {p['shade'] or '未填寫'}"
            )
            st.write(f"**記錄的標示有效期限：** {p.get('expiry_date') or '未填寫'}")
            st.write(
                f"**開封日期 / PAO 月數：** {p.get('opened_date') or '未填寫'} / {p.get('pao_months') or '無'}"
            )
            st.write(f"**計算依據日期：** {info['check_date'] or '無'}")
            if info["days_remaining"] is not None:
                if info["days_remaining"] >= 0:
                    st.write(f"**距離記錄期限剩餘：** {info['days_remaining']} 天")
                else:
                    st.write(f"**已超過記錄期限：** {-info['days_remaining']} 天")

