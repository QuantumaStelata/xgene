import pytest
from model_bakery import baker

from test_fixtures.utils import set_obj_in_kwargs

__all__ = ['build_fixture']


@pytest.fixture()
def build_fixture(stronghold_fixture, stronghold_build_type_fixture):
    def wrap(**kwargs):
        set_obj_in_kwargs(kwargs, 'stronghold', stronghold_fixture)
        set_obj_in_kwargs(kwargs, 'type', stronghold_build_type_fixture)
        return baker.make('clan.Build', **kwargs)
    return wrap
