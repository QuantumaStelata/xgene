from rest_framework import permissions, viewsets

from apps.news.api.v1.serializers.categories import CategorySerializer
from apps.news.models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
