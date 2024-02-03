from datetime import datetime


def unix_to_datetime(unix: int) -> datetime:
    return datetime.utcfromtimestamp(unix)
