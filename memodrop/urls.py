"""memodrop URL Configuration

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
import watchman.views
from django.conf.urls import url, include
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from rest_framework.authtoken import views as auth_token_views

urlpatterns = [
    url(r'^$',
        RedirectView.as_view(url=reverse_lazy('braindump-index'), permanent=False),
        name='index'),
    url(r'^auth/', include('authentication.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/health/$', watchman.views.bare_status),
    url(r'^api/(?P<version>(v1))/auth/', include('rest_framework.urls')),
    url(r'^api/(?P<version>(v1))/auth-token/', auth_token_views.obtain_auth_token),
    url(r'^api/(?P<version>(v1))/categories/', include('categories.urls.api')),
    url(r'^api/(?P<version>(v1))/cards/', include('cards.urls.api')),
    url(r'^braindump/', include('braindump.urls')),
    url(r'^cards/', include('cards.urls.gui')),
    url(r'^categories/', include('categories.urls.gui')),
]
