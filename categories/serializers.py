from rest_framework import serializers

from cards.models import Card
from categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    cards = serializers.PrimaryKeyRelatedField(many=True, queryset=Card.objects.all())

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'mode', 'cards', 'last_interaction')
        read_only_fields = ('id', 'last_interaction')

    def create(self, validated_data):
        # Try to retrieve the current user:
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user

        validated_data['owner'] = user

        return super().create(validated_data)
