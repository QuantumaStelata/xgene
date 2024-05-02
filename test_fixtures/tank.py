import pytest
from model_bakery import baker

__all__ = ['tank_fixture']


@pytest.fixture()
def tank_fixture():
    def wrap(**kwargs):
        return baker.make('directory.Tank', **kwargs)
    return wrap
