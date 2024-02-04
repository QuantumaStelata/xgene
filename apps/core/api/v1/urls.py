from rest_framework.routers import SimpleRouter

from apps.core.api.v1.views.login import LoginViewSet
from apps.core.api.v1.views.users import UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet)
router.register('login', LoginViewSet)

urlpatterns = [

]

urlpatterns += router.urls
