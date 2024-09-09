from datetime import datetime

from django.conf import settings


def unix_to_datetime(unix: int) -> datetime:
    return datetime.fromtimestamp(unix)


def concat_path_to_domain(path: str) -> str:
    domain = settings.DOMAIN.rstrip('/')
    path = path.lstrip('/')
    return f'{domain}/{path}'
