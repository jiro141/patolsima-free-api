from datetime import datetime, timedelta


def date_to_admin_readable(timestamp: datetime):
    if not timestamp:
        return "-"
    return timestamp.strftime("%Y-%m-%d %I:%M:%S %p")
