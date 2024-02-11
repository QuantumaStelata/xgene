from rest_framework import serializers

from apps.directory.models import ReserveType


class ReserveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveType
        fields = ('id', 'name', 'file')
