from django_filters import rest_framework as filters

from apps.marks.models import Mastery


class MasteryFilter(filters.FilterSet):
    tank__name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Mastery
        fields = ('tank__level', 'tank__nation', 'tank__type')

    ordering = filters.OrderingFilter(
        fields=(
            ('tank__name', 'tank__name'),
            ('class_3', 'class_3'),
            ('class_2', 'class_2'),
            ('class_1', 'class_1'),
            ('master', 'master'),
        ),
    )
