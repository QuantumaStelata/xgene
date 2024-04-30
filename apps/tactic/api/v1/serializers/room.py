from rest_framework import serializers

from apps.core.api.v1.serializers.users import UserSerializer
from apps.tactic.models import Room


class RoomSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Room
        fields = ('uuid', 'map', 'author', 'created_at')
