from rest_framework import serializers

from apps.clan.models import Reserve


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = (
            'id', 'type', 'level', 'count', 'clan_bonus',
            'random_bonus', 'activated_at', 'active_till',
            'disposable', 'ready_to_activate', 'x_level_only',
        )
