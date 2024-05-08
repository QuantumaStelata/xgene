import pytest
from faker import Faker
from model_bakery import baker

from apps.directory.models import Role

__all__ = ['role_fixture', 'all_role_fixture']
faker = Faker()


@pytest.fixture()
def role_fixture():
    def wrap(**kwargs):
        role = faker.unique.random_element(tuple(zip(Role.PrimaryID.values, Role.ExternalID.values)))
        kwargs.setdefault('id', role[0])
        kwargs.setdefault('external_id', role[1])
        return baker.make('directory.Role', **kwargs)
    return wrap


@pytest.fixture()
def all_role_fixture():
    def wrap(**kwargs):
        kwargs.pop('external_id', None)
        kwargs.pop('_quantity', None)

        stronghold_build_types = []
        for role_id, external_id in zip(Role.PrimaryID, Role.ExternalID):
            stronghold_build_types.append(
                baker.make('directory.Role', id=role_id, external_id=external_id, **kwargs),
            )

        return stronghold_build_types
    return wrap
