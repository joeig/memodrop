from django.conf.urls import url

from categories.views.gui import CategoryList, CategoryDetail, CategoryCreate, CategoryUpdate, CategoryDelete, braindump_index, \
    braindump_session, braindump_ok, braindump_nok

urlpatterns = [
    url(r'^$', CategoryList.as_view(), name='category-list'),
    url(r'^add/$', CategoryCreate.as_view(), name='category-create'),
    url(r'^(?P<pk>[0-9]+)/$', CategoryDetail.as_view(), name='category-detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', CategoryUpdate.as_view(), name='category-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', CategoryDelete.as_view(), name='category-delete'),
    url(r'^braindump/$', braindump_index, name='braindump-index'),
    url(r'^(?P<category_pk>[0-9]+)/braindump/$', braindump_session, name='braindump-session'),
    url(r'^(?P<category_pk>[0-9]+)/braindump/card/(?P<card_pk>[0-9]+)/ok$', braindump_ok, name='braindump-ok'),
    url(r'^(?P<category_pk>[0-9]+)/braindump/card/(?P<card_pk>[0-9]+)/nok$', braindump_nok, name='braindump-nok'),
]
