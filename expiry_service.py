from datetime import datetime, date

def calculate_expiry_status(expiry_date_str, reminder_days=30):
    """
    計算美妝品剩餘效期與狀態（支援 reminder_days 參數以防錯亂）
    """
    if not expiry_date_str:
        return {"status": "unknown", "days_left": None, "color": "gray"}

    try:
        # 解析日期字串 (支援 YYYY-MM-DD)
        expiry_date = datetime.strptime(str(expiry_date_str).split()[0], "%Y-%m-%d").date()
        today = date.today()
        delta = (expiry_date - today).days

        if delta < 0:
            return {"status": "expired", "days_left": delta, "color": "red"}
        elif delta <= reminder_days:
            return {"status": "warning", "days_left": delta, "color": "orange"}
        else:
            return {"status": "safe", "days_left": delta, "color": "green"}
    except Exception:
        return {"status": "unknown", "days_left": None, "color": "gray"}
