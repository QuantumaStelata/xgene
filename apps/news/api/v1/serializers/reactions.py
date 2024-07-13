from rest_framework import serializers

from apps.core.models import User
from apps.news.models import Reaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class ReactionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Reaction
        fields = ('type', 'author', 'modified_at')
        read_only_fields = ('author', 'modified_at')
