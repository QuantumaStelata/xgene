from rest_framework import serializers

from apps.clan.models import Build, Stronghold
from apps.directory.models import StrongholdBuildType


class StrongholdBuildTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrongholdBuildType
        fields = ('id', 'name', 'external_id')


class BuildSerializer(serializers.ModelSerializer):
    type = StrongholdBuildTypeSerializer()

    class Meta:
        model = Build
        fields = ('stronghold', 'type', 'direction', 'position', 'level', 'map', 'reserve_type')


class StrongholdSerializer(serializers.ModelSerializer):
    builds = BuildSerializer(read_only=True, many=True)

    class Meta:
        model = Stronghold
        fields = ('level', 'map', 'builds')
