from rest_framework import serializers

from apps.directory.api.v1.serializers.tanks import TankSerializer
from apps.marks.models import GunMark


class GunMarkSerializer(serializers.ModelSerializer):
    tank = TankSerializer(read_only=True)

    class Meta:
        model = GunMark
        fields = (
            'tank', 'mark_20', 'mark_30', 'mark_40', 'mark_50',
            'mark_55', 'mark_60', 'mark_65', 'mark_70', 'mark_75',
            'mark_80', 'mark_85', 'mark_90', 'mark_95', 'mark_100',
        )
