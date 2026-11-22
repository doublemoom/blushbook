import streamlit as st
from database import init_db
from product_service import get_all_products
from expiry_service import calculate_expiry_status

init_db()
st.title("⏳ 期限與提醒追蹤")

products = get_all_products(status="using")
if not products:
    st.info("目前沒有使用中的產品可供追蹤。")
else:
    for p in products:
        exp = p.get('expiry_date')
        reminder = p.get('reminder_days', 30)
        res = calculate_expiry_status(exp, reminder)

        status_icon = "🟢"
        status_text = "安全"
        if res["status"] == "expired":
            status_icon = "🔴"
            status_text = "已過期！"
        elif res["status"] == "warning":
            status_icon = "🟡"
            status_text = "即將到期"
        elif res["status"] == "unknown":
            status_icon = "⚪"
            status_text = "未設定期限"

        with st.expander(f"{status_icon} {p['name']} ({p['brand'] or '無品牌'}) - {status_text}"):
            st.write(f"**類別：** {p['category']}")
            st.write(f"**有效期限：** {exp or '未填寫'}")
            if res["days_left"] is not None:
                if res["days_left"] >= 0:
                    st.write(f"**距離到期還有：** {res['days_left']} 天")
                else:
                    st.write(f"**已過期：** {-res['days_left']} 天")


i love you
