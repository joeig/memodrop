from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cards.serializers import CardSerializer
from cards.views.gui import CardBelongsUserMixin


class APICardList(CardBelongsUserMixin, generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer


class APICardDetail(CardBelongsUserMixin, generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CardSerializer
