from rest_framework import serializers

from apps.news.models import New


class NewSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = ('id', 'category', 'title', 'description', 'image', 'link', 'pub_date', 'external_id')
