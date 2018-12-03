from django.conf.urls import url

from authentication.views.api import UserGUISettingsDetails, UserGUISettingsDetailsWithDefaults

urlpatterns = [
    url(r'^settings/$',
        UserGUISettingsDetails.as_view(),
        name='api-authentication-settings'),
    url(r'^settings/with-defaults/$',
        UserGUISettingsDetailsWithDefaults.as_view(),
        name='api-authentication-settings-with-defaults'),
]
