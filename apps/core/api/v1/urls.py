from rest_framework.routers import SimpleRouter

from apps.core.api.v1.views.users import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [

]

urlpatterns += router.urls
