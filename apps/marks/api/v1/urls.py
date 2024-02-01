from rest_framework.routers import SimpleRouter

from apps.marks.api.v1.views.gun_marks import GunMarkViewSet
from apps.marks.api.v1.views.mastery import MasteryViewSet

router = SimpleRouter()
router.register('gun_marks', GunMarkViewSet)
router.register('mastery', MasteryViewSet)

urlpatterns = [

]

urlpatterns += router.urls
