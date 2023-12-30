import requests

from django.conf import settings


class WGAPI:
    @classmethod
    def post(cls, url: str, **kwargs) -> dict | None:
        kwargs['application_id'] = settings.APPLICATION_ID
        response = requests.post(f'{settings.WG_API_HOST}{url}', data=kwargs)
        return response.json() if response.ok else None
