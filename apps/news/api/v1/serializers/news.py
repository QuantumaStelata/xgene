from rest_framework import serializers

from apps.news.models import New


class NewSerializer(serializers.ModelSerializer):
    viewers_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = New
        fields = (
            'id', 'category', 'title', 'description', 'image', 'link', 'viewers_count',
            'publicated_at', 'external_id',
        )
