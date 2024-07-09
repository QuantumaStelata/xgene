from rest_framework import serializers

from apps.clan.models import Reserve, ReserveScheduler
from apps.directory.models import ReserveType


class ReserveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveType
        fields = ('name', 'external_id')


class ReserveSchedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReserveScheduler
        fields = ('id', 'reserve', 'day', 'time')
        extra_kwargs = {'reserve': {'write_only': True}}


class ReserveSerializer(serializers.ModelSerializer):
    type = ReserveTypeSerializer(read_only=True)
    schedulers = ReserveSchedulerSerializer(read_only=True, many=True)

    class Meta:
        model = Reserve
        fields = ('id', 'type', 'level', 'schedulers')
