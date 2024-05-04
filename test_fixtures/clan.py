import pytest
from django.conf import settings
from model_bakery import baker

__all__ = ['clan_fixture']


@pytest.fixture()
def clan_fixture(tank_fixture):
    def wrap(**kwargs):
        kwargs.setdefault('external_id', settings.CLAN_ID)
        return baker.make('clan.Clan', **kwargs)
    return wrap
