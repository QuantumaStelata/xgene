from django.conf import settings

from generic.services.requests import RequestService


class WargamingRequestService(RequestService):
    host_domain = settings.WG_API_HOST
    params = {'application_id': settings.APPLICATION_ID}

    @classmethod
    def get(cls, url: str, headers: dict | None = None, max_retries: int = 1, **kwargs):
        return super().get(url, headers, max_retries, params=cls.params, **kwargs)

    @classmethod
    def post(cls, url: str, json: dict | None = None, headers: dict | None = None, max_retries: int = 1, **kwargs):
        return super().post(url, json, headers, max_retries, params=cls.params, **kwargs)
