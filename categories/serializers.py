from rest_framework import serializers
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    cards = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'mode', 'cards')
