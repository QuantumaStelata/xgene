from unittest.mock import patch

import pytest

from apps.marks.models import GunMark, Mastery
from apps.marks.services.marks import MarkService


@pytest.mark.django_db
def test_gun_mark_service(faker, tank_fixture):
    tanks = tank_fixture(_quantity=faker.random_int(1, 3))
    return_value = {
        'data': [
            {
                'id': tank.id,
                'marks': {
                    str(key): faker.random_int(100, 10000) for key in range(20, 110, 10)
                },
            } for tank in tanks
        ],
    }

    with patch('generic.services.requests.RequestService.get', return_value=return_value):
        gun_marks = MarkService.update_gun_marks()
        assert len(gun_marks) == GunMark.objects.all().count()


@pytest.mark.django_db
def test_mastery_service(faker, tank_fixture):
    tanks = tank_fixture(_quantity=faker.random_int(1, 3))
    return_value = {
        'data': [
            {
                'id': tank.id,
                'mastery': [faker.random_int(100, 2000) for _ in range(4)],
            } for tank in tanks
        ],
    }

    with patch('generic.services.requests.RequestService.get', return_value=return_value):
        masteries = MarkService.update_mastery()
        assert len(masteries) == Mastery.objects.all().count()
