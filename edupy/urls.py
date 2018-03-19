"""edupy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from rest_framework.authtoken import views as auth_token_views

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('braindump-index'), permanent=False),
        name='index'),
    url(r'^auth/login/$',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='auth-login'),
    url(r'^auth/logout/$',
        auth_views.logout_then_login,
        name='auth-logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/auth/', include('rest_framework.urls')),
    url(r'^api/auth-token/', auth_token_views.obtain_auth_token),
    url(r'^api/categories/', include('categories.urls.api')),
    url(r'^api/cards/', include('cards.urls.api')),
    url(r'^braindump/', include('braindump.urls')),
    url(r'^cards/', include('cards.urls.gui')),
    url(r'^categories/', include('categories.urls.gui')),
]
