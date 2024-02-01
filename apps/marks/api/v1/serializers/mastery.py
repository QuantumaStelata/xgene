from rest_framework import serializers

from apps.directory.api.v1.serializers.tanks import TankSerializer
from apps.marks.models import Mastery


class MasterySerializer(serializers.ModelSerializer):
    tank = TankSerializer(read_only=True)

    class Meta:
        model = Mastery
        fields = ('tank', 'class_3', 'class_2', 'class_1', 'master')
