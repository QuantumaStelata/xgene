import pytest
from faker import Faker

faker = Faker()


class ViewMixin:
    url: str = ''
    model_fixture_name: str = ''

    list_action_enable: bool = False
    retrieve_action_enable: bool = False
    update_action_enable: bool = False
    destroy_action_enable: bool = False
    create_action_enable: bool = False

    all_action_auth: bool = False
    list_action_auth: bool = False
    retrieve_action_auth: bool = False
    update_action_auth: bool = False
    destroy_action_auth: bool = False
    create_action_auth: bool = False

    @pytest.fixture
    def get_create_body(self):
        def wrap():
            return {}
        return wrap

    @pytest.fixture
    def get_update_body(self):
        def wrap():
            return {}
        return wrap

    def get_url(self, instance_id=None):
        if instance_id:
            return f'{self.url}{instance_id}/'
        return self.url

    def get_model_fixture_name(self):
        return self.model_fixture_name

    def create_fixture(self, model_fixture, many=False):
        if many:
            return [model_fixture() for _ in range(faker.random_int(2, 4))]

        return model_fixture()

    def test_list_action(self, request, unauthorized_api_client, api_client):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instances = self.create_fixture(model_fixture, many=True)

        client = unauthorized_api_client
        if self.list_action_auth or self.all_action_auth:
            client = api_client()

        url = self.get_url()
        r = client.get(url)

        if self.list_action_enable:
            assert r.status_code == 200
            if count := r.json().get('count'):
                assert count == len(instances)
        else:
            assert r.status_code in [404, 405]

    def test_retrieve_action(self, request, unauthorized_api_client, api_client):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instance = self.create_fixture(model_fixture)

        client = unauthorized_api_client
        if self.retrieve_action_auth or self.all_action_auth:
            client = api_client()

        url = self.get_url(instance.id)
        r = client.get(url)

        if self.retrieve_action_enable:
            assert r.status_code == 200
            assert r.json()['id'] == instance.id
        else:
            assert r.status_code in [404, 405]

    def test_update_action(self, request, unauthorized_api_client, api_client, get_update_body):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instance = self.create_fixture(model_fixture)

        client = unauthorized_api_client
        if self.update_action_auth or self.all_action_auth:
            client = api_client()

        url = self.get_url(instance.id)
        r = client.patch(url, data=get_update_body())

        if self.update_action_enable:
            assert r.status_code == 200
        else:
            assert r.status_code in [404, 405]

    def test_destroy_action(self, request, unauthorized_api_client, api_client):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instance = self.create_fixture(model_fixture)

        client = unauthorized_api_client
        if self.destroy_action_auth or self.all_action_auth:
            client = api_client()

        url = self.get_url(instance.id)
        r = client.delete(url)

        if self.destroy_action_enable:
            assert r.status_code == 204
        else:
            assert r.status_code in [404, 405]

    def test_create_action(self, unauthorized_api_client, api_client, get_create_body):
        client = unauthorized_api_client
        if self.create_action_auth or self.all_action_auth:
            client = api_client()

        url = self.get_url()
        r = client.post(url, data=get_create_body())

        if self.create_action_enable:
            assert r.status_code == 201
        else:
            assert r.status_code in [404, 405]
