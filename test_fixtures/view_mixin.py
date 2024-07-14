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

    @pytest.fixture
    def get_user_for_requests(self):
        def wrap(action, instance=None):
            return
        return wrap

    def get_url(self, request, instance=None):
        if instance:
            return f'{self.url}{instance.id}/'
        return self.url

    def get_model_fixture_name(self):
        return self.model_fixture_name

    def create_fixture(self, model_fixture, many=False):
        if many:
            return [model_fixture() for _ in range(faker.random_int(2, 4))]

        return model_fixture()

    def test_list_action(self, request, unauthorized_api_client, api_client, get_user_for_requests):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instances = self.create_fixture(model_fixture, many=True)

        client = unauthorized_api_client
        if self.list_action_auth or self.all_action_auth:
            auth_user = get_user_for_requests('list')
            client = api_client(auth_user=auth_user)

        url = self.get_url(request)
        r = client.get(url)
        self.assert_list_action(r, instances)

    def assert_list_action(self, response, instances):
        if self.list_action_enable:
            assert response.status_code == 200
            data = response.json()
            if isinstance(data, list):
                assert len(data) == len(instances)
            elif isinstance(data, dict):
                if count := response.json().get('count'):
                    assert count == len(instances)
        else:
            assert response.status_code in [404, 405]

    def test_retrieve_action(self, request, unauthorized_api_client, api_client, get_user_for_requests):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instance = self.create_fixture(model_fixture)

        client = unauthorized_api_client
        if self.retrieve_action_auth or self.all_action_auth:
            auth_user = get_user_for_requests('retrieve', instance)
            client = api_client(auth_user=auth_user)

        url = self.get_url(request, instance)
        r = client.get(url)
        self.assert_retrieve_action(r, instance)

    def assert_retrieve_action(self, response, instance):
        if self.retrieve_action_enable:
            assert response.status_code == 200
            assert response.json()['id'] == instance.id
        else:
            assert response.status_code in [404, 405]

    def test_update_action(self, request, unauthorized_api_client, api_client, get_update_body, get_user_for_requests):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instance = self.create_fixture(model_fixture)

        client = unauthorized_api_client
        if self.update_action_auth or self.all_action_auth:
            auth_user = get_user_for_requests('update', instance)
            client = api_client(auth_user=auth_user)

        url = self.get_url(request, instance)
        r = client.patch(url, data=get_update_body())
        self.assert_update_action(r)

    def assert_update_action(self, response):
        if self.update_action_enable:
            assert response.status_code == 200
        else:
            assert response.status_code in [404, 405]

    def test_destroy_action(self, request, unauthorized_api_client, api_client, get_user_for_requests):
        model_fixture = request.getfixturevalue(self.get_model_fixture_name())
        instance = self.create_fixture(model_fixture)

        client = unauthorized_api_client
        if self.destroy_action_auth or self.all_action_auth:
            auth_user = get_user_for_requests('destroy', instance)
            client = api_client(auth_user=auth_user)

        url = self.get_url(request, instance)
        r = client.delete(url)
        self.assert_destroy_action(r)

    def assert_destroy_action(self, response):
        if self.destroy_action_enable:
            assert response.status_code == 204
        else:
            assert response.status_code in [404, 405]

    def test_create_action(self, request, unauthorized_api_client, api_client, get_create_body, get_user_for_requests):
        client = unauthorized_api_client
        if self.create_action_auth or self.all_action_auth:
            auth_user = get_user_for_requests('create')
            client = api_client(auth_user=auth_user)

        url = self.get_url(request)
        r = client.post(url, data=get_create_body())
        self.assert_create_action(r)

    def assert_create_action(self, response):
        if self.create_action_enable:
            assert response.status_code == 201
        else:
            assert response.status_code in [404, 405]
