from unittest.mock import patch

import pytest
from django.conf import settings

from apps.core.models import User
from apps.core.services.core import CoreService



@pytest.mark.django_db
def test_update_users(faker, user_fixture):
    users_count = faker.random_int(2, 4)
    user_fixture()  # Additional user, shoud be removed in service
    return_value = {
        'data': {
            str(settings.CLAN_ID): {
                'members': [
                    {
                        'account_name': faker.name(),
                        'role': faker.random_element(User.ROLE_MAP.keys()),
                        'account_id': faker.random_int(1000, 10000),
                    } for _ in range(users_count)
                ],
            },
        },
    }

    with patch('generic.services.requests.RequestService.get', return_value=return_value):
        users = CoreService.update_users()
        assert users_count == len(users)
        assert users_count == User.objects.all().count()


@pytest.mark.django_db
def test_update_user_access_tokens(faker, user_fixture):
    users = user_fixture(access_token=faker.md5, _quantity=faker.random_int(2, 4))
    users_without_access_token = user_fixture(_quantity=faker.random_int(2, 4))
    return_value = [
        (
            user, {
                'status': 'ok' if user.access_token else 'error',
                'data': {
                    'account_id': user.external_id,
                    'access_token': faker.md5(),
                },
            },
        ) for user in users + users_without_access_token
    ]

    for user, value in return_value:
        old_access_token = user.access_token

        with patch('generic.services.requests.RequestService.post', return_value=value):
            CoreService.update_user_access_token(user)
            if old_access_token:
                assert old_access_token != user.access_token
            else:
                assert old_access_token == user.access_token
                assert not hasattr(user, 'auth_token')
