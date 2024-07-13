from rest_framework import permissions, viewsets

from apps.news.api.v1.filters.news import NewFilter
from apps.news.api.v1.serializers.news import NewSerializer
from apps.news.models import New


class NewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = (permissions.AllowAny,)
    filterset_class = NewFilter
