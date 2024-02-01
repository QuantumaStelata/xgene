from rest_framework import mixins, permissions, viewsets

from apps.marks.api.v1.filters.mastery import MasteryFilter
from apps.marks.api.v1.serializers.mastery import MasterySerializer
from apps.marks.models import Mastery
from generic.paginations import LargeBasePagination


class MasteryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Mastery.objects.select_related('tank').all()
    serializer_class = MasterySerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = MasteryFilter
    pagination_class = LargeBasePagination
