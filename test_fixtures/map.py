import pytest
from model_bakery import baker

__all__ = ['map_fixture']


@pytest.fixture()
def map_fixture():
    def wrap(**kwargs):
        return baker.make('directory.Map', **kwargs)
    return wrap
