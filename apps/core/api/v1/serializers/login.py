from rest_framework import serializers
from rest_framework.authtoken.models import Token


class OpenIdSerializer(serializers.Serializer):
    url = serializers.URLField()


class LoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    username = serializers.CharField()
    external_id = serializers.IntegerField()


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')
