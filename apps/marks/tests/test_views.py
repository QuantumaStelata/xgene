import pytest

from test_fixtures.view_mixin import ViewMixin


@pytest.mark.django_db
class TestGunMarkView(ViewMixin):
    url = '/api/v1/marks/gun_marks/'
    model_fixture_name = 'gun_mark_fixture'
    list_action_enable = True


@pytest.mark.django_db
class TestMasteryView(ViewMixin):
    url = '/api/v1/marks/mastery/'
    model_fixture_name = 'mastery_fixture'
    list_action_enable = True
