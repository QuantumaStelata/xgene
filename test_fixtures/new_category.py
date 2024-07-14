import pytest
from model_bakery import baker

__all__ = ['new_category_fixture']


@pytest.fixture()
def new_category_fixture():
    def wrap(**kwargs):
        return baker.make('news.Category', **kwargs)
    return wrap
