from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from authentication.views.gui import PasswordChangeDoneView, ProfileView, UserGUISettingsUpdate

urlpatterns = [
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='authentication-login'),
    url(r'^logout/$',
        auth_views.logout_then_login,
        name='authentication-logout'),
    url(r'^password-change/$',
        auth_views.PasswordChangeView.as_view(template_name='auth/password-change.html',
                                              success_url=reverse_lazy('authentication-password-change-done')),
        name='authentication-password-change'),
    url(r'^password-change/done/$',
        PasswordChangeDoneView.as_view(),
        name='authentication-password-change-done'),
    url(r'^profile/$',
        ProfileView.as_view(),
        name='authentication-profile'),
    url(r'^settings/$',
        UserGUISettingsUpdate.as_view(),
        name='authentication-user-gui-settings-update'),
]
