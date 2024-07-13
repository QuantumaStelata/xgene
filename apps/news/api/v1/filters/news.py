from django_filters import rest_framework as filters

from generic.filters import NumberInFilter


class NewFilter(filters.FilterSet):
    category = NumberInFilter()
