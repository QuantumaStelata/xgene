import requests
from rest_framework.exceptions import APIException


class ConnectionRuntimeError(APIException):
    default_detail = 'Api connection error'


class RequestService:
    host_domain: str = ''
    is_authorization_in_headers_needed: bool = False
    authorization_header_name: str = None
    authorization_header_type: str = None
    success_status_codes = {200, 201, 204}
    timeout = 10

    @classmethod
    def get(cls, url: str, headers: dict | None = None, max_retries: int = 1, **kwargs):
        url = cls._get_url(url=url)
        headers = cls._generate_headers(headers=headers)
        try:
            response = requests.get(url=url, headers=headers, timeout=cls.timeout, **kwargs)
            return cls._post_process_response(response)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if 0 < max_retries - 1:
                return cls.get(url=url, headers=headers, max_retries=max_retries - 1, **kwargs)

        cls._raise_connection_error()

    @classmethod
    def post(cls, url: str, json: dict, headers: dict | None = None, max_retries: int = 1, **kwargs):
        url = cls._get_url(url=url)
        headers = cls._generate_headers(headers=headers)
        try:
            response = requests.post(url=url, json=json, headers=headers, timeout=cls.timeout, **kwargs)
            return cls._post_process_response(response)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if 0 < max_retries - 1:
                return cls.post(url=url, json=json, headers=headers, max_retries=max_retries - 1, **kwargs)

        cls._raise_connection_error()

    @classmethod
    def put(cls, url: str, json: dict, headers: dict | None = None, max_retries: int = 1, **kwargs):
        url = cls._get_url(url=url)
        headers = cls._generate_headers(headers=headers)
        try:
            response = requests.put(url=url, json=json, headers=headers, timeout=cls.timeout, **kwargs)
            return cls._post_process_response(response)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if 0 < max_retries - 1:
                return cls.put(url=url, json=json, headers=headers, max_retries=max_retries - 1, **kwargs)

        cls._raise_connection_error()

    @classmethod
    def patch(cls, url: str, json: dict, headers: dict | None = None, max_retries: int = 1, **kwargs):
        url = cls._get_url(url=url)
        headers = cls._generate_headers(headers=headers)
        try:
            response = requests.patch(url=url, json=json, headers=headers, timeout=cls.timeout, **kwargs)
            return cls._post_process_response(response)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if 0 < max_retries - 1:
                return cls.patch(url=url, json=json, headers=headers, max_retries=max_retries - 1, **kwargs)

        cls._raise_connection_error()

    @classmethod
    def delete(cls, url: str, headers: dict | None = None, max_retries: int = 1, **kwargs):
        url = cls._get_url(url=url)
        headers = cls._generate_headers(headers=headers)
        try:
            response = requests.delete(url=url, headers=headers, timeout=cls.timeout, **kwargs)
            return cls._post_process_response(response)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            if 0 < max_retries - 1:
                return cls.delete(url=url, headers=headers, max_retries=max_retries - 1, **kwargs)

        cls._raise_connection_error()

    @classmethod
    def _get_url(cls, url: str):
        if cls.host_domain in url:
            return url
        return f'{cls.host_domain}{url}' if url.startswith('/') else f'{cls.host_domain}/{url}'

    @classmethod
    def _generate_headers(cls, headers: dict | None = None) -> dict:
        if isinstance(headers, dict) and not headers:
            return headers
        if not headers:
            headers = {}
        if not cls.is_authorization_in_headers_needed:
            return headers
        if cls.authorization_header_name not in headers:
            headers[f'{cls.authorization_header_name}'] = (
                f'{cls.authorization_header_type} {cls._generate_token()}'
                if cls.authorization_header_type
                else f'{cls._generate_token()}'
            )
        return headers

    @classmethod
    def _generate_token(cls) -> str:
        return ''

    @staticmethod
    def _raise_connection_error():
        raise ConnectionRuntimeError

    @classmethod
    def _post_process_response(cls, response: requests.Response) -> requests.Response:
        return response
