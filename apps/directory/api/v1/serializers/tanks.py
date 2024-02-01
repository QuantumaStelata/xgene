from rest_framework import serializers

from apps.directory.models import Tank


class TankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = ('id', 'name', 'level', 'type', 'nation', 'contour', 'external_id')
