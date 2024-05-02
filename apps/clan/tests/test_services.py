from unittest.mock import patch

import pytest
from django.conf import settings

from apps.clan.models import Reserve
from apps.clan.services.clan import ClanService
from apps.clan.services.reserve import ReserveService
from apps.directory.models import ReserveType
from apps.directory.services.reserve_types import ReserveTypeService


@pytest.mark.django_db
def test_update_clan(faker):
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
def test_update_reserves(faker, user_fixture):
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
