import pytest
from model_bakery import baker

from test_fixtures.utils import set_obj_in_kwargs

__all__ = ['gun_mark_fixture']


@pytest.fixture()
def gun_mark_fixture(tank_fixture):
    def wrap(**kwargs):
        set_obj_in_kwargs(kwargs, 'tank', tank_fixture)
        return baker.make('marks.GunMark', **kwargs)
    return wrap
