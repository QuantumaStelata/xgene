from apps.clan.api.v1.views.clan import ClanViewSet
from apps.clan.api.v1.views.stronghold import StrongholdViewSet
from generic.routers import WithoutLookUpRouter

without_lookup_router = WithoutLookUpRouter()

without_lookup_router.register('', ClanViewSet)
without_lookup_router.register('stronghold', StrongholdViewSet)

urlpatterns = [

]

urlpatterns += without_lookup_router.urls
