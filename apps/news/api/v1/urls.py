from rest_framework.routers import SimpleRouter

from apps.news.api.v1.routers import NestedWithoutLookUpRouter
from apps.news.api.v1.views.categories import CategoryViewSet
from apps.news.api.v1.views.news import NewViewSet
from apps.news.api.v1.views.reactions import ReactionViewSet

router = SimpleRouter()

router.register('categories', CategoryViewSet)
router.register('', NewViewSet)

new_router = NestedWithoutLookUpRouter(router, '', lookup='new')
new_router.register('reactions', ReactionViewSet)

urlpatterns = []

urlpatterns += router.urls
urlpatterns += new_router.urls
