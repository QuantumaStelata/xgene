from rest_framework import serializers

from apps.directory.models import Map


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ('id', 'name', 'file', 'external_id')
