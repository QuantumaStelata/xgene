from rest_framework import mixins, permissions, viewsets

from apps.directory.api.v1.serializers.reserve_types import ReserveTypeSerializer
from apps.directory.models import ReserveType


class ReserveTypeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ReserveType.objects.all()
    serializer_class = ReserveTypeSerializer
    permission_classes = (permissions.AllowAny,)
