from django.conf.urls import url

from braindump.views import BraindumpSession, BraindumpOK, BraindumpNOK, BraindumpIndex, BraindumpPostpone

urlpatterns = [
    url(r'^$',
        BraindumpIndex.as_view(),
        name='braindump-index'),
    url(r'^category/(?P<category_pk>[0-9]+)/$',
        BraindumpSession.as_view(),
        name='braindump-session'),
    url(r'^category/(?P<category_pk>[0-9]+)/card/(?P<card_pk>[0-9]+)/ok$',
        BraindumpOK.as_view(),
        name='braindump-ok'),
    url(r'^category/(?P<category_pk>[0-9]+)/card/(?P<card_pk>[0-9]+)/nok$',
        BraindumpNOK.as_view(),
        name='braindump-nok'),
    url(r'^category/(?P<category_pk>[0-9]+)/card/(?P<card_pk>[0-9]+)/postpone/(?P<seconds>[0-9]+)$',
        BraindumpPostpone.as_view(),
        name='braindump-postpone'),
]
