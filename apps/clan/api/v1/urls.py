from rest_framework.routers import SimpleRouter

from apps.clan.api.v1.views.clan import ClanViewSet
from apps.clan.api.v1.views.reserve import ReserveViewSet
from apps.clan.api.v1.views.stronghold import StrongholdViewSet
from generic.routers import WithoutLookUpRouter

router = SimpleRouter()
without_lookup_router = WithoutLookUpRouter()

router.register('reserves', ReserveViewSet)
without_lookup_router.register('', ClanViewSet)
without_lookup_router.register('stronghold', StrongholdViewSet)

urlpatterns = [

]

urlpatterns += router.urls
urlpatterns += without_lookup_router.urls
