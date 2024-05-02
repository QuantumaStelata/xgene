from unittest.mock import patch

import pytest

from test_fixtures.view_mixin import ViewMixin


@pytest.mark.django_db
class TestLoginView(ViewMixin):
    url = '/api/v1/core/login/'
    model_fixture_name = 'user_fixture'

    def test_openid_action(self, unauthorized_api_client):
        url = f'{self.url}openid/'
        r = unauthorized_api_client.get(url)

        assert r.status_code == 200
        assert r.json()['url']

    def test_login_action(self, unauthorized_api_client, user_fixture, faker):
        url = f'{self.url}login/'
        user = user_fixture(access_token=faker.md5(), external_id=faker.random_int(1, 10000))

        data = {
            'access_token': user.access_token,
            'username': user.username,
            'external_id': user.external_id,
        }
        return_value = {
            'status': 'ok',
            'data': {
                'account_id': user.external_id,
                'access_token': user.access_token,
            },
        }

        with patch('generic.services.requests.RequestService.post', return_value=return_value):
            r = unauthorized_api_client.post(url, data=data)
            response = r.json()
            assert r.status_code == 200
            assert response['key'] and response['user']


@pytest.mark.django_db
class TestUsersView(ViewMixin):
    url = '/api/v1/core/users/'
    model_fixture_name = 'user_fixture'
    list_action_enable = True
    retrieve_action_enable = True

    @pytest.mark.parametrize(['client_fixture_name', 'status'], [['unauthorized_api_client', 401], ['api_client', 200]])
    def test_me_action(self, request, client_fixture_name, status):
        client = request.getfixturevalue(client_fixture_name)
        if client_fixture_name == 'api_client':
            client = client()

        url = f'{self.url}me/'
        r = client.get(url)
        assert r.status_code == status
