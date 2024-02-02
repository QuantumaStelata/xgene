from rest_framework import mixins, permissions, viewsets

from apps.directory.api.v1.filters.maps import MapFilter
from apps.directory.api.v1.serializers.maps import MapSerializer
from apps.directory.models import Map


class MapViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = MapFilter
