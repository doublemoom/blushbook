from datetime import datetime, date

def calculate_expiry_status(expiry_date_str):
    """
    計算美妝品剩餘效期與狀態（符合專案進階效期邏輯）
    """
    if not expiry_date_str:
        return {"status": "未知", "days_left": None, "color": "gray"}
    
    try:
        # 解析日期字串 (支援 YYYY-MM-DD)
        expiry_date = datetime.strptime(str(expiry_date_str).split()[0], "%Y-%m-%d").date()
        today = date.today()
        delta = (expiry_date - today).days
        
        if delta < 0:
            return {"status": "🔴 已過期", "days_left": delta, "color": "red"}
        elif delta <= 30:
            return {"status": "🟡 即將到期", "days_left": delta, "color": "orange"}
        else:
            return {"status": "🟢 使用中", "days_left": delta, "color": "green"}
    except Exception:
        return {"status": "⚪ 日期格式錯誤", "days_left": None, "color": "gray"}
