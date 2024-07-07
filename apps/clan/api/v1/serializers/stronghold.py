from rest_framework import serializers

from apps.clan.models import Build, Stronghold


class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = ('stronghold', 'type', 'direction', 'position', 'level', 'map', 'reserve_type')


class StrongholdSerializer(serializers.ModelSerializer):
    builds = BuildSerializer(read_only=True, many=True)

    class Meta:
        model = Stronghold
        fields = ('level', 'map', 'builds')
