from rest_framework import serializers

from cards.models import Card
from categories.models import Category


class CategoryForeignKey(serializers.PrimaryKeyRelatedField):
    def _get_user(self):
        """Try to retrieve the current user
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        return user

    def get_queryset(self):
        return Category.user_objects.all(self._get_user())


class CardSerializer(serializers.ModelSerializer):
    category = CategoryForeignKey()

    class Meta:
        model = Card
        fields = ('id', 'question', 'answer', 'hint', 'area', 'category', 'last_interaction')
        read_only_fields = ('id', 'last_interaction')
