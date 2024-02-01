from rest_framework import serializers

from apps.clan.models import Clan


class ClanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clan
        fields = ('id', 'tag', 'name', 'motto', 'color', 'emblem', 'external_id')
