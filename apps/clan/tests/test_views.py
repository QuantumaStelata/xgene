from unittest.mock import patch

import pytest
from faker import Faker

from apps.directory.models import Role
from test_fixtures.view_mixin import ViewMixin

faker = Faker()


@pytest.mark.django_db
class TestClanView(ViewMixin):
    url = '/api/v1/clan/'
    model_fixture_name = 'clan_fixture'
    list_action_enable = True

    def create_fixture(self, model_fixture, many=False):
        return model_fixture()


@pytest.mark.django_db
class TestReserveView(ViewMixin):
    url = '/api/v1/clan/reserves/'
    model_fixture_name = 'reserve_fixture'
    list_action_enable = True
    all_action_auth = True

    @pytest.mark.parametrize(
        ['user_kwargs', 'expected_response'],
        [
            (
                {'access_token': faker.md5(), 'role_id': role_id},
                role_id in (Role.PrimaryID.COMMANDER, Role.PrimaryID.EXECUTIVE_OFFICER),
            ) for role_id in Role.PrimaryID.values
        ] + [
            (
                {'access_token': '', 'role_id': role_id}, False,
            ) for role_id in Role.PrimaryID.values
        ],
    )
    @patch('apps.clan.services.reserve.ReserveService.update_reserves')
    def test_activate_action(
        self, mocked, user_fixture, all_role_fixture, reserve_fixture,
        api_client, user_kwargs, expected_response,
    ):
        all_role_fixture()
        user = user_fixture(**user_kwargs)
        reserve = reserve_fixture()
        return_value = {'status': 'ok'}

        with patch('generic.services.requests.RequestService.post', return_value=return_value):
            client = api_client(user)
            r = client.get(f'/api/v1/clan/reserves/{reserve.id}/activate/')

        if expected_response:
            assert r.status_code == 200
            assert r.json()['activated'] == expected_response
        else:
            assert r.status_code == 403

    @pytest.mark.parametrize(
        ['user_kwargs', 'expected_response'],
        [
            (
                {'access_token': faker.md5(), 'role_id': role_id},
                role_id in (Role.PrimaryID.COMMANDER, Role.PrimaryID.EXECUTIVE_OFFICER),
            ) for role_id in Role.PrimaryID.values
        ] + [
            (
                {'access_token': '', 'role_id': role_id}, False,
            ) for role_id in Role.PrimaryID.values
        ],
    )
    def test_can_activate_action(self, user_fixture, all_role_fixture, api_client, user_kwargs, expected_response):
        all_role_fixture()
        user = user_fixture(**user_kwargs)
        client = api_client(user)
        r = client.get('/api/v1/clan/reserves/can_activate/')
        assert r.status_code == 200 if expected_response else 403


@pytest.mark.django_db
class TestStrongholdView(ViewMixin):
    url = '/api/v1/clan/stronghold/'
    model_fixture_name = 'stronghold_fixture'
    list_action_enable = True

    def create_fixture(self, model_fixture, many=False):
        return model_fixture()
