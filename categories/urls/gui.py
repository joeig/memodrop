from django.conf.urls import url

from categories.views.gui import CategoryList, CategoryDetail, CategoryCreate, CategoryUpdate, CategoryDelete

urlpatterns = [
    url(r'^$', CategoryList.as_view(), name='category-list'),
    url(r'^add/$', CategoryCreate.as_view(), name='category-create'),
    url(r'^(?P<pk>[0-9]+)/$', CategoryDetail.as_view(), name='category-detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', CategoryUpdate.as_view(), name='category-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', CategoryDelete.as_view(), name='category-delete'),
]
