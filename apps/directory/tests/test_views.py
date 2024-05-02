import pytest

from test_fixtures.view_mixin import ViewMixin


@pytest.mark.django_db
class TestMapView(ViewMixin):
    url = '/api/v1/directory/maps/'
    model_fixture_name = 'map_fixture'
    list_action_enable = True
    retrieve_action_enable = True


@pytest.mark.django_db
class TestReserveTypeView(ViewMixin):
    url = '/api/v1/directory/reserve_types/'
    model_fixture_name = 'reserve_type_fixture'
    list_action_enable = True


@pytest.mark.django_db
class TestTankView(ViewMixin):
    url = '/api/v1/directory/tanks/'
    model_fixture_name = 'tank_fixture'
    list_action_enable = True
    retrieve_action_enable = True
