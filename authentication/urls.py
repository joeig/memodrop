from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from authentication.views import PasswordChangeDoneView

urlpatterns = [
    url(r'^login/$',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='auth-login'),
    url(r'^logout/$',
        auth_views.logout_then_login,
        name='auth-logout'),
    url(r'^password-change/$',
        auth_views.PasswordChangeView.as_view(template_name='auth/password-change.html',
                                              success_url=reverse_lazy('auth-password-change-done')),
        name='auth-password-change'),
    url(r'^password-change/done/$',
        PasswordChangeDoneView.as_view(),
        name='auth-password-change-done'),
]
