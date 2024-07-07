from rest_framework import serializers

from apps.directory.models import StrongholdBuildType


class StrongholdBuildTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrongholdBuildType
        fields = ('id', 'name')
