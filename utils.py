from datetime import datetime
import pytz

def ensure_tz_name(tz_name: str) -> str:
    try:
        pytz.timezone(tz_name)
        return tz_name
    except Exception:
        return "Asia/Kolkata"

def ist_to_utc(dt: datetime) -> datetime:
    """Converting naive IST datetime to UTC datetime (aware)."""
    ist = pytz.timezone("Asia/Kolkata")
    local_dt = ist.localize(dt)
    return local_dt.astimezone(pytz.utc)

def utc_iso_to_tz(dt: datetime, tz_name: str) -> str:
    """Converting UTC datetime object to given tz and return ISO string."""
    if dt is None:
        return None
    if isinstance(dt, str):  
        dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
    tz = pytz.timezone(tz_name)
    local_dt = dt.astimezone(tz)
    return local_dt.isoformat()
