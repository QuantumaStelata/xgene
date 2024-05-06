from unittest.mock import patch

import pytest
from django.conf import settings
from faker import Faker

from apps.clan.models import Build, Reserve, Stronghold
from apps.clan.services.clan import ClanService
from apps.clan.services.reserve import ReserveService
from apps.clan.services.stronghold import StrongholdService
from apps.directory.models import ReserveType
from apps.directory.services.reserve_types import ReserveTypeService

faker = Faker()


@pytest.mark.django_db
def test_update_clan():
    return_value = {
        'data': {
            str(settings.CLAN_ID): {
                'clan_id': str(settings.CLAN_ID),
                'tag': faker.name()[:5],
                'name': faker.name(),
                'motto': faker.name(),
                'color': faker.color(),
                'emblems': {
                    'x195': {
                        'portal': faker.image_url(placeholder_url='https://dummyimage.com/{width}x{height}'),
                    },
                },
            },
        },
    }

    with patch('generic.services.requests.RequestService.get', return_value=return_value):
        clan = ClanService.update_clan()
        assert clan
        assert clan.external_id
        assert str(clan.external_id) == str(settings.CLAN_ID)


@pytest.mark.django_db
def test_update_reserves(user_fixture):
    user_fixture(access_token=faker.md5())
    ReserveTypeService.update_reserve_types()

    reserves_count = faker.random_int(2, 4)
    return_value = {
        'data': [
            {
                'disposable': faker.pybool(),
                'type': faker.random_elements(ReserveType.ExternalID.values, unique=True, length=1)[0],
                'in_stock': [
                    {
                        'level': faker.random_int(1, 10),
                        'amount': faker.random_int(1, 10),
                        'activated_at': faker.unix_time(),
                        'active_till': faker.unix_time(),
                        'x_level_only': faker.pybool(),
                        'status': 'ready_to_activate',
                        'bonus_values': [
                            {
                                'value': faker.random_int(1, 10),
                            },
                            {
                                'value': faker.random_int(1, 10),
                            },
                        ],
                    },
                ],
            } for _ in range(reserves_count)
        ],
    }

    with patch('generic.services.requests.RequestService.get', return_value=return_value):
        ReserveService.update_reserves()
        assert reserves_count == Reserve.objects.all().count()


@pytest.mark.django_db
@patch('apps.clan.services.reserve.ReserveService.update_reserves')
def test_success_activate_reserve(update_reserves, user_fixture, reserve_fixture):
    user = user_fixture(access_token=faker.md5())
    reserve = reserve_fixture()

    return_value = {'status': 'ok'}

    with patch('generic.services.requests.RequestService.post', return_value=return_value):
        is_activated = ReserveService.activate_reserve(user, reserve)
        assert update_reserves.call_count == 1
        assert is_activated


@pytest.mark.django_db
@patch('apps.clan.services.reserve.ReserveService.update_reserves')
def test_fail_activate_reserve(update_reserves, user_fixture, reserve_fixture):
    user = user_fixture()
    reserve = reserve_fixture()

    return_value = {'status': 'error'}

    with patch('generic.services.requests.RequestService.post', return_value=return_value):
        is_activated = ReserveService.activate_reserve(user, reserve)
        assert update_reserves.call_count == 0
        assert not is_activated


@pytest.mark.django_db
def test_update_stronghold(clan_fixture):
    clan_fixture()
    build_count = 2
    return_value = {
        'data': {
            str(settings.CLAN_ID): {
                'clan_id': str(settings.CLAN_ID),
                'stronghold_level': faker.random_int(1, 10),
                'command_center_arena_id': faker.random_int(1, 10),
                'building_slots': [
                    {
                        'direction': faker.unique.random_element(Build.Direction),
                        'position': faker.unique.random_element(Build.Position),
                        'building_title': faker.unique.random_element(Build.Title),
                        'building_level': faker.random_int(1, 10),
                        'arena_id': faker.random_int(1, 10),
                        'reserve_title': faker.random_int(1, 10),
                    } for _ in range(build_count)
                ],
            },
        },
    }

    with patch('generic.services.requests.RequestService.get', return_value=return_value):
        StrongholdService.update_stronghold()
        assert Stronghold.objects.all().count() == 1
        assert Build.objects.all().count() == build_count
