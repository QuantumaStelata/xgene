import pytest
from model_bakery import baker

__all__ = ['reserve_type_fixture']


@pytest.fixture()
def reserve_type_fixture(faker):
    def wrap(**kwargs):
        kwargs['external_id'] = faker.md5()
        return baker.make('directory.ReserveType', **kwargs)
    return wrap
