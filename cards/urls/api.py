from django.conf.urls import url

from cards.views.api import APICardList, APICardDetail


urlpatterns = [
    url(r'^$', APICardList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', APICardDetail.as_view()),
]
