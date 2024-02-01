from rest_framework import mixins, permissions, viewsets

from apps.marks.api.v1.filters.gun_marks import GunMarkFilter
from apps.marks.api.v1.serializers.gun_marks import GunMarkSerializer
from apps.marks.models import GunMark
from generic.paginations import LargeBasePagination


class GunMarkViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = GunMark.objects.select_related('tank').all()
    serializer_class = GunMarkSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = GunMarkFilter
    pagination_class = LargeBasePagination
