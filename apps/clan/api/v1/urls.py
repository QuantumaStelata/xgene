from apps.clan.api.v1.views.clan import ClanViewSet
from generic.routers import WithoutLookUpRouter

without_lookup_router = WithoutLookUpRouter()

without_lookup_router.register('', ClanViewSet)

urlpatterns = [

]

urlpatterns += without_lookup_router.urls
