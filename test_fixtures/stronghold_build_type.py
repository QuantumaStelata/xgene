import pytest
from faker import Faker
from model_bakery import baker

from apps.directory.models import StrongholdBuildType

__all__ = ['stronghold_build_type_fixture', 'all_stronghold_build_type_fixture']
faker = Faker()


@pytest.fixture()
def stronghold_build_type_fixture():
    def wrap(**kwargs):
        kwargs.setdefault('external_id', faker.unique.random_element(tuple(StrongholdBuildType.ExternalID.values)))
        return baker.make('directory.StrongholdBuildType', **kwargs)
    return wrap


@pytest.fixture()
def all_stronghold_build_type_fixture():
    def wrap(**kwargs):
        kwargs.pop('external_id', None)
        kwargs.pop('_quantity', None)

        stronghold_build_types = []
        for external_id in StrongholdBuildType.ExternalID:
            stronghold_build_types.append(
                baker.make('directory.StrongholdBuildType', external_id=external_id, **kwargs),
            )

        return stronghold_build_types
    return wrap
