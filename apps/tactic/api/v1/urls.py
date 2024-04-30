from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.tactic.api.v1.consumers.tactic import TacticConsumer
from apps.tactic.api.v1.views.room import RoomViewSet

router = SimpleRouter()
router.register('rooms', RoomViewSet)

urlpatterns = [

]

urlpatterns += router.urls

websocket_urlpatterns = [
    path('<uuid:room_uuid>/', TacticConsumer.as_asgi()),
]
