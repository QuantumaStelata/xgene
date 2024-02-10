from rest_framework import serializers

from apps.clan.models import Build, Stronghold


class BuildSerializer(serializers.ModelSerializer):
    title_ru = serializers.SerializerMethodField()

    class Meta:
        model = Build
        fields = ('stronghold', 'title', 'title_ru', 'direction', 'position', 'level', 'map', 'reserve_type')

    def get_title_ru(self, instance: Build):
        return dict(Build.Title.choices)[instance.title]


class StrongholdSerializer(serializers.ModelSerializer):
    builds = BuildSerializer(read_only=True, many=True)

    class Meta:
        model = Stronghold
        fields = ('level', 'map', 'builds')
