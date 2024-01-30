import json
from contextlib import suppress
from typing import NoReturn

from django.conf import settings
from requests import Response

from generic.services.requests import RequestService


class PoliroidRequestService(RequestService):
    host_domain = settings.POLIROID_API_HOST

    @classmethod
    def _post_process_response(cls, response: Response) -> dict | NoReturn:
        if response.ok:
            with suppress(json.decoder.JSONDecodeError):
                return response.json()
        cls._raise_connection_error()
