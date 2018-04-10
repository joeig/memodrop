from django.conf.urls import url

from braindump.views import BraindumpSession, BraindumpOK, BraindumpNOK, BraindumpIndex, BraindumpPostpone, \
    CardReset, CardExpedite, CardSetArea

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
    url(r'^card/(?P<card_pk>[0-9]+)/reset/$',
        CardReset.as_view(),
        name='card-reset'),
    url(r'^card/(?P<card_pk>[0-9]+)/expedite/$',
        CardExpedite.as_view(),
        name='card-expedite'),
    url(r'^card/(?P<card_pk>[0-9]+)/set-area/(?P<area>[1-6])/$',
        CardSetArea.as_view(),
        name='card-set-area'),
]
