from rest_framework import serializers

from apps.core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'role', 'external_id', 'credits', 'bonds', 'gold', 'free_xp', 'battles', 'wins', 'draws',
            'losses', 'max_damage', 'max_frags', 'max_xp', 'frags', 'spotted', 'dropped_capture_points', 'damage_dealt',
            'damage_received', 'shots', 'hits', 'max_damage_tank_id', 'max_frags_tank_id', 'max_xp_tank_id', 'wn8',
            'wins_percent', 'hits_percent',
        )
