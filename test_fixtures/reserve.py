import pytest
from model_bakery import baker

from test_fixtures.utils import set_obj_in_kwargs

__all__ = ['reserve_fixture', 'reserve_scheduler_fixture']


@pytest.fixture()
def reserve_fixture(reserve_type_fixture):
    def wrap(**kwargs):
        set_obj_in_kwargs(kwargs, 'type', reserve_type_fixture)
        return baker.make('clan.Reserve', **kwargs)
    return wrap


@pytest.fixture()
def reserve_scheduler_fixture(reserve_fixture):
    def wrap(**kwargs):
        if 'reserve' not in kwargs and 'reserve_id' not in kwargs:
            kwargs['reserve'] = reserve_fixture(disposable=False)
        return baker.make('clan.ReserveScheduler', author=None, **kwargs)
    return wrap
