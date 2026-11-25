import calendar
from datetime import date, datetime


def add_months(start_date, months):
    month_index = start_date.month - 1 + int(months)
    year = start_date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(start_date.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _parse_date(val):
    if val is None or val == "":
        return None
    if isinstance(val, date) and not isinstance(val, datetime):
        return val
    if isinstance(val, datetime):
        return val.date()
    try:
        return datetime.strptime(str(val).strip()[:10], "%Y-%m-%d").date()
    except ValueError:
        return None


def get_expiry_status(
    today=None,
    expiry_date=None,
    opened_date=None,
    pao_months=None,
    reminder_days=30,
):
    today_dt = _parse_date(today) or date.today()
    exp_dt = _parse_date(expiry_date)
    open_dt = _parse_date(opened_date)
    pao_int = int(pao_months) if pao_months not in (None, "", 0) else None
    rem_int = int(reminder_days) if reminder_days is not None else 30

    candidates = []
    if exp_dt is not None:
        candidates.append(exp_dt)
    if open_dt is not None and pao_int is not None and pao_int > 0:
        candidates.append(add_months(open_dt, pao_int))

    if not candidates:
        return {
            "status": "待確認",
            "days_remaining": None,
            "check_date": None,
        }

    check_date = min(candidates)
    days_remaining = (check_date - today_dt).days

    if days_remaining < 0:
        status = "已超過記錄期限"
    elif days_remaining <= rem_int:
        status = "即將到期"
    else:
        status = "期限內"

    return {
        "status": status,
        "days_remaining": days_remaining,
        "check_date": check_date.isoformat(),
    }
