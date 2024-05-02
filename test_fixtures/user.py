import pytest
from model_bakery import baker

__all__ = ['user_fixture']


@pytest.fixture()
def user_fixture():
    def wrap(**kwargs):
        password = kwargs.pop('password', None)
        user = baker.make('core.User', **kwargs)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user
    return wrap
