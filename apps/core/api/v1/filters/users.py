from django_filters import rest_framework as filters

from apps.core.models import User


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ('role',)

    ordering = filters.OrderingFilter(
        fields=(('battles', 'battles'), ('wins_percent', 'wins_percent'), ('wn8', 'wn8')),
    )
