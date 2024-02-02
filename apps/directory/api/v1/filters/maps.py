from django_filters import rest_framework as filters


class MapFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
