from django_filters import rest_framework as filters

from apps.directory.models import Tank


class TankFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Tank
        fields = ('level', 'type', 'nation')
