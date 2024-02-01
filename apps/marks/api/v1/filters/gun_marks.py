from django_filters import rest_framework as filters

from apps.marks.models import GunMark


class GunMarkFilter(filters.FilterSet):
    tank__name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = GunMark
        fields = ('tank__level', 'tank__nation', 'tank__type')

    ordering = filters.OrderingFilter(
        fields=(
            ('tank__name', 'tank__name'),
            ('mark_20', 'mark_20'),
            ('mark_30', 'mark_30'),
            ('mark_40', 'mark_40'),
            ('mark_50', 'mark_50'),
            ('mark_55', 'mark_55'),
            ('mark_60', 'mark_60'),
            ('mark_65', 'mark_65'),
            ('mark_70', 'mark_70'),
            ('mark_75', 'mark_75'),
            ('mark_80', 'mark_80'),
            ('mark_85', 'mark_85'),
            ('mark_90', 'mark_90'),
            ('mark_95', 'mark_95'),
            ('mark_100', 'mark_100'),
        ),
    )
