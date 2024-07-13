from rest_framework import serializers

from apps.news.models import NewCategory


class NewCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCategory
        fields = ('id', 'name')
