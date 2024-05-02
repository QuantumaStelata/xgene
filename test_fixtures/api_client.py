import json

import pytest
from asgiref.sync import sync_to_async
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.test import APIClient

__all__ = ['api_client', 'unauthorized_api_client']


class _CustomAPIClient(APIClient):
    """
    Helper APIClient class

    As we use `rest_framework.parsers.JSONParser` only we need to make correct
    requests during test run:
        `content_type` should explicitly set to "application/json"
        `data should` properly encoded to JSON.
    """

    def get(self, path, data=None, follow=False, **extra):
        return super().get(path, data, follow, **extra)

    def post(self, path, data=None, format=None, content_type=None, follow=False, **extra):
        if format is None:
            content_type = 'application/json'

            if isinstance(data, (dict, list)):
                data = json.dumps(data, cls=DjangoJSONEncoder)
        response = super().post(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def put(self, path, data=None, format=None, content_type='application/json', follow=False, **extra):
        if isinstance(data, (dict, list)):
            data = json.dumps(data, cls=DjangoJSONEncoder)
        response = super().put(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def patch(self, path, data=None, format=None, content_type='application/json', follow=False, **extra):
        if isinstance(data, (dict, list)):
            data = json.dumps(data, cls=DjangoJSONEncoder)
        response = super().patch(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    def delete(self, path, data=None, format=None, content_type='application/json', follow=False, **extra):
        if isinstance(data, (dict, list)):
            data = json.dumps(data, cls=DjangoJSONEncoder)
        response = super().delete(path, data=data, format=format, content_type=content_type, follow=follow, **extra)
        return response

    aget = sync_to_async(get)
    apost = sync_to_async(post)
    aput = sync_to_async(put)
    apatch = sync_to_async(patch)
    adelete = sync_to_async(delete)


@pytest.fixture()
def unauthorized_api_client():
    return _CustomAPIClient()


@pytest.fixture()
def api_client(user_fixture):
    def _api_client(auth_user=None):
        if auth_user is None:
            auth_user = user_fixture()
        client = _CustomAPIClient()
        client.force_authenticate(auth_user)
        return client

    return _api_client
