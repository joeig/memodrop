from django.conf.urls import url

from categories.views.gui import CategoryList, CategoryDetail, CategoryCreate, CategoryUpdate, CategoryDelete
from categories.views.share_contract_gui import CategoryShareContractList, CategoryShareContractRevoke, \
    CategoryShareContractAccept, CategoryShareContractRequest

urlpatterns = [
    url(r'^$', CategoryList.as_view(), name='category-list'),
    url(r'^add/$', CategoryCreate.as_view(), name='category-create'),
    url(r'^(?P<pk>[0-9]+)/$', CategoryDetail.as_view(), name='category-detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', CategoryUpdate.as_view(), name='category-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', CategoryDelete.as_view(), name='category-delete'),
    url(r'^(?P<pk>[0-9]+)/shares/$', CategoryShareContractList.as_view(), name='category-share-contract-list'),
    url(r'^(?P<pk>[0-9]+)/shares/request/$',
        CategoryShareContractRequest.as_view(),
        name='category-share-contract-request'),
    url(r'^(?P<pk>[0-9]+)/shares/(?P<share_contract_pk>[0-9]+)/revoke/$',
        CategoryShareContractRevoke.as_view(),
        name='category-share-contract-revoke'),
    url(r'^shares/(?P<share_contract_pk>[0-9]+)/accept/$',
        CategoryShareContractAccept.as_view(),
        name='category-share-contract-accept'),
]
