from rest_framework import permissions, viewsets

from apps.news.api.v1.serializers.categories import NewCategorySerializer
from apps.news.models import NewCategory


class NewCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewCategory.objects.all()
    serializer_class = NewCategorySerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
