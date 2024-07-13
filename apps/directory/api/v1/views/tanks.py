from rest_framework import mixins, permissions, viewsets

from apps.directory.api.v1.filters.tanks import TankFilter
from apps.directory.api.v1.serializers.tanks import TankSerializer
from apps.directory.models import Tank


class TankViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Tank.objects.all()
    serializer_class = TankSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = TankFilter
    pagination_class = None
