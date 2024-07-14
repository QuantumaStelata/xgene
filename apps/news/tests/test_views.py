import pytest
from faker import Faker

from test_fixtures.view_mixin import ViewMixin

faker = Faker()


@pytest.mark.django_db
class TestCategoryView(ViewMixin):
    url = '/api/v1/news/categories/'
    model_fixture_name = 'new_category_fixture'

    list_action_enable = True
    retrieve_action_enable = True


@pytest.mark.django_db
class TestNewView(ViewMixin):
    url = '/api/v1/news/'
    model_fixture_name = 'new_fixture'

    list_action_enable = True
    retrieve_action_enable = True


@pytest.mark.django_db
class TestCommentView(ViewMixin):
    url = '/api/v1/news/%s/comments/'
    model_fixture_name = 'new_comment_fixture'
    nested_model_fixture_name = 'new_fixture'

    list_action_enable = True
    create_action_enable = True
    destroy_action_enable = True

    create_action_auth = True
    update_action_auth = True
    destroy_action_auth = True

    def get_url(self, request, instance=None):
        if instance:
            new_id = instance.new_id
        else:
            new_id = request.getfixturevalue(self.nested_model_fixture_name)().id
        self.url = self.url % new_id
        return super().get_url(request, instance)

    @pytest.fixture
    def get_create_body(self):
        def wrap():
            return {
                'text': faker.text(),
            }
        return wrap

    @pytest.fixture
    def get_user_for_requests(self):
        def wrap(action, instance=None):
            if instance:
                return instance.author
        return wrap
