from unittest.mock import patch

import pytest

from apps.directory.models import Map, ReserveType, StrongholdBuildType, Tank
from apps.directory.services.maps import MapService
from apps.directory.services.reserve_types import ReserveTypeService
from apps.directory.services.stronghold import StrongholdBuildTypeService
from apps.directory.services.tanks import TankService


@pytest.mark.django_db
def test_map_service():
    maps = MapService.update_maps()
    assert len(maps) == Map.objects.all().count()


@pytest.mark.django_db
def test_reserve_type_service():
    reserve_types = ReserveTypeService.update_reserve_types()
    assert len(reserve_types) == ReserveType.objects.all().count()


@pytest.mark.django_db
def test_stronghold_service():
    build_types = StrongholdBuildTypeService.update_build_types()
    assert len(build_types) == StrongholdBuildType.objects.all().count()


@pytest.mark.django_db
def test_tank_service(faker):
    tank_ids = [str(faker.random_int(1000, 10000)) for _ in range(faker.random_int(1, 3))]
    return_value = {
        'data': {
            tank_id: {
                'tank_id': tank_id,
                'external_id': faker.random_int(),
                'name': faker.name(),
                'tier': faker.random_int(1, 10),
                'type': faker.random_element(Tank.Type.names),
                'nation': faker.random_element(Tank.Nation.names),
                'images': {
                    'contour_icon': faker.image_url(placeholder_url='https://dummyimage.com/{width}x{height}'),
                },
            } for tank_id in tank_ids
        },
    }

    with patch('generic.services.requests.RequestService.get', return_value=return_value):
        TankService.update_tanks()
        assert len(tank_ids) == Tank.objects.all().count()
