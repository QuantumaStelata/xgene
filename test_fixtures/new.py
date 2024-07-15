import pytest
from model_bakery import baker

from test_fixtures.utils import set_obj_in_kwargs

__all__ = ['new_fixture']


@pytest.fixture()
def new_fixture(new_category_fixture):
    def wrap(**kwargs):
        set_obj_in_kwargs(kwargs, 'category', new_category_fixture)
        return baker.make('news.New', **kwargs)
    return wrap
