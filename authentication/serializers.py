from rest_framework import serializers

from authentication.models import UserGUISettings


class UserGUISettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGUISettings
        fields = ('enable_markdown_editor',)
