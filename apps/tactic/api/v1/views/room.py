from rest_framework import viewsets

from apps.tactic.api.v1.permissions.room import RoomPermission
from apps.tactic.api.v1.serializers.room import RoomSerializer
from apps.tactic.models import Room


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (RoomPermission,)
    lookup_field = 'uuid'
