import pytest
from model_bakery import baker

from test_fixtures.utils import set_obj_in_kwargs

__all__ = ['stronghold_fixture']


@pytest.fixture()
def stronghold_fixture(clan_fixture):
    def wrap(**kwargs):
        set_obj_in_kwargs(kwargs, 'clan', clan_fixture)
        return baker.make('clan.Stronghold', **kwargs)
    return wrap
