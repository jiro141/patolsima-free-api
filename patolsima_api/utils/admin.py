from datetime import datetime, timedelta


def date_to_admin_readable(timestamp: datetime):
    return timestamp.strftime("%Y-%m-%d %I:%M:S %p")
