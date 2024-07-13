from rest_framework.routers import SimpleRouter

from apps.news.api.v1.views.categories import NewCategoryViewSet
from apps.news.api.v1.views.news import NewViewSet

router = SimpleRouter()

router.register('categories', NewCategoryViewSet)
router.register('', NewViewSet)

urlpatterns = []

urlpatterns += router.urls
