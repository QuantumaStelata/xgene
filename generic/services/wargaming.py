import json
from contextlib import suppress
from typing import NoReturn

from django.conf import settings
from requests import Response

from generic.services.requests import RequestService


class WargamingRequestService(RequestService):
    host_domain = settings.WG_API_HOST

    @classmethod
    def get(cls, url: str, headers: dict | None = None, max_retries: int = 1, **kwargs):
        params = kwargs.pop('params', {})
        params.setdefault('application_id', settings.APPLICATION_ID)
        return super().get(url, headers, max_retries, params=params, **kwargs)

    @classmethod
    def post(cls, url: str, json: dict | None = None, headers: dict | None = None, max_retries: int = 1, **kwargs):
        params = kwargs.pop('params', {})
        params.setdefault('application_id', settings.APPLICATION_ID)
        return super().post(url, json, headers, max_retries, params=params, **kwargs)

    @classmethod
    def _post_process_response(cls, response: Response) -> dict | NoReturn:
        if response.ok:
            with suppress(json.decoder.JSONDecodeError):
                return response.json()
        cls._raise_connection_error()
