from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from apps.news.api.v1.routers import NestedWithoutLookUpRouter
from apps.news.api.v1.views.categories import CategoryViewSet
from apps.news.api.v1.views.comments import CommentViewSet
from apps.news.api.v1.views.news import NewViewSet
from apps.news.api.v1.views.reactions import ReactionViewSet

router = SimpleRouter()

router.register('categories', CategoryViewSet)
router.register('', NewViewSet)

new_router_nested_without_lookup = NestedWithoutLookUpRouter(router, '', lookup='new')
new_router_nested_without_lookup.register('reactions', ReactionViewSet)

new_router_nested = NestedSimpleRouter(router, '', lookup='new')
new_router_nested.register('comments', CommentViewSet)

urlpatterns = []

urlpatterns += router.urls
urlpatterns += new_router_nested_without_lookup.urls
urlpatterns += new_router_nested.urls
