import pytest
from model_bakery import baker

from test_fixtures.utils import set_obj_in_kwargs

__all__ = ['mastery_fixture']


@pytest.fixture()
def mastery_fixture(tank_fixture):
    def wrap(**kwargs):
        set_obj_in_kwargs(kwargs, 'tank', tank_fixture)
        return baker.make('marks.Mastery', **kwargs)
    return wrap
