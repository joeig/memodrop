from django.conf.urls import url

from categories.views.api import APICategoryList, APICategoryDetail


urlpatterns = [
    url(r'^$', APICategoryList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', APICategoryDetail.as_view()),
]
