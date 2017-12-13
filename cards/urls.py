from django.conf.urls import url
from .views import CardCreate, CardDelete, CardDetail, CardList, CardUpdate, card_reset, card_set_area

urlpatterns = [
    url(r'^$', CardList.as_view(), name='card-list'),
    url(r'^add/$', CardCreate.as_view(), name='card-create'),
    url(r'^(?P<pk>[0-9]+)/$', CardDetail.as_view(), name='card-detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', CardUpdate.as_view(), name='card-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', CardDelete.as_view(), name='card-delete'),
    url(r'^(?P<pk>[0-9]+)/reset/$', card_reset, name='card-reset'),
    url(r'^(?P<pk>[0-9]+)/set-area/(?P<area>[1-6])/$', card_set_area, name='card-set-area'),
]
