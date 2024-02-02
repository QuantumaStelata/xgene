from rest_framework.routers import SimpleRouter

from apps.directory.api.v1.views.maps import MapViewSet
from apps.directory.api.v1.views.tanks import TankViewSet

router = SimpleRouter()
router.register('maps', MapViewSet)
router.register('tanks', TankViewSet)

urlpatterns = [

]

urlpatterns += router.urls
