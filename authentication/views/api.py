from django.conf import settings
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from authentication.models import UserGUISettings
from authentication.serializers import UserGUISettingsSerializer


class UserGUISettingsDetails(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserGUISettingsSerializer

    def get_object(self):
        return get_object_or_404(UserGUISettings, user=self.request.user)


class UserGUISettingsDetailsWithDefaults(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserGUISettingsSerializer

    def get_object(self):
        normalized_object = get_object_or_404(UserGUISettings, user=self.request.user)
        # Replace None values with system-wide default values:
        for key, value in settings.USER_GUI_SETTINGS_DEFAULTS.items():
            if normalized_object.__getattribute__(key) is None:
                normalized_object.__setattr__(key, value)
        return normalized_object
