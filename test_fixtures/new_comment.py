import pytest
from model_bakery import baker

from test_fixtures.utils import set_obj_in_kwargs

__all__ = ['new_comment_fixture']


@pytest.fixture()
def new_comment_fixture(new_fixture, user_fixture):
    def wrap(**kwargs):
        set_obj_in_kwargs(kwargs, 'new', new_fixture)
        set_obj_in_kwargs(kwargs, 'author', user_fixture)
        return baker.make('news.Comment', **kwargs)
    return wrap
